# 🛠️ Skill Manager

> Gerenciador Multi-IDE de Agent Skills. Instale, ative, desative e gerencie skills em 13 IDEs com TUI interativa, Dashboard visual e API REST.

```bash
npm install -g @hevertonperes/skill-manager
# ou
npx @hevertonperes/skill-manager
```

## Uso Rápido

```bash
# TUI interativa (5 passos)
skill-manager

# Servidor HTTP com dashboard (toggle real de skills)
skill-manager --serve
# → http://localhost:3030

# Ajuda completa
skill-manager --help
```

## 13 IDEs Suportadas

Claude Code · Cursor · Windsurf · Codex CLI · Antigravity · OpenCode · Freebuff · MimoCode · Grok · Oh My Pi · Cline · GitHub Copilot · Custom

## Funcionalidades

- **TUI Interativa** — 5 passos guiados: selecione IDEs, escolha skills por categoria com scoring 0-100, defina escopo, confirme e instale em lote
- **Dashboard Visual** — Painel HTML com categorias, toggle switches, busca, barra de progresso
- **Servidor HTTP** — API REST real: `GET /api/config`, `POST /api/toggle`, `POST /api/save`, `GET /api/job/:id`
- **Instalação Batch** — Fallback triplo (batch completo → sub-lotes → individual)
- **482+ Skills** catalogadas em 14 categorias com scoring inteligente

## Licença

MIT
