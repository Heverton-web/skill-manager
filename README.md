# Monorepo — Projetos Heverton Peres

Repositorio compartilhado contendo tres projetos independentes:

## Estrutura

```
proj_livros/
├── fabrica-de-livros/     ← Fabrica Agentica de Livros
├── skills-manager/        ← Skill Manager (npm)
├── opencode-monitor/      ← Dashboard tempo real OpenCode
└── README.md              ← Este arquivo
```

---

## Fabrica de Livros (`fabrica-de-livros/`)

Industria grafica editorial agentic automatizada para producao de literatura tecnica.
Comando principal: `/criar-livro <tema>`

Documentacao: `fabrica-de-livros/CLAUDE.md`, `fabrica-de-livros/SPEC.md`

---

## Skills Manager (`skills-manager/`)

Gerenciador Multi-IDE de Agent Skills. Instale, ative, desative e gerencie skills em 13 IDEs com TUI, Dashboard visual e API REST.

```bash
cd skills-manager && npm install
node scripts/skill-manager.mjs --help
```

Documentacao: `skills-manager/README.md`, `skills-manager/SKILL_MANAGER_GUIDE.md`

---

## OpenCode Monitor (`opencode-monitor/`)

Dashboard em tempo real para visualizar o fluxo interno do OpenCode (Usuario → Harness → LLM → Tools → Resposta).

```bash
cd opencode-monitor && npm install
npm start
# Abrir http://localhost:7777
```

Documentacao: `opencode-monitor/README.md`

---

## Setup Inicial

### Requisitos
- Node.js >= 18.0.0
- Git

### Instalacao de dependencias
```bash
npm install
```

---

MIT License
