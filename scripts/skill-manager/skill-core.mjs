/**
 * skill-core.mjs — Core do Skill Manager
 * 
 * Funções:
 * - Listar skills instaladas com descrições e categorias
 * - Categorizar skills (usando as mesmas regras do V3)
 * - Instalar skills via npx (local e/ou global)
 * - Remover skills via npx
 * - Suporte multi-IDE
 */
import { readFile, readdir, writeFile, mkdir } from "node:fs/promises";
import { existsSync, mkdirSync, copyFileSync } from "node:fs";
import path from "node:path";
import { execSync, spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

// ─── CATEGORIAS ─────────────────────────────────────────────────────────────
const CATEGORIES = [
  { name: "Design & Visual", icon: "🎨", keywords: ["design","art","visual","ui","ux","canvas","svg","image","style","theme","color","typography","layout","brand","animation","graphic","selo","huashu","dashi","mira","archify","p5","generative","aesthetic","creative","poster","icon","logo"] },
  { name: "Desenvolvimento & Engenharia", icon: "💻", keywords: ["dev","code","program","typescript","javascript","python","react","node","api","sdk","test","tdd","debug","refactor","git","cicd","docker","deploy","backend","frontend","framework","library","module","package","cli","engineering","architecture","compiler","build","webpack","vite","jest","pytest","junit","accessibility","architect","browser","changelog","domain","handoff","merge","migrate","monorepo","nextjs","performance","optimiz","playwright","qa","redis","rust","saas","scaffold","senior","setup","testing","golang","django","karpathy"] },
  { name: "SEO & Marketing", icon: "📈", keywords: ["seo","sem","search","google","keyword","rank","traffic","organic","backlink","link-build","marketing","content-market","growth","conversion","cro","landing","blog","copy","sales","lead","referral","ppc","campaign","analytics","social","email","newsletter","funnel","ad","advert","cpa","roas","aeo","paid-ads","schema-markup","copywriting","churn"] },
  { name: "IA & Machine Learning", icon: "🤖", keywords: ["ai","ml","llm","model","train","dataset","prompt","rag","vector","embedding","nlp","neural","deep","learning","chatbot","agent","intelligence","cognition","reasoning","inference","tensor","openai","claude","gemini","llama","agenthub","context-engine","notebooklm","coach"] },
  { name: "Dados & Analytics", icon: "📊", keywords: ["data","analytics","database","sql","nosql","query","pipeline","etl","bi","dashboard","report","metrics","statistics","insight","warehouse","lake","stream","big-data","tableau","looker","metabase","snowflake","redis"] },
  { name: "Segurança & Compliance", icon: "🔒", keywords: ["security","audit","compliance","legal","privacy","gdpr","access","auth","vulnerability","pentest","threat","risk","policy","encrypt","crypto","firewall","identity","iam","hipaa","soc2","iso","siem","sso","adversarial","authentication","fda","mdr","regulatory","red-team","secrets","secops","incident"] },
  { name: "Produto & Estratégia", icon: "🚀", keywords: ["product","strategy","plan","roadmap","sprint","agile","pm","management","business","startup","innovation","vision","mission","okr","kpi","stakeholder","backlog","prd","spec","requirements","board","brainstorming","decision","capacity","inbox","scrum","init","experiment","change","enterprise"] },
  { name: "Documentação & Escrita", icon: "📝", keywords: ["doc","write","content","article","blog","copywrit","editor","publish","wiki","readme","markdown","md","note","obsidian","knowledge","comms","memo","newsletter","technical-writing","documentation","contract","dossier","litreview","research","proposal","capture","brief"] },
  { name: "Infraestrutura & DevOps", icon: "⚙️", keywords: ["infra","devops","cloud","aws","gcp","azure","server","deploy","kubernetes","k8s","docker","container","terraform","ansible","monitoring","observability","logging","alert","sre","reliability","scaling","load","ci","cd","nginx","linux","unix","shell","bash","zsh","helm","ms365","runbook","slo"] },
  { name: "Finanças & Negócios", icon: "💰", keywords: ["finance","financ","revenue","pricing","subscription","billing","invoice","payment","stripe","accounting","budget","forecast","roi","cpa","ltv","cac","profit","cost","tax","advisor","ceo","cfo","cto","chief","executive","founder","grants","procurement","rfp","vendor","portfolio","asset"] },
  { name: "Token Economy", icon: "🪙", keywords: ["token","lean-ctx","headroom","caveman","gastos","llm-cost","context-engine","fleet-auditor","token-coach","token-dashboard","token-optimizer"] },
  { name: "CRM & Vendas", icon: "🤝", keywords: ["crm","salesforce","hubspot","customer","vendas","lead","pipeline","opportunity","deal","rfp-responder"] },
  { name: "Colaboração & Projetos", icon: "👥", keywords: ["collaboration","team","communication","scheduling","calendar","meeting","project","jira","trello","asana","notion","slack","teams","discord","zoom","confluence","sharepoint","atlassian"] },
  { name: "Outros", icon: "📦", keywords: [] }
];

export function categorize(name) {
  const lower = name.toLowerCase().replace(/[-_]/g, " ").trim();
  for (const cat of CATEGORIES) {
    for (const kw of cat.keywords) {
      if (lower.includes(kw.toLowerCase())) return cat;
    }
  }
  return CATEGORIES[CATEGORIES.length - 1]; // "Outros"
}

export function getCategories() { return CATEGORIES; }

// ─── LISTAR SKILLS ──────────────────────────────────────────────────────────
export async function listSkills(skillsDir) {
  let dir = skillsDir || path.resolve(process.cwd(), ".claude", "skills");
  if (!existsSync(dir)) {
    // Fallback: usa skills embutidas no pacote
    dir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "default-skills");
    if (!existsSync(dir)) return [];
  }
  const skills = (await readdir(dir)).filter(s => !s.startsWith(".") && !s.includes("CATALOG"));
  const result = [];
  for (const skill of skills) {
    let desc = "", content = "";
    const skillPath = path.join(dir, skill);
    if (existsSync(path.join(skillPath, "SKILL.md"))) {
      content = await readFile(path.join(skillPath, "SKILL.md"), "utf-8");
      const descMatch = content.match(/^description:\s*["']?([^"'\n]+)/m);
      desc = descMatch ? descMatch[1].trim().substring(0, 120) : "(sem descrição)";
    }
    const cat = categorize(skill);
    const lines = content.split("\n").length;
    const t1 = testQualidade(content);
    const t2 = testCapacidade(content);
    const t3 = testComplexidade(content);
    result.push({ name: skill, desc, category: cat.name, catIcon: cat.icon, t1, t2, t3, total: t1 + t2 + t3, lines });
  }
  return result;
}

// ─── 3 TESTES DE SCORE ──────────────────────────────────────────────────────
function testQualidade(content) {
  if (!content) return 0;
  let score = 0;
  const fm = content.startsWith("---") && content.indexOf("---", 3) > 0 ? content.substring(3, content.indexOf("---", 3)) : "";
  if (fm.includes("name:")) score += 5;
  if (fm.includes("description:")) score += 5;
  if (fm.includes("license:") || fm.includes("metadata:")) score += 5;
  if (content.match(/description:\s*["']?[^"'\n]{100,}/)) score += 10;
  const sections = content.match(/^##\s+\w+/gm);
  if (sections && sections.length >= 3) score += 5;
  if (sections && sections.length >= 6) score += 5;
  if (content.includes("```") || content.includes("exemplo") || content.includes("example") || content.includes("Usage")) score += 5;
  return Math.min(score, 40);
}

function testCapacidade(content) {
  if (!content) return 0;
  let score = 0;
  const body = content.toLowerCase();
  const frameworks = ["react","python","javascript","typescript","jest","pytest","docker","kubernetes","node","api","sdk","cli","git","npm","pip","webpack","vite","tailwind","django","express","next","vue","angular"];
  let fwCount = 0;
  for (const fw of frameworks) { if (body.includes(fw)) fwCount++; }
  score += Math.min(2 + (fwCount - 1), 10);
  const formatos = ["html","svg","json","md","pdf","png","csv","yaml"];
  for (const fmt of formatos) { if (body.includes(fmt)) score += 2; }
  if (content.includes("scripts/") || content.includes("assets/") || content.includes("templates/")) score += 8;
  if (body.includes("error") || body.includes("edge case") || body.includes("fallback")) score += 7;
  return Math.min(score, 35);
}

function testComplexidade(content) {
  if (!content) return 0;
  let score = 0;
  const lines = content.split("\n").length;
  const body = content.toLowerCase();
  if (lines > 80) score += 4;
  if (lines > 150) score += 4;
  if (body.includes("workflow") || body.includes("fluxo") || body.includes("processo") || body.includes("pipeline") || body.includes("passo")) score += 6;
  if (content.includes("version:") || content.includes("author:") || content.includes("updated:")) score += 6;
  if (body.includes("validation") || body.includes("verification") || body.includes("check") || body.includes("audit") || body.includes("test")) score += 5;
  return Math.min(score, 25);
}

// ─── INSTALAR / REMOVER (INDIVIDUAL) ────────────────────────────────────
export function installSkill(skill, scope = "local") {
  // Tenta via npx skills primeiro
  const cmd = `npx skills add "${skill}" -y${scope === "global" ? " -g" : ""}`;
  try {
    console.log(`  ⏳ Instalando ${skill} via npx...`);
    execSync(cmd, { cwd: process.cwd(), stdio: "pipe", timeout: 120000 });
    return true;
  } catch (e) {
    // Fallback: copia skill do diretório default-skills ou local
    console.log(`  ⏳ Instalando ${skill} via cópia local...`);
    try {
      // Remove extensão se já existir (listSkills retorna ex: lean-ctx.mdc)
      const skillName = skill.replace(/\.mdc$|\.md$/i, "");
      const src = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "default-skills", skillName + ".mdc");
      const skillsDir = path.resolve(process.cwd(), ".claude", "skills");
      if (!existsSync(skillsDir)) { mkdirSync(skillsDir, { recursive: true }); }
      const dest = path.join(skillsDir, skillName + ".mdc");
      if (existsSync(src)) {
        copyFileSync(src, dest);
        console.log(`  ✅ ${skillName} instalado localmente em .claude/skills/`);
        return true;
      }
      // Tenta achar o arquivo no diretório atual
      const localPath = path.resolve(process.cwd(), skillName + ".mdc");
      if (existsSync(localPath)) {
        copyFileSync(localPath, dest);
        console.log(`  ✅ ${skillName} instalado localmente`);
        return true;
      }
      console.error(`  ❌ ${skillName}: arquivo não encontrado`);
      return false;
    } catch (e2) {
      console.error(`  ❌ Erro ao copiar ${skill}: ${e2.message.substring(0, 80)}`);
      return false;
    }
  }
}

export function removeSkill(skill, scope = "local") {
  const cmd = `npx skills remove "${skill}"${scope === "global" ? " -g" : ""}`;
  try {
    console.log(`  ⏳ Removendo ${skill}...`);
    execSync(cmd, { cwd: process.cwd(), stdio: "pipe", timeout: 30000 });
    return true;
  } catch (e) {
    console.error(`  ❌ Erro ao remover ${skill}: ${e.message.substring(0, 80)}`);
    return false;
  }
}

// ─── INSTALAR / REMOVER EM LOTE (BATCH) ────────────────────────────────
/**
 * Instala multiplas skills em lote com fallback individual.
 * Retorna { success, installed, failed, errors[] }
 */
export function installBatch(skills, scope = "local") {
  if (!skills.length) return { success: true, installed: 0, failed: 0, errors: [] };

  const scopeFlag = scope === "global" ? " -g" : "";
  let installed = 0, failed = 0, errors = [];

  // Tenta batch completo primeiro
  const allQuoted = skills.map(s => `"${s}"`).join(" ");
  try {
    console.log(`  ⚡ [batch] Instalando ${skills.length} skills...`);
    execSync(`npx skills add ${allQuoted} -y${scopeFlag}`, {
      cwd: process.cwd(), stdio: "pipe", timeout: 180000
    });
    installed = skills.length;
    return { success: true, installed, failed: 0, errors: [] };
  } catch (e) {
    console.log(`  ⚠️ [batch] Falhou, tentando em lotes menores...`);
  }

  // Fallback: lotes de 5
  const batchSize = 5;
  for (let i = 0; i < skills.length; i += batchSize) {
    const batch = skills.slice(i, i + batchSize);
    const batchQuoted = batch.map(s => `"${s}"`).join(" ");
    try {
      execSync(`npx skills add ${batchQuoted} -y${scopeFlag}`, {
        cwd: process.cwd(), stdio: "pipe", timeout: 180000
      });
      installed += batch.length;
    } catch {
      // Fallback individual
      for (const skill of batch) {
        try {
          execSync(`npx skills add "${skill}" -y${scopeFlag}`, {
            cwd: process.cwd(), stdio: "pipe", timeout: 120000
          });
          installed++;
        } catch (e2) {
          failed++;
          errors.push({ skill, error: e2.message.substring(0, 100) });
        }
      }
    }
  }

  return { success: failed === 0, installed, failed, errors };
}

/**
 * Remove multiplas skills em lote.
 * Retorna { success, removed, failed, errors[] }
 */
export function removeBatch(skills, scope = "local") {
  if (!skills.length) return { success: true, removed: 0, failed: 0, errors: [] };

  let removed = 0, failed = 0, errors = [];
  for (const skill of skills) {
    try {
      execSync(`npx skills remove "${skill}"${scope === "global" ? " -g" : ""}`, {
        cwd: process.cwd(), stdio: "pipe", timeout: 30000
      });
      removed++;
    } catch (e) {
      failed++;
      errors.push({ skill, error: e.message.substring(0, 100) });
    }
  }
  return { success: failed === 0, removed, failed, errors };
}

// ─── SALVAR CONFIG ──────────────────────────────────────────────────────────
// ─── SALVAR / CARREGAR CONFIG ─────────────────────────────────────────
export async function saveConfig(config, configPath) {
  const dir = path.dirname(configPath);
  await mkdir(dir, { recursive: true });
  await writeFile(configPath, JSON.stringify(config, null, 2));
}

export async function loadConfig(configPath) {
  try {
    const data = await readFile(configPath, "utf-8");
    return JSON.parse(data);
  } catch { return { ides: [], skills: [], scope: "local", dashboard: true }; }
}

// ─── INICIAR SERVIDOR DASHBOARD ─────────────────────────────────────────
export function startDashboardServer(port = 3030) {
  const serverPath = path.resolve(
    path.dirname(fileURLToPath(new URL(import.meta.url))),
    "dashboard-server.mjs"
  );
  if (existsSync(serverPath)) {
    console.log(`  🖥️  Iniciando servidor na porta ${port}...`);
    const child = spawn("node", [serverPath, `--port=${port}`], {
      cwd: process.cwd(),
      stdio: "inherit",
      shell: true
    });
    child.on("error", (err) => console.error("  ❌ Erro no servidor:", err.message));
    child.on("exit", (code) => {
      if (code !== 0) console.log(`  ⏹️  Servidor encerrado (código ${code})`);
    });
  } else {
    console.error(`  ❌ Servidor não encontrado: ${serverPath}`);
  }
}
