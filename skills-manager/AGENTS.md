---
description: Instrucoes para agentes de IA trabalhando no Skills Manager
alwaysApply: true
---

# AGENTS.md — Skills Manager

## Contexto

Gerenciador Multi-IDE de Agent Skills. Permite instalar, ativar, desativar e gerencie skills em 13 IDEs diferentes com uma unica CLI.

## Stack

- Node.js 18+ (ESM)
- Enquirer (TUI interativa)
- Sem framework web (dashboard puro)

## Comandos

```bash
node scripts/skill-manager.mjs       # TUI
node scripts/skill-manager.mjs --serve  # Dashboard :3030
npm test                              # (se houver)
```

## Estrutura

```
scripts/
  skill-manager.mjs      # CLI entry point
  skill-manager/          # Core logic
default-skills/           # Built-in skills
```

## Regras e Economia Severa de Tokens

1. **Estilo Caveman Ativo:** Pensamento em formato telegráfico (máx 3-5 linhas). Comunicação sem preâmbulos, saudações ou palavras vazias. Preservar termos técnicos e idioma PT-BR.
2. **Compressão Headroom & RTK:** Todo log, JSON ou output > 7 linhas DEVE ser comprimido via `headroom` (topo 3 + fim 4) e filtrado via `rtk`.
3. **Seleção Cirúrgica (LeanCTX):** Usar `grep_search` antes de abrir arquivos e limitar a leitura por linha (`StartLine`/`EndLine`).
4. **Subagentes Cavecrew:** Usar a skill `cavecrew` para buscas ou edições extensas.
5. **ESM** (`"type": "module"`).
6. **Node.js 18+** (usa `node:test`, `node:readline`).
7. **MIT License**.
8. **Publicação:** `@hevertonperes/skill-manager`.
