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

### 2. Iniciar o monitor

```bash
npm start
# ou
node src/cli.js
```

O monitor abre em `http://localhost:7777`.

### 3. Conectar ao OpenCode

Adicione o plugin no seu `.opencode/plugins/`:

```typescript
import { createMonitorHook } from "../opencode-monitor/src/plugin.js"

export default () => createMonitorHook()
```

### 4. Ver o dashboard

Abra `http://localhost:7777` no navegador. Pronto!

## Arquitetura

```
opencode-monitor/
├── src/
│   ├── cli.js           # Entry point CLI
│   ├── server.js        # HTTP server + SSE
│   ├── event-logger.js  # Salva eventos em JSONL
│   └── plugin.js        # Plugin para OpenCode
├── public/
│   └── index.html       # Dashboard visual
├── test/
│   ├── event-logger.test.js
│   └── server.test.js
└── data/                # Eventos (auto-criado)
```

## Comandos

| Comando | O que faz |
|---------|-----------|
| `npm start` | Inicia o server na porta 7777 |
| `npm run dev` | Inicia com auto-reload |
| `npm test` | Roda os testes |

## Variaveis de ambiente

| Variavel | Default | Descricao |
|----------|---------|-----------|
| `PORT` | 7777 | Porta do server |
| `HOST` | localhost | Host do server |

## Licenca

MIT
