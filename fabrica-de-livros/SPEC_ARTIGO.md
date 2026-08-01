# SPEC_ARTIGO — Produção Autônoma de Artigos Científicos (NBR 6022/12820)

Especifica o processo disparado por `/criar-artigo <slug-do-livro-mae>`. Diferente
de `/criar-livro` e `/criar-tcc`, este comando **não pesquisa do zero**: reaproveita
o dossiê e o sumário macro já produzidos para um livro-mãe (Fase 1 já executada).

## 1. Requisitos Contratuais

| # | Requisito | Critério | Verificação |
|---|---|---|---|
| R-ART-1 | Estrutura IMRaD | Introdução, Metodologia, Resultados e Discussão, Conclusão, Referências | `arquiteto`/`fatiar-obra.py` (estrutura fixa de 4 seções) |
| R-ART-2 | Extensão compacta | 10–20 páginas | `auditar-obra.py --tipo artigo` (contagem de caracteres) |
| R-ART-3 | Citação autor-data | NBR 10520 | `auditar-obra.py --tipo artigo` |
| R-ART-4 | Referências mínimas | `min_referencias_por_capitulo` | `auditar-obra.py --tipo artigo` |
| R-ART-5 | Reaproveitamento do dossiê-mãe | Nenhuma pesquisa nova fora do RAG do livro-mãe | Auditoria manual do `subagente-redator-artigo` (nunca chama `subagente-pesquisador`) |
| R-ART-6 | Resumo/Abstract + palavras-chave (PT+EN) | NBR 6028 | Presença em `artigo_metadados.json` |
| R-ART-7 | PDF final | Pandoc → `.typ` → Typst, `template_artigo.typ` | `compilar-para-pdf.py --tipo artigo` |

## 2. Layout de Diretórios

```
output/<slug-livro-mae>/
├── pesquisa/indice_dossie.json      ← reaproveitado (RAG), nao duplicado
├── sumario_macro.json               ← livro-mae, usado so para fatiar
└── artigos/
    ├── estrutura_artigos.json       ← manifesto: titulo, capitulos-fonte, status
    ├── artigo_1/
    │   ├── sumario_macro.json       ← schema IMRaD (1 parte, 4 secoes)
    │   ├── config_obra.json         ← tipo_obra=artigo, min_referencias_por_capitulo
    │   ├── artigo_metadados.json    ← resumo, palavras_chave, abstract_en, keywords_en
    │   ├── capitulos/cap_1..4.md    ← Introducao/Metodologia/Resultados/Conclusao
    │   ├── livro_final.md
    │   └── livro_final.pdf
    └── artigo_2/ ...
```

O identificador de "slug" usado em todos os scripts (`auditar-obra.py`,
`compilar-para-pdf.py`, `pool-capitulos.py`) para um artigo é o caminho aninhado
`<slug-livro-mae>/artigos/artigo_<n>` — todos os scripts resolvem caminhos por
`output/<slug>/...`, e `Path` trata caminhos com `/` normalmente.

## 3. Fatiamento (scripts/fatiar-obra.py)

Particiona os capítulos do livro-mãe em `qtd_artigos` grupos contíguos e
aproximadamente equilibrados (ex.: 6 capítulos / 2 artigos = 3 + 3). Cada grupo
vira o "recorte temático" de 1 artigo — o `subagente-redator-artigo` usa os
títulos desses capítulos como termos de busca no RAG do livro-mãe.

## 4. Fluxo de Execução

```
[Pre-condicao: livro-mae com dossie+sumario ja gerados]
        │
        ▼
[fatiar-obra.py --artigos --qtd N]
        │
        ▼
[subagente-redator-artigo em lotes de 4]
   (RAG do livro-mae → estrategista/ACAD → redator-academico)
        │
        ▼
[auditar-obra.py --tipo artigo --estrito, por artigo]
        │
        ▼
[compilador-artigo → artigo_metadados.json + livro_final.md
                    → compilar-para-pdf.py --tipo artigo]
        │
        ▼
[Relatório consolidado: N PDFs]
```

## 5. Casos de borda

| Situação | Comportamento |
|---|---|
| Livro-mãe sem dossiê/sumário | Comando aborta e roda a Fase 1 do livro-mãe primeiro |
| `qtd_artigos` maior que o nº de capítulos do livro-mãe | `fatiar-obra.py` gera grupos de 1 capítulo cada, tolerando menos artigos que o pedido se o livro-mãe for muito curto |
| Subagente tenta pesquisar (`WebSearch`) | Proibido — reprova revisão manual (R-ART-5); corrigir removendo a chamada e usando só RAG |
