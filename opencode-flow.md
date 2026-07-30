# O Que Acontece Quando Você Digita Um Prompt No OpenCode

## Uma explicação completa, do início ao fim, de cada etapa que ocorre nos bastidores

---

## Indice

1. Visao Geral do Fluxo
2. Etapa 1 — O Usuario Digita Na Tela
3. Etapa 2 — O Harness Intercepta O Prompt
4. Etapa 3 — Construcao Do System Prompt
5. Etapa 4 — Montagem Do Pacote Completo
6. Etapa 5 — Tokenizacao (Quebra Em Pedacinhos)
7. Etapa 6 — O LLM Recebe E Processa
8. Etapa 7 — O Pensamento Do LLM
9. Etapa 8 — Decisao Probabilistica
10. Etapa 9 — A Resposta JSON Volta Para O Harness
11. Etapa 10 — Os Operarios Executam
12. Etapa 11 — Hooks Dos Plugins Interceptam
13. Etapa 12 — Resultado Volta Para O LLM
14. Etapa 13 — Resposta Final Ao Usuario
15. Resumo Do Ciclo Completo

---

## 1. Visão Geral do Fluxo

Imagine que o OpenCode é uma **fábrica com 4 departamentos**:

```
USUÁRIO
   │
   ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  TELA   │───▶│ HARNESS │───▶│   LLM   │───▶│OPERÁRIOS│
│ (TUI)   │◀───│ (eu)    │◀───│ (cérebro│◀───│ (tools) │
└─────────┘    └─────────┘    │  MiMo)  │    └─────────┘
                  │            └─────────┘         │
                  │                                │
                  ▼                                │
             ┌─────────┐                           │
             │ PLUGINS │◀──────────────────────────┘
             │ (ganchos)│
             └─────────┘
```

Cada mensagem que você digita percorre **todos esses departamentos** antes de voltar a você. Vamos ver cada etapa em detalhe.

---

## 2. Etapa 1 — O Usuário Digita Na Tela

**O que acontece:** Você abre o terminal, digita uma mensagem e aperta Enter.

**Exemplo:** `"Crie uma função em Python que soma dois números"`

**O que a Tela faz:**
- Captura o texto que você digitou
- Identifica qual **agent** está ativo (build, plan, ou outro)
- Identifica qual **modelo** está selecionado (MiMo V2.5, Claude, etc.)
- Envia tudo isso para o Harness via HTTP (o TUI é um cliente HTTP que fala com o servidor OpenCode)

**Detalhe técnico:** O TUI não processa nada — ele é apenas a "janela" por onde você fala. Toda a inteligência fica no Harness.

---

## 3. Etapa 2 — O Harness Intercepta O Prompt

**O que acontece:** O Harness (que é o engine do OpenCode) recebe seu prompt e começa a trabalhar.

**O que o Harness faz nesta etapa:**

### 3.1. Identifica o Contexto
- Qual é o projeto atual? (ele lê o `opencode.json`)
- Qual agent está ativo? (build, plan, ou um custom)
- Qual modelo está configurado? (ex: MiMo V2.5)
- Quais permissões esse agent tem? (pode editar? pode rodar bash?)

### 3.2. Carrega as Regras do Projeto
- Lê o `AGENTS.md` — as regras do projeto
- Lê arquivos de `instructions` — regras extras configuradas
- Lê os `CLAUDE.md` se existirem (compatibilidade)

### 3.3. Carrega os Skills Disponíveis
- Escaneia `.opencode/skills/*/SKILL.md`
- Escaneia `~/.config/opencode/skills/*/SKILL.md`
- Monta a lista de skills que o LLM pode usar

### 3.4. Carrega as Tools Disponíveis
- Lista todas as tools built-in (bash, read, write, edit, grep, glob, etc.)
- Lista MCPs conectados (Supabase, Context7, etc.)
- Lista custom tools
- Para cada tool, verifica qual permissão está configurada

**Neste momento, o Harness monta uma "missão" para o LLM:**

```
"Você é o agente build do OpenCode.
Aqui estão as regras do projeto: [AGENTS.md]
Aqui estão as skills disponíveis: [lista]
Aqui estão as tools que você pode usar: [lista com permissões]
Aqui está a mensagem do usuário: [seu prompt]"
```

---

## 4. Etapa 3 — Construção Do System Prompt

**O que acontece:** O Harness monta o **system prompt** completo — o "manual de instruções" que o LLM recebe antes de qualquer mensagem.

**O system prompt é composto por várias partes, na seguinte ordem:**

### 4.1. Identidade do Agent
```
Você é o agente "build" do OpenCode.
Seu papel é ajudar o desenvolvedor a implementar código.
```

### 4.2. Regras do Projeto (AGENTS.md)
```
# Regras do Projeto
- Use TypeScript com strict mode
- Siga o padrão REST para APIs
- Nunca commite chaves de acesso
```

### 4.3. Instruções Extras (instructions)
```
# Diretrizes de Código
- Prefira funções puras
- Use async/await em vez de callbacks
```

### 4.4. Skills Disponíveis
```
<available_skills>
  <skill>
    <name>simplify</name>
    <description>Simplifica código para clareza</description>
  </skill>
  <skill>
    <name>tdd</name>
    <description>Test-driven development</description>
  </skill>
</available_skills>
```

### 4.5. Tools Disponíveis (com schemas JSON)
```
Você tem acesso às seguintes ferramentas:

1. bash - Execute comandos no terminal
   Argumentos: { command: string }
   
2. read - Leia arquivos
   Argumentos: { filePath: string, offset?: number, limit?: number }
   
3. edit - Edite arquivos
   Argumentos: { filePath: string, oldString: string, newString: string }
   
4. write - Escreva arquivos
   Argumentos: { content: string, filePath: string }
```

### 4.6. Contexto da Sessão
```
Mensagens anteriores desta conversa:
[Usuário]: "Crie uma função em Python que soma dois números"
```

**IMPORTANTE:** Tudo isso é enviado como UM ÚNICO payload para o LLM. O LLM não vê "partes" — ele vê um bloco gigante de texto.

---

## 5. Etapa 4 — Montagem Do Pacote Completo

**O que acontece:** O Harness monta o **payload HTTP** que será enviado ao provider do LLM.

**Estrutura simplificada do payload:**

```json
{
  "model": "mimo-v2.5",
  "messages": [
    {
      "role": "system",
      "content": "[TODO O SYSTEM PROMPT COMPLETO]"
    },
    {
      "role": "user", 
      "content": "Crie uma função em Python que soma dois números"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "bash",
        "description": "Execute comandos no terminal",
        "parameters": {
          "type": "object",
          "properties": {
            "command": {
              "type": "string",
              "description": "Comando a ser executado"
            }
          },
          "required": ["command"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "write",
        "description": "Escreva conteúdo em um arquivo",
        "parameters": {
          "type": "object",
          "properties": {
            "filePath": { "type": "string" },
            "content": { "type": "string" }
          },
          "required": ["filePath", "content"]
        }
      }
    }
  ],
  "temperature": 0.7,
  "stream": true
}
```

**Notas importantes:**
- `temperature: 0.7` controla a criatividade (0 = determinístico, 1 = criativo)
- `stream: true` significa que o LLM responde em pedacinhos (tokens), não tudo de uma vez
- Cada tool tem um **schema JSON** que diz ao LLM quais argumentos pode passar
- O system prompt pode ter **milhares de tokens** — depende do projeto

---

## 6. Etapa 5 — Tokenização (Quebra Em Pedacinhos)

**O que acontece:** Antes de enviar ao LLM, o texto é quebrado em **tokens**.

**O que é um token?**
- Um token é um pedacinho de texto
- Pode ser uma palavra inteira, parte de uma palavra, ou até um caractere
- Exemplos:
  - `"banana"` → 1 token
  - `"opencode"` → 2 tokens (`"open"` + `"code"`)
  - `"Crie uma função"` → 4 tokens

**Por que tokenizar?**
- LLMs não entendem texto — entendem números
- Cada token vira um número (ID) na tabela do modelo
- O modelo precisa saber quantos tokens cabem no contexto (limite)

**Exemplo de contagem:**
```
System prompt: ~3.000 tokens
Mensagem do usuário: ~20 tokens
Total: ~3.020 tokens
Limite do MiMo V2.5: 1.048.576 tokens
Espaço restante: 1.045.556 tokens
```

**O que acontece se o contexto lotar?**
- O Harness detecta que está perto do limite
- Roda a **compaction** — resume as mensagens antigas
- Remove tool outputs antigos (se `prune: true`)
- Mantém apenas o essencial

---

## 7. Etapa 6 — O LLM Recebe E Processa

**O que acontece:** O payload HTTP chega ao servidor do LLM (MiMo V2.5, Claude, etc.).

**O que o LLM faz:**

### 7.1. Decodifica os Tokens
- Cada ID numérico vira um token de texto
- O modelo "vê" o system prompt + sua mensagem + lista de tools

### 7.2. Processa via Attention (Mecanismo de Atenção)
- O modelo analisa **cada token em relação a todos os outros**
- Exemplo: quando lê `"soma"`, presta atenção em `"Python"` e `"dois números"`
- É como se o modelo "lecbrasse" de todas as palavras relevantes simultaneamente

### 7.3. Camadas de Processamento
- O MiMo V2.5 tem **múltiplas camadas** (layers)
- Cada camada processa a informação de forma diferente
- Camadas iniciais: entendem palavras e gramática
- Camadas intermediárias: entendem significado e contexto
- Camadas finais: decidem ação e geram resposta

---

## 8. Etapa 7 — O Pensamento Do LLM

**O que acontece:** O LLM "pensa" internamente antes de responder.

**Como o "pensamento" funciona:**

### 8.1. Análise do Pedido
O LLM interpreta sua mensagem:
- "O usuário quer uma função em Python"
- "A função deve somar dois números"
- "Devo criar um arquivo .py ou apenas mostrar o código?"

### 8.2. Avaliação das Tools
O LLM olha as tools disponíveis e decide:
- "Posso usar `write` para criar um arquivo"
- "Posso usar `bash` para rodar o código"
- "Ou posso apenas mostrar o código como texto"

### 8.3. Geração de Probabilidades
Para cada token que pode gerar, o modelo calcula probabilidades:

```
Próximo token "A": 35% de chance
Próximo token "def": 25% de chance
Próximo token "```python": 20% de chance
Próximo token "Claro": 15% de chance
Outros tokens: 5% de chance
```

### 8.4. Sampling (Amostragem)
- O modelo escolhe o token com base nas probabilidades
- Com `temperature: 0.7`, há variação (não é sempre o mais provável)
- Com `temperature: 0`, seria sempre o mais provável (determinístico)

---

## 9. Etapa 8 — Decisão Probabilística

**O que acontece:** O LLM decide se vai **responder com texto** ou **chamar uma tool**.

**Cenário A — Responder com texto:**
```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "Claro! Aqui está a função em Python:"
    }
  }]
}
```

**Cenário B — Chamar uma tool:**
```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": null,
      "tool_calls": [{
        "id": "call_abc123",
        "type": "function",
        "function": {
          "name": "write",
          "arguments": "{\"filePath\": \"soma.py\", \"content\": \"def soma(a, b):\\n    return a + b\\n\\nprint(soma(3, 5))\"}"
        }
      }]
    }
  }]
}
```

**Notas importantes:**
- O LLM **não executa** a tool — ele apenas **declara** que quer executar
- O `tool_calls` é apenas uma **intenção** em formato JSON
- Quem executa de verdade é o Harness

---

## 10. Etapa 9 — A Resposta JSON Volta Para O Harness

**O que acontece:** O payload de resposta chega ao Harness via HTTP.

**O que o Harness faz:**

### 10.1. Parseia a Resposta
- Lê o JSON que o LLM retornou
- Identifica: é texto? é tool_call? são ambos?

### 10.2. Se For Texto
- Envia o texto para a TUI exibir
- Pode ser streaming (token por token) ou completo
- Na TUI, você vê o texto aparecendo aos poucos

### 10.3. Se For Tool Call
- Extrai o nome da tool e os argumentos
- **NÃO executa ainda** — primeiro verifica permissões

### 10.4. Verificação de Permissões
```
Tool: write
Permissão: allow (ou ask, ou deny)
Resultado: PERMITIDO → pode executar
```

Se a permissão for `ask`:
- O Harness pausa a execução
- Mostra na TUI: "O agente quer usar a tool 'write' no arquivo 'soma.py'. Permitir?"
- Você clica: once / always / reject

---

## 11. Etapa 10 — Os Operários Executam

**O que acontece:** O Harness delega a execução para os **operários** (tool calls).

### 11.1. Preparação
O Harness monta os dados para a tool:

```json
{
  "tool": "write",
  "args": {
    "filePath": "soma.py",
    "content": "def soma(a, b):\n    return a + b\n\nprint(soma(3, 5))"
  }
}
```

### 11.2. Execução
- O operário `write` cria o arquivo `soma.py` no disco
- O operário é uma **função TypeScript** que faz a ação real
- Não é o LLM que escreve — é o código do OpenCode

### 11.3. Captura do Resultado
O operário retorna o resultado:

```json
{
  "success": true,
  "output": "Arquivo criado com sucesso: soma.py",
  "filePath": "soma.py"
}
```

### 11.4. Outros Exemplos de Operários

| Operário | O que faz | Exemplo de resultado |
|----------|-----------|---------------------|
| `bash` | Roda comando no terminal | `"$ python soma.py\n8"` |
| `read` | Lê conteúdo de arquivo | `"def soma(a, b):\n    return a + b"` |
| `edit` | Edita parte de um arquivo | `"Edição aplicada com sucesso"` |
| `grep` | Busca em arquivos | `"Encontrado em soma.py:1"` |
| `glob` | Busca arquivos por padrão | `"soma.py, teste_soma.py"` |
| `webfetch` | Baixa conteúdo de URL | `"<html>...</html>"` |

---

## 12. Etapa 11 — Hooks Dos Plugins Interceptam

**O que acontece:** Enquanto o operário executa, os **plugins** podem interceptar.

### 12.1. Hook ANTES da Execução (`tool.execute.before`)

O Harness pergunta a cada plugin: "Alguém quer fazer algo ANTES de executar esta tool?"

```javascript
// Plugin: env-protection.ts
"tool.execute.before": async (input, output) => {
  if (input.tool === "read" && output.args.filePath.includes(".env")) {
    throw new Error("Access to .env files is blocked")
  }
}
```

**Exemplo prático:**
- Operário vai ler `.env`
- Plugin `env-protection` intercepta
- Lança erro → execução é bloqueada
- O LLM recebe a mensagem de erro e decide o que fazer

### 12.2. Hook DEPOIS da Execução (`tool.execute.after`)

Após o operário terminar, o Harness pergunta aos plugins: "Alguém quer fazer algo DEPOIS?"

```javascript
// Plugin: tool-logger.ts
"tool.execute.after": async (input, output) => {
  await client.app.log({
    body: {
      service: "tool-logger",
      level: "info",
      message: `Tool "${input.tool}" executed`,
      extra: { tool: input.tool, success: !output.error }
    }
  })
}
```

### 12.3. Outros Hooks Disponíveis

| Hook | Quando dispara | Exemplo de uso |
|------|----------------|----------------|
| `session.idle` | Sessão completa | Notificar usuário |
| `session.error` | Erro na sessão | Log de erro |
| `shell.env` | Antes de bash | Injetar variáveis |
| `file.edited` | Após editar arquivo | Auto-formatter |
| `permission.asked` | Pedido de permissão | Auto-aprovar |

### 12.4. Ordem de Execução dos Hooks
```
1. tool.execute.before (plugin 1)
2. tool.execute.before (plugin 2)
3. tool.execute.before (plugin N)
4. OPERÁRIO EXECUTA
5. tool.execute.after (plugin 1)
6. tool.execute.after (plugin 2)
7. tool.execute.after (plugin N)
```

Todos os plugins rodam em sequência. Se qualquer um lançar erro, a execução para.

---

## 13. Etapa 12 — Resultado Volta Para O LLM

**O que acontece:** O resultado da tool é enviado de volta ao LLM como uma nova mensagem.

**O payload agora tem mais uma mensagem:**

```json
{
  "messages": [
    { "role": "system", "content": "[system prompt]" },
    { "role": "user", "content": "Crie uma função..." },
    { "role": "assistant", "content": null, "tool_calls": [...] },
    { 
      "role": "tool", 
      "content": "Arquivo criado com sucesso: soma.py",
      "tool_call_id": "call_abc123"
    }
  ]
}
```

**O que o LLM faz com isso:**
- Lê o resultado da tool
- Decide se precisa fazer mais alguma coisa
- Pode chamar outra tool ou dar a resposta final

**Exemplo de ciclo completo:**
```
1. Usuário: "Crie uma função e teste ela"
2. LLM → tool: write("soma.py", "def soma...")
3. Tool → LLM: "Arquivo criado"
4. LLM → tool: bash("python soma.py")
5. Tool → LLM: "8"
6. LLM → Usuário: "Arquivo criado e teste passou! Resultado: 8"
```

Este ciclo pode se repetir **N vezes** até o LLM decidir que terminou.

---

## 14. Etapa 13 — Resposta Final Ao Usuário

**O que acontece:** O LLM gera a resposta final em texto.

**O que a Tela faz:**
- Recebe o texto do Harness
- Renderiza na tela do terminal
- Mostra formatação (negrito, código, etc.)
- Exibe indicadores (qual agent, qual modelo)

**Se a resposta contém código:**
- A TUI pode colorir a sintaxe
- Mostra o diff se houve edições
- Exibe os arquivos que foram criados/modificados

**Se a resposta é streaming:**
- Cada token aparece na tela assim que chega
- Você vê o texto sendo "digitado" em tempo real
- É como se o LLM estivesse digitando na sua frente

---

## 15. Resumo Do Ciclo Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    CICLO COMPLETO                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. USUÁRIO digita na TELA                                   │
│     │                                                       │
│  2. TELA envia para o HARNESS                               │
│     │                                                       │
│  3. HARNESS monta o SYSTEM PROMPT                           │
│     │  • Identidade do agent                                │
│     │  • Regras do projeto (AGENTS.md)                      │
│     │  • Skills disponíveis                                 │
│     │  • Tools com schemas JSON                             │
│     │  • Histórico da conversa                              │
│     │                                                       │
│  4. HARNESS TOKENIZA o texto                                │
│     │  • Quebra em tokens (pedacinhos)                      │
│     │  • Converte para números                              │
│     │                                                       │
│  5. HARNESS envia PAYLOAD ao LLM                            │
│     │  • POST HTTP para API do provider                     │
│     │  • System prompt + mensagem + tools                   │
│     │                                                       │
│  6. LLM PROCESSA                                            │
│     │  • Decodifica tokens                                  │
│     │  • Roda mecanismo de attention                        │
│     │  • Passa pelas camadas de rede neural                 │
│     │                                                       │
│  7. LLM PENSA                                               │
│     │  • Interpreta o pedido                                │
│     │  • Avalia tools disponíveis                           │
│     │  • Calcula probabilidades                             │
│     │                                                       │
│  8. LLM DECIDE                                              │
│     │  • Responder com texto?                               │
│     │  • Chamar uma tool?                                   │
│     │  • Gerar JSON com intenção                            │
│     │                                                       │
│  9. HARNESS RECEBE a resposta                               │
│     │  • Parseia o JSON                                     │
│     │  • Verifica permissões                                │
│     │  • Pede aprovação se necessário                       │
│     │                                                       │
│ 10. OPERÁRIOS EXECUTAM                                      │
│     │  • bash, read, write, edit, etc.                      │
│     │  • Cada um faz sua tarefa                             │
│     │  • Retorna resultado                                  │
│     │                                                       │
│ 11. PLUGINS INTERCEPTAM                                     │
│     │  • Hooks ANTES da execução                            │
│     │  • Hooks DEPOIS da execução                           │
│     │  • Podem bloquear, modificar ou observar              │
│     │                                                       │
│ 12. RESULTADO volta ao LLM                                  │
│     │  • LLM lê o resultado                                │
│     │  • Decide se precisa de mais ações                    │
│     │  • Se sim, volta ao passo 6                           │
│     │  • Se não, gera resposta final                        │
│     │                                                       │
│ 13. RESPOSTA final volta ao USUÁRIO                         │
│     │  • Texto renderizado na TELA                          │
│     │  • Streaming token por token                          │
│     │  • Código colorido, diffs mostrados                   │
│     │                                                       │
│     ▼                                                       │
│  FIM DO CICLO (ou volta ao passo 1 se o LLM              │
│                 chamou mais tools)                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Exemplo Prático: Do Início Ao Fim

Vamos acompanhar o que acontece quando você digita:

> `"Crie uma função Python que soma dois números e teste ela"`

### Passo 1: TELA captura e envia
```
Prompt: "Crie uma função Python que soma dois números e teste ela"
Agent: build
Model: MiMo V2.5
```

### Passo 2: HARNESS monta system prompt
```
"Você é o agente build. Regras: use Python 3.10+, siga PEP 8.
Tools disponíveis: bash, write, read, edit, grep, glob..."
```

### Passo 3: TOKENIZAÇÃO
```
"Crie" → token 1
"uma" → token 2
"função" → token 3
... (aprox. 20 tokens)
```

### Passo 4: LLM recebe e processa
```
MiMo V2.5 roda 32+ camadas de rede neural
Mecanismo de attention conecta "função" com "Python" e "teste"
```

### Passo 5: LLM DECIDE chamar tool
```json
{
  "tool_calls": [{
    "function": {
      "name": "write",
      "arguments": "{\"filePath\": \"soma.py\", \"content\": \"def soma(a, b):\\n    return a + b\\n\\nprint(soma(3, 5))\"}"
    }
  }]
}
```

### Passo 6: HARNESS verifica permissão
```
Tool: write → Permissão: allow → EXECUTAR
```

### Passo 7: OPERÁRIO write executa
```
Cria arquivo soma.py com o conteúdo
Resultado: "Arquivo criado: soma.py"
```

### Passo 8: PLUGIN tool-logger registra
```
Log: "Tool 'write' executed - success: true"
```

### Passo 9: RESULTADO volta ao LLM
```
"Arquivo criado: soma.py"
```

### Passo 10: LLM DECIDE chamar outra tool
```json
{
  "tool_calls": [{
    "function": {
      "name": "bash",
      "arguments": "{\"command\": \"python soma.py\"}"
    }
  }]
}
```

### Passo 11: OPERÁRIO bash executa
```
$ python soma.py
8
Resultado: "8"
```

### Passo 12: RESULTADO volta ao LLM
```
"8"
```

### Passo 13: LLM GERA RESPOSTA FINAL
```
"Criei o arquivo soma.py com a função:

def soma(a, b):
    return a + b

Executei o teste e o resultado foi 8 (soma de 3 + 5)."
```

### Passo 14: TELA exibe ao usuário
```
Criei o arquivo soma.py com a função:

def soma(a, b):
    return a + b

Executei o teste e o resultado foi 8 (soma de 3 + 5).
```

---

## Dados Curiosos

- **Tokens por segundo:** O MiMo V2.5 gera entre 20-50 tokens por segundo
- **Tamanho do system prompt:** Pode variar de 500 a 10.000+ tokens
- **Ciclos de tool calls:** Uma sessão pode ter de 0 a 50+ ciclos
- **Plugins:** Podem adicionar latência de 1-10ms por hook
- **Compaction:** Quando o contexto lota, o resumo pode ter 1.000-3.000 tokens

---

*Referência técnica completa do fluxo de execução do OpenCode.*
*Gerado em 30/07/2026.*
