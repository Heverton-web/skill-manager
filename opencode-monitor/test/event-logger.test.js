import { describe, it } from "node:test"
import assert from "node:assert"
import { EventLogger } from "../src/event-logger.js"
import { existsSync, readFileSync, rmSync } from "fs"
import { join } from "path"

const TEST_DIR = join(import.meta.dirname, "..", "data", "test")

describe("EventLogger", () => {
  it("cria diretorio de dados", () => {
    const logger = new EventLogger(TEST_DIR)
    assert.ok(existsSync(TEST_DIR))
    rmSync(TEST_DIR, { recursive: true })
  })

  it("gera sessionId unico", () => {
    const a = new EventLogger(TEST_DIR)
    const b = new EventLogger(TEST_DIR)
    assert.notStrictEqual(a.getSessionId(), b.getSessionId())
    rmSync(TEST_DIR, { recursive: true })
  })

  it("log salva evento em JSONL", () => {
    const logger = new EventLogger(TEST_DIR)
    const event = logger.log("test:event", { foo: "bar" })

    assert.strictEqual(event.type, "test:event")
    assert.strictEqual(event.foo, "bar")
    assert.ok(event.id)
    assert.ok(event.sessionId)
    assert.ok(event.timestamp)

    const content = readFileSync(logger.getEventFile(), "utf-8")
    const lines = content.trim().split("\n")
    assert.strictEqual(lines.length, 1)

    const parsed = JSON.parse(lines[0])
    assert.strictEqual(parsed.type, "test:event")

    rmSync(TEST_DIR, { recursive: true })
  })

  it("multiplos logs acumulam no arquivo", () => {
    const logger = new EventLogger(TEST_DIR)
    logger.log("event:a", { n: 1 })
    logger.log("event:b", { n: 2 })
    logger.log("event:c", { n: 3 })

    const content = readFileSync(logger.getEventFile(), "utf-8")
    const lines = content.trim().split("\n")
    assert.strictEqual(lines.length, 3)

    rmSync(TEST_DIR, { recursive: true })
  })

  it("retorna caminho do arquivo de eventos", () => {
    const logger = new EventLogger(TEST_DIR)
    const file = logger.getEventFile()
    assert.ok(file.endsWith(".jsonl"))
    assert.ok(file.includes("session-"))
    rmSync(TEST_DIR, { recursive: true })
  })
})
