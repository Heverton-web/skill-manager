# Fluxo de Funcionamento da Fábrica Agêntica de Livros

> Documento oficial do fluxo operacional completo.
> Versão: V3 (Agosto 2026) | Projeto: Fábrica Agêntica de Livros

---

## 1. Visão Geral

A **Fábrica Agêntica de Livros** é uma esteira editorial automatizada que produz livros técnicos completos — do tema à entrega de PDF formatado (ABNT) — utilizando agentes de IA (Claude Code, Cursor, Windsurf, Codex, etc.) como força de trabalho.

A fábrica opera em **4 Fases** — P&D (1), Manufatura em lotes (2), Peer Review autônomo (2.5) e Acabamento ABNT (3) — executadas por um **Orquestrador Mestre** que coordena **Skills** (operários especializados), **Subagentes** (equipes paralelas), **MCPs** (ferramentas de execução) e **Scripts** (automação local e avaliação determinística).

### Princípios Operacionais

| Regra | Descrição |
|-------|-----------|
| **REGRA 1** | Tudo em PT-BR estrito (comunicação, logs, artefatos) |
| **REGRA 2** | Sem metatexto ou saudações nos artefatos — Markdown limpo |
| **REGRA 3** | Autonomia total após o tema ser definido (sem paradas no chat) |
| **REGRA 4** | Auto-correção interna de desvios estruturais antes da entrega |
| **REGRA 5** | NUNCA usar `---` (horizontal rules) dentro de capítulos individuais — usar apenas separadores de parágrafo duplo (`\n\n`) entre seções |

---

## 2. Arquitetura da Fábrica

### 2.1 Camadas

```
┌─────────────────────────────────────────────────────────────┐
│                    OPERADOR (humano)                         │
│  Dispara /criar-livro <tema>  ou  /compilar-mega-livro      │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│             ORQUESTRADOR MESTRE (CLAUDE.md)                  │
│  Coordena fases, instancia skills, subagentes e MCPs        │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│   ┌─────────────────┐  ┌──────────────────┐                 │
│   │    SKILLS        │  │   SUBAGENTES      │                 │
│   │  (operários)     │  │  (equipes)        │                 │
│   └─────────────────┘  └──────────────────┘                 │
│   ┌─────────────────┐  ┌──────────────────┐                 │
│   │    MCPs          │  │    SCRIPTS        │                 │
│   │  (ferramentas)   │  │  (automação)     │                 │
│   └─────────────────┘  └──────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Skills (Operários Especializados)

Skills são instruções executáveis carregadas automaticamente pelo agente.
Cada skill sabe executar uma etapa específica da produção.

| Skill | Fase | O que faz | Arquivo |
|-------|------|-----------|---------|
| `pesquisador` | 1 (Nó 0A) | Varredura web/técnica via WebSearch/WebFetch | `.claude/skills/pesquisador/SKILL.md` |
| `arquiteto` | 1 (Nó 0B) | Desenha o sumário macro (Partes/Capítulos) | `.claude/skills/arquiteto/SKILL.md` |
| `estrategista` | 2 (Nó 1-2) | Decompõe o capítulo em 3 pilares lógicos | `.claude/skills/estrategista/SKILL.md` |
| `redator-eita` | 2 (Nó 4) | Expande o texto aplicando o framework EITA | `.claude/skills/redator-eita/SKILL.md` |
| `revisor-tecnico` | 2.5 (Nó 4.5) | Peer review autônomo da obra inteira sobre evidência determinística | `.claude/skills/revisor-tecnico/SKILL.md` |
| `compilador-abnt` | 3 (Nós 5-10) | Merge final, ABNT, capa gráfica, CIP, PDF via Pandoc→typ→Typst | `.claude/skills/compilador-abnt/SKILL.md` |
| `compilador-mega-livro` | Pós-produção | Compila múltiplos livros em um só | `.claude/skills/compilador-mega-livro/SKILL.md` |

### 2.3 Subagentes (Execução Paralela)

Subagentes implementam fluxos multi-passo que combinam várias skills.
São disparados em paralelo para acelerar a produção.

| Subagente | O que faz | Arquivo |
|-----------|-----------|---------|
| `subagente-pesquisador` | Varredura web profunda + geração de dossiê | `.claude/agents/subagente-pesquisador.md` |
| `subagente-redator-capitulo` | Estratégia + Redação EITA + Mermaid + CI de código + Auto-validação por capítulo | `.claude/agents/subagente-redator-capitulo.md` |
| `subagente-revisor-tecnico` | Correção paralela, em lotes, dos capítulos reprovados na auditoria | `.claude/agents/subagente-revisor-tecnico.md` |

> **Concorrência controlada (V3):** os subagentes de capítulo são despachados em **lotes de 4**
> pelo pool (`scripts/pool-capitulos.py`), nunca 16 de uma vez. Isso evita throttling de
> TPM/RPM da API e estouro de contexto do Orquestrador, e habilita retentativa com backoff
> exponencial por capítulo.

### 2.4 MCPs (Ferramentas de Execução)

MCPs (Model Context Protocol) são servidores que fornecem ferramentas concretas para o agente executar operações no sistema de arquivos, banco de dados, etc.

| MCP | Função | Tecnologia |
|-----|--------|------------|
| **`db_state`** | Persiste estado da esteira (fase, payload, transições) | SQLite via `mcp-server-sqlite-npx` |
| **`file_writer`** | Leitura e escrita de arquivos no projeto | `@modelcontextprotocol/server-filesystem` |
| **`pdf_gen`** | Geração de PDF via CloudConvert (fallback) | Servidor custom local (Node.js + fetch) |
| **`mcp_deep_search`** | Prospecção web — mapeado para WebSearch/WebFetch nativos | Ferramentas nativas da CLI |

> **Nota:** `pdf_gen` é servidor MCP custom escrito para este projeto, usado como método
> alternativo (fallback). O método principal de PDF é Pandoc+Typst via script Python/PowerShell.

### 2.5 Scripts de Automação (100% Locais)

Scripts que executam tarefas pesadas de compilação e conversão sem depender
de API keys externas.

| Script | Linguagem | O que faz |
|--------|-----------|-----------|
| `scripts/indexar-dossie.py` | Python | **Upgrade 6** — Índice RAG local do dossiê (TF-IDF puro) + busca por bloco |
| `scripts/pool-capitulos.py` | Python | **Upgrade 4** — Planeja lotes de despacho, rastreia tentativas, calcula backoff exponencial |
| `scripts/renderizar-diagramas.py` | Python | **Upgrade 2** — Renderiza blocos ```mermaid em PNG (cache por hash) e valida sintaxe |
| `scripts/validar-codigo.py` | Python | **Upgrade 3** — CI de sintaxe dos blocos de código (sem executar código do livro) |
| `scripts/auditar-obra.py` | Python | **Upgrade 1** — Audita os requisitos automatizáveis (R1-R4, R9-R14), sobreposição entre capítulos, terminologia, truncamento |
| `scripts/metadados_livro.py` | Python | **Upgrade 5** — Paleta da capa, ficha catalográfica (CIP), sinopse da contracapa |
| `compilar-para-pdf.py` | Python | Compila capítulos → Markdown → diagramas → PDF via Pandoc → `.typ` → Typst |
| `compilar-mega-livro.py` | Python | Compila 15 livros AIDD em um mega-livro único com PDF |
| `scripts/converter-md-pdf.ps1` | PowerShell | Converte `livro_final.md` → `livro_final.pdf` via Pandoc+Typst |
| `compilar-livro.mjs` | Node.js | Compila capítulos → Markdown → PDF (Pandoc+Typst + fallback CloudConvert) |

### 2.6 Templates

| Template | Conteúdo | Localização |
|----------|----------|-------------|
| **template.typ** | Template Typst ABNT: margens 3/2cm, Times New Roman 12pt, sumário automático, **capa gráfica com paleta por obra, folha de rosto, ficha catalográfica (CIP) e contracapa** | `templates/template.typ` |
| **template_eita.md** | Molde pedagógico EITA-V2 (7 seções obrigatórias, **diagrama Mermaid na Ilustra, código validável na Técnica**) | `templates/template_eita.md` |
| **payload_estado.json** | Schema de payload de estado entre agentes | `templates/payload_estado.json` |

---

## 3. Fluxo Completo Passo a Passo

### 3.0 Diagrama de Estados

```
  [Tema Informado]
        │
        ▼
  ┌───────────────────────┐
  │ Passo 0 — Preparação  │  slug, db_state
  └─────────┬─────────────┘
            ▼
  ┌───────────────────────────────────┐
  │ Passo 1 — Fase 1 (P&D)            │
  │  pesquisador → indexar-dossie     │
  │  → arquiteto                      │
  │  Saída: dossiê + índice RAG +     │
  │         sumario_macro             │
  └─────────┬─────────────────────────┘
            ▼
   ╔══════════════════════════════════════════════════════╗
   ║ Passo 2 — Fase 2 (Manufatura Paralela EM LOTES)      ║
   ║  pool-capitulos --plano --lote 4                      ║
   ║  [subagente-redator-capitulo] x4 por lote            ║
   ║  (estrategista → redator-eita → mermaid →            ║
   ║   CI de código → auto-validação → registrar)         ║
   ║  falha → backoff exponencial (máx. 3 tentativas)     ║
   ╚══════════════════════════════════════════════════════╝
            │ (nenhum capítulo pendente no pool)
            ▼
   ╔══════════════════════════════════════════════════════╗
   ║ Passo 3 — Fase 2.5 (Peer Review Autônomo)            ║
   ║  auditar-obra + validar-codigo + validar diagramas   ║
   ║  → revisor-tecnico / [subagente-revisor-tecnico]     ║
   ║  Saída: revisao/parecer_revisao.md                    ║
   ╚══════════════════════════════════════════════════════╝
            │ (CONFORME ou COM RESSALVAS)
            ▼
  ┌───────────────────────────────────────┐
  │ Passo 4 — Fase 3 (Acabamento)         │
  │  compilador-abnt: merge + ABNT        │
  │  Nó 9.5: mermaid → PNG                │
  │  Nó 9.6: capa gráfica + ficha CIP     │
  │  Nó 10: Pandoc → .typ → Typst → PDF   │
  └─────────┬─────────────────────────────┘
            ▼
  ┌──────────────────────┐
  │ Passo 5 — Relatório   │  caminhos + checklist R1-R14
  └──────────────────────┘
```

---

### 3.1 Passo 0 — Preparação

| Atributo | Detalhe |
|----------|---------|
| **Quem faz** | Orquestrador Mestre (o próprio agente AI) |
| **Entrada** | `$ARGUMENTS` = tema central da obra |
| **Ferramenta** | Nenhuma específica |
| **Duração** | Instantâneo |

**O que faz:**
1. Deriva o `slug` em kebab-case a partir do tema (ex: "Observabilidade com OpenTelemetry" → `observabilidade-opentelemetry`)
2. Verifica se `output/<slug>/` já existe
3. Se existir, gera sufixo automático (`<slug>-v2`, `<slug>-v3`, etc.)
4. Cria as pastas: `output/<slug>/`, `output/<slug>/capitulos/`, `output/<slug>/pesquisa/`
5. Registra o início no MCP `db_state`:
   ```json
   {
     "fase_atual": "fase_1_pesquisa",
     "estado_execucao": "iniciado_via_comando"
   }
   ```

**Resultado esperado:**
```
output/<slug>/
├── capitulos/     (vazio)
├── pesquisa/      (vazio)
└── sumario_macro.json  (ainda não criado)
```

---

### 3.2 Passo 1 — Fase 1 (P&D e Inteligência)

| Atributo | Detalhe |
|----------|---------|
| **Quem faz** | `subagente-pesquisador` → `arquiteto` |
| **Como faz** | WebSearch/WebFetch para pesquisa; geração de JSON estruturado para o sumário |
| **Entrada** | Tema da obra |
| **Saída** | Dossiê de pesquisa + `sumario_macro.json` |
| **Duração** | 2-5 minutos |

#### Etapa 1A — Pesquisa (Nó 0A)

**Quem:** `subagente-pesquisador` (invoca a skill `pesquisador`)

**O que faz:**
1. Realiza múltiplas buscas web sobre o tema
2. Consulta artigos científicos (arXiv, ACM, IEEE) — mínimo 7 papers
3. Gera dossiê técnico em `output/<slug>/pesquisa/dossie_<slug>.md` contendo:
   - Conceitos-chave e definições
   - Estado da arte
   - Casos de uso reais
   - Riscos e limitações
   - Fontes brutas com URLs (15+ fontes rastreáveis)
   - Artigos científicos no formato ABNT

**Resultado:**
```
output/<slug>/pesquisa/dossie_<slug>.md
```

#### Etapa 1B — Arquitetura (Nó 0B)

**Quem:** Skill `arquiteto`

**O que faz:**
1. Analisa o dossiê de pesquisa
2. Desenha o sumário macro da obra — estrutura de Partes e Capítulos
3. Valida requisitos contratuais:
   - Mínimo **16 capítulos** (R1)
   - Mínimo **70 páginas** estimadas (R2)
   - Estrutura EITA-V2 para cada capítulo (R3)
4. Gera `output/<slug>/sumario_macro.json`

**Formato do sumario_macro.json:**
```json
{
  "titulo_obra": "Título do Livro",
  "subtitulo": "Subtítulo opcional",
  "slug": "slug-da-obra",
  "introducao": "Texto de introdução para o prefácio",
  "conclusao": "Texto de síntese para a conclusão",
  "partes": [
    {
      "parte": 1,
      "titulo_parte": "Título da Parte",
      "capitulos": [
        { "capitulo": 1, "titulo": "Título do Capítulo" },
        { "capitulo": 2, "titulo": "..." }
      ]
    }
  ]
}
```

**Regra de autonomia (REGRA 3):** O Orquestrador avança automaticamente para a Fase 2 assim que o `sumario_macro.json` é gerado, sem pausar para confirmação manual.

**Resultado:**
```
output/<slug>/sumario_macro.json
```

---

### 3.3 Passo 2 — Fase 2 (Manufatura Tática Paralela em Lotes)

| Atributo | Detalhe |
|----------|---------|
| **Quem faz** | `subagente-redator-capitulo` em **lotes de 4** (pool de concorrência) |
| **Como faz** | O Orquestrador despacha um lote, aguarda o lote inteiro, registra o desfecho de cada capítulo e só então despacha o próximo |
| **Entrada** | `sumario_macro.json` + blocos do dossiê obtidos por RAG |
| **Saída** | Capítulos completos em Markdown |
| **Duração** | 10-40 minutos (lotes serializados em troca de estabilidade contra rate-limit) |

#### Etapa 2A — Planejamento do despacho (Upgrade 4)

```bash
python scripts/pool-capitulos.py <slug> --plano --lote 4     # plano completo
python scripts/pool-capitulos.py <slug> --proximo-lote       # próximo lote a despachar
python scripts/pool-capitulos.py <slug> --pendentes          # fila de retentativa
python scripts/pool-capitulos.py <slug> --status             # progresso
```

O pool considera um capítulo entregue somente se `cap_<n>.md` existir, tiver as 7 seções
EITA-V2 e corpo mínimo. Falhas são registradas com backoff exponencial
(15s → 30s → 60s, máximo 3 tentativas); depois disso o capítulo é marcado `esgotado`
e reportado como não conformidade — a esteira nunca fica travada.

#### Etapa 2B — Redação dos Capítulos

**Quem:** `subagente-redator-capitulo` (um por capítulo, 4 por lote)

**Fluxo interno do subagente:**
1. **Pesquisa contextual por RAG** (Upgrade 6) — em vez de carregar o dossiê inteiro:
   ```bash
   python scripts/indexar-dossie.py <slug> --buscar "<termos do capítulo>" --topo 4
   ```
2. **Estrategista** (skill `estrategista`): decompõe o tema do capítulo em 3 pilares lógicos
   - Gera `cap_<n>_draft.json` com os pilares, `ancora_visual` (especificação do diagrama
     Mermaid) e `entrega_tecnica` (artefato de código)
3. **Redator EITA** (skill `redator-eita`): expande o texto seguindo o template EITA-V2:
   - 7 seções obrigatórias: **Introdução, Explica, Ilustra, Técnica, Aplica, Conclusão, Referências**
   - **1+ diagrama ```mermaid na seção Ilustra, com `%% legenda:` (R11)**
   - **1+ bloco de código com linguagem declarada na seção Técnica (R12)**
   - Mínimo 3 referências ABNT por capítulo (R4)
   - Mínimo 3 citações inline `[N]` (R10)
   - 60%+ do conteúdo na seção Técnica
4. **Auto-validação determinística:**
   ```bash
   python scripts/validar-codigo.py <slug> --capitulo <n>
   python scripts/renderizar-diagramas.py <slug> --capitulos --validar
   ```
   - Se falhar, reaplica correção internamente (REGRA 4), no máximo 3 rodadas
   - Quando OK, registra no pool e transiciona estado para `concluido_autonomo`

**Resultado por capítulo:**
```
output/<slug>/capitulos/
├── cap_<n>.md              ← capítulo completo em Markdown
├── cap_<n>_draft.json      ← draft pedagógico (3 pilares)
├── cap_<n>_estado.json     ← estado de execução
└── _pool_estado.json       ← tentativas e estado de todos os capítulos
```

---

### 3.4 Passo 3 — Fase 2.5 (Revisão Técnica Autônoma / Peer Review)

| Atributo | Detalhe |
|----------|---------|
| **Quem faz** | Skill `revisor-tecnico` + `subagente-revisor-tecnico` (lotes de 4) |
| **Pré-condição** | Nenhum capítulo pendente no pool |
| **Como faz** | Auditoria determinística por script → correção dirigida por evidência |
| **Saída** | `revisao/parecer_revisao.md` + capítulos corrigidos |
| **Duração** | 5-20 minutos |

#### Etapa 3A — Auditoria determinística (Upgrades 1 e 3)

```bash
python scripts/auditar-obra.py <slug>
python scripts/validar-codigo.py <slug>
python scripts/renderizar-diagramas.py <slug> --capitulos --validar
```

O auditor verifica os requisitos automatizáveis (R1-R4 e R9-R14 — R5, R6, R7 e R8
dependem de julgamento e ficam com o `pesquisador`, o `compilador-abnt` e o
`revisor-tecnico`) e, além disso, detecta os defeitos que só aparecem quando se
olha a obra inteira:

| Defeito | Método de detecção |
|---|---|
| Sobreposição de conteúdo entre capítulos | Shingles de 6 palavras + Jaccard ≥ 0,45 entre parágrafos de capítulos diferentes |
| Grafia inconsistente de termos técnicos | Agrupamento por forma normalizada (sem acento, sem hífen) e comparação de variantes |
| Capítulo truncado | Última linha sem pontuação de fechamento |
| Pendência textual | `TODO`, `FIXME`, `TBD`, `placeholder`, `[inserir`, `lorem ipsum` |
| Citação órfã | `[N]` no corpo sem entrada correspondente na seção 7 |

#### Etapa 3B — Correção

A skill `revisor-tecnico` lê os relatórios JSON (não os capítulos inteiros — lean-ctx) e
corrige por classe de defeito. Sobreposição é resolvida reescrevendo o trecho do capítulo
**posterior** como referência cruzada ("como visto no Capítulo N, ..."). Termos divergentes
são padronizados na forma canônica em toda a obra.

#### Etapa 3C — Reauditoria e veredito

```bash
python scripts/auditar-obra.py <slug> --estrito
python scripts/validar-codigo.py <slug> --estrito
```

Máximo de 3 rodadas. O que restar é registrado como ressalva no parecer — a obra segue
para a Fase 3 de qualquer forma (o Markdown nunca deixa de ser expedido).

**Resultado:**
```
output/<slug>/
├── revisao/
│   ├── relatorio_auditoria.json   ← R1-R4/R9-R14, sobreposição, terminologia
│   └── parecer_revisao.md         ← veredito + correções aplicadas
└── validacao/
    ├── relatorio_codigo.json      ← sintaxe por bloco de código
    └── relatorio_diagramas.json   ← diagramas renderizados / com falha
```

---

### 3.5 Passo 4 — Fase 3 (Acabamento & ABNT)

| Atributo | Detalhe |
|----------|---------|
| **Quem faz** | Skill `compilador-abnt` |
| **Pré-condição** | Parecer da Fase 2.5 gravado |
| **Como faz** | Merge manual (via skill) OU scripts automatizados |
| **Entrada** | `sumario_macro.json`, `capitulos/cap_*.md` |
| **Saída** | `livro_final.md` + `livro_final.pdf` |
| **Duração** | 2-10 minutos (dependendo do tamanho) |

#### Método A — Automatizado (Recomendado)

**Script Python (`compilar-para-pdf.py`):**
```bash
python compilar-para-pdf.py <slug> --paginas-exatas
```

**O que faz:**
1. Lê todos os `cap_<n>.md` do diretório `capitulos/` (Nó 5)
2. Concatena na ordem correta do sumário (Nó 5)
3. Remove frontmatter YAML interno dos capítulos
4. Inclui `introducao.md` se existir (Prefácio — Nó 6)
5. Inclui `conclusao.md` se existir (Conclusão — Nó 6)
6. Extrai título do `sumario_macro.json` para metadados (Nó 8)
7. Aplica formatação ABNT com YAML frontmatter (Nó 8):
   ```yaml
   title: "Título da Obra"
   author: "Heverton Eduardo Peres"
   date: "Julho 2026"
   lang: pt-BR
   ```
8. Grava `output/<slug>/livro_final.md` (Nó 9)
9. **Renderiza os diagramas Mermaid em PNG (Nó 9.5 — Upgrade 2):**
   - `imagens/diagramas/dia_<contexto>_<seq>_<hash>.png`, escala 3 (≈300 dpi)
   - grava `_livro_render.md` com os blocos substituídos por figuras com legenda
   - cache por hash do diagrama: rodar de novo não re-renderiza o que não mudou
   - diagrama inválido permanece como bloco de código e a compilação segue
10. **Deriva capa gráfica, ficha catalográfica e sinopse (Nó 9.6 — Upgrade 5)**
11. Converte para PDF via **Pandoc → `.typ` → `typst compile --root`** com template ABNT (Nó 10):
   - Margens ABNT: 3cm superior/esquerda, 2cm inferior/direita
   - Tipografia: Times New Roman / Liberation Serif, 12pt
   - Parágrafos justificados com recuo 1.25cm
   - Capa gráfica colorida (paleta determinística por slug), folha de rosto,
     ficha catalográfica (CIP fictícia) e contracapa com sinopse
   - Cabeçalho com título da obra (a partir da página 2)
   - Rodapé com paginação "X de Y"
   - Sumário automático com 3 níveis
   - Blocos de código com fundo cinza claro; figuras a 88% da mancha com legenda
   - Quebra de página antes de cada título nível 1
12. Com `--paginas-exatas`, compila uma segunda vez para gravar a paginação real na CIP

> **Por que não `pandoc --pdf-engine=typst`:** nesse modo o Pandoc extrai as imagens para
> uma pasta temporária e reescreve os caminhos em forma absoluta; o Typst recusa caminho
> absoluto no Windows (`path contains invalid component "C:"`) e a compilação falha em
> qualquer livro com figuras. Gerando o `.typ` dentro da pasta do livro, os caminhos
> relativos das figuras continuam válidos.

#### Método B — Script PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File scripts/converter-md-pdf.ps1 -Slug <slug>
```

Equivalente ao método Python, com detecção automática dos executáveis Pandoc/Typst.

#### Método C — Manual (via Skill)

Se os scripts automatizados não estiverem disponíveis, a skill `compilador-abnt`
guia o agente passo a passo pelos Nós 5 a 10 descritos acima.

#### Caso de Borda: Falha no PDF

Se Pandoc ou Typst não estiverem disponíveis:
1. O Markdown (`livro_final.md`) é expedido normalmente — **nunca bloqueia a entrega**
2. O script tenta fallback para CloudConvert via `compilar-livro.mjs` (requer API key)
3. Se ambos falharem, a pendência do PDF é reportada objetivamente em relatório final

**Resultado:**
```
output/<slug>/
├── livro_final.md             ← Markdown completo formatado
├── livro_final.pdf            ← PDF ABNT (Pandoc+Typst)
└── <slug>.pdf                 ← cópia com nome do slug
```

---

### 3.6 Passo 5 — Relatório Final

| Atributo | Detalhe |
|----------|---------|
| **Quem faz** | Orquestrador Mestre |
| **Entrada** | Artefatos finais + relatórios JSON das Fases 2 e 2.5 |
| **Saída** | Mensagem objetiva ao operador |

**O que faz:**
1. Coleta estatísticas: total de capítulos, páginas do PDF, tamanho do PDF, diagramas
   renderizados, taxa de aprovação do CI de código
2. Valida conformidade com requisitos contratuais (R1-R14)
3. Exibe relatório objetivo contendo:
   - Caminho do `livro_final.md`
   - Status do `livro_final.pdf`
   - Total de capítulos produzidos e capítulos `esgotado` (se houver)
   - Veredito da auditoria (CONFORME / COM RESSALVAS / NÃO CONFORME)
   - Resumo de subagentes executados
   - Lista de conformidade (R1-R14: OK ou FALHA)

---

## 4. Comandos de Entrada

### 4.1 `/criar-livro <tema>` — Produzir um Novo Livro

Ponto de entrada principal da fábrica. Dispara o fluxo completo da obra.

```
/criar-livro Observabilidade em Sistemas Distribuídos com OpenTelemetry
```

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `$ARGUMENTS` | Sim | Tema central da obra (texto livre) |

### 4.2 `/compilar-mega-livro <slugs>` — Compilar Múltiplos Livros

Compila livros existentes em um único mega-livro estruturado.

```
/compilar-mega-livro 01-aidd-ai-driven-development 02-harness-camada-orquestracao
/compilar-mega-livro --todas
/compilar-mega-livro --all
```

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `<slug1> [slug2] ...` | Alternativo | Slugs específicos dos livros a compilar |
| `--todas` / `--all` | Alternativo | Compila todos os livros AIDD (exceto mega-livro) |

**Fluxo da compilação:**
1. Define slug do compilado (com timestamp se `--todas`: `compilado-completo-aidd-2026-07-30`)
2. Cria pasta limpa (`rm -rf` + `mkdir -p`)
3. Unifica sumários macro de todos os livros fonte
4. Concatena e **renumera** capítulos sequencialmente (1 a N)
5. Gera prefácio, sumário dinâmico e conclusão geral
6. Monta `livro_final.md` na pasta do compilado
7. Gera PDF via Pandoc+Typst
8. Valida: existência, numeração sem saltos, tamanho

### 4.3 Compilação Direta via Script

```bash
# Compilar um livro específico (com paginação real na ficha catalográfica)
python compilar-para-pdf.py <slug> --paginas-exatas

# Compilar todos os livros cadastrados
python compilar-para-pdf.py

# Compilar sem diagramas ou sem capa gráfica
python compilar-para-pdf.py <slug> --sem-diagramas --sem-capa

# Compilar mega-livro completo
python compilar-mega-livro.py
```

### 4.4 Auditoria e Validação Isoladas

```bash
# Auditoria contratual dos requisitos automatizáveis (R1-R4, R9-R14) + sobreposição + terminologia
python scripts/auditar-obra.py <slug>

# CI de sintaxe dos blocos de código
python scripts/validar-codigo.py <slug> --estrito

# Validar apenas a sintaxe dos diagramas Mermaid
python scripts/renderizar-diagramas.py <slug> --capitulos --validar

# RAG do dossiê
python scripts/indexar-dossie.py <slug> --indexar
python scripts/indexar-dossie.py <slug> --buscar "cardinalidade metricas" --topo 4

# Pool de concorrência
python scripts/pool-capitulos.py <slug> --plano --lote 4
python scripts/pool-capitulos.py <slug> --pendentes

# Metadados de capa e ficha catalográfica
python scripts/metadados_livro.py <slug>
```

---

## 5. Estrutura de Diretórios de uma Obra

```
output/<slug>/
│
├── sumario_macro.json           ← Planta baixa da obra (Partes/Capítulos)
├── livro_final.md               ← Obra completa em Markdown
├── livro_final.pdf              ← PDF formatado ABNT
├── <slug>.pdf                   ← Cópia do PDF com nome do slug
│
├── capitulos/
│   ├── cap_1.md                 ← Capítulo 1 completo (Markdown EITA-V2)
│   ├── cap_1_draft.json         ← Draft pedagógico (3 pilares)
│   ├── cap_1_estado.json        ← Estado de execução do capítulo
│   ├── cap_2.md
│   ├── _pool_estado.json        ← Tentativas/estado no pool de concorrência
│   └── ...
│
├── pesquisa/
│   ├── dossie_<slug>.md         ← Dossiê de pesquisa com fontes e papers
│   └── indice_dossie.json       ← Índice RAG (blocos + IDF) do dossiê
│
├── imagens/
│   └── diagramas/               ← PNGs dos diagramas Mermaid (cache por hash)
│       └── dia_livro_01_<hash>.png
│
├── revisao/
│   ├── relatorio_auditoria.json ← R1-R4/R9-R14, sobreposição, terminologia
│   └── parecer_revisao.md       ← Parecer da Fase 2.5
│
└── validacao/
    ├── relatorio_codigo.json    ← Sintaxe por bloco de código
    └── relatorio_diagramas.json ← Diagramas renderizados / com falha
```

---

## 6. Portabilidade Multi-IDE

A Fábrica é projetada para funcionar em **qualquer IDE/CLI agêntica** que suporte
o formato de regras do projeto:

| IDE/CLI | Arquivo de Regras | Origem |
|---------|-------------------|--------|
| Claude Code | `.claude/skills/`, `.claude/commands/`, `.mcp.json` | **Fonte da verdade** |
| Cursor | `.cursor/rules/fabrica-agentica.mdc` | Hardlink de `CLAUDE.md` |
| Windsurf | `.windsurfrules` | Hardlink de `CLAUDE.md` |
| Cline | `.clinerules` | Hardlink de `CLAUDE.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | Hardlink de `CLAUDE.md` |
| Codex | `AGENTS.md` | Hardlink de `CLAUDE.md` |

Os diretórios `agentic/` são **junctions** (Windows) ou **symlinks** (macOS/Linux)
que espelham `.claude/` para acesso neutro.

**Para recriar os links após clonar o projeto:**
```powershell
# Windows
.\scripts\setup-links.ps1
```

```bash
# macOS/Linux
bash scripts/setup-links.sh
```

---

## 7. Resumo dos Requisitos Contratuais (R1-R14)

| # | Requisito | Mínimo | Onde se aplica | Verificação automática |
|---|-----------|--------|----------------|------------------------|
| R1 | Capítulos | 16 por obra | Sumário macro | `auditar-obra.py` |
| R2 | Páginas | ~70 (~175K caracteres ABNT) | Compilação final | `auditar-obra.py` |
| R3 | Estrutura do capítulo | 7 seções (EITA-V2) | Cada capítulo | `auditar-obra.py` |
| R4 | Referências por capítulo | 3 ABNT | Seção "Referências" | `auditar-obra.py` |
| R5 | Artigos no dossiê | 3 papers | Pesquisa/P&D | Skill `pesquisador` |
| R6 | Formatação ABNT | Livro completo (capa gráfica, folha de rosto, CIP, sumário) | Compilação | `template.typ` |
| R7 | PDF final | 1 arquivo .pdf | Pandoc → `.typ` → Typst | `compilar-para-pdf.py` |
| R8 | Tom transformacional | Acessível + denso | Redação EITA | Skill `revisor-tecnico` |
| R9 | Sem horizontal rules | Nenhum `---` no capítulo | Cada capítulo | `auditar-obra.py` |
| R10 | Citações inline [N] | 3 por capítulo | Seção Técnica/Explica | `auditar-obra.py` |
| R11 | Diagrama Mermaid | 1 por capítulo | Seção Ilustra | `auditar-obra.py` + `renderizar-diagramas.py --validar` |
| R12 | Código validado | 1 bloco aprovado no CI | Seção Técnica | `validar-codigo.py` |
| R13 | Sem truncamento | Nenhum TODO/placeholder | Cada capítulo | `auditar-obra.py` |
| R14 | Rastreabilidade | Todo `[N]` existe na seção 7 | Cada capítulo | `auditar-obra.py` |

---

## 8. Glossário

| Termo | Significado |
|-------|-------------|
| **Slug** | Identificador em kebab-case do livro (ex: `observabilidade-opentelemetry`) |
| **EITA-V2** | Framework pedagógico: **E**xplica, **I**lustra, **T**écnica, **A**plica + Introdução + Conclusão + Referências |
| **Skill** | Instrução executável carregada pelo agente AI (arquivo `SKILL.md`) |
| **Subagente** | Fluxo multi-passo que combina várias skills |
| **MCP** | Model Context Protocol — servidor que expõe ferramentas para o agente AI |
| **Nó** | Etapa numerada dentro de uma fase (Nó 0A, Nó 0B, Nós 1-10) |
| **Sumário macro** | JSON com a estrutura completa da obra (Partes + Capítulos) |
| **ABNT** | Formatação segundo normas da Associação Brasileira de Normas Técnicas |
| **Pandoc+Typst** | Pipeline de conversão Markdown → `.typ` → PDF (100% local, sem API key) |
| **Pool de concorrência** | Fila que despacha os subagentes de capítulo em lotes de 4, com retentativa e backoff exponencial (`scripts/pool-capitulos.py`) |
| **Backoff exponencial** | Espera crescente entre retentativas (15s → 30s → 60s, teto de 240s) para não agravar rate-limit |
| **RAG local** | Busca por relevância nos blocos do dossiê (TF-IDF puro em Python), sem carregar o dossiê inteiro no contexto |
| **CI de código** | Validação de sintaxe de cada bloco de código do livro, sem executar o código (`scripts/validar-codigo.py`) |
| **Shingles / Jaccard** | Técnica usada pelo auditor para achar parágrafos quase idênticos entre capítulos diferentes |
| **CIP** | Ficha catalográfica (Catalogação na Publicação), gerada de forma fictícia para diagramação |
| **Cutter** | Notação alfanumérica de autoria usada na ficha catalográfica (ex.: `P265o`) |
| **Fase 2.5** | Peer review autônomo entre a manufatura dos capítulos e a compilação ABNT |
| **Hardlink** | Link de arquivo no sistema de arquivos (mesmo conteúdo físico, nomes diferentes) |
| **Junction** | Link de diretório no Windows (equivalente a symlink para pastas) |
