# 🏭 Monorepo — Fábrica Agêntica de Livros + Skills Manager

Repositório compartilhado contendo dois projetos independentes:

## 📂 Estrutura

```
proj_livros/
├── fabrica-de-livros/     ← Fábrica Agêntica de Livros
├── skills-manager/        ← Skill Manager (npm @hevertonperes/skill-manager)
├── node_modules/          ← Dependências compartilhadas
└── README.md              ← Este arquivo
```

---

## 📚 Fábrica de Livros (`fabrica-de-livros/`)

Indústria gráfica editorial agêntica automatizada para produção de literatura técnica.
Comando principal: `/criar-livro <tema>`

**Para usar:** Abra a pasta `fabrica-de-livros/` no Claude Code (ou outra IDE agêntica) e execute `/criar-livro <tema>`.

Documentação completa: `fabrica-de-livros/CLAUDE.md`, `fabrica-de-livros/SPEC.md`

---

## 🛠️ Skills Manager (`skills-manager/`)

Gerenciador Multi-IDE de Agent Skills. Instale, ative, desative e gerencie skills em 13 IDEs com TUI, Dashboard visual e API REST.

```bash
cd skills-manager
npm install
node scripts/skill-manager.mjs --help
```

Documentação completa: `skills-manager/README.md`, `skills-manager/SKILL_MANAGER_GUIDE.md`

---

## ⚙️ Setup Inicial

### Requisitos
- Node.js >= 18.0.0
- Git

### Instalação de dependências
```bash
npm install
```

### Recriar links entre IDEs (após clone)
```bash
# Windows
powershell -ExecutionPolicy Bypass -File fabrica-de-livros/scripts/setup-links.ps1

# macOS/Linux
bash fabrica-de-livros/scripts/setup-links.sh
```

---

MIT License
