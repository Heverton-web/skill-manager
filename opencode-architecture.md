# Arquitetura Completa do OpenCode: Camadas e Personalização

## Visão Geral

O OpenCode opera em **10 camadas principais** e **10 subcamadas**, totalizando 20 níveis de configuração e personalização.

```
┌─────────────────────────────────────────────────┐
│  8. GERÊNCIA (MDM / Managed Settings)           │  macOS .mobileconfig, /etc/opencode/
├─────────────────────────────────────────────────┤
│  7. REMOTO (.well-known/opencode)               │  Config organizacional via API
├─────────────────────────────────────────────────┤
│  6. POLICY (policies)                           │  Allow/deny por provider, ações
├─────────────────────────────────────────────────┤
│  5. SKILLS / MCPs / ACP                         │  Capacidades externas conectadas
├─────────────────────────────────────────────────┤
│  4. AGENTS (build, plan, explore, + custom)     │  Subagents, prompts, permissões
├─────────────────────────────────────────────────┤
│  3. PLUGINS (.opencode/plugins/)                │  Event hooks, custom tools, shims
├─────────────────────────────────────────────────┤
│  2. TOOLS (operários)                           │  read, write, edit, bash, glob...
├─────────────────────────────────────────────────┤
│  1. LLM (MiMo, Claude, GPT...)                 │  Cérebro que decide
├─────────────────────────────────────────────────┤
│  0. HARNESS (eu)                                │  Orquestra tools × agents × hooks
├─────────────────────────────────────────────────┤
│  -1. TELA (TUI / Desktop / IDE / Web / CLI)     │  Interface humana
└─────────────────────────────────────────────────┘
```

---

# AS 10 CAMADAS PRINCIPAIS

---

## CAMADA 0: TELA (TUI / Desktop / IDE / Web / CLI)

**O que faz:** Interface visual onde o humano interage com o sistema. Pode ser TUI (terminal), desktop app, extensão de IDE, web ou CLI pura.

**Como faz:** Renderiza o prompt, mostra respostas, exibe indicadores de agent, diffs, notificações e atalhos. Cada interface tem seu próprio comportamento.

**Importância:** É a única camada visível ao humano. Sem ela, não há interação.

**O que personaliza:**
- `tui.json` — keybinds, scroll speed, acceleration, mouse, diff style
- Notificações sonoras e desktop (`attention`)
- Temas visuais
- Atalhos de teclado

**Como personalizar:** Criar/editar `~/.config/opencode/tui.json` ou `tui.jsonc` no projeto.

**Efeito da personalização:** Mudanças na TUI afetam **apenas a experiência visual/interação** — não afetam o LLM, tools nem agents.

---

## CAMADA 1: HARNESS (orquestrador)

**O que faz:** O engine do OpenCode que gerencia sessões, coordena agents, injeta contexto, gerencia memória, executa compaction e distribui trabalho entre subagents.

**Como faz:** Lê `AGENTS.md` + `instructions`, injeta system prompt, gerencia ciclo de vida da sessão, faz compaction automática quando o contexto lota, gerencia undo/redo via snapshots.

**Importância:** É o cérebro operacional. Sem ele, LLM e tools não se conectam.

**O que personaliza:**
- `AGENTS.md` — regras de comportamento do projeto
- `instructions` — arquivos `.md` extras no system prompt
- `default_agent` — qual agent usar por padrão
- `subagent_depth` — quantos níveis de subagents (0, 1, 2)
- `compaction` — auto, prune, reserved tokens
- `snapshot` — on/off (undo/redo)
- `share` — manual, auto, disabled

**Como personalizar:** Editar `opencode.json` e/ou `AGENTS.md`.

**Efeito:** Mudanças afetam **como o harness se comporta** — quais agents existem, como delega, quando compacta, se salva snapshots.

---

## CAMADA 2: LLM (MiMo V2.5, Claude, GPT...)

**O que faz:** O modelo de linguagem que processa o prompt e gera decisões (texto ou tool calls).

**Como faz:** Recebe system prompt + contexto + mensagem do usuário. Retorna texto ou chama tools. Cada provider tem API diferente.

**Importância:** É o "cérebro cognitivo". Toda decisão parte dele.

**O que personaliza:**
- `provider` — quais providers estão habilitados (API keys, base URLs)
- `model` — modelo principal por agent
- `small_model` — modelo leve para tarefas simples (títulos)
- `temperature` — criatividade vs determinismo
- `top_p` — diversidade de respostas
- `timeout` / `chunkTimeout` — limites de tempo
- `disabled_providers` / `enabled_providers` — whitelist/blacklist

**Como personalizar:** Editar `opencode.json` ou usar `/connect` no TUI.

**Efeito:** Trocar de LLM muda **tudo** — qualidade, velocidade, custo, capacidade de raciocínio. Um modelo ruim limita todas as outras camadas.

---

## CAMADA 3: TOOLS (Operários)

**O que faz:** Ferramentas executáveis que o LLM pode chamar: bash, read, write, edit, grep, glob, webfetch, websearch, question, todowrite, lsp, skill.

**Como faz:** Cada tool é uma função que recebe args do LLM, executa a ação no sistema e retorna resultado. O LLM decide qual tool chamar.

**Importância:** É a ponte entre "decidir" e "fazer". Sem tools, o LLM só conversa.

**O que personaliza:**
- `permission` — allow/ask/deny por tool
- `permission.bash` — granular por comando (`git *`, `rm *`)
- `permission.edit` — granular por path/glob
- `permission.external_directory` — acesso a fora do projeto
- Custom tools — tools próprias em `.opencode/tools/`

**Como personalizar:** Editar `permission` em `opencode.json` ou por agent.

**Efeito:** Permissões afetam **o que o LLM pode fazer**. Um `deny` em `edit` impede qualquer modificação de arquivo.

---

## CAMADA 4: PLUGINS (Hooks de evento)

**O que faz:** Módulos que interceptam eventos do ciclo de vida (antes/depois de tool calls, sessões, etc). Podem bloquear, modificar ou observar.

**Como faz:** Plugins exportam funções que retornam hooks. Hooks rodam em sequência antes/depois de cada evento.

**Importância:** Permite customizar o comportamento interno do harness sem modificar o código fonte.

**O que personaliza:**
- `tool.execute.before` — antes de qualquer tool call
- `tool.execute.after` — depois de qualquer tool call
- `session.idle`, `session.created`, `session.error`
- `shell.env` — injetar variáveis de ambiente
- `file.edited`, `file.watcher.updated`
- Custom tools via plugin API
- `experimental.session.compacting`

**Como personalizar:** Criar `.ts`/`.js` em `.opencode/plugins/` ou `~/.config/opencode/plugins/`. Também via npm em `plugin: [...]`.

**Efeito:** Plugins podem **bloquear tools, injetar contexto, logar tudo, notificar**, etc. São os "ganchos" que conectam o harness ao mundo externo.

---

## CAMADA 5: AGENTS (Especialistas)

**O que faz:** Agentes com prompts, modelos e permissões próprios. Cada agent tem uma personalidade e capacidades diferentes.

**Como faz:** O harness gerencia agents. Primary agents (build, plan) são os principais. Subagents (explore, general, scout) são invocados por agents ou pelo usuário via `@`.

**Importância:** Permite delegação especializada — um agent de review não deve editar, um agent de plan não deve executar bash.

**O que personaliza:**
- `agent.<name>.model` — modelo por agent
- `agent.<name>.prompt` — system prompt customizado
- `agent.<name>.permission` — permissões próprias
- `agent.<name>.temperature` — criatividade por agent
- `agent.<name>.steps` — limite de iterações
- `agent.<name>.mode` — primary, subagent, all
- `agent.<name>.hidden` — ocultar do @ autocomplete
- Agents via markdown em `.opencode/agents/*.md`

**Como personalizar:** `opencode.json` ou `.opencode/agents/*.md`.

**Efeito:** Cada agent é um "funcionário" diferente. Trocar o prompt de um agent muda **como ele interpreta tarefas**. Trocar o modelo muda **sua capacidade cognitiva**.

---

## CAMADA 6: SKILLS (Conhecimento reutilizável)

**O que faz:** Instruções em markdown que o agent pode carregar sob demanda via tool `skill`. São "manuais" que o LLM lê quando precisa.

**Como faz:** Cada skill é um `SKILL.md` em pasta própria. O LLM vê a lista de skills disponíveis e decide qual carregar.

**Importância:** Evita que o LLM "adivinhe" convenções. Skills documentam padrões específicos.

**O que personaliza:**
- Skills por projeto: `.opencode/skills/<name>/SKILL.md`
- Skills globais: `~/.config/opencode/skills/<name>/SKILL.md`
- Compatível com `.claude/skills/` e `.agents/skills/`
- Permissão por skill: `permission.skill`
- Skills por agent: `skills: ["*"]` ou lista explícita

**Como personalizar:** Criar pastas com `SKILL.md` contendo frontmatter YAML (`name`, `description`) + conteúdo.

**Efeito:** Skills dão ao LLM **conhecimento específico do projeto** sem poluir o system prompt. Carregadas sob demanda, economizam contexto.

---

## CAMADA 7: MCPs (Servidores externos)

**O que faz:** Conecta o OpenCode a serviços externos via Model Context Protocol — bancos de dados, APIs, GitHub, Sentry, etc.

**Como faz:** Servidores MCP exportam tools que aparecem junto com as built-in. Podem ser locais (executam localmente) ou remotos (HTTP).

**Importância:** Expande as capacidades do LLM para além do filesystem — acesso a APIs, dados, serviços.

**O que personaliza:**
- `mcp.<name>.type` — local ou remote
- `mcp.<name>.command` — comando para servidor local
- `mcp.<name>.url` — URL do servidor remoto
- `mcp.<name>.headers` — autenticação
- `mcp.<name>.oauth` — fluxo OAuth automático
- `mcp.<name>.enabled` — ativar/desativar
- Permissão por MCP: `"mymcp_*": "allow"` ou `"deny"`

**Como personalizar:** `opencode.json` em `mcp: {...}`.

**Efeito:** Cada MCP adiciona **novas tools** ao LLM. Mas também consome tokens de contexto — mais MCPs = mais tokens gastos.

---

## CAMADA 8: POLICY (Políticas de acesso)

**O que faz:** Controla quais providers o OpenCode PODE usar. Separado de permissions — permissions controlam tools, policies controlam providers.

**Como faz:** Array de regras `experimental.policies` com effect (allow/deny), action e resource (provider ID com wildcard).

**Importância:** É a camada de governança — impede que o LLM use providers não autorizados.

**O que personaliza:**
- `experimental.policies[].effect` — allow ou deny
- `experimental.policies[].action` — provider.use
- `experimental.policies[].resource` — provider ID com wildcard
- Substitui `disabled_providers` / `enabled_providers`

**Como personalizar:** `opencode.json` em `experimental.policies`.

**Efeito:** Uma policy `deny` em `openai` **bloqueia o provider completamente**, mesmo com credenciais configuradas.

---

## CAMADA 9: GERÊNCIA (MDM / Managed Settings)

**O que faz:** Config que o usuário NÃO pode override. Usada em ambientes corporativos.

**Como faz:** Arquivos em diretórios de sistema ou preferências macOS via MDM (.mobileconfig).

**Importância:** Garante conformidade em empresas — bloqueia providers, impede sharing, controla permissões.

**O que personaliza:**
- macOS: `/Library/Application Support/opencode/` ou `.mobileconfig` via MDM
- Linux: `/etc/opencode/`
- Windows: `%ProgramData%\opencode`
- Qualquer campo do `opencode.json`

**Como personalizar:** Via admin de TI, não pelo usuário final.

**Efeito:** Sobrescreve **tudo** — config do usuário, projeto e global. Impossível de contornar.

---

# AS 10 SUBCAMADAS

---

## SUB 1: COMPACTION (Compactação de contexto)

**O que faz:** Quando o contexto lota, resume a conversa em texto menor para continuar.

**Como faz:** LLM gera um resumo dos pontos-chave. Old messages são removidas, resumo fica como contexto.

**O que personaliza:** `compaction.auto` (true/false), `compaction.prune` (remover tool outputs antigos), `compaction.reserved` (buffer de tokens).

**Efeito:** `prune: true` economiza tokens mas perde detalhes de tools antigas.

---

## SUB 2: WATCHER (Monitor de arquivos)

**O que faz:** Monitora mudanças em arquivos do projeto e notifica o sistema.

**Como faz:** Usa file system events. Pode ignorar diretórios.

**O que personaliza:** `watcher.ignore` — padrões glob para ignorar (`node_modules/**`, `dist/**`).

**Efeito:** Menos ruído — o LLM não reage a mudanças em `node_modules`.

---

## SUB 3: FORMATTERS (Formatadores de código)

**O que faz:** Formata arquivos após write/edit automaticamente.

**Como faz:** Roda prettier, biome, ruff, etc. no arquivo modificado.

**O que personaliza:** `formatter: true/false`, por formatter (`prettier.disabled`), custom formatters com `command` + `extensions`.

**Efeito:** Código fica formatado automaticamente — menos trabalho manual.

---

## SUB 4: LSP SERVERS (Servidores de linguagem)

**O que faz:** Fornece type checking, diagnostics, go-to-definition, etc. ao harness.

**Como faz:** Inicia processos LSP (typescript, pyright, etc.) que analisam código em background.

**O que personaliza:** `lsp: true/false`, por server (`typescript.disabled`), custom servers com `command` + `extensions` + `env` + `initialization`.

**Efeito:** Diagnostics ajudam o LLM a encontrar erros — mas consomem memória e podem ficar desatualizados.

---

## SUB 5: COMMANDS (Comandos customizados)

**O que faz:** Atalhos `/comando` que enviam prompts pré-definidos ao LLM.

**Como faz:** Markdown files ou JSON definem template + opções. `/component Button` injeta o prompt com `$ARGUMENTS`.

**O que personaliza:** Template, description, agent, model, subtask, suporte a `$ARGUMENTS`, `$1`, shell output, file references.

**Efeito:** Comandos repetitivos ficam em um atalho — `/test`, `/deploy`, `/review`.

---

## SUB 6: KEYBINDS (Atalhos de teclado)

**O que faz:** Mapeia teclas para ações no TUI.

**Como faz:** Merge com defaults built-in. Só precisa configurar o que mudar.

**O que personaliza:** `tui.json` → `keybinds.<action>` — ex: `"command_list": "ctrl+p"`.

**Efeito:** Fluxo de trabalho mais rápido — teclas familiares.

---

## SUB 7: THEMES (Temas visuais)

**O que faz:** Controla cores, fontes e aparência do TUI.

**Como faz:** Temas built-in ou custom. Aplicam paleta de cores consistente.

**O que personaliza:** `tui.json` → `"theme": "tokyonight"` ou temas custom.

**Efeito:** Visual mais confortável para sessões longas.

---

## SUB 8: SHARING (Compartilhamento)

**O que faz:** Gera links públicos de conversas para colaboração.

**Como faz:** Sincroniza histórico com servidores OpenCode. URL: `opncd.ai/s/<id>`.

**O que personaliza:** `share: "manual"` / `"auto"` / `"disabled"`.

**Efeito:** `"disabled"` impede qualquer sharing — importante para código sensível.

---

## SUB 9: SNAPSHOT (Snapshots de undo/redo)

**O que faz:** Salva estado dos arquivos antes de cada operação do agent. Permite undo/redo.

**Como faz:** Git interno rastreia mudanças. `/undo` reverte.

**O que personaliza:** `snapshot: true/false`.

**Efeito:** `false` desabilita undo — mas economiza disco em repositórios grandes.

---

## SUB 10: VARIABLES (Substituição de variáveis)

**O que faz:** Permite usar `{env:VAR}` e `{file:path}` em configs.

**Como faz:** Substitution no carregamento do config.

**O que personaliza:** Qualquer campo do `opencode.json` pode usar variáveis:
- `{env:ANTHROPIC_API_KEY}` — lê de env var
- `{file:~/.secrets/key}` — lê conteúdo de arquivo

**Efeito:** API keys e configs sensíveis ficam fora do JSON — segurança e flexibilidade.

---

# Resumo Visual das Precedências

```
CONFIG PRECEDENCE (de menor pra maior prioridade):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Remote config (.well-known/opencode)
2. Global config (~/.config/opencode/opencode.json)
3. Custom config (OPENCODE_CONFIG env)
4. Project config (opencode.json no projeto)
5. .opencode/ directories
6. Inline config (OPENCODE_CONFIG_CONTENT env)
7. Managed settings (/etc/opencode/ ou /Library/Application Support/)
8. macOS MDM preferences (.mobileconfig)
```

```
CAMADAS (ordem de precedência, de baixo pra cima):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. GERÊNCIA        ← admin sobrescreve tudo
8. POLICY          ← bloqueia providers
7. MCPs            ← tools externas
6. SKILLS          ← conhecimento reutilizável
5. AGENTS          ← especialistas com personalidade
4. PLUGINS         ← hooks de evento
3. TOOLS           ← operários executam
2. LLM             ← decide
1. HARNESS         ← orquestra
0. TELA            ← humano interage

SUBCAMADAS (suportam as principais):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Compaction │ Watcher │ Formatters │ LSP │ Commands
Keybinds   │ Themes  │ Sharing    │ Snapshot │ Variables
```

---

*Gerado em 30/07/2026 — OpenCode Architecture Reference*
