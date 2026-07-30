---
name: compilador-mega-livro
description: Compila múltiplos livros da Fábrica Agêntica em um único mega-livro estruturado — lê sumários macro, unifica partes e capítulos em numeração sequencial, gera prefácio, sumário dinâmico e conclusão geral, e exporta PDF via Pandoc+Typst (formatação ABNT). Use quando o operador solicitar unificação de livros em uma obra completa.
---

# Skill_Compilador_Mega_Livro

Você é o compilador de mega-livros da Fábrica Agêntica de Livros. Sua função é
pegar múltiplos livros (cada um com seu `sumario_macro.json` e `capitulos/cap_<n>.md`)
e fundi-los em **um único livro completo e estruturado**, com numeração contínua de
capítulos, prefácio, sumário unificado, conclusão geral e PDF ABNT.

## Regras

- PT-BR estrito (REGRA 1). Sem metatexto (REGRA 2).
- **Auto-correção (REGRA 4):** corrija internamente problemas de estrutura,
  hierarquia de títulos inconsistente, paths de imagens ou referências duplicadas.
- **VALIDAÇÃO CONTRATUAL:** ao final, valide:
  1. PDF foi gerado com sucesso via Pandoc+Typst
  2. A estrutura do livro_final.md está completa (Prefácio → Sumário → Partes/Capítulos → Conclusão)
  3. A numeração de capítulos é sequencial e sem saltos

## Fluxo de Compilação

### 1. Receber slugs dos livros

O operador informa a lista de slugs (pastas em `output/<slug>/`) a compilar.
Exemplo: `01-aidd-ai-driven-development, 02-harness-camada-orquestracao`

Se o operador usar `--todas` ou `--all`, compile automaticamente todos os slugs
da lista `SLUGS` em `compilar-para-pdf.py` (exceto `00-mega-livro-todos-aidd`).

### 2. Definir nome do livro compilado e criar pasta específica (limpa)

**O slug do compilado determina o nome da pasta de saída.**

- Se `--todas`: slug = `compilado-completo-aidd-<AAAA-MM-DD>`
  (ex: `compilado-completo-aidd-2026-07-30`) — o timestamp previne sobrescrita
  de compilações anteriores.
- Se slugs específicos: derive um slug descritivo a partir do primeiro slug
  Exemplo: `01-aidd-ai-driven-development` + `02-harness-camada-orquestracao` →
  slug = `compilado-01-aidd-02-harness`

**Crie a estrutura de pastas do zero — com limpeza prévia:**

```bash
rm -rf output/<slug-compilado>          # garante pasta limpa
mkdir -p output/<slug-compilado>/capitulos
mkdir -p output/<slug-compilado>/imagens
```

> ⚠️ O `rm -rf` garante que não haja arquivos residuais de compilações anteriores.
> A pasta é criada especificamente para esta compilação. O nome reflete o conteúdo
> compilado. Toda a estrutura (sumário, capítulos, MD final, PDF) será salva DENTRO
> desta pasta.

### 3. Coletar capa e contracapa dos livros fonte

Para dar identidade visual ao compilado, copie `capa.svg` e `contracapa.svg`
do primeiro livro da lista para `output/<slug-compilado>/imagens/`.

```bash
cp output/<slug-primeiro>/imagens/capa.svg output/<slug-compilado>/imagens/capa.svg
cp output/<slug-primeiro>/imagens/contracapa.svg output/<slug-compilado>/imagens/contracapa.svg
```

Se o primeiro não tiver, tente o segundo, e assim por diante.

### 4. Ler e unificar sumários macro

Para cada slug, leia `output/<slug>/sumario_macro.json`.

Crie um novo sumário macro unificado com:

```json
{
  "titulo_obra": "Guia Completo de AI-Driven Development",
  "subtitulo": "Compilado dos Livros da Fábrica Agêntica de Livros",
  "introducao": "Este compilado reúne N livros da Fábrica Agêntica de Livros, totalizando M capítulos que abrangem desde fundamentos conceituais até padrões avançados de orquestração de agentes de IA.",
  "conclusao": "Ao longo desta obra completa, exploramos as múltiplas facetas do paradigma AI-Driven Development. O conhecimento aqui consolidado forma uma base sólida para qualquer profissional que deseja dominar a arte de orquestrar agentes de IA.",
  "partes": [
    {
      "parte": 1,
      "titulo_parte": "<título do primeiro livro>",
      "capitulos": [
        { "capitulo": 1, "titulo": "<título do primeiro capítulo>" }
      ]
    }
  ]
}
```

Regras para o sumário unificado:
- **Partes** = mantém os títulos originais de cada livro como título de Parte
- **Capítulos** = renumere sequencialmente do 1 ao total final
- **Subtítulos**: inclua subtítulo de cada capítulo se existir no sumário original

### 5. Salvar sumário macro na pasta do compilado

```bash
# Salva na pasta específica da compilação
output/<slug-compilado>/sumario_macro.json
```

### 6. Concatenar capítulos na ordem, renumerando sequencialmente

Para cada parte (livro) no sumário unificado, em ordem:

1. Para cada capítulo, leia `output/<slug-original>/capitulos/cap_<n>.md`
2. **Corrija o título do capítulo** para refletir a numeração SEQUENCIAL global
   (ex: cap_1 do livro 02 vira "Capítulo 21" no compilado, não "Capítulo 1")
3. **Corrija paths de imagens**: `../imagens/` → `imagens/`
4. **Remova frontmatter YAML interno** (`---\n...\n---`) que possa conflitar
5. Salve o capítulo renumerado em:
   ```bash
   output/<slug-compilado>/capitulos/cap_<n>.md
   ```
   Onde `<n>` é o número SEQUENCIAL GLOBAL (1, 2, 3, ..., total_final)

> ⚠️ A RENUMERAÇÃO é obrigatória para que o sumário (TOC) do PDF gerado por
> Pandoc+Typst exiba a numeração correta do Capítulo 1 ao Capítulo N, sem saltos.

#### Como renumerar

No conteúdo de cada capítulo, substitua o título:
```
# Capítulo <numero_original> — Título
# Capítulo <numero_original>: Título
```
por:
```
# Capítulo <numero_sequencial> — Título
```

Use regex:
```python
conteudo = re.sub(
    r'^# Cap[ií]tulo \d+[\s]*[—:]+[\s]*',
    f'# Capítulo {contador_global} — ',
    conteudo
)
```

### 7. Gerar elementos extrusos

#### Prefácio

Use `sumario_macro.unificado.introducao` como base. Inclua:
- Número de livros compilados
- Total de capítulos
- Visão geral dos temas abordados

#### Sumário dinâmico

```markdown
# Sumário

- **Parte 1 — Título da Parte**
  - Capítulo 1: Título do Capítulo
  - Capítulo 2: Título do Capítulo
...
```

#### Conclusão Geral

Use `sumario_macro.unificado.conclusao` como base. Síntese da jornada.

### 8. Montar livro_final.md e salvar na pasta do compilado

Ordem obrigatória:

```markdown
![Capa do Livro](imagens/capa.svg)

# <Título da Obra>

*<Subtítulo>*

# Prefácio
...

# Sumário
...

---

<corpo dos capítulos>

---

# Conclusão
...

![Contracapa do Livro](imagens/contracapa.svg)
```

Salve em:
```
output/<slug-compilado>/livro_final.md
```

### 9. Gerar PDF via Pandoc+Typst e salvar na pasta do compilado

**Método principal (Pandoc+Typst):**

```powershell
powershell -ExecutionPolicy Bypass -File scripts/converter-md-pdf.ps1 -Slug <slug-compilado>
```

**Alternativa Python:**

```bash
python compilar-para-pdf.py <slug-compilado>
```

Os PDFs serão gerados em:
```
output/<slug-compilado>/livro_final.pdf
output/<slug-compilado>/<slug-compilado>.pdf   ← nome descritivo da compilação
```

### 10. Validação final

Verifique dentro da pasta do compilado:
- [ ] `output/<slug-compilado>/livro_final.md` existe
- [ ] `output/<slug-compilado>/sumario_macro.json` existe
- [ ] `output/<slug-compilado>/livro_final.pdf` existe e tem tamanho > 0
- [ ] `output/<slug-compilado>/<slug-compilado>.pdf` existe (cópia com nome descritivo)
- [ ] Todos os capítulos estão incluídos (conferir contagem no sumário vs arquivos)
- [ ] Numeração sequencial SEM SALTOS (1, 2, 3, ..., N)
- [ ] Capítulos individuais salvos em `output/<slug-compilado>/capitulos/cap_*.md`

---

## Template de livro_final.md completo

```markdown
![Capa do Livro](imagens/capa.svg)

# <Título da Obra>

*<Subtítulo>*

# Prefácio

Este compilado reúne <N> livros, totalizando <M> capítulos que cobrem...

# Sumário

- **Parte 1 — <Título>**
  - Capítulo 1: <Título>
  - Capítulo 2: <Título>
...

---

# Parte 1 — <Título do Livro 1>

# Capítulo 1 — <Título>
## E — Explique
...

# Capítulo 2 — <Título>
...

---

# Parte 2 — <Título do Livro 2>

# Capítulo <N+1> — <Título>
...

---

# Conclusão

...

![Contracapa do Livro](imagens/contracapa.svg)
```

## Solução de Problemas

| Problema | Causa | Solução |
|----------|-------|---------|
| Capítulos na ordem errada | Ordem incorreta no sumário unificado | Verificar sequência no sumario_macro.json |
| Imagens quebradas no PDF | Path relativo incorreto | Corrigir `../imagens/` → `imagens/` nos capítulos |
| Numeração duplicada | Capítulos com mesmo número original | Renumerar sequencialmente no sumário unificado |
| Livro muito grande | Muitos capítulos (ex: 238) | Aumentar timeout do Pandoc para 300s+ |
