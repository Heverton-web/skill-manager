/**
 * ides-config.mjs — Suporte multi-IDE para o Skill Manager
 * 
 * Cada IDE tem:
 * - name: Nome amigável
 * - id: Identificador único
 * - skillsDir: Onde as skills são instaladas
 * - configFile: Arquivo de configuração (se houver)
 * - installCmd: Comando de instalação
 * - removeCmd: Comando de remoção
 * - icon: Emoji/ícone
 * - known: Se é uma IDE conhecida ou genérica
 */

export const IDES = [
  {
    id: "claude-code",
    name: "Claude Code (Anthropic)",
    skillsDir: ".claude/skills",
    configFile: "CLAUDE.md",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🟣",
    known: true,
    description: "Terminal agentic coding tool by Anthropic. Reads CLAUDE.md at project root."
  },
  {
    id: "cursor",
    name: "Cursor (AI Code Editor)",
    skillsDir: ".cursor/rules",
    configFile: ".cursorrules",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🔵",
    known: true,
    description: "AI-first code editor. Supports .cursorrules for project-level instructions."
  },
  {
    id: "windsurf",
    name: "Windsurf (Codeium)",
    skillsDir: ".windsurf/rules",
    configFile: ".windsurfrules",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🌊",
    known: true,
    description: "Agentic IDE by Codeium. Supports .windsurfrules for project config."
  },
  {
    id: "codex",
    name: "Codex CLI (OpenAI)",
    skillsDir: ".codex/skills",
    configFile: "AGENTS.md",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🟢",
    known: true,
    description: "OpenAI's terminal coding agent. Reads AGENTS.md for project instructions."
  },
  {
    id: "antigravity",
    name: "Antigravity CLI",
    skillsDir: ".antigravity/skills",
    configFile: "AGENTS.md",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🔄",
    known: true,
    description: "AI coding CLI by Antigravity. Compatible with Agent Skills standard."
  },
  {
    id: "opencode",
    name: "OpenCode CLI",
    skillsDir: ".opencode/skills",
    configFile: "AGENTS.md",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🔓",
    known: true,
    description: "Open-source AI coding assistant. Supports AGENTS.md standard."
  },
  {
    id: "freebuff",
    name: "Freebuff",
    skillsDir: ".freebuff/skills",
    configFile: "AGENTS.md",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🆓",
    known: true,
    description: "Free AI coding platform by Buffy. Compatible with Agent Skills."
  },
  {
    id: "mimocode",
    name: "MimoCode",
    skillsDir: ".mimocode/skills",
    configFile: "AGENTS.md",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🎯",
    known: true,
    description: "AI coding assistant by mimo.ai. Uses standard Agent Skills format."
  },
  {
    id: "grok",
    name: "Grok (xAI)",
    skillsDir: ".grok/skills",
    configFile: "AGENTS.md",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🧠",
    known: true,
    description: "AI assistant by xAI (Elon Musk). Compatible with Agent Skills ecosystem."
  },
  {
    id: "oh-my-pi",
    name: "Oh My Pi",
    skillsDir: ".ohmy.pi/skills",
    configFile: "AGENTS.md",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🥧",
    known: true,
    description: "AI coding agent platform. Uses standard Agent Skills format."
  },
  {
    id: "cline",
    name: "Cline (VS Code Extension)",
    skillsDir: ".cline/rules",
    configFile: ".clinerules",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🦎",
    known: true,
    description: "Autonomous coding agent VS Code extension. Reads .clinerules."
  },
  {
    id: "github-copilot",
    name: "GitHub Copilot",
    skillsDir: ".github/copilot-instructions.md",
    configFile: ".github/copilot-instructions.md",
    installCmd: (skill) => `echo "GitHub Copilot uses its own skill format"`,
    removeCmd: (skill) => `echo "Remove manually"`,
    listCmd: "echo ",
    icon: "👽",
    known: true,
    description: "AI pair programmer by GitHub. Uses copilot-instructions.md for context."
  },
  {
    id: "custom",
    name: "Custom / Genérico",
    skillsDir: ".agents/skills",
    configFile: "AGENTS.md",
    installCmd: (skill) => `npx skills add ${skill} -y`,
    removeCmd: (skill) => `npx skills remove ${skill}`,
    listCmd: "npx skills list",
    icon: "🔧",
    known: false,
    description: "Para qualquer outra IDE/ferramenta que suporte o padrão Agent Skills."
  }
];

export function getIde(id) {
  return IDES.find(ide => ide.id === id);
}

export function getKnownIdes() {
  return IDES.filter(ide => ide.known);
}

export function getAllIdes() {
  return IDES;
}

// ─── GERAR COMANDO DE INSTALAÇÃO MULTI-IDE ───────────────────────────────
export function generateInstallCommand(ide, skills, scope) {
  const ideConfig = getIde(ide);
  if (!ideConfig) return "";
  const skillStr = skills.join(" ");
  const scopeFlag = scope === "global" ? " -g" : "";
  return `npx skills add ${skillStr} -y${scopeFlag}`;
}

// ─── GERAR CONFIG PARA CADA IDE ──────────────────────────────────────────
export function generateIdeConfig(ide, skills) {
  const ideConfig = getIde(ide);
  if (!ideConfig) return "";
  
  if (ide === "claude-code") {
    return `# Habilidades Instaladas via Skill Manager\n` +
      skills.map(s => `# - ${s}`).join("\n") +
      `\n# Gerado em ${new Date().toISOString()}\n`;
  }
  if (ide === "cursor") {
    return JSON.stringify({ skills: skills }, null, 2);
  }
  return `# ${ideConfig.name} - Skills configuradas\n${skills.map(s => `# - ${s}`).join("\n")}\n`;
}
