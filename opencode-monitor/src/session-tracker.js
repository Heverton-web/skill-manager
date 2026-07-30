export class SessionTracker {
  constructor() {
    this.state = {
      sessionId: null,
      totalTokens: 0,
      totalCost: 0,
      inputTokens: 0,
      outputTokens: 0,
      cacheRead: 0,
      cacheWrite: 0,
      toolCount: 0,
      messageCount: 0,
      activeTools: [],
      tokensPerSecond: 0,
      lastModel: null,
      contextLimit: { input: 0, output: 0 },
      contextUsed: 0,
      sessionStatus: "idle",
      startTime: null,
      lastActivity: null,
    }
  }

  getState() {
    return { ...this.state, activeTools: [...this.state.activeTools] }
  }

  processEvent(event) {
    this.state.lastActivity = Date.now()
    if (!this.state.startTime) this.state.startTime = Date.now()

    switch (event.type) {
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
      this.state.totalTokens = this.state.inputTokens + this.state.outputTokens + this.state.cacheRead + this.state.cacheWrite

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
        input: model.limit.context || 0,
        output: model.limit.output || 0,
      }
    }
  }

  _handleToolBefore(event) {
    this.state.toolCount++
    this.state.activeTools.push({
      tool: event.properties?.tool,
      callID: event.properties?.callID,
      startTime: Date.now(),
    })
  }

  _handleToolAfter(event) {
    const callID = event.properties?.callID
    this.state.activeTools = this.state.activeTools.filter(t => t.callID !== callID)
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
