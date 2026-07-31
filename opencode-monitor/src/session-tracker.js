const MODEL_LIMITS = {
  "mimo-v2.5-free": { input: 1000000, output: 32000 },
  "mimo-v2-pro": { input: 1000000, output: 32000 },
  "claude-sonnet-4-20250514": { input: 200000, output: 8192 },
  "claude-opus-4-20250514": { input: 200000, output: 8192 },
  "claude-haiku-3.5": { input: 200000, output: 8192 },
  "gpt-4o": { input: 128000, output: 16384 },
  "gpt-4-turbo": { input: 128000, output: 4096 },
  "gemini-2.5-pro": { input: 1000000, output: 65536 },
  "gemini-2.5-flash": { input: 1000000, output: 65536 },
}

export class SessionTracker {
  constructor() {
    this.state = {
      sessionId: null,
      agent: null,
      totalTokens: 0,
      totalCost: 0,
      inputTokens: 0,
      outputTokens: 0,
      reasoningTokens: 0,
      cacheRead: 0,
      cacheWrite: 0,
      toolCount: 0,
      messageCount: 0,
      activeTools: [],
      usedTools: [],
      tokensPerSecond: 0,
      lastModel: null,
      contextLimit: { input: 0, output: 0 },
      contextUsed: 0,
      sessionStatus: "idle",
      startTime: null,
      lastActivity: null,
      lastUpdateTime: null,
      sessionInputTokens: 0,
      sessionOutputTokens: 0,
      sessionReasoningTokens: 0,
      sessionCost: 0,
      allSessionsTokens: 0,
    }
  }

  getState() {
    return { ...this.state, activeTools: [...this.state.activeTools] }
  }

  updateFromAPISession(session) {
    this.state.sessionId = session.id || this.state.sessionId
    this.state.agent = session.agent || this.state.agent
    this.state.lastUpdateTime = Date.now()

    if (session.model) {
      const providerID = session.model.providerID || ""
      const modelID = session.model.id || ""
      this.state.lastModel = providerID && modelID ? `${providerID}/${modelID}` : modelID || this.state.lastModel

      if (session.model.limit) {
        this.state.contextLimit = {
          input: session.model.limit.context || this.state.contextLimit.input || 200000,
          output: session.model.limit.output || this.state.contextLimit.output || 8192,
        }
      } else if (modelID && MODEL_LIMITS[modelID]) {
        this.state.contextLimit = { ...MODEL_LIMITS[modelID] }
      } else if (this.state.contextLimit.input === 0) {
        this.state.contextLimit = { input: 200000, output: 8192 }
      }
    }

    if (session.tokens) {
      this.state.sessionInputTokens = session.tokens.input || 0
      this.state.sessionOutputTokens = session.tokens.output || 0
      this.state.sessionReasoningTokens = session.tokens.reasoning || 0

      this.state.inputTokens = this.state.sessionInputTokens
      this.state.outputTokens = this.state.sessionOutputTokens
      this.state.reasoningTokens = this.state.sessionReasoningTokens
      this.state.cacheRead = session.tokens.cache?.read || 0
      this.state.cacheWrite = session.tokens.cache?.write || 0

      this.state.totalTokens =
        this.state.inputTokens +
        this.state.outputTokens +
        this.state.reasoningTokens

      this.state.contextUsed = this.state.inputTokens
    }

    if (typeof session.cost === "number") {
      this.state.sessionCost = session.cost
      this.state.totalCost = session.cost
    }

    if (session.time?.created) {
      this.state.startTime = session.time.created
    }
  }

  updateFromAllSessions(sessions) {
    let total = 0
    let totalInput = 0
    let totalOutput = 0
    let totalReasoning = 0
    let totalCost = 0

    for (const s of sessions) {
      if (s.tokens) {
        totalInput += s.tokens.input || 0
        totalOutput += s.tokens.output || 0
        totalReasoning += s.tokens.reasoning || 0
      }
      if (typeof s.cost === "number") {
        totalCost += s.cost
      }
    }

    total = totalInput + totalOutput + totalReasoning
    this.state.allSessionsTokens = total
  }

  processEvent(event) {
    this.state.lastActivity = Date.now()
    if (!this.state.startTime) this.state.startTime = Date.now()

    switch (event.type) {
      case "chat.message":
        this._handleChatMessage(event)
        break
      case "message.updated":
        this._handleMessageUpdated(event)
        break
      case "tool.execute.before":
        this._handleToolBefore(event)
        break
      case "tool.execute.after":
        this._handleToolAfter(event)
        break
      case "session.status":
        this._handleSessionStatus(event)
        break
      case "session.compacted":
        this._handleSessionCompacted()
        break
    }
  }

  _handleChatMessage(event) {
    this.state.sessionId = event.properties?.sessionID || this.state.sessionId
    this.state.agent = event.properties?.agent || this.state.agent
    this.state.messageCount++

    if (event.properties?.model) {
      const m = event.properties.model
      if (m.id) this.state.lastModel = `${m.providerID || "unknown"}/${m.id}`
    }
  }

  _handleMessageUpdated(event) {
    const info = event.properties?.info
    if (!info) return

    this.state.sessionId = info.sessionID || this.state.sessionId
    this.state.messageCount++

    if (info.role === "assistant") {
      this.state.totalCost += info.cost || 0
      const tokens = info.tokens || {}
      this.state.inputTokens += tokens.input || 0
      this.state.outputTokens += tokens.output || 0
      this.state.cacheRead += tokens.cache?.read || 0
      this.state.cacheWrite += tokens.cache?.write || 0
      this.state.totalTokens =
        this.state.inputTokens +
        this.state.outputTokens +
        this.state.cacheRead +
        this.state.cacheWrite

      if (info.providerID && info.modelID) {
        this.state.lastModel = `${info.providerID}/${info.modelID}`
      }

      if (info.time?.created && info.time?.completed) {
        const duration = (info.time.completed - info.time.created) / 1000
        if (duration > 0) {
          this.state.tokensPerSecond = Math.round((tokens.output || 0) / duration)
        }
      }

      this.state.contextUsed = this.state.inputTokens
    }

    const model = event.properties?.model
    if (model?.limit) {
      this.state.contextLimit = {
        input: model.limit.context || 200000,
        output: model.limit.output || 8192,
      }
    }
  }

  _handleToolBefore(event) {
    this.state.toolCount++
    const tool = event.properties?.tool
    this.state.activeTools.push({
      tool,
      callID: event.properties?.callID,
      startTime: Date.now(),
    })
    if (tool && !this.state.usedTools.includes(tool)) {
      this.state.usedTools.push(tool)
    }
  }

  _handleToolAfter(event) {
    const callID = event.properties?.callID
    this.state.activeTools = this.state.activeTools.filter((t) => t.callID !== callID)
  }

  _handleSessionStatus(event) {
    const status = event.properties?.status
    if (status?.type) {
      this.state.sessionStatus = status.type
    }
  }

  _handleSessionCompacted() {
    this.state.contextUsed = 0
    this.state.inputTokens = 0
    this.state.outputTokens = 0
  }
}
