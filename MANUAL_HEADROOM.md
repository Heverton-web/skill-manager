# Manual Completo: Headroom — Guia de Compressão de Contexto e Redução de Tokens

> **Repositório:** [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom)  
> **Documentação:** [headroom-docs.vercel.app](https://headroom-docs.vercel.app/docs)  
> **Objetivo:** Comprimir outputs de ferramentas, logs, JSONs, buscas de código e histórico em **60% a 95%**, além de reduzir o consumo de tokens de resposta (*Output Tokens*) com roteamento inteligente de esforço.

---

## 1. Visão Geral e Arquitetura

O **Headroom** é uma camada de compressão de contexto local e reversível (*Reversible Context Compression - CCR*) projetada para agentes de IA e aplicativos LLM.

### Como o Headroom opera (ContentRouter):
```
 Agente de IA / Editor (Claude Code, Cursor, Gemini, Copilot...)
                          │  Prompts, logs, JSON, arquivos, respostas
                          ▼
 ┌─────────────────────────────────────────────────────────────────┐
 │                       Headroom (Local)                          │
 │  ─────────────────────────────────────────────────────────────  │
 │  CacheAligner ──> ContentRouter                                 │
 │                    ├─ SmartCrusher (para dados JSON/objetos)    │
 │                    ├─ CodeCompressor (para arquivos e AST)      │
 │                    └─ Kompress-v2-base (para textos e logs)     │
 └─────────────────────────────────────────────────────────────────┘
                          │  Prompt Comprimido + Ferramenta de Recuperação (CCR)
                          ▼
                  Provedor de LLM (Anthropic / OpenAI / Gemini)
```

### Principais Recursos:
1. **Compressão Adaptativa:**
   * **Dados JSON / Objetos:** Redução de **60% a 95%** de tokens.
   * **Buscas de Código e Incidentes SRE:** Redução de **~90%** em saídas massivas.
2. **Reversibilidade Garantida (CCR):** O conteúdo original é armazenado em cache local e o modelo pode recuperar os dados originais se necessário através da função `headroom_retrieve`.
3. **Model Output Shaper (Redução de Output Tokens):** Controla e reduz o texto que o provedor de IA *escreve de volta* (que custa até 5x mais caro), suprimindo introduções prolixas e ajustando a janela de raciocínio (*thinking budget*) em etapas simples.
4. **Aprendizado Automático (`headroom learn`):** Examina sessões anteriores e gera regras de aprendizado direto nos arquivos de instrução do projeto (`CLAUDE.local.md`, `AGENTS.md`).

---

## 2. Instalação e Configuração

### 2.1 Instalação Global da CLI (Python / UV)

A ferramenta CLI `headroom` é disponibilizada via pacote PyPI:

#### Opção A: via UV (Recomendado - Isolado e Rápido)
```bash
uv tool install --python 3.13 "headroom-ai[all]"
```

#### Opção B: via PIP (Python 3.10+)
```bash
pip install "headroom-ai[all]"
```

---

### 2.2 Instalação no Projeto Local

#### Em Projetos Node.js / TypeScript:
```bash
npm install --save-dev headroom-ai
```

#### Em Projetos Python:
```bash
pip install "headroom-ai[all]"
```

---

### 2.3 Inicialização e Uso dos Modos de Operação

#### Modo 1: Encapsulamento de Agente (`headroom wrap`)
Inicia o proxy local do Headroom e lança uma sessão do seu agente configurada para rodar através dele:

```bash
# Para Claude Code
headroom wrap claude

# Para Cursor / Copilot / Gemini / outros
headroom wrap cursor
headroom wrap gemini
```

#### Modo 2: Proxy HTTP Transparente (`headroom proxy`)
Inicia um servidor proxy local na porta 8787 para redirecionar requisições da API da Anthropic/OpenAI:

```bash
# Rodar proxy local
headroom proxy --port 8787
```

#### Modo 3: Ativação da Redução de Tokens de Resposta (*Output Shaper*)
Para ativar o encurtador de respostas e economia de tokens de escrita do modelo:

```bash
export HEADROOM_OUTPUT_SHAPER=1
headroom proxy --port 8787
```

#### Modo 4: Servidor MCP (Model Context Protocol)
Para conectar ao Claude Desktop, Cursor ou Antigravity via MCP:

```json
{
  "mcpServers": {
    "headroom": {
      "command": "headroom",
      "args": ["mcp", "serve"]
    }
  }
}
```

---

## 3. O Quadrante Supremo da Engenharia de Contexto

Integrando o **Headroom** com o **LeanCTX**, **RTK** e **Caveman**, seu ambiente de desenvolvimento obtém o nível mais avançado de economia de contexto da indústria:

| Camada | Ferramenta | O que otimiza | Redução de Tokens |
| :--- | :--- | :--- | :---: |
| **1. Código & Cache AST** | **LeanCTX** | Leituras de arquivos, cache de AST e estrutura | **60% a 90%** |
| **2. Terminal CLI Proxy** | **RTK** | Comandos de console (`git`, `npm`, `cargo`, `docker`) | **60% a 90%** |
| **3. Respostas da IA** | **Caveman** | Estilo de escrita direto, telegráfico e sem rodeios | **~65%** |
| **4. JSON, Logs & Reversibilidade** | **Headroom** | Objetos JSON, logs massivos, RAG e Output Shaper | **60% a 95%** |

---

## 4. Comandos de Diagnóstico e Métricas

```bash
# Verificação de saúde e roteamento
headroom doctor

# Dashboard de economia em tempo real (com o proxy rodando)
headroom dashboard

# Teste de performance de compressão
headroom perf

# Analisar sessões anteriores e gerar aprendizados para o projeto
headroom learn --apply
```
