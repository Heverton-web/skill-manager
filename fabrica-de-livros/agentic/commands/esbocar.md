---
description: Fase 0 (V4) da Fábrica Agêntica de Publicações — elicitação interativa que decide tipo de obra (Livro/TCC), tamanho, mínimo de referências e se gera artigos/ebooks derivados. Único ponto de interação humana; depois disso a esteira roda 100% autônoma (REGRA 3).
---

Você é o Orquestrador Mestre. O operador disparou `/esbocar` com o tema em `$ARGUMENTS`.
Esta é a **Fase 0** — a única rodada de perguntas de toda a esteira.

## Passo 0 — Preparação
1. Slug em kebab-case a partir do tema. Se `output/livros/<slug>/` ou
   `output/tccs/<slug>/` já existir com conteúdo, use sufixo `-v2`.
2. A pasta raiz da obra (`output/livros/<slug>/` ou `output/tccs/<slug>/`, conforme
   o tipo escolhido no Passo 1) só é criada no Passo 2, quando o tipo já é conhecido —
   livros, TCCs, artigos e e-books vivem em raízes separadas no topo de `output/`
   (`output/livros/`, `output/tccs/`, `output/artigos/`, `output/ebooks/`); artigos e
   e-books derivados de uma obra não ficam aninhados dentro da pasta da obra-mãe,
   apenas referenciam o slug dela via `slug_livro_mae`.

## Passo 1 — Elicitação (2 rodadas de `AskUserQuestion`)

**Rodada 1 — sempre perguntar (até 4 perguntas por chamada):**

| Header | Pergunta | Opções |
|---|---|---|
| Tipo | Qual o tipo de obra a ser escrita? | Livro (Recommended) \| TCC |
| Refs | Mínimo de referências por capítulo? | 5 \| 8 \| 12 \| 16 \| 20 |
| Artigos | Deseja gerar artigos científicos a partir do tema? | Sim \| Não (Recommended) |
| Ebooks | Deseja gerar e-books a partir da obra? | Sim \| Não (Recommended) |

**Rodada 2 — só as perguntas aplicáveis às respostas da Rodada 1:**

| Header | Pergunta | Condição | Opções |
|---|---|---|---|
| Tamanho | Qual o tamanho do livro? | Tipo = Livro | P — 1 Parte, 3-5 capítulos, ~40 páginas \| M — 3 Partes, 9 capítulos, ~90 páginas (Recommended) \| G — 5 Partes, 10 capítulos, ~150 páginas |
| Qtd. Artigos | Quantos artigos científicos? | Artigos = Sim | 1 \| 2 \| 3 \| 4 \| 5 |
| Qtd. Ebooks | Quantos e-books? | Ebooks = Sim | 1-3 \| 4-6 \| 7-10 |

Se "Qtd. Ebooks" vier como faixa, use o valor médio da faixa (2, 5 ou 8) como `qtd_ebooks`.
Se o operador selecionar "Other" em qualquer pergunta, use o valor livre fornecido,
respeitando os limites: refs 5-20, artigos 1-5, ebooks 1-10.

## Passo 2 — Gravar `config_obra.json`

Com o `tipo_obra` já respondido no Passo 1, defina `prefixo = "livros"` (tipo_obra=livro)
ou `prefixo = "tccs"` (tipo_obra=tcc) e crie `output/<prefixo>/<slug>/`.

Grave `output/<prefixo>/<slug>/config_obra.json` (raiz da obra, sem subpasta `esboco/`)
no schema:
```json
{
  "tema": "$ARGUMENTS",
  "tipo_obra": "livro | tcc",
  "min_referencias_por_capitulo": 5,
  "tamanho_obra": "P | M | G | null",
  "gerar_artigos": true,
  "qtd_artigos": 3,
  "gerar_ebooks": true,
  "qtd_ebooks": 5
}
```
Valide com:
```bash
python scripts/parametros_obra.py <prefixo>/<slug> --validar
```
Se inválido, corrija os valores fora de faixa antes de prosseguir (nunca pergunte de novo — REGRA 3).

## Passo 3 — Gerar o esboço (sem pausa)

3. Invoque `subagente-pesquisador` com o tema. Dossiê em `output/<prefixo>/<slug>/pesquisa/`.
4. Indexe o dossiê: `python scripts/indexar-dossie.py <prefixo>/<slug> --indexar`.
5. Invoque `arquiteto` passando `tipo_obra` e `tamanho_obra` de `config_obra.json` — o
   sumário macro gerado deve respeitar os mínimos de `scripts/parametros_obra.py`
   (tabela `TAMANHOS` para livro; TCC usa 1 "parte" com as seções do framework ACAD
   como "capítulos" — ver `SPEC_TCC.md`).
6. Se `gerar_artigos=true`: `python scripts/fatiar-obra.py <prefixo>/<slug> --artigos --qtd <qtd_artigos>`
   — particiona o sumário macro em `qtd_artigos` recortes temáticos (1-2 capítulos
   cada, sem sobreposição), cria cada `output/artigos/<slug>--art-NN-<titulo>/` e
   grava `output/<prefixo>/<slug>/derivados.json` (seção `artigos`).
7. Se `gerar_ebooks=true`: `python scripts/fatiar-obra.py <prefixo>/<slug> --ebooks --qtd <qtd_ebooks>`
   — mesmo princípio, cria cada `output/ebooks/<slug>--eb-NN-<titulo>/` e grava a
   seção `ebooks` do mesmo `derivados.json` (preserva a seção `artigos` já gravada).

## Passo 4 — Relatório objetivo (REGRA 2, sem metatexto)

Exiba: slug completo (`<prefixo>/<slug>`), tipo de obra, tamanho (se livro),
quantidade de capítulos planejados, quantidade de artigos/ebooks planejados (se
solicitados), e a lista de comandos disponíveis para prosseguir:

```
/produzir-obra-completa <prefixo>/<slug>     — dispara tudo encadeado/paralelo
/criar-livro <prefixo>/<slug>                — só o livro/TCC
/criar-artigo <prefixo>/<slug>               — só os artigos (requer livro-mãe com dossiê+sumário)
/criar-ebook <prefixo>/<slug>                — só os ebooks (requer livro-mãe compilado)
```

Nenhuma pergunta adicional é feita a partir daqui — a esteira é 100% autônoma
(REGRA 3) até a entrega final de qualquer um dos comandos acima.
