---
description: Compila múltiplos livros da Fábrica Agêntica em um único mega-livro estruturado — unifica sumários, concatena capítulos em numeração sequencial, gera prefácio + sumário + conclusão, e exporta PDF via Pandoc+Typst (ABNT). Use: /compilar-mega-livro slug1 slug2 ... ou /compilar-mega-livro --todas
---

Você é o Orquestrador Mestre da Fábrica Agêntica de Livros (ver `CLAUDE.md`).

O operador solicitou a compilação de múltiplos livros em um mega-livro único.

## Sintaxe

```
/compilar-mega-livro <slug1> [slug2] [slug3] ...
/compilar-mega-livro --todas
/compilar-mega-livro --all
```

Exemplos:
```
/compilar-mega-livro 01-aidd-ai-driven-development 02-harness-camada-orquestracao
/compilar-mega-livro --todas
```

## Fluxo

### 1. Interpretar argumentos

Se `$ARGUMENTS` contiver `--todas` ou `--all`:
   Use todos os slugs de `compilar-para-pdf.py` (exceto `00-mega-livro-todos-aidd`).
   Slug do compilado: `compilado-completo-aidd-<AAAA-MM-DD>` (data atual).
   Ex: `compilado-completo-aidd-2026-07-30`

Se `$ARGUMENTS` contiver slugs específicos:
   Use exatamente os slugs informados.
   Derive o slug do compilado a partir dos slugs (ex: `01-aidd-02-harness`).

### 2. Validar slugs

Para cada slug, verifique se `output/<slug>/sumario_macro.json` existe.
Se algum não existir, reporte e pergunte se deseja continuar sem ele.

### 3. Invocar skill compilador-mega-livro

Invoque a skill `compilador-mega-livro` com:
- A lista de slugs validados
- O slug do compilado (nome da pasta)

> A criação da estrutura de pastas (`rm -rf`, `mkdir -p`) é de responsabilidade
> exclusiva da skill (passo 2 da skill). O comando não deve duplicar essa lógica.

A skill irá:
1. Limpar e criar a pasta `output/<slug-compilado>/` com subpastas `capitulos/` e `imagens/`
2. Coletar capa/contracapa do primeiro livro
3. Ler e unificar os sumários macro
4. Salvar `sumario_macro.json` na pasta do compilado
5. Concatenar e RENUMERAR todos os capítulos sequencialmente
6. Salvar cada capítulo renumerado em `output/<slug-compilado>/capitulos/`
7. Gerar prefácio + sumário + conclusão
8. Salvar `livro_final.md` na pasta do compilado
9. Gerar PDF via Pandoc+Typst na pasta do compilado

### 4. Validar PDF gerado

Após a execução da skill, verifique DENTRO da pasta do compilado:
```bash
ls -la output/<slug-compilado>/livro_final.pdf
ls -la output/<slug-compilado>/<slug-compilado>.pdf
ls -la output/<slug-compilado>/livro_final.md
ls -la output/<slug-compilado>/sumario_macro.json
ls output/<slug-compilado>/capitulos/cap_*.md | wc -l
```

### 5. Relatório final

Exiba:
- **Pasta do compilado:** `output/<slug-compilado>/`
- **Slug:** `<slug-compilado>`
- **Total de livros incluídos:** N
- **Total de capítulos:** M
- **PDF:** `output/<slug-compilado>/<slug-compilado>.pdf` (tamanho)
- **Markdown:** `output/<slug-compilado>/livro_final.md`
- **Sumário:** `output/<slug-compilado>/sumario_macro.json`
- **Capítulos individuais:** `output/<slug-compilado>/capitulos/cap_*.md`
- **Numeração:** sequencial 1 a M ✓ ou ✗ (verificar se há saltos)
- **Status:** OK ou FALHA
