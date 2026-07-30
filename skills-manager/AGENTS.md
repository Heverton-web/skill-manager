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

## Regras

1. ESM (`"type": "module"`)
2. Node.js 18+ (usa `node:test`, `node: readline`)
3. MIT License
4. Publicacao: `@hevertonperes/skill-manager`
