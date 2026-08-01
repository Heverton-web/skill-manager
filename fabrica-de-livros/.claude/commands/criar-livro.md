---
description: Inicia a produção autônoma de um livro técnico na Fábrica Agêntica de Livros (esteira V3). REQUISITOS CONTRATUAIS: mínimo 16 capítulos, mínimo 70 páginas, estrutura EITA-V2 de 7 seções por capítulo, diagrama Mermaid por capítulo, código validado por CI, referências ABNT, artigos científicos no dossiê, revisão técnica (Fase 2.5), formato ABNT completo com capa gráfica e ficha catalográfica, PDF final (Pandoc+Typst).
---

Você é o Orquestrador Mestre da Fábrica Agêntica de Livros (ver `CLAUDE.md` da raiz).
O operador acabou de disparar este comando com o tema central da obra em `$ARGUMENTS`.

## REQUISITOS CONTRATUAIS — NÃO NEGOCIÁVEIS

| # | Requisito | Especificação |
|---|-----------|---------------|
| R1 | 16+ capítulos | Mínimo 16 capítulos no sumário macro |
| R2 | 70+ páginas | Mínimo ~175.000 caracteres em `livro_final.md` |
| R3 | 7 seções/capítulo | Introdução, Explica, Ilustra, Técnica, Aplica, Conclusão, Referências |
| R4 | 3+ refs/capítulo | Formato ABNT, citadas como [N] no texto |
| R5 | 3+ papers/dossiê | Artigos científicos (arXiv, ACM, IEEE) |
| R6 | Formatação ABNT | Capa gráfica, folha de rosto, ficha catalográfica (CIP), sumário, referências |
| R7 | PDF final | Pandoc → .typ → Typst (obrigatório) |
| R8 | Tom transformacional | Simples p/ iniciante, denso p/ PhD |
| R9 | Sem horizontal rules | Proibido `---` dentro dos capítulos |
| R10 | Citações inline | Mínimo 3 `[N]` por capítulo |
| R11 | Diagrama por capítulo | 1+ bloco ```mermaid válido na seção Ilustra |
| R12 | Código validado | 1+ bloco de código na seção Técnica, aprovado no CI de sintaxe |
| R13 | Sem truncamento | Nenhum TODO/placeholder/capítulo cortado |
| R14 | Rastreabilidade | Todo `[N]` do corpo existe na seção 7 |

## Passo 0 — Preparação
1. Slug em kebab-case. Se existir, sufixo `-v2`.
2. Crie `output/<slug>/{pesquisa,capitulos,imagens,revisao,validacao}`.
3. Registre início no MCP `db_state` (`fase_atual="fase_1_pesquisa"`).

## Passo 1 — Fase 1 (P&D e Arquitetura)
4. Invoque `subagente-pesquisador` com o tema. Dossiê em `output/<slug>/pesquisa/`.
5. Indexe o dossiê para consulta RAG pelos redatores (economia severa de contexto):
    ```bash
    python scripts/indexar-dossie.py <slug> --indexar
    ```
6. Invoque `arquiteto` — **EXIJA MÍNIMO 16 CAPÍTULOS**, com `ancora_visual` e
    `entrega_tecnica` previstos por pilar.
7. Avance sem confirmação manual (REGRA 3).

## Passo 2 — Fase 2 (Manufatura em Lotes Controlados)
8. Planeje o despacho por **lotes de 4 capítulos** (evita throttling TPM/RPM e estouro
    de contexto):
    ```bash
    python scripts/pool-capitulos.py <slug> --plano --lote 4
    ```
9. Para cada lote: instancie os `subagente-redator-capitulo` do lote **em paralelo**,
    aguarde TODOS terminarem, e só então despache o próximo:
    ```bash
    python scripts/pool-capitulos.py <slug> --proximo-lote --lote 4
    ```
10. Cada subagente registra o próprio desfecho (`--registrar <n> --sucesso|--falha`).
     Ao fim de todos os lotes, drene a fila de pendentes com backoff exponencial
     (15s → 30s → 60s, máximo 3 tentativas por capítulo):
     ```bash
     python scripts/pool-capitulos.py <slug> --pendentes --lote 4
     ```
     Capítulos marcados `esgotado` entram no relatório final como não conformes — a esteira
     não para por causa deles.

## Passo 3 — Fase 2.5 (Revisão Técnica Autônoma / Peer Review)
11. Rode a auditoria determinística da obra inteira:
     ```bash
     python scripts/auditar-obra.py <slug>
     python scripts/validar-codigo.py <slug>
     python scripts/renderizar-diagramas.py <slug> --capitulos --validar
     ```
12. Invoque a skill `revisor-tecnico`. Se houver muitos capítulos defeituosos, distribua
     os capítulos apontados nos relatórios entre `subagente-revisor-tecnico` em lotes de 4.
     O revisor corrige: seções faltantes, referências insuficientes, `---`, citações órfãs,
     diagramas inválidos, código com erro de sintaxe, truncamento, **sobreposição de conteúdo
     entre capítulos** e **grafia inconsistente de termos**.
13. Reaudite até `--estrito` retornar 0, no máximo 3 rodadas:
     ```bash
     python scripts/auditar-obra.py <slug> --estrito
     python scripts/validar-codigo.py <slug> --estrito
     ```
     Parecer em `output/<slug>/revisao/parecer_revisao.md`.

## Passo 4 — Fase 3 (Compilação + PDF)
14. Invoque `compilador-abnt` — merge + elementos pré/pós-textuais + ABNT → `livro_final.md`.
15. Compile o PDF (renderiza os diagramas Mermaid em PNG, monta capa gráfica e ficha
     catalográfica, e usa o caminho Pandoc → `.typ` → Typst):
     ```bash
     python compilar-para-pdf.py <slug> --paginas-exatas
     ```
     > Alternativa PowerShell: `powershell -ExecutionPolicy Bypass -File scripts/converter-md-pdf.ps1 -Slug <slug>`
16. Se Pandoc+Typst falhar, tente o fallback CloudConvert:
     ```bash
     node .claude/mcp-servers/pdf-gen-server/compilar-livro.mjs <slug>
     ```
17. VALIDE o PDF gerado (existe, tamanho > 0, contagem de páginas ≥ 70).

## Passo 5 — Relatório de Entrega
18. Exiba, de forma telegráfica (REGRA 2):
     - caminhos de `livro_final.md` e `livro_final.pdf`
     - total de capítulos, caracteres e páginas do PDF
     - diagramas renderizados e taxa de aprovação do CI de código
     - veredito da auditoria (CONFORME / COM RESSALVAS / NÃO CONFORME)
     - checklist R1-R14 com o status de cada requisito
