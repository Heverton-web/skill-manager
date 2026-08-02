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

## 2. Layout de Diretórios (V4.1)

Artigos vivem no TOPO de `output/` (`output/artigos/`), não aninhados dentro da
pasta do livro-mãe — isso permite listar todos os artigos de qualquer livro em
um só lugar. A referência cruzada para o livro-mãe é o campo `slug_livro_mae`
dentro do `sumario_macro.json` de cada artigo, e o manifesto oficial de todos os
derivados de um livro fica em `output/livros/<slug-livro-mae>/derivados.json`.

```
output/livros/<slug-livro-mae>/
├── pesquisa/indice_dossie.json      ← reaproveitado (RAG), nao duplicado
├── sumario_macro.json               ← livro-mae, usado so para fatiar
└── derivados.json                   ← manifesto: artigos.itens[] (titulo, slug,
                                        diretorio, capitulos-fonte, status) + ebooks.itens[]

output/artigos/
├── <slug-livro-mae>--art-01-<slug-titulo>/
│   ├── sumario_macro.json       ← schema IMRaD (1 parte, 4 secoes) + slug_livro_mae
│   ├── config_obra.json         ← tipo_obra=artigo, min_referencias_por_capitulo
│   ├── artigo_metadados.json    ← resumo, palavras_chave, abstract_en, keywords_en
│   ├── capitulos/cap_1..4.md    ← Introducao/Metodologia/Resultados/Conclusao
│   ├── livro_final.md
│   └── livro_final.pdf
└── <slug-livro-mae>--art-02-<slug-titulo>/ ...
```

O identificador de "slug" usado em todos os scripts (`auditar-obra.py`,
`compilar-para-pdf.py`, `pool-capitulos.py`) para um artigo é o caminho completo
`artigos/<slug-livro-mae>--art-<NN>-<slug-titulo>` — todos os scripts resolvem
caminhos por `output/<slug>/...`, e `Path` trata caminhos com `/` normalmente. O
prefixo `<slug-livro-mae>--` evita colisão de nomes entre artigos de livros
diferentes e mantém os artigos do mesmo livro agrupados alfabeticamente ao
listar `output/artigos/`.

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
