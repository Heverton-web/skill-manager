#!/usr/bin/env node
/**
 * extrair-selo-svg.mjs
 * Gera versões SVG estáticas de selos generativos p5.js.
 * Usa o mesmo algoritmo seeded determinístico — sem dependências externas.
 *
 * Uso: node scripts/extrair-selo-svg.mjs <slug> <parte>
 * Ex: node scripts/extrair-selo-svg.mjs aidd-v2 I
 *
 * Saída: output/<slug>/imagens/selo_parte_<parte>.svg
 */

import { readFile, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { createHash, randomInt } from "node:crypto";

// ─── Gerador de números pseudo-aleatórios seeded (LCG) ──────────────
function createSeededRandom(seed) {
  let state = BigInt(seed) % (1n << 32n);
  if (state === 0n) state = 1n;
  const a = 1103515245n, c = 12345n, m = 1n << 31n;
  return {
    next() {
      state = (a * state + c) % m;
      return Number(state) / 2147483648;
    },
    nextInt(min, max) {
      return Math.floor(this.next() * (max - min + 1)) + min;
    },
    nextFloat(min, max) {
      return this.next() * (max - min) + min;
    },
    pick(arr) {
      return arr[Math.floor(this.next() * arr.length)];
    },
  };
}

// ─── Hash SHA-256 para gerar seed numérico ───────────────────────────
function hashSeed(input) {
  return createHash("sha256").update(input).digest("hex");
}

function hashToInt(hex) {
  return parseInt(hex.slice(0, 16), 16);
}

// ─── Paletas por estilo ──────────────────────────────────────────────
const PALETAS = {
  sober:        ["#6b7280", "#5a7d8a", "#c4735a", "#f5f0e8"],
  premium:      ["#0a0a0a", "#c9a84c", "#6b2020", "#c0c0c0", "#1a2744"],
  dense:        ["#ff6b35", "#00b4d8", "#e91e63", "#7cda24", "#3f37c9"],
  exploratory:  ["#ff8fa3", "#7ae0d4", "#c8b6ff", "#f8f4f0"],
};

// ─── Geradores de padrões SVG ───────────────────────────────────────

function gerarCrystalLattice(rng, cx, cy, size, paleta) {
  const linhas = [];
  const camadas = 6;
  const raioBase = size * 0.08;
  const incremento = (size * 0.38) / camadas;
  linhas.push(`<g stroke-width="1.5" fill-opacity="0.1">`);
  for (let layer = 1; layer <= camadas; layer++) {
    const nVerts = 5 + layer * 2;
    const raio = raioBase + layer * incremento + rng.nextFloat(-6, 6);
    const cor = paleta[layer % paleta.length];
    const pts = [];
    for (let i = 0; i < nVerts; i++) {
      const ang = (2 * Math.PI * i) / nVerts + rng.nextFloat(-0.12, 0.12);
      const r = raio + rng.nextFloat(-10, 10);
      pts.push([cx + Math.cos(ang) * r, cy + Math.sin(ang) * r]);
    }
    // Polígono
    linhas.push(`<polygon points="${pts.map(p => p.map(v => v.toFixed(1)).join(",")).join(" ")}" fill="${cor}" stroke="${cor}" />`);
    // Conexões radiais da camada anterior
    if (layer > 1) {
      const raioAnt = raioBase + (layer - 1) * incremento;
      for (let i = 0; i < nVerts; i++) {
        const ang = (2 * Math.PI * i) / nVerts;
        const x1 = cx + Math.cos(ang) * raioAnt;
        const y1 = cy + Math.sin(ang) * raioAnt;
        const r2 = raio + rng.nextFloat(-10, 10);
        const x2 = cx + Math.cos(ang + 0.05) * (raio - 10);
        const y2 = cy + Math.sin(ang + 0.05) * (raio - 10);
        linhas.push(`<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${cor}" stroke-opacity="0.4" />`);
      }
    }
  }
  linhas.push(`</g>`);
  // Círculo central
  linhas.push(`<circle cx="${cx}" cy="${cy}" r="8" fill="${paleta[0]}" />`);
  return linhas.join("\n");
}

function gerarParticleOrbit(rng, cx, cy, size, paleta) {
  const partes = 60;
  const linhas = [`<g stroke-width="1" fill-opacity="0.9">`];
  for (let i = 0; i < partes; i++) {
    const ang = rng.nextFloat(0, 2 * Math.PI);
    const raio = rng.nextFloat(12, size * 0.42);
    const x = cx + Math.cos(ang + 0.5) * raio;
    const y = cy + Math.sin(ang + 0.5) * raio;
    const cor = paleta[i % paleta.length];
    const r = rng.nextFloat(1.5, 4);
    linhas.push(`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r.toFixed(1)}" fill="${cor}" />`);
    // Trilha
    const tx = cx + Math.cos(ang + 0.5 - 0.08) * (raio + rng.nextFloat(-6, 6));
    const ty = cy + Math.sin(ang + 0.5 - 0.08) * (raio + rng.nextFloat(-6, 6));
    linhas.push(`<line x1="${x.toFixed(1)}" y1="${y.toFixed(1)}" x2="${tx.toFixed(1)}" y2="${ty.toFixed(1)}" stroke="${cor}" stroke-opacity="0.3" />`);
  }
  linhas.push(`</g>`);
  for (let i = 0; i < 3; i++) {
    const r = 40 + i * 30;
    linhas.push(`<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${paleta[0]}" stroke-opacity="0.15" stroke-width="1" />`);
  }
  return linhas.join("\n");
}

function gerarFlowField(rng, cx, cy, size, paleta) {
  const linhas = [`<g stroke-width="1.5" fill="none" stroke-opacity="0.6">`];
  const nLinhas = 25;
  for (let i = 0; i < nLinhas; i++) {
    const x0 = rng.nextFloat(size * 0.1, size * 0.9);
    const y0 = rng.nextFloat(size * 0.1, size * 0.9);
    const cor = paleta[i % paleta.length];
    let pts = [];
    let x = x0, y = y0;
    for (let passo = 0; passo < 20; passo++) {
      pts.push(`${x.toFixed(1)},${y.toFixed(1)}`);
      const ang = rng.nextFloat(0, 2 * Math.PI) + Math.sin(passo * 0.5) * 0.5;
      x += Math.cos(ang) * 8;
      y += Math.sin(ang) * 8;
      if (x < 5 || x > size - 5 || y < 5 || y > size - 5) break;
    }
    if (pts.length > 1) {
      linhas.push(`<polyline points="${pts.join(" ")}" stroke="${cor}" />`);
    }
  }
  linhas.push(`</g>`);
  return linhas.join("\n");
}

function gerarWaveInterference(rng, cx, cy, size, paleta) {
  const linhas = [`<g fill="none" stroke-opacity="0.25">`];
  const nOndas = 12;
  for (let i = 0; i < nOndas; i++) {
    const raioBase = rng.nextFloat(10, size * 0.45);
    const cor = paleta[i % paleta.length];
    const nAneis = rng.nextInt(3, 7);
    for (let a = 0; a < nAneis; a++) {
      const r = raioBase + a * (size * 0.04 + rng.nextFloat(2, 8));
      if (r > size * 0.48) break;
      linhas.push(`<circle cx="${cx}" cy="${cy}" r="${r.toFixed(1)}" stroke="${cor}" stroke-width="${(0.5 + rng.nextFloat(0, 1.5)).toFixed(1)}" />`);
    }
  }
  linhas.push(`</g>`);
  return linhas.join("\n");
}

function gerarNoiseStrata(rng, cx, cy, size, paleta) {
  const linhas = [`<g stroke-width="1.5" fill="none">`];
  const nCamadas = 15;
  for (let i = 0; i < nCamadas; i++) {
    const yBase = (size / (nCamadas + 1)) * (i + 1) + rng.nextFloat(-8, 8);
    const cor = paleta[i % paleta.length];
    const pts = [];
    for (let x = 0; x <= size; x += 6) {
      const y = yBase + Math.sin(x * 0.02 + i * 1.5) * (8 + rng.nextFloat(-4, 4)) + Math.sin(x * 0.05 + i) * 4;
      pts.push(`${x.toFixed(1)},${y.toFixed(1)}`);
    }
    linhas.push(`<polyline points="${pts.join(" ")}" stroke="${cor}" stroke-opacity="${(0.15 + i * 0.04).toFixed(2)}" />`);
  }
  linhas.push(`</g>`);
  return linhas.join("\n");
}

const GERADORES = {
  "crystal-lattice": gerarCrystalLattice,
  "particle-orbit": gerarParticleOrbit,
  "flow-field": gerarFlowField,
  "wave-interference": gerarWaveInterference,
  "noise-strata": gerarNoiseStrata,
};

const PADROES = Object.keys(GERADORES);

// ─── Função principal ────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error("Uso: node scripts/extrair-selo-svg.mjs <slug> <parte> [--padrao <padrao>] [--estilo <estilo>]");
    process.exit(1);
  }

  const slug = args[0];
  const parte = args[1];
  const padraoOverride = args.indexOf("--padrao") !== -1 ? args[args.indexOf("--padrao") + 1] : null;
  const estiloOverride = args.indexOf("--estilo") !== -1 ? args[args.indexOf("--estilo") + 1] : null;

  // Seed deve ser IDENTICO ao usado pelo subagente-design-por-parte:
  // sha256(slug + "parte" + parte_atual) — sem separadores
  const seedStr = `${slug}parte${parte}`;
  const seedHex = hashSeed(seedStr);
  const seedInt = hashToInt(seedHex);
  const rng = createSeededRandom(seedInt);

  // Seleciona padrão pelo seed (primeiros 2 dígitos hex mod 5)
  const padrao = padraoOverride || PADROES[parseInt(seedHex.slice(0, 2), 16) % PADROES.length];
  const estilo = estiloOverride || rng.pick(["premium", "sober", "dense", "exploratory"]);
  const paleta = PALETAS[estilo];

  const size = 400;
  const cx = size / 2, cy = size / 2;

  const gerador = GERADORES[padrao];
  if (!gerador) {
    console.error(`Padrão desconhecido: ${padrao}. Opções: ${PADROES.join(", ")}`);
    process.exit(1);
  }

  const bg = estilo === "premium" || estilo === "dense" ? "#0a0a14" : "#0f0f1a";
  const conteudo = gerador(rng, cx, cy, size, paleta);

  const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" width="${size}" height="${size}">
  <rect width="${size}" height="${size}" fill="${bg}" rx="8" />
  ${conteudo}
</svg>`;

  const dirSaida = path.resolve("output", slug, "imagens");
  const caminho = path.join(dirSaida, `selo_parte_${parte}.svg`);

  await writeFile(caminho, svg, "utf-8");
  console.log(`✅ SVG gerado: ${caminho}`);
  console.log(`   Seed: ${seedHex.slice(0, 16)}...`);
  console.log(`   Padrão: ${padrao}`);
  console.log(`   Estilo: ${estilo}`);
  console.log(`   Tamanho: ${svg.length} bytes`);
}

main().catch((err) => {
  console.error("Erro:", err);
  process.exit(1);
});
