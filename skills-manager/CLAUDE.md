# CLAUDE.md — Skills Manager

## O que e

Gerenciador Multi-IDE de Agent Skills. Instala, ativa, desativa e gerencia skills em 13 IDEs com TUI, Dashboard visual e API REST.

## Como usar

```bash
npm install
node scripts/skill-manager.mjs --help
```

## IDEs suportadas

Claude Code, Cursor, Windsurf, Codex CLI, Antigravity, OpenCode, Freebuff, MimoCode, Grok, Oh My Pi, Cline, GitHub Copilot, Custom

## Comandos

| Comando | O que faz |
|---------|-----------|
| `sm` | TUI interativa |
| `sm --serve` | Dashboard na porta 3030 |
| `sm --help` | Ajuda |

## Estrutura

```
scripts/
  skill-manager.mjs      # CLI principal
  skill-manager/          # Modulos internos
default-skills/           # Skills padrao
```

## Regras

- Node.js 18+
- Publicacao npm: `@hevertonperes/skill-manager`
- MIT License
