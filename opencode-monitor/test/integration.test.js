import { describe, it, before, after } from "node:test"
import assert from "node:assert"
import http from "node:http"
import { MonitorServer } from "../src/server.js"
import { appendFileSync, mkdirSync, existsSync, rmSync } from "fs"
import { join } from "path"

const TEST_DIR = join(import.meta.dirname, "..", "data", "integration-test")
const TEST_PORT = 8765

function fetch(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = ""
      res.on("data", (chunk) => (data += chunk))
      res.on("end", () => resolve({ status: res.statusCode, headers: res.headers, body: data }))
    }).on("error", reject)
  })
}

function fetchSSE(url) {
  return new Promise((resolve, reject) => {
    const req = http.get(url, (res) => {
      let data = ""
      res.on("data", (chunk) => {
        data += chunk.toString()
        if (data.includes("\n\n")) {
          res.destroy()
          resolve({ status: res.statusCode, headers: res.headers, body: data })
        }
      })
      res.on("end", () => resolve({ status: res.statusCode, headers: res.headers, body: data }))
    })
    req.on("error", reject)
    setTimeout(() => { req.destroy(); resolve({ status: 0, body: "timeout" }) }, 3000)
  })
}

describe("Integracao Completa", () => {
  let server

  before(() => {
    if (!existsSync(TEST_DIR)) {
      mkdirSync(TEST_DIR, { recursive: true })
    }
    server = new MonitorServer(TEST_PORT, "127.0.0.1")
    server.setDataDir(TEST_DIR)
    server.start()
  })

  after(() => {
    server.stop()
    if (existsSync(TEST_DIR)) {
      rmSync(TEST_DIR, { recursive: true })
    }
  })

  it("GET / retorna HTML do dashboard", async () => {
    const res = await fetch(`http://127.0.0.1:${TEST_PORT}/`)
    assert.strictEqual(res.status, 200)
    assert.strictEqual(res.headers["content-type"], "text/html")
    assert.ok(res.body.includes("OpenCode Monitor"))
  })

  it("GET /events retorna SSE stream", async () => {
    const res = await fetchSSE(`http://127.0.0.1:${TEST_PORT}/events`)
    assert.strictEqual(res.status, 200)
    assert.strictEqual(res.headers["content-type"], "text/event-stream")
    assert.ok(res.body.includes('"type":"connected"'))
  })

  it("GET /api/events retorna JSON", async () => {
    const res = await fetch(`http://127.0.0.1:${TEST_PORT}/api/events`)
    assert.strictEqual(res.status, 200)
    assert.strictEqual(res.headers["content-type"], "application/json")
    const data = JSON.parse(res.body)
    assert.ok(Array.isArray(data.events))
  })

  it("CORS headers presentes", async () => {
    const res = await fetch(`http://127.0.0.1:${TEST_PORT}/`)
    assert.strictEqual(res.headers["access-control-allow-origin"], "*")
  })

  it("GET /rota-inexistente retorna 404", async () => {
    const res = await fetch(`http://127.0.0.1:${TEST_PORT}/nao-existe`)
    assert.strictEqual(res.status, 404)
  })
})
