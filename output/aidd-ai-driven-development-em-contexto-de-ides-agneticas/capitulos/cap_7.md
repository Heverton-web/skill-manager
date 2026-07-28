# Capítulo 7 — Model Context Protocol: A Ponte Universal

Nos capítulos anteriores, falamos sobre coding agents, especificações e arquivos de regras. Mas um agente só é tão útil quanto as ferramentas que ele pode usar. Um agente que só escreve texto é limitado. Um agente que pode consultar bancos de dados, chamar APIs, ler sistemas de arquivos e executar comandos é transformador.

O **Model Context Protocol (MCP)**, criado pela Anthropic e adotado por OpenAI, Google, Microsoft e AWS, é o padrão aberto que tornou essa integração universal possível. Este capítulo explica sua arquitetura, primitivas e modelo de segurança.

## Arquitetura MCP: Host, Client e Server

O MCP segue uma arquitetura cliente-servidor estrita, frequentemente comparada ao "USB-C para IA" — um padrão único que conecta qualquer agente a qualquer ferramenta.

### Os três participantes

**MCP Host:** A aplicação de IA que coordena as conexões — Claude Desktop, Claude Code (CLI), Cursor, VS Code com extensão Cline, etc. O host gerencia múltiplas conexões simultâneas com diferentes servidores.

**MCP Client:** Um componente protocolar instanciado pelo host para cada servidor conectado. Cada cliente mantém uma conexão 1:1 com seu servidor correspondente.

**MCP Server:** Um programa leve que expõe funcionalidades para o agente. Pode rodar localmente (comunicação via STDIO) ou remotamente (via HTTP SSE — Server-Sent Events).

```
Host (Claude Code/Cursor)
    ├── Client A ──── Server A (Sistema de Arquivos)
    ├── Client B ──── Server B (Banco de Dados)
    └── Client C ──── Server C (API Externa via HTTP)
```

![Arquitetura MCP: Host, Client e Server](../imagens/cap_7_diagrama_1.svg)

### Camadas de transporte

O MCP suporta dois transportes:

**Stdio Transport:** Comunicação via entrada e saída padrão (STDIN/STDOUT). Ideal para servidores locais — zero overhead de rede, latência mínima, segurança simplificada. Usado para sistemas de arquivos, bancos locais, ferramentas de terminal.

**Streamable HTTP Transport:** Comunicação HTTP POST com SSE (Server-Sent Events). Para servidores remotos, suporta autenticação via bearer tokens e OAuth 2.0. Usado para APIs externas, bancos remotos, serviços SaaS.

## Primitivas do MCP: Tools, Resources, Prompts, Elicitation

O MCP define quatro primitivas fundamentais que qualquer servidor pode expor.

### Tools (Ferramentas)

Funções executáveis que o modelo de linguagem pode invocar ativamente. São definidas com schema JSON (draft 2020-12) e podem retornar texto, imagens, áudio ou recursos incorporados.

Exemplo de tool: `consultar_banco(sql: string) → { linhas: Record<string, any>[] }`

O agente decide *quando* e *com quais argumentos* chamar a ferramenta. O servidor executa e retorna o resultado. O agente pode usar o resultado para decidir os próximos passos.

### Resources (Recursos)

Fontes de dados passivas, identificadas por URI único (ex: `file:///docs/spec.md`, `database://schema/users`). O host ou o modelo pode ler esses recursos para obter contexto, mas não pode modificá-los.

Resources também suportam templates de URI (`weather://forecast/{cidade}/{data}`) para acesso dinâmico a dados.

### Prompts (Modelos de Prompt)

Modelos de instrução pré-construídos expostos pelo servidor para guiar interações específicas. São ativados pelo usuário (não pelo modelo), geralmente via comandos como `/analisar-log`.

### Elicitation (Solicitação)

Mecanismo que permite ao servidor pausar a execução e solicitar entrada do usuário — confirmação de ações destrutivas, preenchimento de formulários, autorização de operações sensíveis.

## Ciclo de vida de uma tool call

1. **initialize:** Cliente e servidor negociam capacidades e versão do protocolo
2. **tools/list:** Cliente descobre quais ferramentas o servidor oferece
3. **tools/call:** Agente decide invocar uma ferramenta com argumentos específicos
4. **Resposta:** Servidor executa e retorna resultado (ou erro)
5. **Iteração:** Agente usa o resultado para decidir próximos passos

![Ciclo de vida de uma ferramenta MCP](../imagens/cap_7_diagrama_2.svg)

### Tratamento de erros

O MCP separa erros em duas categorias:
- **Protocol Errors:** Mensagens JSON-RPC malformadas — erros de infraestrutura
- **Tool Execution Errors:** A ferramenta executou mas retornou erro (`isError: true`) — o agente recebe a descrição do erro e pode tentar novamente com argumentos ajustados

## Segurança e governança no MCP

### Human-in-the-Loop (HITL)

O protocolo exige que operações sensíveis passem por confirmação humana. Ferramentas destrutivas (deletar arquivos, modificar banco de produção, fazer deploy) devem ser anotadas como requiring human confirmation.

### Autenticação e autorização

- **Servidores locais:** Segurança por isolamento de processo — o servidor só acessa o que o usuário explicitamente configurou
- **Servidores remotos:** Bearer tokens, OAuth 2.0 com Dynamic Client Registration simplificado (SEP-991)
- **Enterprise allowlists:** Organizações podem manter listas de servidores aprovados

### Ecosystema de servidores

Milhares de servidores MCP públicos e corporativos existem em 2026, cobrindo:
- **Bancos de dados:** PostgreSQL, SQLite, MySQL, MongoDB
- **APIs:** GitHub, Slack, Jira, Notion, Google Workspace
- **Infraestrutura:** Docker, Kubernetes, AWS, Cloudflare
- **Ferramentas de dev:** Git, Filesystem, Terminal, Playwright

---

Neste capítulo, vimos a arquitetura do MCP, suas primitivas fundamentais e o modelo de segurança que viabiliza a conexão entre agentes e ferramentas. No próximo capítulo, exploraremos padrões de orquestração multi-agente para tarefas complexas.
