#!/usr/bin/env node
/**
 * estressar_skills.mjs — Aplica 3 testes de estresse em TODAS as skills por categoria.
 * 
 * Teste 1 — Qualidade do SKILL.md (0-40)
 *   - Frontmatter completo (name + description + license) = 15pts
 *   - Descrição > 100 chars = 10pts
 *   - Possui seções bem definidas (##) = 10pts  
 *   - Inclui exemplos de uso = 5pts
 * 
 * Teste 2 — Capacidade Técnica (0-35)
 *   - Referencia frameworks/ferramentas (React, Python, Jest, etc) = 10pts
 *   - Menciona formatos de saída (HTML, SVG, JSON, MD, PDF) = 10pts
 *   - Possui scripts/arquivos auxiliares = 8pts
 *   - Cobertura de casos de erro/edge = 7pts
 * 
 * Teste 3 — Complexidade & Maturidade (0-25)
 *   - Linhas no SKILL.md > 80 = 8pts
 *   - Possui workflow/processo definido = 6pts
 *   - Inclui metadados (version, author, updated) = 6pts
 *   - Possui validação/verificação no final = 5pts
 * 
 * Total: 0-100 pontos
 */
import { mkdir, writeFile, readFile, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { existsSync } from "node:fs";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILLS_DIR = path.resolve(DIR, "..", "..", ".claude", "skills");
const OUT = path.resolve(DIR, "ranking_estresse");
const CAT_OUT = path.join(OUT, "por-categoria");

// ─── CATEGORIAS (mesmas do V3) ────────────────────────────────────────────
const CATEGORY_RULES = [
  { cat: "Design & Visual", keywords: ["design","art","visual","ui","ux","canvas","svg","image","style","theme","color","typography","layout","brand","animation","graphic","selo","huashu","dashi","mira","archify","p5","generative","aesthetic","creative","poster","icon","logo","frontend-design"] },
  { cat: "Desenvolvimento & Engenharia", keywords: ["dev","code","program","typescript","javascript","python","react","node","api","sdk","test","tdd","debug","refactor","git","cicd","docker","deploy","backend","frontend","framework","library","module","package","cli","engineering","architecture","compiler","build","bundler","webpack","vite","jest","pytest","junit","mocha","vitest","eslint","prettier","a11y","accessibility","architect","browser","changelog","diagnos","domain","handoff","merge","migrate","monorepo","nextjs","performance","optimiz","playwright","postgres","pr-review","qa","redis","rust","saas","scaffold","senior","setup","skill-creator","spec-driven","systematic","testing","websocket","golang","django","karpathy"] },
  { cat: "SEO & Marketing Digital", keywords: ["seo","sem","search","google","keyword","rank","traffic","organic","backlink","link-build","marketing","content-market","growth","conversion","cro","landing","blog","copy","sales","lead","referral","ppc","campaign","analytics","social","email","newsletter","funnel","ad","advert","cpa","roas","aeo","paid-ads","schema-markup","copywriting","churn"] },
  { cat: "IA & Machine Learning", keywords: ["ai","ml","llm","model","train","dataset","prompt","rag","vector","embedding","nlp","neural","deep","learning","chatbot","agent","intelligence","cognition","reasoning","inference","tensor","openai","claude","gemini","llama","agenthub","context-engine","notebooklm","coach"] },
  { cat: "Dados & Analytics", keywords: ["data","analytics","database","sql","nosql","query","pipeline","etl","bi","dashboard","report","metrics","statistics","insight","warehouse","lake","stream","big-data","tableau","looker","metabase","snowflake","redis"] },
  { cat: "Segurança & Compliance", keywords: ["security","audit","compliance","legal","privacy","gdpr","access","auth","vulnerability","pentest","threat","risk","policy","encrypt","crypto","firewall","identity","iam","zero-trust","hipaa","soc2","iso","siem","sso","adversarial","authentication","fda","mdr","patent","regulatory","red-team","secrets","secops","incident","iso42001"] },
  { cat: "Produto & Estratégia", keywords: ["product","strategy","plan","roadmap","sprint","agile","pm","management","business","startup","innovation","vision","mission","okr","kpi","stakeholder","prioritiz","backlog","prd","spec","requirements","board","brainstorming","decision","capacity","inbox","scrum","init","experiment","ship-gate","hard-call","change","enterprise"] },
  { cat: "Documentação & Comunicação", keywords: ["doc","write","content","article","blog","copywrit","editor","publish","wiki","readme","markdown","md","note","obsidian","knowledge","comms","internal-comms","status","memo","newsletter","technical-writing","documentation","contract","dossier","litreview","research","writing","proposal","notebook","capture","brief"] },
  { cat: "Infraestrutura & DevOps", keywords: ["infra","devops","cloud","aws","gcp","azure","server","deploy","kubernetes","k8s","docker","container","terraform","ansible","monitoring","observability","logging","alert","sre","reliability","scaling","load","ci","cd","nginx","linux","unix","shell","bash","zsh","helm","ms365","runbook","slo","env-secrets"] },
  { cat: "Finanças & Negócios", keywords: ["finance","financ","revenue","pricing","subscription","billing","invoice","payment","stripe","accounting","budget","forecast","roi","cpa","ltv","cac","profit","cost","tax","advisor","ceo","cfo","cto","chief","executive","founder","grants","procurement","rfp","vendor","portfolio","asset"] },
  { cat: "Token Economy", keywords: ["token","fleet-auditor","token-coach","token-dashboard","token-optimizer","lean-ctx","headroom","caveman","gastos-sessao","llm-cost","context-engine"] },
  { cat: "MCP & Ferramentas", keywords: ["mcp","tool","plugin","extension","integration","connector","gateway","bridge","middleware","webhook","util","helper","generator"] },
  { cat: "Colaboração & Projetos", keywords: ["collaboration","team","communication","scheduling","calendar","meeting","project","jira","trello","asana","notion","slack","teams","discord","zoom","confluence","sharepoint","atlassian"] },
  { cat: "CRM & Vendas", keywords: ["crm","salesforce","hubspot","customer","relationship","vendas","lead","pipeline","opportunity","deal","rfp-responder","account-executive"] },
  { cat: "RH & Talentos", keywords: ["hr","recruiting","talent","people","culture","onboarding","offboarding","resume","cv","interview","candidate","career","org-health","engagement","team-health"] },
  { cat: "Mobile & Apps", keywords: ["mobile","app","ios","android","swift","kotlin","flutter","react-native","app-store","google-play","aso"] },
];

function categorize(name) {
  const lower = name.toLowerCase().replace(/[-_]/g, " ").trim();
  for (const rule of CATEGORY_RULES) {
    for (const kw of rule.keywords) {
      if (lower.includes(kw.toLowerCase())) return rule.cat;
    }
  }
  return "Outros (Geral)";
}

// ─── 3 TESTES DE ESTRESSE ─────────────────────────────────────────────────
function test1Qualidade(content) {
  let score = 0;
  const lines = content.split("\n");
  const hasFrontmatter = content.startsWith("---");
  const fmEnd = content.indexOf("---", 3);
  const fm = hasFrontmatter && fmEnd > 0 ? content.substring(3, fmEnd) : "";

  // Frontmatter completo (name + description + license/metadata)
  if (fm.includes("name:")) score += 5;
  if (fm.includes("description:")) score += 5;
  if (fm.includes("license:") || fm.includes("metadata:")) score += 5;
  
  // Descrição longa
  const descMatch = content.match(/description:\s*["']?([^"'\n]{100,})/);
  if (descMatch) score += 10;
  
  // Seções bem definidas
  const sections = content.match(/^##\s+\w+/gm);
  if (sections) {
    if (sections.length >= 3) score += 5;
    if (sections.length >= 6) score += 5;
  }
  
  // Exemplos de uso
  if (content.includes("```") || content.includes("exemplo") || content.includes("example") || content.includes("Usage")) score += 5;

  return Math.min(score, 40);
}

function test2Capacidade(content) {
  let score = 0;
  const body = content.toLowerCase();
  
  // Frameworks/ferramentas
  const frameworks = ["react","python","javascript","typescript","jest","pytest","docker","kubernetes","node","api","sdk","cli","git","npm","pip","gradle","maven","webpack","vite","tailwind","django","flask","spring","express","next","nuxt","vue","angular","svelte"];
  for (const fw of frameworks) {
    if (body.includes(fw)) { score += 2; break; }
  }
  // Bonus por multiplos frameworks
  let fwCount = 0;
  for (const fw of frameworks) {
    if (body.includes(fw)) fwCount++;
  }
  score += Math.min(fwCount - 1, 8); // até +8 por frameworks adicionais
  
  // Formatos de saída
  const formatos = ["html","svg","json","md","pdf","png","csv","xml","yaml"];
  for (const fmt of formatos) {
    if (body.includes(fmt)) score += 2;
  }
  
  // Scripts/arquivos auxiliares
  if (content.includes("scripts/") || content.includes("assets/") || content.includes("templates/") || content.includes("tests/")) score += 8;
  
  // Casos de erro/edge
  if (body.includes("error") || body.includes("edge case") || body.includes("fallback") || body.includes("tratamento")) score += 7;
  
  return Math.min(score, 35);
}

function test3Complexidade(content) {
  let score = 0;
  const lines = content.split("\n");
  const body = content.toLowerCase();
  
  // Tamanho do documento
  if (lines.length > 80) score += 4;
  if (lines.length > 150) score += 4;
  
  // Workflow definido
  if (body.includes("workflow") || body.includes("fluxo") || body.includes("processo") || body.includes("pipeline") || body.includes("passo")) score += 6;
  
  // Metadados
  if (content.includes("version:") || content.includes("author:") || content.includes("updated:") || content.includes("created:")) score += 6;
  
  // Validação/verificação
  if (body.includes("validation") || body.includes("verification") || body.includes("check") || body.includes("audit") || body.includes("test")) score += 5;
  
  return Math.min(score, 25);
}

// ─── MAIN ─────────────────────────────────────────────────────────────────
async function main() {
  console.log("🧪 TESTE DE ESTRESSE — 3 testes por skill, 482 skills, 16 categorias\n");
  
  const skills = (await readdir(SKILLS_DIR)).filter(s => !s.startsWith(".") && !s.includes("CATALOG"));
  console.log(`📦 Total de skills: ${skills.length}\n`);

  const CATS = {};
  let processadas = 0, falhas = 0;

  for (const skill of skills) {
    const cat = categorize(skill);
    if (!CATS[cat]) CATS[cat] = [];

    try {
      const content = await readFile(path.join(SKILLS_DIR, skill, "SKILL.md"), "utf-8").catch(() => "");
      
      const t1 = test1Qualidade(content);
      const t2 = test2Capacidade(content);
      const t3 = test3Complexidade(content);
      const total = t1 + t2 + t3;
      
      CATS[cat].push({ name: skill, t1, t2, t3, total, lines: content.split("\n").length });
      processadas++;
    } catch (e) {
      falhas++;
      CATS[cat].push({ name: skill, t1: 0, t2: 0, t3: 0, total: 0, lines: 0 });
    }
  }

  // ─── GERAR RANKINGS ─────────────────────────────────────────────────────
  const sortedCats = Object.entries(CATS).sort((a, b) => b[1].length - a[1].length);
  const colors = ["#6c63ff","#00d4aa","#ff6b9d","#ffaa33","#e91e63","#2196f3","#4caf50","#9c27b0","#ff5722","#00bcd4","#cddc39","#ff9800","#795548","#607d8b","#f44336","#3f51b5"];
  
  await mkdir(CAT_OUT, { recursive: true });

  // Index global
  let globalMd = [];
  globalMd.push("# Ranking de Estresse — Skills por Categoria\n\n");
  globalMd.push(`**Skills testadas:** ${processadas} | **Falhas:** ${falhas}\n`);
  globalMd.push(`**Testes:** 1-Qualidade SKILL.md (0-40) · 2-Capacidade Técnica (0-35) · 3-Complexidade (0-25) · **Total (0-100)**\n\n`);
  globalMd.push("---\n\n## Resumo por Categoria\n\n");
  globalMd.push("| # | Categoria | Skills | Média Total | Melhor Skill |\n");
  globalMd.push("|---|----------|--------|-------------|--------------|\n");

  let globalHtml = [];
  globalHtml.push(`<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Ranking de Estresse — ${processadas} Skills</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
  *{margin:0;padding:0;box-sizing:border-box}body{background:#050510;color:#e0e0ff;font-family:'Inter',sans-serif}
  .hero{text-align:center;padding:3rem 2rem 2rem}
  .hero h1{font-size:2rem;font-weight:800;background:linear-gradient(135deg,#6c63ff,#00d4aa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
  .hero p{color:#8888bb;margin-top:.5rem}
  .badge{display:inline-block;background:rgba(108,99,255,.12);border:1px solid rgba(108,99,255,.2);padding:.2rem .8rem;border-radius:100px;font-size:.75rem;color:#6c63ff;margin-bottom:1rem}
  .grid{max-width:1100px;margin:0 auto;padding:1rem 2rem 3rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.2rem}
  .card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:20px;padding:1.5rem;transition:all .3s;position:relative;overflow:hidden}
  .card:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.12)}
  .card .glow{position:absolute;top:-40px;right:-40px;width:100px;height:100px;border-radius:50%;opacity:0.08}
  .card:hover .glow{opacity:0.2}
  .card .count{font-size:2rem;font-weight:800;margin-bottom:.2rem}
  .card .medal{font-size:1.5rem}
  .card h2{font-size:1rem;font-weight:600;margin-bottom:.3rem}
  .card p{font-size:.8rem;color:#8888bb;line-height:1.4}
  .card .bested{font-size:.7rem;color:#555577;margin-bottom:.3rem}
  .card a{display:inline-block;margin-top:.6rem;padding:.3rem .8rem;border-radius:8px;font-size:.75rem;color:#e0e0ff;text-decoration:none;background:rgba(108,99,255,.12);border:1px solid rgba(108,99,255,.2);transition:all .2s}
  .card a:hover{background:rgba(108,99,255,.25)}
  footer{text-align:center;padding:2rem;color:#555577;font-size:.75rem}
  </style></head><body>
  <section class="hero"><div class="badge">🧪 Teste de Estresse</div>
  <h1>Ranking de Skills por Categoria</h1>
  <p><strong>${processadas} skills testadas</strong> · 3 testes por skill · 16 categorias · Score 0-100</p></section>
  <div class="grid">\n`);

  for (const [cat, skList] of sortedCats) {
    const total = skList.reduce((a, s) => a + s.total, 0);
    const media = (total / skList.length).toFixed(1);
    const sorted = [...skList].sort((a, b) => b.total - a.total);
    const best = sorted[0];
    const catSlug = cat.toLowerCase().replace(/[ &,()]/g, "-").replace(/-+/g, "-");
    const cor = colors[sortedCats.indexOf([cat, skList]) % colors.length];
    
    globalMd.push(`| ${sortedCats.indexOf([cat,skList])+1} | **${cat}** | ${skList.length} | ${media} | \`${best.name}\` (${best.total}) |\n`);

    globalHtml.push(`<div class="card"><div class="glow" style="background:${cor}"></div>
    <div class="count" style="color:${cor}">${media}</div>
    <div class="medal">${sortedCats.indexOf([cat,skList]) < 3 ? ["🥇","🥈","🥉"][sortedCats.indexOf([cat,skList])] : `#${sortedCats.indexOf([cat,skList])+1}`}</div>
    <h2>${cat}</h2>
    <p>${skList.length} skills testadas · Média ${media}/100</p>
    <div class="bested">🥇 ${best.name} (${best.total}pts)</div>
    <a href="por-categoria/${catSlug}/index.html">Ver ranking &#8594;</a></div>\n`);

    // ─── RANKING POR CATEGORIA (MD + HTML) ─────────────────────────────
    const catDir = path.join(CAT_OUT, catSlug);
    await mkdir(catDir, { recursive: true });
    
    const sortedSkills = [...skList].sort((a, b) => b.total - a.total);
    
    // Markdown
    let md = [];
    md.push(`# ${cat} — Ranking de Estresse\n\n`);
    md.push(`**Skills:** ${skList.length} | **Média:** ${media}/100 | **Melhor:** ${best.name} (${best.total}pts)\n\n`);
    md.push("## Critérios\n\n");
    md.push("| Teste | Pontos | Descrição |\n");
    md.push("|-------|--------|-----------|\n");
    md.push("| T1 — Qualidade SKILL.md | 0-40 | Frontmatter completo, descrição longa, seções, exemplos |\n");
    md.push("| T2 — Capacidade Técnica | 0-35 | Frameworks, formatos de saída, scripts auxiliares, edge cases |\n");
    md.push("| T3 — Complexidade | 0-25 | Tamanho, workflow, metadados, validação |\n");
    md.push("| **Total** | **0-100** | **Soma ponderada dos 3 testes** |\n\n");
    md.push("## Ranking\n\n");
    md.push("| # | Skill | T1 (0-40) | T2 (0-35) | T3 (0-25) | **Total (0-100)** | Linhas |\n");
    md.push("|---|-------|-----------|-----------|-----------|-------------------|--------|\n");
    sortedSkills.forEach((s, i) => {
      const medal = i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `#${i+1}`;
      const bar = "█".repeat(Math.round(s.total / 5)) + "░".repeat(20 - Math.round(s.total / 5));
      md.push(`| ${medal} | \`${s.name}\` | ${s.t1} | ${s.t2} | ${s.t3} | **${s.total}** ${bar} | ${s.lines} |\n`);
    });
    
    await writeFile(path.join(catDir, "ranking.md"), md.join(""));

    // HTML
    const html = `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>${cat} — Ranking de Estresse</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
    *{margin:0;padding:0;box-sizing:border-box}body{background:#050510;color:#e0e0ff;font-family:'Inter',sans-serif}
    .hero{text-align:center;padding:3rem 2rem 2rem}
    .hero h1{font-size:1.8rem;font-weight:800;background:linear-gradient(135deg,${cor},#00d4aa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
    .hero p{color:#8888bb;margin-top:.5rem;font-size:.9rem}
    .badge{display:inline-block;background:rgba(108,99,255,.12);border:1px solid rgba(108,99,255,.2);padding:.2rem .8rem;border-radius:100px;font-size:.75rem;color:${cor};margin-bottom:1rem}
    .container{max-width:900px;margin:0 auto;padding:1rem 2rem 3rem}
    .skill-row{display:flex;align-items:center;padding:.6rem 1rem;border-radius:12px;margin-bottom:.3rem;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.04);transition:all .2s}
    .skill-row:hover{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.08)}
    .skill-row .rank{width:40px;font-weight:700;font-size:.9rem;color:#8888bb}
    .skill-row .rank.gold{color:#ffd700}
    .skill-row .rank.silver{color:#c0c0c0}
    .skill-row .rank.bronze{color:#cd7f32}
    .skill-row .name{flex:1;font-size:.85rem;font-weight:500}
    .skill-row .score{width:70px;text-align:right;font-weight:700;font-size:.9rem;color:${cor}}
    .skill-row .bar-wrap{width:150px;margin-left:1rem;background:rgba(255,255,255,.04);border-radius:10px;height:8px;overflow:hidden}
    .skill-row .bar{height:100%;border-radius:10px;transition:width .5s}
    .skill-row .details{font-size:.7rem;color:#555577;margin-left:1rem;width:120px;text-align:right}
    .legend{display:flex;flex-wrap:wrap;gap:1rem;padding:1rem 2rem;max-width:900px;margin:0 auto;font-size:.75rem;color:#8888bb}
    .legend span{display:flex;align-items:center;gap:.3rem}
    .legend .dot{width:10px;height:10px;border-radius:50%}
    footer{text-align:center;padding:2rem;color:#555577;font-size:.75rem}
    @media(max-width:600px){.skill-row .bar-wrap{width:80px}.skill-row .details{width:80px}}
    </style></head><body>
    <section class="hero"><div class="badge">${skList.length} skills</div>
    <h1>${cat}</h1>
    <p>Média: ${media}/100 · Melhor: ${best.name} (${best.total}pts)</p></section>
    <div class="legend">
      <span><div class="dot" style="background:${cor}"></div>T1 — Qualidade SKILL.md (0-40)</span>
      <span><div class="dot" style="background:#00d4aa"></div>T2 — Capacidade Técnica (0-35)</span>
      <span><div class="dot" style="background:#ff6b9d"></div>T3 — Complexidade (0-25)</span>
    </div>
    <div class="container">
    ${sortedSkills.map((s, i) => {
      const medalCls = i === 0 ? "gold" : i === 1 ? "silver" : i === 2 ? "bronze" : "";
      const medal = i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `${i+1}`;
      const barW = Math.round((s.total / 100) * 100);
      return `<div class="skill-row">
        <div class="rank ${medalCls}">${medal}</div>
        <div class="name">${s.name}</div>
        <div class="bar-wrap"><div class="bar" style="width:${barW}%;background:${cor}"></div></div>
        <div class="score">${s.total}</div>
        <div class="details">T1:${s.t1} T2:${s.t2} T3:${s.t3}</div>
      </div>`;
    }).join("\n    ")}
    </div>
    <footer>Fabrica Agentica · Teste de Estresse · ${new Date().toISOString().split("T")[0]}</footer>
    </body></html>`;

    await writeFile(path.join(catDir, "index.html"), html);
    console.log(`  ✅ ${cat}: ${skList.length} skills, média ${media}`);
  }

  // Global ranking MD
  globalMd.push("\n---\n\n## Ranking Global por Categoria\n\n");
  sortedCats.forEach(([cat, skList], i) => {
    const total = skList.reduce((a, s) => a + s.total, 0);
    const media = (total / skList.length).toFixed(1);
    const best = [...skList].sort((a, b) => b.total - a.total)[0];
    const worst = [...skList].sort((a, b) => a.total - b.total)[0];
    globalMd.push(`### ${i+1}. ${cat} — Média ${media}/100\n\n`);
    globalMd.push(`- Skills: ${skList.length}\n`);
    globalMd.push(`- Melhor: \`${best.name}\` (${best.total}pts)\n`);
    globalMd.push(`- Pior: \`${worst.name}\` (${worst.total}pts)\n`);
    globalMd.push(`- Mediana: ${[...skList].sort((a,b) => a.total - b.total)[Math.floor(skList.length/2)].total}pts\n\n`);
  });

  // Fechar HTML global
  globalHtml.push(`</div>
  <footer>Fabrica Agentica · Teste de Estresse · ${new Date().toISOString().split("T")[0]}</footer>
  </body></html>`);

  await writeFile(path.join(OUT, "RANKING_ESTRESSE.md"), globalMd.join(""));
  await writeFile(path.join(OUT, "index.html"), globalHtml.join(""));

  console.log("\n" + "=".repeat(50));
  console.log("✅ TESTE DE ESTRESSE CONCLUIDO!");
  console.log("=".repeat(50));
  console.log(`   Skills testadas: ${processadas}`);
  console.log(`   Falhas: ${falhas}`);
  console.log(`   Categorias: ${sortedCats.length}`);
  console.log(`\n📁 output/teste_skills_massivo/ranking_estresse/`);
  console.log(`   ├── index.html (ranking global)`);
  console.log(`   ├── RANKING_ESTRESSE.md (relatório completo)`);
  console.log(`   └── por-categoria/ (16 rankings individuais)`);
}

main().catch(e => { console.error("ERRO FATAL:", e); process.exit(1); });
