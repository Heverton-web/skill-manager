# 🛠️ Skill Manager — Guia Passo a Passo

> Gerencie Agent Skills em 13 IDEs com um comando só.

## 📦 Instalação

### 🔴 Antes de começar

Se você já usou uma versão local do Skill Manager, pode haver **arquivos residuais** no npm global:

```bash
# Limpeza prévia (opcional, mas recomendada)
npm uninstall -g @hevertonperes/skill-manager 2>/dev/null
```

**Windows (CMD):**
```cmd
del "%APPDATA%\npm\sm" "%APPDATA%\npm\sm.cmd"
del "%APPDATA%\npm\skill-manager" "%APPDATA%\npm\skill-manager.cmd"
```

**Windows (PowerShell):**
```powershell
Remove-Item "$env:APPDATA\npm\sm", "$env:APPDATA\npm\sm.cmd" -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\npm\skill-manager", "$env:APPDATA\npm\skill-manager.cmd" -ErrorAction SilentlyContinue
```

**Linux / Mac:**
```bash
rm -f $(which sm) $(which skill-manager)
```

### Opção 1: npm global (recomendado)

```bash
npm install -g @hevertonperes/skill-manager
```

> Se der erro `404 Not Found`, espere 2 minutos e tente de novo (propagação do CDN).
> Alternativa: `npm install -g @hevertonperes/skill-manager --registry https://registry.npmjs.org`

### ⚠️ Resolvendo erros comuns na instalação

| Erro | Causa | Solução |
|------|-------|---------|
| `EEXIST: file already exists — sm` | Binário `sm` de instalação anterior | `npm install -g @hevertonperes/skill-manager --force` |
| `EEXIST: file already exists — skill-manager` | Binário `skill-manager` residual | Mesmo comando com `--force` |
| `EPERM: operation not permitted — rmdir enquirer` | Permissão de arquivo no Windows (pasta lockada) | 🔸 Inofensivo! Ignore o warning. Se insistir, feche terminais abertos e rode como **Admin** |
| `404 Not Found` | CDN do npm ainda propagando | Aguarde 2-5 minutos ou use `--registry https://registry.npmjs.org` |

**Solução resumida para qualquer erro de binário existente:**

```bash
npm install -g @hevertonperes/skill-manager --force
```

O `--force` sobrescreve os binários antigos sem pedir confirmação.

### Opção 2: GitHub

```bash
git clone https://github.com/Heverton-web/skill-manager.git
cd skill-manager
npm install -g .
```

### Opção 3: npx (sem instalar)

```bash
npx @hevertonperes/skill-manager --help
```

---

## 🚀 Primeiros Passos

### 1. Verificar instalação

```bash
sm --help
```

Saída esperada:

```
🛠️  SKILL MANAGER — Gerenciador de Skills Multi-IDE

USO:
  sm                          Inicia TUI interativa
  sm --serve                  Inicia servidor HTTP
  sm --dashboard              Abre dashboard visual
  sm --port=9090              Altera porta do servidor
  sm --help                   Mostra esta ajuda
```

### 2. Iniciar TUI interativa

```bash
sm
```

Fluxo de 5 passos:

| Passo | O que fazer |
|-------|-------------|
| 1. IDEs | Selecione quais IDEs usar (espaço pra marcar, enter pra confirmar) |
| 2. Skills | Escolha categorias → selecione skills individuais (score ≥50 pré-marcadas) |
| 3. Escopo | Local (só este projeto), Global (todas IDEs), ou Ambos |
| 4. Dashboard | ✅ Sim, instalar painel visual |
| 5. Submit | Veja o resumo e confirme |

### 3. Dashboard visual (opcional)

```bash
sm --serve
# → http://localhost:3030
```

O dashboard permite:

- ✅ Ativar/desativar skills com 1 clique (efeito real)
- ✅ Ver scoring 0-100 de cada skill
- ✅ Buscar por nome
- ✅ Salvar alterações em lote

---

## 📋 Cenários de Uso

### 🆕 Projeto Novo

```bash
mkdir meu-projeto && cd meu-projeto
npm install -g @hevertonperes/skill-manager
sm
# → Passo 1: Selecione Claude Code + Cursor
# → Passo 2: Escolha skills de Desenvolvimento + Token Economy
# → Passo 3: Escopo local
# → Passo 5: SUBMIT
```

### 📁 Projeto Existente

```bash
cd meu-projeto-existente
sm
# → O sistema detecta config salva e pergunta:
#   🔄 Reinstalar
#   📊 Abrir Dashboard
#   🖥️ Iniciar Servidor HTTP
#   🚫 Sair
```

### 🖥️ Gestão Contínua (dia a dia)

```bash
# Iniciar servidor de manhã
sm --serve

# Abrir http://localhost:3030 no navegador
# → Ativar skills para a tarefa do dia
# → Desativar skills não utilizadas
# → Clicar "Salvar Todas as Alterações"

# Fim do dia: Ctrl+C no servidor
```

---

## 🔌 API REST

Com o servidor rodando (`sm --serve`):

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Dashboard HTML |
| `/api/config` | GET | JSON com todas skills + estado |
| `/api/toggle` | POST | `{skill, active}` → ativa/desativa |
| `/api/save` | POST | `{activeSkills:[...]}` → salva lote |
| `/api/job/:id` | GET | Poll do resultado do batch |

Exemplo de toggle via curl:

```bash
curl -X POST http://localhost:3030/api/toggle \
  -H "Content-Type: application/json" \
  -d '{"skill":"lean-ctx","active":true}'
```

---

## 🎯 13 IDEs Suportadas

| IDE | Diretório de Skills |
|-----|---------------------|
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

## 📊 Sistema de Scoring

Cada skill recebe um score de **0 a 100**:

| Score | Classificação | Cor |
|-------|--------------|-----|
| ≥ 70 | Excelente | 🟢 Verde |
| 40 — 69 | Boa | 🟡 Amarelo |
| < 40 | Básica | 🔴 Vermelho |

O score é composto por:

- **T1 — Qualidade (0-40)**: frontmatter, descrição, seções, exemplos
- **T2 — Capacidade (0-35)**: frameworks, formatos, scripts, edge cases
- **T3 — Complexidade (0-25)**: tamanho, workflow, metadados, validação

---

## 🏗️ Arquitetura

```
scripts/
├── skill-manager.mjs                   ← Entry point (sm, --serve, --help)
└── skill-manager/
    ├── skill-manager.mjs               ← TUI interativa (5 passos)
    ├── skill-core.mjs                  ← Core: install, batch, score
    ├── ides-config.mjs                 ← 13 IDEs configuradas
    ├── dashboard-server.mjs            ← Servidor HTTP REST
    └── dashboard/
        └── template.html               ← Template do dashboard
```

---

## 🔗 Links Úteis

| Recurso | URL |
|---------|-----|
| 📦 npm | https://www.npmjs.com/package/@hevertonperes/skill-manager |
| 💻 GitHub | https://github.com/Heverton-web/skill-manager |
| 🐛 Issues | https://github.com/Heverton-web/skill-manager/issues |

---

## 📝 Comandos Rápidos

```bash
sm                    # TUI interativa
sm --serve            # Servidor HTTP (localhost:3030)
sm --dashboard        # Dashboard estático
sm --help             # Ajuda
sm --port=9090        # Servidor em porta diferente
```

> ⚡ **Aliases úteis** (adicione no seu `~/.bashrc` ou `$PROFILE` do PowerShell):
> ```bash
> # Bash / ZSH
> alias sm-serve="sm --serve"
> alias sm-dash="sm --dashboard"
> ```
> ```powershell
> # PowerShell (função, porque Set-Alias não aceita argumentos)
> function sm-serve { sm --serve $args }
> function sm-dash { sm --dashboard $args }
> ```
