---
name: compilador-abnt
description: Fase 4 da Fábrica Agêntica de Livros (Nós 5-10) — faz o merge de todos os capítulos aprovados e ilustrados, gera prefácio, conclusão geral e sumário dinâmico, compila as referências bibliográficas sem duplicatas, aplica normas ABNT de formatação e exporta o PDF final do livro via CloudConvert. Use somente depois que todos os capítulos da obra passaram pelo checkpoint humano e pela Fase 3.
---

# Skill_Compilador_ABNT

Você é o operário de acabamento e expedição da Fábrica Agêntica de Livros (Fase 4).

## Regras
- PT-BR estrito (REGRA 1). Sem metatexto (REGRA 2).
- **Auto-correção (REGRA 4):** se detectar capítulo fora do template EITA, hierarquia
  de títulos inconsistente, ou referência duplicada, corrija internamente antes de
  entregar o artefato final ao operador.
- **Nunca crie conta nem gere API key do CloudConvert em nome do operador.** Se
  `CLOUDCONVERT_API_KEY` não estiver disponível para o MCP `pdf_gen`, reporte a
  pendência objetivamente (com o link para o operador criar a própria conta gratuita) e
  siga em frente — a ausência da chave não bloqueia a expedição em Markdown.

## Requisitos Mínimos da Obra (VALIDAÇÃO OBRIGATÓRIA)
Antes de declarar a obra como concluída, o compilador DEVE validar:
- **Mínimo de 15 capítulos** na obra final. Se houver menos, reporte ao operador que a obra está incompleta e quais capítulos faltam.
- **Mínimo de 70 páginas** no PDF final (~17.500-21.000 palavras). Se o conteúdo não atingir esse patamar, reporte ao operador.
- **Todos os capítulos seguem o template EITA** (Explica, Ilustra, Técnica, Aplica). Rejeite capítulos que não seguem o padrão.
- **Referências bibliográficas REAIS e ACESSÍVEIS** — toda referência DEVE ter URL funcional ou estar em publicação amplamente disponível. Referências quebradas ou fictícias devem ser sinalizadas.
- **Conteúdo TRANSFORMACIONAL e com fator UAU** — o livro deve ir além de informar; deve transformar o leitor. Valide se há pelo menos uma revelação ou técnica surpreendente por capítulo.

## Objetivo
Consolidar capítulos, elementos extrusos e referências em um único manuscrito final,
normalizado conforme ABNT, e exportar em Markdown + PDF.

## Método Automatizado (recomendado)

Use o script `compilar-livro.mjs` que executa todos os 6 nós automaticamente:

```bash
node .claude/mcp-servers/pdf-gen-server/compilar-livro.mjs <slug-do-livro>
```

Exemplo:

```bash
node .claude/mcp-servers/pdf-gen-server/compilar-livro.mjs \
  aidd-ai-driven-development-em-contexto-de-ides-agneticas
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
9. Dispara MCP `pdf_gen` para gerar PDF via CloudConvert (Nó 10)

**Pré-requisitos para PDF:**
- `CLOUDCONVERT_API_KEY` configurada em `.claude/mcp-servers/pdf-gen-server/.env`
- Ver `README.md`, seção "Configurando o pdf_gen"

## Método Manual (se o script não estiver disponível)

Siga o procedimento abaixo passo a passo:

### Nó 5 — O Compilador (merge)
1. Leia `output/<livro>/sumario_macro.json` e, na ordem de Partes/Capítulos ali
   definida, concatene todos os `output/<livro>/capitulos/cap_<n>.md` (já ilustrados
   pelo `Skill_Diretor_Arte`) em um fluxo contínuo.
2. Corrija os paths das imagens: onde os capítulos usam `../imagens/`, mude para
   `imagens/` (porque `livro_final.md` fica no diretório raiz da obra, não em `capitulos/`).

### Nó 5.5 — Exportação de Selos Generativos (p5.js → SVG)
*Os selos de abertura de Parte são originalmente gerados como HTML/p5.js pelo
`subagente-design-por-parte` (reversa-selo-generativo). Para inclusão no PDF,
é necessário extrair versões SVG estáticas — o script `extrait-selo-svg.mjs` faz
isso sem depender de navegador headless, usando o mesmo algoritmo determinístico.*

3. Para cada Parte no `sumario_macro.json`:
   - Verifique se `output/<livro>/imagens/selo_parte_<n>.svg` já existe.
     (Se o `subagente-design-por-parte` já executou a extração, o SVG já estará lá.)
   - Se não existir, execute o script de extração:
     ```bash
     node scripts/extrair-selo-svg.mjs <slug> <parte> \
       --padrao <padrao> --estilo <estilo>
     ```
     - `<slug>`: o slug completo da obra (ex: `aidd-ai-driven-development-em-contexto-de-ides-agneticas-v2`)
     - `<parte>`: numeral romano (ex: `I`, `II`, `III`)
     - `--padrao`: opcional — um dos 5 padrões (flow-field, particle-orbit, crystal-lattice, wave-interference, noise-strata). Se omitido, deriva do seed.
     - `--estilo`: opcional — sober, premium, dense, exploratory. Se omitido, deriva do seed.
   - O script usa o **mesmo seed determinístico** do `subagente-design-por-parte`:
     `sha256(slug + "parte" + parte_atual)` — garantindo que o SVG gerado corresponda
     ao padrão visual do HTML original.
   - Saída: `output/<slug>/imagens/selo_parte_<parte>.svg`
4. Insira os selos SVG no `livro_final.md` como imagens antes de cada Parte:
   ```markdown
   ![Selo Generativo Parte I](imagens/selo_parte_I.svg)
   ```

> ⚠️ **Nota sobre PNG:** O script gera apenas SVG (escalável, ideal para PDF).
> Para versões PNG, instale `puppeteer` e use-o para capturar screenshot do
> `selo_parte_<n>.html` — ou converta o SVG gerado para PNG via ferramentas
> como Inkscape ou ImageMagick.

### Nó 6 — Elementos Extrusos
3. Gere um **Prefácio** em prosa densa, ancorando a visão macro da obra a partir de
   `sumario_macro.json.introducao`.
4. Gere uma **Conclusão Geral** em prosa densa, a partir de
   `sumario_macro.json.conclusao`.
5. Gere o **Sumário dinâmico**: lista de Partes/Capítulos com títulos exatos.

### Nó 7 — Auditor de Rastreabilidade
6. Colete todas as seções "Fontes brutas" de todos os
   `output/<livro>/pesquisa/dossie_*.md`, elimine duplicatas por URL normalizada, e
   ordene alfabeticamente por título.

### Nó 8 — Selo de Conformidade (ABNT)
7. Aplique formatação ABNT:
   - Hierarquia de títulos: `#` para todo elemento de primeiro nível.
   - Referências no formato ABNT (SOBRENOME, Nome. *Título*. Fonte/Editora, ano.)
   - Citações no corpo do texto no padrão autor-data quando aplicável.

### Nó 9 — A Expedição
8. Grave o artefato final consolidado em `output/<livro>/livro_final.md` com a ordem:
   Capa → Prefácio → Sumário → Partes/Capítulos com imagens →
   Conclusão Geral → Referências Bibliográficas → Contracapa.
9. Reporte ao operador, em uma linha objetiva, que o livro foi expedido em Markdown.

### Nó 10 — Exportação em PDF
10. Chame a tool `markdown_para_pdf` do MCP `pdf_gen` com:
    - `caminho_markdown`: caminho absoluto de `output/<livro>/livro_final.md`
    - `caminho_pdf_saida`: caminho absoluto de `output/<livro>/livro_final.pdf`
    - `titulo_obra`: o título do livro de `sumario_macro.json`
    - `subtitulo`: opcional, ex: "N Partes · N Capítulos"
11. Se a chamada retornar erro por ausência de `CLOUDCONVERT_API_KEY`, repasse a
    mensagem de configuração ao operador sem tentar contornar.
12. Se a conversão for bem-sucedida, reporte o caminho do PDF gerado.

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
- O template Paged.js (`template_livro.js`) já procura imagens em múltiplos
  candidatos de path, mas o path correto no Markdown é sem "../"
