# CLAUDE.md — OpenCode Monitor

## O que e

Dashboard web em tempo real que visualiza o fluxo interno do OpenCode (Usuario → Harness → LLM → Tools → Resposta).

## Stack

- Node.js 18+ (sem frameworks, puro)
- Server-Sent Events (SSE) para push em tempo real
- HTML/CSS/JS puro no frontend (sem build)
- `node:test` para testes

## Comandos importantes

```bash
npm start          # Inicia server na porta 7777
npm run dev        # Inicia com auto-reload
npm test           # Roda todos os testes
```

## Estrutura

- `src/server.js` — Server HTTP + SSE
- `src/event-logger.js` — Logger de eventos em JSONL
- `src/plugin.js` — Plugin para conectar ao OpenCode
- `src/cli.js` — CLI entry point
- `public/index.html` — Dashboard visual
- `test/` — Testes

## Regras

- Zero dependencias desnecessarias (so `ws` para WebSocket se precisar)
- Testes rodando antes de commit
- HTML/CSS/JS puro no frontend (sem React/Vue/etc)
- Eventos em formato JSONL (append-only)
- Porta padrao: 7777
