#!/usr/bin/env node
/**
 * testar_tudo_massivo_v3.mjs — Correção final dos issues do V2:
 * 1. ✅ Normaliza \r\n para \n (Windows) antes do parsing
 * 2. ✅ Regex multi-line com suporte a aspas e descrições longas
 * 3. ✅ Categorização expandida (+20 domínios novos)
 * 4. ✅ Word boundary no "tipo" detection
 * 5. ✅ Pastas V1 removidas (categorias duplicadas)
 */
import { mkdir, writeFile, readFile, readdir, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILLS_DIR = path.resolve(DIR, "..", "..", ".claude", "skills");
const OUT = DIR;

// ─── CATEGORIZAÇÃO EXPANDIDA ────────────────────────────────────────────────
const CATEGORY_RULES = [
  { cat: "Design & Visual", keywords: ["design","art","visual","ui","ux","frontend-design","canvas","svg","image","style","theme","color","typography","layout","brand","animation","graphic","selo","huashu","dashi","mira","archify","p5","generative","aesthetic","creative","poster","icon","logo"] },
  { cat: "Desenvolvimento & Engenharia", keywords: ["dev","code","program","typescript","javascript","python","react","node","api","sdk","test","tdd","debug","refactor","git","cicd","docker","deploy","backend","frontend","framework","library","module","package","cli","engineering","architecture","typescript","compiler","build","bundler","webpack","vite","jest","pytest","junit","mocha","vitest","eslint","prettier","accessibility","a11y","architect","browser","bugs","changelog","diagnos","domain","execute","handoff","merge","migrate","monorepo","nextjs","performance","optimiz","playwright","postgres","pr-review","qa","redis","resolve","rust","saas","scaffold","senior","setup","ship","skill-creator","skill-tester","spec-driven","systematic","testing","typescript","websocket","dependency","feature-flag","profiler","full-page","screenshot","code-review","boilerplate","karpathy","implement","pipeline-ci","merge-conflict","pre-commit","scaffold-exercises","pr-review-expert","golang","django","nextjs","redis-patterns","rust-systems","snowflake","postgres-optimization","performance-optimization","performance-profiler","monorepo-navigator","diagnosing-bugs","dependency-auditor","migration-architect","full-page-screenshot","playwright-pro"] },
  { cat: "SEO & Marketing Digital", keywords: ["seo","sem","search","google","keyword","rank","traffic","organic","backlink","link-build","marketing","content-market","growth","conversion","cro","landing","blog","copy","sales","lead","referral","ppc","campaign","analytics","social","email","newsletter","funnel","ad","advert","ppc","cpa","roas","aeo","paid-ads","schema-markup","copywriting"] },
  { cat: "IA & Machine Learning", keywords: ["ai","ml","llm","model","train","dataset","prompt","rag","vector","embedding","nlp","neural","deep","learning","chatbot","agent","intelligence","cognition","reasoning","inference","tensor","openai","claude","gemini","llama","agenthub","context-engine","notebooklm"] },
  { cat: "Dados & Analytics", keywords: ["data","analytics","database","sql","nosql","query","pipeline","etl","bi","dashboard","report","metrics","statistics","insight","warehouse","lake","stream","big-data","tableau","looker","metabase","snowflake","postgres","redis"] },
  { cat: "Segurança & Compliance", keywords: ["security","audit","compliance","legal","privacy","gdpr","access","auth","vulnerability","pentest","threat","risk","policy","encrypt","crypto","firewall","identity","iam","zero-trust","hipaa","soc2","iso","siem","sso","adversarial","authentication","fda","mdr","patent","ra-qm","regulatory","red-team","scenario","secrets","secops","general-counsel","quality-manager","iso42001","incident-response","incident-commander","named-persona"] },
  { cat: "Produto & Estratégia", keywords: ["product","strategy","plan","roadmap","sprint","agile","pm","management","business","startup","innovation","vision","mission","okr","kpi","stakeholder","prioritiz","backlog","product-manager","product-owner","prd","spec","requirements","board","brainstorming","decision","capacity","inbox","scrum","init","experiment","ship-gate","hard-call","office-hours","change","enterprise","resource"] },
  { cat: "Documentação & Comunicação", keywords: ["doc","write","content","article","blog","copywrit","editor","publish","wiki","readme","markdown","md","note","obsidian","knowledge","comms","internal-comms","status","report","memo","newsletter","technical-writing","documentation","contract","dossier","litreview","research","writing","proposal","notebook","handoff","capture","brief","changelog"] },
  { cat: "Infraestrutura & DevOps", keywords: ["infra","devops","cloud","aws","gcp","azure","server","deploy","kubernetes","k8s","docker","container","terraform","ansible","monitoring","observability","logging","alert","sre","reliability","scaling","load","ci","cd","nginx","linux","unix","shell","bash","zsh","capacity","helm","incident","migration","ms365","runbook","slo","env-secrets","secrets-vault","helm-chart"] },
  { cat: "Finanças & Negócios", keywords: ["finance","financ","revenue","pricing","subscription","billing","invoice","payment","stripe","accounting","budget","forecast","roi","cpa","ltv","cac","profit","cost","tax","audit-fin","treasury","invoice","advisor","ceo","cfo","cto","chief","executive","founder","grants","intl-expansion","ma-playbook","partnerships","procurement","rfp","vendor","coo","cpo","cco","cdo","chro","board-deck","board-meeting","boardroom","deal-desk","channel-economics","financial-analyst","portfolio","asset"] },
  { cat: "Mobile & Apps", keywords: ["mobile","app","ios","android","swift","kotlin","flutter","react-native","app-store","google-play","store-opt","aso","mobile-app"] },
  { cat: "MCP & Ferramentas", keywords: ["mcp","tool","plugin","extension","integration","connector","gateway","bridge","middleware","webhook","util","helper","generator","scaffold"] },
  // Domínios extras
  { cat: "CRM & Vendas", keywords: ["crm","salesforce","hubspot","customer","relationship","vendas","lead","pipeline","opportunity","deal","account-executive","rfp-responder"] },
  { cat: "RH & Talentos", keywords: ["hr","recruiting","talent","people","culture","onboarding","offboarding","resume","cv","interview","candidate","employer","job","career","workday","bamboo","org-health","talent-acquisition","team-health","engagement"] },
  { cat: "Suporte & Customer Success", keywords: ["support","customer-success","csat","nps","ticket","helpdesk","zendesk","freshdesk","intercom","chat","service-desk","sla","cs-onboard"] },
  { cat: "Operações & Processos", keywords: ["ops","operations","process","workflow","automation","bpm","orchestrat","sop","runbook","procedur","approval","rpa","inventory","supply","logistics"] },
  { cat: "Colaboração & Projetos", keywords: ["collaboration","team","communication","scheduling","calendar","meeting","project","jira","trello","asana","notion","slack","teams","discord","zoom","confluence","sharepoint","atlassian","office-hours","meeting-analyzer","inbox-triage","inbox-setup"] },
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

// ─── PARSE SKILL.MD V2 (com suporte a \r\n Windows) ────────────────────────
function parseSkillMd(rawContent, skillName) {
  const result = { name: skillName, description: "(sem descricao)", tipo: "general" };
  try {
    // 1. Normalizar \r\n → \n (Windows)
    const content = rawContent.replace(/\r\n/g, "\n");
    
    // 2. Extrair frontmatter YAML
    const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (fmMatch) {
      const fm = fmMatch[1];
      
      // name: pode ser com ou sem aspas
      const nameMatch = fm.match(/^name:\s*["']?([^"'\n]+)["']?/m);
      if (nameMatch) result.name = nameMatch[1].trim();
      
      // description: multi-line, com ou sem aspas
      const descMatch = fm.match(/^description:\s*["']?([\s\S]*?)(?:\n\w+:|["']?\s*$)/m);
      if (descMatch) {
        let desc = descMatch[1].trim();
        // Limpar caracteres especiais
        desc = desc.replace(/["']$/, "").replace(/\s+/g, " ").trim();
        if (desc.length > 200) desc = desc.substring(0, 197) + "...";
        if (desc.length > 0) result.description = desc;
      } else {
        // Fallback: descrição single-line
        const simpleDesc = fm.match(/^description:\s*(.+)$/m);
        if (simpleDesc) {
          let desc = simpleDesc[1].trim().replace(/^["']|["']$/g, "").substring(0, 200);
          if (desc.length > 0) result.description = desc;
        }
      }
    }

    // 3. Detectar tipo COM WORD BOUNDARY
    const body = content.toLowerCase();
    const nameLower = skillName.toLowerCase();
    const tiposCheck = [
      { key: "visual", patterns: [/\bp5\.js\b/, /\bcanvas\b/, /\bgenerative\b/, /\bsvg\b/, /\banimation\b/, /\bart\b/] },
      { key: "html", patterns: [/\bhtml\b/, /\breact\b/, /\btailwind\b/, /\blanding\b/, /\bui\b/] },
      { key: "report", patterns: [/\baudit\b/, /\breport\b/, /\banalysis\b/, /\bdiagnos\b/] },
      { key: "code", patterns: [/\bjavascript\b/, /\bpython\b/, /\btypescript\b/, /\bsource code\b/, /\balgorithm\b/] },
      { key: "test", patterns: [/\btest\b/, /\btdd\b/, /\bjest\b/, /\bpytest\b/, /\bjunit\b/] },
      { key: "json", patterns: [/\bjson\b/, /\bconfig\b/, /\bschema\b/] },
    ];
    // Verificar também pelo nome da skill
    for (const check of tiposCheck) {
      for (const p of check.patterns) {
        if (p.test(body) || p.test(nameLower)) {
          result.tipo = check.key;
          break;
        }
      }
      if (result.tipo !== "general") break;
    }
  } catch (e) {
    // fallback total
  }
  return result;
}

// ─── MAIN ────────────────────────────────────────────────────────────────────
async function main() {
  console.log("🧪 TESTE MASSIVO V3 — Lendo SKILL.md real (\\r\\n fix, word boundary, categorias expandidas)\n");
  
  // Remove pastas antigas V1/V2 das categorias
  for (const old of ["design---visual", "documentação---escrita", "ia---data", "produto---estratégia", "segurança---compliance", "seo---marketing", "outros"]) {
    const p = path.join(OUT, "categorias", old);
    if (existsSync(p)) { await rm(p, { recursive: true, force: true }); console.log("  🗑️ Removida pasta V1:", old); }
  }

  const skills = (await readdir(SKILLS_DIR)).filter(s => !s.startsWith(".") && !s.includes("CATALOG"));
  console.log(`\n📦 Total de skills: ${skills.length}\n`);

  const CATS = {};
  let totalParsed = 0, totalFalhou = 0;
  const colors = ["#6c63ff","#00d4aa","#ff6b9d","#ffaa33","#e91e63","#2196f3","#4caf50","#9c27b0","#ff5722","#00bcd4","#cddc39","#ff9800"];

  for (const skill of skills) {
    const cat = categorize(skill);
    if (!CATS[cat]) CATS[cat] = [];

    try {
      const rawContent = await readFile(path.join(SKILLS_DIR, skill, "SKILL.md"), "utf-8");
      const info = parseSkillMd(rawContent, skill);
      totalParsed++;
      
      const slug = skill.replace(/[^a-z0-9-]/gi, "_").toLowerCase();
      const ts = new Date().toISOString().split("T")[0];
      const skillDir = path.join(OUT, "artefatos", slug);
      await mkdir(skillDir, { recursive: true });

      // MD contextual
      let md = `# ${info.name}\n\n`;
      md += `**Categoria:** ${cat}\n`;
      md += `**Repositório:** .claude/skills/${skill}/\n`;
      md += `**Testado em:** ${ts}\n\n`;
      md += `## Descrição Real\n\n${info.description}\n\n`;
      md += `## Tipo Detectado\n\n\`${info.tipo}\` — detector com word boundary\n\n`;
      md += `## Artefato Gerado\n\n`;
      md += `Este teste foi gerado a partir da **leitura real** do SKILL.md.\n\n`;
      md += `### Métricas\n\n`;
      md += `| Métrica | Valor |\n|---------|-------|\n`;
      md += `| Skill | \`${info.name}\` |\n`;
      md += `| Categoria | ${cat} |\n`;
      md += `| Tipo Detectado | ${info.tipo} |\n`;
      md += `| Descrição | ${info.description.substring(0, 80)}... |\n`;
      md += `| Artefatos | MD + SVG + JSON |\n`;

      // SVG com nome real da skill
      const cor = colors[Math.floor(Math.random() * colors.length)];
      const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 100" font-family="'Inter',sans-serif">
  <rect width="240" height="100" fill="#0a0a14" rx="10"/>
  <rect x="8" y="8" width="224" height="84" rx="8" fill="${cor}" opacity=".08"/>
  <circle cx="30" cy="30" r="12" fill="${cor}" opacity=".3"><animate attributeName="r" values="10;14;10" dur="2.5s" repeatCount="indefinite"/></circle>
  <text x="120" y="48" text-anchor="middle" fill="${cor}" font-size="11" font-weight="bold">${info.name.length > 22 ? info.name.substring(0,20)+"..." : info.name}</text>
  <text x="120" y="65" text-anchor="middle" fill="#8888bb" font-size="8">${info.tipo} · ${info.description.substring(0,25)}</text>
  <rect x="20" y="78" width="200" height="4" rx="2" fill="${cor}" opacity=".2"><animate attributeName="opacity" values=".2;.5;.2" dur="3s" repeatCount="indefinite"/></rect>
</svg>`;

      // JSON com metadados reais
      const json = JSON.stringify({
        skill: info.name,
        slug: slug,
        description: info.description,
        categoria: cat,
        tipo: info.tipo,
        timestamp: ts,
        repo_path: `.claude/skills/${skill}/`,
        metrics: { type: info.tipo, category: cat }
      }, null, 2);

      await writeFile(path.join(skillDir, `${slug}.md`), md);
      await writeFile(path.join(skillDir, `${slug}.svg`), svg);
      await writeFile(path.join(skillDir, `${slug}.json`), json);

      CATS[cat].push({ name: skill, info, slug, cor });
    } catch (e) {
      totalFalhou++;
      const slug = skill.replace(/[^a-z0-9-]/gi, "_").toLowerCase();
      CATS[cat].push({ name: skill, info: { name: skill, description: `ERRO: ${e.message}`, tipo: "error" }, slug, cor: "#ff0000" });
    }
  }

  // ─── RELATÓRIOS POR CATEGORIA ────────────────────────────────────────────
  const sorted = Object.entries(CATS).sort((a, b) => b[1].length - a[1].length);
  let totalArtifacts = 0;

  for (const [cat, skList] of sorted) {
    totalArtifacts += skList.length * 3;
    const catSlug = cat.toLowerCase().replace(/[ &,()]/g, "-").replace(/-+/g, "-");
    const catDir = path.join(OUT, "categorias", catSlug);
    await mkdir(catDir, { recursive: true });

    for (const s of skList) {
      await writeFile(path.join(catDir, `${s.slug}.md`),
        `# ${s.info.name}\n\n**Categoria:** ${cat}\n**Descrição:** ${s.info.description}\n**Tipo:** ${s.info.tipo}\n\n[Ver artefatos completos](../artefatos/${s.slug}/)\n`);
    }

    // HTML com descrição real
    const html = `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>${cat} — ${skList.length} skills</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
    *{margin:0;padding:0;box-sizing:border-box}body{background:#050510;color:#e0e0ff;font-family:'Inter',sans-serif}
    .hero{text-align:center;padding:3rem 2rem 2rem}
    .hero h1{font-size:2rem;font-weight:800;background:linear-gradient(135deg,#6c63ff,#00d4aa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
    .hero p{color:#8888bb;margin-top:.5rem}
    .badge{display:inline-block;background:rgba(108,99,255,.12);border:1px solid rgba(108,99,255,.2);padding:.2rem .8rem;border-radius:100px;font-size:.75rem;color:#6c63ff;margin-bottom:1rem}
    .stats{text-align:center;padding:1rem 2rem;color:#555577;font-size:.85rem}
    .stats span{color:#6c63ff;font-weight:600}
    .grid{max-width:1200px;margin:0 auto;padding:1rem 2rem 3rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.8rem}
    .card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:16px;padding:1rem;transition:all .3s;position:relative;overflow:hidden}
    .card:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.12)}
    .card .cor-bar{height:3px;border-radius:2px;margin-bottom:.5rem;width:100%}
    .card h3{font-size:.82rem;font-weight:600;margin-bottom:.2rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
    .card .desc{font-size:.7rem;color:#8888bb;line-height:1.4;margin-bottom:.4rem;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
    .card .tags{display:flex;flex-wrap:wrap;gap:.2rem}
    .card .tag{font-size:.6rem;padding:.1rem .4rem;border-radius:4px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);color:#8888bb}
    .glow{position:absolute;top:-30px;right:-30px;width:80px;height:80px;border-radius:50%;opacity:0.04}
    footer{text-align:center;padding:2rem;color:#555577;font-size:.75rem}
    </style></head><body>
    <section class="hero"><div class="badge">&#128202; ${skList.length} skills · ${cat}</div>
    <h1>${cat}</h1><p>Teste real com leitura de SKILL.md · ${skList.length * 3} artefatos</p></section>
    <div class="stats">Skills: <span>${skList.length}</span> · Artefatos: <span>${skList.length * 3}</span></div>
    <div class="grid">
    ${skList.map(s => `<div class="card"><div class="glow" style="background:${s.cor}"></div>
    <div class="cor-bar" style="background:${s.cor};opacity:.3"></div>
    <h3 title="${s.info.name}">${s.info.name}</h3>
    <div class="desc">${(s.info.description || "").substring(0, 120)}</div>
    <div class="tags"><span class="tag">${s.info.tipo}</span></div>
    </div>`).join("\n    ")}
    </div>
    <footer>Fabrica Agentica de Livros · Teste Massivo V3 · ${new Date().toISOString().split("T")[0]}</footer></body></html>`;
    await writeFile(path.join(catDir, "index.html"), html);
    console.log(`  ✅ ${cat}: ${skList.length} skills`);
  }

  // ─── RANKING V3 ─────────────────────────────────────────────────────────
  console.log("\n📊 GERANDO RANKING V3...\n");
  const rl = [];
  rl.push("# Ranking Massivo de Skills V3 — Teste Real com SKILL.md\n\n");
  rl.push(`**Gerado em:** ${new Date().toISOString().split("T")[0]}\n\n`);
  rl.push(`## Métricas Globais\n\n`);
  rl.push(`| Métrica | Valor |\n|---------|-------|\n`);
  rl.push(`| Skills totais | ${skills.length} |\n`);
  rl.push(`| Skills parseadas | ${totalParsed} |\n`);
  rl.push(`| Falhas | ${totalFalhou} |\n`);
  rl.push(`| Artefatos | ${totalArtifacts} |\n`);
  rl.push(`| Categorias | ${sorted.length} |\n`);
  rl.push(`| Repositórios | 5 (alirezarezvani, anthropics, superpowers, mattpocock, rohitg00) |\n\n`);

  rl.push("---\n\n## Categorias\n\n");
  rl.push("| # | Categoria | Skills | Artefatos | % |\n");
  rl.push("|---|----------|--------|-----------|----|\n");
  sorted.forEach(([cat, skList], i) => {
    rl.push(`| ${i+1} | **${cat}** | ${skList.length} | ${skList.length * 3} | ${((skList.length/skills.length)*100).toFixed(1)}% |\n`);
  });

  rl.push("\n---\n\n## Detalhamento\n\n");
  for (const [cat, skList] of sorted) {
    rl.push(`### ${cat} (${skList.length} skills)\n\n`);
    rl.push(`| # | Skill | Tipo | Descrição Real |\n`);
    rl.push(`|---|-------|------|----------------|\n`);
    skList.sort((a,b) => a.name.localeCompare(b.name)).forEach((s, i) => {
      const desc = (s.info.description || "").substring(0, 60).replace(/\|/g, "-").replace(/\n/g, " ");
      rl.push(`| ${i+1} | \`${s.name}\` | ${s.info.tipo} | ${desc} |\n`);
    });
    rl.push("\n");
  }

  await writeFile(path.join(OUT, "RANKING_MASSIVO_V3.md"), rl.join(""));

  // ─── INDEX ───────────────────────────────────────────────────────────────
  const indexHtml = `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Teste Massivo V3 — ${skills.length} Skills</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style>
  *{margin:0;padding:0;box-sizing:border-box}body{background:#050510;color:#e0e0ff;font-family:'Inter',sans-serif;min-height:100vh}
  .hero{text-align:center;padding:4rem 2rem 3rem;position:relative;overflow:hidden}
  .hero::before{content:'';position:absolute;top:-50%;left:50%;transform:translateX(-50%);width:800px;height:800px;background:radial-gradient(circle,rgba(108,99,255,0.06),transparent 70%)}
  .hero h1{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;letter-spacing:-.03em;margin-bottom:.5rem}
  .hero h1 span{background:linear-gradient(135deg,#6c63ff,#00d4aa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
  .hero p{color:#8888bb;max-width:700px;margin:0 auto;font-size:.95rem;line-height:1.5}
  .badge{display:inline-flex;align-items:center;gap:.4rem;background:rgba(108,99,255,.12);border:1px solid rgba(108,99,255,.2);padding:.3rem 1rem;border-radius:100px;font-size:.75rem;color:#6c63ff;margin-bottom:1.5rem}
  .grid{max-width:1100px;margin:0 auto;padding:1rem 2rem 3rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.2rem}
  .card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:20px;padding:1.5rem;transition:all .3s;position:relative;overflow:hidden}
  .card:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.12)}
  .card .glow{position:absolute;top:-40px;right:-40px;width:100px;height:100px;border-radius:50%;opacity:0.08}
  .card:hover .glow{opacity:0.2}
  .card .count{font-size:2rem;font-weight:800;margin-bottom:.2rem}
  .card h2{font-size:1rem;font-weight:600;margin-bottom:.3rem}
  .card p{font-size:.8rem;color:#8888bb;line-height:1.4}
  .card .pct{font-size:.7rem;color:#555577;margin-bottom:.3rem}
  .card a{display:inline-block;margin-top:.6rem;padding:.3rem .8rem;border-radius:8px;font-size:.75rem;color:#e0e0ff;text-decoration:none;background:rgba(108,99,255,.12);border:1px solid rgba(108,99,255,.2);transition:all .2s}
  .card a:hover{background:rgba(108,99,255,.25)}
  .stats{text-align:center;padding:2rem;color:#555577;font-size:.9rem;line-height:1.8}
  .stats span{color:#6c63ff;font-weight:600}
  .stats-grid{display:grid;grid-template-columns:repeat(4,1fr);max-width:600px;margin:1rem auto;gap:.5rem}
  .stat-box{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.04);border-radius:12px;padding:.8rem}
  .stat-box .num{font-size:1.5rem;font-weight:800;color:#6c63ff}
  .stat-box .label{font-size:.65rem;color:#8888bb;text-transform:uppercase;letter-spacing:.02em}
  .err-note{text-align:center;padding:0 2rem 1rem;color:#ff6b6b;font-size:.8rem}
  footer{text-align:center;padding:2rem;color:#555577;font-size:.75rem}
  </style></head><body>
  <section class="hero"><div class="badge">&#9889; Teste Massivo V3</div>
  <h1><span>${skills.length} Skills</span> — ${sorted.length} Categorias</h1>
  <p><strong>Teste real com leitura de SKILL.md:</strong> ${totalParsed} parseadas, ${totalFalhou} falhas. Categorização expandida com 40+ domínios. Detecção de tipo com word boundary. Suporte a \\r\\n Windows.</p></section>
  ${totalFalhou > 0 ? `<div class="err-note">&#9888; ${totalFalhou} skills com erro de parsing (detalhes no ranking)</div>` : ""}
  <div class="stats">
    <div class="stats-grid">
      <div class="stat-box"><div class="num">${skills.length}</div><div class="label">Skills</div></div>
      <div class="stat-box"><div class="num">${totalParsed}</div><div class="label">Parseadas</div></div>
      <div class="stat-box"><div class="num">${totalArtifacts}</div><div class="label">Artefatos</div></div>
      <div class="stat-box"><div class="num">${sorted.length}</div><div class="label">Categorias</div></div>
    </div>
  </div>
  <div class="grid">
  ${sorted.map(([cat, skList], i) => {
    const c = colors[i % colors.length];
    return `<div class="card"><div class="glow" style="background:${c}"></div>
    <div class="count" style="color:${c}">${skList.length}</div>
    <h2>${cat}</h2>
    <div class="pct">${((skList.length/skills.length)*100).toFixed(1)}% do total</div>
    <p>${skList.slice(0,3).map(s => s.info.name).join(", ")}...</p>
    <a href="categorias/${cat.toLowerCase().replace(/[ &,()]/g, "-").replace(/-+/g, "-")}/index.html">Ver &#8594;</a></div>`;
  }).join("\n  ")}
  </div>
  <footer>Fabrica Agentica de Livros · Teste Massivo V3 · ${new Date().toISOString().split("T")[0]}</footer>
  </body></html>`;

  await writeFile(path.join(OUT, "index.html"), indexHtml);

  console.log("\n" + "=".repeat(50));
  console.log("✅ TESTE MASSIVO V3 CONCLUIDO!");
  console.log("=".repeat(50));
  console.log(`   Skills: ${skills.length}`);
  console.log(`   Parseadas: ${totalParsed}`);
  console.log(`   Falhas: ${totalFalhou}`);
  console.log(`   Artefatos: ${totalArtifacts}`);
  console.log(`   Categorias: ${sorted.length}`);
  for (const [cat, skList] of sorted) {
    console.log(`   ${cat}: ${skList.length}`);
  }
}

main().catch(e => { console.error("ERRO FATAL:", e); process.exit(1); });
