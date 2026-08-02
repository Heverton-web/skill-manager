# SPEC_TCC — Produção Autônoma de TCC/Monografia (NBR 14724)

Especifica o processo disparado por `/criar-tcc <tema-ou-slug>` — variação do
`/criar-livro` da V3 para `tipo_obra=tcc`. Ver `CLAUDE.md` para as regras globais e
`docs/normas-abnt-referencia.md` para o resumo das normas ABNT envolvidas.

## 1. Requisitos Contratuais

| # | Requisito | Critério | Verificação |
|---|---|---|---|
| R-TCC-1 | Estrutura NBR 14724 completa | Capa, folha de rosto, folha de aprovação, resumo, abstract, sumário | `template_tcc.typ` (estrutural) + `validar-abnt-tcc.py` (conteúdo) |
| R-TCC-2 | Resumo em PT + palavras-chave | Não vazio, NBR 6028 | `validar-abnt-tcc.py` |
| R-TCC-3 | Abstract + keywords | Tradução fiel do resumo | `validar-abnt-tcc.py` |
| R-TCC-4 | Numeração progressiva | `\d+(\.\d+)*` sem saltos (NBR 6024) | `auditar-obra.py --tipo tcc` (por seção) + `validar-abnt-tcc.py` (global) |
| R-TCC-5 | Citação autor-data | `(SOBRENOME, ano)` — nenhum `[N]` numérico | `auditar-obra.py --tipo tcc` |
| R-TCC-6 | Referências mínimas | `min_referencias_por_capitulo` (5–20, de `config_obra.json`) | `auditar-obra.py --tipo tcc` |
| R-TCC-7 | Tom acadêmico impessoal | Sem 2ª pessoa, sem linguagem comercial-transformacional | `revisor-tecnico` (amostragem manual) |
| R-TCC-8 | Sem truncamento/pendência | Nenhum TODO/placeholder | `auditar-obra.py --tipo tcc` |
| R-TCC-9 | PDF final | Via Pandoc → `.typ` → Typst, `template_tcc.typ` | `compilar-para-pdf.py` |

## 2. Diferenças estruturais vs. Livro (V3)

| | Livro | TCC |
|---|---|---|
| `sumario_macro.json` | N Partes × M Capítulos | 1 "parte" única, seções sequenciais |
| Framework de redação | EITA-V2 (7 seções, tom comercial) | ACAD (4 momentos, tom acadêmico) |
| Citação | `[N]` numérica | `(SOBRENOME, ano)` autor-data |
| Numeração de título | `--number-sections` do Pandoc | Manual no corpo (NBR 6024) — Pandoc NÃO numera |
| Capa | Gráfica colorida + ficha CIP | Sobre (sem cor) + folha de aprovação |
| Diagrama Mermaid | Obrigatório | Opcional |
| Template Typst | `templates/template.typ` | `templates/template_tcc.typ` |

## 3. Fluxo de Execução

```
[Fase 0 — /esbocar ou pergunta minima de refs]
        │
        ▼
[Fase 1 — Pesquisa + arquiteto (schema TCC)]
        │
        ▼
[Fase 2 — subagente-redator-secao-tcc em lotes de 4]
   (estrategista/ACAD → redator-academico → CI de citacao)
        │
        ▼
[Fase 2.5 — auditar-obra.py --tipo tcc → revisor-tecnico]
        │
        ▼
[Fase 3 — compilador-tcc → tcc_metadados.json + livro_final.md
          → compilar-para-pdf.py (template_tcc.typ)
          → validar-abnt-tcc.py --estrito]
        │
        ▼
[Relatório de entrega]
```

## 4. Contratos de dados

TCC vive em `output/tccs/<slug>/` (V4.1: raízes separadas por tipo de obra no topo
de `output/`). `config_obra.json` fica na raiz da obra, sem subpasta `esboco/`.

- `output/tccs/<slug>/config_obra.json` — `tipo_obra="tcc"`, `min_referencias_por_capitulo`.
- `output/tccs/<slug>/sumario_macro.json` — schema com 1 parte, seções ACAD.
- `output/tccs/<slug>/capitulos/cap_<n>.md` — seção com numeração progressiva + citação autor-data.
- `output/tccs/<slug>/tcc_metadados.json` — `resumo`, `palavras_chave`, `abstract_en`,
  `keywords_en`, `instituicao`, `curso`, `orientador`, `local`, `ano`.
- `output/tccs/<slug>/revisao/relatorio_abnt_tcc.json` — saída de `validar-abnt-tcc.py`.

## 5. Casos de borda

| Situação | Comportamento |
|---|---|
| `tcc_metadados.json` ausente na compilação | `compilar-para-pdf.py` cai no template comercial de livro — `validar-abnt-tcc.py` reprova `TCC-PRE-METADADOS` |
| Citação `[N]` residual em uma seção | `revisor-tecnico` converte para autor-data antes do merge |
| Numeração com salto (1, 3, ...) | `compilador-tcc` renumera antes de gravar `livro_final.md` |
| Instituição/curso/orientador não fornecidos | Campos ficam vazios no template (blocos condicionais `$if(...)$` os omitem) |
