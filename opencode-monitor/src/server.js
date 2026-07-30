import { createServer } from "http"
import { readFileSync, existsSync, watch, statSync } from "fs"
import { join, dirname } from "path"
import { fileURLToPath } from "url"
import { EventEmitter } from "events"

const __dirname = dirname(fileURLToPath(import.meta.url))
const PUBLIC_DIR = join(__dirname, "..", "public")

function addCORS(res) {
  res.setHeader("Access-Control-Allow-Origin", "*")
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
  res.setHeader("Access-Control-Allow-Headers", "Content-Type")
}

export class MonitorServer {
  constructor(port = 7777, host = "localhost") {
    this.port = port
    this.host = host
    this.clients = new Set()
    this.events = new EventEmitter()
    this.server = null
    this.eventFile = null
    this.watcher = null
    this.fileCursor = 0
  }

  setEventFile(path) {
    this.eventFile = path
    this.fileCursor = 0
  }

  watchFile() {
    if (!this.eventFile || !existsSync(this.eventFile)) {
      return
    }

    try {
      const stat = statSync(this.eventFile)
      this.fileCursor = stat.size
    } catch {
      this.fileCursor = 0
    }

    try {
      this.watcher = watch(this.eventFile, () => {
        this._readNewEvents()
      })
      this.watcher.on("error", (err) => {
        console.error("Erro no watcher:", err.message)
      })
    } catch (err) {
      console.error("Erro ao iniciar watcher:", err.message)
    }
  }

  _readNewEvents() {
    if (!this.eventFile || !existsSync(this.eventFile)) return

    try {
      const stat = statSync(this.eventFile)
      if (stat.size <= this.fileCursor) return

      const fd = require("fs").openSync(this.eventFile, "r")
      const buffer = Buffer.alloc(stat.size - this.fileCursor)
      require("fs").readSync(fd, buffer, 0, buffer.length, this.fileCursor)
      require("fs").closeSync(fd)

      this.fileCursor = stat.size

      const newContent = buffer.toString("utf-8")
      const lines = newContent.trim().split("\n").filter(Boolean)

      for (const line of lines) {
        try {
          const event = JSON.parse(line)
          this.broadcast(event)
        } catch {
          // linha inválida, ignora
        }
      }
    } catch (err) {
      console.error("Erro ao ler novos eventos:", err.message)
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

        this._serveStatic(req, res)
      } catch (err) {
        console.error("Erro na requisição:", err.message)
        res.writeHead(500, { "Content-Type": "application/json" })
        res.end(JSON.stringify({ error: "Erro interno do servidor" }))
      }
    })

    this.server.listen(this.port, this.host, () => {
      console.log(`Monitor rodando em http://${this.host}:${this.port}`)
    })

    return this
  }

  _handleAPIEvents(req, res) {
    if (!this.eventFile || !existsSync(this.eventFile)) {
      res.writeHead(200, { "Content-Type": "application/json" })
      res.end(JSON.stringify({ events: [], total: 0, sessionId: null }))
      return
    }

    try {
      const content = readFileSync(this.eventFile, "utf-8")
      const lines = content.trim().split("\n").filter(Boolean)
      const events = lines.map((line) => {
        try {
          return JSON.parse(line)
        } catch {
          return null
        }
      }).filter(Boolean)

      const sessionId = events.length > 0 ? events[0].sessionId : null

      res.writeHead(200, { "Content-Type": "application/json" })
      res.end(JSON.stringify({ events, total: events.length, sessionId }))
    } catch (err) {
      console.error("Erro ao ler eventos:", err.message)
      res.writeHead(500, { "Content-Type": "application/json" })
      res.end(JSON.stringify({ error: "Erro ao ler eventos" }))
    }
  }

  _handleSSE(req, res) {
    res.writeHead(200, {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
      "Access-Control-Allow-Origin": "*",
    })

    res.write("data: {\"type\":\"connected\"}\n\n")
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
    const data = JSON.stringify(event)
    for (const client of this.clients) {
      client.write(`data: ${data}\n\n`)
    }
  }

  stop() {
    if (this.watcher) {
      this.watcher.close()
      this.watcher = null
    }

    for (const client of this.clients) {
      client.write("data: {\"type\":\"server:shutdown\"}\n\n")
      client.end()
    }
    this.clients.clear()

    if (this.server) {
      this.server.close()
    }
  }
}
