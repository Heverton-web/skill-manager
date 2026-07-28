# Fábrica Agêntica de Livros

Indústria gráfica editorial agêntica automatizada: transforma um tema em um livro
técnico completo — pesquisado, redigido, ilustrado, normalizado em ABNT, exportado em
PDF e expedido — usando 18 skills (editorial, economia severa de tokens e fable method), 4 servidores MCP e um checkpoint humano obrigatório
entre a redação e a arte. Construído com o Claude Code como referência, mas utilizável
em outras IDEs/CLIs agênticas (Cursor, Windsurf, Cline, GitHub Copilot, qualquer
ferramenta compatível com `AGENTS.md`) sem duplicar arquivo nenhum — ver
["Compatibilidade com outras IDEs"](#compatibilidade-com-outras-ides-agênticas).

## Início rápido

```
/criar-livro <tema central do livro>
```

Esse comando (definido em [.claude/commands/criar-livro.md](.claude/commands/criar-livro.md))
é o ponto de entrada único: dispara pesquisa, sumário, redação capítulo a capítulo (com
parada obrigatória aguardando `APROVADO`), arte e compilação final em Markdown + PDF.
Especificação completa do processo em [SPEC.md](SPEC.md).

## Como funciona

Qualquer sessão do Claude Code aberta neste diretório carrega automaticamente
[CLAUDE.md](CLAUDE.md), que define as 4 regras da fábrica (idioma PT-BR estrito,
silenciamento estético, checkpoint humano obrigatório, auto-correção interna), o
squad de skills e o fluxo operacional completo.

```
Tema do operador
   │
   ▼
Fase 1 — P&D          Skill_Pesquisador (WebSearch/WebFetch) → Skill_Arquiteto (sumário macro)
   │
   ▼
Fase 2 — Manufatura    Skill_Estrategista (3 pilares) → Skill_Redator_EITA (texto EITA)
   │                              │
   │                    ⏸ CHECKPOINT: aguarda "APROVADO" do operador
   ▼
Fase 3 — Arte          Skill_Diretor_Arte → MCP image_gen (capa, contracapa, diagramas SVG)
   │
   ▼
Fase 4 — Acabamento    Skill_Compilador_ABNT (merge, prefácio, conclusão, referências, ABNT)
   │
   ▼
Fase 4, passo final   Skill_Compilador_ABNT → MCP pdf_gen (CloudConvert): PDF de livro
   │
   ▼
livro_final.md + livro_final.pdf
```

## Estrutura do projeto

```
.claude/
  skills/                  18 Claude Code Skills (esteira editorial, economia de tokens, fable)
  commands/                comando /criar-livro (ponto de entrada único)
  mcp-servers/
    image-gen-server/      MCP custom (mcp_image_gen): renderiza SVG determinístico
    pdf-gen-server/        MCP custom (mcp_pdf_gen): Markdown → PDF de livro via CloudConvert
    deps/                  MCP sqlite (db_state) e filesystem (file_writer), via npm
agentic/                   pastas neutras (junction/symlink) para skills/commands/mcp-servers
.mcp.json                  Registro dos 4 MCPs (Claude Code, Cursor, Windsurf)
.vscode/mcp.json           Mesmos MCPs traduzidos para o schema do VS Code (arquivo gerado)
AGENTS.md, .cursorrules... links para CLAUDE.md — ver seção "Compatibilidade" abaixo
CLAUDE.md                  Regras + squad + fluxo do orquestrador (fonte da verdade)
SPEC.md                    Especificação completa do comando /criar-livro
templates/                 Payload de estado (JSON) e molde pedagógico EITA
data/estado_fabrica.db     Banco sqlite com o histórico de transições da esteira
output/<livro>/            Cada livro produzido: pesquisa/, capitulos/, imagens/, livro_final.md, livro_final.pdf
scripts/                   setup-links.ps1/.sh (recria os links) e sync-vscode-mcp.mjs
```

## Compatibilidade com outras IDEs agênticas

Nenhum conteúdo é duplicado: os arquivos abaixo são **hardlinks/junctions** (Windows)
ou **symlinks reais** (macOS/Linux) apontando para `CLAUDE.md` ou `.mcp.json` — editar
o arquivo fonte atualiza todos os outros instantaneamente, porque fisicamente é o mesmo
arquivo.

| Ferramenta | Arquivo/pasta | Link para |
|---|---|---|
| Padrão aberto AGENTS.md (Codex e 20+ ferramentas) | `AGENTS.md` | `CLAUDE.md` |
| Cursor (Project Rules) | `.cursor/rules/fabrica-agentica.mdc` | `CLAUDE.md` |
| Cursor (MCP) | `.cursor/mcp.json` | `.mcp.json` |
| Windsurf/Cascade | `.windsurfrules`, `.windsurf/rules/fabrica-agentica.md` | `CLAUDE.md` |
| Cline | `.clinerules` | `CLAUDE.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | `CLAUDE.md` |
| Acesso neutro (qualquer ferramenta/humano) | `agentic/skills`, `agentic/commands`, `agentic/mcp-servers` | `.claude/skills`, `.claude/commands`, `.claude/mcp-servers` |

`.vscode/mcp.json` é a única exceção — o VS Code usa um schema diferente
(`servers`/`type: "stdio"` em vez de `mcpServers`), então é um arquivo **gerado** (não
um link) por `scripts/sync-vscode-mcp.mjs`. Rode-o de novo depois de qualquer mudança em
`.mcp.json`.

**Depois de clonar ou copiar este projeto para outra máquina**, `git clone`/cópia de
pasta/`.zip` não preservam hardlinks/junctions/symlinks — eles viram arquivos
independentes de novo. Rode um dos scripts abaixo (idempotentes) para recriá-los:

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\setup-links.ps1

# macOS/Linux
bash scripts/setup-links.sh
```

## Skills da Fábrica

### Esteira Editorial
| Skill | Fase | Papel |
|---|---|---|
| `pesquisador` | 1 | Varredura web/técnica (mapeia `mcp_deep_search` para `WebSearch`/`WebFetch`) |
| `arquiteto` | 1 | Desenha o sumário macro (Partes/Capítulos) |
| `estrategista` | 2 | Decompõe o capítulo em 3 pilares lógicos |
| `redator-eita` | 2 | Expande o texto no framework EITA (Explica, Ilustra, Técnica, Aplica) |
| `diretor-arte` | 3 | Aciona o `image_gen` e posiciona as ilustrações no texto |
| `compilador-abnt` | 4 | Merge final, elementos extrusos, referências, normas ABNT e exportação em PDF |

### Skills de Imagem, Diagramação e Design Visual
| Skill | Função | API Key? |
|---|---|---|
| `archify` | Diagramas de arquitetura, workflow, sequência e lifecycle em HTML interativo standalone (SVG, dark/light, export PNG/JPEG/WebM) | ❌ Não |
| `dashi-ppt` | Geração de apresentações HTML (PPT) com 12 temas visuais, exportável para PPTX/PDF | ❌ Não |
| `design-taste-frontend` | Design anti-slop: landing pages, portfolios e redesigns com padrões premium | ❌ Não |
| `high-end-visual-design` | Diretrizes de design de alto nível: tipografia, sombras, cards, animações | ❌ Não |
| `reversa-selo-generativo` | Selos generativos seeded com p5.js — HTML standalone para capas e aberturas | ❌ Não |
| `reversa-image-prompt-json` | Prompts JSON estruturados para Midjourney/DALL-E/Flux/Nano Banana 2 | ❌ Não* |
| `svg-animations` | Animação SVG (SMIL, CSS keyframes, stroke drawing, shape morphing) | ❌ Não |
| `ai-graphic-design` | Guia metodológico: ferramentas, prompts, vetorização, mockups, IP safety | ❌ Não |
| `ai-studio-image` | Fotos humanizadas estilo influencer/educacional via Google Gemini 2.0 Flash | ✅ Gemini API |
| `stability-ai` | Arte digital, ilustração, edição, inpainting, upscale (SD3.5, Ultra, Core) | ✅ Stability API |

### Fable Skills & Auxiliares
| Skill | Função |
|---|---|
| `fable-method` | Arquitetura e especificação FABLE (Domain, Judge, Loop) |
| `fable-judge` | Avaliação, pontuação e auditoria de qualidade de artefatos |
| `fable-loop` | Ciclos de execução e iteração contínua |
| `lean-ctx` | Economia de contexto: grep antes de read |
| `headroom` | Compressão de logs/outputs > 7 linhas |
| `caveman` | Respostas telegráficas e diffs cirúrgicos |
| `pre-flight-check` | Validações obrigatórias antes de commit/deploy |
| `rtk-memory` | Registro persistente de erros e padrões |
| `self-learning` | Criação autônoma de novas skills |
| `i-have-adhd` | Resumos estruturados para clareza visual |

### MIRA Animator (Framework Externo)
| Skill | Função |
|---|---|
| `MIRA Animator` | Framework de apresentações animadas em HTML com 39 agentes: extract → planner → copywriter → builder → animator → 3D → SVG morph → chart → quiz → survey → vídeo. Instala: `npx mira-animator install` |

Invoque uma skill diretamente com `/pesquisador`, `/arquiteto` etc., ou deixe o
orquestrador (esta sessão) decidir qual acionar a partir do seu pedido.

## Os 4 MCPs

| MCP | Pacote/implementação | Função |
|---|---|---|
| `db_state` | `mcp-server-sqlite-npx` (banco em `data/estado_fabrica.db`) | Estado da esteira (fase, coordenadas, payload) |
| `file_writer` | `@modelcontextprotocol/server-filesystem` (raiz do projeto) | Gravação de Markdown no repositório |
| `image_gen` | Servidor custom (`.claude/mcp-servers/image-gen-server/`) | Renderização determinística de capa, contracapa e diagramas em SVG |
| `pdf_gen` | Servidor custom (`.claude/mcp-servers/pdf-gen-server/`), API real do **CloudConvert** | Converte `livro_final.md` em `livro_final.pdf` — livro completo (capa, folha de rosto, sumário paginado, cabeçalho corrente, tipografia serifada) |

`mcp_deep_search` **não** é um servidor MCP externo — é mapeado para as ferramentas
nativas `WebSearch`/`WebFetch` já disponíveis nesta CLI.

O `image_gen` é um motor de layout local, sem custo e sem dependência de API paga.
Para trocá-lo por um serviço de geração de imagem por IA (DALL-E, Stability,
Ideogram), basta substituir a entrada `image_gen` em [.mcp.json](.mcp.json) por um
servidor que fale o mesmo contrato de tool (`gerar_imagem`).

### Configurando o `pdf_gen` (CloudConvert)

Este MCP usa a API real do [CloudConvert](https://cloudconvert.com) (plano gratuito:
25 minutos de conversão por dia). Você precisa criar sua própria conta e API key —
a Fábrica nunca faz isso por você:

1. Crie uma conta gratuita em https://cloudconvert.com/register.
2. Gere uma API key em https://cloudconvert.com/dashboard/api/v2/keys.
3. Copie `.claude/mcp-servers/pdf-gen-server/.env.example` para `.env` (mesma pasta) e
   cole a chave em `CLOUDCONVERT_API_KEY=`.

Sem essa chave, a tool `markdown_para_pdf` responde com instruções de configuração em
vez de tentar a conversão — o restante do pipeline (Markdown, imagens, ABNT) continua
funcionando normalmente.

## Como produzir um livro novo

1. Informe o tema central da obra ao orquestrador (esta sessão do Claude Code).
2. Acompanhe a Fase 1 e a Fase 2 capítulo a capítulo; ao final de cada capítulo, revise
   o Markdown gerado em `output/<livro>/capitulos/` e responda `APROVADO` para liberar
   a Fase 3.
3. A Fase 3 gera os ativos visuais e injeta as tags de imagem automaticamente.
4. Repita 2–3 para todos os capítulos do sumário macro.
5. Acione (ou deixe o orquestrador acionar) `compilador-abnt` para expedir o
   `livro_final.md` — como último passo da mesma execução, ele também gera
   `livro_final.pdf` via `pdf_gen` (CloudConvert), se `CLOUDCONVERT_API_KEY` estiver
   configurada.

## Piloto de referência

O diretório `output/livro_piloto/` contém uma execução ponta a ponta completa e real
(pesquisa via `WebSearch`, sumário, redação EITA, checkpoint humano `APROVADO`, arte via
MCP `image_gen`, e compilação ABNT) sobre o tema "Arquitetura de Servidores MCP como
Motor de Ferramentas para Agentes de IA". Use-o como referência de formato antes de
produzir a primeira obra real. A exportação `livro_final.pdf` deste piloto ainda
depende do operador configurar `CLOUDCONVERT_API_KEY` (ver seção acima).

Detalhes de como cada componente foi construído e testado estão em
[RELATORIO_FABRICA.md](RELATORIO_FABRICA.md).
