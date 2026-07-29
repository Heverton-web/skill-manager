// Traduz .mcp.json (schema "mcpServers", usado por Claude Code/Cursor/Windsurf) para
// .vscode/mcp.json (schema "servers" com "type" obrigatorio por servidor, usado pelo
// VS Code/Copilot). Nao e um link porque os dois schemas sao genuinamente diferentes.
// Rode de novo sempre que .mcp.json mudar: node scripts/sync-vscode-mcp.mjs

import { readFile, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const raizProjeto = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const origem = path.join(raizProjeto, ".mcp.json");
const destinoDir = path.join(raizProjeto, ".vscode");
const destino = path.join(destinoDir, "mcp.json");

const mcpJson = JSON.parse(await readFile(origem, "utf-8"));

const servers = {};
for (const [nome, def] of Object.entries(mcpJson.mcpServers)) {
  servers[nome] = {
    type: def.url ? "http" : "stdio",
    ...(def.url ? { url: def.url } : { command: def.command, args: def.args }),
    ...(def.env ? { env: def.env } : {}),
  };
}

await mkdir(destinoDir, { recursive: true });
await writeFile(destino, JSON.stringify({ servers }, null, 2) + "\n", "utf-8");
console.log(`Gerado: ${destino} (${Object.keys(servers).length} servidores traduzidos de .mcp.json)`);
