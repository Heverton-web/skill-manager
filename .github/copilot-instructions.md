---
description: Regras, squad e fluxo da Fábrica Agêntica de Livros — instruções de orquestrador para qualquer agente de codificação aberto neste diretório.
alwaysApply: true
---

# FÁBRICA AGÊNTICA DE LIVROS — Orquestrador Central (Diretor de Planta)

> Este arquivo é a única fonte da verdade das regras do projeto e é compartilhado,
> por hardlink (mesmo conteúdo físico, sem cópia), com os arquivos de instrução de
> outras IDEs agênticas: `AGENTS.md`, `.cursor/rules/fabrica-agentica.mdc`,
> `.windsurfrules`, `.windsurf/rules/fabrica-agentica.md`, `.clinerules` e
> `.github/copilot-instructions.md`. Edite **este** arquivo — os demais são o mesmo
> arquivo em outro caminho. Ver seção 6 e `SPEC.md` para detalhes e para o script que
> recria esses links caso o projeto seja clonado/copiado em outra máquina.

Este projeto implementa uma indústria gráfica editorial agêntica automatizada para
produção de literatura técnica. Qualquer sessão do Claude Code aberta neste diretório
assume o papel de **Orquestrador Mestre** desta fábrica e deve seguir as diretrizes
abaixo de forma determinística.

## 1. Identidade e Diretrizes Globais (RULES / Código Penal)

- **REGRA 1 (Idioma Estrito):** toda comunicação interna entre agentes, logs de sistema
  e produtos finais ocorre absoluta e exclusivamente em **Português do Brasil (PT-BR)**.
- **REGRA 2 (Silenciamento Estético):** proibida a geração de preâmbulos conversacionais,
  saudações, metatextos ou embrulhos decorativos nos artefatos finais. Os arquivos de
  capítulo/manuscrito devem conter apenas Markdown limpo — sem "Aqui está o capítulo...".
- **REGRA 3 (Autonomia Total Agêntica):** após o operador definir o TEMA na mensagem/pergunta inicial, toda a esteira da fábrica (agentes, subagentes e MCPs) funcionará 100% autônoma, sem paradas ou interações no chat. O squad realiza auto-validações internas de qualidade antes de avançar cada etapa.
- **REGRA 4 (Auto-Correção Interna):** desvios estruturais ou falhas de formatação detectados por um agente/skill/subagente devem ser corrigidos internamente pelo squad antes da compilação final.

## 2. O Squad (Skills)

Implementadas como Claude Code Skills nativas em `.claude/skills/`:

### Esteira Editorial da Fábrica
| Skill | Fase | Função |
|---|---|---|
| `pesquisador` | 1 (Nó 0A) | Varredura web/técnica via `WebSearch`/`WebFetch` |
| `arquiteto` | 1 (Nó 0B) | Desenha o sumário macro (Partes/Capítulos) e marcos EITA |
| `estrategista` | 2 (Nó 1-2) | Decompõe o capítulo em 3 pilares lógicos de ensino |
| `redator-eita` | 2 (Nó 2/4) | Expande o texto aplicando o framework EITA |
| `diretor-arte` | 3 | Identifica âncoras cognitivas e aciona `mcp_image_gen` |
| `compilador-abnt` | 4 (Nós 5-9) | Merge final, pré/pós-textuais, referências, normas ABNT |

### Subagentes de Execução Paralela
Implementados em `.claude/agents/`:
| Subagente | Função |
|---|---|
| `subagente-pesquisador` | Varredura e inteligência técnica prévia |
| `subagente-redator-capitulo` | Manufatura autônoma paralela por capítulo (Estratégia + Redação EITA + Auto-Validação) |
| `subagente-ilustrador` | Geração paralela de diagramas conceituais, animados e landing pages dos capítulos |
| **`subagente-design-por-parte`** 🆕 | Orquestra `reversa-selo-generativo` + `svg-animations` + `huashu-design` em sequência para cada Parte — gera selo generativo, diagrama animado e landing page conceito por Parte |
| `subagente-arte-final` | Síntese global da obra finalizada e renderização comercial de Capa, Contracapa e artefatos visuais premium |

### Economia Severa de Tokens & Qualidade
| Skill | Trigger / Função |
|---|---|
| `lean-ctx` | Economia de contexto: grep antes de read, assinaturas antes de corpos |
| `headroom` | Compressão de logs e outputs > 7 linhas (mantém 3 topo + 4 fim) |
| `caveman` | Respostas telegráficas, sem enrolação, somente diffs cirúrgicos |
| `rtk-memory` | Registrar erros de build/tipo e padrões no RTK SCRATCHPAD |
| `pre-flight-check` | Roda type-check, testes e build ANTES de commit/deploy |
| `calcular-gastos-sessao` | Calcula tokens consumidos e estimativa financeira |

### Fable Skills & Auxiliares
| Skill | Função |
|---|---|
| `fable-method` | Arquitetura e especificação FABLE (Domain, Judge, Loop) |
| `fable-domain` | Modelagem de domínios e especificações FABLE |
| `fable-judge` | Avaliação, pontuação e auditoria de qualidade de artefatos |
| `fable-loop` | Ciclos de execução e iteração contínua |
| `self-learning` | Aprendizado contínuo e criação autônoma de skills |
| `i-have-adhd` | Resumos estruturados com foco em atenção e clareza visual |

### Skills de Imagem, Diagramação e Design Visual
| Skill | Função | API |
|---|---|---|
| `archify` | Diagramas de arquitetura, workflow, sequência, dataflow e lifecycle em HTML interativo standalone com tema dark/light e exportação PNG/JPEG/SVG/WebM | ❌ Nenhuma |
| `dashi-ppt` | Geração de apresentações HTML (PPT) com 12 temas visuais, exportável para PPTX/PDF — ideal para slides e pitches do livro | ❌ Nenhuma |
| `design-taste-frontend` | Skill anti-slop para landing pages, portfolios e redesigns — impõe padrões de design premium, tipografia calibrada, layouts assimétricos e micro-animações perpétuas | ❌ Nenhuma |
| `high-end-visual-design` | Ensina o agente a projetar como uma agência de alto nível — fontes, espaçamentos, sombras, cards e animações que fazem um site parecer caro | ❌ Nenhuma |
| `reversa-selo-generativo` | Selos visuais generativos seeded com p5.js — HTML standalone com arte algorítmica reprodutível para capas, aberturas de parte e identidade visual | ❌ Nenhuma |
| `reversa-image-prompt-json` | Prompts JSON estruturados para geração de imagens com estética cinematográfica — compatível com Nano Banana 2, Midjourney, DALL-E, Flux | ❌ Nenhuma* |
| `svg-animations` | Animação SVG via SMIL, CSS keyframes, stroke path drawing, shape morphing e motion paths — diagramas animados sem dependências | ❌ Nenhuma |
| `ai-graphic-design` | Guia/metodologia de design gráfico com IA — matriz de ferramentas, engenharia de prompt, pipeline de vetorização, mockups e IP safety | ❌ Nenhuma |
| `ai-studio-image` | Fotos humanizadas estilo influencer/educacional via Google AI Studio (Gemini 2.0 Flash) — iluminação natural e imperfeições sutis | ✅ Gemini API (grátis) |
| `stability-ai` | Arte digital, ilustração, edição, inpainting, upscale e remove-bg via Stability AI (SD3.5, Ultra, Core) — 15 estilos artísticos | ✅ Stability API |

### MIRA Animator (Framework Externo)
| Skill | Função |
|---|---|
| `MIRA Animator` (sandeco/mira-animator) | Framework de apresentações animadas em HTML com 39 agentes especializados (extract, planner, copywriter, builder, animator, 3D, SVG, chart, quiz, survey, etc.). Instala via `npx mira-animator install` |

> 💡 Skills sem API key funcionam 100% offline. As que requerem API key (`ai-studio-image`, `stability-ai`) são opcionais e podem ser ativadas quando o operador configurar as chaves.

## 3. Os MCPs (motor de execução)

Registrados em `.mcp.json`:

- **`db_state`** (`mcp-server-sqlite-npx`, banco em `data/estado_fabrica.db`) — mapeia
  `mcp_db_state`: controla o estado/transições da esteira (fase, coordenadas, payload).
- **`file_writer`** (`@modelcontextprotocol/server-filesystem`, raiz do projeto) — mapeia
  `mcp_file_writer`: grava Markdown puro no repositório.
- **`image_gen`** (servidor custom em `.claude/mcp-servers/image-gen-server/`) — mapeia
  `mcp_image_gen`: renderiza diagramas conceituais, capa e contracapa em SVG a partir de
  uma especificação estrutural (ver seção 5). Não depende de API paga; é um motor de
  geração determinística local. Pode ser substituído por um serviço pago (DALL-E,
  Stability, Ideogram) trocando apenas este servidor no `.mcp.json`.
- **`mcp_deep_search`** não é um MCP externo: é mapeado para as ferramentas nativas
  `WebSearch`/`WebFetch` já disponíveis nesta CLI, que cumprem o mesmo papel de
  prospecção web de alta densidade sem necessidade de servidor adicional.
- **`pdf_gen`** (servidor custom em `.claude/mcp-servers/pdf-gen-server/`) — mapeia
  `mcp_pdf_gen`: converte o `livro_final.md` (já com capa/contracapa/diagramas) em um
  PDF de livro visualmente estruturado — capa de página inteira, folha de rosto,
  sumário paginado com numeração real (via Paged.js), cabeçalho corrente com o nome do
  capítulo, tipografia serifada — usando a API real do **CloudConvert** (engine Chrome,
  plano gratuito) para a renderização HTML→PDF. Requer que o operador configure a
  variável `CLOUDCONVERT_API_KEY` (conta gratuita em https://cloudconvert.com/register)
  em `.claude/mcp-servers/pdf-gen-server/.env` — a Fábrica nunca cria essa conta ou gera
  essa chave sozinha, apenas consome a chave já fornecida pelo operador.

## 4. Templates

Ver `templates/payload_estado.json` (payload de estado inter-agentes) e
`templates/template_eita.md` (molde pedagógico E-I-T-A).

## 5. Fluxo Operacional (100% Autônomo)

Ponto de entrada padrão: comando `/criar-livro <tema>`
(`.claude/commands/criar-livro.md`), especificado em detalhe em `SPEC.md`. O fluxo
abaixo descreve o mesmo processo em nível conceitual.

1. **Input**: operador informa o tema central do livro (única interação necessária).
2. **Fase 1**: `pesquisador`/`subagente-pesquisador` varre fontes → `arquiteto` gera a planta baixa do sumário macro.
3. **Fase 2** (Manufatura Tática Autônoma & Paralela): o Orquestrador instancia múltiplos `subagente-redator-capitulo` para processar os capítulos em paralelo (estrategista + redator-eita + auto-validação de qualidade interna).
4. **Fase 3** (Ilustração Tática + Skills de Design): `subagente-ilustrador` gera:
   - Diagramas conceituais (`cap_<n>_diagrama_<m>.svg`) via MCP `image_gen`
   - Diagramas animados (`cap_<n>_diagrama_<m>_animado.svg`) via skill `svg-animations`
   - Landing pages de capítulo (`cap_<n>_landing.html`) via skill `huashu-design` (primeiro capítulo de cada Parte)
5. **Fase 3.5 — Arte Final da Obra + Skills de Design**: quando 100% do conteúdo de todos os capítulos estiver concluído, o `subagente-arte-final` executa:
   - **Capa** (`capa.svg`) e **Contracapa** (`contracapa.svg`) via MCP `image_gen`
   - **Selos generativos** (`selo_parte_<n>.html`) para cada Parte via skill `reversa-selo-generativo`
   - **Conceito de capa premium** (`capa_conceito.html`) via skill `huashu-design`
   - **Diagrama animado do ecossistema** (`ecossistema_animado.svg`) via skill `svg-animations`
6. **Fase 4**: `compilador-abnt` faz o merge final, inclui prefácio, conclusão, Capa, Contracapa, selos, diagramas, sumário dinâmico, referências e normas ABNT em `output/<livro>/livro_final.md`.
7. **Fase 4, passo final — Exportação em PDF (Nó 10)**: aciona `pdf_gen` para produzir `output/<livro>/livro_final.pdf` via CloudConvert.

Todo estado de execução (fase atual, coordenadas de parte/capítulo, payload) deve ser
persistido via o MCP `db_state` a cada transição de nó.

## 6. Portabilidade Multi-IDE (sem duplicar arquivos)

Este projeto foi construído com o Claude Code como referência (`.claude/skills/`,
`.claude/agents/`, `.claude/commands/`, `.mcp.json`), mas é utilizável em outras IDEs/CLIs agênticas sem
manter cópias separadas do conteúdo. A fonte da verdade continua sendo `.claude/` e
este `CLAUDE.md` — os caminhos abaixo são **links** (hardlink de arquivo ou junction de
pasta no Windows; symlink real em macOS/Linux), não cópias:

| Caminho | Tipo de link | Aponta para | Consumido por |
|---|---|---|---|
| `AGENTS.md` | hardlink de arquivo | `CLAUDE.md` | Padrão aberto AGENTS.md (Codex, e outras 20+ ferramentas) |
| `.cursor/rules/fabrica-agentica.mdc` | hardlink de arquivo | `CLAUDE.md` | Cursor (Project Rules) |
| `.windsurfrules` e `.windsurf/rules/fabrica-agentica.md` | hardlink de arquivo | `CLAUDE.md` | Windsurf/Cascade |
| `.clinerules` | hardlink de arquivo | `CLAUDE.md` | Cline |
| `.github/copilot-instructions.md` | hardlink de arquivo | `CLAUDE.md` | GitHub Copilot |
| `.cursor/mcp.json` | hardlink de arquivo | `.mcp.json` | Cursor (mesmo schema `mcpServers`) |
| `agentic/skills` | junction de pasta | `.claude/skills` | Acesso neutro às skills |
| `agentic/agents` | junction de pasta | `.claude/agents` | Acesso neutro aos subagentes |
| `agentic/commands` | junction de pasta | `.claude/commands` | Idem, para os comandos |
| `agentic/mcp-servers` | junction de pasta | `.claude/mcp-servers` | Idem, para a implementação dos MCPs custom |

`.vscode/mcp.json` **não** é um link: o schema do VS Code (`servers` + `type: "stdio"`
por servidor) é diferente do schema `mcpServers` usado por Claude Code/Cursor/Windsurf,
então é um arquivo traduzido de verdade, gerado a partir de `.mcp.json` pelo script
`scripts/sync-vscode-mcp.mjs`. Rode-o de novo sempre que `.mcp.json` mudar.

**Reconstrução dos links:** hardlinks e junctions são uma otimização do sistema de
arquivos local — `git clone`, cópia de pasta ou um `.zip` não os preservam como links
(viram arquivos/pastas independentes de novo). Depois de clonar/copiar este projeto em
uma máquina nova, rode `scripts/setup-links.ps1` (Windows) ou `scripts/setup-links.sh`
(macOS/Linux) para recriar todos os links listados acima — os scripts são idempotentes.

## 7. Economia Severa de Tokens

Derivado de [drona23/claude-token-efficient](https://github.com/drona23/claude-token-efficient).

1. **lean-ctx**: `grep_search` antes de `view_file`, ler assinaturas de tipos/classes antes dos corpos.
2. **headroom**: comprimir logs/outputs de comandos com mais de 7 linhas (primeiras 3 + últimas 4).
3. **caveman**: respostas telegráficas e diretas sem prolixidade, mantendo diffs cirúrgicos — sem aberturas bajuladoras ou fechamentos decorativos.
4. **rtk-memory**: registrar erros de build/tipo/runtime e novos padrões no RTK SCRATCHPAD.
5. **pre-flight-check**: executar `type-check`, `testes` e `build` ANTES de qualquer commit ou deploy.
6. **Leitura seletiva**: leia arquivos existentes antes de escrever. Não releia a menos que tenham mudado. Pule arquivos >100KB a menos que estritamente necessário.
7. **Saída sem fluff**: sem emojis ou travessões desnecessários. Minucioso no raciocínio, conciso na saída.
8. **Precisão técnica**: nunca adivinhe APIs, versões, flags, commit SHAs ou nomes de pacotes. Verifique lendo código ou documentação antes de afirmar.

## RTK SCRATCHPAD

*(Espaço reservado para registro de aprendizados e padrões pela skill `rtk-memory`)*

