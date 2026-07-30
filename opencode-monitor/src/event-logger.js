import { appendFileSync, mkdirSync, existsSync } from "fs"
import { join, dirname } from "path"
import { fileURLToPath } from "url"
import { randomUUID } from "crypto"

const __dirname = dirname(fileURLToPath(import.meta.url))
const DEFAULT_DIR = join(__dirname, "..", "data")

export class EventLogger {
  constructor(dataDir) {
    this.dataDir = dataDir || DEFAULT_DIR
    this.sessionId = randomUUID()
    this.eventFile = join(this.dataDir, `session-${this.sessionId}.jsonl`)

    if (!existsSync(this.dataDir)) {
      mkdirSync(this.dataDir, { recursive: true })
    }
  }

  log(type, payload = {}) {
    const event = {
      id: randomUUID(),
      type,
      sessionId: this.sessionId,
      timestamp: Date.now(),
      ...payload,
    }

    appendFileSync(this.eventFile, JSON.stringify(event) + "\n")
    return event
  }

  getEventFile() {
    return this.eventFile
  }

  getSessionId() {
    return this.sessionId
  }
}
