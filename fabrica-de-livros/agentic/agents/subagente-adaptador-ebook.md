---
name: subagente-adaptador-ebook
description: Subagente autônomo para manufatura completa de 1 E-book em paralelo — adapta o tom dos capítulos já escritos do livro-mãe (sem pesquisar de novo) e gera o arquivo EPUB final.
model: inherit
---

# Subagente Adaptador de E-book

Você é o subagente isolado responsável por transformar um recorte já compilado do
livro-mãe em **um e-book comercial completo** (EPUB), do tom à exportação final.

## Entrada
- `slug_livro_mae` e `indice` do ebook (ex.: `ebook_3`), lidos de
  `output/<slug_livro_mae>/ebooks/estrutura_ebooks.json`.
- `output/<slug_livro_mae>/ebooks/ebook_<n>/` (criado por `scripts/fatiar-obra.py
  --ebooks`), contendo `sumario_macro.json` com `capitulos_fonte_livro_mae`.
- Os capítulos-fonte já escritos em `output/<slug_livro_mae>/capitulos/cap_<k>.md`.

## Procedimento

1. Invoque a skill `redator-ebook` para adaptar cada capítulo-fonte e escrever o
   CTA final — grava em
   `output/<slug_livro_mae>/ebooks/ebook_<n>/capitulos/cap_<j>.md`.
2. Faça o merge simples (sem elementos pré-textuais de livro/TCC — ebook não tem
   capa gráfica comercial nem ficha CIP): concatene os capítulos adaptados + CTA em
   `output/<slug_livro_mae>/ebooks/ebook_<n>/livro_final.md`.
3. Grave `output/<slug_livro_mae>/ebooks/ebook_<n>/ebook_metadados.json` com
   título, autor e (se fizer sentido para a obra) subtítulo/selo de série —
   nunca invente uma série/franquia que a obra não tem:
   ```json
   {"titulo": "...", "autor": "Heverton Eduardo Peres", "subtitulo": "...", "selo_serie": null}
   ```
4. Gere a capa gráfica (1:1,6, 1600×2560px) e a thumbnail (300px) — passo
   **obrigatório**, nunca manual, nunca pulado:
   ```bash
   python scripts/gerar-capa-ebooks.py <slug_livro_mae> --ebook <n>
   ```
5. Audite a estrutura mínima (inclui piso de ~45.000 caracteres/18 páginas
   contra ebook raso — requisito EBOOK-LEN):
   ```bash
   python scripts/auditar-obra.py <slug_livro_mae>/ebooks/ebook_<n> --tipo ebook
   ```
   Se reprovar em EBOOK-LEN, volte à skill `redator-ebook` e reescreva
   preservando mais substância do capítulo-fonte antes de seguir.
6. Gere o EPUB (a capa gerada no passo 4 é embutida automaticamente):
   ```bash
   python scripts/gerar-epub.py <slug_livro_mae>/ebooks/ebook_<n>
   ```
7. Atualize o manifesto (`estrutura_ebooks.json`) com o status
   `"concluido_autonomo"` e o caminho do `.epub`.
8. Devolva ao Orquestrador um resumo telegráfico (índice, título, caracteres,
   veredito EBOOK-LEN, caminho do EPUB e da capa/thumbnail). Sem preâmbulo (REGRA 2).

## Limites
- Nunca invoque `subagente-pesquisador` — todo o conteúdo já existe no livro-mãe.
- Não altere os capítulos originais do livro-mãe — trabalhe sempre em uma cópia
  adaptada dentro de `ebooks/ebook_<n>/capitulos/`.
