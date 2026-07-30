#!/usr/bin/env node

import { MonitorServer } from "./server.js"
import { EventLogger } from "./event-logger.js"
import { createMonitorHook } from "./plugin.js"

const PORT = parseInt(process.env.PORT || "7777")
const HOST = process.env.HOST || "localhost"

const logger = new EventLogger()
const server = new MonitorServer(PORT, HOST)

server.setEventFile(logger.getEventFile())

const plugin = createMonitorHook(logger.getEventFile(), (event) => {
  server.broadcast(event)
})

server.events.on("event", (event) => {
  server.broadcast(event)
})

server.start()
server.watchFile()

console.log(`Sessao: ${logger.getSessionId()}`)
console.log(`Events file: ${logger.getEventFile()}`)
console.log(`Dashboard: http://${HOST}:${PORT}`)
console.log("")
console.log("Para conectar o OpenCode, adicione este plugin:")
console.log(`  import { createMonitorHook } from "./src/plugin.js"`)
console.log(`  createMonitorHook("${logger.getEventFile()}")`)

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
