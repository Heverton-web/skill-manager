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
  cli.js           # Entry point CLI
  server.js        # HTTP server + SSE
  event-logger.js  # Salva eventos em JSONL
  plugin.js        # Plugin para OpenCode
public/
  index.html       # Dashboard visual
test/
  *.test.js        # Testes
data/              # Eventos (auto-criado, gitignored)
```

## Regras

1. **Zero deps extras** — so `ws` se precisar de WebSocket real
2. **Testes passando** — `npm test` antes de commit
3. **Frontend puro** — sem frameworks JS, so HTML/CSS/JS
4. **JSONL append-only** — eventos sao append, nunca editados
5. **Porta 7777** — padrao, configuravel via env
