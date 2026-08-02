# CLAUDE.md — Skills Manager

## O que e

Gerenciador Multi-IDE de Agent Skills. Instala, ativa, desativa e gerencia skills em 13 IDEs com TUI, Dashboard visual e API REST.

## Como usar

```bash
npm install
node scripts/skill-manager.mjs --help
```

## IDEs suportadas

Claude Code, Cursor, Windsurf, Codex CLI, Antigravity, OpenCode, Freebuff, MimoCode, Grok, Oh My Pi, Cline, GitHub Copilot, Custom

## Comandos

| Comando | O que faz |
|---------|-----------|
| `sm` | TUI interativa |
| `sm --serve` | Dashboard na porta 3030 |
| `sm --help` | Ajuda |

## Estrutura

```
scripts/
  skill-manager.mjs      # CLI principal
  skill-manager/          # Modulos internos
default-skills/           # Skills padrao
```

## Regras de Economia Severa de Tokens (Prioridade Máxima)

1. **Estilo Caveman Ativo:** Pensamento em formato telegráfico (máx 3-5 linhas). Comunicação sem preâmbulos, saudações ou palavras vazias. Preservar termos técnicos e idioma PT-BR.
2. **Compressão Headroom & RTK:** Todo log, JSON ou output > 7 linhas DEVE ser comprimido via `headroom` (topo 3 + fim 4) e filtrado via `rtk`.
3. **Seleção Cirúrgica (LeanCTX):** Usar `grep_search` antes de abrir arquivos e limitar a leitura por linha (`StartLine`/`EndLine`).
4. **Subagentes Cavecrew:** Usar a skill `cavecrew` para buscas ou edições extensas.

## Regras

- Node.js 18+
- Publicacao npm: `@hevertonperes/skill-manager`
- MIT License
