#!/usr/bin/env node
/**
 * skill-manager.mjs — Skill Manager Dashboard + TUI
 * 
 * Uso: node scripts/skill-manager/skill-manager.mjs
 * 
 * Fluxo:
 * 1. Seleciona IDEs (multi-select)
 * 2. Escolhe skills por categoria (como OMP Harness)
 * 3. Escolhe escopo (local, global, ambos)
 * 4. Escolhe se instala dashboard visual
 * 5. SUBMIT → instala tudo
 * 6. Painel visual para ativar/desativar skills
 */
import enquirer from "enquirer";
import { listSkills, categorize, installSkill, removeSkill, saveConfig, loadConfig, getCategories, installBatch, removeBatch } from "./skill-core.mjs";
import { getAllIdes, getIde, generateInstallCommand, generateIdeConfig } from "./ides-config.mjs";
import { mkdir, writeFile, readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { execSync, spawn } from "node:child_process";

const { prompt, MultiSelect, Select, Form } = enquirer;
const CONFIG_PATH = path.resolve(process.cwd(), ".skill-manager-config.json");
const SKILLS_DIR = path.resolve(process.cwd(), ".claude", "skills");

// ─── PASSO 1: SELECIONAR IDES ─────────────────────────────────────────────
async function stepSelectIdes() {
  console.log("\n🖥️  SKILL MANAGER — Selecione as IDEs para instalar as skills\n");
  console.log("  (Use ESPAÇO para marcar/desmarcar, ENTER para confirmar)\n");

  const ides = getAllIdes();
  const response = await new MultiSelect({
    name: "ides",
    message: "Quais IDEs voce usa?",
    choices: ides.map(ide => ({
      name: ide.id,
      message: `${ide.icon} ${ide.name}`,
      hint: ide.description.substring(0, 50) + "..."
    })),
    validate: (selected) => selected.length === 0 ? "Selecione pelo menos uma IDE" : true
  }).run().catch(() => []);

  return Array.isArray(response) ? response : [];
}

// ─── PASSO 2: SELECIONAR CATEGORIAS/SKILLS ───────────────────────────────
async function stepSelectSkills(selectedIdes) {
  console.log("\n📦 CARREGANDO SKILLS DISPONIVEIS...\n");

  const allSkills = await listSkills(SKILLS_DIR);
  const categories = {};
  
  for (const skill of allSkills) {
    const cat = categorize(skill.name);
    if (!categories[cat.name]) categories[cat.name] = [];
    categories[cat.name].push(skill);
  }

  const catChoices = Object.entries(categories)
    .filter(([_, skills]) => skills.length > 0)
    .sort((a, b) => b[1].length - a[1].length)
    .map(([cat, skills]) => ({
      name: cat,
      message: `${skills[0]?.catIcon || "📦"} ${cat}`,
      hint: `${skills.length} skills disponiveis`
    }));

  console.log("  Selecione as CATEGORIAS de skills que deseja instalar:");
  console.log("  (Use ESPAÇO para marcar, ENTER para confirmar)\n");

  const selectedCats = await new MultiSelect({
    name: "categories",
    message: "Quais categorias de skills instalar?",
    choices: catChoices,
    validate: (selected) => selected.length === 0 ? "Selecione pelo menos uma categoria" : true
  }).run().catch(() => []);

  if (!Array.isArray(selectedCats) || selectedCats.length === 0) return [];

  // Para cada categoria selecionada, mostrar skills individuais
  const allSelected = [];
  for (const cat of selectedCats) {
    const skills = categories[cat].sort((a, b) => b.total - a.total);
    
    const skillChoices = skills.map(s => ({
      name: s.name,
      message: `${s.name}`,
      hint: `Score: ${s.total}/100 | ${s.desc.substring(0, 40)}`,
      checked: s.total >= 50 // auto-check skills com score >= 50
    }));

    const selectedSkills = await new MultiSelect({
      name: cat.replace(/[^a-z]/gi, "_"),
      message: `${skills[0]?.catIcon || "📦"} ${cat} — Selecione as skills`,
      choices: skillChoices,
      validate: (selected) => selected.length === 0 ? "Selecione pelo menos uma skill ou ESC para pular" : true
    }).run().catch(() => []);

    if (Array.isArray(selectedSkills)) {
      allSelected.push(...selectedSkills);
    }
  }

  return allSelected;
}

// ─── PASSO 3: ESCOLHER ESCOPO ────────────────────────────────────────────
async function stepSelectScope() {
  console.log("\n🌐 DEFININDO ESCOPO DE INSTALAÇÃO...\n");

  const response = await new Select({
    name: "scope",
    message: "Onde instalar as skills?",
    choices: [
      { name: "local", message: "📁 Apenas no projeto atual (recomendado)" },
      { name: "global", message: "🌍 Apenas global (todas as IDEs, todos projetos)" },
      { name: "both", message: "🔄 Ambos (projeto + global)" }
    ]
  }).run().catch(() => "local");

  return response || "local";
}

// ─── PASSO 4: DASHBOARD ──────────────────────────────────────────────────
async function stepDashboard() {
  console.log("\n📊 PAINEL VISUAL...\n");

  const response = await new Select({
    name: "dashboard",
    message: "Deseja instalar o painel visual para gerenciar skills?",
    choices: [
      { name: "yes", message: "✅ Sim, instalar painel visual com categorias e ranking" },
      { name: "no", message: "❌ Não, apenas instalar skills via terminal" }
    ]
  }).run().catch(() => "yes");

  return response === "yes";
}

// ─── PASSO 5: RESUMO E SUBMIT ───────────────────────────────────────────
async function stepConfirm(ides, skills, scope, dashboard) {
  console.log("\n" + "=".repeat(60));
  console.log("📋 RESUMO DA INSTALAÇÃO");
  console.log("=".repeat(60));
  console.log(`\n🎯 IDEs: ${ides.length} selecionadas`);
  for (const ideId of ides) {
    const ide = getIde(ideId);
    if (ide) console.log(`   ${ide.icon} ${ide.name}`);
  }
  console.log(`\n📦 Skills: ${skills.length} selecionadas`);
  const grouped = {};
  for (const s of skills) {
    const cat = categorize(s);
    if (!grouped[cat.name]) grouped[cat.name] = [];
    grouped[cat.name].push(s);
  }
  for (const [cat, skList] of Object.entries(grouped)) {
    console.log(`   ${skList[0]?.catIcon || "📦"} ${cat}: ${skList.join(", ")}`);
  }
  console.log(`\n🌐 Escopo: ${scope === "local" ? "📁 Apenas local" : scope === "global" ? "🌍 Global" : "🔄 Local + Global"}`);
  console.log(`📊 Painel Visual: ${dashboard ? "✅ Sim" : "❌ Não"}`);
  console.log(`\n📁 Config salva em: ${CONFIG_PATH}\n`);

  const response = await new Select({
    name: "confirm",
    message: "Confirmar e instalar?",
    choices: [
      { name: "yes", message: "✅ Sim, instalar agora!" },
      { name: "no", message: "❌ Não, quero revisar" },
      { name: "cancel", message: "🚫 Cancelar" }
    ]
  }).run().catch(() => "cancel");

  return response || "cancel";
}

// ─── INSTALAR (BATCH) ───────────────────────────────────────────────────
async function doInstall(ides, skills, scope, dashboard) {
  console.log("\n⏳ INSTALANDO EM LOTE...\n");

  // Escopos a processar
  const scopes = scope === "both" ? ["local", "global"] : [scope];
  let totalInstalled = 0, totalFailed = 0;

  for (const s of scopes) {
    console.log(`  🌐 Escopo: ${s === "local" ? "📁 Local" : "🌍 Global"}`);

    const result = installBatch(skills, s);
    totalInstalled += result.installed;
    totalFailed += result.failed;

    if (result.errors.length > 0) {
      console.log(`  ⚠️  ${result.errors.length} erro(s):`);
      result.errors.slice(0, 5).forEach(e =>
        console.log(`     ❌ ${e.skill}: ${e.error.substring(0, 60)}`)
      );
      if (result.errors.length > 5) {
        console.log(`     ... e mais ${result.errors.length - 5} erro(s)`);
      }
    }
  }

  // Salvar config
  await saveConfig({
    ides,
    skills,
    scope,
    dashboard,
    installedAt: new Date().toISOString()
  }, CONFIG_PATH);

  if (dashboard) {
    await installDashboard();
  }

  console.log("\n" + "=".repeat(60));
  console.log("✅ INSTALAÇÃO CONCLUÍDA!");
  console.log("=".repeat(60));
  console.log(`   ✅ ${totalInstalled} instaladas | ❌ ${totalFailed} falhas`);
  console.log(`   📁 Config: ${CONFIG_PATH}`);
  if (dashboard) {
    console.log(`   📊 Dashboard: scripts/skill-manager/dashboard/index.html`);
    console.log(`   🖥️  Servidor: node scripts/skill-manager/dashboard-server.mjs`);
  }
}

// ─── INSTALAR DASHBOARD ─────────────────────────────────────────────────
async function installDashboard() {
  const dashDir = path.resolve(process.cwd(), "scripts", "skill-manager", "dashboard");
  await mkdir(dashDir, { recursive: true });

  // Processar template
  const templatePath = path.join(dashDir, "template.html");
  const indexPath = path.join(dashDir, "index.html");

  if (!existsSync(templatePath)) {
    console.log("  ⚠️ Template não encontrado. Gerando dashboard inline...");
    // Fallback: gerar inline (legado)
    const allSkills = await listSkills(SKILLS_DIR);
    const config = await loadConfig(CONFIG_PATH);
    const activeSkills = config.skills || [];
    const html = generateDashboardHtml(allSkills, activeSkills);
    await writeFile(indexPath, html);
    return;
  }

  // Copiar template como dashboard inicial
  const template = await readFile(templatePath, "utf-8");
  const allSkills = await listSkills(SKILLS_DIR);
  const config = await loadConfig(CONFIG_PATH);
  const activeSkills = config.skills || [];

  // Processar placeholders mínimos para versão estática
  const categories = {};
  for (const s of allSkills) {
    const cat = categorize(s.name);
    if (!categories[cat.name]) categories[cat.name] = { icon: cat.icon, skills: [] };
    categories[cat.name].skills.push(s);
  }

  let html = template
    .replace(/\{\{TOTAL_SKILLS\}\}/g, allSkills.length.toString())
    .replace(/\{\{TOTAL_CATEGORIES\}\}/g, Object.keys(categories).length.toString())
    .replace(/\{\{ACTIVE_SKILLS\}\}/g, activeSkills.length.toString())
    .replace(/\{\{SCORE_MAX\}\}/g, Math.max(...allSkills.map(s => s.total), 0).toString())
    .replace(/\{\{SERVER_STATUS_CLASS\}\}/g, "server-offline")
    .replace(/\{\{SERVER_STATUS_TEXT\}\}/g, "🔴 Servidor offline — inicie com node scripts/skill-manager/dashboard-server.mjs")
    .replace(/\{\{LAST_SYNC\}\}/g, new Date().toLocaleString("pt-BR"));

  // Placeholder de categorias (será preenchido pelo servidor)
  html = html.replace("{{CATEGORIES_HTML}}", "<p style='text-align:center;color:#555577'>Carregando... Inicie o servidor para visualizar.</p>");

  await writeFile(indexPath, html);
  console.log("  📊 Dashboard visual instalado em scripts/skill-manager/dashboard/index.html");
  console.log(`  🖥️  Inicie o servidor: node scripts/skill-manager/dashboard-server.mjs`);
}

// ─── GERAR DASHBOARD HTML ──────────────────────────────────────────────
function generateDashboardHtml(allSkills, activeSkills) {
  const categories = {};
  for (const skill of allSkills) {
    const cat = categorize(skill.name);
    if (!categories[cat.name]) categories[cat.name] = { icon: cat.icon, skills: [] };
    categories[cat.name].skills.push(skill);
  }

  const sortedCats = Object.entries(categories).sort((a, b) => b[1].skills.length - a[1].skills.length);
  const colors = ["#6c63ff","#00d4aa","#ff6b9d","#ffaa33","#e91e63","#2196f3","#4caf50","#9c27b0","#ff5722","#00bcd4","#cddc39","#ff9800","#795548","#607d8b"];

  return `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Skill Manager — Painel de Controle</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
  *{margin:0;padding:0;box-sizing:border-box}body{background:#050510;color:#e0e0ff;font-family:'Inter',sans-serif;min-height:100vh}
  .hero{text-align:center;padding:3rem 2rem 2rem;position:relative;overflow:hidden}
  .hero::before{content:'';position:absolute;top:-50%;left:50%;transform:translateX(-50%);width:800px;height:800px;background:radial-gradient(circle,rgba(108,99,255,0.06),transparent 70%)}
  .hero h1{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:800;letter-spacing:-.03em;margin-bottom:.3rem}
  .hero h1 span{background:linear-gradient(135deg,#6c63ff,#00d4aa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
  .hero p{color:#8888bb;font-size:.85rem}
  .hero .stats{display:flex;justify-content:center;gap:2rem;margin-top:1.5rem;font-size:.8rem}
  .hero .stats div{text-align:center}
  .hero .stats .num{font-size:1.2rem;font-weight:700;color:#6c63ff}
  .hero .stats .lab{color:#555577;font-size:.7rem;text-transform:uppercase}
  .controls{text-align:center;padding:0 2rem 1rem;display:flex;justify-content:center;gap:.5rem;flex-wrap:wrap}
  .controls input{padding:.5rem 1rem;border-radius:8px;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.02);color:#e0e0ff;font-size:.8rem;width:250px;font-family:'Inter',sans-serif}
  .controls input::placeholder{color:#555577}
  .controls button{padding:.5rem 1rem;border-radius:8px;border:1px solid rgba(108,99,255,.3);background:rgba(108,99,255,.1);color:#6c63ff;cursor:pointer;font-size:.8rem;transition:all .2s}
  .controls button:hover{background:rgba(108,99,255,.2)}
  .container{max-width:1100px;margin:0 auto;padding:1rem 2rem 3rem}
  .category{margin-bottom:2rem}
  .category-header{display:flex;align-items:center;gap:.5rem;padding:.5rem 0;margin-bottom:.5rem;border-bottom:1px solid rgba(255,255,255,.04);cursor:pointer;user-select:none}
  .category-header .toggle{font-size:.7rem;color:#555577;transition:transform .2s}
  .category-header .toggle.open{transform:rotate(90deg)}
  .category-header h2{font-size:1rem;font-weight:600}
  .category-header .count{font-size:.7rem;color:#555577;background:rgba(255,255,255,.04);padding:.1rem .5rem;border-radius:100px}
  .category-header .active-count{font-size:.7rem;color:#00d4aa}
  .skills{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:.5rem}
  .skill-card{display:flex;align-items:center;gap:.6rem;padding:.6rem .8rem;border-radius:10px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.04);transition:all .2s}
  .skill-card:hover{background:rgba(255,255,255,.04)}
  .skill-card.active{border-color:rgba(0,212,170,.2);background:rgba(0,212,170,.04)}
  .skill-card .switch{position:relative;width:36px;height:20px;flex-shrink:0}
  .skill-card .switch input{opacity:0;width:0;height:0}
  .skill-card .switch .slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background:rgba(255,255,255,.08);transition:.3s;border-radius:10px}
  .skill-card .switch .slider:before{content:"";position:absolute;height:16px;width:16px;left:2px;bottom:2px;background:#555577;transition:.3s;border-radius:50%}
  .skill-card .switch input:checked+.slider{background:rgba(0,212,170,.3)}
  .skill-card .switch input:checked+.slider:before{transform:translateX(16px);background:#00d4aa}
  .skill-card .info{flex:1;min-width:0}
  .skill-card .info .name{font-size:.8rem;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .skill-card .info .desc{font-size:.65rem;color:#8888bb;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .skill-card .score{font-size:.7rem;font-weight:600;padding:.15rem .4rem;border-radius:4px;flex-shrink:0}
  .score-high{color:#00d4aa;background:rgba(0,212,170,.1)}
  .score-med{color:#ffaa33;background:rgba(255,170,51,.1)}
  .score-low{color:#ff6b6b;background:rgba(255,107,107,.1)}
  .actions{text-align:center;padding:1rem 2rem 2rem;display:flex;justify-content:center;gap:.5rem}
  .actions button{padding:.6rem 1.5rem;border-radius:10px;border:none;font-weight:600;cursor:pointer;font-size:.85rem;transition:all .2s}
  .btn-primary{background:linear-gradient(135deg,#6c63ff,#00d4aa);color:#fff}
  .btn-primary:hover{transform:translateY(-2px);box-shadow:0 4px 20px rgba(108,99,255,.3)}
  .btn-secondary{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08)!important;color:#e0e0ff}
  .btn-secondary:hover{background:rgba(255,255,255,.08)}
  footer{text-align:center;padding:2rem;color:#555577;font-size:.7rem}
  .hidden{display:none}
  </style></head><body>
  <section class="hero">
    <h1>Skill Manager <span>Dashboard</span></h1>
    <p>Gerencie suas skills por categoria · Ative/Desative com um clique</p>
    <div class="stats">
      <div><div class="num">${allSkills.length}</div><div class="lab">Skills</div></div>
      <div><div class="num">${sortedCats.length}</div><div class="lab">Categorias</div></div>
      <div><div class="num">${activeSkills.length}</div><div class="lab">Ativas</div></div>
    </div>
  </section>
  <div class="controls">
    <input type="text" id="search" placeholder="🔍 Buscar skills..." oninput="filterSkills(this.value)">
    <button onclick="toggleAll()">Toggle Todos</button>
    <button onclick="expandAll()">Expandir Todos</button>
    <button onclick="collapseAll()">Recolher Todos</button>
  </div>
  <div class="container" id="container">
  ${sortedCats.map(([cat, data], ci) => {
    const cor = colors[ci % colors.length];
    const sorted = data.skills.sort((a, b) => b.total - a.total);
    const activeCount = sorted.filter(s => activeSkills.includes(s.name)).length;
    return `<div class="category">
      <div class="category-header" onclick="toggleCategory(this)">
        <span class="toggle open">&#9654;</span>
        <span>${data.icon}</span>
        <h2>${cat}</h2>
        <span class="count">${sorted.length}</span>
        <span class="active-count">${activeCount} ativas</span>
      </div>
      <div class="skills" data-category="${cat}">
      ${sorted.map(s => {
        const isActive = activeSkills.includes(s.name);
        const scoreClass = s.total >= 70 ? "score-high" : s.total >= 40 ? "score-med" : "score-low";
        return `<div class="skill-card ${isActive ? "active" : ""}" data-skill="${s.name}" data-category="${cat}">
          <label class="switch">
            <input type="checkbox" ${isActive ? "checked" : ""} onchange="toggleSkill('${s.name}', this.checked)">
            <span class="slider"></span>
          </label>
          <div class="info">
            <div class="name" title="${s.name}">${s.name}</div>
            <div class="desc">${s.desc || "(sem descrição)"}</div>
          </div>
          <div class="score ${scoreClass}">${s.total}</div>
        </div>`;
      }).join("\n        ")}
      </div>
    </div>`;
  }).join("\n  ")}
  </div>
  <div class="actions">
    <button class="btn-primary" onclick="saveChanges()">💾 Salvar Alterações</button>
    <button class="btn-secondary" onclick="window.location.href='../../skill-manager.mjs'">🔄 Reabrir TUI</button>
  </div>
  <footer>Skill Manager Dashboard · Gerado em ${new Date().toISOString().split("T")[0]} · Fabrica Agentica de Livros</footer>
  <script>
    function toggleCategory(header) {
      const toggle = header.querySelector(".toggle");
      const skills = header.nextElementSibling;
      toggle.classList.toggle("open");
      skills.classList.toggle("hidden");
    }

    function toggleSkill(skillName, active) {
      const cards = document.querySelectorAll(\`.skill-card[data-skill="\${skillName}"]\`);
      cards.forEach(c => {
        c.classList.toggle("active", active);
        c.querySelector("input").checked = active;
      });
      updateCounts();
    }

    function updateCounts() {
      document.querySelectorAll(".category").forEach(cat => {
        const skills = cat.querySelector(".skills");
        const catName = skills.dataset.category;
        const active = skills.querySelectorAll('.skill-card.active').length;
        const total = skills.querySelectorAll('.skill-card').length;
        cat.querySelector(".active-count").textContent = active + " ativas";
      });
    }

    function filterSkills(query) {
      const q = query.toLowerCase();
      document.querySelectorAll(".skill-card").forEach(card => {
        const name = card.dataset.skill.toLowerCase();
        const desc = card.querySelector(".desc").textContent.toLowerCase();
        card.style.display = name.includes(q) || desc.includes(q) ? "flex" : "none";
      });
      document.querySelectorAll(".category").forEach(cat => {
        const visible = cat.querySelectorAll('.skill-card[style*="display: flex"], .skill-card:not([style])').length;
        cat.style.display = visible > 0 ? "block" : "none";
      });
    }

    function toggleAll() {
      const allActive = document.querySelectorAll(".skill-card.active").length;
      const allTotal = document.querySelectorAll(".skill-card").length;
      const turnOn = allActive < allTotal / 2;
      document.querySelectorAll(".skill-card").forEach(card => {
        const cb = card.querySelector("input");
        if (cb.checked !== turnOn) {
          cb.checked = turnOn;
          card.classList.toggle("active", turnOn);
        }
      });
      updateCounts();
    }

    function expandAll() {
      document.querySelectorAll(".skills").forEach(s => s.classList.remove("hidden"));
      document.querySelectorAll(".toggle").forEach(t => t.classList.add("open"));
    }

    function collapseAll() {
      document.querySelectorAll(".skills").forEach(s => s.classList.add("hidden"));
      document.querySelectorAll(".toggle").forEach(t => t.classList.remove("open"));
    }

    function saveChanges() {
      const active = [];
      document.querySelectorAll(".skill-card.active").forEach(card => {
        active.push(card.dataset.skill);
      });
      
      // Salvar no localStorage
      localStorage.setItem("skill-manager-active", JSON.stringify(active));
      
      // Mostrar feedback
      const btn = document.querySelector(".btn-primary");
      const orig = btn.textContent;
      btn.textContent = "✅ Salvo!";
      btn.style.background = "linear-gradient(135deg,#00d4aa,#00d4aa)";
      setTimeout(() => {
        btn.textContent = orig;
        btn.style.background = "";
      }, 2000);
      
      // Gerar download do JSON
      const config = { active, timestamp: new Date().toISOString() };
      const blob = new Blob([JSON.stringify(config, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "skill-manager-config.json";
      a.click();
      URL.revokeObjectURL(url);
    }

    // Restaurar estado do localStorage
    try {
      const saved = JSON.parse(localStorage.getItem("skill-manager-active") || "[]");
      if (saved.length > 0) {
        document.querySelectorAll(".skill-card").forEach(card => {
          const isActive = saved.includes(card.dataset.skill);
          card.classList.toggle("active", isActive);
          card.querySelector("input").checked = isActive;
        });
        updateCounts();
      }
    } catch(e) {}
  </script>
  </body></html>`;
}

// ─── MAIN ─────────────────────────────────────────────────────────────────
async function main() {
  console.log("\n" + "█".repeat(60));
  console.log("  🛠️  SKILL MANAGER — Gerenciador de Skills Multi-IDE");
  console.log("█".repeat(60) + "\n");

  // Verificar se já existe config
  const existing = await loadConfig(CONFIG_PATH);
  if (existing.ides && existing.ides.length > 0) {
    const response = await new Select({
      name: "mode",
      message: "Configuracao existente encontrada. O que deseja fazer?",
      choices: [
        { name: "reinstall", message: "🔄 Reinstalar com nova configuracao" },
        { name: "dashboard", message: "📊 Abrir painel visual (dashboard)" },
        { name: "serve", message: "🖥️ Iniciar servidor HTTP do dashboard" },
        { name: "cancel", message: "🚫 Sair" }
      ]
    }).run().catch(() => "cancel");

    if (response === "dashboard") {
      console.log("\n📊 Abrindo dashboard...");
      console.log("   scripts/skill-manager/dashboard/index.html");
      console.log("   Abra este arquivo no navegador.");
      console.log("   Ou inicie o servidor: node scripts/skill-manager/dashboard-server.mjs\n");
      return;
    }
    if (response === "serve") {
      console.log("\n🖥️ Iniciando servidor HTTP...\n");
      const { startDashboardServer } = await import("./skill-core.mjs");
      startDashboardServer(3030);
      return;
    }
    if (response !== "reinstall") {
      console.log("👋 Até logo!\n");
      return;
    }
  }

  // Fluxo completo
  const ides = await stepSelectIdes();
  if (!ides || ides.length === 0) { console.log("\n👋 Até logo!\n"); return; }

  const skills = await stepSelectSkills(ides);
  if (!skills || skills.length === 0) { console.log("\n👋 Até logo!\n"); return; }

  const scope = await stepSelectScope();
  const dashboard = await stepDashboard();

  const confirm = await stepConfirm(ides, skills, scope, dashboard);
  if (confirm === "cancel") { console.log("\n👋 Instalação cancelada.\n"); return; }
  if (confirm === "no") {
    console.log("\n🔄 Refazendo...\n");
    return await main();
  }

  await doInstall(ides, skills, scope, dashboard);

  // Perguntar se quer iniciar servidor
  if (dashboard) {
    console.log("\n" + "=".repeat(60));
    const startServer = await new Select({
      name: "startServer",
      message: "Deseja iniciar o servidor HTTP do dashboard agora?",
      choices: [
        { name: "yes", message: "🖥️ Sim, iniciar servidor na porta 3030" },
        { name: "no", message: "⏭️ Não, vou iniciar depois" }
      ]
    }).run().catch(() => "no");

    if (startServer === "yes") {
      console.log("\n🖥️ Iniciando servidor HTTP do dashboard...\n");
      const { startDashboardServer } = await import("./skill-core.mjs");
      startDashboardServer(3030);
    }
  }
}

main().catch(e => { console.error("ERRO:", e); process.exit(1); });
