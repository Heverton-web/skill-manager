import { describe, it, beforeEach } from "node:test"
import assert from "node:assert"
import { SessionTracker } from "../src/session-tracker.js"

describe("SessionTracker", () => {
  let tracker

  beforeEach(() => {
    tracker = new SessionTracker()
  })

  it("initialize with default state", () => {
    const state = tracker.getState()
    assert.strictEqual(state.sessionId, null)
    assert.strictEqual(state.totalTokens, 0)
    assert.strictEqual(state.totalCost, 0)
    assert.strictEqual(state.toolCount, 0)
    assert.strictEqual(state.messageCount, 0)
    assert.deepStrictEqual(state.contextLimit, { input: 0, output: 0 })
  })

  it("track message.updated with tokens and cost", () => {
    tracker.processEvent({
      type: "message.updated",
      properties: {
        info: {
          id: "msg-1",
          sessionID: "sess-1",
          role: "assistant",
          modelID: "claude-sonnet-4-20250514",
          providerID: "anthropic",
          cost: 0.015,
          tokens: { input: 1000, output: 500, reasoning: 0, cache: { read: 0, write: 0 } },
          time: { created: Date.now() }
        }
      }
    })

    const state = tracker.getState()
    assert.strictEqual(state.sessionId, "sess-1")
    assert.strictEqual(state.totalTokens, 1500)
    assert.strictEqual(state.totalCost, 0.015)
    assert.strictEqual(state.messageCount, 1)
    assert.strictEqual(state.lastModel, "anthropic/claude-sonnet-4-20250514")
  })

  it("track tool.execute.before", () => {
    tracker.processEvent({
      type: "tool.execute.before",
      properties: { tool: "bash", sessionID: "sess-1", callID: "call-1" }
    })

    const state = tracker.getState()
    assert.strictEqual(state.toolCount, 1)
    assert.strictEqual(state.activeTools.length, 1)
    assert.strictEqual(state.activeTools[0].tool, "bash")
  })

  it("track tool.execute.after removes from active", () => {
    tracker.processEvent({
      type: "tool.execute.before",
      properties: { tool: "bash", sessionID: "sess-1", callID: "call-1" }
    })
    tracker.processEvent({
      type: "tool.execute.after",
      properties: { tool: "bash", sessionID: "sess-1", callID: "call-1", title: "ls", output: "file.txt" }
    })

    const state = tracker.getState()
    assert.strictEqual(state.activeTools.length, 0)
  })

  it("compute tokens per second", () => {
    const now = Date.now()
    tracker.processEvent({
      type: "message.updated",
      properties: {
        info: {
          id: "msg-1",
          sessionID: "sess-1",
          role: "assistant",
          cost: 0.01,
          tokens: { input: 1000, output: 2000, reasoning: 0, cache: { read: 0, write: 0 } },
          time: { created: now - 5000, completed: now }
        }
      }
    })

    const state = tracker.getState()
    assert.ok(state.tokensPerSecond > 0)
    assert.ok(Math.abs(state.tokensPerSecond - 400) < 10)
  })

  it("track context limit from model info", () => {
    tracker.processEvent({
      type: "message.updated",
      properties: {
        info: {
          id: "msg-1",
          sessionID: "sess-1",
          role: "assistant",
          cost: 0,
          tokens: { input: 500, output: 100, reasoning: 0, cache: { read: 0, write: 0 } },
          time: { created: Date.now() }
        },
        model: {
          id: "claude-sonnet-4-20250514",
          limit: { context: 200000, output: 8192 }
        }
      }
    })

    const state = tracker.getState()
    assert.strictEqual(state.contextLimit.input, 200000)
    assert.strictEqual(state.contextLimit.output, 8192)
  })

  it("track session.status events", () => {
    tracker.processEvent({
      type: "session.status",
      properties: { sessionID: "sess-1", status: { type: "busy" } }
    })
    assert.strictEqual(tracker.getState().sessionStatus, "busy")

    tracker.processEvent({
      type: "session.status",
      properties: { sessionID: "sess-1", status: { type: "idle" } }
    })
    assert.strictEqual(tracker.getState().sessionStatus, "idle")
  })

  it("updateFromAPISession sets tokens and model from API data", () => {
    tracker.updateFromAPISession({
      id: "ses_abc123",
      agent: "build",
      model: { id: "mimo-v2.5-free", providerID: "opencode", variant: "default" },
      cost: 0.042,
      tokens: {
        input: 254145,
        output: 38076,
        reasoning: 6209,
        cache: { read: 11028480, write: 0 }
      },
      time: { created: 1785450753889, updated: 1785452784142 }
    })

    const state = tracker.getState()
    assert.strictEqual(state.sessionId, "ses_abc123")
    assert.strictEqual(state.agent, "build")
    assert.strictEqual(state.lastModel, "opencode/mimo-v2.5-free")
    assert.strictEqual(state.totalCost, 0.042)
    assert.strictEqual(state.inputTokens, 254145)
    assert.strictEqual(state.outputTokens, 38076)
    assert.strictEqual(state.reasoningTokens, 6209)
    assert.strictEqual(state.cacheRead, 11028480)
    assert.strictEqual(state.totalTokens, 254145 + 38076 + 6209)
    assert.strictEqual(state.contextUsed, 254145)
  })

  it("track chat.message event", () => {
    tracker.processEvent({
      type: "chat.message",
      properties: {
        sessionID: "sess-2",
        agent: "build",
        model: { id: "mimo-v2.5-free", providerID: "opencode" },
        parts: [{ type: "text", text: "hello" }]
      }
    })

    const state = tracker.getState()
    assert.strictEqual(state.sessionId, "sess-2")
    assert.strictEqual(state.agent, "build")
    assert.strictEqual(state.messageCount, 1)
    assert.strictEqual(state.lastModel, "opencode/mimo-v2.5-free")
  })
})
