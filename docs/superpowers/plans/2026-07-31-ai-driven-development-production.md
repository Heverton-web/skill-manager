# Plano de Produção: Livro AI-Driven Development com OpenCode

> **Para trabalhadores agênticos:** OBRIGATÓRIO usar a skill `superpowers:executing-plans` ou executar os passos sequencialmente. Cada tarefa usa checkbox (`- [ ]`) para rastreamento.

**Objetivo:** Produzir o livro "AI-Driven Development com OpenCode" (18 capítulos, 70-90 páginas, PDF ABNT) usando a Fábrica Agêntica de Livros.

**Arquitetura:** A Fábrica Agêntica já está implementada em `fabrica-de-livros/`. Este plano executa a produção do livro específico usando a esteira existente (pesquisador → arquiteto → redatores paralelos → compilador → PDF).

**Tech Stack:** Fábrica Agêntica (Claude Code Skills, MCPs SQLite/filesystem, Pandoc+Typst)

---

## Pré-requisitos

| Item | Status esperado | Validação |
|------|----------------|-----------|
| Node.js >= 18 | Instalado | `node --version` |
| Pandoc | Instalado | `pandoc --version` |
| Typst | Instalado | `typst --version` |
| Git | Instalado | `git --version` |
| Fábrica clonada | Diretório `fabrica-de-livros/` existe | `ls fabrica-de-livros/` |

---

## Tarefa 1: Verificação de Prontidão

**Arquivos:** Nenhum (comandos de verificação)

- [ ] **Passo 1: Verificar dependências**

```powershell
node --version
pandoc --version
typst --version
git --version
```

Esperado: Todas as versões exibidas sem erro.

- [ ] **Passo 2: Verificar estrutura da fábrica**

```powershell
ls fabrica-de-livros/.claude/skills/
ls fabrica-de-livros/.claude/agents/
ls fabrica-de-livros/.claude/commands/
ls fabrica-de-livros/.mcp.json
```

Esperado: Listagens com conteúdo (não vazio).

- [ ] **Passo 3: Verificar MCP db_state**

```powershell
ls fabrica-de-livros/data/
```

Esperado: Pasta `data/` existe (será criada automaticamente se não existir).

- [ ] **Passo 4: Verificar templates**

```powershell
ls fabrica-de-livros/templates/
```

Esperado: `payload_estado.json` e `template_eita.md` presentes.

---

## Tarefa 2: Limpeza de Estado Anterior

**Arquivos:** Nenhum (verificação de conflitos)

- [ ] **Passo 1: Verificar se output/ai-driven-development já existe**

```powershell
ls fabrica-de-livros/output/ai-driven-development
```

Se existir → será usado sufixo `-v2` automaticamente (não requer ação manual).

- [ ] **Passo 2: Verificar estado do banco de dados**

```powershell
# Opcional: verificar se há registros antigos
ls fabrica-de-livros/data/estado_fabrica.db
```

Se existir registros antigos, a fábrica trata automaticamente (REGRA 4 — Auto-Correção Interna).

---

## Tarefa 3: Disparo da Produção

**Arquivos:** `.claude/commands/criar-livro.md` (já implementado)

- [ ] **Passo 1: Executar comando de produção**

Abrir terminal no diretório `fabrica-de-livros/` e executar:

```
/criar-livro AI-Driven Development com OpenCode: LLMs Gratuitas, FABLE e Economia Severa de Tokens
```

**Alternativa (fora do Claude Code):**

```
Peça ao agente: "Siga o processo de .claude/commands/criar-livro.md para o tema AI-Driven Development com OpenCode: LLMs Gratuitas, FABLE e Economia Severa de Tokens"
```

- [ ] **Passo 2: Aguardar conclusão autônoma**

A esteira executa 100% autônoma (REGRA 3). Tempos estimados:

| Fase | Atividade | Tempo estimado |
|------|-----------|----------------|
| 0 | Preparação (slug, db_state) | 1-2 min |
| 1 | Pesquisa + Arquitetura | 5-10 min |
| 2 | Redação paralela (18 capítulos) | 15-30 min |
| 3 | Compilação + PDF | 5-10 min |
| **Total** | | **25-50 min** |

---

## Tarefa 4: Validação Pós-Produção

**Arquivos:** `output/ai-driven-development/livro_final.md`, `output/ai-driven-development/livro_final.pdf`

- [ ] **Passo 1: Verificar existência dos arquivos finais**

```powershell
ls fabrica-de-livros/output/ai-driven-development/livro_final.md
ls fabrica-de-livros/output/ai-driven-development/livro_final.pdf
```

Esperado: Ambos os arquivos existem.

- [ ] **Passo 2: Validar número de capítulos**

```powershell
(Get-ChildItem fabrica-de-livros/output/ai-driven-development/capitulos/).Count
```

Esperado: >= 18

- [ ] **Passo 3: Validar tamanho (caracteres)**

```powershell
(Get-Content fabrica-de-livros/output/ai-driven-development/livro_final.md | Measure-Object -Character).Characters
```

Esperado: >= 175.000

- [ ] **Passo 4: Validar seções EITA em todos os capítulos**

```powershell
Get-ChildItem fabrica-de-livros/output/ai-driven-development/capitulos/*.md | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $nome = $_.Name
    $hasIntro = $content -match "^## 1\. Introdução"
    $hasSecoes = $content -match "^## [2-7]\. "
    Write-Host "$nome - Intro: $hasIntro, Secoes 2-7: $hasSecoes"
}
```

Esperado: Todos com `True`.

- [ ] **Passo 5: Validar referências inline**

```powershell
Select-String "\[\d+\]" fabrica-de-livros/output/ai-driven-development/livro_final.md | Measure-Object
```

Esperado: Múltiplas ocorrências (>= 3 por capítulo = 54+ total).

- [ ] **Passo 6: Validar PDF**

```powershell
$pdf = Get-Item fabrica-de-livros/output/ai-driven-development/livro_final.pdf
Write-Host "Tamanho: $($pdf.Length / 1MB) MB"
```

Esperado: PDF não corrompido, tamanho > 100KB.

---

## Tarefa 5: Relatório Final

**Arquivos:** Nenhum (geração de mensagem)

- [ ] **Passo 1: Gerar relatório de conformidade**

Após validação, exibir:

```
=== LIVRO PRODUZIDO COM SUCESSO ===

Título: AI-Driven Development com OpenCode
Localização: fabrica-de-livros/output/ai-driven-development/

Arquivos:
  - livro_final.md (Markdown)
  - livro_final.pdf (PDF ABNT)

Estatísticas:
  - Capítulos: [N]
  - Caracteres: [N]
  - Páginas estimadas: [N]

Conformidade:
  [✓] R1: 18+ capítulos
  [✓] R2: 70+ páginas
  [✓] R3: 7 seções EITA por capítulo
  [✓] R4: 3+ referências por capítulo
  [✓] R5: 3+ papers no dossiê
  [✓] R6: Formatação ABNT
  [✓] R7: PDF final
  [✓] R8: Tom transformacional
  [✓] R9: Citações inline

Status: APROVADO
```

---

## Casos de Erro

| Erro | Ação |
|------|------|
| Pandoc não encontrado | Instalar: `winget install JohnMacFarlane.Pandoc` |
| Typst não encontrado | Instalar: `winget install Typst.Typst` |
| LLM indisponível | Retry automático (fábrica trata) |
| Capítulo sem referências | compilador-abnt reporta não-conformidade (fábrica corrige) |
| PDF não gerado | Verificar Pandoc/Typst; Markdown ainda é entregue |

---

## Economia de Tokens na Produção

A própria produção obedece às regras de economia:

1. **lean-ctx:** Pesquisador faz grep antes de ler arquivos inteiros
2. **headroom:** Logs de execução comprimidos (3+4)
3. **caveman:** Comunicação entre agentes telegráfica
4. **rtk-memory:** Erros de formatação registrados
5. **pre-flight-check:** Validação de cada capítulo antes de avançar
