import { createServer } from "http"
import {
  readFileSync,
  existsSync,
  watch,
  statSync,
  openSync,
  readSync,
  closeSync,
  readdirSync,
} from "fs"
import { join, dirname, basename } from "path"
import { homedir } from "os"
import { fileURLToPath } from "url"
import { EventEmitter } from "events"
import { SessionTracker } from "./session-tracker.js"

const __dirname = dirname(fileURLToPath(import.meta.url))
const PUBLIC_DIR = join(__dirname, "..", "public")
const DEFAULT_DATA_DIR = join(__dirname, "..", "data")

function addCORS(res) {
  res.setHeader("Access-Control-Allow-Origin", "*")
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
  res.setHeader("Access-Control-Allow-Headers", "Content-Type")
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = []
    req.on("data", (c) => chunks.push(c))
    req.on("end", () => resolve(Buffer.concat(chunks).toString()))
    req.on("error", reject)
  })
}

export class MonitorServer {
  constructor(port = 7777, host = "localhost", openCodeUrl = "http://localhost:57129") {
    this.port = port
    this.host = host
    this.openCodeUrl = process.env.OPENCODE_URL || openCodeUrl
    this.clients = new Set()
    this.events = new EventEmitter()
    this.server = null
    this.dataDir = DEFAULT_DATA_DIR
    this.fileCursors = new Map()
    this.dirWatcher = null
    this.fileWatchers = new Map()
    this.sessionTracker = new SessionTracker()
    this._pollTimer = null
    this._statusBroadcastTimer = null
  }

  setDataDir(dir) {
    this.dataDir = dir
  }

  watchDir() {
    if (!existsSync(this.dataDir)) {
      return
    }

    const files = this._getJsonlFiles()
    for (const file of files) {
      this._initFileCursor(file)
      this._watchFile(file)
    }

    try {
      this.dirWatcher = watch(this.dataDir, (eventType, filename) => {
        if (!filename || !filename.endsWith(".jsonl")) return

        const filePath = join(this.dataDir, filename)

        if (eventType === "rename") {
          if (existsSync(filePath)) {
            this._initFileCursor(filePath)
            this._watchFile(filePath)
          } else {
            this._unwatchFile(filePath)
          }
        }
      })
      this.dirWatcher.on("error", (err) => {
        console.error("Erro no watcher do diretorio:", err.message)
      })
    } catch (err) {
      console.error("Erro ao iniciar watcher do diretorio:", err.message)
    }
  }

  _getJsonlFiles() {
    try {
      return readdirSync(this.dataDir)
        .filter((f) => f.endsWith(".jsonl"))
        .map((f) => join(this.dataDir, f))
    } catch {
      return []
    }
  }

  _initFileCursor(filePath) {
    if (this.fileCursors.has(filePath)) return
    try {
      const stat = statSync(filePath)
      this.fileCursors.set(filePath, stat.size)
    } catch {
      this.fileCursors.set(filePath, 0)
    }
  }

  _watchFile(filePath) {
    if (this.fileWatchers.has(filePath)) return

    try {
      const watcher = watch(filePath, () => {
        this._readNewEvents(filePath)
      })
      watcher.on("error", (err) => {
        console.error(`Erro no watcher de ${basename(filePath)}:`, err.message)
      })
      this.fileWatchers.set(filePath, watcher)
    } catch (err) {
      console.error(`Erro ao iniciar watcher de ${basename(filePath)}:`, err.message)
    }
  }

  _unwatchFile(filePath) {
    const watcher = this.fileWatchers.get(filePath)
    if (watcher) {
      watcher.close()
      this.fileWatchers.delete(filePath)
    }
    this.fileCursors.delete(filePath)
  }

  _readNewEvents(filePath) {
    if (!existsSync(filePath)) return

    const cursor = this.fileCursors.get(filePath) || 0

    try {
      const stat = statSync(filePath)
      if (stat.size <= cursor) return

      const fd = openSync(filePath, "r")
      const buffer = Buffer.alloc(stat.size - cursor)
      readSync(fd, buffer, 0, buffer.length, cursor)
      closeSync(fd)

      this.fileCursors.set(filePath, stat.size)

      const newContent = buffer.toString("utf-8")
      const lines = newContent.trim().split("\n").filter(Boolean)

      for (const line of lines) {
        try {
          const event = JSON.parse(line)
          this.broadcast(event)
        } catch {
          // linha invalida, ignora
        }
      }
    } catch (err) {
      console.error(`Erro ao ler eventos de ${basename(filePath)}:`, err.message)
    }
  }

  start() {
    this.server = createServer((req, res) => {
      addCORS(res)

      if (req.method === "OPTIONS") {
        res.writeHead(204)
        res.end()
        return
      }

      try {
        if (req.url === "/events") {
          this._handleSSE(req, res)
          return
        }

        if (req.url === "/api/events") {
          this._handleAPIEvents(req, res)
          return
        }

        if (req.url === "/api/session-status" && req.method === "GET") {
          res.writeHead(200, { "Content-Type": "application/json" })
          res.end(JSON.stringify(this.sessionTracker.getState()))
          return
        }

        if (req.url === "/api/session" && req.method === "GET") {
          this._handleGetSessions(req, res)
          return
        }

        if (req.url === "/api/tools" && req.method === "GET") {
          this._handleGetTools(req, res)
          return
        }

        if (req.url === "/api/compact" && req.method === "POST") {
          this._handleCompact(req, res)
          return
        }

        if (req.url === "/api/clear" && req.method === "POST") {
          this._handleClear(req, res)
          return
        }

        if (req.url === "/api/summarize" && req.method === "POST") {
          this._handleSummarize(req, res)
          return
        }

        this._serveStatic(req, res)
      } catch (err) {
        console.error("Erro na requisicao:", err.message)
        res.writeHead(500, { "Content-Type": "application/json" })
        res.end(JSON.stringify({ error: "Erro interno do servidor" }))
      }
    })

    this.server.listen(this.port, this.host, () => {
      console.log(`Monitor rodando em http://${this.host}:${this.port}`)
      this._startPolling()
    })

    return this
  }

  _startPolling() {
    this._pollSession()
    this._pollTimer = setInterval(() => this._pollSession(), 3000)
    this._statusBroadcastTimer = setInterval(() => this._broadcastStatus(), 2000)
  }

  _broadcastStatus() {
    if (this.clients.size === 0) return
    const state = this.sessionTracker.getState()
    const data = JSON.stringify({ type: "session-status", ...state })
    for (const client of this.clients) {
      client.write(`data: ${data}\n\n`)
    }
  }

  async _pollSession() {
    try {
      const response = await fetch(`${this.openCodeUrl}/api/session`)
      if (!response.ok) return
      const data = await response.json()
      const sessions = data?.data
      if (!Array.isArray(sessions) || sessions.length === 0) return

      this.sessionTracker.updateFromAllSessions(sessions)

      const currentId = this.sessionTracker.getState().sessionId
      let session = null

      if (currentId) {
        session = sessions.find((s) => s.id === currentId)
      }
      if (!session) {
        session = sessions.find((s) => s.id) || sessions[0]
      }

      if (session) {
        this.sessionTracker.updateFromAPISession(session)
      }
    } catch {
      // OpenCode offline
    }
  }

  async _handleCompact(req, res) {
    const sessionId = this.sessionTracker.getState().sessionId
    if (!sessionId) {
      res.writeHead(200, { "Content-Type": "application/json" })
      res.end(JSON.stringify({ ok: true, message: "Nenhuma sessao ativa para compactar" }))
      return
    }
    await this._proxyToOpenCode(req, res, `/api/session/${sessionId}/compact`, { method: "POST" })
  }

  async _handleClear(req, res) {
    const sessionId = this.sessionTracker.getState().sessionId
    if (!sessionId) {
      res.writeHead(200, { "Content-Type": "application/json" })
      res.end(JSON.stringify({ ok: true, message: "Nenhuma sessao ativa para limpar" }))
      return
    }
    await this._proxyToOpenCode(req, res, `/api/session/${sessionId}/clear`, { method: "POST" })
  }

  async _handleSummarize(req, res) {
    const sessionId = this.sessionTracker.getState().sessionId
    if (!sessionId) {
      res.writeHead(200, { "Content-Type": "application/json" })
      res.end(JSON.stringify({ ok: true, message: "Nenhuma sessao ativa para resumir" }))
      return
    }
    await this._proxyToOpenCode(req, res, `/api/session/${sessionId}/summarize`, { method: "POST" })
  }

  async _handleGetSessions(req, res) {
    try {
      const response = await fetch(`${this.openCodeUrl}/api/session`)
      if (!response.ok) {
        res.writeHead(response.status, { "Content-Type": "application/json" })
        res.end(await response.text())
        return
      }
      const data = await response.json()
      res.writeHead(200, { "Content-Type": "application/json" })
      res.end(JSON.stringify(data))
    } catch (err) {
      res.writeHead(502, { "Content-Type": "application/json" })
      res.end(JSON.stringify({ error: "OpenCode server unreachable", detail: err.message }))
    }
  }

  _handleGetTools(req, res) {
    const configDir = join(homedir(), ".config", "opencode")
    const result = { mcp: [], skills: [], agents: [], usedTools: [] }

    try {
      const configPath = join(configDir, "opencode.json")
      if (existsSync(configPath)) {
        const config = JSON.parse(readFileSync(configPath, "utf-8"))
        if (config.mcp) {
          for (const [name, mcp] of Object.entries(config.mcp)) {
            result.mcp.push({ name, type: mcp.type || "local", enabled: mcp.enabled !== false })
          }
        }
      }
    } catch {}

    for (const dir of ["skill", "skills"]) {
      const skillsDir = join(configDir, dir)
      if (!existsSync(skillsDir)) continue
      try {
        this._scanSkillsDir(skillsDir, dir, result.skills)
      } catch {}
    }

    const seen = new Set()
    result.skills = result.skills.filter((s) => {
      if (seen.has(s.name)) return false
      seen.add(s.name)
      return true
    })

    const usedTools = this.sessionTracker.getState().usedTools || []
    result.usedTools = usedTools

    res.writeHead(200, { "Content-Type": "application/json" })
    res.end(JSON.stringify(result))
  }

  _scanSkillsDir(dir, source, result) {
    const entries = readdirSync(dir, { withFileTypes: true })
    for (const entry of entries) {
      if (!entry.isDirectory()) continue
      const fullPath = join(dir, entry.name)
      const skillFile = join(fullPath, "SKILL.md")
      if (existsSync(skillFile)) {
        result.push({ name: entry.name, source, hasSkillFile: true })
      } else {
        this._scanSkillsDir(fullPath, source, result)
      }
    }
  }

  _handleAPIEvents(req, res) {
    const files = this._getJsonlFiles()
    const allEvents = []

    for (const file of files) {
      try {
        const content = readFileSync(file, "utf-8")
        const lines = content.trim().split("\n").filter(Boolean)
        for (const line of lines) {
          try {
            allEvents.push(JSON.parse(line))
          } catch {
            // invalida
          }
        }
      } catch {
        // erro ao ler arquivo
      }
    }

    allEvents.sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0))

    const sessionId = allEvents.length > 0 ? allEvents[0].sessionId : null

    res.writeHead(200, { "Content-Type": "application/json" })
    res.end(
      JSON.stringify({
        events: allEvents,
        total: allEvents.length,
        sessionId,
      })
    )
  }

  _handleSSE(req, res) {
    res.writeHead(200, {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
      "Access-Control-Allow-Origin": "*",
    })

    res.write('data: {"type":"connected"}\n\n')
    this.clients.add(res)

    req.on("close", () => {
      this.clients.delete(res)
    })
  }

  _serveStatic(req, res) {
    let filePath = req.url === "/" ? "/index.html" : req.url
    filePath = join(PUBLIC_DIR, filePath)

    if (!existsSync(filePath)) {
      res.writeHead(404)
      res.end("Not found")
      return
    }

    const ext = filePath.split(".").pop()
    const mimeTypes = {
      html: "text/html",
      css: "text/css",
      js: "application/javascript",
      json: "application/json",
      png: "image/png",
      svg: "image/svg+xml",
    }

    res.writeHead(200, { "Content-Type": mimeTypes[ext] || "text/plain" })
    res.end(readFileSync(filePath))
  }

  broadcast(event) {
    this.sessionTracker.processEvent(event)
    const data = JSON.stringify(event)
    for (const client of this.clients) {
      client.write(`data: ${data}\n\n`)
    }
  }

  async _proxyToOpenCode(req, res, path, options = {}) {
    try {
      const url = new URL(path, this.openCodeUrl)
      const fetchOptions = {
        method: options.method || req.method,
        headers: { "Content-Type": "application/json" },
      }

      const response = await fetch(url.toString(), { ...fetchOptions, signal: AbortSignal.timeout(5000) })
      const data = await response.text()

      res.writeHead(response.status, { "Content-Type": "application/json" })
      res.end(data)
    } catch (err) {
      const detail = err.name === "TimeoutError" ? "OpenCode timeout (5s)" : err.message
      res.writeHead(200, { "Content-Type": "application/json" })
      res.end(JSON.stringify({ ok: false, error: "OpenCode indisponivel", detail }))
    }
  }

  stop() {
    if (this._pollTimer) {
      clearInterval(this._pollTimer)
      this._pollTimer = null
    }

    if (this._statusBroadcastTimer) {
      clearInterval(this._statusBroadcastTimer)
      this._statusBroadcastTimer = null
    }

    if (this.dirWatcher) {
      this.dirWatcher.close()
      this.dirWatcher = null
    }

    for (const [, watcher] of this.fileWatchers) {
      watcher.close()
    }
    this.fileWatchers.clear()
    this.fileCursors.clear()

    for (const client of this.clients) {
      client.write('data: {"type":"server:shutdown"}\n\n')
      client.end()
    }
    this.clients.clear()

    if (this.server) {
      this.server.close()
    }
  }
}
