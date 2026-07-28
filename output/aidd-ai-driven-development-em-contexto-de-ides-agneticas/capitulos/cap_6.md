# Capítulo 6 — O Padrão AGENTS.md e a Portabilidade Multi-IDE

Um dos maiores desafios práticos de quem adota coding agents é a fragmentação de configurações. Cada ferramenta — Claude Code, Cursor, Windsurf, Cline, Copilot — tem seu próprio formato de arquivo de instruções. Manter todos sincronizados é um pesadelo logístico.

O AGENTS.md emergiu como a resposta da indústria para esse problema: um padrão aberto, multi-ferramenta, para instruções de projeto que qualquer agente de IA entende.

## AGENTS.md como padrão aberto multi-ferramenta

### A origem

No início de 2025, cada ferramenta de IA tinha seu próprio formato proprietário. Cursor usava `.cursorrules` (arquivo único de regras), Claude Code usava `CLAUDE.md`, Windsurf usava `.windsurfrules`, e assim por diante. Desenvolvedores que usavam múltiplas ferramentas precisavam manter cópias do mesmo conteúdo em formatos diferentes — um convite à dessincronização.

OpenAI, Cursor, Zed, Sourcegraph e Aider se uniram para criar o padrão **AGENTS.md**: um arquivo Markdown na raiz do repositório que qualquer agente de IA lê automaticamente para entender as regras do projeto.

### O que deve conter

O AGENTS.md não é um arquivo para humanos — é para agentes. Portanto, deve ser:

- **Conciso:** 500-2000 tokens idealmente (não ultrapassar 4000)
- **Estruturado:** Seções claras para rápida recuperação
- **Executável:** Instruções que o agente possa seguir deterministicamente

![AGENTS.md como hub central conectando múltiplas ferramentas](../imagens/cap_6_diagrama_1.svg)

Seções recomendadas:
1. **Visão geral do projeto:** O que é, stack principal, arquitetura
2. **Comandos de setup:** Como instalar dependências, configurar ambiente
3. **Estilo de código:** Convenções, padrões, guias
4. **Testes:** Como rodar, o que cobrir, ferramentas
5. **Diretrizes de PR:** Título, descrição, revisão
6. **Segurança:** Restrições, o que não fazer

![AGENTS.md como hub central conectando múltiplas ferramentas](../imagens/cap_6_diagrama_1.svg)

### Exemplo de AGENTS.md

```markdown
# MeuProjeto

Stack: Next.js 15 + Prisma + PostgreSQL + Tailwind
Arquitetura: App Router, Server Components por padrão,
             Client Components apenas quando necessário

## Setup
- `pnpm install` para instalar
- `pnpm dev` para desenvolvimento
- `pnpm build` para build de produção

## Estilo
- TypeScript estrito, sem `any`
- Componentes em `src/components/`, páginas em `src/app/`
- Testes com Vitest em arquivos `*.test.ts` ao lado do componente
- Nomes em inglês, camelCase para funções, PascalCase para componentes

## Regras
- SEMPRE execute `pnpm lint --fix` antes de concluir qualquer task
- NUNCA modifique `prisma/schema.prisma` sem aprovação explícita
- Testes unitários obrigatórios para toda função utilitária
- Coverage mínimo: 80%
```

## Estratégias de sincronia entre ambientes

### O problema da fragmentação

Desenvolvedores usam múltiplas ferramentas. Num mesmo dia, um desenvolvedor pode usar Claude Code (CLI) para refatoração pesada, Cursor para edição visual e GitHub Copilot para tarefas rápidas. Cada ferramenta lê um arquivo de regras diferente.

A solução não é duplicar — é criar uma única fonte da verdade com links.

### Hardlinks (Windows e Unix)

Hardlinks são entradas de diretório que apontam para o mesmo inode (mesmo conteúdo físico). Um arquivo com hardlinks é um único arquivo que aparece em múltiplos caminhos. Editar um caminho edita todos.

```
CLAUDE.md ──── hardlink ────→ AGENTS.md (mesmo inode)
.cursor/rules/project.mdc ── hardlink ────→ AGENTS.md
```

### Symlinks e Junctions

- **Symlinks (macOS/Linux):** Referências simbólicas a outro caminho. O sistema operacional resolve automaticamente. Útil para compatibilidade com ferramentas que esperam caminhos específicos.
- **Junctions (Windows):** Equivalentes a symlinks para diretórios. Permitem que uma pasta como `agentic/skills` aponte para `.claude/skills`.

### Scripts de setup automáticos

Como `git clone` não preserva hardlinks (eles viram arquivos independentes), scripts de setup são necessários. Exemplo de script PowerShell:

```powershell
# setup-links.ps1
New-Item -ItemType HardLink -Path "AGENTS.md" -Target "CLAUDE.md"
New-Item -ItemType Junction -Path "agentic/skills" -Target ".claude/skills"
```

Isso garante que o repositório clonado recrie a estrutura de links automaticamente.

![Arquitetura de links entre arquivos de regras](../imagens/cap_6_diagrama_2.svg)

![Arquitetura de links entre arquivos de regras](../imagens/cap_6_diagrama_2.svg)

### Sincronia de configurações MCP

Além dos arquivos de regras, as configurações dos servidores MCP precisam ser sincronizadas entre ferramentas. O schema do VS Code (`servers` + `type: "stdio"`) é diferente do schema do Claude Code (`mcpServers`). Scripts de conversão automática resolvem isso:

```javascript
// sync-vscode-mcp.mjs
// Lê .mcp.json (schema Claude Code) e gera .vscode/mcp.json (schema VS Code)
```

## Skills, MDC rules e instruções modulares

### O limite do AGENTS.md

O AGENTS.md funciona bem para regras globais do projeto, mas não escala para regras específicas de módulos ou domínios. Inchar o AGENTS.md com regras de todos os módulos quebra a regra de 500-2000 tokens.

### MDC rules (Cursor)

O Cursor substituiu o monolítico `.cursorrules` por um diretório estruturado de arquivos MDC (Markdown com frontmatter YAML). Cada regra pode ter um escopo definido por glob pattern:

```yaml
# .cursor/rules/react-components.mdc
---
description: Regras para componentes React
globs: "src/components/**/*.tsx"
---
Sempre usar Server Components por padrão.
Client Components apenas quando interatividade é necessária.
```

![Hierarquia de regras: global → diretório → skill específica](../imagens/cap_6_diagrama_3.svg)

### Skills (Claude Code)

Skills são pastas modulares com instruções detalhadas que o agente carrega sob demanda. Diferente do AGENTS.md (sempre carregado), as skills só entram no contexto quando o desenvolvedor as invoca explicitamente.

Vantagens do sistema modular:
1. **AGENTS.md enxuto:** Apenas regras globais e essenciais
2. **Regras por diretório:** Aplicam-se automaticamente quando o agente navega para aquele diretório
3. **Skills sob demanda:** Conhecimento especializado carregado apenas quando necessário

![Hierarquia de regras: global → diretório → skill específica](../imagens/cap_6_diagrama_3.svg)

---

Neste capítulo, vimos como o AGENTS.md se tornou o padrão aberto para instruções portáteis, as estratégias de sincronia entre ambientes via hardlinks e scripts de setup, e a arquitetura modular de regras com MDC e Skills. No próximo capítulo, mergulharemos no Model Context Protocol (MCP), o protocolo que conecta agentes a ferramentas externas.
