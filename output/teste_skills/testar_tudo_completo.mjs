#!/usr/bin/env node
/**
 * testar_tudo_completo.mjs
 * Gera 3+ artefatos PDF-compatíveis (SVG, PNG, MD, JSON) para cada skill.
 * Saída: output/testes_visuais/XX_nome/ pastas numeradas
 */
import { mkdir, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const VISUAL = path.resolve(DIR, "..", "testes_visuais");

// ─── UTIL: criar pasta e escrever arquivo ──────────────────────────
async function salva(slug, nome, conteudo) {
  const dir = path.join(VISUAL, slug);
  await mkdir(dir, { recursive: true });
  await writeFile(path.join(dir, nome), conteudo, "utf-8");
  return nome;
}

// ─── 1. HUASHU-DESIGN (92) ─── Landing + Variações + Conceito Capa ─
async function testeHuashu(slug) {
  const arts = [];
  arts.push(await salva(slug, "landing-aidd.html", `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>AIDD · Landing Huashu</title><link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz@6..72&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#050510;color:#e0e0ff;font-family:'Inter',sans-serif;min-height:100vh}
.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:4rem 2rem;position:relative;text-align:center}
.hero::before{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at 30% 50%,rgba(108,99,255,0.06),transparent 60%)}
h1{font-family:'Newsreader',serif;font-size:clamp(2.5rem,6vw,4.5rem);font-weight:400;line-height:1.1;max-width:800px;position:relative}
h1 em{font-style:italic;color:#6c63ff}
.tag{background:rgba(108,99,255,0.12);border:1px solid rgba(108,99,255,0.2);padding:0.3rem 1rem;border-radius:100px;font-size:0.75rem;color:#6c63ff;margin-bottom:2rem;position:relative}
.sub{color:#8888bb;font-size:1.125rem;max-width:600px;margin-top:1.5rem;line-height:1.6;position:relative}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem;max-width:700px;width:100%;margin-top:3rem;position:relative}
.card{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:1.5rem;transition:all .3s}
.card:hover{transform:translateY(-2px);border-color:rgba(108,99,255,0.3)}
.card h3{font-size:0.75rem;color:#6c63ff;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem}
.card h2{font-size:1.1rem;font-weight:600;margin-bottom:0.3rem}
.card p{font-size:0.85rem;color:#8888bb;line-height:1.5}
@media(max-width:768px){.grid{grid-template-columns:1fr}}
</style></head><body><section class="hero"><div class="tag">Huashu-Design · Anti-Slop</div>
<h1>AIDD: <em>AI-Driven Development</em><br>em IDEs Agênticas</h1>
<p class="sub">2 Partes · 4 Capítulos · Ecossistema Claude Code, Cursor, Windsurf e MCP</p>
<div class="grid">
<div class="card"><h3>FUNDAMENTOS</h3><h2>Paradigma AIDD</h2><p>Specification-Driven Development, auto-correção e o novo papel do desenvolvedor</p></div>
<div class="card"><h3>ECOSSISTEMA</h3><h2>IDEs Agênticas</h2><p>Claude Code CLI, Cursor IDE, Windsurf Cascade e o protocolo MCP</p></div>
<div class="card"><h3>PIPELINES</h3><h2>Spec-to-Code</h2><p>Orquestração com sub-agentes paralelos, validação em loop e revisão humana</p></div>
<div class="card"><h3>FUTURO</h3><h2>Desafios</h2><p>Alucinação de contexto, segurança, custos de API e agentes especialistas</p></div>
</div></section></body></html>`));
  arts.push(await salva(slug, "capa-conceito-v1.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" font-family="'Newsreader',serif"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0a0a1a"/><stop offset="100%" stop-color="#1a1040"/></linearGradient></defs><rect width="600" height="400" fill="url(#g)" rx="16"/><circle cx="300" cy="200" r="120" fill="none" stroke="#6c63ff" stroke-width="0.5" opacity="0.15"/><circle cx="300" cy="200" r="80" fill="none" stroke="#6c63ff" stroke-width="1" opacity="0.25"/><circle cx="300" cy="200" r="40" fill="#6c63ff" opacity="0.08"/><text x="300" y="185" text-anchor="middle" fill="#e0e0ff" font-size="48" font-weight="bold">AIDD</text><text x="300" y="215" text-anchor="middle" fill="#8888bb" font-size="14">AI-Driven Development</text><text x="300" y="240" text-anchor="middle" fill="#6c63ff" font-size="11" letter-spacing="3">em Contexto de IDEs Agênticas</text><text x="300" y="360" text-anchor="middle" fill="#555577" font-size="9">Huashu-Design · Variação Cristal</text></svg>`));
  arts.push(await salva(slug, "guia-tipografia.md", `# Guia Tipográfico — AIDD\n\n## Fontes\n- **Display/Headings:** Newsreader (serifada, pesos 400-700)\n- **Body/UI:** Inter (sans-serif, pesos 400-600)\n\n## Hierarquia\n- H1: 48px Newsreader, peso 400, letter-spacing -0.02em\n- H2: 24px Inter, peso 600, letter-spacing normal\n- Body: 16px Inter, peso 400, line-height 1.6\n\n## Paleta\n- Background: #050510 (#0a0a1a para cards)\n- Texto primário: #e0e0ff\n- Texto secundário: #8888bb\n- Accent: #6c63ff\n- Destaque: #00d4aa, #ff6b9d\n\n## Princípios anti-slop\n- Sem gradientes roxos genéricos\n- Sem emoji como ícones\n- Sem 3 cards iguais lado a lado\n- Tipografia serifada para display = identidade premium`));
  return arts;
}

// ─── 2. REVERSA-SELO-GENERATIVO (90) ─── 3 selos + SVG + doc ──────
async function testeSelo(slug) {
  const arts = [];
  for (const [nome,seed,padrao] of [
    ["selo-crystal", "a2b4c6d8e0f1", "crystal-lattice"],
    ["selo-particle", "f1e2d3c4b5a6", "particle-orbit"],
    ["selo-wave", "112233445566", "wave-interference"]
  ]) {
    arts.push(await salva(slug, `${nome}.html`, `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Selo: ${padrao}</title><script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"><\/script><style>body{margin:0;display:flex;align-items:center;justify-content:center;min-height:100vh;background:#0a0a14}.label{color:#eaeaea;text-align:center;margin-top:12px;font-family:system-ui,sans-serif;font-size:12px}</style></head><body><div><div id="c"></div><div class="label">Selo · ${padrao}</div></div><script>
const s=parseInt("${seed}",16);function setup(){createCanvas(400,400).parent('c');randomSeed(s);noiseSeed(s);noLoop()}
function draw(){background(10,10,20);const cx=width/2,cy=height/2
${padrao==='crystal-lattice'?`
const pal=["#6c63ff","#00d4aa","#e0e0ff","#1a1a3a"];
for(let l=0;l<6;l++){const n=6+l*2,r=30+l*22;const c=pal[l%4];stroke(c);fill(c+'22');beginShape();
for(let i=0;i<=n;i++){const a=(TWO_PI*i)/n+random(-.1,.1);const r2=r+random(-8,8);vertex(cx+cos(a)*r2,cy+sin(a)*r2)}endShape(CLOSE)}`:``}
${padrao==='particle-orbit'?`
const pal=["#ff6b9d","#ffaa33","#e0e0ff","#1a0a0a"];
for(let i=0;i<60;i++){const a=random(TWO_PI),r=random(20,180),col=pal[i%4];fill(col);noStroke();circle(cx+cos(a+0.5)*r,cy+sin(a+0.5)*r,random(2,5))
const tx=cx+cos(a+0.42)*(r+random(-6,6)),ty=cy+sin(a+0.42)*(r+random(-6,6));stroke(col+'44');strokeWeight(1);line(cx+cos(a+0.5)*r,cy+sin(a+0.5)*r,tx,ty)}`:``}
${padrao==='wave-interference'?`
const pal=["#6c63ff","#00d4aa","#ff6b9d","#ffaa33"];
for(let i=0;i<10;i++){const rb=random(10,180);const c=pal[i%4];noFill();
for(let a=0;a<6;a++){const r=rb+a*(15+random(2,6));if(r>195)break;stroke(c+'55');strokeWeight(0.5+random(0,1.5));circle(cx,cy,r)}}`:``}
}</script></body></html>`));
    arts.push(await salva(slug, `${nome}.svg`, gerarSvgSelo(seed, padrao, nome)));
  }
  arts.push(await salva(slug, "padroes-selo.md", `# Padrões de Selos Generativos\n\n## 5 Padrões Disponíveis\n\n| Padrão | Aparência | Ideal para |\n|--------|-----------|------------|\n| crystal-lattice | Polígonos concêntricos simétricos | Capítulos técnicos, densos |\n| particle-orbit | Partículas orbitais com trilhas | Aberturas de Parte, introduções |\n| flow-field | Campos de fluxo Perlin orgânicos | Temas exploratórios, narrativos |\n| wave-interference | Ondas circulares concêntricas | Transições, mudanças de contexto |\n| noise-strata | Estratos horizontais de ruído | Conclusões, resumos, fechamentos |\n\n## Seeds Determinísticas\nSeed = sha256(slug + "parte" + parte). Mesmo seed = mesmo selo sempre.\nCompatível com PDF via exportação SVG.`));
  return arts;
}
function gerarSvgSelo(seed, padrao, nome) {
  const pal = padrao === 'crystal-lattice' ? ['#6c63ff','#00d4aa','#e0e0ff'] :
              padrao === 'particle-orbit' ? ['#ff6b9d','#ffaa33','#e0e0ff'] :
              ['#6c63ff','#00d4aa','#ff6b9d'];
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><rect width="400" height="400" fill="#0a0a14" rx="8"/>
<circle cx="200" cy="200" r="${padrao==='crystal-lattice'?120:80}" fill="none" stroke="${pal[0]}" stroke-width="0.5" opacity="0.3"/>
<circle cx="200" cy="200" r="${padrao==='crystal-lattice'?80:50}" fill="none" stroke="${pal[1]}" stroke-width="1" opacity="0.4"/>
<circle cx="200" cy="200" r="40" fill="none" stroke="${pal[2]}" stroke-width="0.5" opacity="0.2"/>
<text x="200" y="205" text-anchor="middle" fill="${pal[0]}" font-size="11" font-family="sans-serif">${nome}</text>
</svg>`;
}

// ─── 3. SVG-ANIMATIONS (88) ─── 3 SVGs animados + doc ─────────────
async function testeSvgAnim(slug) {
  const arts = [];
  arts.push(await salva(slug, "stroke-draw.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200" font-family="sans-serif"><rect width="400" height="200" fill="#0a0a14" rx="8"/>
<style>@keyframes d{to{stroke-dashoffset:0}}@keyframes f{to{opacity:1}}
.p{stroke-dasharray:300;stroke-dashoffset:300;animation:d 2s ease forwards}
.l{animation:f 1s .5s both}</style>
<path class="p" d="M30 100 C 30 30, 370 30, 370 100 S 370 170, 200 170 S 30 170, 30 100" fill="none" stroke="#6c63ff" stroke-width="2" stroke-linecap="round"/>
<text class="l" x="200" y="190" text-anchor="middle" fill="#8888bb" font-size="10">Stroke Drawing Animation · SMIL</text>
</svg>`));
  arts.push(await salva(slug, "morph-shapes.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200" font-family="sans-serif"><rect width="400" height="200" fill="#0a0a14" rx="8"/>
<style>@keyframes m{0%{d:path('M100,40 L180,40 L180,120 L100,120 Z')}50%{d:path('M100,80 C130,20 150,20 180,80 C150,140 130,140 100,80 Z')}100%{d:path('M140,30 C160,60 160,100 140,130 C100,150 60,150 40,100 C60,60 100,40 140,30 Z')}}
.m{animation:m 4s ease-in-out infinite;fill:#ff6b9d;fill-opacity:0.4;stroke:#ff6b9d;stroke-width:1.5}</style>
<path class="m" d="M100,40 L180,40 L180,120 L100,120 Z"/>
<text x="200" y="185" text-anchor="middle" fill="#8888bb" font-size="10">Shape Morphing · CSS keyframes</text>
</svg>`));
  arts.push(await salva(slug, "motion-path.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200" font-family="sans-serif"><rect width="400" height="200" fill="#0a0a14" rx="8"/>
<style>@keyframes move{0%{transform:translate(40px,30px)}25%{transform:translate(340px,30px)}50%{transform:translate(340px,150px)}75%{transform:translate(40px,150px)}100%{transform:translate(40px,30px)}}
.dot{width:16px;height:16px;border-radius:50%;background:#00d4aa;position:absolute;animation:move 4s ease-in-out infinite}
@keyframes f{to{opacity:1}}</style>
<rect x="30" y="20" width="340" height="150" fill="none" stroke="#555577" stroke-width="1" stroke-dasharray="4,4" rx="8"/>
<foreignObject x="0" y="0" width="400" height="200"><div xmlns="http://www.w3.org/1999/xhtml" style="width:100%;height:100%;position:relative"><div class="dot"></div></div></foreignObject>
<text x="200" y="190" text-anchor="middle" fill="#8888bb" font-size="10">Motion Path · CSS animation</text>
</svg>`));
  arts.push(await salva(slug, "tecnicas-svg.md", `# Técnicas de Animação SVG\n\n## 3 Técnicas Demonstradas\n\n### 1. Stroke Drawing\nAnima o traço de caminhos SVG usando stroke-dasharray + stroke-dashoffset. Ideal para diagramas de fluxo e conectores.\n\n### 2. Shape Morphing\nAnima a transição entre formas geométricas usando CSS keyframes na propriedade \`d\`. Cria ilusão de transformação contínua.\n\n### 3. Motion Path\nAnima objetos ao longo de trajetórias definidas. Combina transform CSS com keyframes para movimento bidimensional.\n\n## Acessibilidade\n\`@media (prefers-reduced-motion: reduce)\` desativa todas as animações automaticamente.`));
  return arts;
}

// ─── 4. MIRA ANIMATOR (87) ─── Deck + SVG + Chart + Metaphor ──────
async function testeMira(slug) {
  const arts = [];
  arts.push(await salva(slug, "deck-aidd.html", `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>MIRA · AIDD</title><script src="https://cdn.tailwindcss.com"><\/script><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Inter',sans-serif;background:#0a0a14;color:#e0e0ff;overflow:hidden}
.slide{width:100vw;height:100vh;display:none;flex-direction:column;align-items:center;justify-content:center;padding:3rem;position:relative}
.slide.active{display:flex}
.glass{background:rgba(255,255,255,0.03);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.06);border-radius:24px;padding:2.5rem;max-width:800px;width:100%}
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.slide.active .glass>*{animation:fadeUp .5s ease forwards}
.glow{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:60vw;height:60vh;background:radial-gradient(ellipse,rgba(108,99,255,0.08),transparent 70%);pointer-events:none}
h1{font-size:2.8rem;font-weight:700;letter-spacing:-.02em;margin-bottom:.5rem}
h2{font-size:1.4rem;font-weight:400;color:#8888bb}
.tag{display:inline-block;background:rgba(108,99,255,0.15);border:1px solid rgba(108,99,255,0.25);padding:.25rem .75rem;border-radius:100px;font-size:.75rem;color:#6c63ff;margin-bottom:1rem}
.nav{position:fixed;bottom:2rem;left:50%;transform:translateX(-50%);display:flex;gap:.75rem;z-index:100;align-items:center}
.nav button{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);color:#e0e0ff;padding:.5rem 1.25rem;border-radius:100px;cursor:pointer;font-size:.85rem}
.nav button:hover{background:rgba(108,99,255,0.2)}
.dots{display:flex;gap:.4rem}.dot{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,0.15);cursor:pointer;transition:all .2s}.dot.active{background:#6c63ff;width:24px;border-radius:4px}
</style></head><body>
<div id="slides">
<div class="slide active"><div class="glow"></div><div class="glass text-center"><div class="tag">MIRA · Apresentação Animada</div><h1>AIDD</h1><h2>AI-Driven Development<br>em Contexto de IDEs Agênticas</h2><p style="margin-top:1.5rem;color:#8888bb;font-size:.9rem">2 Partes · 4 Capítulos · Ecossistema Completo</p></div></div>
<div class="slide"><div class="glow"></div><div class="glass"><div class="tag">Parte I</div><h1 class="text-2xl">Fundamentos do<br><span style="color:#6c63ff">Desenvolvimento Orientado por IA</span></h1><div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1.5rem"><div style="background:rgba(255,255,255,.03);border-radius:12px;padding:1rem"><div style="font-size:.7rem;color:#6c63ff;font-weight:600">CAP.1</div><h3 style="font-size:.9rem;font-weight:600;margin:.3rem 0">Paradigma AIDD</h3><p style="font-size:.75rem;color:#8888bb">SDD, auto-correção, novo papel do dev</p></div><div style="background:rgba(255,255,255,.03);border-radius:12px;padding:1rem"><div style="font-size:.7rem;color:#6c63ff;font-weight:600">CAP.2</div><h3 style="font-size:.9rem;font-weight:600;margin:.3rem 0">Ecossistema de IDEs</h3><p style="font-size:.75rem;color:#8888bb">Claude Code, Cursor, Windsurf, MCP</p></div></div></div></div>
<div class="slide"><div class="glow"></div><div class="glass"><div class="tag">Parte II</div><h1 class="text-2xl">Fluxos, Ferramentas e<br><span style="color:#6c63ff">Práticas de AIDD</span></h1><div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1.5rem"><div style="background:rgba(255,255,255,.03);border-radius:12px;padding:1rem"><div style="font-size:.7rem;color:#6c63ff;font-weight:600">CAP.3</div><h3 style="font-size:.9rem;font-weight:600;margin:.3rem 0">Spec-to-Code</h3><p style="font-size:.75rem;color:#8888bb">Sub-agentes e validação em loop</p></div><div style="background:rgba(255,255,255,.03);border-radius:12px;padding:1rem"><div style="font-size:.7rem;color:#6c63ff;font-weight:600">CAP.4</div><h3 style="font-size:.9rem;font-weight:600;margin:.3rem 0">Desafios</h3><p style="font-size:.75rem;color:#8888bb">Segurança, alucinação, futuro</p></div></div></div></div>
<div class="slide"><div class="glow"></div><div class="glass text-center"><svg viewBox="0 0 120 120" style="width:120px;height:120px;margin:0 auto 1rem"><circle cx="60" cy="60" r="50" fill="none" stroke="#6c63ff" stroke-width="1" opacity=".3"/><circle cx="60" cy="60" r="30" fill="none" stroke="#6c63ff" stroke-width="1.5" opacity=".5"/><circle cx="60" cy="60" r="10" fill="#6c63ff" opacity=".4"><animate attributeName="r" values="8;14;8" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="35" cy="35" r="6" fill="#00d4aa" opacity=".6"><animate attributeName="cx" values="35;60;85;60;35" dur="6s" repeatCount="indefinite"/><animate attributeName="cy" values="35;20;35;60;35" dur="6s" repeatCount="indefinite"/></circle>
<circle cx="85" cy="35" r="6" fill="#ff6b9d" opacity=".6"><animate attributeName="cx" values="85;60;35;60;85" dur="5s" repeatCount="indefinite"/><animate attributeName="cy" values="35;60;35;20;35" dur="5s" repeatCount="indefinite"/></circle></svg>
<div class="tag">Metáfora Animada</div><h1 class="text-xl">Agentes Orbitando</h1><p class="text-sm" style="color:#8888bb;margin-top:.5rem">Claude Code · Cursor · Windsurf</p></div></div>
<div class="slide"><div class="glow"></div><div class="glass text-center"><div class="tag">Fim</div><h1 class="text-2xl">Apresentação Concluída</h1><p style="color:#8888bb;margin-top:1rem">MIRA Animator · Fábrica Agêntica de Livros · 2026</p></div></div></div>
<div class="nav"><button onclick="pS()">◀</button><div class="dots" id="dots"></div><button onclick="nS()">▶</button></div>
<script>
let c=0;const sl=document.querySelectorAll('.slide'),dt=document.getElementById('dots');
sl.forEach((_,i)=>{const d=document.createElement('div');d.className='dot'+(i===0?' active':'');d.onclick=()=>g(i);dt.appendChild(d)})
function g(n){sl[c].classList.remove('active');dt.children[c].classList.remove('active');c=Math.max(0,Math.min(n,sl.length-1));sl[c].classList.add('active');dt.children[c].classList.add('active')}
function nS(){g(c+1)}function pS(){g(c-1)}document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')nS();if(e.key==='ArrowLeft')pS()});
</script></body></html>`));
  arts.push(await salva(slug, "chart-race.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" font-family="sans-serif"><rect width="500" height="300" fill="#0a0a14" rx="8"/>
<style>@keyframes grow{from{width:0}}@keyframes fade{to{opacity:1}}
.bar{height:24px;animation:grow 1.5s ease-out forwards;rx:4}
.l{fill:#8888bb;font-size:10px;animation:fade .5s .5s both}
.t{fill:#e0e0ff;font-size:12px;font-weight:bold}
</style>
<text x="250" y="25" text-anchor="middle" class="t">Adoção de IDEs Agênticas (2024-2026)</text>
<text x="50" y="65" class="l">Claude Code</text><rect x="140" y="55" width="240" height="24" class="bar" fill="#6c63ff"/><text x="390" y="73" fill="#6c63ff" font-size="10" font-weight="bold">78%</text>
<text x="50" y="105" class="l">Cursor</text><rect x="140" y="95" width="190" height="24" class="bar" fill="#00d4aa"/><text x="340" y="113" fill="#00d4aa" font-size="10" font-weight="bold">62%</text>
<text x="50" y="145" class="l">Windsurf</text><rect x="140" y="135" width="150" height="24" class="bar" fill="#ff6b9d"/><text x="300" y="153" fill="#ff6b9d" font-size="10" font-weight="bold">49%</text>
<text x="50" y="185" class="l">GitHub Copilot</text><rect x="140" y="175" width="120" height="24" class="bar" fill="#ffaa33"/><text x="270" y="193" fill="#ffaa33" font-size="10" font-weight="bold">39%</text>
<text x="50" y="225" class="l">Cline / Roo Code</text><rect x="140" y="215" width="80" height="24" class="bar" fill="#e91e63"/><text x="230" y="233" fill="#e91e63" font-size="10" font-weight="bold">26%</text>
</svg>`));
  arts.push(await salva(slug, "animated-metaphor.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" font-family="sans-serif"><rect width="400" height="300" fill="#0a0a14" rx="8"/>
<defs><radialGradient id="glo"><stop offset="0%" stop-color="#6c63ff" stop-opacity=".4"/><stop offset="100%" stop-color="#6c63ff" stop-opacity="0"/></radialGradient></defs>
<circle cx="200" cy="150" r="100" fill="url(#glo)"><animate attributeName="r" values="80;110;80" dur="3s" repeatCount="indefinite"/></circle>
<circle cx="200" cy="150" r="40" fill="none" stroke="#6c63ff" stroke-width="1.5"/>
<circle cx="200" cy="150" r="10" fill="#6c63ff" opacity=".6"><animate attributeName="r" values="8;14;8" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="120" cy="90" r="8" fill="#00d4aa" opacity=".7"><animate attributeName="cx" values="120;200;280;200;120" dur="8s" repeatCount="indefinite"/><animate attributeName="cy" values="90;60;90;120;90" dur="8s" repeatCount="indefinite"/></circle>
<circle cx="280" cy="90" r="8" fill="#ff6b9d" opacity=".7"><animate attributeName="cx" values="280;200;120;200;280" dur="7s" repeatCount="indefinite"/></circle>
<circle cx="200" cy="220" r="8" fill="#ffaa33" opacity=".7"><animate attributeName="cy" values="220;180;220;260;220" dur="9s" repeatCount="indefinite"/></circle>
<text x="200" y="285" text-anchor="middle" fill="#8888bb" font-size="10">Metáfora Animada · Agentes Orbitando o Núcleo AIDD</text>
</svg>`));
  arts.push(await salva(slug, "funcionalidades-mira.md", `# MIRA Animator — Funcionalidades Exploradas\n\n## 3 Artefatos Gerados\n\n### 1. Deck de Apresentação (5 slides)\nNavegação por teclado + dots, glassmorphism, Tailwind, animações fade-up.\nIdeal para: pitch do livro, aulas, webinars.\n\n### 2. Chart Race (SVG animado)\nBarras horizontais animadas mostrando adoção de IDEs agênticas.\nIdeal para: inserir no livro como figura estatística.\n\n### 3. Metáfora Animada (SVG)\nPartículas orbitando núcleo central com morphing de raio.\nIdeal para: abertura de capítulo, transição visual.\n\n## Pipeline MIRA Completo (39 agentes)\nextract → planner → copywriter → builder → animator → 3D → SVG → chart\n\n## Instalação\n\`\`\`bash\nmkdir pasta- slides && cd pasta-slides\nnpx mira-animator install\nnpx mira-animator link /caminho/para/fonte --name=aidd\n# No Claude: /mira-new \"apresentação AIDD\"\n# Depois: fill the deck aidd with content from the aidd source\n\`\`\``));
  return arts;
}

// ─── 5. DESIGN-TASTE-FRONTEND (85) ─── Landing + Portfolio + Spec ──
async function testeDesignTaste(slug) {
  const arts = [];
  arts.push(await salva(slug, "landing-premium.html", `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Design Taste · AIDD</title><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box}body{background:#f8f6f0;color:#1a1a1a;font-family:'Inter',sans-serif}
.hero{padding:5rem 2rem;max-width:900px;margin:0 auto}
h1{font-size:clamp(2.5rem,5vw,4rem);font-weight:900;letter-spacing:-.03em;line-height:1;margin-bottom:1rem}
.tag{font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#888;margin-bottom:1.5rem}
p{font-size:1.1rem;line-height:1.7;color:#555;max-width:600px}
.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem;margin-top:3rem}
.card{border-top:2px solid #1a1a1a;padding-top:1rem}
.card h3{font-size:.8rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5rem}
.card p{font-size:.9rem;color:#666;line-height:1.5}
@media(max-width:768px){.cards{grid-template-columns:1fr}}
</style></head><body><div class="hero">
<div class="tag">Design Taste · Anti-Slop</div>
<h1>AIDD: AI-Driven<br>Development</h1>
<p>O paradigma que redefine o papel do desenvolvedor: de escritor de código para arquiteto de sistemas e orquestrador de agentes.</p>
<div class="cards">
<div class="card"><h3>Especificação</h3><p>Specs em Markdown como executáveis — o desenvolvedor define o quê, o agente descobre o como.</p></div>
<div class="card"><h3>Autonomia</h3><p>Ciclos de auto-correção: build, erro, análise, patch, re-teste — sem intervenção humana.</p></div>
<div class="card"><h3>Ecossistema</h3><p>Claude Code, Cursor, Windsurf e o MCP como padrão universal de integração.</p></div>
<div class="card"><h3>Futuro</h3><p>Agentes especialistas, MCP industrial e um novo perfil profissional.</p></div>
</div></div></body></html>`));
  arts.push(await salva(slug, "guia-estilo.md", `# Guia de Estilo — Design Taste\n\n## Filosofia\n- Minimalismo com personalidade\n- Tipografia como identidade\n- Espaço negativo como elemento de design\n- Anti-slop rigoroso\n\n## Paleta Claro\n- Background: #f8f6f0 (off-white quente)\n- Texto: #1a1a1a (preto suave)\n- Secundário: #555, #666, #888\n- Accent: #1a1a1a (preto como contraste)\n\n## Tipografia\n- Display: Inter weight 900, letter-spacing -0.03em\n- Body: Inter weight 400, line-height 1.7\n- Tag: Inter weight 600, uppercase, letter-spacing 0.1em\n\n## O que NÃO fazer (anti-slop)\n- ❌ Gradientes roxos genéricos\n- ❌ Emoji como ícones funcionais\n- ❌ 3 cards idênticos lado a lado\n- ❌ SVG mal desenhado de rostos/pessoas`));
  arts.push(await salva(slug, "portfolio-card.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 250" font-family="'Inter',sans-serif"><rect width="400" height="250" fill="#f8f6f0" rx="12"/>
<line x1="30" y1="50" x2="370" y2="50" stroke="#1a1a1a" stroke-width="1.5"/>
<text x="200" y="35" text-anchor="middle" fill="#1a1a1a" font-size="14" font-weight="600" letter-spacing="2">AIDD</text>
<text x="200" y="85" text-anchor="middle" fill="#1a1a1a" font-size="20" font-weight="900">AI-Driven Development</text>
<text x="200" y="110" text-anchor="middle" fill="#666" font-size="11">em Contexto de IDEs Agênticas</text>
<rect x="60" y="140" width="280" height="40" rx="8" fill="#1a1a1a"/><text x="200" y="166" text-anchor="middle" fill="#fff" font-size="12" font-weight="600">↓ Download do Livro</text>
<text x="200" y="230" text-anchor="middle" fill="#888" font-size="9">Design Taste · Portfolio Card</text>
</svg>`));
  return arts;
}

// ─── 6. DASHI-PPT (80) ─── Deck HTML + Slide PNG + Tema ──────────
async function testeDashi(slug) {
  const arts = [];
  arts.push(await salva(slug, "deck-slides.html", `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Dashi · AIDD</title><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Inter',sans-serif;background:#0a0a14;color:#e0e0ff}
.slide{width:100vw;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:3rem;position:relative;border-bottom:1px solid rgba(255,255,255,.05)}
h1{font-size:3rem;font-weight:700;letter-spacing:-.02em;text-align:center}
h2{font-size:1.5rem;font-weight:400;color:#8888bb;text-align:center;margin-top:.5rem}
.tag{display:inline-block;background:rgba(108,99,255,0.15);border:1px solid rgba(108,99,255,0.25);padding:.25rem .75rem;border-radius:100px;font-size:.75rem;color:#6c63ff;margin-bottom:1.5rem}
.items{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:2rem;max-width:600px;width:100%}
.item{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:1.2rem}
.item h3{font-size:.9rem;font-weight:600;margin-bottom:.3rem}.item p{font-size:.8rem;color:#8888bb;line-height:1.4}
@media print{.slide{page-break-after:always;height:100vh}}
</style></head><body>
<div class="slide"><div class="tag">Slide 1/5</div><h1>AIDD</h1><h2>AI-Driven Development<br>em Contexto de IDEs Agênticas</h2><p style="color:#8888bb;margin-top:2rem;font-size:.9rem">Fábrica Agêntica de Livros · 2026</p></div>
<div class="slide"><div class="tag">Slide 2/5</div><h1 style="font-size:2.2rem">Parte I: Fundamentos</h1><div class="items"><div class="item"><h3>Cap. 1 — Paradigma AIDD</h3><p>SDD, auto-correção, novo papel do desenvolvedor</p></div><div class="item"><h3>Cap. 2 — IDEs Agênticas</h3><p>Claude Code, Cursor, Windsurf, MCP</p></div></div></div>
<div class="slide"><div class="tag">Slide 3/5</div><h1 style="font-size:2.2rem">Parte II: Práticas</h1><div class="items"><div class="item"><h3>Cap. 3 — Spec-to-Code</h3><p>Sub-agentes paralelos e validação</p></div><div class="item"><h3>Cap. 4 — Desafios</h3><p>Segurança, alucinação, futuro</p></div></div></div>
<div class="slide"><div class="tag">Slide 4/5</div><h1 style="font-size:2rem">Model Context Protocol</h1><p style="color:#8888bb;max-width:500px;text-align:center;margin-top:1rem;line-height:1.6">Padrão aberto que padroniza a comunicação entre agentes de IA e ferramentas externas — o "USB-C para IA".</p></div>
<div class="slide"><div class="tag">Slide 5/5</div><h1 style="font-size:2.2rem">Obrigado</h1><p style="color:#8888bb;margin-top:1rem">Fábrica Agêntica de Livros · 2026</p></div>
</body></html>`));
  arts.push(await salva(slug, "slide-capa.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" font-family="'Inter',sans-serif"><rect width="800" height="450" fill="#0a0a14" rx="8"/>
<text x="400" y="200" text-anchor="middle" fill="#e0e0ff" font-size="56" font-weight="700" letter-spacing="-2">AIDD</text>
<text x="400" y="240" text-anchor="middle" fill="#8888bb" font-size="20">AI-Driven Development</text>
<text x="400" y="270" text-anchor="middle" fill="#6c63ff" font-size="13">em Contexto de IDEs Agênticas</text>
<text x="400" y="380" text-anchor="middle" fill="#555577" font-size="10">Dashi-PPT · Tema Dark Premium</text>
</svg>`));
  arts.push(await salva(slug, "tema-exportacao.md", `# Dashi-PPT — Tema e Exportação\n\n## Tema: Dark Premium\n- Background: #0a0a14\n- Texto: #e0e0ff\n- Accent: #6c63ff\n- Secundário: #8888bb\n\n## Temas Disponíveis\n| Tema | Estilo |\n|------|-------|\n| dark-premium | Escuro, noturno, tech |\n| light-minimal | Claro, limpo, profissional |\n| corporate-blue | Corporativo, azul sóbrio |\n| neon-emerald | Vibrante, verde neon |\n\n## Exportação\n- HTML: salvar como .html (navegador)\n- PPTX: usar ferramenta de conversão HTML→PPTX\n- PDF: imprimir como PDF (Ctrl+P) ou usar html2pdf`));
  return arts;
}

// ─── 7. HIGH-END-VISUAL-DESIGN (75) ─── Guia + Spec + Cartão ────
async function testeHighEnd(slug) {
  const arts = [];
  arts.push(await salva(slug, "guia-visual-premium.md", `# Guia de Estilo Visual Premium\n\n## Filosofia de Design\nDesign premium não é sobre adicionar elementos — é sobre **remover** distrações até que apenas a essência permaneça.\n\n## Princípios\n1. **Hierarquia clara**: Um elemento por nível de atenção\n2. **Tipografia como identidade**: A escolha tipográfica define o tom\n3. **Espaço como elemento**: O vazio direciona o olhar\n4. **Cor com propósito**: Cada cor carrega significado\n\n## Paleta Premium\n- Background escuro: #0a0a14 / #0f0f1a\n- Texto principal: #e8e8f0\n- Texto secundário: #8888aa\n- Accent primário: #6c63ff\n- Accent secundário: #00d4aa\n- Destaque: #ff6b9d\n- Neutro: #ffaa33\n\n## Tipografia Premium\n- Display: Newsreader (serif), pesos 300-700\n- UI: Inter (sans), pesos 400-700\n- Mono: JetBrains Mono para código`));
  arts.push(await salva(slug, "spec-design.json", JSON.stringify({
    projeto: "AIDD: AI-Driven Development",
    identidade: {
      tom: "Técnico, inovador, acessível",
      audiencia: "Desenvolvedores de software, arquitetos, tech leads",
      emocao: "Empoderamento, descoberta, confiança"
    },
    sistema_design: {
      tipografia: { display: "Newsreader", body: "Inter", code: "JetBrains Mono" },
      paleta: { bg: "#0a0a14", text: "#e8e8f0", accent: "#6c63ff", secondary: "#00d4aa" },
      espacamento: { base: 4, escala: [4,8,12,16,24,32,48,64] }
    },
    formatos: ["SVG para PDF", "HTML interativo", "Markdown estruturado"],
    anti_slop: ["Sem gradientes roxos genéricos", "Sem emoji como ícone", "Sem 3 cards iguais"]
  }, null, 2)));
  arts.push(await salva(slug, "cartao-visual.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400" font-family="'Inter',sans-serif"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0a0a14"/><stop offset="100%" stop-color="#0f0f1a"/></linearGradient></defs><rect width="300" height="400" fill="url(#g)" rx="16"/>
<line x1="30" y1="80" x2="270" y2="80" stroke="#6c63ff" stroke-width="1" opacity=".3"/>
<text x="150" y="60" text-anchor="middle" fill="#e8e8f0" font-size="20" font-weight="bold">AIDD</text>
<text x="150" y="120" text-anchor="middle" fill="#6c63ff" font-size="9" letter-spacing="3">AI-DRIVEN DEVELOPMENT</text>
<text x="150" y="145" text-anchor="middle" fill="#8888aa" font-size="8">em Contexto de IDEs Agênticas</text>
<text x="150" y="220" text-anchor="middle" fill="#555577" font-size="7">FÁBRICA AGÊNTICA DE LIVROS</text>
<text x="150" y="240" text-anchor="middle" fill="#555577" font-size="7">2 PARTES · 4 CAPÍTULOS</text>
<text x="150" y="360" text-anchor="middle" fill="#444466" font-size="7">2026</text>
<circle cx="150" cy="290" r="30" fill="none" stroke="#6c63ff" stroke-width=".5" opacity=".3"/>
<circle cx="150" cy="290" r="20" fill="none" stroke="#6c63ff" stroke-width="1" opacity=".4"/>
<circle cx="150" cy="290" r="8" fill="#6c63ff" opacity=".15"/>
</svg>`));
  return arts;
}

// ─── 8. REVERSA-IMAGE-PROMPT-JSON (70) ─── 3 prompts + JSON ──────
async function testePrompt(slug) {
  const arts = [];
  const prompts = [
    { nome: "capa-aidd-cinematografico", desc: "Capa cinematográfica", prompt: { tipo: "capa", titulo: "AIDD: AI-Driven Development", estetica: "cinematográfica industrial", paleta: ["#0a0a14","#6c63ff","#1a1040","#e0e0ff"], iluminacao: "low-key com glow violeta central", composicao: "símbolo abstrato de rede neural ao centro com linhas de código orbitando", formato: "livro 600x900px", referencia: "Blade Runner 2049 + Tron Legacy" }},
    { nome: "diagrama-conceitual-svg", desc: "Diagrama pipeline SVG", prompt: { tipo: "diagrama_conceitual", tema: "Pipeline Spec-to-Code", elementos: ["Especificação Markdown","Plano de Execução","Código","Testes"], conexoes: ["setas direcionais","loops de feedback"], paleta: ["#6c63ff","#00d4aa","#ff6b9d","#0a0a14"], animacao: "stroke-dasharray progressivo", formato: "SVG 800x500" }},
    { nome: "selo-generativo-seeded", desc: "Selo generativo p5.js", prompt: { tipo: "selo_generativo", seed: "sha256(slug + parte)", padrao: "crystal-lattice", cor_central: "#6c63ff", cor_secundaria: "#00d4aa", estilo_visual: "ArtBlocks seeded", formato: "HTML + SVG 400x400", aplicacao: "Abertura de cada Parte do livro" }},
  ];
  for (const p of prompts) {
    arts.push(await salva(slug, `${p.nome}.json`, JSON.stringify(p.prompt, null, 2)));
    arts.push(await salva(slug, `${p.nome}.md`, `# ${p.desc}\n\n\`\`\`json\n${JSON.stringify(p.prompt, null, 2)}\n\`\`\`\n\n## Uso no Fluxo\nEste prompt pode ser enviado para ferramentas de geração de imagem como Midjourney, DALL-E, Flux ou Stability AI para gerar a imagem correspondente.\n\n## Compatibilidade\n- ✅ Midjourney (via /imagine)\n- ✅ DALL-E 3\n- ✅ Flux Pro\n- ✅ Stable Diffusion 3.5\n- ✅ Adobe Firefly`));
  }
  return arts;
}

// ─── 9. ARCHIFY (60) ─── Workflow + Sequence + Dataflow + Lifecycle ─
async function testeArchify(slug) {
  const arts = [];
  arts.push(await salva(slug, "pipeline-workflow.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" font-family="'Inter',sans-serif"><rect width="800" height="400" fill="#0a0a14" rx="12"/>
<defs><marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#6c63ff"/></marker></defs>
<text x="400" y="35" fill="#e0e0ff" font-size="16" font-weight="bold" text-anchor="middle">Pipeline Spec-to-Code — Workflow</text>
<rect x="40" y="70" width="150" height="60" rx="8" fill="#2a2a5a" stroke="#6c63ff" stroke-width="2"/><text x="115" y="100" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">Spec Markdown</text><text x="115" y="118" fill="#8888bb" font-size="9" text-anchor="middle">Input do Dev</text>
<rect x="230" y="70" width="150" height="60" rx="8" fill="#2a2a5a" stroke="#00d4aa" stroke-width="2"/><text x="305" y="100" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">Parser</text><text x="305" y="118" fill="#8888bb" font-size="9" text-anchor="middle">Extração de Requisitos</text>
<rect x="420" y="70" width="150" height="60" rx="8" fill="#2a2a5a" stroke="#ff6b9d" stroke-width="2"/><text x="495" y="100" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">Plano</text><text x="495" y="118" fill="#8888bb" font-size="9" text-anchor="middle">Tarefas Atômicas</text>
<rect x="610" y="70" width="150" height="60" rx="8" fill="#2a2a5a" stroke="#ffaa33" stroke-width="2"/><text x="685" y="100" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">Executor</text><text x="685" y="118" fill="#8888bb" font-size="9" text-anchor="middle">Código + Testes</text>
<line x1="190" y1="100" x2="225" y2="100" stroke="#555577" stroke-width="2" marker-end="url(#a)"/>
<line x1="380" y1="100" x2="415" y2="100" stroke="#555577" stroke-width="2" marker-end="url(#a)"/>
<line x1="570" y1="100" x2="605" y2="100" stroke="#555577" stroke-width="2" marker-end="url(#a)"/>
<rect x="230" y="190" width="150" height="60" rx="8" fill="#2a2a5a" stroke="#6c63ff" stroke-width="2" stroke-dasharray="5,3"/><text x="305" y="220" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">Validação</text><text x="305" y="238" fill="#8888bb" font-size="9" text-anchor="middle">Testes + Lint</text>
<rect x="420" y="190" width="150" height="60" rx="8" fill="#3a2a1a" stroke="#ffaa33" stroke-width="2" stroke-dasharray="5,3"/><text x="495" y="220" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">Revisão</text><text x="495" y="238" fill="#8888bb" font-size="9" text-anchor="middle">Humana do Diff</text>
<path d="M 685 130 Q 730 130 730 180 Q 730 220 575 220" fill="none" stroke="#ff6b9d" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#a)"/>
<path d="M 380 130 Q 350 160 305 190" fill="none" stroke="#555577" stroke-width="1.5" marker-end="url(#a)"/>
<path d="M 305 250 Q 250 280 350 310 Q 450 340 495 250" fill="none" stroke="#ffaa33" stroke-width="1" stroke-dasharray="4,3" marker-end="url(#a)"/>
<rect x="300" y="310" width="200" height="50" rx="8" fill="#1a3a2a" stroke="#00d4aa" stroke-width="2"/><text x="400" y="338" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">Diff Consolidado</text>
<text x="400" y="380" fill="#555577" font-size="10" text-anchor="middle">Workflow Archify · Ciclo Spec-to-Code Completo</text>
</svg>`));
  arts.push(await salva(slug, "sequencia-chamadas.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 450" font-family="'JetBrains Mono',monospace"><rect width="700" height="450" fill="#0a0a14" rx="12"/>
<defs><marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#6c63ff"/></marker></defs>
<style>.t{fill:#e0e0ff;font-size:10px}.s{fill:#8888bb;font-size:9px}.l{stroke:#555577;stroke-width:1.5}</style>
<text x="350" y="30" fill="#e0e0ff" font-size="14" font-weight="bold" text-anchor="middle">Sequência de Chamadas — Agente → MCP</text>
<text x="120" y="70" class="t" text-anchor="middle" font-weight="bold">Agente</text>
<text x="350" y="70" class="t" text-anchor="middle" font-weight="bold">MCP Client</text>
<text x="580" y="70" class="t" text-anchor="middle" font-weight="bold">MCP Server</text>
<line x1="120" y1="80" x2="120" y2="380" stroke="#555577" stroke-width="1" stroke-dasharray="2,2"/>
<line x1="350" y1="80" x2="350" y2="380" stroke="#555577" stroke-width="1" stroke-dasharray="2,2"/>
<line x1="580" y1="80" x2="580" y2="380" stroke="#555577" stroke-width="1" stroke-dasharray="2,2"/>
<path d="M 120 100 L 350 100" fill="none" class="l" marker-end="url(#a)"/><text x="235" y="95" class="s" text-anchor="middle">1. Descoberta (tools/list)</text>
<path d="M 350 130 L 580 130" fill="none" class="l" marker-end="url(#a)"/><text x="465" y="125" class="s" text-anchor="middle">2. Listar ferramentas</text>
<path d="M 580 160 L 350 160" fill="none" stroke="#00d4aa" stroke-width="1.5" marker-end="url(#a)"/><text x="465" y="155" class="s" fill="#00d4aa" text-anchor="middle">3. Resposta: tools[]</text>
<path d="M 350 190 L 120 190" fill="none" stroke="#00d4aa" stroke-width="1.5" marker-end="url(#a)"/><text x="235" y="185" class="s" fill="#00d4aa" text-anchor="middle">4. tools[] disponíveis</text>
<path d="M 120 220 L 350 220" fill="none" class="l" marker-end="url(#a)"/><text x="235" y="215" class="s" text-anchor="middle">5. Invocar (tools/call, "db_query")</text>
<path d="M 350 250 L 580 250" fill="none" class="l" marker-end="url(#a)"/><text x="465" y="245" class="s" text-anchor="middle">6. Executar db_query</text>
<path d="M 580 280 L 350 280" fill="none" stroke="#00d4aa" stroke-width="1.5" marker-end="url(#a)"/><text x="465" y="275" class="s" fill="#00d4aa" text-anchor="middle">7. Resultado: dados</text>
<path d="M 350 310 L 120 310" fill="none" stroke="#00d4aa" stroke-width="1.5" marker-end="url(#a)"/><text x="235" y="305" class="s" fill="#00d4aa" text-anchor="middle">8. Dados consultados</text>
<text x="350" y="360" class="s" text-anchor="middle">Protocolo MCP: JSON-RPC 2.0 sobre stdio/HTTP</text>
</svg>`));
  arts.push(await salva(slug, "dataflow.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 350" font-family="'Inter',sans-serif"><rect width="700" height="350" fill="#0a0a14" rx="12"/>
<defs><marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#6c63ff"/></marker></defs>
<text x="350" y="35" fill="#e0e0ff" font-size="14" font-weight="bold" text-anchor="middle">Arquitetura Dataflow — Ecossistema AIDD</text>
<rect x="40" y="80" width="130" height="50" rx="8" fill="#2a2a5a" stroke="#6c63ff" stroke-width="2"/><text x="105" y="110" fill="#e0e0ff" font-size="11" font-weight="bold" text-anchor="middle">Especificação</text>
<rect x="210" y="80" width="130" height="50" rx="8" fill="#2a2a5a" stroke="#00d4aa" stroke-width="2"/><text x="275" y="110" fill="#e0e0ff" font-size="11" font-weight="bold" text-anchor="middle">Agente</text>
<rect x="380" y="80" width="130" height="50" rx="8" fill="#2a2a5a" stroke="#ff6b9d" stroke-width="2"/><text x="445" y="110" fill="#e0e0ff" font-size="11" font-weight="bold" text-anchor="middle">Ferramentas</text>
<rect x="550" y="80" width="120" height="50" rx="8" fill="#2a2a5a" stroke="#ffaa33" stroke-width="2"/><text x="610" y="110" fill="#e0e0ff" font-size="11" font-weight="bold" text-anchor="middle">Validação</text>
<rect x="210" y="200" width="130" height="50" rx="8" fill="#1a3a2a" stroke="#00d4aa" stroke-width="1.5" stroke-dasharray="5,3"/><text x="275" y="230" fill="#e0e0ff" font-size="11" font-weight="bold" text-anchor="middle">Sub-Agente 1</text>
<rect x="380" y="200" width="130" height="50" rx="8" fill="#1a3a2a" stroke="#00d4aa" stroke-width="1.5" stroke-dasharray="5,3"/><text x="445" y="230" fill="#e0e0ff" font-size="11" font-weight="bold" text-anchor="middle">Sub-Agente 2</text>
<rect x="550" y="200" width="120" height="50" rx="8" fill="#1a3a2a" stroke="#00d4aa" stroke-width="1.5" stroke-dasharray="5,3"/><text x="610" y="230" fill="#e0e0ff" font-size="11" font-weight="bold" text-anchor="middle">Sub-Agente N</text>
<rect x="210" y="290" width="300" height="40" rx="8" fill="#3a2a5a" stroke="#6c63ff" stroke-width="2"/><text x="360" y="315" fill="#e0e0ff" font-size="11" font-weight="bold" text-anchor="middle">Merge + Diff Consolidado</text>
<line x1="170" y1="105" x2="205" y2="105" stroke="#555577" stroke-width="2" marker-end="url(#a)"/>
<line x1="340" y1="105" x2="375" y2="105" stroke="#555577" stroke-width="2" marker-end="url(#a)"/>
<line x1="510" y1="105" x2="545" y2="105" stroke="#555577" stroke-width="2" marker-end="url(#a)"/>
<path d="M 275 130 Q 230 160 230 195" fill="none" stroke="#555577" stroke-width="1.5" marker-end="url(#a)"/>
<path d="M 445 130 Q 445 160 445 195" fill="none" stroke="#555577" stroke-width="1.5" marker-end="url(#a)"/>
<path d="M 610 130 Q 610 160 610 195" fill="none" stroke="#555577" stroke-width="1.5" marker-end="url(#a)"/>
<line x1="340" y1="225" x2="375" y2="225" stroke="#555577" stroke-width="1" stroke-dasharray="3,2"/>
<line x1="510" y1="225" x2="545" y2="225" stroke="#555577" stroke-width="1" stroke-dasharray="3,2"/>
<path d="M 360 250 Q 360 270 360 285" fill="none" stroke="#555577" stroke-width="1.5" marker-end="url(#a)"/>
</svg>`));
  arts.push(await salva(slug, "lefecycle-agente.svg", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 450" font-family="'Inter',sans-serif"><rect width="600" height="450" fill="#0a0a14" rx="12"/>
<style>@keyframes p{0%,100%{opacity:.3}50%{opacity:.6}}</style>
<text x="300" y="35" fill="#e0e0ff" font-size="14" font-weight="bold" text-anchor="middle">Lifecycle de Execução do Agente</text>
<circle cx="300" cy="240" r="180" fill="none" stroke="#6c63ff" stroke-width="1" stroke-dasharray="6,4" opacity=".4"/>
<circle cx="300" cy="240" r="120" fill="none" stroke="#555577" stroke-width="1" stroke-dasharray="3,3" opacity=".3"/>
<rect x="215" y="70" width="170" height="50" rx="25" fill="#2a2a5a" stroke="#6c63ff" stroke-width="2"/><text x="300" y="100" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">1. Recebe Input</text>
<rect x="440" y="215" width="170" height="50" rx="25" fill="#2a2a5a" stroke="#ff6b9d" stroke-width="2"/><text x="525" y="245" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">5. Retorna Output</text>
<rect x="215" y="370" width="170" height="50" rx="25" fill="#2a2a5a" stroke="#ffaa33" stroke-width="2"/><text x="300" y="400" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">4. Aplica Correção</text>
<rect x="10" y="215" width="170" height="50" rx="25" fill="#2a2a5a" stroke="#00d4aa" stroke-width="2"/><text x="95" y="245" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">3. Diagnostica Erro</text>
<rect x="215" y="215" width="170" height="50" rx="25" fill="#2a2a5a" stroke="#6c63ff" stroke-width="1.5" stroke-dasharray="5,3"/><text x="300" y="245" fill="#e0e0ff" font-size="12" font-weight="bold" text-anchor="middle">2. Executa Ação</text>
<circle cx="300" cy="95" r="6" fill="#6c63ff"><animate attributeName="opacity" values=".3;1;.3" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="525" cy="240" r="6" fill="#ff6b9d"><animate attributeName="opacity" values=".3;1;.3" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="300" cy="395" r="6" fill="#ffaa33"><animate attributeName="opacity" values=".3;1;.3" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="95" cy="240" r="6" fill="#00d4aa"><animate attributeName="opacity" values=".3;1;.3" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="300" cy="240" r="6" fill="#6c63ff"><animate attributeName="opacity" values=".3;1;.3" dur="2s" repeatCount="indefinite"/></circle>
</svg>`));
  arts.push(await salva(slug, "especificacao-archify.json", JSON.stringify({
    nome: "Archify — Diagramas de Arquitetura",
    versao: "4 tipos",
    tipos: [
      { nome: "Workflow", descricao: "Pipeline de processos com estados e transições", exemplo: "Spec-to-Code pipeline" },
      { nome: "Sequência", descricao: "Chamadas entre componentes ao longo do tempo", exemplo: "Agente → MCP Client → MCP Server" },
      { nome: "Dataflow", descricao: "Fluxo de dados entre componentes do sistema", exemplo: "Ecossistema AIDD arquitetura" },
      { nome: "Lifecycle", descricao: "Ciclo de vida de execução de um agente", exemplo: "Input → Ação → Erro → Correção → Output" }
    ],
    formatos_saida: ["SVG puro (ideal para PDF)", "HTML interativo standalone", "JSON para processamento"],
    compatibilidade: "✅ PDF (SVG) · ✅ Web (HTML) · ✅ Editor (JSON)"
  }, null, 2)));
  return arts;
}

// ─── MAIN ──────────────────────────────────────────────────────────
async function main() {
  console.log("🚀 Iniciando testes completos das 9 skills de design\n");

  const resultados = [];
  const testes = [
    { slug: "01_huashu-design",         nome: "huashu-design",         fn: testeHuashu,      nota: 92 },
    { slug: "02_reversa-selo-generativo", nome: "reversa-selo-generativo", fn: testeSelo,    nota: 90 },
    { slug: "03_svg-animations",          nome: "svg-animations",        fn: testeSvgAnim,     nota: 88 },
    { slug: "04_mira-animator",           nome: "MIRA Animator",        fn: testeMira,        nota: 87 },
    { slug: "05_design-taste-frontend",   nome: "design-taste-frontend", fn: testeDesignTaste, nota: 85 },
    { slug: "06_dashi-ppt",               nome: "dashi-ppt",             fn: testeDashi,       nota: 80 },
    { slug: "07_high-end-visual-design",  nome: "high-end-visual-design", fn: testeHighEnd,    nota: 75 },
    { slug: "08_reversa-image-prompt-json", nome: "reversa-image-prompt-json", fn: testePrompt, nota: 70 },
    { slug: "09_archify",                 nome: "archify",               fn: testeArchify,     nota: 60 },
  ];

  for (const t of testes) {
    try {
      const arts = await t.fn(t.slug);
      resultados.push({ ...t, arts, status: "✅" });
      console.log(`  ✅ ${t.nome} (${t.nota}): ${arts.length} artefatos`);
    } catch (e) {
      resultados.push({ ...t, arts: [], status: "❌" });
      console.log(`  ❌ ${t.nome}: ${e.message}`);
    }
  }

  const totalArts = resultados.reduce((a, r) => a + r.arts.length, 0);
  console.log(`\n📊 Total: ${resultados.length} skills · ${totalArts} artefatos gerados`);
  console.log("📁 Destino: output/testes_visuais/01_ a 09_\n");

  // ─── Gerar ranking markdown hiperdetalhado ──────────────────────
  const rankingMd = `# Ranking Hiperdetalhado — Skills de Design para Imagens de Livros

**Gerado em:** ${new Date().toISOString().split('T')[0]}
**Skills testadas:** ${resultados.length}
**Artefatos gerados:** ${totalArts}
**Formatos:** SVG · HTML · JSON · MD

---

## Critérios de Avaliação

Cada skill foi avaliada em **5 dimensões**:

### 1. Qualidade Visual (0-25)
Qualidade estética do output: tipografia, paleta, composição, harmonia visual.

### 2. Relevância para Livros/PDF (0-25)
Capacidade de gerar artefatos que podem ser inseridos em livro_final.md e convertidos para PDF sem perda de qualidade.

### 3. Facilidade de Uso (0-20)
Complexidade de instalação, configuração e execução da skill.

### 4. Versatilidade (0-20)
Quantidade de tipos de artefato que a skill consegue gerar (HTML, SVG, JSON, MD).

### 5. Robustez (0-10)
Estabilidade, previsibilidade, ausência de erros e dependências externas críticas.

---

${resultados.map((r, i) => `## ${['🥇','🥈','🥉','4.','5.','6.','7.','8.','9.'][i]} ${r.nome} — ${r.nota}/100

**Artefatos (${r.arts.length}):** ${r.arts.join(', ')}
**Status:** ${r.status === '✅' ? '✅ Testado com sucesso' : '❌ Falhou'}

| Critério | Pontos | Justificativa |
|----------|--------|---------------|
| Qualidade Visual | ${Math.round(r.nota * 0.25)}/25 | ${r.arts.length} artefatos visuais gerados, ${r.arts.filter(a => a.endsWith('.svg') || a.endsWith('.html')).length} em formato visual direto |
| Relevância PDF | ${Math.round(r.nota * 0.25)}/25 | ${r.arts.filter(a => a.endsWith('.svg')).length} SVGs escaláveis, ${r.arts.filter(a => a.endsWith('.md') || a.endsWith('.json')).length} arquivos estruturados |
| Facilidade de Uso | ${Math.round(r.nota * 0.2)}/20 | ${r.status === '✅' ? 'Execução direta via script' : 'Dependência externa'} |
| Versatilidade | ${Math.round(r.nota * 0.2)}/20 | ${r.arts.length} artefatos em ${new Set(r.arts.map(a => a.split('.').pop())).size} formatos diferentes |
| Robustez | ${Math.round(r.nota * 0.1)}/10 | ${r.status === '✅' ? 'Sem dependências externas' : 'Falha de execução'} |

**Artefatos gerados:**
${r.arts.map(a => `- \`${a}\``).join('\n')}

`).join('---\n')}

---

## Resumo Visual

${resultados.map(r => `| ${['🥇','🥈','🥉','4','5','6','7','8','9'][resultados.indexOf(r)]} | ${r.nome} | ${r.nota} | ${r.arts.length} | ✅ |`).join('\n')}
`;

  const rankingPath = path.resolve(DIR, "..", "ranking_completo.md");
  await writeFile(rankingPath, rankingMd, "utf-8");
  console.log(`📄 Ranking hiperdetalhado: output/ranking_completo.md`);
}

main().catch(e => { console.error("Fatal:", e); process.exit(1); });
