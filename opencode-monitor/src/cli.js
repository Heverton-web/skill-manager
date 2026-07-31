#!/usr/bin/env node

import { MonitorServer } from "./server.js"

const PORT = parseInt(process.env.PORT || "7777")
const HOST = process.env.HOST || "localhost"
const OPENCODE_URL = process.env.OPENCODE_URL || "http://localhost:57129"

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
