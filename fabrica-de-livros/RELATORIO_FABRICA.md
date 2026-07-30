# Relatório de Construção — Fábrica Agêntica de Livros

Data: 28/07/2026

> **Nota (30/07/2026):** Toda a geração de imagens foi removida do processo ativo.
> Foram deletados: `image-gen-server/` (MCP), `subagente-ilustrador`, `subagente-design-por-parte`,
> `subagente-arte-final`, skill `diretor-arte`, script `extrair-selo-svg.mjs`.
> O conteúdo abaixo documenta o estado histórico da fábrica e pode conter referências
> a esses componentes que já não fazem mais parte do fluxo operacional.
> Ver `docs/fluxo-fabrica-de-livros.md` para o fluxo atual.
Diretório do projeto: `C:\Users\trcnologia\Desktop\proj_livros`

## 1. Contexto e decisões de arquitetura

O projeto partiu de uma especificação conceitual (mapa de fases, squad de skills, MCPs,
regras e templates) para uma "fábrica agêntica" de produção de livros técnicos. O
diretório estava vazio; três decisões arquiteturais foram alinhadas com o operador
antes de iniciar a construção:

1. **Skills como Claude Code Skills nativas** (`.claude/skills/*/SKILL.md`), em vez de
   subagentes dedicados ou apenas documentação — para que cada operário da fábrica seja
   diretamente invocável nesta CLI.
2. **MCPs reais onde possível**, em vez de contratos simulados:
   - `mcp_db_state` → servidor MCP sqlite real.
   - `mcp_file_writer` → servidor MCP filesystem real.
   - `mcp_image_gen` → servidor MCP **custom**, escrito para este projeto, com motor de
     renderização SVG determinístico (sem custo, sem API paga).
   - `mcp_deep_search` → mapeado para as ferramentas nativas `WebSearch`/`WebFetch` já
     disponíveis na CLI, em vez de um servidor adicional redundante.
3. **Escopo da entrega**: scaffolding completo + execução ponta a ponta de 1 capítulo
   piloto, para provar o pipeline antes de produzir uma obra real.

## 2. O que foi construído

### 2.1 Orquestrador (`CLAUDE.md`)
Arquivo na raiz do projeto com as 4 regras (idioma PT-BR estrito, silenciamento
estético, checkpoint humano obrigatório entre Fase 2 e Fase 3, auto-correção interna), a
tabela do squad de skills, o mapeamento dos MCPs e o fluxo operacional completo. É
carregado automaticamente por qualquer sessão do Claude Code aberta neste diretório.

### 2.2 As 6 Skills (`.claude/skills/`)
Cada uma implementada como um `SKILL.md` com frontmatter `name`/`description` (para
disparo automático por contexto) e um corpo de instruções operacionais fiel ao nó da
fábrica que representa:

| Skill | Nó da fábrica | Arquivo |
|---|---|---|
| `pesquisador` | Fase 1, Nó 0A | `.claude/skills/pesquisador/SKILL.md` |
| `arquiteto` | Fase 1, Nó 0B | `.claude/skills/arquiteto/SKILL.md` |
| `estrategista` | Fase 2, Nós 1-2 | `.claude/skills/estrategista/SKILL.md` |
| `redator-eita` | Fase 2, Nó 4 | `.claude/skills/redator-eita/SKILL.md` |
| `diretor-arte` | Fase 3 | `.claude/skills/diretor-arte/SKILL.md` |
| `compilador-abnt` | Fase 4, Nós 5-9 | `.claude/skills/compilador-abnt/SKILL.md` |

Confirmação objetiva: após a criação dos 6 arquivos, as 6 skills passaram a aparecer
listadas automaticamente como disponíveis nesta sessão (verificado via reminder de
sistema do harness), confirmando que o formato de frontmatter foi reconhecido
corretamente.

### 2.3 O MCP custom `image_gen`
Construído em `.claude/mcp-servers/image-gen-server/` usando `@modelcontextprotocol/sdk`
(v1.30.0) e `zod` para validação de schema. Expõe uma única tool, `gerar_imagem`, com
três modos (`capa`, `contracapa`, `diagrama`), cada um com uma função de renderização
SVG dedicada (`renderCapa`, `renderContracapa`, `renderDiagrama`) que:
- Usa uma paleta de cores fixa (fundo escuro, destaque dourado, texto claro).
- Implementa quebra de linha manual (`quebrarLinhas`) e texto multilinha em SVG, já que
  SVG não faz wrap automático de texto.
- Para diagramas, distribui N caixas horizontalmente com setas conectoras, a partir de
  uma lista arbitrária de `elementos` (labels), com marcador de seta via `<marker>`.

Esse motor não depende de nenhuma API paga de geração de imagem — é determinístico e
gratuito. O `README.md` e o `CLAUDE.md` documentam explicitamente que, para gerar arte
com um modelo de difusão (DALL-E, Stability, Ideogram), basta substituir a entrada
`image_gen` do `.mcp.json` por outro servidor que implemente o mesmo contrato de tool.

### 2.4 Registro dos MCPs (`.mcp.json`)
Três servidores registrados:

```json
{
  "mcpServers": {
    "db_state": { "command": "node", "args": ["...mcp-server-sqlite-npx/dist/index.js", "...data/estado_fabrica.db"] },
    "file_writer": { "command": "node", "args": ["...@modelcontextprotocol/server-filesystem/dist/index.js", "..."] },
    "image_gen": { "command": "node", "args": ["...image-gen-server/index.js"] }
  }
}
```

**Nota de compatibilidade Windows:** a primeira tentativa de registro usou
`"command": "cmd", "args": ["/c", "npx", "-y", "<pacote>", ...]` — o padrão mais comum
em exemplos de MCP para Windows. Ao testar essa configuração isoladamente, o processo
retornou o erro do Windows *"A sintaxe do nome do arquivo, do nome do diretório ou do
rótulo do volume está incorreta"* e um timeout de conexão JSON-RPC — incompatibilidade
entre a camada `cmd /c npx` e o transporte stdio do SDK MCP neste ambiente. A correção
aplicada foi instalar os dois pacotes localmente
(`.claude/mcp-servers/deps/node_modules/`) e apontar o `.mcp.json` diretamente para o
arquivo `bin` resolvido de cada pacote, invocado via `node` — eliminando a camada
`cmd`/`npx` por completo. Após a correção, ambos os servidores conectaram e responderam
normalmente (ver seção 3).

### 2.5 Templates
- `templates/payload_estado.json`: schema do payload de estado inter-agentes.
- `templates/template_eita.md`: molde pedagógico E-I-T-A usado pelo `redator-eita`.

## 3. Testes realizados nos 3 MCPs

Cada servidor foi testado de forma isolada com um cliente MCP real
(`@modelcontextprotocol/sdk` client + `StdioClientTransport`), validando conexão,
`tools/list` e ao menos uma chamada de tool real:

| MCP | Conexão | Ferramentas descobertas | Chamada de teste | Resultado |
|---|---|---|---|---|
| `image_gen` | OK | `gerar_imagem` | `gerar_imagem(tipo=diagrama, ...)` | SVG de 1968 bytes retornado |
| `db_state` | OK | `read_query`, `write_query`, `create_table`, `list_tables`, `describe_table` | `create_table` + `write_query` + `read_query` | Tabela criada, linha inserida e lida de volta corretamente |
| `file_writer` | OK | `read_file`, `write_file`, `edit_file`, `list_directory`, `search_files`, `list_allowed_directories`, entre outras (14 no total) | `list_allowed_directories` | Retornou o diretório raiz do projeto como escopo permitido |

Script de teste: `.claude/mcp-servers/image-gen-server/test_mcp.mjs` (reutilizável para
qualquer servidor MCP stdio — recebe comando, argumentos e, opcionalmente, uma tool e
argumentos para chamar).

## 4. Execução do piloto ponta a ponta

Tema escolhido para o piloto: **"Arquitetura de Servidores MCP como Motor de
Ferramentas para Agentes de IA"** (1 Parte, 1 Capítulo), dentro da obra de trabalho
"Arquitetura de Agentes: Model Context Protocol na Prática".

| Fase | Skill acionada | Artefato gerado |
|---|---|---|
| 1 (Nó 0A) | `pesquisador` | `output/livro_piloto/pesquisa/dossie_mcp-servidores-motor-de-ferramentas.md` — dossiê com 4 buscas web reais (`WebSearch`), conceitos-chave, estado da arte, casos de uso, riscos e 10 fontes brutas rastreáveis |
| 1 (Nó 0B) | `arquiteto` | `output/livro_piloto/sumario_macro.json` — sumário macro escopado a 1 Parte / 1 Capítulo |
| 2 (Nós 1-2) | `estrategista` | `output/livro_piloto/capitulos/cap_1_draft.json` — 3 pilares com escopo e âncora visual definidos |
| 2 (Nó 4) | `redator-eita` | `output/livro_piloto/capitulos/cap_1.md` — capítulo completo em EITA (~1300 palavras) |
| — | **Checkpoint humano** | Pipeline parado; operador respondeu **APROVADO** explicitamente no chat antes de qualquer ação de Fase 3 |
| 3 | `diretor-arte` | 5 SVGs em `output/livro_piloto/imagens/` (3 diagramas + capa + contracapa), gerados via `tools/call` real no MCP `image_gen`, com tags de imagem inseridas no ponto exato de cada âncora visual do capítulo |
| 4 (Nós 5-9) | `compilador-abnt` | `output/livro_piloto/livro_final.md` — capa, prefácio, sumário, capítulo ilustrado, conclusão geral, 10 referências em formato ABNT (deduplicadas e ordenadas alfabeticamente) e contracapa |

O estado de cada transição de fase foi persistido em `data/estado_fabrica.db` via o MCP
`db_state` (3 linhas: início da pesquisa, aguardando checkpoint humano, expedição
final) — confirmando que o mecanismo de rastreamento de estado da esteira funciona de
ponta a ponta, não apenas como especificação.

**REGRA 3 (Checkpoint Obrigatório) foi respeitada literalmente**: a skill
`redator-eita` parou a esteira após gravar o capítulo e o Diretor de Arte só foi
acionado depois que o operador confirmou `APROVADO` explicitamente nesta conversa — em
nenhum momento a aprovação foi presumida ou simulada.

## 5. Verificações de qualidade (pós-implementação)

- Todos os arquivos JSON do projeto (`sumario_macro.json`, `cap_1_draft.json`,
  `cap_1_estado.json`, `payload_estado.json`, `.mcp.json`) validados com
  `JSON.parse` — sem erros de sintaxe.
- Os 5 SVGs gerados verificados quanto a balanceamento de tags `<svg>`/`</svg>` — sem
  problemas estruturais.
- Releitura do banco `estado_fabrica.db` confirmando as 3 transições de estado
  gravadas durante o piloto.
- Removido 1 arquivo de debris (`--help`) criado acidentalmente durante um teste
  manual do CLI do MCP sqlite antes da correção descrita na seção 2.4.

## 6. Limitações conhecidas e próximos passos

- O `image_gen` produz arte vetorial determinística (layout, tipografia, paleta), não
  arte gerada por difusão/modelo de imagem. É uma escolha deliberada para não depender
  de credenciais de API pagas que o operador não forneceu; a troca por um servidor de
  IA generativa de imagem é um drop-in replacement no `.mcp.json` (mesmo contrato de
  tool `gerar_imagem`).
- Os 3 MCPs foram registrados em `.mcp.json` e testados de forma isolada e real via um
  cliente MCP dedicado (`test_mcp.mjs`); como o projeto foi criado durante esta mesma
  sessão do Claude Code (que já estava em execução antes do `.mcp.json` existir), os
  servidores ainda não apareceram na lista de ferramentas *desta* sessão — isso é
  esperado: sessões do Claude Code carregam `.mcp.json` na inicialização. Uma nova
  sessão aberta neste diretório os carregará automaticamente.
- O piloto cobre 1 capítulo. Para uma obra completa, o `arquiteto` deve ser re-acionado
  sem a restrição de escopo "piloto" para gerar o sumário macro completo, e as Fases 2–4
  repetidas por capítulo conforme o fluxo documentado no `README.md`.

## 7. Addendum — 4º MCP: exportação em PDF via CloudConvert

Adicionado a pedido do operador: um MCP `pdf_gen` que converte `livro_final.md` em um
PDF de livro visualmente estruturado, usando a **API real do CloudConvert** (decisão
explícita do operador entre essa opção e uma alternativa 100% local via Puppeteer/
Chromium). O CLAUDE.md, o README.md, a skill `compilador-abnt` e o `.mcp.json` foram
atualizados para incorporar este MCP como o passo final (Nó 10) da Fase 4.

### 7.1 Arquitetura do `pdf_gen`
Servidor em `.claude/mcp-servers/pdf-gen-server/`, com três módulos:
- `template_livro.js`: converte o Markdown em um HTML de livro autocontido — parseia
  com `marked`, embute todas as imagens SVG referenciadas como `data:` URIs (inclusive
  capa/contracapa, que ganham páginas dedicadas de sangria total), remove o título da
  obra e o "## Sumário" estático do corpo (substituídos pela folha de rosto e por um
  sumário paginado gerado automaticamente), e aplica uma folha de estilo de impressão
  com **Paged.js** (polyfill CSS para paginação, cabeçalho corrente via
  `string-set`/`string()` e numeração via `counter(page)`, além de `target-counter()`
  para calcular o número de página real de cada entrada do sumário).
- `cloudconvert.js`: cliente HTTP direto (via `fetch`/`FormData` nativos do Node 22,
  sem SDK) para a API v2 do CloudConvert — cria um job com três tarefas
  (`import/upload` → `convert` com `engine: chrome` e `wait_for_element` apontando para
  um marcador que o Paged.js define quando termina de paginar → `export/url`), envia o
  HTML via upload multipart, aguarda o job (`/jobs/{id}/wait`) e baixa o PDF resultante.
- `index.js`: expõe a tool MCP `markdown_para_pdf`, carrega a `CLOUDCONVERT_API_KEY` de
  uma variável de ambiente ou de um `.env` local (nunca hardcoded), e retorna uma
  mensagem de configuração clara — sem chamar a API — quando a chave não está presente.

### 7.2 Por que a API key não foi criada pela Fábrica
Criar contas e gerar credenciais em nome do operador é uma ação proibida por política
de segurança desta sessão. O `README.md` documenta o passo a passo (conta gratuita em
cloudconvert.com → gerar API key → salvar em
`.claude/mcp-servers/pdf-gen-server/.env`, a partir do `.env.example` incluído) para o
próprio operador realizar essa etapa.

### 7.3 Testes realizados sem a API key
- Conexão do MCP, `tools/list` (retorna `markdown_para_pdf`) e uma chamada real da
  tool: confirmado que, sem `CLOUDCONVERT_API_KEY`, a tool responde com uma mensagem de
  configuração clara e **não** tenta nenhuma chamada de rede ao CloudConvert.
- Geração do HTML de livro testada isoladamente (`test_template.mjs`, sem depender do
  CloudConvert): validado que embute corretamente as 5 imagens (3 diagramas + capa +
  contracapa) sem duplicação, remove o sumário estático e o título duplicado do corpo,
  e monta um sumário paginado com links para Prefácio, Parte I, Capítulo 1, Conclusão
  Geral e Referências Bibliográficas.
- Verificação visual real no navegador (Paged.js roda inteiramente no cliente): o HTML
  gerado foi carregado no Browser tool e o Paged.js paginou corretamente o documento em
  13 páginas, na ordem esperada (capa → folha de rosto → sumário → prefácio → parte →
  capítulo → conclusão → referências → contracapa), confirmado via inspeção do DOM
  (`data-pagedjs-pronto`, contagem de `.pagedjs_page`, texto por página).
- **Limitação encontrada e não totalmente resolvida:** o conteúdo dinâmico das caixas
  de margem do `@page` (cabeçalho corrente via `string()` e número de página via
  `counter(page)`) não apareceu preenchido nos testes visuais realizados no Browser
  tool desta sessão, mesmo após corrigir um bug real (dois blocos `@page` separados
  foram unificados em um só, e um bug de quebra de página duplicada — página em branco
  entre sumário e prefácio — foi corrigido). Um teste mínimo isolado, seguindo
  literalmente o exemplo oficial do Paged.js para numeração de página, apresentou o
  mesmo sintoma nesta ferramenta de navegador sandboxed, e essa mesma ferramenta emite
  o aviso "files outside the project folder render as static snapshots" — indício de
  que o ambiente de preview usado para a verificação visual não é um Chrome completo
  para este tipo de medição de layout assíncrona, e não necessariamente que o CSS está
  incorreto. Como o CloudConvert renderiza com um **Chrome real** (não este preview),
  a paginação e a quebra de página (que já validamos que funcionam) devem se manter, mas
  o cabeçalho corrente e a numeração de página **precisam ser confirmados no primeiro
  PDF gerado de verdade**, assim que o operador configurar a API key. Se não
  aparecerem, o ajuste é localizado em `template_livro.js` (bloco `CSS_LIVRO`).
- Não foi possível (nem tentado) testar a chamada real ao CloudConvert, pois isso
  exige uma API key que só o operador pode gerar.

## 8. Addendum — Comando `/criar-livro` e `SPEC.md`

Adicionado a pedido do operador: um ponto de entrada único que dispara o processo
completo a partir de um tema.

- **`.claude/commands/criar-livro.md`**: comando de slash customizado do Claude Code.
  Recebe o tema em `$ARGUMENTS` e contém as instruções de orquestração passo a passo
  (Fase 1 → Fase 2 por capítulo com checkpoint humano → Fase 3 → Fase 4 + PDF),
  reaproveitando as 6 skills já existentes — nenhuma lógica nova foi duplicada, o
  comando apenas sequencia o que já estava especificado em `CLAUDE.md` e em cada
  `SKILL.md`.
- **`SPEC.md`** (raiz): especificação completa do processo disparado pelo comando —
  máquina de estados de alto nível, tabela detalhada por etapa (agente, entrada, saída,
  checkpoint), contratos de dados e uma tabela de casos de borda (tema vazio, obra já
  existente, ajuste em vez de aprovação, ausência de `CLOUDCONVERT_API_KEY`, falha de
  rede no CloudConvert, sessão interrompida entre capítulos).
- Deixado explícito no próprio `SPEC.md`: o comando **pausa de verdade** a cada
  capítulo aguardando `APROVADO` do operador — não é um job em lote, por decorrência
  direta da REGRA 3.

## 9. Addendum — Portabilidade para outras IDEs agênticas (sem duplicar arquivos)

Adicionado a pedido do operador: o projeto passou a ser utilizável em IDEs/CLIs
agênticas além do Claude Code, sem manter cópias separadas de `CLAUDE.md` ou
`.mcp.json`.

### 9.1 Restrição de ambiente descoberta e decisão tomada
Testei a criação de um symlink real de arquivo neste Windows e a operação falhou por
exigir privilégio de administrador (`New-Item -ItemType SymbolicLink` → "A operação
requer privilégio de administrador"). Testei também uma junction de pasta
(`New-Item -ItemType Junction`), que funcionou sem elevação. Apresentei essa restrição
ao operador antes de prosseguir; ele escolheu a opção sem exigir elevação:
**hardlink de arquivo + junction de pasta no Windows**, com o script equivalente para
macOS/Linux usando **symlink real** (que não tem essa restrição de privilégio fora do
Windows).

### 9.2 O que foi criado
- Frontmatter YAML adicionado ao topo de `CLAUDE.md` (`description` + `alwaysApply:
  true`) — inócuo para o Claude Code (tratado como texto) e necessário para o Cursor
  reconhecer o arquivo como regra "always apply" no formato `.mdc`.
- Hardlinks de arquivo (mesmo conteúdo físico do `CLAUDE.md`, sem cópia):
  `AGENTS.md`, `.cursor/rules/fabrica-agentica.mdc`, `.windsurfrules`,
  `.windsurf/rules/fabrica-agentica.md`, `.clinerules`,
  `.github/copilot-instructions.md`.
- Hardlink de arquivo do `.mcp.json`: `.cursor/mcp.json` (schema `mcpServers`
  idêntico entre Claude Code, Cursor e Windsurf — verificado via pesquisa antes de
  criar o link, para não apresentar um link tecnicamente incorreto como funcional).
- Junctions de pasta: `agentic/skills` → `.claude/skills`, `agentic/commands` →
  `.claude/commands`, `agentic/mcp-servers` → `.claude/mcp-servers` — acesso neutro
  para ferramentas/humanos que não conhecem a convenção `.claude/` do Claude Code.
- **Exceção deliberada, não um link**: `.vscode/mcp.json`. O VS Code usa um schema
  genuinamente diferente (`servers` + `type: "stdio"` obrigatório por servidor, em vez
  de `mcpServers`) — confirmado via pesquisa antes de decidir. Um hardlink aqui geraria
  um arquivo que o VS Code não conseguiria interpretar corretamente. Em vez disso,
  criei `scripts/sync-vscode-mcp.mjs`, que lê `.mcp.json` e gera `.vscode/mcp.json`
  traduzido; deve ser rodado de novo a cada mudança em `.mcp.json`.
- `scripts/setup-links.ps1` (Windows) e `scripts/setup-links.sh` (macOS/Linux):
  recriam todos os links acima de forma idempotente — necessário porque `git clone`,
  cópia de pasta ou `.zip` não preservam hardlinks/junctions/symlinks (o conteúdo é
  copiado como arquivos/pastas independentes de novo).

### 9.3 Verificações realizadas
- `Get-Item` confirmou `LinkType: HardLink` em todos os arquivos e `LinkType: Junction`
  em todas as pastas criadas.
- `Get-FileHash` confirmou hash idêntico entre `CLAUDE.md`/`AGENTS.md`/`.windsurfrules`
  e entre `.mcp.json`/`.cursor/mcp.json` — prova de que é o mesmo conteúdo físico, não
  uma cópia coincidentemente igual.
- `agentic/skills` listado via `Get-ChildItem` mostrou corretamente as 6 pastas de
  skills através da junction.
- `.vscode/mcp.json` gerado e inspecionado: 4 servidores traduzidos corretamente para
  o formato `servers`/`type: "stdio"`.
- O script `setup-links.ps1` foi executado **duas vezes**; na segunda execução, todos
  os itens reportaram "OK (já é hardlink/junction)" sem erro e sem recriar nada —
  confirma idempotência.

### 9.4 Limitação conhecida
Symlinks/hardlinks/junctions são uma otimização do sistema de arquivos **local**. Se
este projeto for versionado em Git e depois clonado (ou copiado/zipado) em outra
máquina, os links não sobrevivem — viram arquivos/pastas independentes de novo no
destino. É por isso que os scripts de setup existem e estão documentados no
`README.md` e no `CLAUDE.md` (seção 6): rodar um deles após qualquer clone/cópia
restaura o comportamento de fonte única.
