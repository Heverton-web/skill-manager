---
name: compilador-abnt
description: Fase 3 da Fábrica Agêntica de Livros (Nós 5-10) — faz o merge de todos os capítulos aprovados e validados, gera prefácio, conclusão geral e sumário dinâmico, compila as referências bibliográficas sem duplicatas, aplica normas ABNT de formatação e exporta o PDF final do livro via Pandoc+Typst (método principal) ou CloudConvert (fallback). Use somente depois que todos os capítulos da obra passaram pela validação da Fase 2.
---

# Skill_Compilador_ABNT

Você é o operário de acabamento e expedição da Fábrica Agêntica de Livros (Fase 3).

## Regras
- PT-BR estrito (REGRA 1). Sem metatexto (REGRA 2).
- **Auto-correção (REGRA 4):** se detectar capítulo fora do template EITA-V2, hierarquia
  de títulos inconsistente, ou referência duplicada, corrija internamente antes de
  entregar o artefato final ao operador.
- **VALIDAÇÃO CONTRATUAL:** o compilador DEVE validar:
  1. Mínimo de 16 capítulos no sumário — caso contrário, reportar como NÃO CONFORME
  2. Mínimo estimado de 70 páginas (aproximadamente 175.000-210.000 caracteres de texto no formato ABNT) — alerta se abaixo
  3. Cada capítulo segue o template EITA-V2 (7 seções: Introdução, Explica, Ilustra, Técnica, Aplica, Conclusão, Referências)
  4. Todas as obras têm capa.svg, contracapa.svg e diagrama de arquitetura
  5. PDF foi gerado com sucesso via Pandoc+Typst (método principal)

## Objetivo
Consolidar capítulos, elementos extrusos e referências em um único manuscrito final,
normalizado conforme ABNT, e exportar em Markdown + PDF.

---

## Método Principal: Pandoc + Typst (recomendado)

Método 100% local, sem necessidade de API key ou conta externa. Gera PDF de alta qualidade
com formatação ABNT usando Pandoc como motor de conversão e Typst como motor de renderização.

### Pré-requisitos

| Ferramenta | Instalação | Verificação |
|---|---|---|
| **Pandoc** | `winget install JohnMacFarlane.Pandoc` ou https://pandoc.org/installing.html | `pandoc --version` |
| **Typst** | `winget install Typst.Typst` ou https://github.com/typst/typst/releases | `typst --version` |

### Arquivos do Método

| Arquivo | Caminho | Função |
|---|---|---|
| **Script de conversão** | `scripts/converter-md-pdf.ps1` | Executa Pandoc+Typst em lote ou individual |
| **Template ABNT** | `templates/template.typ` | Template Typst com margens ABNT, tipografia serifada, sumário, capa |

### Uso do Script

**Converter um livro específico:**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/converter-md-pdf.ps1 -Slug <slug-do-livro>
```

**Converter TODOS os livros da pasta output:**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/converter-md-pdf.ps1
```

**Parâmetros:**

| Parâmetro | Obrigatório | Descrição |
|---|---|---|
| `-Slug` | Não | Slug do livro. Se omitido, converte todos os livros com `livro_final.md` |
| `-OutputDir` | Não | Diretório de saída (padrão: `fabrica-de-livros\output`) |
| `-TemplatePath` | Não | Caminho do template.typ (padrão: `fabrica-de-livros\templates\template.typ`) |

### Pipeline de Conversão

O script `converter-md-pdf.ps1` executa o seguinte pipeline:

1. **Leitura** — Lê `livro_final.md` do diretório do livro
2. **Extração de título** — Regex `^#\s+(.+)$` para extrair o título do conteúdo
3. **Escaping de dollar signs** — Regex `(?<!\\)\$(?!\$)` escapeia `$` solitários para evitar erros de TeX math no Typst
4. **Arquivo temporário** — Grava conteúdo processado em `_temp_convert.md` usando `[System.IO.File]::WriteAllText()` (sem BOM)
5. **Conversão Pandoc** — Executa Pandoc com:
   - `--pdf-engine=typst` — Motor de renderização Typst
   - `--toc --toc-depth=3` — Gera sumário automático
   - `--number-sections` — Numera seções
   - `--template=template.typ` — Template ABNT
   - `--wrap=preserve` — Preserva quebras de linha do Markdown (importante para blocos de poesia/letras)
   - `--resource-path=$LivroPath` — Fallback para imagens relativas
   - `--from=markdown-citations` — Desabilita processamento de citações para evitar erros quando o livro não tem bibliografia estruturada
6. **Validação** — Verifica se o PDF foi gerado e conta páginas (estimativa via regex)
7. **Limpeza** — Remove arquivo temporário `_temp_convert.md`

### Template ABNT (template.typ)

O template Typst implementa:

| Elemento | Especificação |
|---|---|
| **Papel** | A4 |
| **Margens** | Topo: 3cm, Fundo: 2cm, Esquerda: 3cm, Direita: 2cm |
| **Tipografia** | Times New Roman / Liberation Serif, 12pt |
| **Parágrafos** | Justificados, espaçamento 0.75em, recuo 1.25cm |
| **Cabeçalho** | Título da obra (a partir da página 2) |
| **Rodapé** | Paginação "X de Y" |
| **Capa** | Título, subtítulo, autor, data |
| **Sumário** | Automático, 3 níveis, com recuo 1.5cm |
| **Títulos Nível 1** | 16pt bold com pagebreak; "Parte" usa 20pt |
| **Títulos Nível 2** | 14pt bold |
| **Títulos Nível 3** | 12pt bold |
| **Código** | Fundo cinza claro (luma 240), borda arredondada |

### Solução de Problemas Comuns

| Erro | Causa | Solução |
|---|---|---|
| `pandoc: command not found` | Pandoc não está no PATH | Instale via winget ou adicione ao PATH manualmente |
| `typst: command not found` | Typst não está no PATH | Instale via winget ou baixe do GitHub Releases |
| `expected integer, float... found content` | Template com `try/catch` inválido | Usar `type(it.body) == str` em vez de try/catch |
| `$` isolado causa erro de math | Dollar sign interpretado como TeX | Script já escapa automaticamente com regex |
| PDF com poucas páginas | Conteúdo insuficiente | Expandir capítulos para mínimo 70 páginas |
| Imagens não aparecem | Path incorreto | Usar `--resource-path` (já implementado no script) |

### Validação Pós-Conversão

O script valida automaticamente:
- **Existência do PDF** — Verifica se o arquivo foi gerado
- **Contagem de páginas** — Estimativa via regex `/Type\s*/Page[^s]` no PDF
- **Aviso mínimo 70 páginas** — Alerta amarelo se abaixo do mínimo (não bloqueia)

---

## Método Alternativo: CloudConvert (fallback)

Usa o MCP `pdf_gen` com API do CloudConvert. Requer configuração prévia.

### Pré-requisitos
- `CLOUDCONVERT_API_KEY` configurada em `.claude/mcp-servers/pdf-gen-server/.env`
- Conta gratuita em https://cloudconvert.com/register
- **Nunca crie conta nem gere API key em nome do operador**

### Uso via MCP
Chame a tool `markdown_para_pdf` do MCP `pdf_gen` com:
- `caminho_markdown`: caminho absoluto de `output/<livro>/livro_final.md`
- `caminho_pdf_saida`: caminho absoluto de `output/<livro>/livro_final.pdf`
- `titulo_obra`: o título do livro de `sumario_macro.json`
- `subtitulo`: opcional, ex: "N Partes · N Capítulos"

### Uso via Script (compilar-livro.mjs)
```bash
node .claude/mcp-servers/pdf-gen-server/compilar-livro.mjs <slug-do-livro>
```

---

## Método Automatizado Completo (recomendado para produção)

### Opção A — Python (Pandoc+Typst, recomendado)

Use o script `compilar-para-pdf.py` que executa merge + conversão PDF:

```bash
python compilar-para-pdf.py <slug-do-livro>
```

O script:
1. Lê todos os `cap_<n>.md` do diretório `capitulos/` (Nó 5)
2. Concatena na ordem correta (Nó 5)
3. Gera Prefácio e Conclusão (Nó 6)
4. Aplica formatação ABNT com YAML frontmatter (Nó 8)
5. Converte para PDF via Pandoc+Typst com template ABNT (Nó 10)

### Opção B — Node.js (Pandoc+Typst com fallback CloudConvert)

Use o script `compilar-livro.mjs` para merge + PDF:

```bash
node .claude/mcp-servers/pdf-gen-server/compilar-livro.mjs <slug-do-livro>
```

O script:
1. Lê `sumario_macro.json` da obra (Nó 5)
2. Concatena todos os `cap_<n>.md` na ordem correta (Nó 5)
3. Gera Prefácio a partir de `sumario_macro.json.introducao` (Nó 6)
4. Gera Conclusão Geral a partir de `sumario_macro.json.conclusao` (Nó 6)
5. Gera Sumário dinâmico com todos os Partes/Capítulos (Nó 6)
6. Compila referências dos dossiês de pesquisa, eliminando duplicatas (Nó 7)
7. Aplica formatação ABNT (Nó 8)
8. Grava `output/<slug>/livro_final.md` (Nó 9)
9. Gera PDF via Pandoc+Typst (Nó 10 — método principal)
10. Fallback para CloudConvert se Pandoc+Typst não estiver disponível

---

## Método Manual (se os scripts não estiverem disponíveis)

Siga o procedimento abaixo passo a passo:

### Nó 5 — O Compilador (merge)
1. Leia `output/<livro>/sumario_macro.json` e, na ordem de Partes/Capítulos ali
   definida, concatene todos os `output/<livro>/capitulos/cap_<n>.md` em um fluxo contínuo.

### Nó 6 — Elementos Extrusos
2. Gere um **Prefácio** em prosa densa a partir de `sumario_macro.json.introducao`.
3. Gere uma **Conclusão Geral** em prosa densa a partir de `sumario_macro.json.conclusao`.
4. Gere o **Sumário dinâmico**: lista de Partes/Capítulos com títulos exatos.

### Nó 7 — Auditor de Rastreabilidade
5. Colete todas as seções "Fontes brutas" de todos os
   `output/<livro>/pesquisa/dossie_*.md`, elimine duplicatas por URL normalizada, e
   ordene alfabeticamente por título.

### Nó 8 — Selo de Conformidade (ABNT)
6. Aplique formatação ABNT:
   - Hierarquia de títulos: `#` para todo elemento de primeiro nível.
   - Referências no formato ABNT (SOBRENOME, Nome. *Título*. Fonte/Editora, ano.)

### Nó 9 — A Expedição
7. Grave o artefato final em `output/<livro>/livro_final.md` com a ordem:
    Prefácio → Sumário → Partes/Capítulos → Conclusão Geral → Referências Bibliográficas.

### Nó 10 — Exportação em PDF (Pandoc+Typst — método principal)
8. Execute o script de conversão Pandoc+Typst (método principal, 100% local):
    ```powershell
    powershell -ExecutionPolicy Bypass -File scripts/converter-md-pdf.ps1 -Slug <slug>
    ```
    Ou via Python (alternativa recomendada para produção):
    ```bash
    python compilar-para-pdf.py <slug>
    ```
    **Fallback — CloudConvert (requer API key):**
    ```bash
    node .claude/mcp-servers/pdf-gen-server/compilar-livro.mjs <slug>
    ```

---

## Template de livro_final.md

```
![Capa do Livro](imagens/capa.svg)

# Prefácio
...

# Sumário
...

---

# Parte I — Título
...

# Conclusão
...

# Referências Bibliográficas
...

![Contracapa do Livro](imagens/contracapa.svg)
```

## Notas sobre paths de imagens no livro_final.md

- `livro_final.md` está em `output/<slug>/`
- As imagens estão em `output/<slug>/imagens/`
- Portanto, paths relativos são: `imagens/capa.svg` (NÃO `../imagens/capa.svg`)
- O script de conversão usa `--resource-path` como fallback para paths relativos
