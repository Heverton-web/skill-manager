#!/usr/bin/env bash
# Recria os links de portabilidade multi-IDE da Fabrica Agentica de Livros (macOS/Linux).
# Idempotente. Aqui symlink real de arquivo e de pasta funciona sem privilegio elevado,
# entao usamos symlink em todos os casos (equivalente ao hardlink+junction do Windows).
#
# Uso: bash scripts/setup-links.sh
set -euo pipefail

raiz="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$raiz"

link() {
  local alvo="$1" link="$2"
  if [ ! -e "$alvo" ]; then
    echo "AVISO: alvo nao encontrado, pulando: $alvo"
    return
  fi
  mkdir -p "$(dirname "$link")"
  if [ -L "$link" ]; then
    echo "OK (ja e symlink): $link"
    return
  fi
  if [ -e "$link" ]; then
    echo "AVISO: ja existe e NAO e symlink, pulando (apague manualmente se quiser recriar): $link"
    return
  fi
  ln -s "$(realpath --relative-to="$(dirname "$link")" "$alvo")" "$link"
  echo "Criado symlink: $link -> $alvo"
}

echo "== Arquivos de instrucao (symlink para CLAUDE.md) =="
link "CLAUDE.md" "AGENTS.md"
link "CLAUDE.md" ".cursor/rules/fabrica-agentica.mdc"
link "CLAUDE.md" ".windsurfrules"
link "CLAUDE.md" ".windsurf/rules/fabrica-agentica.md"
link "CLAUDE.md" ".clinerules"
link "CLAUDE.md" ".github/copilot-instructions.md"

echo
echo "== MCP (symlink para .mcp.json, schema compativel) =="
link ".mcp.json" ".cursor/mcp.json"

echo
echo "== Pastas neutras (symlink para .claude/...) =="
link ".claude/skills" "agentic/skills"
link ".claude/agents" "agentic/agents"
link ".claude/commands" "agentic/commands"
link ".claude/mcp-servers" "agentic/mcp-servers"

echo
echo "== MCP traduzido para VS Code (schema diferente, gerado por script) =="
node "$raiz/scripts/sync-vscode-mcp.mjs"

echo
echo "Concluido."
