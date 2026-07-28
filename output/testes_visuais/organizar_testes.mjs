#!/usr/bin/env node

/**
 * organzar_testes.mjs
 * Organiza todos os artefatos dos testes em pastas ranking (01_melhor → 08)
 * e gera um index.html navegável para inspeção visual.
 */

import { mkdir, writeFile, copyFile, readFile } from "node:fs/promises";
import { existsSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const DIR_TEST = path.resolve(DIR, "../teste_skills");
const DIR_RANKING = path.join(DIR_TEST, "ranking_design");

// ─── Ranking oficial (melhor → pior) ──────────────────────────────────────

const RANKING = [
  {
    rank: 1,
    nota: 92,
    slug: "01_huashu-design",
    nome: "huashu-design",
    descricao: "Landing page hi-fi premium — tipografia Newsreader+Inter, grid decorativa, 4 pilares, stats, anti-slop",
    nota_detalhe: "Design completo: 40+ estilos, brand asset protocol, subagentes, animações, vídeo",
    artefatos: [
      { src: path.join(DIR_RANKING, "aidd-huashu-landing.html"), nome: "aidd-huashu-landing.html" },
    ],
  },
  {
    rank: 2,
    nota: 90,
    slug: "02_reversa-selo-generativo",
    nome: "reversa-selo-generativo",
    descricao: "3 selos generativos seeded com p5.js — Cristal, Partículas Orbitais, Campos de Fluxo",
    nota_detalhe: "Arte algorítmica determinística, 3 padrões distintos, tema gold/dark, zero dependências",
    artefatos: [
      { src: path.join(DIR_RANKING, "selo-aidd-crystal-lattice.html"), nome: "selo-aidd-crystal-lattice.html" },
      { src: path.join(DIR_RANKING, "selo-aidd-particle-orbit.html"), nome: "selo-aidd-particle-orbit.html" },
      { src: path.join(DIR_RANKING, "selo-aidd-flow-field.html"), nome: "selo-aidd-flow-field.html" },
    ],
  },
  {
    rank: 3,
    nota: 88,
    slug: "03_svg-animations",
    nome: "svg-animations",
    descricao: "Diagrama SVG animado do ecossistema AIDD — 4 camadas com animações SMIL nativas",
    nota_detalhe: "SVG puro com glow, animações de fluxo, gradientes gold/dark, zero dependências",
    artefatos: [
      { src: path.join(DIR_RANKING, "ecossistema-aidd.svg"), nome: "ecossistema-aidd.svg" },
      { src: path.join(DIR_RANKING, "ecossistema-aidd.html"), nome: "ecossistema-aidd.html" },
    ],
  },
  {
    rank: 4,
    nota: 85,
    slug: "04_design-taste-frontend",
    nome: "design-taste-frontend",
    descricao: "Landing page conceito premium + relatório Design Read com 3 dials configurados",
    nota_detalhe: "Design anti-slop, tipografia Geist, paleta dark+gold, hover states premium",
    artefatos: [
      { src: path.join(DIR_RANKING, "aidd-landing-concept.html"), nome: "aidd-landing-concept.html" },
      { src: path.join(DIR_RANKING, "aidd-design-read.md"), nome: "aidd-design-read.md" },
    ],
  },
  {
    rank: 5,
    nota: 80,
    slug: "05_dashi-ppt",
    nome: "dashi-ppt",
    descricao: "Apresentação HTML em 5 slides — capa dourada, grid de cards, layout responsivo",
    nota_detalhe: "Tema gold/escuro premium, glassmorphism, tipografia serifada, exportável para PPTX/PDF",
    artefatos: [
      { src: path.join(DIR_RANKING, "decks", "aidd-deck.html"), nome: "aidd-deck.html" },
    ],
  },
  {
    rank: 6,
    nota: 75,
    slug: "06_high-end-visual-design",
    nome: "high-end-visual-design",
    descricao: "Guia de estilo visual premium completo — paleta, tipografia, diagramas e anti-padrões",
    nota_detalhe: "Define identidade visual consistente para capa, diagramas, landing page e PDF",
    artefatos: [
      { src: path.join(DIR_RANKING, "guia-estilo-visual-premium.md"), nome: "guia-estilo-visual-premium.md" },
    ],
  },
  {
    rank: 7,
    nota: 70,
    slug: "07_reversa-image-prompt-json",
    nome: "reversa-image-prompt-json",
    descricao: "Prompt JSON estruturado para capa premium — compatível com 4 engines de IA",
    nota_detalhe: "Nano Banana 2, Midjourney, DALL-E, Flux — prompt cinematográfico ultra-detalhado",
    artefatos: [
      { src: path.join(DIR_RANKING, "prompt-capa-aidd-premium.json"), nome: "prompt-capa-aidd-premium.json" },
      { src: path.join(DIR_RANKING, "prompt-capa-aidd-premium.md"), nome: "prompt-capa-aidd-premium.md" },
    ],
  },
  {
    rank: 8,
    nota: 60,
    slug: "08_archify",
    nome: "archify",
    descricao: "Diagrama interativo do pipeline editorial AIDD — 9 estados, 8 transições",
    nota_detalhe: "Diagrama de workflow com fallback manual (CLI não funcionou no Windows)",
    artefatos: [
      { src: path.join(DIR_RANKING, "pipeline-aidd.workflow.html"), nome: "pipeline-aidd.workflow.html" },
      { src: path.join(DIR_RANKING, "pipeline-aidd.workflow.json"), nome: "pipeline-aidd.workflow.json" },
    ],
  },
];

// ─── Main ─────────────────────────────────────────────────────────────────

async function main() {
  console.log("╔══════════════════════════════════════════════════╗");
  console.log("║  ORGANIZANDO TESTES VISUAIS                    ║");
  console.log("╚══════════════════════════════════════════════════╝\n");

  // Cria pastas numeradas para cada skill

  // Para cada skill, cria pasta e copia artefatos
  const cards = [];

  for (const skill of RANKING) {
    const dirSkill = path.join(DIR, skill.slug);
    await mkdir(dirSkill, { recursive: true });

    const medal = skill.rank === 1 ? "🥇" : skill.rank === 2 ? "🥈" : skill.rank === 3 ? "🥉" : `${skill.rank}.`;

    console.log(`${medal} ${skill.slug} (${skill.nota}/100)`);

    // Copia cada artefato
    const arquivos = [];
    for (const art of skill.artefatos) {
      if (existsSync(art.src)) {
        const dest = path.join(dirSkill, art.nome);
        await copyFile(art.src, dest);
        const stat = statSync(dest);
        arquivos.push({ nome: art.nome, path: `${skill.slug}/${art.nome}`, size: stat.size });
        console.log(`  📄 ${art.nome} (${(stat.size / 1024).toFixed(0)} KB)`);
      } else {
        console.log(`  ⚠️  ${art.nome} não encontrado em ${art.src}`);
      }
    }

    cards.push({
      rank: skill.rank,
      nota: skill.nota,
      slug: skill.slug,
      nome: skill.nome,
      descricao: skill.descricao,
      nota_detalhe: skill.nota_detalhe,
      medal,
      arquivos,
      // Usa o primeiro HTML como preview se existir
      preview: arquivos.find(a => a.nome.endsWith(".html")),
    });
  }

  // ─── Gera index.html ──────────────────────────────────────────────────

  const cardHtml = cards.map(c => {      const previewSrc = c.preview ? c.preview.path : "";
      const hasPreview = !!previewSrc;
      const previewTag = hasPreview
        ? `<iframe src="${previewSrc}" class="preview-frame" loading="lazy" onerror="this.style.display='none'"></iframe><p class="click-hint">👆 Clique para abrir</p>`
        : `<div class="no-preview"><span>📄</span><p>Visualizar arquivo diretamente</p></div>`;
      const previewLink = c.preview ? c.preview.path : (c.arquivos[0]?.path || "");

    return `
    <article class="skill-card rank-${c.rank}">
      <div class="card-header">
        <span class="medal">${c.medal}</span>
        <span class="nota">${c.nota}/100</span>
      </div>
      <h2 class="skill-name">${c.nome}</h2>
      <p class="skill-desc">${c.descricao}</p>
      <div class="preview-area">
        <a href="${previewLink}" target="_blank" class="preview-link">
          ${previewTag}
        </a>
      </div>
      <div class="nota-detalhe">${c.nota_detalhe}</div>
      <div class="arquivos">
        <strong>📁 Artefatos:</strong>
        <ul>
          ${c.arquivos.map(a => `<li><a href="${c.slug}/${a.nome}" target="_blank">${a.nome}</a> <span class="size">(${(a.size / 1024).toFixed(0)} KB)</span></li>`).join("")}
        </ul>
      </div>
    </article>
    `;
  }).join("\n");

  const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Testes Visuais — Skills de Design</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Inter', -apple-system, system-ui, sans-serif;
    background: #0b0b12;
    color: #eaeaea;
    min-height: 100vh;
  }
  .container { max-width: 1400px; margin: 0 auto; padding: 2em; }

  /* Header */
  header {
    text-align: center;
    padding: 3em 1em 2em;
    border-bottom: 1px solid #1e1e30;
    margin-bottom: 3em;
  }
  header h1 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: clamp(1.8em, 3.5vw, 2.8em);
    font-weight: 300;
    color: #d4af37;
    letter-spacing: 0.02em;
    margin-bottom: 0.3em;
  }
  header p { color: #8888a0; font-size: 1em; font-weight: 300; }
  header .sub { color: #555; font-size: 0.85em; margin-top: 0.5em; }

  /* Grid */
  .skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 420px), 1fr));
    gap: 2em;
  }

  /* Card */
  .skill-card {
    background: #12121e;
    border: 1px solid #1e1e30;
    border-radius: 16px;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.3s;
    display: flex;
    flex-direction: column;
  }
  .skill-card:hover { border-color: rgba(212,175,55,0.3); transform: translateY(-3px); }
  .skill-card.rank-1 { border-color: rgba(212,175,55,0.5); }
  .skill-card.rank-2 { border-color: rgba(180,180,200,0.3); }
  .skill-card.rank-3 { border-color: rgba(180,120,60,0.3); }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1em 1.5em;
    background: rgba(255,255,255,0.02);
    border-bottom: 1px solid #1e1e30;
  }
  .medal { font-size: 1.5em; }
  .nota {
    font-family: Georgia, serif;
    font-size: 1.1em;
    color: #d4af37;
    font-weight: 500;
  }

  .skill-name {
    font-family: Georgia, serif;
    font-size: 1.2em;
    font-weight: 500;
    color: #eaeaea;
    padding: 0.8em 1.5em 0.3em;
  }
  .skill-desc {
    color: #8888a0;
    font-size: 0.85em;
    line-height: 1.6;
    padding: 0 1.5em 1em;
    font-weight: 300;
  }

  /* Preview */
  .preview-area {
    margin: 0 1em 1em;
    border-radius: 8px;
    overflow: hidden;
    background: #0a0a0f;
    border: 1px solid #1a1a1a;
    position: relative;
  }
  .preview-link { display: block; text-decoration: none; color: inherit; }
  .preview-frame {
    width: 100%;
    height: 280px;
    border: none;
    display: block;
    background: #0a0a0f;
  }
  .click-hint {
    position: absolute;
    bottom: 0;
    left: 0; right: 0;
    text-align: center;
    padding: 0.5em;
    background: linear-gradient(transparent, rgba(0,0,0,0.8));
    color: #d4af37;
    font-size: 0.8em;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s;
  }
  .preview-area:hover .click-hint { opacity: 1; }
  .no-preview {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 120px;
    color: #555;
    gap: 0.5em;
  }
  .no-preview span { font-size: 2em; }
  .no-preview p { font-size: 0.8em; }

  /* Detalhes */
  .nota-detalhe {
    padding: 0 1.5em;
    font-size: 0.8em;
    color: #666;
    line-height: 1.5;
    font-weight: 300;
  }
  .arquivos {
    padding: 1em 1.5em 1.5em;
    font-size: 0.85em;
  }
  .arquivos ul {
    list-style: none;
    margin-top: 0.5em;
  }
  .arquivos li {
    padding: 0.3em 0;
    border-bottom: 1px solid #1a1a1a;
  }
  .arquivos li:last-child { border-bottom: none; }
  .arquivos a {
    color: #d4af37;
    text-decoration: none;
  }
  .arquivos a:hover { text-decoration: underline; }
  .size { color: #555; font-size: 0.85em; }

  /* Footer */
  footer {
    text-align: center;
    padding: 3em;
    border-top: 1px solid #1e1e30;
    margin-top: 3em;
    color: #555;
    font-size: 0.8em;
    font-weight: 300;
  }

  @media (max-width: 768px) {
    .skills-grid { grid-template-columns: 1fr; }
    .preview-frame { height: 200px; }
  }
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>🎨 Testes Visuais — Skills de Design</h1>
    <p>8 skills testadas para geração de imagens e visuais de livros</p>
    <p class="sub">Organizado do melhor (🥇) ao pior (8.) • Clique nos cards para inspecionar</p>
  </header>

  <div class="skills-grid">
    ${cardHtml}
  </div>

  <footer>
    Fábrica Agêntica de Livros • Testes de Skills de Design • ${new Date().toISOString().slice(0, 10)}
  </footer>
</div>
</body>
</html>`;

  const indexPath = path.join(DIR, "index.html");
  await writeFile(indexPath, html, "utf-8");

  console.log(`\n📄 Index navegável: ${indexPath}`);
  console.log(`📁 ${RANKING.length} pastas criadas em ${DIR}/`);
  console.log("\n✅ Pronto! Abra o index.html no navegador para inspecionar.");
}

main().catch(err => {
  console.error("ERRO:", err.message);
  process.exit(1);
});
