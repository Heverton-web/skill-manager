# OpenCode Monitor

Dashboard em tempo real para visualizar o fluxo interno do OpenCode.

## O que e

Um monitor que mostra visualmente cada camada do OpenCode trabalhando:

```
USUARIO → HARNESS → LLM → TOOLS → RESPOSTA
```

## Como usar

### 1. Instalar dependencias

```bash
cd opencode-monitor
npm install
```

### 2. Plugin (ja configurado)

O plugin `event-writer.js` esta instalado em `.opencode/plugins/event-writer.js` e registrado no `opencode.json` global.

Para verificar se esta carregado:

```bash
opencode debug config | grep event-writer
```

### 3. Iniciar o monitor (Terminal 1)

```bash
npm start
```

### 4. Usar o OpenCode (Terminal 2)

```bash
opencode
```

O plugin automaticamente escreve eventos em `data/*.jsonl`.

### 5. Ver o dashboard

Abra `http://localhost:7777` no navegador. Pronto!

## Arquitetura

```
┌─────────────────────────────────────────────────┐
│  OpenCode (com plugin)                           │
│  ┌───────────────────────────────────┐           │
│  │ .opencode/plugins/event-writer.js │── JSONL ─┐│
│  │ captura: event, tool.execute.*    │          ││
│  │ chat.message, session.*           │          ││
│  └───────────────────────────────────┘          ││
│                                                  ││
│  ┌───────────────────────────────────┐          ││
│  │ Terminal 1: npm start             │          ││
│  │ server.js assiste data/*.jsonl    │◄─────────┘│
│  │ SSE → navegador :7777             │           │
│  └───────────────────────────────────┘           │
└─────────────────────────────────────────────────┘
```

## Arquivos

```
opencode-monitor/
├── src/
│   ├── cli.js              # Entry point CLI
│   ├── server.js           # HTTP server + SSE + API proxy
│   ├── session-tracker.js  # Estado da sessao (tokens, cost, context)
│   ├── event-logger.js     # Logger auxiliar
│   └── plugin.js           # Plugin OpenCode hooks
├── public/
│   ├── index.html          # Dashboard visual
│   ├── app.css             # Estilos do dashboard
│   └── app.js              # JS do dashboard
├── data/                   # Eventos JSONL (auto-criado, gitignored)
├── test/
│   ├── event-logger.test.js
│   ├── server.test.js
│   └── session-tracker.test.js
└── package.json
```

## Eventos Capturados

| Tipo | Descricao |
|------|-----------|
| `event` | Evento generico do OpenCode |
| `chat.message` | Mensagem do usuario |
| `tool.execute.before` | Tool sendo executada |
| `tool.execute.after` | Tool finalizada |
| `message.updated` | Mensagem atualizada (resposta do assistente) |
| `message.part.updated` | Parte da mensagem (streaming) |
| `session.*` | Eventos de sessao |

## Comandos

| Comando | O que faz |
|---------|-----------|
| `npm start` | Inicia server na porta 7777 |
| `npm run dev` | Inicia com auto-reload |
| `npm test` | Roda os testes |

## Variaveis de ambiente

| Variavel | Default | Descricao |
|----------|---------|-----------|
| `PORT` | 7777 | Porta do server |
| `HOST` | localhost | Host do server |
| `OPENCODE_URL` | http://localhost:4096 | URL do server OpenCode para proxy |

## V2 Features

### Context Window Bar

Barra de progresso mostrando uso do contexto. Atualiza em tempo real.

- **Compact**: dispara compactacao da sessao via OpenCode
- **Clear**: cria nova sessao
- **Summarize**: gera resumo da sessao via OpenCode

### Cost & Performance Tracking

- **Tokens**: total de tokens utilizados (input + output + cache)
- **Custo**: custo acumulado da sessao em USD
- **Tokens/s**: velocidade de geracao de output
- **Status**: estado da sessao (idle/busy/retry)

### Tools Panel

Painel mostrando agentes e MCPs disponiveis. Carregado na inicializacao via API do OpenCode.

### Grouped Timeline

Eventos da timeline sao agrupados por input do usuario. Cada mensagem do usuario inicia um novo grupo, com todas as tool calls, respostas do LLM e eventos do sistema aninhados.

### API Proxy Routes

| Rota | Metodo | Descricao |
|------|--------|-----------|
| `/api/session-status` | GET | Estado da sessao (tokens, cost, context) |
| `/api/tools` | GET | Lista de agentes |
| `/api/mcp` | GET | Status dos MCPs |
| `/api/compact` | GET | Dispara compactacao |
| `/api/clear` | GET | Cria nova sessao |
| `/api/summarize` | GET | Gera resumo da sessao |

## Licenca

MIT
