---
description: Instrucoes para agentes de IA trabalhando no OpenCode Monitor
alwaysApply: true
---

# AGENTS.md — OpenCode Monitor

## Contexto

Dashboard web em tempo real que visualiza o fluxo interno do OpenCode. Mostra cada camada (Usuario → Harness → LLM → Tools → Resposta) trabalhando, com timeline, stats e log completo.

## Stack

- Node.js 18+ (puro, sem Express/Koa/etc)
- Server-Sent Events (SSE) para push em tempo real
- HTML/CSS/JS puro no frontend (sem build tools)
- `node:test` para testes
- JSONL para persistencia de eventos

## Comandos

```bash
npm start          # Inicia server na porta 7777
npm run dev        # Inicia com auto-reload (node --watch)
npm test           # Roda todos os testes
```

## Estrutura de arquivos

```
src/
  cli.js              # Entry point CLI
  server.js           # HTTP server + SSE + API proxy
  session-tracker.js  # Estado da sessao (tokens, cost, context)
  event-logger.js     # Salva eventos em JSONL
  plugin.js           # Plugin para OpenCode
public/
  index.html          # Dashboard visual
  app.css             # Estilos
  app.js              # JS do dashboard
test/
  *.test.js           # Testes
data/                 # Eventos (auto-criado, gitignored)
```

## Arquitetura V2

```
OpenCode (plugin) → JSONL → server.js → SSE → browser
                         ↓
                   session-tracker.js (tokens, cost, context, tools)
                         ↓
                   /api/* routes (proxy para OpenCode SDK)
```

## Regras Gerais e Economia Severa de Tokens

1. **Estilo Caveman Ativo:** Pensamento em formato telegráfico (máx 3-5 linhas). Comunicação sem preâmbulos, saudações ou palavras vazias. Preservar termos técnicos e idioma PT-BR.
2. **Compressão Headroom & RTK:** Todo log, JSON ou output de comando > 7 linhas DEVE ser comprimido via `headroom` (topo 3 + fim 4) e filtrado via `rtk`.
3. **Seleção Cirúrgica (LeanCTX):** Usar `grep_search` antes de abrir arquivos e limitar a leitura com `StartLine`/`EndLine`.
4. **Subagentes Cavecrew:** Usar a skill `cavecrew` para buscas ou edições extensas.
5. **Zero deps extras** — so `ws` se precisar de WebSocket real.
6. **Testes passando** — `npm test` antes de commit.
7. **Frontend puro** — sem frameworks JS, so HTML/CSS/JS.
8. **JSONL append-only** — eventos sao append, nunca editados.
9. **Porta 7777** — padrao, configuravel via env.
