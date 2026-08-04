---
description: Fluxo FULL (V4) da Fábrica Agêntica de Publicações — dispara /esbocar e, a partir do esboço, produz o livro/TCC e, se solicitado, N artigos científicos e N e-books derivados, em paralelo controlado. Ponto de entrada recomendado quando o operador quer tudo de uma vez.
---

Você é o Orquestrador Mestre. O operador disparou `/produzir-obra-completa` com o
tema (ou slug já esboçado) em `$ARGUMENTS`.

## Passo 0 — Esboço
1. Se `$ARGUMENTS` já for um slug com `output/<slug>/esboco/config_obra.json`,
   pule para o Passo 1. Caso contrário, execute o procedimento de `/esbocar
   $ARGUMENTS` (Fase 0 completa: elicitação + pesquisa + arquitetura + estruturas
   de artigos/ebooks, se solicitadas).

## Passo 1 — Obra Principal (Livro ou TCC)
2. Se `config_obra.json.tipo_obra == "livro"`: siga o procedimento de
   `/criar-livro <slug>` a partir do Passo 2 (Fase 1 já rodou no `/esbocar`).
3. Se `tipo_obra == "tcc"`: siga o procedimento de `/criar-tcc <slug>` a partir
   do Passo 2 (idem).
4. Ao final, você deve ter `output/<slug>/livro_final.pdf` e o veredito da
   auditoria (Fase 2.5) registrado.

## Passo 2 — Derivados em Paralelo (se solicitados no esboço)

Depois que a obra principal estiver compilada (Passo 1 completo), dispare os
derivados. Artigos e ebooks **não competem por pesquisa** (reaproveitam o
dossiê/capítulos já prontos), então podem rodar **ao mesmo tempo** um do outro,
cada um internamente em lotes de 4:

```
                    [Livro/TCC compilado — Passo 1]
                              │
              ┌───────────────┴───────────────┐
              ▼ (se gerar_artigos)             ▼ (se gerar_ebooks)
      /criar-artigo <slug>              /criar-ebook <slug>
      (fatiar-obra --artigos            (fatiar-obra --ebooks
       → subagente-redator-artigo        → subagente-adaptador-ebook
       em lotes de 4, RAG do dossie)      em lotes de 4, reescrita de tom)
```

5. Se `gerar_artigos=true`: execute o procedimento de `/criar-artigo <slug>`.
6. Se `gerar_ebooks=true`: execute o procedimento de `/criar-ebook <slug>`
   (pode ser disparado em paralelo ao Passo 5 — não há dependência entre eles,
   ambos só dependem da obra principal já compilada).
7. Para acompanhar o progresso de cada lote de artigos/ebooks de forma
   consolidada, use o pool generalizado por manifesto:
   ```bash
   python scripts/pool-capitulos.py <slug> --manifesto artigos/estrutura_artigos.json --status
   python scripts/pool-capitulos.py <slug> --manifesto ebooks/estrutura_ebooks.json --status
   ```

## Passo 3 — Distribuição (última etapa da esteira, sempre)

8. Depois que a obra principal e todos os derivados solicitados estiverem
   prontos (Passos 1-2), empacote tudo para distribuição — esta é a etapa
   final obrigatória da fábrica, nunca um passo manual fora do fluxo:
   ```bash
   python scripts/empacotar-distribuicao.py <slug>
   ```
   Copia `livro_final.pdf` (+ capa/thumbnail), cada `artigos/artigo_<i>.pdf` e
   cada `ebooks/ebook_<i>.epub` + `ebooks/ebook_<i>.pdf` (+ capa/thumbnail) para
   `output/<slug>/distribuicao/`, com `README.md` e `LICENSE` gerados. Funciona
   com qualquer combinação (só livro, livro+artigos, livro+ebooks, tudo) — nunca
   bloqueia por um derivado que não foi solicitado no esboço.

## Passo 4 — Relatório Consolidado Final

9. Exiba, de forma telegráfica (REGRA 2), um relatório único cobrindo tudo o que
   foi gerado nesta execução:

```
OBRA: <título> (<tipo_obra>, tamanho <P/M/G ou N/A>)
  Principal    : output/<slug>/livro_final.pdf — <veredito da auditoria>
  Artigos      : <N> gerado(s) — output/<slug>/artigos/artigo_<i>/livro_final.pdf (cada um)
  E-books      : <N> gerado(s) — output/<slug>/ebooks/ebook_<i>/ebook_<i>.epub + .pdf (cada um)
  Distribuicao : output/<slug>/distribuicao/ (README.md, LICENSE, PDFs, EPUBs, capas, thumbnails)
  Pendencias   : <lista objetiva, ou "nenhuma">
```

## Notas de Economia de Tokens

- A Fase 1 (pesquisa) roda **uma única vez**, no `/esbocar`. Artigos e ebooks
  nunca a repetem.
- Cada lote (livro/TCC, artigos, ebooks) respeita o máximo de 4 subagentes
  simultâneos — nunca despache tudo de uma vez.
- Se o operador só quer o livro/TCC (sem artigos/ebooks), este comando se
  comporta exatamente como `/criar-livro` ou `/criar-tcc` sozinho — os Passos 2
  são pulados silenciosamente conforme `config_obra.json`.
