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
│   ├── cli.js           # Entry point CLI
│   ├── server.js        # HTTP server + SSE + file watcher
│   ├── event-logger.js  # Logger auxiliar
│   └── plugin.js        # Referencia do plugin (nao usado diretamente)
├── .opencode/
│   └── plugins/
│       └── event-writer.js  # Plugin OpenCode (carregado pelo OpenCode)
├── public/
│   └── index.html       # Dashboard visual
├── data/                # Eventos JSONL (auto-criado)
├── test/
│   ├── event-logger.test.js
│   └── server.test.js
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

## Licenca

MIT
