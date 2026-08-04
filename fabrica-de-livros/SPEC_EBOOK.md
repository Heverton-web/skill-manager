# SPEC_EBOOK — Produção Autônoma de E-books (padrão de mercado, sem ABNT)

Especifica o processo disparado por `/criar-ebook <slug-do-livro-mae>`. Diferente
de todos os outros tipos de obra da fábrica, o e-book **não segue norma ABNT** —
segue padrões de mercado (Amazon KDP, Hotmart, Kiwify) e **não gera conteúdo
novo**: reescreve o tom de capítulos já compilados do livro-mãe.

## 1. Requisitos Contratuais

| # | Requisito | Critério | Verificação |
|---|---|---|---|
| R-EBK-1 | Formato EPUB reflowable | Gerado via Pandoc | `gerar-epub.py` |
| R-EBK-2 | Capa padrão Editora Agêntica | `imagens/capa.png` (1200×1600px, flat 2D, terminal + código) | `gerar-capa-ebook-padrao.py` |
| R-EBK-3 | Sumário clicável | TOC nativo do EPUB (`--toc`) | `gerar-epub.py` |
| R-EBK-4 | CTA final | Seção "Próximos Passos" presente | `redator-ebook` (procedimento) |
| R-EBK-5 | Reaproveitamento do livro-mãe | Conteúdo adaptado, não pesquisado de novo | `subagente-adaptador-ebook` (nunca chama `subagente-pesquisador`) |
| R-EBK-6 | Sem exigência ABNT | Sem citação numérica/autor-data obrigatória, sem ficha CIP | `auditar-obra.py --tipo ebook` (não verifica R-REF/R-CIT/R-NUM) |

## 2. Diferenças vs. Livro/TCC/Artigo

| | Livro/TCC/Artigo | E-book |
|---|---|---|
| Conteúdo | Gerado do zero (pesquisa + redação) | Reescrito a partir de capítulos já prontos |
| Norma | ABNT (NBR 6029/14724/6022) | Nenhuma — padrão de mercado |
| Formato final | PDF (Pandoc→Typst) | **EPUB** (Pandoc nativo) |
| Citação | `[N]` ou autor-data, obrigatória | Nenhuma exigida |
| Estrutura | Fixa (EITA-V2/ACAD/IMRaD) | Livre, parágrafos curtos, CTA final |

## 3. Layout de Diretórios (V4.1)

E-books vivem no TOPO de `output/` (`output/ebooks/`), não aninhados dentro da
pasta do livro-mãe — a referência cruzada é o campo `slug_livro_mae` dentro do
`sumario_macro.json` de cada ebook, e o manifesto oficial fica em
`output/livros/<slug-livro-mae>/derivados.json` (seção `ebooks`).

```
output/livros/<slug-livro-mae>/
├── capitulos/cap_1..N.md            ← fonte (livro-mae ja compilado)
└── derivados.json                   ← manifesto: ebooks.itens[] (titulo, slug,
                                        diretorio, capitulos-fonte, status, caminho .epub)

output/ebooks/
├── <slug-livro-mae>--eb-01-<slug-titulo>/
│   ├── sumario_macro.json       ← capitulos_fonte_livro_mae + slug_livro_mae
│   ├── ebook_metadados.json     ← titulo, autor
│   ├── capitulos/cap_1..M.md    ← versao adaptada (tom leve) + CTA
│   ├── imagens/capa.png         ← opcional (1:1,6)
│   ├── livro_final.md
│   └── <slug-livro-mae>--eb-01-<slug-titulo>.epub
└── <slug-livro-mae>--eb-02-<slug-titulo>/ ...
```

O prefixo `<slug-livro-mae>--` no nome da pasta evita colisão entre ebooks de
livros diferentes e mantém os ebooks do mesmo livro agrupados alfabeticamente
ao listar `output/ebooks/`. `gerar-epub.py` nomeia o `.epub` a partir do nome da
própria pasta — sem passo manual de renomeação.

## 4. Fatiamento (scripts/fatiar-obra.py --ebooks)

- Se `qtd_ebooks` for igual ao número de Partes do livro-mãe: 1 ebook por Parte.
- Caso contrário: fatiamento linear dos capítulos em `qtd_ebooks` grupos
  contíguos (mesmo algoritmo dos artigos).

## 5. Fluxo de Execução

```
[Pre-condicao: livro-mae com capitulos ja compilados]
        │
        ▼
[fatiar-obra.py --ebooks --qtd N]
        │
        ▼
[subagente-adaptador-ebook em lotes de 4]
   (redator-ebook: tom leve + CTA → merge → auditoria minima)
        │
        ▼
[gerar-epub.py — EPUB reflowable, capa opcional]
        │
        ▼
[Relatório consolidado: N EPUBs]
```

## 6. Casos de borda

| Situação | Comportamento |
|---|---|
| Livro-mãe sem capítulos compilados | Comando aborta, orienta rodar `/criar-livro` primeiro |
| Capa ausente | EPUB gerado sem imagem de capa; pendência reportada (não bloqueia) |
| Capítulo-fonte com citação `[N]` | `redator-ebook` remove ou converte em atribuição narrativa leve |
| `qtd_ebooks` igual ao nº de Partes | 1 ebook por Parte (mapeamento natural) |
