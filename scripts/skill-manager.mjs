#!/usr/bin/env node
/**
 * skill-manager.mjs — Ponto de entrada do Skill Manager
 * 
 * Uso:
 *   node scripts/skill-manager.mjs                Inicia TUI interativa
 *   node scripts/skill-manager.mjs --dashboard     Abre dashboard visual (estático)
 *   node scripts/skill-manager.mjs --serve         Inicia servidor HTTP do dashboard (com API real)
 *   node scripts/skill-manager.mjs --port=9090     Altera porta do servidor (padrão 3030)
 *   node scripts/skill-manager.mjs --help          Mostra esta ajuda
 * 
 * Aliases recomendados:
 *   alias sm="node scripts/skill-manager.mjs"
 *   Set-Alias sm "node scripts/skill-manager.mjs"
 */
import path from "node:path";
import { fileURLToPath } from "node:url";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const MAIN = path.resolve(DIR, "skill-manager", "skill-manager.mjs");

async function main() {
  const args = process.argv.slice(2);

  if (args.includes("--help") || args.includes("-h")) {
    console.log(`
🛠️  SKILL MANAGER — Gerenciador de Skills Multi-IDE

USO:
  node scripts/skill-manager.mjs                Inicia TUI interativa
  node scripts/skill-manager.mjs --dashboard     Abre dashboard visual (estático)
  node scripts/skill-manager.mjs --serve         Inicia servidor HTTP do dashboard (com API real)
  node scripts/skill-manager.mjs --port=9090     Altera porta do servidor (padrão 3030)
  node scripts/skill-manager.mjs --help          Mostra esta ajuda

ALIASES RECOMENDADOS:
  Bash/Zsh:  alias sm="node scripts/skill-manager.mjs"
  PowerShell: Set-Alias sm "node scripts/skill-manager.mjs"

FLUXO:
  1. Seleciona IDEs (Claude, Cursor, Codex, OpenCode, Freebuff, MimoCode, Grok, etc)
  2. Escolhe skills por categoria (com scoring 0-100)
  3. Define escopo (local, global, ambos)
  4. Instala dashboard visual opcional
  5. SUBMIT → instala tudo em lote (batch)
  6. Opcional: inicia servidor HTTP para toggle real de skills

IDES SUPORTADAS (13):
  Claude Code · Cursor · Windsurf · Codex CLI · Antigravity
  OpenCode · Freebuff · MimoCode · Grok · Oh My Pi
  Cline · GitHub Copilot · Custom/Genérico

DASHBOARD COM SERVIDOR:
  node scripts/skill-manager.mjs --serve
  → http://localhost:3030
  → Toggle skills com efeito real (npx skills add/remove)
  → API REST: /api/config, /api/toggle, /api/save, /api/job/:id
`);
    return;
  }

  if (args.includes("--dashboard")) {
    console.log("\n📊 Abrindo dashboard...");
    console.log(`   ${path.resolve(DIR, "skill-manager", "dashboard", "index.html")}`);
    console.log("   Abra este arquivo no navegador.");
    console.log("   Ou inicie o servidor: node scripts/skill-manager.mjs --serve\n");
    return;
  }

  if (args.includes("--serve")) {
    const portIndex = args.findIndex(a => a.startsWith("--port="));
    const port = portIndex >= 0 ? parseInt(args[portIndex].split("=")[1]) : 3030;
    const { spawn } = await import("node:child_process");
    const serverPath = path.resolve(DIR, "skill-manager", "dashboard-server.mjs");
    console.log(`\n🖥️  Iniciando servidor HTTP do dashboard na porta ${port}...`);
    console.log(`   ${'='.repeat(50)}`);
    const child = spawn("node", [serverPath, `--port=${port}`], {
      cwd: process.cwd(),
      stdio: "inherit",
      shell: true
    });
    child.on("exit", (code) => {
      process.exit(code || 0);
    });
    return;
  }

  // Iniciar TUI
  try {
    await import(MAIN);
  } catch (e) {
    console.error("ERRO ao iniciar Skill Manager:", e.message);
    process.exit(1);
  }
}

main().then(() => {}).catch(e => {
  console.error("ERRO:", e.message);
  process.exit(1);
});
