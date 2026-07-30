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
      "event:session:create": async (event) => {
        emit("session:create", { session: event.properties?.info })
      },
      "event:session:prompt": async (event) => {
        emit("session:prompt", {
          prompt: event.properties?.message?.content,
        })
      },
      "event:session:response": async (event) => {
        emit("session:response", {
          response: event.properties?.message?.content,
        })
      },
      "event:tool:call": async (event) => {
        emit("tool:call", {
          tool: event.properties?.tool,
          args: event.properties?.args,
        })
      },
      "event:tool:result": async (event) => {
        emit("tool:result", {
          tool: event.properties?.tool,
          result: event.properties?.result,
        })
      },
      "event:llm:completion": async (event) => {
        emit("llm:completion", {
          provider: event.properties?.provider,
          model: event.properties?.model,
          tokens: event.properties?.tokens,
        })
      },
    },
  }
}
