# Fluxo de Funcionamento da Fábrica Agêntica de Livros

> Documento oficial do fluxo operacional completo.
> Versão: Julho 2026 | Projeto: Fábrica Agêntica de Livros

---

## 1. Visão Geral

A **Fábrica Agêntica de Livros** é uma esteira editorial automatizada que produz livros técnicos completos — do tema à entrega de PDF formatado (ABNT) — utilizando agentes de IA (Claude Code, Cursor, Windsurf, Codex, etc.) como força de trabalho.

A fábrica opera em **3 Fases** (P&D, Manufatura, Acabamento), executadas por um **Orquestrador Mestre** que coordena **Skills** (operários especializados), **Subagentes** (equipes paralelas), **MCPs** (ferramentas de execução) e **Scripts** (automação local).

### Princípios Operacionais

| Regra | Descrição |
|-------|-----------|
| **REGRA 1** | Tudo em PT-BR estrito (comunicação, logs, artefatos) |
| **REGRA 2** | Sem metatexto ou saudações nos artefatos — Markdown limpo |
| **REGRA 3** | Autonomia total após o tema ser definido (sem paradas no chat) |
| **REGRA 4** | Auto-correção interna de desvios estruturais antes da entrega |

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
| `compilador-abnt` | 3 (Nós 5-10) | Merge final, ABNT, PDF via Pandoc+Typst | `.claude/skills/compilador-abnt/SKILL.md` |
| `compilador-mega-livro` | Pós-produção | Compila múltiplos livros em um só | `.claude/skills/compilador-mega-livro/SKILL.md` |

### 2.3 Subagentes (Execução Paralela)

Subagentes implementam fluxos multi-passo que combinam várias skills.
São disparados em paralelo para acelerar a produção.

| Subagente | O que faz | Arquivo |
|-----------|-----------|---------|
| `subagente-pesquisador` | Varredura web profunda + geração de dossiê | `.claude/agents/subagente-pesquisador.md` |
| `subagente-redator-capitulo` | Estratégia + Redação EITA + Auto-validação por capítulo | `.claude/agents/subagente-redator-capitulo.md` |

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
| `compilar-para-pdf.py` | Python | Compila capítulos → Markdown → PDF via Pandoc+Typst |
| `compilar-mega-livro.py` | Python | Compila 15 livros AIDD em um mega-livro único com PDF |
| `scripts/converter-md-pdf.ps1` | PowerShell | Converte `livro_final.md` → `livro_final.pdf` via Pandoc+Typst |
| `compilar-livro.mjs` | Node.js | Compila capítulos → Markdown → PDF (Pandoc+Typst + fallback CloudConvert) |
| `expandir-livros.py` | Python | Expande livros adicionando novos capítulos automaticamente |
| `expandir-todos-livros.py` | Python | Expande todos os livros cadastrados |
| `merge-livros.py` | Python | Combina múltiplos arquivos Markdown/PDF em um só |

### 2.6 Templates

| Template | Conteúdo | Localização |
|----------|----------|-------------|
| **template.typ** | Template Typst ABNT: margens 3/2cm, Times New Roman 12pt, sumário automático | `templates/template.typ` |
| **template_eita.md** | Molde pedagógico EITA-V2 (7 seções obrigatórias por capítulo) | `templates/template_eita.md` |
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
  │  pesquisador → arquiteto          │
  │  Saída: dossiê + sumario_macro    │
  └─────────┬─────────────────────────┘
            ▼
   ╔══════════════════════════════════════════════════════╗
   ║ Passo 2 — Fase 2 (Manufatura Paralela)               ║
   ║  [subagente-redator-capitulo] para CADA capítulo     ║
   ║  (estrategista → redator-eita → auto-validação)      ║
   ╚══════════════════════════════════════════════════════╝
            │ (todos os capítulos concluídos)
            ▼
  ┌───────────────────────────────────────┐
  │ Passo 3 — Fase 3 (Acabamento)         │
  │  compilador-abnt: merge + ABNT        │
  │  Pandoc+Typst → PDF                   │
  └─────────┬─────────────────────────────┘
            ▼
  ┌──────────────────────┐
  │ Passo 4 — Relatório   │  caminhos + estatísticas
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

### 3.3 Passo 2 — Fase 2 (Manufatura Tática Paralela)

| Atributo | Detalhe |
|----------|---------|
| **Quem faz** | Múltiplos `subagente-redator-capitulo` em paralelo |
| **Como faz** | Cada subagente é instanciado independentemente, processando capítulos em paralelo |
| **Entrada** | `sumario_macro.json` com coordenadas de Partes/Capítulos |
| **Saída** | Capítulos completos em Markdown |
| **Duração** | 10-30 minutos (dependendo do número de capítulos e paralelismo) |

#### Etapa 2A — Redação dos Capítulos

**Quem:** `subagente-redator-capitulo` (um por capítulo, em paralelo)

**Fluxo interno do subagente:**
1. **Estrategista** (skill `estrategista`): decompõe o tema do capítulo em 3 pilares lógicos
   - Gera `cap_<n>_draft.json` com os pilares e âncora visual
2. **Redator EITA** (skill `redator-eita`): expande o texto seguindo o template EITA-V2:
   - 7 seções obrigatórias: **Introdução, Explica, Ilustra, Técnica, Aplica, Conclusão, Referências**
   - Mínimo 3 referências ABNT por capítulo (R4)
   - Mínimo 3 citações inline `[N]` (R10)
   - 60%+ do conteúdo na seção Técnica
3. **Auto-validação:** verifica conformidade com o template EITA-V2
   - Se falhar, reaplica correção internamente (REGRA 4)
   - Quando OK, transiciona estado para `concluido_autonomo`

**Resultado por capítulo:**
```
output/<slug>/capitulos/
├── cap_<n>.md              ← capítulo completo em Markdown
├── cap_<n>_draft.json      ← draft pedagógico (3 pilares)
└── cap_<n>_estado.json     ← estado de execução
```

---

### 3.4 Passo 3 — Fase 3 (Acabamento & ABNT)

| Atributo | Detalhe |
|----------|---------|
| **Quem faz** | Skill `compilador-abnt` |
| **Pré-condição** | Todos os capítulos finalizados |
| **Como faz** | Merge manual (via skill) OU scripts automatizados |
| **Entrada** | `sumario_macro.json`, `capitulos/cap_*.md` |
| **Saída** | `livro_final.md` + `livro_final.pdf` |
| **Duração** | 2-10 minutos (dependendo do tamanho) |

#### Método A — Automatizado (Recomendado)

**Script Python (`compilar-para-pdf.py`):**
```bash
python compilar-para-pdf.py <slug>
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
   author: "Heberton Peres"
   date: "Julho 2026"
   lang: pt-BR
   ```
8. Grava `output/<slug>/livro_final.md` (Nó 9)
9. Converte para PDF via Pandoc+Typst com template ABNT (Nó 10):
   - Margens ABNT: 3cm superior/esquerda, 2cm inferior/direita
   - Tipografia: Times New Roman / Liberation Serif, 12pt
   - Parágrafos justificados com recuo 1.25cm
   - Cabeçalho com título da obra (a partir da página 2)
   - Rodapé com paginação "X de Y"
   - Sumário automático com 3 níveis
   - Blocos de código com fundo cinza claro
   - Quebra de página antes de cada título nível 1

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

### 3.5 Passo 4 — Relatório Final

| Atributo | Detalhe |
|----------|---------|
| **Quem faz** | Orquestrador Mestre |
| **Entrada** | Artefatos finais |
| **Saída** | Mensagem objetiva ao operador |

**O que faz:**
1. Coleta estatísticas: total de capítulos, páginas estimadas, tamanho do PDF
2. Valida conformidade com requisitos contratuais (R1-R10)
3. Exibe relatório objetivo contendo:
   - Caminho do `livro_final.md`
   - Status do `livro_final.pdf`
   - Total de capítulos produzidos
   - Resumo de subagentes executados
   - Lista de conformidade (R1-R10: OK ou FALHA)

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
# Compilar um livro específico
python compilar-para-pdf.py <slug>

# Compilar todos os livros cadastrados
python compilar-para-pdf.py

# Compilar mega-livro completo
python compilar-mega-livro.py
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
│   └── ...
│
├── pesquisa/
│   └── dossie_<slug>.md         ← Dossiê de pesquisa com fontes e papers
│
└── capitulos/                   ← (capítulos renumerados, se compilado)
    ├── cap_1.md
    └── ...
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

## 7. Resumo dos Requisitos Contratuais (R1-R10)

| # | Requisito | Mínimo | Onde se aplica |
|---|-----------|--------|----------------|
| R1 | Capítulos | 16 por obra | Sumário macro |
| R2 | Páginas | ~70 (~175K caracteres ABNT) | Compilação final |
| R3 | Estrutura do capítulo | 7 seções (EITA-V2) | Cada capítulo |
| R4 | Referências por capítulo | 3 ABNT | Seção "Referências" |
| R5 | Artigos no dossiê | 3 papers | Pesquisa/P&D |
| R6 | Formatação ABNT | Livro completo | Compilação |
| R7 | PDF final | 1 arquivo .pdf | Pandoc+Typst |
| R8 | Tom transformacional | Acessível + denso | Redação EITA |
| R9 | Citações inline [N] | 3 por capítulo | Seção Técnica/Explica |

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
| **Pandoc+Typst** | Pipeline de conversão Markdown → PDF (100% local, sem API key) |
| **Hardlink** | Link de arquivo no sistema de arquivos (mesmo conteúdo físico, nomes diferentes) |
| **Junction** | Link de diretório no Windows (equivalente a symlink para pastas) |
