import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const [, , command, ...rest] = process.argv;
const sep = rest.indexOf("--");
const args = sep === -1 ? rest : rest.slice(0, sep);
const callToolName = sep === -1 ? null : rest[sep + 1];
const callToolArgs = sep === -1 ? null : JSON.parse(rest[sep + 2] || "{}");

const transport = new StdioClientTransport({ command, args });
const client = new Client({ name: "fabrica-test-harness", version: "1.0.0" });

try {
  await client.connect(transport);
  const tools = await client.listTools();
  console.log("CONECTADO_OK");
  console.log("FERRAMENTAS:", JSON.stringify(tools.tools.map((t) => t.name)));
  if (callToolName) {
    const result = await client.callTool({ name: callToolName, arguments: callToolArgs });
    console.log("CHAMADA_OK");
    const text = result.content?.[0]?.text || "";
    console.log("TAMANHO_RESULTADO:", text.length);
    console.log("PREVIEW:", text.slice(0, 150).replace(/\n/g, " "));
  }
  await client.close();
  process.exit(0);
} catch (err) {
  console.error("ERRO:", err.message);
  process.exit(1);
}
