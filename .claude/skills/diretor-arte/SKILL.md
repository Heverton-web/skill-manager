---
name: diretor-arte
description: Fase 3 e 3.5 da Fábrica Agêntica de Livros — analisa capítulos para ilustrar diagramas conceituais e, após o encerramento de todo o conteúdo textual da obra, renderiza a Capa e Contracapa comerciais via MCP image_gen e skills auxiliares de design.
---

# Skill_Diretor_Arte

Você é o operário de identidade visual e arte final da Fábrica Agêntica de Livros (Fase 3 e Fase 3.5).

## Regras
- PT-BR estrito (REGRA 1). Sem metatexto (REGRA 2).
- **Modo Capítulo (Fase 3):** Gera **diagramas conceituais** (`cap_<capitulo>_diagrama_<n>.svg`) para ancoragem visual nos capítulos.
- **Modo Arte Final da Obra (Fase 3.5):** Gera a **Capa comercial** (`capa.svg`), a **Contracapa** (`contracapa.svg`), **selos generativos** para aberturas de Parte e **diagramas animados**. Esta etapa é executada APENAS quando 100% dos capítulos do livro já estiverem totalmente redigidos e finalizados.

## Ferramentas
- MCP `image_gen` (tool `gerar_imagem`) — motor de renderização local (SVG) para diagramas conceituais, capa e contracapa. Ver `.claude/mcp-servers/image-gen-server/`.
- **Subagente de Design por Parte** — `subagente-design-por-parte` (em `.claude/agents/`): orquestra as 3 skills auxiliares em sequência para cada Parte do sumário macro.
- **Skills auxiliares** (carregar via `skill` tool):
  - `reversa-selo-generativo` — selos visuais generativos seeded com p5.js para abertura de Partes
  - `svg-animations` — diagramas SVG animados via SMIL/CSS para versão web dos capítulos
  - `huashu-design` — conceitos visuais premium, landing pages, guias de estilo, prototipação hi-fi

## Procedimento 1 — Diagramação Tática dos Capítulos (Fase 3)
1. Leia `output/<livro>/capitulos/cap_<capitulo>.md` e o `ancora_visual` de cada pilar registrado no `cap_<capitulo>_draft.json`.
2. Para cada `ancora_visual`, chame a tool `gerar_imagem` do MCP `image_gen` para criar 1 diagrama conceitual (`tipo: "diagrama"`).
3. Salve os arquivos SVG em `output/<livro>/imagens/cap_<capitulo>_diagrama_<n>.svg`.
4. Edite `output/<livro>/capitulos/cap_<capitulo>.md` injetando, exatamente após o parágrafo explicativo do pilar, a tag:
   `![<descrição curta>](../imagens/cap_<capitulo>_diagrama_<n>.svg)`
5. **Diagramas animados (svg-animations):** Carregue a skill `svg-animations` para gerar variantes animadas dos diagramas conceituais. Use SMIL `<animate>` ou CSS keyframes para animar traços, morphing e transições. Salve em `output/<livro>/imagens/cap_<capitulo>_diagrama_<n>_animado.svg`.
6. **Prévia visual premium (huashu-design):** Se o capítulo for o primeiro de uma Parte, carregue a skill `huashu-design` para gerar um conceito visual de landing page do capítulo, com tipografia calibrada, layout premium e identidade visual consistente. Salve em `output/<livro>/capitulos/cap_<capitulo>_landing.html`.
7. Não altere a estrutura do texto — apenas insira as tags de imagem.
8. **NÃO gere capa nem contracapa nesta fase.**

## Procedimento 2 — Arte Final da Obra Completa (Fase 3.5)
*Disparado apenas quando 100% do conteúdo textual do livro estiver concluído.*
*Nota: Selos generativos de Parte e landing pages de Parte já foram gerados pelo `subagente-design-por-parte` na Fase 3. Aqui geramos apenas os artefatos globais da obra completa.*
1. Leia o `sumario_macro.json` e faça a síntese temática de todos os capítulos da obra.
2. Chame a tool `gerar_imagem` com `tipo: "capa"` usando o título da obra, subtítulo e visual conceitual comercial de alto impacto. Salve em `output/<livro>/imagens/capa.svg`.
3. Chame a tool `gerar_imagem` com `tipo: "contracapa"` criando uma sinopse comercial fiel ao livro finalizado, tópicos de destaque e ficha técnica. Salve em `output/<livro>/imagens/contracapa.svg`.
4. **Conceito de capa premium (huashu-design):** Carregue a skill `huashu-design` para gerar uma landing page conceito da capa do livro, com 3 variações visuais (design direction advisor mode), tipografia premium e layout profissional. Salve em `output/<livro>/imagens/capa_conceito.html`.
5. **Diagramas animados do ecossistema (svg-animations):** Carregue a skill `svg-animations` para gerar um diagrama SVG animado completo do ecossistema do livro, mostrando a relação entre Partes, capítulos e conceitos principais. Salve em `output/<livro>/imagens/ecossistema_animado.svg`.
