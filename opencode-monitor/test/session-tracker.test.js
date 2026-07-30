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
})
