# 🛠️ Skill Manager

> Gerenciador Multi-IDE de Agent Skills. Instale, ative, desative e gerencie skills em 13 IDEs com TUI interativa, Dashboard visual e API REST.

## 📦 Instalação

```bash
npm install -g @hevertonperes/skill-manager
# ou
npx @hevertonperes/skill-manager
```

### ⚠️ Resolvendo erros comuns

Se você já instalou uma versão anterior, pode aparecer erro de binário existente:

| Erro | Causa | Solução |
|------|-------|---------|
| `EEXIST: file already exists — sm` | Binário `sm` de instalação anterior | `npm install -g @hevertonperes/skill-manager --force` |
| `EEXIST: file already exists — skill-manager` | Binário `skill-manager` residual | Mesmo comando com `--force` |
| `EPERM: operation not permitted — rmdir enquirer` | Permissão de arquivo no Windows | 🔸 Inofensivo! Ignore o warning |
| `404 Not Found` | CDN do npm propagando | Aguarde 2-5 min ou use `--registry https://registry.npmjs.org` |

**Solução resumida:**
```bash
npm install -g @hevertonperes/skill-manager --force
```

### 🧹 Limpeza prévia (se necessário)

**CMD:**
```cmd
del "%APPDATA%\npm\sm" "%APPDATA%\npm\sm.cmd"
del "%APPDATA%\npm\skill-manager" "%APPDATA%\npm\skill-manager.cmd"
```

**PowerShell:**
```powershell
Remove-Item "$env:APPDATA\npm\sm", "$env:APPDATA\npm\sm.cmd" -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\npm\skill-manager", "$env:APPDATA\npm\skill-manager.cmd" -ErrorAction SilentlyContinue
```

**Linux / Mac:**
```bash
rm -f $(which sm) $(which skill-manager)
```

---

## 🚀 Uso Rápido

```bash
# TUI interativa (5 passos)
sm

# Servidor HTTP com dashboard (toggle real de skills)
sm --serve
# → http://localhost:3030

# Ajuda completa
sm --help
```

Com o servidor rodando, abra `http://localhost:3030` para o painel visual com:
- ✅ Ativar/desativar skills com 1 clique
- ✅ Scoring 0-100 de cada skill
- ✅ Busca por nome
- ✅ Salvar alterações em lote

---

## 🎯 13 IDEs Suportadas

| IDE | Diretório |
|-----|-----------|
| 🟣 Claude Code | `.claude/skills/` |
| 🔵 Cursor | `.cursor/rules/` |
| 🌊 Windsurf | `.windsurf/rules/` |
| 🟢 Codex CLI | `.codex/skills/` |
| 🔄 Antigravity | `.antigravity/skills/` |
| 🔓 OpenCode | `.opencode/skills/` |
| 🆓 Freebuff | `.freebuff/skills/` |
| 🎯 MimoCode | `.mimocode/skills/` |
| 🧠 Grok (xAI) | `.grok/skills/` |
| 🥧 Oh My Pi | `.ohmy.pi/skills/` |
| 🦎 Cline | `.cline/rules/` |
| 👽 GitHub Copilot | `.github/copilot-instructions.md` |
| 🔧 Custom | `.agents/skills/` |

---

## 📊 Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| **TUI Interativa** | 5 passos guiados: IDEs → Skills (com scoring) → Escopo → Dashboard → Submit |
| **Dashboard Visual** | Painel HTML com categorias, toggle switches, busca, progresso |
| **API REST** | `GET /api/config`, `POST /api/toggle`, `POST /api/save`, `GET /api/job/:id` |
| **Instalação Batch** | Fallback triplo: batch completo → sub-lotes → individual |
| **Scoring 0-100** | Qualidade (T1), Capacidade (T2), Complexidade (T3) |
| **482+ Skills** | Catalogadas em 14 categorias |

---

## 🔗 Links

| Recurso | URL |
|---------|-----|
| 📦 npm | https://www.npmjs.com/package/@hevertonperes/skill-manager |
| 💻 GitHub | https://github.com/Heverton-web/skill-manager |
| 📖 Guia completo | https://github.com/Heverton-web/skill-manager/blob/main/SKILL_MANAGER_GUIDE.md |
| 🐛 Issues | https://github.com/Heverton-web/skill-manager/issues |

---

## 📝 Licença

MIT © Heverton Peres
