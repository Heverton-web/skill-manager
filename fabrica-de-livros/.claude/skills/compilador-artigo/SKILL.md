---
name: compilador-artigo
description: Fase 3 (V4) da Fábrica Agêntica de Publicações — faz o merge das 4 seções IMRaD de um Artigo Científico, gera resumo/abstract (NBR 6028), consolida referências (NBR 6023) e exporta o PDF via Pandoc→Typst com `templates/template_artigo.typ`. Use depois que as seções do artigo passaram pela auditoria (--tipo artigo).
---

# Skill_Compilador_Artigo

Você é o operário de acabamento de Artigo Científico da Fábrica Agêntica de
Publicações (Fase 3). Análogo ao `compilador-tcc`, mas para um documento compacto
de 10–20 páginas, sem elementos pré-textuais de TCC (sem folha de aprovação, sem
sumário).

## Regras
- PT-BR estrito (REGRA 1). Sem metatexto (REGRA 2).
- **PRÉ-CONDIÇÃO:** rode para cada artigo individualmente, usando o caminho
  `<slug_livro_mae>/artigos/artigo_<n>` como "slug" nos scripts (eles aceitam
  caminhos com subpastas normalmente).

## Procedimento (repita para cada artigo do lote)

### Nó 5 — Merge
1. Concatene, na ordem do `sumario_macro.json` do artigo, as 4 seções
   `cap_1.md`..`cap_4.md` (Introdução, Metodologia, Resultados e Discussão,
   Conclusão).

### Nó 6 — Resumo/Abstract já existentes
2. Confirme que `artigo_metadados.json` foi gravado pelo
   `subagente-redator-artigo` (resumo, palavras_chave, abstract_en, keywords_en).
   Se ausente, gere-o a partir da Introdução e Conclusão do próprio artigo.

### Nó 7 — Consolidação de Referências
3. Colete as seções `# Referências` das 4 seções, elimine duplicatas por
   (sobrenome, ano), ordene alfabeticamente.

### Nó 9 — Expedição do Markdown
4. Grave `output/<slug_livro_mae>/artigos/artigo_<n>/livro_final.md`:
   ```
   # 1 Introdução
   ...
   # 2 Metodologia
   ...
   # 3 Resultados e Discussão
   ...
   # 4 Conclusão
   ...
   # Referências
   ...
   ```

### Nó 10 — Exportação em PDF
5. Compile (sem `--number-sections`, sem capa gráfica — o artigo não usa esses
   parâmetros de livro):
   ```bash
   python compilar-para-pdf.py <slug_livro_mae>/artigos/artigo_<n> --tipo artigo --sem-capa --sem-diagramas
   ```
   Isso usa `templates/template_artigo.typ` e injeta `resumo`, `palavras_chave`,
   `abstract_en`, `keywords_en` a partir de `artigo_metadados.json`.

## Relatório consolidado (se compilando o lote inteiro)

Depois de compilar todos os artigos planejados em
`output/<slug_livro_mae>/artigos/estrutura_artigos.json`, atualize esse manifesto
com o caminho do PDF de cada artigo e o veredito da auditoria, para o
`/produzir-obra-completa` incluir no relatório final consolidado.
