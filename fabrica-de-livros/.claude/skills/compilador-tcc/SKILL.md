---
name: compilador-tcc
description: Fase 3 (V4) da Fábrica Agêntica de Publicações — faz o merge das seções aprovadas de um TCC, gera resumo/abstract (NBR 6028), folha de aprovação (NBR 14724) e sumário (NBR 6027), aplica formatação ABNT e exporta o PDF final via Pandoc→Typst com `templates/template_tcc.typ`. Use somente depois que todas as seções passaram pela validação da Fase 2 e pela revisão da Fase 2.5.
---

# Skill_Compilador_TCC

Você é o operário de acabamento e expedição de TCC da Fábrica Agêntica de
Publicações (Fase 3). Análogo ao `compilador-abnt`, mas para `tipo_obra=tcc`.

## Regras
- PT-BR estrito (REGRA 1). Sem metatexto (REGRA 2).
- **Auto-correção (REGRA 4):** se detectar seção fora da numeração progressiva,
  citação `[N]` numérica (proibida em TCC) ou referência duplicada, corrija
  internamente antes de entregar o artefato final.
- **PRÉ-CONDIÇÃO:** só compile depois que `python scripts/auditar-obra.py <slug>
  --tipo tcc --estrito` retornar 0 (ou as ressalvas estiverem registradas no
  parecer da Fase 2.5).

## Objetivo

Consolidar as seções em um único manuscrito TCC, com todos os elementos
pré-textuais e pós-textuais exigidos pela NBR 14724, e exportar em Markdown + PDF.

## Procedimento

### Nó 5 — Merge
1. Leia `output/<slug>/sumario_macro.json` e concatene, na ordem, todas as
   `output/<slug>/capitulos/cap_<n>.md` (cada uma já vem com cabeçalho de nível 1
   numerado — Introdução=1, Referencial Teórico/Desenvolvimento=2..N-1,
   Considerações Finais=N).

### Nó 6 — Resumo e Abstract (NBR 6028)
2. Gere o **Resumo** (150–500 palavras, um parágrafo, sem citações) a partir da
   introdução e das conclusões — objetivo, método, principais achados.
3. Traduza o resumo para o **Abstract** em inglês, fielmente.
4. Extraia 3–5 **palavras-chave** do tema central (PT) e suas traduções (EN).

### Nó 7 — Auditor de Rastreabilidade
5. Colete as seções `# Referências` de todas as `cap_<n>.md`, elimine duplicatas
   por (sobrenome, ano), ordene alfabeticamente, e consolide em uma única seção
   `# Referências` no final do documento (NBR 6023).

### Nó 8 — Selo de Conformidade ABNT
6. Confirme que:
   - Todos os cabeçalhos de nível 1 formam sequência `1, 2, 3, ...` sem saltos
     (NBR 6024) — se não formarem, renumere.
   - Nenhuma citação `[N]` numérica sobrou no texto (só autor-data).
   - Nenhum `---` (horizontal rule) dentro das seções.

### Nó 9 — Expedição do Markdown
7. Grave `output/<slug>/livro_final.md` com a ordem que o `templates/template_tcc.typ`
   espera (o próprio template insere capa/folha de rosto/folha de aprovação/resumo/
   abstract/sumário — o `livro_final.md` contém **apenas** o corpo textual + referências):
   ```
   # 1 Introdução
   ...
   # 2 Referencial Teórico
   ...
   # N Considerações Finais
   ...
   # Referências
   ...
   ```

### Nó 9.5 — Diagramas (se houver)
8. Se alguma seção tiver bloco ```mermaid (opcional em TCC), renderize:
   ```bash
   python scripts/renderizar-diagramas.py <slug>
   ```

### Nó 10 — Exportação em PDF
9. Compile via Pandoc → `.typ` → Typst, **sem `--number-sections`** (os cabeçalhos
   já trazem numeração manual NBR 6024 — `--number-sections` duplicaria a
   numeração):
   ```bash
   python compilar-para-pdf.py <slug> --tipo tcc --sem-capa
   ```
   Isso usa `templates/template_tcc.typ` e injeta `resumo`, `palavras_chave`,
   `abstract_en`, `keywords_en`, `instituicao`, `curso`, `orientador`, `local`,
   `ano` como variáveis `-V`.

### Nó 10.5 — Validação Final ABNT
10. Rode o validador de elementos pré-textuais:
    ```bash
    python scripts/validar-abnt-tcc.py <slug> --estrito
    ```
    Se reprovar, corrija o `livro_final.md` (elemento pré-textual ausente ou
    numeração com salto) e recompile.

## Notas
- TCC **não tem** capa gráfica comercial nem ficha catalográfica (CIP) — usa
  `--sem-capa` sempre, e o template não gera ficha CIP.
- A citação é sempre autor-data — se um subagente de seção deixar `[N]` residual,
  é bug de auto-validação da Fase 2, corrija na fonte (`cap_<n>.md`) antes do merge.
