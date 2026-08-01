---
description: Gera N Artigos Científicos (NBR 6022/12820) a partir do dossiê e sumário já produzidos para um livro-mãe. Requer que a Fase 1 (pesquisa + arquitetura) do livro-mãe já tenha rodado — artigos nunca pesquisam do zero. Ver SPEC_ARTIGO.md.
---

Você é o Orquestrador Mestre. O operador disparou `/criar-artigo` com `$ARGUMENTS`
(slug do livro-mãe, opcionalmente seguido de `--n N` para sobrescrever a
quantidade de artigos).

## Pré-condição
1. Verifique `output/<slug>/pesquisa/indice_dossie.json` e
   `output/<slug>/sumario_macro.json`. Se algum estiver ausente, rode primeiro a
   Fase 1 do livro-mãe (`subagente-pesquisador` → `indexar-dossie.py --indexar` →
   `arquiteto`) antes de prosseguir — artigos **nunca** pesquisam do zero
   (economia de tokens e tempo).

## Passo 1 — Fatiamento
2. Determine `qtd_artigos`: de `--n`, ou de `output/<slug>/esboco/config_obra.json`,
   ou 3 por padrão.
3. Execute:
   ```bash
   python scripts/fatiar-obra.py <slug> --artigos --qtd <qtd_artigos>
   ```
   Isso cria `output/<slug>/artigos/artigo_<n>/` (1..qtd) com `sumario_macro.json`
   IMRaD e `config_obra.json` próprios.

## Passo 2 — Manufatura em Paralelo (lotes de 4)
4. Para cada `artigo_<n>`, instancie `subagente-redator-artigo` — todos os artigos
   do lote em paralelo, cada um consultando o dossiê do livro-mãe via RAG (nunca
   pesquisa nova). Use o pool de concorrência com o caminho aninhado como
   identificador de unidade:
   ```bash
   python scripts/pool-capitulos.py <slug>/artigos/artigo_<n> --plano --lote 4
   ```

## Passo 3 — Auditoria por Artigo
5. Para cada artigo:
   ```bash
   python scripts/auditar-obra.py <slug>/artigos/artigo_<n> --tipo artigo --estrito
   ```
   Corrija reprovações via `revisor-tecnico` antes de compilar.

## Passo 4 — Compilação
6. Invoque `compilador-artigo` para cada artigo (merge + resumo/abstract + refs):
   ```bash
   python compilar-para-pdf.py <slug>/artigos/artigo_<n> --tipo artigo --sem-capa --sem-diagramas
   ```

## Passo 5 — Relatório de Entrega
7. Exiba (REGRA 2): quantidade de artigos gerados, título e caminho do PDF de
   cada um, veredito da auditoria por artigo. Atualize
   `output/<slug>/artigos/estrutura_artigos.json` com os caminhos finais.
