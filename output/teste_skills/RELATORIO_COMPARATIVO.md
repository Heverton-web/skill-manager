╔══════════════════════════════════════════════════════════════╗
║  RELATÓRIO COMPARATIVO — Skills de Imagem                  ║
╚══════════════════════════════════════════════════════════════╝

Gerado em: 2026-07-28


## 📊 Tabela Comparativa

| # | Skill | Status | Gera Imagem? | API Key? | Uso Principal |
|---|-------|--------|-------------|----------|---------------|
| 1 | `reversa-selo-generativo` | ✅ OK | ✅ HTML/SVG | ❌ Não | Selos generativos p5.js (capas, identidade) |
| 2 | `reversa-image-prompt-json` | ✅ OK | ❌ Só prompt | ❌ Não* | Prompts estruturados para Midjourney/DALL-E/Flux |
| 3 | `svg-animations` | ✅ OK | ✅ SVG | ❌ Não | Diagramas SVG animados com SMIL/CSS |
| 4 | `ai-graphic-design` | ✅ OK | ❌ Guia | ❌ Não | Metodologia de design gráfico com IA |
| 5 | `ai-studio-image` | ⚠️ Não testado | ✅ Foto/Imagem | ✅ Gemini API | Fotos humanizadas estilo influencer/educacional |
| 6 | `image-studio` | ⚠️ Não testado | ✅ Roteador | ✅ Gemini/SD | Roteia entre ai-studio-image e stability-ai |
| 7 | `stability-ai` | ⚠️ Não testado | ✅ Arte/Ilustração | ✅ Stability API | Arte digital, ilustração, edição, upscale |
| 8 | **`MIRA Animator`** | ✅ **Framework** | ✅ **HTML Slides** | ❌ Não | **Apresentações animadas c/ 39 agentes especializados** |


## 📋 Detalhes por Skill

### ✅ reversa-selo-generativo
- **Descrição:** HTML standalone com p5.js — selo generativo seeded
- **API necessária:** Nenhuma (p5.js via CDN, gratuito)
- **Tempo:** 0.0s
- **Artefatos gerados:**
  - `selo_aidd.html`

### ✅ reversa-image-prompt-json
- **Descrição:** Prompt JSON estruturado para geração de imagem — compatível com Nano Banana 2, Midjourney, DALL-E, Flux
- **API necessária:** Nano Banana 2 (grátis via Google Antigravity) ou serviço de imagem externo
- **Tempo:** 0.0s
- **Artefatos gerados:**
  - `prompt_capa_aidd.json`
  - `prompt_capa_aidd.md`

### ✅ svg-animations
- **Descrição:** Diagrama SVG animado com SMIL — agentes, MCP e ferramentas com animações nativas
- **API necessária:** Nenhuma (SVG puro com animações SMIL + CSS, roda em qualquer navegador)
- **Tempo:** 0.0s
- **Artefatos gerados:**
  - `diagrama_animado_aidd.svg`
  - `diagrama_animado_aidd.html`

### ✅ ai-graphic-design
- **Descrição:** Guia/metodologia de design gráfico com IA — 9 seções com matriz de ferramentas, prompts, pipelines
- **API necessária:** Nenhuma (é um guia metodológico, não gera imagens diretamente)
- **Tempo:** 0.0s
- **Artefatos gerados:**
  - `guia_ai_graphic_design.md`

### ✅ MIRA Animator (sandeco/mira-animator)
- **Descrição:** Framework completo de apresentações animadas em HTML — 39 agentes especializados
- **Versão:** 0.1.49
- **Licença:** PolyForm Noncommercial 1.0.0
- **Instalação:** `npx mira-animator install` (na pasta de trabalho, nunca no código-fonte)
- **Link:** https://github.com/sandeco/mira-animator
- **Docs:** https://sandeco.github.io/mira-animator/
- **API necessária:** Nenhuma (geração 100% local, HTML/CDN)
- **Pipeline multi-agente:**
  - `/mira-new` → Cria deck + orquestra pipeline
  - `/mira-extract` → Lê fonte vinculada e gera briefing
  - `/mira-planner` → Estrutura os slides
  - `/mira-copywriter` → Refina textos e conceitos
  - `/mira-builder` → Monta HTML/Tailwind/glassmorphism
  - `/mira-animator` → Cria animações vetoriais em loop contínuo
- **39 agentes especializados:**
  - `mira-image`, `mira-image-prompt`, `mira-image-template` — Geração/assets de imagens
  - `mira-3d` — Elementos 3D interativos (Three.js)
  - `mira-chart`, `mira-chart-race` — Gráficos de dados animados
  - `mira-svg-animator`, `mira-svg-morph`, `mira-icon-morph` — Animação/morphing SVG
  - `mira-animated-metaphor` — Metáforas visuais animadas
  - `mira-visuals` — Imagens estáticas via D3.js PNG / prompt JSON
  - `mira-slide-to-video` — Renderização MP4 via Puppeteer + FFmpeg
  - `mira-qrcode`, `mira-quiz`, `mira-survey` — Interatividade
  - `mira-remote-control`, `mira-studio` — Controle remoto + estúdio webcam
  - `mira-squared`, `mira-vertical`, `mira-thirds` — Variantes de formato
  - `mira-tactics` — Mesa tática de futebol interativa
  - `mira-webview` — Sites vivos dentro de slides
  - `mira-validator` — Validação visual/estrutural
- **Artefatos gerados:** Decks HTML standalone em `decks/<theme>/index.html`
- **Fluxo de trabalho:**
  1. `cd slides-folder && npx mira-animator install`
  2. `npx mira-animator link ../proj_livros --name=aidd` (vincula fonte)
  3. `/mira-new "apresentação AIDD"` (no Claude)
  4. "fill the deck aidd with content from the aidd source"
  5. Deck pronto em `decks/aidd/index.html` (abre direto file://)

### ❌ ai-studio-image
- **Descrição:** Geração de fotos humanizadas via Google AI Studio (Gemini 2.0 Flash). Requer GEMINI_API_KEY (grátis).
- **API necessária:** GEMINI_API_KEY (https://aistudio.google.com/apikey)
- **Tempo:** -

### ❌ image-studio
- **Descrição:** Roteador inteligente — detecta se pede foto (ai-studio-image) ou arte (stability-ai).
- **API necessária:** GEMINI_API_KEY + STABILITY_API_KEY
- **Tempo:** -

### ❌ stability-ai
- **Descrição:** Geração de arte/ilustração/edição via Stability AI. Requer STABILITY_API_KEY (Community License grátis).
- **API necessária:** STABILITY_API_KEY
- **Tempo:** -


## 💡 Recomendação

### Inserir no fluxo AGORA:

| Prioridade | Skill | Onde inserir |
|------------|-------|-------------|
| 🔴 **Alta** | **`MIRA Animator`** | **Fase 4** (pós-compilação): gerar deck de apresentação do livro completo via `/mira-new` |
| 🔴 Alta | `reversa-selo-generativo` | **Fase 3** (diretor-arte): selo generativo p5.js para abertura de cada **Parte** |
| 🔴 Alta | `svg-animations` | **Fase 3**: diagramas animados para versão **web** do livro |
| 🟡 Média | `reversa-image-prompt-json` | **Fase 3**: estruturar prompts profissionais para capa/contracapa |
| 🟢 Baixa | `ai-graphic-design` | Guia de referência para o diretor-arte refinar prompts |

### Testar depois (requerem API keys):

| Prioridade | Skill | API necessária |
|------------|-------|---------------|
| 🟡 Média | `ai-studio-image` | Gemini API Key (grátis, 50 img/dia) |
| 🟡 Média | `stability-ai` | Stability AI Community License |
| 🟢 Baixa | `MIRA Animator` | Nenhuma (já incluso) |


## 🔗 Links Úteis

| Skill | Instalação |
|-------|-----------|
| MIRA Animator | `npx mira-animator install` (npm package) |
| reversa-selo-generativo | `npx skills add sandeco/reversa --skill reversa-selo-generativo` |
| reversa-image-prompt-json | `npx skills add sandeco/reversa --skill reversa-image-prompt-json` |
| svg-animations | `npx skills add epicenterhq/epicenter --skill svg-animations` |
| ai-graphic-design | `npx skills add designrique/ai-graphic-design-skill --skill ai-graphic-design` |
| ai-studio-image | `npx skills add sickn33/antigravity-awesome-skills --skill ai-studio-image` |
| stability-ai | `npx skills add sickn33/antigravity-awesome-skills --skill stability-ai` |
