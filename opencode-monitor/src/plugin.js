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
          parts: output.parts?.map((p) => ({
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
        if (
          evt.type === "session.created" ||
          evt.type === "session.updated" ||
          evt.type === "session.idle" ||
          evt.type === "session.compacted" ||
          evt.type === "session.error" ||
          evt.type === "session.status"
        ) {
          emit(evt.type, evt.properties)
        }
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
