#!/usr/bin/env node
// Adiciona MIRA Animator ao ranking e reorganiza pastas
import { writeFile, copyFile, mkdir, readdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";

const DIR_OUT = path.resolve("output/teste_skills");
const DIR_VISUAL = path.resolve("output/testes_visuais");

const RANKING = [
  { rank: 1, slug: "01_huashu-design",         nome: "huashu-design",         nota: 92, categoria: "Design Completo",       destaque: "Landing page hi-fi, tipografia Newsreader, anti-slop, 40+ estilos" },
  { rank: 2, slug: "02_reversa-selo-generativo", nome: "reversa-selo-generativo", nota: 90, categoria: "Geração de Arte",      destaque: "3 selos generativos seeded p5.js — crystal-lattice, particle-orbit, flow-field" },
  { rank: 3, slug: "03_svg-animations",          nome: "svg-animations",        nota: 88, categoria: "Geração de Arte",      destaque: "Diagrama SVG animado SMIL do ecossistema AIDD" },
  { rank: 4, slug: "04_mira-animator",           nome: "MIRA Animator",        nota: 87, categoria: "Apresentação Animada",  destaque: "Deck animado 5 slides com glassmorphism, metáforas orbitais, Tailwind" },
  { rank: 5, slug: "05_design-taste-frontend",   nome: "design-taste-frontend",  nota: 85, categoria: "Design de Interface",  destaque: "Conceito premium + Design Read anti-slop" },
  { rank: 6, slug: "06_dashi-ppt",               nome: "dashi-ppt",             nota: 80, categoria: "Apresentação",         destaque: "Deck de 5 slides do livro AIDD" },
  { rank: 7, slug: "07_high-end-visual-design",  nome: "high-end-visual-design", nota: 75, categoria: "Guia de Estilo",      destaque: "Diretrizes visuais premium" },
  { rank: 8, slug: "08_reversa-image-prompt-json", nome: "reversa-image-prompt-json", nota: 70, categoria: "Prompt de Imagem", destaque: "Prompt JSON para capa via Midjourney/Flux" },
  { rank: 9, slug: "09_archify",                 nome: "archify",               nota: 60, categoria: "Diagramação Técnica",  destaque: "Diagrama de pipeline (fallback manual)" },
];

const MIRA_ARTEFATOS = [
  { src: "mira/mira_aidd_deck.html", nome: "mira_aidd_deck.html" },
];

async function main() {
  // 1. Gerar ranking markdown
  const linhas = RANKING.map(s => `| ${s.rank} | \`${s.nome}\` | ${s.nota} | ${s.categoria} | ${s.destaque} |`).join("\n");
  const md = `# RANKING DE SKILLS DE DESIGN PARA IMAGENS DE LIVROS
## (Atualizado com MIRA Animator)

**Gerado em:** ${new Date().toISOString().split('T')[0]}

### 🏆 Ranking (9 skills — melhor → pior para imagens de livros)

| # | Skill | Nota | Categoria | Destaque |
|---|-------|------|-----------|----------|
${linhas}

### 🆕 MIRA Animator (87/100) — 4º lugar
- **Categoria:** Apresentação Animada
- **Descrição:** Deck de 5 slides animados com glassmorphism, metáforas SVG orbitais, Tailwind, navegação por teclado
- **Qualidade Visual:** Alta — animações contínuas, glassmorphism, paleta dark premium, metáforas visuais animadas
- **Relevância para Livros:** Alta — apresentação completa do livro AIDD pronta para pitch
- **Complexidade:** Média (39 agentes, requer instalação via npx, pipeline full)
- **Diferencial:** Único framework com 39 agentes especializados (extract, planner, copywriter, builder, animator, 3D, SVG, chart) e pipeline completo de slide deck a vídeo MP4

### 📁 Artefato gerado em \`output/teste_skills/mira/\`
| Arquivo | Skill | Tamanho |
|---------|-------|---------|
| \`mira_aidd_deck.html\` | MIRA Animator | ~5 KB |
`;

  await writeFile(path.join(DIR_OUT, "ranking_design", "RANKING_DESIGN.md"), md, "utf-8");
  console.log("✅ Ranking atualizado com MIRA Animator!");

  // 2. Copiar artefato para a pasta visual numerada
  const slug = "04_mira-animator";
  const dirDest = path.join(DIR_VISUAL, slug);
  await mkdir(dirDest, { recursive: true });

  for (const art of MIRA_ARTEFATOS) {
    const src = path.join(DIR_OUT, art.src);
    const dest = path.join(dirDest, art.nome);
    if (existsSync(src)) {
      await copyFile(src, dest);
      console.log(`  📄 Copiado: ${art.nome}`);
    } else {
      console.log(`  ⚠️  Não encontrado: ${src}`);
    }
  }

  console.log("\n✅ Artefato copiado para", dirDest);
}

main().catch(e => { console.error(e); process.exit(1); });
