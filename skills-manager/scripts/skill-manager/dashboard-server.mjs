#!/usr/bin/env node
/**
 * dashboard-server.mjs — Mini servidor HTTP para o Dashboard do Skill Manager
 *
 * Fornece API REST para:
 *   GET  /              → Dashboard HTML (template processado)
 *   GET  /api/config    → Config atual (skills ativas/inativas + metadados)
 *   POST /api/toggle    → Ativar/Desativar skill individual
 *   POST /api/save      → Salvar lista completa de skills ativas (batch)
 *   GET  /api/job/:id   → Poll resultado de job batch
 *
 * Uso: node scripts/skill-manager/dashboard-server.mjs [--port=3030]
 */
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const TEMPLATE_PATH = path.join(DIR, "dashboard", "template.html");
const CONFIG_PATH = path.resolve(process.cwd(), ".skill-manager-config.json");
const SKILLS_DIR = path.resolve(process.cwd(), ".claude", "skills");

const PORT = parseInt(process.argv.find(a => a.startsWith("--port="))?.split("=")[1] || "3030");
const HOST = "127.0.0.1";

// ─── ESTADO EM MEMÓRIA ─────────────────────────────────────────────────────
let estado = {
  activeSkills: [],
  allSkills: [],
  categories: [],
  activeCount: 0
};

// Jobs em andamento para polling
const jobs = new Map();
let jobCounter = 0;
let batchRunning = false; // guard contra dupla execução

// ─── CARREGAR SKILLS ──────────────────────────────────────────────────────
async function carregarSkills() {
  try {
    const { listSkills, categorize } = await import("./skill-core.mjs");
    const allSkills = await listSkills(SKILLS_DIR);

    // Agrupar por categoria
    const catMap = {};
    for (const s of allSkills) {
      const cat = categorize(s.name);
      if (!catMap[cat.name]) catMap[cat.name] = { icon: cat.icon, skills: [] };
      catMap[cat.name].skills.push(s);
    }

    // Ordenar categorias por quantidade
    const categories = Object.entries(catMap)
      .sort((a, b) => b[1].skills.length - a[1].skills.length)
      .map(([name, data]) => ({
        name,
        icon: data.icon,
        count: data.skills.length,
        skills: data.skills.sort((a, b) => b.total - a.total)
      }));

    // Carregar config
    let activeSkills = [];
    try {
      const configData = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
      activeSkills = configData.skills || [];
    } catch {
      activeSkills = [];
    }

    estado = {
      allSkills,
      categories,
      activeSkills,
      activeCount: activeSkills.length
    };
    return true;
  } catch (e) {
    console.error("  ❌ Erro ao carregar skills:", e.message);
    return false;
  }
}

// ─── GERAR HTML DO DASHBOARD ──────────────────────────────────────────────
function gerarDashboardHtml() {
  let template;
  try {
    template = fs.readFileSync(TEMPLATE_PATH, "utf-8");
  } catch {
    return "<html><body><h1>Erro: template.html não encontrado</h1></body></html>";
  }

  const colors = ["#6c63ff","#00d4aa","#ff6b9d","#ffaa33","#e91e63","#2196f3","#4caf50","#9c27b0","#ff5722","#00bcd4","#cddc39","#ff9800","#795548","#607d8b"];

  const catsHtml = estado.categories.map((cat, ci) => {
    const cor = colors[ci % colors.length];
    const activeCount = cat.skills.filter(s => estado.activeSkills.includes(s.name)).length;
    return `<div class="category">
      <div class="category-header" onclick="toggleCategory(this)">
        <span class="arrow open">&#9654;</span>
        <span>${cat.icon}</span>
        <h2>${cat.name}</h2>
        <span class="count">${cat.count}</span>
        <span class="active-count">${activeCount} ativas</span>
      </div>
      <div class="skills" data-category="${cat.name}">
      ${cat.skills.map(s => {
        const isActive = estado.activeSkills.includes(s.name);
        const scoreClass = s.total >= 70 ? "score-high" : s.total >= 40 ? "score-med" : "score-low";
        return `<div class="skill-card ${isActive ? "active" : ""}" data-skill="${s.name}" data-category="${cat.name}" style="border-left:3px solid ${cor}40">
          <label class="switch">
            <input type="checkbox" ${isActive ? "checked" : ""} onchange="toggleSkill(this, '${s.name}')">
            <span class="slider"></span>
            <span class="spinner"></span>
          </label>
          <div class="info">
            <div class="name" title="${s.name}">${s.name}</div>
            <div class="desc">${s.desc || "(sem descrição)"}</div>
          </div>
          <div class="score ${scoreClass}">${s.total}</div>
        </div>`;
      }).join("\n      ")}
      </div>
    </div>`;
  }).join("\n  ");

  const maxScore = Math.max(...estado.allSkills.map(s => s.total), 0);

  return template
    .replace("{{TOTAL_SKILLS}}", estado.allSkills.length.toString())
    .replace("{{TOTAL_CATEGORIES}}", estado.categories.length.toString())
    .replace("{{ACTIVE_SKILLS}}", estado.activeCount.toString())
    .replace("{{SCORE_MAX}}", maxScore.toString())
    .replace("{{CATEGORIES_HTML}}", catsHtml)
    .replace("{{SERVER_STATUS_CLASS}}", "server-online")
    .replace("{{SERVER_STATUS_TEXT}}", "🟢 Servidor online — alterações em tempo real")
    .replace("{{LAST_SYNC}}", new Date().toLocaleString("pt-BR"));
}

// ─── API HANDLERS ──────────────────────────────────────────────────────────
function handleApiConfig() {
  return JSON.stringify({
    allSkills: estado.allSkills.map(s => ({ name: s.name, desc: s.desc, total: s.total, category: s.category })),
    activeSkills: estado.activeSkills,
    categories: estado.categories.map(c => ({ name: c.name, icon: c.icon, count: c.count })),
    activeCount: estado.activeCount,
    totalSkills: estado.allSkills.length,
    totalCategories: estado.categories.length
  });
}

async function handleApiToggle(body) {
  const { skill, active } = body;
  if (!skill) return { success: false, error: "skill name required" };

  try {
    if (active) {
      // Instalar a skill
      execSync(`npx skills add "${skill}" -y`, { cwd: process.cwd(), stdio: "pipe", timeout: 120000 });
      if (!estado.activeSkills.includes(skill)) {
        estado.activeSkills.push(skill);
      }
    } else {
      // Remover a skill
      execSync(`npx skills remove "${skill}"`, { cwd: process.cwd(), stdio: "pipe", timeout: 30000 });
      estado.activeSkills = estado.activeSkills.filter(s => s !== skill);
    }

    estado.activeCount = estado.activeSkills.length;

    // Persistir config
    salvarConfig();

    return { success: true, skill, active, activeCount: estado.activeCount };
  } catch (e) {
    return { success: false, error: e.message.substring(0, 200) };
  }
}

async function handleApiSave(body) {
  const { activeSkills } = body;
  if (!Array.isArray(activeSkills)) return { success: false, error: "activeSkills array required" };
  if (batchRunning) return { success: false, error: "batch job already running, aguarde conclusao" };

  const jobId = ++jobCounter;
  const job = {
    id: jobId,
    status: "running",
    installed: 0,
    removed: 0,
    errors: [],
    message: "Iniciando...",
    completed: false,
    activeSkills: []
  };
  jobs.set(jobId, job);

  // Executar em background (assíncrono)
  executeBatch(job, activeSkills);

  return { success: true, jobId };
}

async function executeBatch(job, desiredActive) {
  batchRunning = true;
  try {
    await executeBatchInternal(job, desiredActive);
  } finally {
    batchRunning = false;
  }
}

async function executeBatchInternal(job, desiredActive) {
  const currentActive = [...estado.activeSkills];

  // Skills para instalar (nao estao ativas mas deveriam)
  const toInstall = desiredActive.filter(s => !currentActive.includes(s));
  // Skills para remover (estao ativas mas nao deveriam)
  const toRemove = currentActive.filter(s => !desiredActive.includes(s));

  job.message = `📦 ${toInstall.length} para instalar, ${toRemove.length} para remover...`;

  let installed = 0, removed = 0, errors = [];

  // Batch install: unir todas em um comando (o npx skills add aceita multiplos nomes)
  if (toInstall.length > 0) {
    job.message = `📦 Instalando ${toInstall.length} skills em lote...`;
    // Install em lotes de 5 para nao estourar o argumento
    const batchSize = 5;
    for (let i = 0; i < toInstall.length; i += batchSize) {
      const batch = toInstall.slice(i, i + batchSize);
      try {
        execSync(`npx skills add ${batch.map(s => `"${s}"`).join(" ")} -y`, {
          cwd: process.cwd(), stdio: "pipe", timeout: 180000
        });
        installed += batch.length;
        job.message = `📦 Instalando... ${installed}/${toInstall.length}`;
      } catch (e) {
        // Tentar uma a uma para isolar falha
        for (const s of batch) {
          try {
            execSync(`npx skills add "${s}" -y`, {
              cwd: process.cwd(), stdio: "pipe", timeout: 120000
            });
            installed++;
          } catch (e2) {
            errors.push({ skill: s, error: e2.message.substring(0, 100) });
          }
        }
      }
    }
  }

  // Batch remove: igual
  if (toRemove.length > 0) {
    job.message = `🗑️ Removendo ${toRemove.length} skills em lote...`;
    for (const skill of toRemove) {
      try {
        execSync(`npx skills remove "${skill}"`, {
          cwd: process.cwd(), stdio: "pipe", timeout: 30000
        });
        removed++;
      } catch (e) {
        errors.push({ skill, error: e.message.substring(0, 100) });
      }
    }
  }

  // Atualizar estado
  estado.activeSkills = [...desiredActive];
  estado.activeCount = estado.activeSkills.length;
  salvarConfig();

  // Finalizar job
  Object.assign(job, {
    status: "completed",
    completed: true,
    installed,
    removed,
    errors,
    activeCount: estado.activeCount,
    success: errors.length === 0 || installed > 0,
    message: errors.length > 0
      ? `✅ ${installed} instaladas, ${removed} removidas, ${errors.length} erros`
      : `✅ ${installed} instaladas, ${removed} removidas — sucesso total!`
  });
}

function handleApiJob(jobId) {
  const job = jobs.get(parseInt(jobId));
  if (!job) return JSON.stringify({ success: false, error: "job not found" });
  return JSON.stringify({
    completed: job.completed,
    success: job.success,
    installed: job.installed,
    removed: job.removed,
    errors: job.errors,
    activeCount: job.activeCount,
    message: job.message,
    status: job.status
  });
}

function salvarConfig() {
  try {
    fs.writeFileSync(CONFIG_PATH, JSON.stringify({
      ides: [],
      skills: estado.activeSkills,
      scope: "local",
      dashboard: true,
      installedAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }, null, 2));
  } catch (e) {
    console.error("  ⚠️ Erro ao salvar config:", e.message);
  }
}

// ─── PARSE BODY ────────────────────────────────────────────────────────────
function parseBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", chunk => data += chunk);
    req.on("end", () => {
      try { resolve(JSON.parse(data)); }
      catch { resolve({}); }
    });
    req.on("error", reject);
  });
}

// ─── SERVER ────────────────────────────────────────────────────────────────
async function start() {
  console.log("  ⏳ Carregando skills...");
  const loaded = await carregarSkills();
  if (!loaded) {
    console.log("  ⚠️ Nenhuma skill encontrada. O dashboard será gerado vazio.");
  }

  const server = http.createServer(async (req, res) => {
    // CORS
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");

    if (req.method === "OPTIONS") {
      res.writeHead(204);
      return res.end();
    }

    const url = new URL(req.url, `http://${HOST}:${PORT}`);
    const pathname = url.pathname;

    try {
      // Dashboard HTML
      if (pathname === "/" || pathname === "/index.html") {
        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        return res.end(gerarDashboardHtml());
      }

      // API: GET config
      if (pathname === "/api/config" && req.method === "GET") {
        res.writeHead(200, { "Content-Type": "application/json" });
        return res.end(handleApiConfig());
      }

      // API: POST toggle (skill individual)
      if (pathname === "/api/toggle" && req.method === "POST") {
        const body = await parseBody(req);
        const result = await handleApiToggle(body);
        res.writeHead(200, { "Content-Type": "application/json" });
        return res.end(JSON.stringify(result));
      }

      // API: POST save (batch completo)
      if (pathname === "/api/save" && req.method === "POST") {
        const body = await parseBody(req);
        const result = await handleApiSave(body);
        res.writeHead(200, { "Content-Type": "application/json" });
        return res.end(JSON.stringify(result));
      }

      // API: GET job status
      const jobMatch = pathname.match(/^\/api\/job\/(\d+)$/);
      if (jobMatch && req.method === "GET") {
        res.writeHead(200, { "Content-Type": "application/json" });
        return res.end(handleApiJob(jobMatch[1]));
      }

      // Favicon (silencioso)
      if (pathname === "/favicon.ico") {
        res.writeHead(204);
        return res.end();
      }

      // 404
      res.writeHead(404);
      res.end(JSON.stringify({ error: "not found" }));
    } catch (e) {
      console.error("  ❌ Erro no servidor:", e.message);
      res.writeHead(500);
      res.end(JSON.stringify({ error: e.message }));
    }
  });

  server.listen(PORT, HOST, () => {
    console.log(`\n📊 Skill Manager Dashboard Server`);
    console.log(`   ${"=".repeat(50)}`);
    console.log(`   🔗  http://${HOST}:${PORT}`);
    console.log(`   🖥️  ${estado.allSkills.length} skills · ${estado.categories.length} categorias`);
    console.log(`   ✅  ${estado.activeCount} ativas`);
    console.log(`   📁  Ctrl+C para parar o servidor\n`);
  });
}

start().catch(e => {
  console.error("❌ Erro fatal:", e);
  process.exit(1);
});
