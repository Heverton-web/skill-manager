---
description: Gera N E-books (EPUB, padrão de mercado, sem ABNT) a partir dos capítulos já escritos e compilados de um livro-mãe. Requer que a Fase 2 (manufatura dos capítulos) do livro-mãe já tenha rodado — ebooks reescrevem tom, não pesquisam nem escrevem conteúdo novo. Ver SPEC_EBOOK.md.
---

Você é o Orquestrador Mestre. O operador disparou `/criar-ebook` com `$ARGUMENTS`
(slug do livro-mãe, opcionalmente seguido de `--n N` para sobrescrever a
quantidade de ebooks).

## Pré-condição
1. Verifique que `output/<slug>/capitulos/cap_*.md` existem (a Fase 2 do
   livro-mãe já produziu os capítulos-fonte). Se não existirem, avise que
   `/criar-livro <slug>` precisa rodar primeiro — ebooks **nunca** geram conteúdo
   novo, apenas readaptam.

## Passo 1 — Fatiamento
2. Determine `qtd_ebooks`: de `--n`, ou de `output/<slug>/esboco/config_obra.json`,
   ou 3 por padrão.
3. Execute:
   ```bash
   python scripts/fatiar-obra.py <slug> --ebooks --qtd <qtd_ebooks>
   ```
   Isso cria `output/<slug>/ebooks/ebook_<n>/` (1..qtd_ebooks), cada um apontando
   para um subconjunto de `capitulos_fonte_livro_mae` (por Parte, se
   `qtd_ebooks` == nº de Partes; senão por agrupamento linear de capítulos).

## Passo 2 — Adaptação em Paralelo (lotes de 4)
4. Para cada `ebook_<n>`, instancie `subagente-adaptador-ebook` — todos os ebooks
   do lote em paralelo (redator-ebook adapta tom → capa+thumbnail → auditoria
   EBOOK-LEN → EPUB), sem qualquer subagente de pesquisa.
   **REGRA:** Todo ebook DEVE começar com o capítulo fixo EITA (`templates/capitulo_eita.md`)
   explicando as 7 seções do framework. O subagente deve incluí-lo ao adaptar o conteúdo.

## Passo 3 — Auditoria e Geração
5. Cada subagente gera capa no padrão Editora Agêntica (`scripts/gerar-capa-ebook-padrao.py`),
   audita (`--tipo ebook`, inclui piso EBOOK-LEN de ~45.000 caracteres) e gera EPUB + PDF
   (`scripts/gerar-epub.py --pdf-tambem`) como parte do seu próprio procedimento — o
   Orquestrador só confere que todos os `ebook_<n>/` têm `.epub`, `.pdf` e `capa.png`
   gerados ao final do lote.

## Passo 4 — Relatório de Entrega
6. Exiba (REGRA 2): quantidade de ebooks gerados, título, caracteres e caminho
   do `.epub`/`.pdf`/`capa.png` de cada um, e o veredito EBOOK-LEN.
   Atualize `output/<slug>/ebooks/estrutura_ebooks.json` com os caminhos finais.
