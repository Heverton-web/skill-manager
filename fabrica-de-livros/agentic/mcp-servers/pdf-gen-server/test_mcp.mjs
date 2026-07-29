import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { readFile } from "node:fs/promises";

const [, , command, ...rest] = process.argv;
const sep = rest.indexOf("--");
const args = sep === -1 ? rest : rest.slice(0, sep);
const callToolName = sep === -1 ? null : rest[sep + 1];

let callToolArgs = {};
if (sep !== -1 && rest[sep + 2]) {
  const raw = rest[sep + 2];
  // Detecta se é file path: começa com /, ./, ../, ~/ ou X: (Windows)
  // Um JSON inline sempre começa com { ou [
  const primeiroChar = raw.trim()[0];
  const isFilePath = primeiroChar === '/' || primeiroChar === '~' ||
    /^[A-Za-z]:[\\/]/.test(raw.trim()) ||
    /^\.[\\/]/.test(raw.trim()) ||
    /^\.\.[\\/]/.test(raw.trim());
  if (isFilePath) {
    const conteudo = await readFile(raw.trim(), "utf-8");
    callToolArgs = JSON.parse(conteudo);
  } else {
    callToolArgs = JSON.parse(raw);
  }
}

const transport = new StdioClientTransport({ command, args });
const client = new Client({ name: "fabrica-test-harness", version: "1.0.0" });

try {
  await client.connect(transport);
  const tools = await client.listTools();
  console.log("CONECTADO_OK");
  console.log("FERRAMENTAS:", JSON.stringify(tools.tools.map((t) => t.name)));
  if (callToolName) {
    const result = await client.callTool({ name: callToolName, arguments: callToolArgs });
    console.log("CHAMADA_OK isError=", !!result.isError);
    const text = result.content?.[0]?.text || "";
    console.log("TAMANHO_RESULTADO:", text.length);
    console.log("PREVIEW:", text.slice(0, 300).replace(/\n/g, " "));
  }
  await client.close();
  process.exit(0);
} catch (err) {
  console.error("ERRO:", err.message);
  process.exit(1);
}
