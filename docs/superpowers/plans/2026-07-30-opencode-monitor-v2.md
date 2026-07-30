# OpenCode Monitor V2 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform OpenCode Monitor from a passive event viewer into an active debugging dashboard with context window visibility, tool control, cost tracking, and grouped timeline.

**Architecture:** Extend the existing SSE-based monitor to consume richer OpenCode SDK events, compute derived metrics (cost, tokens/s, context usage), and expose session actions (compact, clear, summarize) via API proxy to the OpenCode server. Frontend gets a context bar, tools panel, cost stats, and grouped-by-input timeline.

**Tech Stack:** Node.js 18+ (vanilla), SSE, HTML/CSS/JS (no build tools), OpenCode SDK REST API for session actions.

---

## File Structure

```
opencode-monitor/
├── src/
│   ├── cli.js              # Entry point (minor: add OPENCODE_URL config)
│   ├── server.js            # HTTP server + SSE + NEW: API proxy routes
│   ├── session-tracker.js   # NEW: tracks session state (tokens, cost, tools)
│   ├── event-logger.js      # Unchanged
│   └── plugin.js            # Unchanged
├── public/
│   ├── index.html           # Major rewrite: new layout with context bar + tools panel
│   └── app.js               # NEW: extracted JS (was inline, now separate file)
├── test/
│   ├── server.test.js       # Update for new routes
│   └── session-tracker.test.js  # NEW
└── package.json
```

---

## Task 1: Session Tracker — State Management

**Files:**
- Create: `opencode-monitor/src/session-tracker.js`
- Create: `opencode-monitor/test/session-tracker.test.js`

- [ ] **Step 1: Write the failing test for SessionTracker**

```javascript
// test/session-tracker.test.js
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
    assert.deepStrictEqual(state.activeTools, [{ tool: "bash", callID: "call-1", startTime: Date.now() }])
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
    tracker.processEvent({
      type: "message.updated",
      properties: {
        info: {
          id: "msg-1",
          sessionID: "sess-1",
          role: "assistant",
          cost: 0.01,
          tokens: { input: 1000, output: 2000, reasoning: 0, cache: { read: 0, write: 0 } },
          time: { created: Date.now() - 5000, completed: Date.now() }
        }
      }
    })

    const state = tracker.getState()
    assert.ok(state.tokensPerSecond > 0)
    assert.ok(Math.abs(state.tokensPerSecond - 600) < 10) // ~600 t/s
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd opencode-monitor && node --test test/session-tracker.test.js`
Expected: FAIL with "Cannot find module '../src/session-tracker.js'"

- [ ] **Step 3: Implement SessionTracker**

```javascript
// src/session-tracker.js
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
    return { ...this.state }
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
        this._handleSessionCompacted(event)
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

      // Tokens per second from completion time
      if (info.time?.created && info.time?.completed) {
        const duration = (info.time.completed - info.time.created) / 1000
        if (duration > 0) {
          this.state.tokensPerSecond = Math.round((tokens.output || 0) / duration)
        }
      }

      // Context usage (input tokens approximate context usage)
      this.state.contextUsed = this.state.inputTokens
    }

    // Model limits from event properties
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
    // Reset context tracking after compaction
    this.state.contextUsed = 0
    this.state.inputTokens = 0
    this.state.outputTokens = 0
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd opencode-monitor && node --test test/session-tracker.test.js`
Expected: PASS (7 tests)

- [ ] **Step 5: Commit**

```bash
git add opencode-monitor/src/session-tracker.js opencode-monitor/test/session-tracker.test.js
git commit -m "feat: add SessionTracker for token/cost/context state"
```

---

## Task 2: Server API Proxy Routes

**Files:**
- Modify: `opencode-monitor/src/server.js` (add proxy routes)
- Modify: `opencode-monitor/test/server.test.js` (add tests)

- [ ] **Step 1: Write failing tests for new routes**

```javascript
// Add to test/server.test.js

it("GET /api/session-status retorna estado do tracker", () => {
  const server = new MonitorServer(9997, "127.0.0.1")
  server.start()

  return new Promise((resolve) => {
    import("http").then(({ get }) => {
      get("http://127.0.0.1:9997/api/session-status", (res) => {
        let data = ""
        res.on("data", (chunk) => { data += chunk })
        res.on("end", () => {
          const body = JSON.parse(data)
          assert.ok("sessionId" in body)
          assert.ok("totalTokens" in body)
          assert.ok("totalCost" in body)
          assert.ok("contextLimit" in body)
          server.stop()
          resolve()
        })
      })
    })
  })
})

it("POST /api/compact retorna 200", () => {
  const server = new MonitorServer(9996, "127.0.0.1")
  server.start()

  return new Promise((resolve) => {
    import("http").then(({ request }) => {
      const req = request("http://127.0.0.1:9996/api/compact", { method: "POST" }, (res) => {
        assert.ok(res.statusCode === 200 || res.statusCode === 502)
        server.stop()
        resolve()
      })
      req.end()
    })
  })
})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd opencode-monitor && node --test test/server.test.js`
Expected: FAIL on new tests (routes don't exist yet)

- [ ] **Step 3: Add proxy routes to server.js**

Add to `server.js` constructor:
```javascript
constructor(port = 7777, host = "localhost", openCodeUrl = "http://localhost:4096") {
  // ... existing code ...
  this.openCodeUrl = process.env.OPENCODE_URL || openCodeUrl
  this.sessionTracker = new SessionTracker()
}
```

Add import at top:
```javascript
import { SessionTracker } from "./session-tracker.js"
```

Add route handlers inside the server callback, after existing routes:
```javascript
if (req.url === "/api/session-status" && req.method === "GET") {
  res.writeHead(200, { "Content-Type": "application/json" })
  res.end(JSON.stringify(this.sessionTracker.getState()))
  return
}

if (req.url === "/api/tools" && req.method === "GET") {
  this._proxyToOpenCode(req, res, "/agent")
  return
}

if (req.url === "/api/mcp" && req.method === "GET") {
  this._proxyToOpenCode(req, res, "/mcp")
  return
}

if (req.url === "/api/compact" && req.method === "POST") {
  const sessionId = this.sessionTracker.getState().sessionId
  if (!sessionId) {
    res.writeHead(400, { "Content-Type": "application/json" })
    res.end(JSON.stringify({ error: "No active session" }))
    return
  }
  this._proxyToOpenCode(req, res, `/session/${sessionId}/compact`)
  return
}

if (req.url === "/api/clear" && req.method === "POST") {
  // /clear = create new session via command
  const sessionId = this.sessionTracker.getState().sessionId
  if (!sessionId) {
    res.writeHead(400, { "Content-Type": "application/json" })
    res.end(JSON.stringify({ error: "No active session" }))
    return
  }
  this._proxyToOpenCode(req, res, `/session/${sessionId}/command`, {
    method: "POST",
    body: JSON.stringify({ command: "clear", arguments: "", agent: "build" })
  })
  return
}

if (req.url === "/api/summarize" && req.method === "POST") {
  const sessionId = this.sessionTracker.getState().sessionId
  if (!sessionId) {
    res.writeHead(400, { "Content-Type": "application/json" })
    res.end(JSON.stringify({ error: "No active session" }))
    return
  }
  this._proxyToOpenCode(req, res, `/session/${sessionId}/summarize`)
  return
}
```

Add proxy method:
```javascript
async _proxyToOpenCode(req, res, path, options = {}) {
  try {
    const url = new URL(path, this.openCodeUrl)
    const fetchOptions = {
      method: options.method || req.method,
      headers: { "Content-Type": "application/json" },
    }
    if (options.body) fetchOptions.body = options.body

    const response = await fetch(url.toString(), fetchOptions)
    const data = await response.text()

    res.writeHead(response.status, { "Content-Type": "application/json" })
    res.end(data)
  } catch (err) {
    res.writeHead(502, { "Content-Type": "application/json" })
    res.end(JSON.stringify({ error: "OpenCode server unreachable", detail: err.message }))
  }
}
```

Update `broadcast()` to also feed events to session tracker:
```javascript
broadcast(event) {
  this.sessionTracker.processEvent(event)
  const data = JSON.stringify(event)
  for (const client of this.clients) {
    client.write(`data: ${data}\n\n`)
  }
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd opencode-monitor && node --test test/server.test.js`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add opencode-monitor/src/server.js opencode-monitor/test/server.test.js
git commit -m "feat: add API proxy routes for session actions and status"
```

---

## Task 3: Update Plugin to Capture Richer Events

**Files:**
- Modify: `opencode-monitor/src/plugin.js`

- [ ] **Step 1: Update plugin.js with additional hooks**

Replace the existing `plugin.js` with:

```javascript
import { appendFileSync, mkdirSync, existsSync } from "fs"
import { join, dirname } from "path"
import { fileURLToPath } from "url"
import { randomUUID } from "crypto"

const __dirname = dirname(fileURLToPath(import.meta.url))
const DEFAULT_DIR = join(__dirname, "..", "data")

export function createMonitorHook(eventFilePath, onEvent) {
  const dataDir = eventFilePath
    ? dirname(eventFilePath)
    : DEFAULT_DIR

  if (!existsSync(dataDir)) {
    mkdirSync(dataDir, { recursive: true })
  }

  const sessionId = randomUUID()
  const logFile = eventFilePath || join(dataDir, `session-${sessionId}.jsonl`)

  function emit(type, payload = {}) {
    const event = {
      id: randomUUID(),
      type,
      sessionId,
      timestamp: Date.now(),
      ...payload,
    }
    appendFileSync(logFile, JSON.stringify(event) + "\n")

    if (typeof onEvent === "function") {
      try {
        onEvent(event)
      } catch (err) {
        console.error("Erro no callback onEvent:", err.message)
      }
    }
  }

  return {
    name: "opencode-monitor",
    hooks: {
      "chat.message": async (input, output) => {
        emit("chat.message", {
          sessionID: input.sessionID,
          agent: input.agent,
          model: input.model,
          messageID: input.messageID,
          parts: output.parts?.map(p => ({
            type: p.type,
            text: p.type === "text" ? p.text?.slice(0, 500) : undefined,
            tool: p.type === "tool" ? p.tool : undefined,
          })),
        })
      },

      "tool.execute.before": async (input, output) => {
        emit("tool.execute.before", {
          tool: input.tool,
          sessionID: input.sessionID,
          callID: input.callID,
          args: output.args,
        })
      },

      "tool.execute.after": async (input, output) => {
        emit("tool.execute.after", {
          tool: input.tool,
          sessionID: input.sessionID,
          callID: input.callID,
          args: input.args,
          title: output.title,
          output: output.output?.slice(0, 1000),
          metadata: output.metadata,
        })
      },

      "command.execute.before": async (input, output) => {
        emit("command.execute.before", {
          command: input.command,
          sessionID: input.sessionID,
          arguments: input.arguments,
          parts: output.parts,
        })
      },

      "experimental.session.compacting": async (input, output) => {
        emit("session.compacting", {
          sessionID: input.sessionID,
          context: output.context,
        })
      },

      event: async (input) => {
        const evt = input.event
        // Capture session lifecycle events
        if (evt.type === "session.created" || evt.type === "session.updated" ||
            evt.type === "session.idle" || evt.type === "session.compacted" ||
            evt.type === "session.error" || evt.type === "session.status") {
          emit(evt.type, evt.properties)
        }
        // Capture message updates for cost/tokens
        if (evt.type === "message.updated") {
          emit("message.updated", { info: evt.properties?.info })
        }
        if (evt.type === "message.part.updated") {
          emit("message.part.updated", {
            part: evt.properties?.part,
            delta: evt.properties?.delta,
          })
        }
      },
    },
  }
}
```

- [ ] **Step 2: Test plugin loads without errors**

Run: `cd opencode-monitor && node -e "import('./src/plugin.js').then(m => { const h = m.createMonitorHook(); console.log('Hooks:', Object.keys(h.hooks)); })"`
Expected: Output showing all hook names

- [ ] **Step 3: Commit**

```bash
git add opencode-monitor/src/plugin.js
git commit -m "feat: extend plugin hooks for richer event capture"
```

---

## Task 4: Dashboard HTML — Context Bar + Cost Stats

**Files:**
- Modify: `opencode-monitor/public/index.html` (major layout change)

- [ ] **Step 1: Rewrite index.html with new layout**

Replace the entire `index.html` with the following. Key changes:
- New context bar below header (progress bar + tokens + cost + t/s)
- Quick actions panel (compact, clear, summarize buttons)
- Stats row updated with cost, tokens, model info
- Timeline section restructured for grouping (Task 5)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OpenCode Monitor</title>
  <link rel="stylesheet" href="app.css">
</head>
<body>
  <header>
    <h1>OpenCode Monitor</h1>
    <div class="status">
      <div class="dot" id="statusDot"></div>
      <span id="statusText">Desconectado</span>
    </div>
  </header>

  <main>
    <!-- Context Window Bar -->
    <section class="context-bar" id="contextBar">
      <div class="context-header">
        <span class="context-label">Context Window</span>
        <span class="context-model" id="contextModel">—</span>
      </div>
      <div class="context-progress">
        <div class="context-track">
          <div class="context-fill" id="contextFill" style="width: 0%"></div>
        </div>
        <span class="context-text" id="contextText">0 / 0 tokens</span>
      </div>
      <div class="context-actions">
        <button class="btn-action" id="btnCompact" title="Compactar sessão (/compact)">
          <span class="btn-icon">📦</span> Compact
        </button>
        <button class="btn-action" id="btnClear" title="Limpar sessão (/clear)">
          <span class="btn-icon">🗑️</span> Clear
        </button>
        <button class="btn-action" id="btnSummarize" title="Gerar resumo da sessão">
          <span class="btn-icon">📝</span> Summarize
        </button>
      </div>
    </section>

    <!-- Flow Diagram -->
    <div class="flow-container" id="flowDiagram">
      <div class="flow-node" id="node-user">
        <div class="icon">👤</div>
        <div class="label">USUARIO</div>
        <div class="sublabel">Prompt</div>
      </div>
      <div class="flow-arrow" id="arrow-1">→</div>
      <div class="flow-node" id="node-harness">
        <div class="icon">⚙️</div>
        <div class="label">HARNESS</div>
        <div class="sublabel" id="agentLabel">Agent</div>
      </div>
      <div class="flow-arrow" id="arrow-2">→</div>
      <div class="flow-node" id="node-llm">
        <div class="icon">🧠</div>
        <div class="label">LLM</div>
        <div class="sublabel" id="modelLabel">Model</div>
      </div>
      <div class="flow-arrow" id="arrow-3">→</div>
      <div class="flow-node" id="node-tools">
        <div class="icon">🔧</div>
        <div class="label">TOOLS</div>
        <div class="sublabel" id="toolLabel">Tool Calls</div>
      </div>
      <div class="flow-arrow" id="arrow-4">→</div>
      <div class="flow-node" id="node-response">
        <div class="icon">💬</div>
        <div class="label">RESPOSTA</div>
        <div class="sublabel">Output</div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats">
      <div class="stat-card">
        <div class="stat-label">Eventos</div>
        <div class="stat-value" id="statEvents">0</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Tool Calls</div>
        <div class="stat-value" id="statTools">0</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Tokens</div>
        <div class="stat-value" id="statTokens">0</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Custo</div>
        <div class="stat-value" id="statCost">$0.00</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Tokens/s</div>
        <div class="stat-value" id="statTps">0</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Duracao</div>
        <div class="stat-value" id="statDuration">0s</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Status</div>
        <div class="stat-value" id="statStatus">idle</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Sessao</div>
        <div class="stat-value" id="statSession">-</div>
      </div>
    </div>

    <!-- Tools Panel -->
    <section class="tools-panel" id="toolsPanel">
      <h2>Ferramentas Disponiveis</h2>
      <div class="tools-grid" id="toolsGrid">
        <div class="no-events">Carregando...</div>
      </div>
    </section>

    <!-- Timeline Grouped by Input -->
    <h2 style="margin: 24px 0 12px; font-size: 1.1rem; color: #fff;">Timeline</h2>
    <div class="timeline" id="timeline">
      <div class="no-events">Aguardando eventos...</div>
    </div>

    <!-- Log Completo -->
    <h2 style="margin: 24px 0 12px; font-size: 1.1rem; color: #fff;">Log Completo</h2>
    <div class="events-log" id="eventsLog">
      <div class="no-events">Nenhum evento registrado</div>
    </div>
  </main>

  <script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Create app.css**

Create `public/app.css` with all styles:

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: #0a0a0f;
  color: #e0e0e0;
  min-height: 100vh;
}

header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-bottom: 1px solid #333;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

header h1 { font-size: 1.4rem; font-weight: 600; color: #fff; }

header .status {
  display: flex; align-items: center; gap: 8px; font-size: 0.85rem;
}

header .status .dot {
  width: 10px; height: 10px; border-radius: 50%;
  background: #ef4444; transition: background 0.3s;
}

header .status .dot.connected { background: #22c55e; }

main { max-width: 1400px; margin: 0 auto; padding: 24px; }

/* Context Bar */
.context-bar {
  background: #1a1a2e;
  border: 1px solid #333;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 24px;
}

.context-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 12px;
}

.context-label { font-size: 0.9rem; font-weight: 600; color: #fff; }
.context-model { font-size: 0.8rem; color: #888; }

.context-progress { display: flex; align-items: center; gap: 12px; }

.context-track {
  flex: 1; height: 8px; background: #333; border-radius: 4px; overflow: hidden;
}

.context-fill {
  height: 100%;
  background: linear-gradient(90deg, #22c55e, #fbbf24, #ef4444);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.context-text { font-size: 0.8rem; color: #888; white-space: nowrap; min-width: 140px; }

.context-actions { display: flex; gap: 8px; margin-top: 12px; }

.btn-action {
  background: #2563eb; border: none; color: #fff; padding: 8px 16px;
  border-radius: 6px; cursor: pointer; font-size: 0.8rem;
  display: flex; align-items: center; gap: 6px; transition: background 0.2s;
}

.btn-action:hover { background: #1d4ed8; }
.btn-action:active { background: #1e40af; }
.btn-action:disabled { background: #555; cursor: not-allowed; }
.btn-icon { font-size: 1rem; }

/* Flow Container */
.flow-container {
  display: flex; align-items: center; justify-content: center;
  gap: 12px; margin: 32px 0; flex-wrap: wrap;
}

.flow-node {
  background: #1a1a2e; border: 2px solid #333; border-radius: 12px;
  padding: 20px 24px; text-align: center; min-width: 140px;
  transition: all 0.3s ease;
}

.flow-node.active { border-color: #3b82f6; box-shadow: 0 0 20px rgba(59,130,246,0.3); transform: scale(1.05); }
.flow-node.done { border-color: #22c55e; }
.flow-node .icon { font-size: 2rem; margin-bottom: 8px; }
.flow-node .label { font-size: 0.9rem; font-weight: 600; color: #fff; }
.flow-node .sublabel { font-size: 0.75rem; color: #888; margin-top: 4px; }

.flow-arrow { font-size: 1.5rem; color: #555; transition: color 0.3s; }
.flow-arrow.active { color: #3b82f6; }

/* Stats */
.stats {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px; margin: 24px 0;
}

.stat-card {
  background: #1a1a2e; border: 1px solid #333;
  border-radius: 8px; padding: 16px;
}

.stat-card .stat-label {
  font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 0.5px;
}

.stat-card .stat-value {
  font-size: 1.3rem; font-weight: 700; color: #fff; margin-top: 4px;
}

/* Tools Panel */
.tools-panel {
  background: #111; border: 1px solid #333; border-radius: 8px;
  padding: 16px; margin: 24px 0;
}

.tools-panel h2 {
  font-size: 1rem; margin-bottom: 12px; color: #fff;
}

.tools-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 8px;
}

.tool-chip {
  background: #1a1a2e; border: 1px solid #444; border-radius: 6px;
  padding: 8px 12px; cursor: pointer; transition: all 0.2s;
  font-size: 0.8rem; display: flex; align-items: center; gap: 6px;
}

.tool-chip:hover { border-color: #3b82f6; background: #1e293b; }
.tool-chip .tool-icon { font-size: 1rem; }
.tool-chip .tool-name { font-weight: 500; }
.tool-chip .tool-type { color: #666; font-size: 0.7rem; }

/* Timeline */
.timeline {
  position: relative; margin: 24px 0; padding-left: 24px; border-left: 2px solid #333;
}

.timeline-group {
  margin-bottom: 24px;
}

.timeline-group-header {
  background: #16213e; border: 1px solid #333; border-radius: 8px;
  padding: 12px 16px; margin-bottom: 8px; font-weight: 600;
  display: flex; align-items: center; gap: 8px;
}

.timeline-group-header .user-icon { font-size: 1.2rem; }
.timeline-group-header .user-text { color: #60a5fa; flex: 1; }
.timeline-group-header .group-time { color: #666; font-size: 0.75rem; }

.timeline-item {
  position: relative; margin-bottom: 8px; padding: 10px 14px;
  background: #1a1a2e; border-radius: 6px; border: 1px solid #333;
  margin-left: 16px;
}

.timeline-item::before {
  content: ''; position: absolute; left: -22px; top: 14px;
  width: 10px; height: 10px; border-radius: 50%;
  background: #333; border: 2px solid #1a1a2e;
}

.timeline-item.active::before { background: #3b82f6; }
.timeline-item.done::before { background: #22c55e; }
.timeline-item.error::before { background: #ef4444; }

.timeline-item .event-time { color: #666; font-size: 0.75rem; }
.timeline-item .event-type { font-weight: 600; font-size: 0.8rem; }
.timeline-item .event-detail { color: #888; font-size: 0.8rem; margin-top: 4px; }

.timeline-item .event-type.session { color: #a78bfa; }
.timeline-item .event-type.chat { color: #60a5fa; }
.timeline-item .event-type.tool { color: #fbbf24; }
.timeline-item .event-type.message { color: #34d399; }
.timeline-item .event-type.part { color: #f472b6; }
.timeline-item .event-type.system { color: #94a3b8; }

/* Events Log */
.events-log {
  background: #111; border: 1px solid #333; border-radius: 8px;
  max-height: 400px; overflow-y: auto;
  font-family: 'Cascadia Code', 'Fira Code', monospace; font-size: 0.75rem;
}

.events-log .event-row {
  padding: 6px 12px; border-bottom: 1px solid #222;
  display: flex; gap: 10px; align-items: flex-start;
}

.events-log .event-row:hover { background: #1a1a2e; }
.events-log .event-time { color: #666; white-space: nowrap; min-width: 70px; }
.events-log .event-type { font-weight: 600; min-width: 160px; }

.events-log .event-type.session { color: #a78bfa; }
.events-log .event-type.chat { color: #60a5fa; }
.events-log .event-type.tool { color: #fbbf24; }
.events-log .event-type.message { color: #34d399; }
.events-log .event-type.part { color: #f472b6; }
.events-log .event-type.system { color: #94a3b8; }

.events-log .event-detail {
  color: #999; overflow: hidden; text-overflow: ellipsis;
  white-space: nowrap; max-width: 400px;
}

.no-events { text-align: center; color: #555; padding: 48px; font-size: 1.1rem; }

@media (max-width: 768px) {
  .flow-container { flex-direction: column; }
  .flow-arrow { transform: rotate(90deg); }
  .context-actions { flex-wrap: wrap; }
  .stats { grid-template-columns: repeat(2, 1fr); }
}
```

- [ ] **Step 3: Create app.js (extracted from inline script)**

Create `public/app.js`:

```javascript
const statusDot = document.getElementById('statusDot')
const statusText = document.getElementById('statusText')
const contextModel = document.getElementById('contextModel')
const contextFill = document.getElementById('contextFill')
const contextText = document.getElementById('contextText')
const btnCompact = document.getElementById('btnCompact')
const btnClear = document.getElementById('btnClear')
const btnSummarize = document.getElementById('btnSummarize')
const statEvents = document.getElementById('statEvents')
const statTools = document.getElementById('statTools')
const statTokens = document.getElementById('statTokens')
const statCost = document.getElementById('statCost')
const statTps = document.getElementById('statTps')
const statDuration = document.getElementById('statDuration')
const statStatus = document.getElementById('statStatus')
const statSession = document.getElementById('statSession')
const timeline = document.getElementById('timeline')
const eventsLog = document.getElementById('eventsLog')
const toolsGrid = document.getElementById('toolsGrid')

let eventCount = 0
let startTime = null
let eventSource = null
let currentInput = null
let timelineGroups = []

function connect() {
  eventSource = new EventSource('/events')

  eventSource.onopen = () => {
    statusDot.classList.add('connected')
    statusText.textContent = 'Conectado'
  }

  eventSource.onerror = () => {
    statusDot.classList.remove('connected')
    statusText.textContent = 'Reconectando...'
    setTimeout(connect, 3000)
  }

  eventSource.onmessage = (msg) => {
    const event = JSON.parse(msg.data)
    handleEvent(event)
  }
}

function handleEvent(event) {
  if (event.type === 'connected') return

  eventCount++
  statEvents.textContent = eventCount

  if (!startTime) {
    startTime = event.timestamp
    statSession.textContent = event.sessionId?.slice(0, 8) || event.properties?.sessionID?.slice(0, 8) || '-'
  }

  const elapsed = ((event.timestamp - startTime) / 1000).toFixed(0)
  statDuration.textContent = elapsed + 's'

  updateFlowDiagram(event)
  addTimelineEntry(event)
  addLogEntry(event)
  fetchSessionStatus()
}

function updateFlowDiagram(event) {
  document.querySelectorAll('.flow-node').forEach(n => n.classList.remove('active', 'done'))
  document.querySelectorAll('.flow-arrow').forEach(a => a.classList.remove('active'))

  const t = event.type

  if (t === 'chat.message' || t === 'session:prompt') {
    document.getElementById('node-user').classList.add('active')
    const agent = event.properties?.agent || event.agent
    if (agent) document.getElementById('agentLabel').textContent = agent
  } else if (t === 'tool.execute.before' || t === 'tool:call') {
    document.getElementById('node-tools').classList.add('active')
    document.getElementById('arrow-3').classList.add('active')
    const tool = event.properties?.tool || event.tool
    if (tool) document.getElementById('toolLabel').textContent = tool
  } else if (t === 'tool.execute.after' || t === 'tool:result') {
    document.getElementById('node-tools').classList.add('done')
  } else if (t === 'message.updated' || t === 'session:response') {
    const msg = event.properties?.info || event.properties
    if (msg?.role === 'assistant') {
      document.getElementById('node-harness').classList.add('done')
      document.getElementById('node-llm').classList.add('done')
      document.getElementById('node-response').classList.add('active')
      const model = msg.modelID || msg.model || ''
      if (model) document.getElementById('modelLabel').textContent = model.split('/').pop()
    }
  } else if (t === 'message.part.updated') {
    const part = event.properties?.part
    if (part?.type === 'tool') {
      document.getElementById('node-tools').classList.add('active')
    } else if (part?.type === 'text') {
      document.getElementById('node-llm').classList.add('active')
    }
  }
}

function addTimelineEntry(event) {
  if (timeline.querySelector('.no-events')) {
    timeline.innerHTML = ''
    timelineGroups = []
  }

  const t = event.type
  const isUserInput = t === 'chat.message' || t === 'session:prompt'

  // Start new group on user input
  if (isUserInput) {
    const group = document.createElement('div')
    group.className = 'timeline-group'

    const header = document.createElement('div')
    header.className = 'timeline-group-header'

    const userText = event.properties?.parts?.find(p => p.type === 'text')?.text
      || event.prompt
      || ''

    const time = new Date(event.timestamp).toLocaleTimeString('pt-BR')
    header.innerHTML = `
      <span class="user-icon">👤</span>
      <span class="user-text">${userText.slice(0, 120)}${userText.length > 120 ? '...' : ''}</span>
      <span class="group-time">${time}</span>
    `
    group.appendChild(header)
    timeline.appendChild(group)
    currentInput = group
    return
  }

  // Add events to current group (or create orphan group)
  if (!currentInput) {
    const group = document.createElement('div')
    group.className = 'timeline-group'
    const header = document.createElement('div')
    header.className = 'timeline-group-header'
    header.innerHTML = `<span class="user-icon">📡</span><span class="user-text">System Events</span>`
    group.appendChild(header)
    timeline.appendChild(group)
    currentInput = group
  }

  const item = document.createElement('div')
  item.className = 'timeline-item active'

  const time = new Date(event.timestamp).toLocaleTimeString('pt-BR')
  let detail = ''
  const props = event.properties || {}

  if (t === 'tool.execute.before') {
    detail = `${props.tool}(${JSON.stringify(props.args || {}).slice(0, 60)})`
  } else if (t === 'tool.execute.after') {
    detail = `${props.tool} → ${props.title || 'OK'}`
  } else if (t === 'message.updated') {
    const msg = props.info || props
    detail = `${msg.role || '?'} — ${(msg.modelID || msg.model || '').slice(0, 30)}`
  } else if (t === 'message.part.updated') {
    const part = props.part || {}
    detail = `${part.type}: ${(part.text || part.tool || '').slice(0, 60)}`
  } else if (t === 'session.status') {
    detail = `status: ${props.status?.type || '?'}`
  } else {
    detail = JSON.stringify(props).slice(0, 80)
  }

  item.innerHTML = `
    <span class="event-time">${time}</span>
    <span class="event-type ${t.split('.')[0].split(':')[0]}">${t}</span>
    <div class="event-detail">${detail}</div>
  `
  currentInput.appendChild(item)
}

function addLogEntry(event) {
  if (eventsLog.querySelector('.no-events')) {
    eventsLog.innerHTML = ''
  }

  const row = document.createElement('div')
  row.className = 'event-row'

  const time = new Date(event.timestamp).toLocaleTimeString('pt-BR')
  const t = event.type
  const typeClass = t.split('.')[0].split(':')[0]
  let detail = JSON.stringify(event).slice(0, 150)

  row.innerHTML = `
    <span class="event-time">${time}</span>
    <span class="event-type ${typeClass}">${t}</span>
    <span class="event-detail">${detail}</span>
  `
  eventsLog.appendChild(row)
  eventsLog.scrollTop = eventsLog.scrollHeight
}

async function fetchSessionStatus() {
  try {
    const res = await fetch('/api/session-status')
    const state = await res.json()

    if (state.totalTokens > 0) statTokens.textContent = formatNumber(state.totalTokens)
    if (state.totalCost > 0) statCost.textContent = '$' + state.totalCost.toFixed(4)
    if (state.tokensPerSecond > 0) statTps.textContent = state.tokensPerSecond
    if (state.sessionStatus) statStatus.textContent = state.sessionStatus
    if (state.sessionId) statSession.textContent = state.sessionId.slice(0, 8)
    if (state.lastModel) contextModel.textContent = state.lastModel

    // Context bar
    if (state.contextLimit.input > 0) {
      const used = state.contextUsed
      const limit = state.contextLimit.input
      const pct = Math.min(100, (used / limit) * 100)
      contextFill.style.width = pct + '%'
      contextText.textContent = `${formatNumber(used)} / ${formatNumber(limit)} tokens`
    }

    // Update stat card for active tools
    statTools.textContent = state.toolCount
  } catch {
    // Server might be down
  }
}

function formatNumber(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'K'
  return n.toString()
}

async function loadTools() {
  try {
    const [agentsRes, mcpRes] = await Promise.all([
      fetch('/api/tools').catch(() => null),
      fetch('/api/mcp').catch(() => null),
    ])

    const items = []

    if (agentsRes?.ok) {
      const agents = await agentsRes.json()
      for (const agent of (Array.isArray(agents) ? agents : [])) {
        items.push({
          name: agent.name,
          type: 'agent',
          icon: agent.mode === 'subagent' ? '🤖' : '👤',
          description: agent.description || agent.mode,
        })
      }
    }

    if (mcpRes?.ok) {
      const mcps = await mcpRes.json()
      for (const [name, status] of Object.entries(mcps)) {
        items.push({
          name,
          type: 'mcp',
          icon: status.status === 'connected' ? '🔌' : '⚠️',
          description: status.status,
        })
      }
    }

    if (items.length === 0) {
      toolsGrid.innerHTML = '<div class="no-events">Nenhuma ferramenta detectada</div>'
      return
    }

    toolsGrid.innerHTML = items.map(item => `
      <div class="tool-chip" data-type="${item.type}" data-name="${item.name}" title="${item.description}">
        <span class="tool-icon">${item.icon}</span>
        <span class="tool-name">${item.name}</span>
        <span class="tool-type">${item.type}</span>
      </div>
    `).join('')
  } catch {
    toolsGrid.innerHTML = '<div class="no-events">Erro ao carregar ferramentas</div>'
  }
}

// Quick actions
btnCompact.addEventListener('click', async () => {
  btnCompact.disabled = true
  try {
    await fetch('/api/compact', { method: 'POST' })
  } catch {}
  btnCompact.disabled = false
})

btnClear.addEventListener('click', async () => {
  if (!confirm('Criar nova sessão? A sessão atual será finalizada.')) return
  btnClear.disabled = true
  try {
    await fetch('/api/clear', { method: 'POST' })
  } catch {}
  btnClear.disabled = false
})

btnSummarize.addEventListener('click', async () => {
  btnSummarize.disabled = true
  try {
    await fetch('/api/summarize', { method: 'POST' })
  } catch {}
  btnSummarize.disabled = false
})

// Poll session status every 2s
setInterval(fetchSessionStatus, 2000)

connect()
loadTools()
fetchSessionStatus()
```

- [ ] **Step 4: Verify server serves the new files**

Run: `cd opencode-monitor && npm start`
Open: http://localhost:7777
Expected: New layout loads with context bar, stats, tools panel, grouped timeline

- [ ] **Step 5: Commit**

```bash
git add opencode-monitor/public/
git commit -m "feat: redesign dashboard with context bar, tools panel, grouped timeline"
```

---

## Task 5: Wire Everything Together

**Files:**
- Modify: `opencode-monitor/src/cli.js` (pass openCodeUrl config)

- [ ] **Step 1: Update cli.js to accept OPENCODE_URL**

```javascript
#!/usr/bin/env node

import { MonitorServer } from "./server.js"

const PORT = parseInt(process.env.PORT || "7777")
const HOST = process.env.HOST || "localhost"
const OPENCODE_URL = process.env.OPENCODE_URL || "http://localhost:4096"

const server = new MonitorServer(PORT, HOST, OPENCODE_URL)

server.start()
server.watchDir()

console.log(`Dashboard: http://${HOST}:${PORT}`)
console.log(`OpenCode: ${OPENCODE_URL}`)
console.log("Aguardando eventos do OpenCode...")
console.log("Para parar: Ctrl+C")

let shutdownTimeout = null

function gracefulShutdown() {
  console.log("\nEncerrando monitor...")
  server.stop()

  if (shutdownTimeout) {
    clearTimeout(shutdownTimeout)
  }

  shutdownTimeout = setTimeout(() => {
    console.log("Shutdown forcado.")
    process.exit(1)
  }, 5000)

  shutdownTimeout.unref()
  process.exit(0)
}

process.on("SIGINT", gracefulShutdown)
process.on("SIGTERM", gracefulShutdown)
process.on("uncaughtException", (err) => {
  console.error("Excecao nao capturada:", err.message)
})
process.on("unhandledRejection", (reason) => {
  console.error("Rejeicao nao tratada:", reason)
})
```

- [ ] **Step 2: Run all tests**

Run: `cd opencode-monitor && npm test`
Expected: All tests pass

- [ ] **Step 3: Manual verification**

1. Start monitor: `npm start`
2. Open http://localhost:7777
3. Verify context bar shows (empty initially)
4. Verify tools panel loads agents and MCPs
5. Verify quick action buttons exist
6. Verify timeline groups by user input

- [ ] **Step 4: Commit**

```bash
git add opencode-monitor/src/cli.js
git commit -m "feat: wire OPENCODE_URL config and finalize integration"
```

---

## Task 6: Update Documentation

**Files:**
- Modify: `opencode-monitor/README.md`
- Modify: `opencode-monitor/AGENTS.md`

- [ ] **Step 1: Update README.md with new features**

Add a "V2 Features" section after the existing setup instructions:

```markdown
## V2 Features

### Context Window Bar
Progress bar showing context usage. Updates in real-time as tokens accumulate.
- **Compact** button: triggers session compaction
- **Clear** button: creates a new session
- **Summarize** button: generates session summary via OpenCode

### Cost & Performance Tracking
- **Tokens**: total tokens used (input + output + cache)
- **Custo**: accumulated session cost in USD
- **Tokens/s**: output generation speed
- **Status**: session state (idle/busy/retry)

### Tools Panel
Shows available agents and MCP servers. Loaded on startup from OpenCode API.
- Agents (primary and subagents)
- MCP servers (with connection status)

### Grouped Timeline
Timeline events are grouped by user input. Each user message starts a new group,
with all subsequent tool calls, LLM responses, and system events nested under it.

### API Proxy Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/api/session-status` | GET | Session state (tokens, cost, context) |
| `/api/tools` | GET | List agents |
| `/api/mcp` | GET | MCP server status |
| `/api/compact` | POST | Trigger session compaction |
| `/api/clear` | POST | Create new session |
| `/api/summarize` | POST | Generate session summary |
```

- [ ] **Step 2: Update AGENTS.md**

Add V2 architecture info:

```markdown
## Arquitetura V2

```
OpenCode (plugin) → JSONL → server.js → SSE → browser
                         ↓
                   session-tracker.js (computa tokens, cost, context)
                         ↓
                   /api/* routes (proxy para OpenCode SDK)
```

### Novos componentes
- `session-tracker.js` — estado da sessao (tokens, cost, context, tools)
- `public/app.js` — JS extraido do inline
- `public/app.css` — CSS extraido do inline
```

- [ ] **Step 3: Commit**

```bash
git add opencode-monitor/README.md opencode-monitor/AGENTS.md
git commit -m "docs: update README and AGENTS for V2 features"
```

---

## Summary

| Task | Files Changed | New Files | Tests |
|------|---------------|-----------|-------|
| 1. Session Tracker | 0 | 2 | 7 |
| 2. Server API Routes | 2 | 0 | 2 |
| 3. Plugin Hooks | 1 | 0 | manual |
| 4. Dashboard HTML | 0 | 3 | manual |
| 5. Wire Together | 1 | 0 | existing |
| 6. Documentation | 2 | 0 | 0 |
| **Total** | **6** | **5** | **9+** |

**Estimated effort:** 45-60 minutes
