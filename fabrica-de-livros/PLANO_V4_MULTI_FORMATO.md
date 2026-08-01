# PLANO V4 — Fábrica Agêntica de Publicações (Multi-Formato)

> **Status:** PROPOSTA — planejamento completo para validação antes de qualquer implementação.
> **Escopo:** expandir a Fábrica (hoje: só livro técnico, fluxo linear `/criar-livro`) para
> uma fábrica multi-formato — **Livro, TCC, Artigo Científico e E-book** — com uma
> **Fase 0 interativa** (`/esbocar`) que substitui as decisões hardcoded do V3 por escolhas
> do operador, e permite disparar cada tipo de obra sozinho ou todos encadeados/paralelos
> a partir de um único tema.

---

## 0. Resumo Executivo

| | V3 (atual) | V4 (proposto) |
|---|---|---|
| Tipos de obra | 1 (livro técnico) | 4 (Livro, TCC, Artigo, E-book) |
| Interação humana | Nenhuma após o tema | 1 rodada de perguntas (`/esbocar`) após o tema |
| Tamanho da obra | Fixo (mín. 16 cap./70 pág.) | Parametrizável (P/M/G para livro; próprio para TCC/artigo/ebook) |
| Refs por capítulo | Fixo em 3 | Parametrizável (5–20) |
| Normas aplicadas | ABNT genérica (livro) | ABNT específica por tipo (NBR 14724, 6022/12820, 6029, todas apoiadas por 6023/10520/6024/6027/6028) + padrão de mercado para ebook (sem ABNT) |
| Motor determinístico | `auditar-obra.py` fixo | Mesmo motor, **parametrizado por tipo** (`--tipo`, `--min-refs`) |
| Saída | 1 PDF | 1 PDF (livro) + N PDFs (artigos) + N EPUBs (ebooks), sob demanda |
| Orquestração | 1 comando linear | Comandos individuais por tipo + 1 comando full (`/produzir-obra-completa`) |

**O que se reaproveita do V3 sem mudança estrutural:** `pool-capitulos.py` (concorrência em
lotes), `indexar-dossie.py` (RAG do dossiê), `renderizar-diagramas.py` (Mermaid → PNG),
`validar-codigo.py` (CI de código), a arquitetura de hardlinks multi-IDE, e o princípio de
"evidência determinística antes de julgamento do agente".

**O que é genuinamente novo:** Fase 0 interativa, parametrização por tipo de obra, redator
acadêmico (tom impessoal, diferente do tom comercial do EITA-V2), pipeline EPUB, fatiamento
de um livro-mãe em N ebooks/artigos, e uma segunda convenção de citação (autor-data) ao lado
da já existente (`[N]` numérico).

---

## 1. Fase 0 — `/esbocar <tema>` (Elicitação Interativa)

Este é o **único** ponto de interação humana da fábrica (mantém a REGRA 3 — autonomia total
depois da elicitação). Implementado com `AskUserQuestion`, em **duas rodadas** porque há
perguntas condicionais (tamanho só faz sentido se for Livro; quantidade só faz sentido se a
resposta anterior for Sim).

### 1.1 Rodada 1 — perguntas sempre feitas (até 4 por chamada)

| # | Pergunta | Opções |
|---|---|---|
| Q1 | Tipo de obra | Livro \| TCC |
| Q2 | Mínimo de referências bibliográficas por capítulo | 5 \| 8 \| 12 \| 16 \| 20 (+ "Other" p/ valor livre) |
| Q3 | Deseja gerar artigos científicos a partir do tema? | Sim \| Não |
| Q4 | Deseja gerar e-books a partir da obra? | Sim \| Não |

### 1.2 Rodada 2 — perguntas condicionais (só as aplicáveis)

| # | Pergunta | Condição | Opções |
|---|---|---|---|
| Q5 | Tamanho do livro | Q1 = Livro | P (1 Parte, 3–5 cap., ~40 pág.) \| M (3 Partes, 9 cap., ~90 pág.) \| G (5 Partes, 10 cap., ~150 pág.) |
| Q6 | Quantos artigos científicos? | Q3 = Sim | 1 \| 2 \| 3 \| 4 \| 5 |
| Q7 | Quantos e-books? | Q4 = Sim | 1–3 \| 4–6 \| 7–10 (+ "Other" p/ valor exato) |

> **Nota sobre o tamanho G:** a especificação do operador tem G com **menos capítulos que M
> (10 vs. 9... na verdade 10 > 9) mas com apenas 5 Partes/10 Capítulos para 150 páginas**,
> ou seja, capítulos mais densos e menos numerosos por parte que M (9 cap. em 3 partes = 3
> cap./parte; G tem 10 cap. em 5 partes = 2 cap./parte). Isso é assumido como intencional
> (capítulos mais profundos em vez de mais numerosos) — **flagado para confirmação**, ver
> seção 9.

### 1.3 Saída da Fase 0

```
output/<slug>/
└── esboco/
    ├── config_obra.json       ← respostas do operador (schema abaixo)
    ├── sumario_macro.json     ← sumário do livro-mãe OU estrutura do TCC (schema por tipo)
    ├── artigos/
    │   └── estrutura_artigos.json   ← N estruturas de artigo (se Q3 = Sim)
    └── ebooks/
        └── estrutura_ebooks.json    ← N estruturas de ebook (se Q4 = Sim)
```

**Schema de `config_obra.json`:**
```json
{
  "tema": "string",
  "tipo_obra": "livro | tcc",
  "min_referencias_por_capitulo": 5,
  "tamanho_obra": "P | M | G | null",
  "gerar_artigos": true,
  "qtd_artigos": 3,
  "gerar_ebooks": true,
  "qtd_ebooks": 5,
  "criado_em": "ISO-8601"
}
```

Ao final da Fase 0, o relatório objetivo (REGRA 2) exibe o sumário gerado e uma única
linha de próximo passo: `/produzir-obra-completa <slug>` (fluxo full) ou os comandos
individuais (`/criar-livro <slug>`, `/criar-tcc <slug>`, `/criar-artigo <slug>`,
`/criar-ebook <slug>`) — sem pedir mais nada ao operador.

---

## 2. Tipos de Obra: Regras e Diferenças

### 2.1 Tabela comparativa

| | Livro | TCC | Artigo Científico | E-book |
|---|---|---|---|---|
| Norma principal | NBR 6029 | NBR 14724 | NBR 6022 / NBR 12820 | Nenhuma (padrão de mercado) |
| Citação | Numérica `[N]` | Autor-data `(SOBRENOME, ano)` | Autor-data `(SOBRENOME, ano)` | Nenhuma obrigatória |
| Tom de redação | Comercial/transformacional (EITA-V2) | Acadêmico impessoal, 3ª pessoa | Acadêmico impessoal, IMRaD | Conversacional, parágrafos curtos |
| Estrutura | Partes → Capítulos (7 seções EITA) | Pré-textual → Textual → Pós-textual | Título/Resumo/Intro/Método/Resultados/Conclusão/Refs | Capa → Créditos → Sumário clicável → Capítulos → CTA |
| Elementos obrigatórios extra | Capa gráfica, ficha CIP | Folha de aprovação, resumo PT+EN, lista de ilustrações | Resumo+abstract, palavras-chave | CTA final, proporção de capa 1:1,6 |
| Formato de saída | PDF (Pandoc→Typst) | PDF (Pandoc→Typst) | PDF (Pandoc→Typst) | **EPUB** (Pandoc nativo) + PDF opcional |
| Diagramas Mermaid | Obrigatório (1/cap.) | Opcional | Opcional | Opcional (herdado do livro-mãe) |
| Origem do conteúdo | Pesquisa própria | Pesquisa própria | Reaproveita dossiê do livro-mãe | Reaproveita capítulos do livro-mãe (reescrita de tom, não pesquisa nova) |

### 2.2 Livro (parametrizado)

Já implementado no V3 (Upgrades 1–6); ganha 2 parâmetros novos vindos de `config_obra.json`:
- `tamanho_obra` (P/M/G) → substitui a constante `MIN_CAPITULOS=16` fixa em `auditar-obra.py`
  por uma tabela `{P: 4, M: 9, G: 10}` (capítulos) e `{P: 100_000, M: 225_000, G: 375_000}`
  (caracteres, ~2.500/página).
- `min_referencias_por_capitulo` → substitui `MIN_REFS_CAPITULO=3` fixo.

### 2.3 TCC (Trabalho de Conclusão de Curso)

**Estrutura NBR 14724** (elementos obrigatórios marcados com ✱):

| Bloco | Elementos |
|---|---|
| Pré-textual | Capa ✱, Folha de rosto ✱, Folha de aprovação ✱ (campo de assinatura como texto placeholder — a Fábrica nunca assina por ninguém), Dedicatória (opcional), Agradecimentos (opcional), Epígrafe (opcional), Resumo em português + palavras-chave ✱ (NBR 6028), Abstract + keywords ✱, Lista de ilustrações/tabelas/abreviaturas (se houver), Sumário ✱ (NBR 6027) |
| Textual | Introdução ✱ (problema, objetivos, justificativa, metodologia), Desenvolvimento ✱ (capítulos/seções numerados progressivamente — NBR 6024, ex. `1`, `1.1`, `1.1.1`), Considerações Finais ✱ |
| Pós-textual | Referências ✱ (NBR 6023), Apêndices (opcional), Anexos (opcional) |

**Diferença crítica de tom:** o TCC **não pode** usar o framework EITA-V2 comercial (proibido
"você vai perceber que...", "ao dominar isso..."). Precisa de um framework novo:

**Framework ACAD (proposto, análogo ao EITA mas acadêmico):**
1. Contextualização — problema de pesquisa, motivação
2. Referencial Teórico — revisão de literatura com citação autor-data densa
3. Análise/Desenvolvimento — corpo argumentativo/técnico da seção
4. Síntese Parcial — fecho da seção, ponte para a próxima (sem tom de "conquista pessoal")

**Citação:** autor-data `(SOBRENOME, ano)` ou `SOBRENOME (ano)` na narrativa, conforme
NBR 10520 — diferente do `[N]` numérico do livro comercial.

### 2.4 Artigo Científico

**Estrutura NBR 6022 / NBR 12820** (formato compacto, tipicamente 10–20 páginas):
Título → Autor(es) → Resumo (150–250 palavras) + palavras-chave (NBR 6028) → Abstract +
keywords → Introdução → Metodologia → Resultados e Discussão → Conclusão → Referências
(NBR 6023).

Cada artigo **não pesquisa do zero**: é gerado a partir de um recorte temático do dossiê
já indexado do livro-mãe (1–2 capítulos de profundidade), usando RAG
(`indexar-dossie.py --buscar`) para reaproveitar as fontes já mineradas — economia de
tokens e de tempo de pesquisa.

### 2.5 E-book (comercial, sem ABNT)

Regras de mercado (Amazon KDP, Hotmart, Kiwify), não acadêmicas:

| Elemento | Especificação |
|---|---|
| Formato | **EPUB reflowable** (padrão-ouro para texto corrido) — Pandoc gera nativamente via `pandoc livro.md -o livro.epub`, reaproveitando o mesmo Markdown do livro |
| Capa | Proporção 1:1,6 (ex. 1600×2560 px), legível em miniatura |
| Página de créditos | Autor, título, ano, ISBN (opcional) |
| Sumário | Clicável (TOC nativo do EPUB — Pandoc gera automaticamente a partir dos headings) |
| Corpo | Parágrafos mais curtos que o livro-mãe, subtítulos frequentes, sem exigência de citação numerada |
| Página final | CTA (redes sociais, outros livros, próximos passos) |
| Ficha catalográfica | Dispensável (não é publicação acadêmica) |

Cada ebook é uma **reescrita de tom** de um recorte do livro-mãe (ex.: 1 Parte inteira, ou
um agrupamento temático de capítulos) — não gera conteúdo novo, apenas adapta o tom
comercial-denso do EITA-V2 para tom comercial-leve de ebook e insere o CTA.

---

## 3. Normas ABNT por Tipo (matriz de referência)

| Norma | O que regula | Onde se aplica |
|---|---|---|
| NBR 14724 | Estrutura de TCC/monografia/dissertação/tese | TCC |
| NBR 6022 | Artigo em publicação periódica | Artigo (periódico) |
| NBR 12820 | Artigo em congresso/simpósio | Artigo (evento) |
| NBR 6029 | Estrutura de livros e folhetos | Livro |
| NBR 6023 | Elaboração de referências | Livro, TCC, Artigo |
| NBR 10520 | Citações no corpo do texto | Livro (numérico), TCC/Artigo (autor-data) |
| NBR 6024 | Numeração progressiva de seções | TCC, Artigo |
| NBR 6027 | Elaboração de sumários | Livro, TCC |
| NBR 6028 | Resumos | TCC, Artigo |

Este resumo vira `docs/normas-abnt-referencia.md` (fonte única, citada por cada
`SPEC_<TIPO>.md` em vez de duplicar o texto da norma em 4 lugares).

---

## 4. Arquitetura Modular (skills/agents/commands/specs por tipo)

### 4.1 Estrutura de pastas proposta

```
.claude/
├── skills/
│   ├── arquiteto/                    (parametrizado: tipo_obra, tamanho_obra)
│   ├── estrategista/                 (reaproveitado por livro; variante leve p/ TCC)
│   ├── redator-eita/                 (existente — tom comercial, livro)
│   ├── redator-academico/            (NOVO — tom acadêmico, TCC + Artigo)
│   ├── redator-ebook/                (NOVO — reescreve tom, não pesquisa)
│   ├── revisor-tecnico/              (existente — reaproveitado, parametrizado por tipo)
│   ├── compilador-abnt/              (existente — vira "compilador-livro", mantém nome p/ compat)
│   ├── compilador-tcc/               (NOVO — template_tcc.typ, folha de aprovação, resumo/abstract)
│   ├── compilador-artigo/            (NOVO — template_artigo.typ, formato compacto)
│   └── compilador-ebook/             (NOVO — pipeline EPUB via Pandoc)
├── agents/
│   ├── subagente-pesquisador/        (existente, reaproveitado por todos)
│   ├── subagente-redator-capitulo/   (existente — livro)
│   ├── subagente-redator-secao-tcc/  (NOVO)
│   ├── subagente-redator-artigo/     (NOVO — 1 por artigo, usa RAG do dossiê-mãe)
│   ├── subagente-adaptador-ebook/    (NOVO — 1 por ebook, reescreve tom)
│   └── subagente-revisor-tecnico/    (existente, reaproveitado)
└── commands/
    ├── esbocar.md                    (NOVO — Fase 0)
    ├── criar-livro.md                (existente, ganha parâmetros)
    ├── criar-tcc.md                  (NOVO)
    ├── criar-artigo.md               (NOVO)
    ├── criar-ebook.md                (NOVO)
    └── produzir-obra-completa.md     (NOVO — fluxo full)
```

### 4.2 Decisão de design: 1 CLAUDE.md ou 1 por tipo?

O pedido original menciona "**AGENTS.md e CLAUDE.md**" próprios por tipo de material.
**Tecnicamente isso não é como o Claude Code resolve instruções** — ele lê o `CLAUDE.md` da
raiz do projeto (mais qualquer `CLAUDE.md` em subpastas do diretório de trabalho atual), não
"um CLAUDE.md por categoria de tarefa" dentro da mesma árvore. Multiplicar `CLAUDE.md`
concorrentes na raiz quebraria a arquitetura de hardlink multi-IDE já existente (que depende
de **um único arquivo físico** compartilhado por 6 ferramentas).

**Proposta (divergência assumida, ver seção 9):** manter **1 único `CLAUDE.md`** (fonte da
verdade, como hoje) com uma nova seção "Módulos por Tipo de Obra" que aponta para 4 arquivos
`SPEC_LIVRO.md`, `SPEC_TCC.md`, `SPEC_ARTIGO.md`, `SPEC_EBOOK.md` — cada um com o detalhe
completo de regras, requisitos contratuais e comando de entrada daquele tipo. Isso preserva
a portabilidade multi-IDE e ainda dá a cada tipo sua "casa" documental própria, que é o
espírito do pedido original.

---

## 5. Motor Determinístico — Extensões Necessárias

| Script | Mudança necessária |
|---|---|
| `scripts/auditar-obra.py` | Aceitar `--tipo livro\|tcc\|artigo` e `--min-refs N` (hoje `MIN_CAPITULOS`/`MIN_REFS_CAPITULO` são constantes fixas); regras de seção variam por tipo (EITA-V2 só para livro) |
| `scripts/metadados_livro.py` | Branch por tipo: TCC não gera capa comercial nem ficha CIP (usa folha de aprovação); ebook usa proporção 1:1,6 e dispensa CIP |
| `scripts/pool-capitulos.py` | Já é agnóstico ao tipo de conteúdo (só depende de `sumario_macro.json`) — reaproveitável sem mudança para TCC, e generalizável para "unidade de trabalho" (artigo, ebook) |
| `scripts/indexar-dossie.py` | Sem mudança — já serve tanto o livro-mãe quanto os artigos/ebooks derivados |
| `scripts/validar-abnt-tcc.py` (NOVO) | Verifica folha de aprovação, resumo+abstract, numeração progressiva `\d+(\.\d+)*`, lista de ilustrações se houver figura |
| `scripts/gerar-epub.py` (NOVO) | `pandoc <capitulos-do-recorte> -o ebook_<n>.epub --toc --epub-cover-image=capa.png` |
| `scripts/fatiar-obra.py` (NOVO) | Recorta `sumario_macro.json` do livro-mãe em N sub-sumários (1 por artigo ou ebook), preservando referência às fontes originais do dossiê |
| `templates/template_tcc.typ` (NOVO) | Folha de aprovação, resumo/abstract, numeração progressiva, sem capa gráfica comercial |
| `templates/template_artigo.typ` (NOVO) | Layout compacto de artigo (título, autor, resumo/abstract em 2 colunas ou 1, conforme preferência) |

---

## 6. Orquestração: Fluxo Individual vs. Fluxo Full

### 6.1 Comandos individuais (podem ser acionados sozinhos)

```
/esbocar <tema>                    → Fase 0 (sempre primeiro, gera config_obra.json)
/criar-livro <slug>                → Fases 1-3 do livro (V3 já implementado, parametrizado)
/criar-tcc <slug>                  → Fases 1-3 do TCC
/criar-artigo <slug> [--n N]       → gera N artigos a partir do dossiê já indexado
/criar-ebook <slug> [--n N]        → gera N ebooks a partir dos capítulos já compilados
```

Cada comando individual assume que `/esbocar` já rodou; se não, roda uma versão mínima
inline da Fase 0 restrita ao que aquele comando precisa (ex.: `/criar-artigo` sozinho só
pergunta quantos artigos, não pergunta tamanho de livro).

### 6.2 Fluxo Full — `/produzir-obra-completa <tema>`

```
[Fase 0 — /esbocar]
        │
        ▼
[Fase 1 — Pesquisa + Arquitetura do livro-mãe]  (sempre roda: artigos/ebooks dependem dele)
        │
        ▼
[Fase 2 — Manufatura do livro-mãe em lotes]  (se tipo_obra = livro; ou TCC em lotes de seção)
        │
        ▼
[Fase 2.5 — Peer Review]
        │
        ▼
[Fase 3 — Compilação do livro-mãe/TCC → PDF]
        │
        ├──────────────┬──────────────┐
        ▼              ▼              ▼
  [N Artigos]     [N E-books]    (paralelo, se solicitados)
  subagente-      subagente-
  redator-artigo  adaptador-ebook
        │              │
        ▼              ▼
  compilador-      compilador-
  artigo → PDF     ebook → EPUB
        │              │
        └──────┬───────┘
               ▼
      [Relatório Final Consolidado]
      1 livro.pdf + N artigos.pdf + N ebooks.epub
```

### 6.3 Encadeado vs. assíncrono — trade-off de tokens

O pedido menciona "encadeados (ou assíncronos, o que gastar menos tokens)". A resposta não
é uma escolha binária — é uma composição:

- **Artigos e e-books NÃO pesquisam do zero.** Reaproveitam o dossiê e o sumário macro
  já produzidos para o livro-mãe (artigos = aprofundamento de 1–2 capítulos via RAG;
  ebooks = reempacotamento de tom de capítulos já escritos). Isso já é a maior economia
  possível — pesquisa web repetida seria o custo dominante.
- **A geração de N artigos/N ebooks é paralela entre si** (via `pool-capitulos.py`
  generalizado para "unidade de trabalho", em lotes de 4, como já acontece com capítulos),
  não sequencial — mas cada subagente individual consulta o RAG por bloco relevante em vez
  de recarregar o dossiê inteiro, então o paralelismo não multiplica o custo de contexto.
- **Recomendação:** paralelo controlado (lotes de 4) + RAG obrigatório para artigos/ebooks.
  Isso já está descrito no upgrade 4 e 6 do V3 e é diretamente reaproveitável.

---

## 7. Novos Requisitos Contratuais

### 7.1 TCC (R-TCC-1 a R-TCC-9)

| # | Requisito | Critério |
|---|---|---|
| R-TCC-1 | Estrutura NBR 14724 completa | Folha de rosto, folha de aprovação, resumo, abstract, sumário presentes |
| R-TCC-2 | Resumo em PT + palavras-chave | 150–500 palavras, NBR 6028 |
| R-TCC-3 | Abstract + keywords | Tradução fiel do resumo |
| R-TCC-4 | Numeração progressiva | Seções no formato `\d+(\.\d+)*` (NBR 6024) |
| R-TCC-5 | Citação autor-data | `(SOBRENOME, ano)` — nenhuma citação `[N]` numérica |
| R-TCC-6 | Referências mínimas | Parametrizável (config_obra.json), NBR 6023 |
| R-TCC-7 | Tom acadêmico impessoal | Sem 2ª pessoa, sem linguagem comercial-transformacional |
| R-TCC-8 | Sem truncamento/pendência | Igual ao livro (R13) |
| R-TCC-9 | PDF final via Pandoc→Typst | Igual ao livro (R7) |

### 7.2 Artigo Científico (R-ART-1 a R-ART-7)

| # | Requisito | Critério |
|---|---|---|
| R-ART-1 | Estrutura IMRaD | Resumo/Abstract, Introdução, Metodologia, Resultados, Conclusão, Referências |
| R-ART-2 | Extensão compacta | 10–20 páginas |
| R-ART-3 | Citação autor-data | NBR 10520 |
| R-ART-4 | Referências mínimas | Parametrizável |
| R-ART-5 | Reaproveitamento do dossiê-mãe | Nenhuma pesquisa nova fora do RAG do livro-mãe |
| R-ART-6 | Palavras-chave PT+EN | NBR 6028 |
| R-ART-7 | PDF final | Pandoc→Typst |

### 7.3 E-book (R-EBK-1 a R-EBK-6)

| # | Requisito | Critério |
|---|---|---|
| R-EBK-1 | Formato EPUB reflowable | Gerado via Pandoc |
| R-EBK-2 | Capa 1:1,6 | Proporção verificável |
| R-EBK-3 | Sumário clicável | TOC nativo do EPUB |
| R-EBK-4 | CTA final | Página de encerramento presente |
| R-EBK-5 | Reaproveitamento do livro-mãe | Conteúdo adaptado, não pesquisado de novo |
| R-EBK-6 | Sem exigência ABNT | Não valida citação numérica nem ficha CIP |

---

## 8. Roadmap de Implementação (fases do trabalho de codificação)

| Fase | Entregável | Depende de |
|---|---|---|
| **A** | `/esbocar`, `config_obra.json`, parametrização de `arquiteto` e `auditar-obra.py` (tamanho + min_refs) | — |
| **B** | TCC completo: `SPEC_TCC.md`, `redator-academico`, `subagente-redator-secao-tcc`, `compilador-tcc`, `template_tcc.typ`, `validar-abnt-tcc.py`, `/criar-tcc` | Fase A |
| **C** | Artigo Científico: `SPEC_ARTIGO.md`, `subagente-redator-artigo`, `compilador-artigo`, `template_artigo.typ`, `fatiar-obra.py`, `/criar-artigo` | Fase A (RAG do livro-mãe) |
| **D** | E-book: `SPEC_EBOOK.md`, `redator-ebook`, `subagente-adaptador-ebook`, `gerar-epub.py`, `/criar-ebook` | Fase A + livro-mãe compilado |
| **E** | Orquestração full: `/produzir-obra-completa`, generalização do `pool-capitulos.py` para "unidade de trabalho", relatório consolidado multi-artefato | Fases B, C, D |

---

## 9. Decisões Assumidas (flagadas para confirmação antes da Fase A)

1. **Tamanho G do livro** (5 Partes, 10 Capítulos, 150 páginas) tem menos capítulos que M
   proporcionalmente às partes — assumido como capítulos mais densos e profundos (2 por
   parte), não um erro de digitação. **Confirmar.**
2. **Citação em TCC/Artigo = autor-data**, diferente do `[N]` numérico do livro/ebook. Essa
   é a convenção real mais usada em TCCs brasileiros sob NBR 10520 (que permite ambas), e
   reforça a diferença de tom acadêmico vs. comercial. **Confirmar ou manter `[N]` em tudo
   por simplicidade de manutenção do sistema de citação já existente.**
3. **1 único `CLAUDE.md`** (não um por tipo) — ver justificativa técnica na seção 4.2. Cada
   tipo ganha seu `SPEC_<TIPO>.md` em vez de um `CLAUDE.md` próprio. **Confirmar que essa
   adaptação atende à intenção original do pedido.**
4. **Artigos e ebooks nunca pesquisam do zero** — sempre derivam do dossiê/sumário do
   livro-mãe. Isso implica que `/criar-artigo` e `/criar-ebook` **exigem** que a Fase 1 do
   livro-mãe já tenha rodado (mesmo que o operador não queira o livro completo, ainda
   precisa do dossiê + sumário macro como matéria-prima). **Confirmar que está OK gerar
   sempre um "esqueleto" de livro-mãe mesmo quando o operador só quer artigos/ebooks.**

---

## 10. Próximos Passos

Após validação das decisões da seção 9, a implementação segue o Roadmap (seção 8),
Fase A primeiro — é a base da qual todas as outras dependem (config_obra.json e
parametrização do motor determinístico existente).
