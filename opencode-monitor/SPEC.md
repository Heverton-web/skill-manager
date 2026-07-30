# SPEC — OpenCode Monitor

## Visao Geral

Dashboard web em tempo real que visualiza o fluxo interno do OpenCode, mostrando cada camada trabalhando: Usuario, Harness, LLM, Tools e Resposta.

## Problema

Quando usa o OpenCode, o usuario nao ve o que acontece nos bastidores. O fluxo de 4 camadas (Tela → Harness → LLM → Operarios) e invisivel. Isso dificulta:

- Entender como a ferramenta funciona
- Depurar problemas de tool calls
- Otimizar prompts
- Ensinar outros usuarios

## Solucao

Um dashboard web que recebe eventos em tempo real via Server-Sent Events (SSE) e mostra:

1. **Diagrama de fluxo** — nos iluminados em tempo real conforme cada camada trabalha
2. **Timeline** — historico cronologico de todos os eventos
3. **Stats** — contadores de eventos, tools calls, duracao
4. **Log completo** — todos os eventos com detalhes

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│  OpenCode (com plugin)                                  │
│  ┌─────────────────────┐                                │
│  │ plugin.js           │──── JSONL ────┐               │
│  │ captura eventos     │               │               │
│  └─────────────────────┘               ▼               │
│                               ┌─────────────────┐      │
│                               │ event-logger.js │      │
│                               │ data/sessao.jsonl│      │
│                               └────────┬────────┘      │
│                                        │               │
│  ┌─────────────────────┐               │               │
│  │ server.js           │◄──────────────┘               │
│  │ HTTP + SSE          │                               │
│  │ porta 7777          │──── SSE ──── Navegador        │
│  └─────────────────────┘                               │
└─────────────────────────────────────────────────────────┘
```

## Componentes

### 1. event-logger.js

- Gera ID unico por sessao
- Salva eventos em formato JSONL (append-only)
- Cada evento: `{ id, type, sessionId, timestamp, ...data }`
- Tipos de evento:
  - `session:create` — nova sessao
  - `session:prompt` — usuario enviou prompt
  - `session:response` — resposta enviada
  - `tool:call` — tool sendo executada
  - `tool:result` — resultado da tool
  - `llm:completion` — LLM respondeu

### 2. server.js

- Server HTTP puro (sem Express)
- Rota `/events` — SSE para browsers
- Rota `/api/events` — JSON historico
- Rota `/` e estáticos — serve `public/`
- `broadcast(event)` — envia para todos os clientes SSE

### 3. plugin.js

- Plugin para OpenCode
- Hook em todos os eventos (`event:*`)
- Emite eventos para o event-logger
- Conecta automaticamente ao server

### 4. public/index.html

- Dashboard visual responsivo
- CSS escuro (dark theme)
- Diagrama de fluxo com nos iluminados
- Timeline cronologica
- Stats em cards
- Log completo com scroll

## APIs

### Server → Browser (SSE)

```
GET /events
Content-Type: text/event-stream

data: {"type":"tool:call","tool":"bash","args":{"command":"ls"},"timestamp":1234567890}
```

### Eventos

| Tipo | Payload | Descricao |
|------|---------|-----------|
| `session:create` | `{session}` | Nova sessao OpenCode |
| `session:prompt` | `{prompt}` | Usuario digitou |
| `session:response` | `{response}` | Resposta final |
| `tool:call` | `{tool, args}` | Tool executando |
| `tool:result` | `{tool, result}` | Tool terminou |
| `llm:completion` | `{provider, model, tokens}` | LLM respondeu |

## Design Visual

### Paleta

- Fundo: `#0a0a0f`
- Superficie: `#1a1a2e`
- Borda: `#333`
- Texto: `#e0e0e0`
- Accent: `#3b82f6` (azul)
- Sucesso: `#22c55e` (verde)

### Layout

```
┌──────────────────────────────────────────┐
│  OpenCode Monitor          ● Conectado   │
├──────────────────────────────────────────┤
│                                          │
│  [USUARIO] → [HARNESS] → [LLM] → [TOOLS]│
│                                          │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │Eventos│ │Tools │ │Durac │ │Sessao│   │
│  │  42   │ │  12  │ │ 45s  │ │ a3f2 │   │
│  └──────┘ └──────┘ └──────┘ └──────┘   │
│                                          │
│  Timeline                                │
│  ──● 14:32:01 session:prompt "crie..."  │
│  ──● 14:32:03 tool:call bash(ls)        │
│  ──● 14:32:05 tool:result bash → OK     │
│                                          │
│  Log Completo                            │
│  14:32:01 session:prompt {...}           │
│  14:32:03 tool:call {...}                │
└──────────────────────────────────────────┘
```

## Stack Tecnico

- **Backend:** Node.js 18+ (puro, sem frameworks)
- **Frontend:** HTML/CSS/JS puro (sem build tools)
- **Comunicacao:** Server-Sent Events (SSE)
- **Persistencia:** JSONL (append-only)
- **Testes:** `node:test`
- **Dependencias:** nenhuma (zero deps)

## Testes

| Arquivo | Testes | Cobre |
|---------|--------|-------|
| `event-logger.test.js` | 5 | Criacao de diretorio, session ID, log JSONL, multiplos logs, caminho do arquivo |
| `server.test.js` | 4 | Instancia, start/stop, broadcast, setEventFile |

Total: 9 testes, todos passando.

## Entregaveis

1. `src/event-logger.js` — Logger de eventos
2. `src/server.js` — Server HTTP + SSE
3. `src/plugin.js` — Plugin para OpenCode
4. `src/cli.js` — CLI entry point
5. `public/index.html` — Dashboard visual
6. `test/*.test.js` — Testes (9 total)
7. `package.json` — Dependencias
8. `README.md` — Documentacao
9. `CLAUDE.md` — Instrucoes para agentes
10. `AGENTS.md` — Instrucoes para agentes
11. `.gitignore` — Arquivos ignorados
12. `.env.example` — Variaveis de ambiente

## Status

- [x] EventLogger implementado e testado (5 testes)
- [x] MonitorServer implementado e testado (4 testes)
- [x] Dashboard HTML implementado
- [x] Plugin para OpenCode implementado
- [x] CLI funcional
- [x] Documentacao completa
- [x] Testes passando (9/9)
