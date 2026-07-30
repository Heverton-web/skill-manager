import { describe, it } from "node:test"
import assert from "node:assert"
import { MonitorServer } from "../src/server.js"

describe("MonitorServer", () => {
  it("instancia com porta e host", () => {
    const server = new MonitorServer(8888, "127.0.0.1")
    assert.strictEqual(server.port, 8888)
    assert.strictEqual(server.host, "127.0.0.1")
  })

  it("inicia e para sem erros", () => {
    const server = new MonitorServer(9999, "127.0.0.1")
    server.start()
    server.stop()
  })

  it("broadcast envia para clientes conectados", () => {
    const server = new MonitorServer(9998, "127.0.0.1")
    server.start()

    const mockClient = {
      write: () => {},
    }
    server.clients.add(mockClient)

    let written = ""
    mockClient.write = (data) => { written = data }

    server.broadcast({ type: "test", data: "hello" })

    assert.ok(written.includes('"type":"test"'))
    assert.ok(written.includes('"data":"hello"'))

    server.clients.delete(mockClient)
    server.stop()
  })

  it("setDataDir define diretorio", () => {
    const server = new MonitorServer()
    server.setDataDir("/tmp/test-data")
    assert.strictEqual(server.dataDir, "/tmp/test-data")
  })
})
