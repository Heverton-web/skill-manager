---
description: Produz um TCC/monografia completo conforme NBR 14724, a partir de um tema ou de um esboço já gerado por /esbocar. Requisitos NÃO NEGOCIÁVEIS — ver SPEC_TCC.md.
---

Você é o Orquestrador Mestre. O operador disparou `/criar-tcc` com `$ARGUMENTS`
(um slug de obra já esboçada, ou um tema novo).

## Passo 0 — Preparação
1. Se `$ARGUMENTS` for um slug existente com `output/<slug>/esboco/config_obra.json`
   e `tipo_obra=tcc`, use-o diretamente.
2. Caso contrário (tema novo, sem esboço prévio), rode uma Fase 0 mínima: pergunte
   apenas o mínimo de referências por capítulo (5-20) via `AskUserQuestion` — o tipo
   já é TCC por definição deste comando — e grave `config_obra.json` com
   `tipo_obra="tcc"`, `tamanho_obra=null`.
3. Registre início no MCP `db_state`.

## Passo 1 — Fase 1 (P&D e Arquitetura)
4. Invoque `subagente-pesquisador` com o tema. Dossiê em `output/<slug>/pesquisa/`.
5. Indexe: `python scripts/indexar-dossie.py <slug> --indexar`.
6. Invoque `arquiteto` com `tipo_obra=tcc` — gera `sumario_macro.json` no schema TCC
   (1 parte, seções: Introdução → N×Referencial Teórico/Desenvolvimento →
   Considerações Finais).

## Passo 2 — Fase 2 (Manufatura em Lotes)
7. Planeje o despacho: `python scripts/pool-capitulos.py <slug> --plano --lote 4`.
8. Para cada lote, instancie `subagente-redator-secao-tcc` em paralelo
   (estrategista com pilares ACAD → redator-academico → auto-validação).
9. Drene pendências com backoff: `python scripts/pool-capitulos.py <slug> --pendentes --lote 4`.

## Passo 3 — Fase 2.5 (Peer Review)
10. Audite: `python scripts/auditar-obra.py <slug> --tipo tcc`.
11. Invoque `revisor-tecnico` (adaptado: sem verificação de tom transformacional,
    sem exigência de diagrama Mermaid) para corrigir os requisitos `TCC-*`
    reprovados. Reaudite com `--estrito`, máximo 3 rodadas.

## Passo 4 — Fase 3 (Compilação ABNT + PDF)
12. Invoque `compilador-tcc`: merge das seções, geração de resumo/abstract
    (NBR 6028), consolidação de referências (NBR 6023), grava
    `output/<slug>/tcc_metadados.json` (resumo, palavras_chave, abstract_en,
    keywords_en, instituicao, curso, orientador, local, ano) e
    `output/<slug>/livro_final.md`.
13. Compile o PDF (usa `templates/template_tcc.typ` automaticamente por causa de
    `tipo_obra=tcc` em `config_obra.json`):
    ```bash
    python compilar-para-pdf.py <slug> --sem-capa
    ```
14. Valide os elementos pré-textuais:
    ```bash
    python scripts/validar-abnt-tcc.py <slug> --estrito
    ```

## Passo 5 — Relatório de Entrega
15. Exiba (REGRA 2, telegráfico): caminho do PDF, total de seções, veredito da
    auditoria (`--tipo tcc`) e da validação ABNT (`validar-abnt-tcc.py`).
