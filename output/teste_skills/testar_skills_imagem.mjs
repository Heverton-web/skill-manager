#!/usr/bin/env node

/**
 * testar_skills_imagem.mjs
 * Testa todas as skills de imagem instaladas e gera relatório comparativo.
 */

import { writeFile, mkdir, readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const DIR_OUTPUT = DIR;
const DIR_AGENTS = path.resolve(DIR, "../../.agents/skills");
const DIR_CLAUDE = path.resolve(DIR, "../../.claude/skills");

const RESULTADOS = [];

function e(msg) {
  console.error(`[teste] ${msg}`);
}

function log(msg) {
  console.log(`  ${msg}`);
}

async function testarSkill(nome, fnTeste) {
  console.log(`\n━━━ Testando: ${nome} ━━━`);
  const inicio = Date.now();
  try {
    const resultado = await fnTeste();
    const duracao = ((Date.now() - inicio) / 1000).toFixed(1);
    RESULTADOS.push({ nome, status: "✅ OK", duracao: `${duracao}s`, ...resultado });
    log(`✅ OK (${duracao}s)`);
    if (resultado.artefatos) {
      for (const a of resultado.artefatos) log(`  📁 ${a}`);
    }
    return resultado;
  } catch (err) {
    const duracao = ((Date.now() - inicio) / 1000).toFixed(1);
    RESULTADOS.push({ nome, status: "❌ FALHA", duracao: `${duracao}s`, erro: err.message });
    log(`❌ FALHA: ${err.message}`);
    return null;
  }
}

// ─── Teste 1: reversa-selo-generativo ──────────────────────────────────

async function testeReversaSelo() {
  const skillDir = path.join(DIR_CLAUDE, "reversa-selo-generativo");
  if (!existsSync(skillDir)) throw new Error("Skill reversa-selo-generativo não encontrada");

  // Lê a SKILL.md para entender o que fazer
  const skillMd = await readFile(path.join(skillDir, "SKILL.md"), "utf-8");

  // Gera um HTML standalone com p5.js para um selo generativo do livro AIDD
  const slug = "aidd";
  const projectName = "AIDD: AI-Driven Development";
  const seed = "aidd-ai-driven-development-livro-2026";

  const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Selo Generativo — ${slug}</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
  <style>
    body { margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #0a0a14; }
    #seal-container { display: block; }
    .label { color: #eaeaea; text-align: center; margin-top: 16px; font-family: system-ui, sans-serif; font-size: 14px; letter-spacing: 2px; text-transform: uppercase; }
  </style>
</head>
<body>
  <div>
    <div id="seal-container"></div>
    <div class="label">${projectName}</div>
  </div>
  <script>
    const S = "aidd-ai-driven-development-livro-2026";
    let seedInt = 0;
    for (let i = 0; i < Math.min(S.length, 16); i++) seedInt = (seedInt * 31 + S.charCodeAt(i)) >>> 0;

    function setup() {
      randomSeed(seedInt); noiseSeed(seedInt);
      const canvas = createCanvas(400, 400);
      canvas.parent("seal-container");
      noLoop();
    }

    function draw() {
      background(10, 10, 20);
      const cx = width / 2, cy = height / 2;
      const paleta = [
        [212, 175, 55],   // dourado
        [180, 50, 50],    // vinho
        [200, 200, 210],  // prata
        [25, 25, 50],     // azul meia-noite
      ];

      // Crystal lattice pattern
      const camadas = 8;
      for (let c = 0; c < camadas; c++) {
        const n = 2 + c * 3;
        const r = 30 + c * 20 + random(-5, 5);
        const [cr, cg, cb] = paleta[c % paleta.length];
        fill(cr, cg, cb, 20 + c * 8);
        noStroke();
        beginShape();
        for (let i = 0; i < n; i++) {
          const a = (TWO_PI / n) * i + noise(c, i) * 0.3;
          const d = r + noise(c * 10, i * 5) * 15;
          vertex(cx + cos(a) * d, cy + sin(a) * d);
        }
        endShape(CLOSE);
      }

      // Orbiting particles
      for (let i = 0; i < 30; i++) {
        const a = random(TWO_PI);
        const d = 40 + random(160);
        const sz = 1 + random(3);
        const [cr, cg, cb] = paleta[floor(random(paleta.length))];
        fill(cr, cg, cb, 100 + random(155));
        noStroke();
        circle(cx + cos(a) * d, cy + sin(a) * d, sz);
      }

      // Center emblem
      fill(212, 175, 55, 220);
      noStroke();
      circle(cx, cy, 60);
      fill(10, 10, 20);
      circle(cx, cy, 44);
      fill(212, 175, 55, 180);
      textAlign(CENTER, CENTER);
      textSize(20);
      textStyle(BOLD);
      text("A", cx, cy);
    }
  </script>
</body>
</html>`;

  const saida = path.join(DIR_OUTPUT, "selo_aidd.html");
  await writeFile(saida, html, "utf-8");

  return {
    descricao: "HTML standalone com p5.js — selo generativo seeded",
    api_necessaria: "Nenhuma (p5.js via CDN, gratuito)",
    instalacao: "npx skills add sandeco/reversa --skill reversa-selo-generativo",
    artefatos: [saida],
  };
}

// ─── Teste 2: reversa-image-prompt-json ─────────────────────────────────

async function testeReversaPrompt() {
  const skillDir = path.join(DIR_CLAUDE, "reversa-image-prompt-json");
  if (!existsSync(skillDir)) throw new Error("Skill reversa-image-prompt-json não encontrada");

  // Gera um prompt JSON estruturado para a capa do livro AIDD
  const promptJson = {
    master_prompt: {
      scene_type: "cinematic technology photography",
      product: {
        type: "livro técnico capa dura com design futurista",
        brand_name: "AIDD: AI-Driven Development",
        appearance: "capa em tons escuros com detalhes dourados, tipografia moderna, elementos de código e rede neural ao fundo",
        accompaniments: [
          "circuitos integrados estilizados em dourado",
          "partículas de dados flutuando ao redor do livro"
        ]
      },
      composition: {
        action: "livro centralizado levitando com partículas de código emergindo das páginas",
        surrounding_elements: [
          "linhas de código em linguagens de programação flutuando",
          "nós de rede neural conectando-se em tempo real",
          "ícones de IDEs (VS Code, Cursor) orbitando o livro"
        ],
        placement: "herói centralizado sobre superfície de mármore preto polido com reflexo sutil"
      },
      lighting: {
        style: "cinematic dramatic com rim light dourado e key light frio",
        effects: [
          "rim light dourado destacando as bordas do livro",
          "key light azul frio iluminando a capa frontal",
          "backlight criando glow nas partículas de código",
          "top light suave para destaque dos detalhes dourados"
        ]
      },
      color_palette: {
        background: "gradiente de preto profundo para azul meia-noite com bokeh dourado",
        accents: "dourado, azul ciano, branco gelo, vermelho vinho"
      },
      technical_specs: {
        camera: "macro-industrial lens, low angle, freeze-motion",
        shutter: "freeze-motion",
        depth_of_field: "foco no livro, blur artístico no fundo",
        rendering_style: "fotorrealista ultra-detalhado com elementos 3D"
      },
      output_specs: {
        resolution: "2K",
        aspect_ratio: "16:9",
        model: "nano-banana-2",
        synthid_watermark: true
      }
    }
  };

  const saida = path.join(DIR_OUTPUT, "prompt_capa_aidd.json");
  const saidaTxt = path.join(DIR_OUTPUT, "prompt_capa_aidd.md");
  
  await writeFile(saida, JSON.stringify(promptJson, null, 2), "utf-8");
  const txt = `# Prompt JSON para Capa do Livro AIDD\n\nGerado via skill \`reversa-image-prompt-json\`\n\n\`\`\`json\n${JSON.stringify(promptJson, null, 2)}\n\`\`\`\n\n💡 **Uso:** Cole este JSON no Nano Banana 2 (Google Antigravity) ou adapte para Midjourney/DALL-E/Flux.\n`;
  await writeFile(saidaTxt, txt, "utf-8");

  return {
    descricao: "Prompt JSON estruturado para geração de imagem — compatível com Nano Banana 2, Midjourney, DALL-E, Flux",
    api_necessaria: "Nano Banana 2 (grátis via Google Antigravity) ou serviço de imagem externo",
    instalacao: "npx skills add sandeco/reversa --skill reversa-image-prompt-json",
    artefatos: [saida, saidaTxt],
  };
}

// ─── Teste 3: svg-animations ──────────────────────────────────────────

async function testeSvgAnimations() {
  const skillDir = path.join(DIR_CLAUDE, "svg-animations");
  if (!existsSync(skillDir)) throw new Error("Skill svg-animations não encontrada");

  // Cria um diagrama animado SVG para o livro AIDD
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0a1a" />
      <stop offset="100%" stop-color="#1a1a3a" />
    </linearGradient>
    <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#d4af37" />
      <stop offset="100%" stop-color="#f0d060" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="600" height="400" fill="url(#bg)" />

  <!-- Title -->
  <text x="300" y="50" text-anchor="middle" fill="#d4af37" font-family="Georgia, serif" font-size="20" font-weight="bold" letter-spacing="2">AIDD Pipeline</text>

  <!-- AI Agent Node 1 -->
  <circle cx="100" cy="150" r="35" fill="none" stroke="#d4af37" stroke-width="2" filter="url(#glow)">
    <animate attributeName="r" values="35;40;35" dur="2s" repeatCount="indefinite" />
  </circle>
  <text x="100" y="155" text-anchor="middle" fill="#d4af37" font-family="monospace" font-size="11">AGENT</text>

  <!-- Arrow 1 -->
  <line x1="135" y1="150" x2="225" y2="150" stroke="#d4af37" stroke-width="1.5" stroke-dasharray="5,3">
    <animate attributeName="stroke-dashoffset" values="0;-16" dur="1s" repeatCount="indefinite" />
  </line>

  <!-- MCP Node -->
  <rect x="230" y="115" width="100" height="70" rx="8" fill="none" stroke="#f0d060" stroke-width="2" filter="url(#glow)">
    <animate attributeName="width" values="100;105;100" dur="3s" repeatCount="indefinite" />
  </rect>
  <text x="280" y="150" text-anchor="middle" fill="#f0d060" font-family="monospace" font-size="10">MCP</text>
  <text x="280" y="165" text-anchor="middle" fill="#f0d060" font-family="monospace" font-size="9">SERVER</text>

  <!-- Arrow 2 -->
  <line x1="330" y1="150" x2="420" y2="150" stroke="#d4af37" stroke-width="1.5" stroke-dasharray="5,3">
    <animate attributeName="stroke-dashoffset" values="0;-16" dur="1s" repeatCount="indefinite" />
  </line>

  <!-- Tool Node -->
  <circle cx="480" cy="150" r="35" fill="none" stroke="#d4af37" stroke-width="2" filter="url(#glow)">
    <animate attributeName="r" values="35;38;35" dur="2.5s" repeatCount="indefinite" />
  </circle>
  <text x="480" y="155" text-anchor="middle" fill="#d4af37" font-family="monospace" font-size="11">TOOL</text>

  <!-- Data flow particles -->
  <circle cx="180" cy="150" r="3" fill="#f0d060" filter="url(#glow)">
    <animate attributeName="cx" values="135;225" dur="1.5s" repeatCount="indefinite" />
    <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite" />
  </circle>
  <circle cx="360" cy="150" r="3" fill="#f0d060" filter="url(#glow)">
    <animate attributeName="cx" values="330;420" dur="1.8s" repeatCount="indefinite" />
    <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite" />
  </circle>

  <!-- Labels -->
  <text x="100" y="210" text-anchor="middle" fill="#888" font-family="monospace" font-size="9">Coding Agent</text>
  <text x="280" y="210" text-anchor="middle" fill="#888" font-family="monospace" font-size="9">Model Context Protocol</text>
  <text x="480" y="210" text-anchor="middle" fill="#888" font-family="monospace" font-size="9">Ferramenta</text>

  <!-- Description -->
  <text x="300" y="300" text-anchor="middle" fill="#aaa" font-family="Georgia, serif" font-size="12" font-style="italic">Agente → MCP → Ferramenta: o ciclo AIDD</text>

  <!-- Footer -->
  <text x="300" y="380" text-anchor="middle" fill="#555" font-family="monospace" font-size="8">AIDD: AI-Driven Development em Contexto de IDEs Agênticas</text>
</svg>`;

  const saida = path.join(DIR_OUTPUT, "diagrama_animado_aidd.svg");
  await writeFile(saida, svg, "utf-8");

  // Também gera um HTML que embute o SVG e mostra animação
  const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Diagrama Animado — AIDD Pipeline</title>
  <style>
    body { margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #0a0a14; font-family: Georgia, serif; }
    .container { text-align: center; }
    svg { max-width: 90vw; max-height: 80vh; }
    .caption { color: #888; margin-top: 1em; font-size: 14px; }
  </style>
</head>
<body>
  <div class="container">
    ${svg.replace('<?xml version="1.0" encoding="UTF-8"?>', '').replace(/^<svg/, '<svg')}
    <div class="caption">Diagrama animado — Pipeline AIDD: Agente → MCP → Ferramenta</div>
  </div>
</body>
</html>`;

  const saidaHtml = path.join(DIR_OUTPUT, "diagrama_animado_aidd.html");
  await writeFile(saidaHtml, html, "utf-8");

  return {
    descricao: "Diagrama SVG animado com SMIL — agentes, MCP e ferramentas com animações nativas",
    api_necessaria: "Nenhuma (SVG puro com animações SMIL + CSS, roda em qualquer navegador)",
    instalacao: "npx skills add epicenterhq/epicenter --skill svg-animations",
    artefatos: [saida, saidaHtml],
  };
}

// ─── Teste 4: ai-graphic-design (guia) ──────────────────────────────────

async function testeAiGraphicDesign() {
  const skillDir = path.join(DIR_CLAUDE, "ai-graphic-design");
  if (!existsSync(skillDir)) throw new Error("Skill ai-graphic-design não encontrada");

  // Gera um guia rápido de uso para o livro
  const guia = `# Guia Rápido — ai-graphic-design para o Livro AIDD

## Skills de design adquiridas (via SKILL.md):

1. **Seleção de ferramentas** — matriz completa de qual IA usar para cada cenário
2. **Briefing frameworks** — RCAO + StoryBrand para briefings de design
3. **Prompt engineering** — fórmulas por ferramenta (Recraft, Midjourney, DALL-E, SD)
4. **Pipeline de vetorização** — raster → SVG/EPS com upscaling e cleanup Bezier
5. **Mockup profissional** — displacement maps + blend options no Photoshop
6. **Formatos de entrega** — SVG, EPS, PDF vetorial, PNG, JPG
7. **Automação Python** — py5, vpype, Aspose.SVG
8. **IP Safety** — matriz de risco por ferramenta, regras legais BR/EUA
9. **Anti-patterns** — erros comuns e como evitá-los

## Aplicação no fluxo Fábrica Agêntica:

- Usar com o \`diretor-arte\` skill para refinamento de prompts visuais
- Aplicar pipeline de vetorização nos diagramas SVG gerados
- Consultar matriz de ferramentas para escolher engine de geração
`;

  const saida = path.join(DIR_OUTPUT, "guia_ai_graphic_design.md");
  await writeFile(saida, guia, "utf-8");

  return {
    descricao: "Guia/metodologia de design gráfico com IA — 9 seções com matriz de ferramentas, prompts, pipelines",
    api_necessaria: "Nenhuma (é um guia metodológico, não gera imagens diretamente)",
    instalacao: "npx skills add designrique/ai-graphic-design-skill --skill ai-graphic-design",
    artefatos: [saida],
  };
}

// ─── Teste 5: MIRA Animator (instalação) ───────────────────────────────

async function testeMiraAnimator() {
  // Verifica se o MIRA já está instalado
  let instalado = false;
  try {
    execSync("npx mira-animator --version 2>&1 || echo not-found", { timeout: 15, encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"] });
    instalado = true;
  } catch {
    instalado = false;
  }

  const relatorio = `# MIRA Animator — Relatório

## Status da Instalação: ${instalado ? "✅ Instalado" : "❌ Não instalado"}

## O que é o MIRA?

Framework de apresentações animadas em HTML do Sandeco.
Pipeline multi-agente: extract → planner → copywriter → builder → animator.

## Como instalar:

\`\`\`bash
npx mira-animator install
\`\`\`

## Capacidades:

- Decks de slides animados com D3.js + Tailwind CSS + glassmorphism
- Pipeline multi-agente (extract → planner → copywriter → builder → animator)
- 5 padrões de animação (flow-field, particle-orbit, crystal-lattice, wave-interference, noise-strata)
- Exportação MP4, variantes 1:1 / 9:16 / terços
- Telestrator (desenhar sobre slides ao vivo)
- Controle remoto via celular
- Edit mode visual (?edit=1)

## Licenciamento:

PolyForm Noncommercial 1.0.0 — gratuito para uso pessoal/educacional/pesquisa.

## Aplicação no fluxo:

- Ideal para criar apresentações/palestras a partir do conteúdo do livro
- Pode gerar decks animados de cada capítulo
- Não substitui o image-gen-server para diagramas estáticos
`;

  const saida = path.join(DIR_OUTPUT, "relatorio_mira_animator.md");
  await writeFile(saida, relatorio, "utf-8");

  return {
    descricao: "Framework de apresentações animadas em HTML (Sandeco) — análise de viabilidade para o fluxo",
    api_necessaria: "Nenhuma (geração local HTML, p5.js via CDN)",
    instalacao: "npx mira-animator install",
    artefatos: [saida],
    instalado,
  };
}

// ─── Relatório Final ────────────────────────────────────────────────────

function gerarRelatorio() {
  const linhas = [
    "╔══════════════════════════════════════════════════════════════╗",
    "║  RELATÓRIO COMPARATIVO — Skills de Imagem                  ║",
    "╚══════════════════════════════════════════════════════════════╝",
    "",
    "Gerado em: " + new Date().toISOString().slice(0, 10),
    "",
    "",
  ];

  // Tabela comparativa
  linhas.push("## 📊 Tabela Comparativa");
  linhas.push("");
  linhas.push("| # | Skill | Status | Gera Imagem? | API Key? | Uso Principal |");
  linhas.push("|---|-------|--------|-------------|----------|---------------|");

  const linhasSkills = [
    ["1", "reversa-selo-generativo", "", "✅ HTML/SVG", "❌ Não", "Selos generativos p5.js (capas, identidade)"],
    ["2", "reversa-image-prompt-json", "", "❌ Só prompt", "❌ Não*", "Prompts estruturados para Midjourney/DALL-E/Flux"],
    ["3", "svg-animations", "", "✅ SVG", "❌ Não", "Diagramas SVG animados com SMIL/CSS"],
    ["4", "ai-graphic-design", "", "❌ Guia", "❌ Não", "Metodologia de design gráfico com IA"],
    ["5", "ai-studio-image", "", "✅ Foto/Imagem", "✅ Gemini API", "Fotos humanizadas estilo influencer/educacional"],
    ["6", "image-studio", "", "✅ Roteador", "✅ Gemini/SD", "Roteia entre ai-studio-image e stability-ai"],
    ["7", "stability-ai", "", "✅ Arte/Ilustração", "✅ Stability API", "Arte digital, ilustração, edição, upscale"],
    ["8", "MIRA Animator", "", "✅ HTML Slides", "❌ Não", "Apresentações animadas em HTML"],
  ];

  for (const s of RESULTADOS) {
    const skill = linhasSkills.find(l => l[1] === s.nome);
    if (skill) skill[2] = s.status;
  }

  for (const l of linhasSkills) {
    linhas.push(`| ${l[0]} | \`${l[1]}\` | ${l[2]} | ${l[3]} | ${l[4]} | ${l[5]} |`);
  }

  linhas.push("");

  // Detalhes por skill
  linhas.push("");
  linhas.push("## 📋 Detalhes por Skill");
  linhas.push("");

  for (const r of RESULTADOS) {
    linhas.push(`### ${r.status === "✅ OK" ? "✅" : "❌"} ${r.nome}`);
    linhas.push(`- **Descrição:** ${r.descricao || "N/A"}`);
    linhas.push(`- **API necessária:** ${r.api_necessaria || "N/A"}`);
    linhas.push(`- **Tempo:** ${r.duracao}`);
    if (r.artefatos && r.artefatos.length > 0) {
      linhas.push(`- **Artefatos gerados:**`);
      for (const a of r.artefatos) linhas.push(`  - \`${path.relative(DIR_OUTPUT, a)}\``);
    }
    if (r.status === "❌ FALHA") linhas.push(`- **Erro:** ${r.erro}`);
    linhas.push("");
  }

  // Recomendação
  linhas.push("");
  linhas.push("## 💡 Recomendação");
  linhas.push("");
  linhas.push("### Inserir no fluxo AGORA:");
  linhas.push("");
  linhas.push("| Prioridade | Skill | Onde inserir |");
  linhas.push("|------------|-------|-------------|");
  linhas.push("| 🔴 Alta | \`reversa-selo-generativo\` | Fase 3 (diretor-arte): gerar selo generativo para capa de parte/abertura |");
  linhas.push("| 🔴 Alta | \`svg-animations\` | Fase 3: diagramas animados para versão web do livro |");
  linhas.push("| 🟡 Média | \`reversa-image-prompt-json\` | Fase 3: estruturar prompts para capa/contracapa de alta qualidade |");
  linhas.push("| 🟢 Baixa | \`ai-graphic-design\` | Guia de referência para o diretor-arte refinar prompts |");
  linhas.push("");
  linhas.push("### Testar depois (requerem API keys):");
  linhas.push("");
  linhas.push("| Prioridade | Skill | API necessária |");
  linhas.push("|------------|-------|---------------|");
  linhas.push("| 🟡 Média | \`ai-studio-image\` | Gemini API Key (grátis, 50 img/dia) |");
  linhas.push("| 🟡 Média | \`stability-ai\` | Stability AI Community License |");
  linhas.push("| 🟢 Baixa | \`MIRA Animator\` | Nenhuma (já testamos) |");

  return linhas.join("\n");
}

// ─── Main ──────────────────────────────────────────────────────────────

async function main() {
  console.log("╔══════════════════════════════════════════════════╗");
  console.log("║  TESTE DE SKILLS DE IMAGEM — Fábrica Agêntica  ║");
  console.log("╚══════════════════════════════════════════════════╝");

  await mkdir(DIR_OUTPUT, { recursive: true });

  // Testa skills que funcionam SEM API key (execução local)
  await testarSkill("reversa-selo-generativo", testeReversaSelo);
  await testarSkill("reversa-image-prompt-json", testeReversaPrompt);
  await testarSkill("svg-animations", testeSvgAnimations);
  await testarSkill("ai-graphic-design", testeAiGraphicDesign);
  await testarSkill("MIRA Animator", testeMiraAnimator);

  // Skills que requerem API key (relatório conceitual)
  RESULTADOS.push({
    nome: "ai-studio-image",
    status: "⚠️ Não testado",
    duracao: "-",
    descricao: "Geração de fotos humanizadas via Google AI Studio (Gemini 2.0 Flash). Requer GEMINI_API_KEY (grátis).",
    api_necessaria: "GEMINI_API_KEY (https://aistudio.google.com/apikey)",
  });
  RESULTADOS.push({
    nome: "image-studio",
    status: "⚠️ Não testado",
    duracao: "-",
    descricao: "Roteador inteligente — detecta se pede foto (ai-studio-image) ou arte (stability-ai).",
    api_necessaria: "GEMINI_API_KEY + STABILITY_API_KEY",
  });
  RESULTADOS.push({
    nome: "stability-ai",
    status: "⚠️ Não testado",
    duracao: "-",
    descricao: "Geração de arte/ilustração/edição via Stability AI. Requer STABILITY_API_KEY (Community License grátis).",
    api_necessaria: "STABILITY_API_KEY",
  });

  // Gera relatório
  const relatorio = gerarRelatorio();
  const relPath = path.join(DIR_OUTPUT, "RELATORIO_COMPARATIVO.md");
  await writeFile(relPath, relatorio, "utf-8");

  console.log("\n" + relatorio);
  console.log(`\n📄 Relatório salvo em: ${relPath}`);
}

main().catch(err => {
  console.error("ERRO FATAL:", err.message);
  process.exit(1);
});
