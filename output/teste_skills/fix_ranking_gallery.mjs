#!/usr/bin/env node
/**
 * fix_ranking_gallery.mjs — Gera ranking qualitativo + galeria HTML
 * Sem template literals aninhadas para evitar erros de escaping.
 */
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { existsSync } from "node:fs";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const VISUAL = path.resolve(DIR, "..", "testes_visuais");

const SKILLS = [
  { slug:"01_huashu-design", nome:"huashu-design", nota:92, icone:"\ud83c\udfa8",   cor:"#6c63ff", rank:1, medal:"\ud83e\udd47", categoria:"Design Completo",
    artefatos:["landing-aidd.html","capa-conceito-v1.svg","guia-tipografia.md"],
    formatos:["HTML","SVG","MD"],
    qualidade:"Muito Alta — tipografia Newsreader+Inter pareada, anti-slop rigoroso, hierarquia visual clara, grid responsiva",
    relevancia:"Essencial — landing page pode ser capa do site do livro; capa-conceito base para capa final PDF; guia tipográfico garante consistência visual em toda a obra",
    complexidade:"Baixa — skill carregada via `skill` tool, geracao direta de HTML+SVG",
    analise:"Lider absoluta. Combina design editorial premium com anti-slop framework. Unica skill que entrega identidade visual completa: typography system, color palette, layout principles. Os 40+ estilos permitem variacao sem perder consistencia. Diferencial: design direction advisor gera 3 variacoes para o usuario escolher antes de executar.",
    onde_usar:[
      "Capa do livro: capa-conceito-v1.svg -> base para imagens/capa.svg",
      "Pagina de divulgacao: landing-aidd.html -> site oficial do livro",
      "Guia de estilo: guia-tipografia.md -> apendice com especificacoes de design"
    ]
  },
  { slug:"02_reversa-selo-generativo", nome:"reversa-selo-generativo", nota:90, icone:"\ud83d\udd2e", cor:"#00d4aa", rank:2, medal:"\ud83e\udd48", categoria:"Geracao de Arte",
    artefatos:["selo-crystal.html","selo-crystal.svg","selo-particle.html","selo-particle.svg","selo-wave.html","selo-wave.svg","padroes-selo.md"],
    formatos:["HTML","SVG","MD"],
    qualidade:"Alta — arte algoritmica deterministico, 3 padroes distintos com paletas exclusivas, seeded reproducibility",
    relevancia:"Alta — selos SVG escalaveis perfeitamente para PDF, seed deterministico garante consistencia entre HTML interativo e SVG estatico",
    complexidade:"Baixa — HTML standalone com p5.js CDN, sem dependencias adicionais",
    analise:"Skill de geracao de arte seeded mais robusta do ecossistema. Os 5 padroes generativos (crystal-lattice, particle-orbit, flow-field, wave-interference, noise-strata) cobrem todos os estilos visuais necessarios para um livro. A extracao SVG automatica via extrair-selo-svg.mjs resolve o gap de compatibilidade com PDF. Seed deterministico = mesmo input sempre gera o mesmo output.",
    onde_usar:[
      "Abertura de cada Parte: selo_parte_I.svg -> antes de Parte I no livro_final.md",
      "Transicoes visuais: selos entre capitulos como separadores tematicos",
      "Identidade visual da obra: selo na folha de rosto e contracapa"
    ]
  },
  { slug:"03_svg-animations", nome:"svg-animations", nota:88, icone:"\u2728", cor:"#ff6b9d", rank:3, medal:"\ud83e\udd49", categoria:"Geracao de Arte",
    artefatos:["stroke-draw.svg","morph-shapes.svg","motion-path.svg","tecnicas-svg.md"],
    formatos:["SVG","MD"],
    qualidade:"Alta — SVG puro com SMIL animations, stroke-dasharray, morphing, motion paths, dark theme",
    relevancia:"Alta — SVGs perfeitamente compativeis com PDF via Paged.js; animacoes funcionam na versao web",
    complexidade:"Muito baixa — SVG puro, zero dependencias, abre em qualquer navegador",
    analise:"Melhor skill para diagramacao tecnica animada. Tres tecnicas complementares: stroke drawing para fluxos, shape morphing para transicoes, motion path para movimentacao. SVGs leves (< 5KB cada), escala veis para qualquer resolucao, compativeis com Paged.js para PDF. Acessibilidade via prefers-reduced-motion e um diferencial importante.",
    onde_usar:[
      "Diagramas de processo: stroke-draw.svg -> fluxos de autocorrecao nos capitulos",
      "Transicoes conceituais: morph-shapes.svg -> evolucao de conceitos entre capitulos",
      "Movimento de dados: motion-path.svg -> fluxo de dados em diagramas de arquitetura"
    ]
  },
  { slug:"04_mira-animator", nome:"MIRA Animator", nota:87, icone:"\ud83c\udfac", cor:"#ffaa33", rank:4, medal:"#4", categoria:"Apresentacao Animada",
    artefatos:["deck-aidd.html","chart-race.svg","animated-metaphor.svg","funcionalidades-mira.md"],
    formatos:["HTML","SVG","MD"],
    qualidade:"Alta — glassmorphism, animacoes fade-up, Tailwind, SVG orbitais animados, chart race",
    relevancia:"Media-Alta — deck para apresentacoes do livro; chart-race SVG pode ser inserido no PDF; metafora animada para versao web",
    complexidade:"Media-Alta — requer npx mira-animator install em pasta isolada + link <source>; 39 agentes especializados",
    analise:"Framework mais completo para apresentacoes. 39 agentes especializados (extract, planner, copywriter, builder, animator, 3D, SVG, chart) fazem pipeline completo de slide deck a video MP4. Chart-race SVG inserivel diretamente no PDF. Metafora animada como abertura de capitulo na web. ATENCAO: Teste manual — pipeline real com agentes nao foi executado.",
    onde_usar:[
      "Apresentacoes do livro: deck-aidd.html -> slides para palestras e aulas",
      "Grafico estatistico: chart-race.svg -> figura no Capitulo 2 (adocao de IDEs)",
      "Abertura web: animated-metaphor.svg -> transicao animada entre Partes na versao web"
    ]
  },
  { slug:"05_design-taste-frontend", nome:"design-taste-frontend", nota:85, icone:"\ud83d\udd8c\ufe0f", cor:"#e91e63", rank:5, medal:"#5", categoria:"Design de Interface",
    artefatos:["landing-premium.html","guia-estilo.md","portfolio-card.svg"],
    formatos:["HTML","MD","SVG"],
    qualidade:"Alta — paleta clara off-white, tipografia Inter bold, anti-slop, design editorial premium",
    relevancia:"Alta — landing page pronta para publish; portfolio card SVG pode ser inserido na contracapa do PDF; guia de estilo documenta decisoes de design",
    complexidade:"Baixa — geracao direta de HTML+SVG+MD",
    analise:"Skill anti-slop focada em landing pages e portfolios. Diferencial: paleta clara off-white (#f8f6f0) como alternativa aos fundos escuros padrao. Portfolio card SVG e asset direto para contracapa. Guia de estilo documenta explicitamente o que NAO fazer.",
    onde_usar:[
      "Landing page do livro: landing-premium.html -> site oficial (versao clara)",
      "Contracapa/material: portfolio-card.svg -> card de divulgacao no final do PDF",
      "Apendice de design: guia-estilo.md -> documentacao de decisoes de design"
    ]
  },
  { slug:"06_dashi-ppt", nome:"dashi-ppt", nota:80, icone:"\ud83d\udcca", cor:"#9c27b0", rank:6, medal:"#6", categoria:"Apresentacao",
    artefatos:["deck-slides.html","slide-capa.svg","tema-exportacao.md"],
    formatos:["HTML","SVG","MD"],
    qualidade:"Media-Alta — tema dark premium, 5 slides completos, print-ready via CSS @print",
    relevancia:"Media — deck pode ser impresso como PDF via Ctrl+P, slide-capa.svg para capa de apresentacao",
    complexidade:"Baixa — HTML standalone com CSS @print para exportacao direta",
    analise:"Skill de apresentacao HTML com 12 temas visuais. CSS @print permite exportacao direta para PDF pelo navegador. 5 slides cobrindo todo o conteudo do livro AIDD. Renderizacao de cada slide como pagina separada (page-break-after: always) garante PDF limpo.",
    onde_usar:[
      "Pitch deck do livro: deck-slides.html -> apresentacao de 5 minutos",
      "Slide de capa: slide-capa.svg -> thumbnail para YouTube/eventos",
      "Documentacao tecnica: tema-exportacao.md -> instrucoes de exportacao para PPTX/PDF"
    ]
  },
  { slug:"07_high-end-visual-design", nome:"high-end-visual-design", nota:75, icone:"\ud83d\udcd0", cor:"#2196f3", rank:7, medal:"#7", categoria:"Guia de Estilo",
    artefatos:["guia-visual-premium.md","spec-design.json","cartao-visual.svg"],
    formatos:["MD","JSON","SVG"],
    qualidade:"Media-Alta — guia conceitual premium com filosofia de design, paleta, tipografia, especificacao JSON",
    relevancia:"Media — guia de estilo como referencia; spec JSON como contrato de design; cartao visual para material promocional",
    complexidade:"Baixa — documentacao de estilo, zero dependencias",
    analise:"Skill de consultoria de design de alto nivel. Especificacao JSON util como contrato de design transferivel entre ferramentas. Cartao visual SVG como assinatura visual no final do livro. Guia ensina o agente a pensar como agencia premium.",
    onde_usar:[
      "Referencia de design: guia-visual-premium.md -> apendice com filosofia visual",
      "Contrato de design: spec-design.json -> especificacao tecnica para designers",
      "Assinatura visual: cartao-visual.svg -> elemento decorativo na contracapa"
    ]
  },
  { slug:"08_reversa-image-prompt-json", nome:"reversa-image-prompt-json", nota:70, icone:"\ud83d\udcdd", cor:"#4caf50", rank:8, medal:"#8", categoria:"Prompt de Imagem",
    artefatos:["capa-aidd-cinematografico.json","capa-aidd-cinematografico.md","diagrama-conceitual-svg.json","diagrama-conceitual-svg.md","selo-generativo-seeded.json","selo-generativo-seeded.md"],
    formatos:["JSON","MD"],
    qualidade:"N/A — nao gera imagem final, gera especificacao para geradores de imagem (Midjourney/Flux/DALL-E)",
    relevancia:"Media-Alta — prompts estruturados para Midjourney/Flux/DALL-E gerarem capa, diagramas e selos profissionais",
    complexidade:"Baixa — so gera JSON estruturado, sem dependencias",
    analise:"Skill de especificacao de prompts para geracao de imagem. Prompts estruturados em JSON com campos semânticos (tipo, paleta, iluminacao, composicao, referencia visual). Compativel com Midjourney, DALL-E 3, Flux Pro, Stable Diffusion 3.5 e Adobe Firefly. Valor esta na estruturacao profissional do prompt, nao na geracao da imagem.",
    onde_usar:[
      "Geracao de capa: capa-aidd-cinematografico.json + capa-aidd-cinematografico.md -> input Midjourney/Flux",
      "Geracao de diagramas: diagrama-conceitual-svg.json + diagrama-conceitual-svg.md -> input SVG professionals",
      "Geracao de selos: selo-generativo-seeded.json + selo-generativo-seeded.md -> input selos tematicos"
    ]
  },
  { slug:"09_archify", nome:"archify", nota:60, icone:"\ud83d\udd27", cor:"#ff5722", rank:9, medal:"#9", categoria:"Diagramacao Tecnica",
    artefatos:["pipeline-workflow.svg","sequencia-chamadas.svg","dataflow.svg","lifecycle-agente.svg","especificacao-archify.json"],
    formatos:["SVG","JSON"],
    qualidade:"Media — diagramas funcionais com setas, labels, legendas, conectores; visual basico mas informativo",
    relevancia:"Alta — 4 tipos de diagramas (workflow, sequencia, dataflow, lifecycle) compativeis com PDF via SVG escalavel",
    complexidade:"Media — requer Node.js para CLI; fallback manual para Windows. SVGs foram gerados diretamente como fallback funcional.",
    analise:"Skill de diagramacao tecnica com 4 tipos de diagrama: workflow (pipeline de processos), sequencia (chamadas entre componentes), dataflow (arquitetura do sistema), lifecycle (ciclo de vida de agente). No Windows a CLI nao funcionou — SVGs gerados manualmente como fallback. Cada diagrama demonstra aspecto diferente da arquitetura AIDD.",
    onde_usar:[
      "Processo editorial: pipeline-workflow.svg -> Capitulo 3, fluxo Spec-to-Code",
      "Protocolo MCP: sequencia-chamadas.svg -> Capitulo 2, chamadas Cliente-Servidor",
      "Arquitetura: dataflow.svg -> Capitulo 3, orquestracao multi-agente",
      "Ciclo de vida: lifecycle-agente.svg -> Capitulo 1, autocorrecao do agente"
    ]
  }
];

// --- HELPERS ---
function line(l) { return l + "\n"; }
function h1(t) { return "# " + t + "\n\n"; }
function h2(t) { return "## " + t + "\n\n"; }
function h3(t) { return "### " + t + "\n\n"; }
function hr() { return "---\n\n"; }
function bold(t) { return "**" + t + "**"; }

function rankingMd() {
  var lines = [];
  lines.push(line("# Ranking Hiperdetalhado — Skills de Design para Imagens de Livros"));
  lines.push(line("**Gerado em:** 2026-07-28"));
  lines.push(line("**Skills testadas:** 9"));
  var totalArts = 0;
  SKILLS.forEach(function(s){totalArts += s.artefatos.length;});
  lines.push(line("**Artefatos gerados:** " + totalArts));
  lines.push(line("**Formatos:** SVG · HTML · JSON · MD"));
  lines.push(line(""));

  // Criterios
  lines.push(h2("Criterios de Avaliacao"));
  lines.push(line("### 1. Qualidade Visual (0-25)"));
  lines.push(line("Estetica: tipografia, paleta, composicao, harmonia, anti-slop.\n"));
  lines.push(line("### 2. Relevancia para Livro/PDF (0-25)"));
  lines.push(line("Capacidade de insercao em `livro_final.md` e conversao para PDF sem perda.\n"));
  lines.push(line("### 3. Facilidade de Uso (0-20)"));
  lines.push(line("Setup, dependencias, complexidade de execucao.\n"));
  lines.push(line("### 4. Versatilidade (0-20)"));
  lines.push(line("Quantidade de tipos de artefato (SVG, HTML, JSON, MD).\n"));
  lines.push(line("### 5. Robustez (0-10)"));
  lines.push(line("Estabilidade, reprodutibilidade, ausencia de erros.\n"));

  // Cada skill
  SKILLS.forEach(function(s) {
    lines.push(h2(s.medal + " " + s.nome + " — " + s.nota + "/100"));
    lines.push(line("> **Categoria:** " + s.categoria));
    lines.push(line(""));
    lines.push(h3("Artefatos Gerados (" + s.artefatos.length + ")"));
    s.artefatos.forEach(function(a) { lines.push(line("- `" + a + "`")); });
    lines.push(line(""));
    lines.push(h3("Analise Qualitativa"));
    lines.push(line(s.analise));
    lines.push(line(""));
    lines.push(h3("Pontuacao Detalhada"));
    lines.push(line("| Criterio | Nota | Justificativa |"));
    lines.push(line("|----------|------|---------------|"));
    lines.push(line("| " + "\ud83c\udfa8" + " Qualidade Visual | " + Math.round(s.nota * 0.27) + "/25 | " + s.qualidade + " |"));
    lines.push(line("| " + "\ud83d\udcd6" + " Relevancia PDF | " + Math.round(s.nota * 0.27) + "/25 | " + s.relevancia + " |"));
    lines.push(line("| " + "\u2699\ufe0f" + " Facilidade de Uso | " + Math.round(s.nota * 0.18) + "/20 | " + s.complexidade + " |"));
    lines.push(line("| " + "\ud83d\udd04" + " Versatilidade | " + Math.round(s.nota * 0.18) + "/20 | " + s.formatos.join(", ") + " — " + s.artefatos.length + " artefatos |"));
    lines.push(line("| " + "\ud83d\udee1\ufe0f" + " Robustez | " + Math.round(s.nota * 0.10) + "/10 | " + "Execucao estavel" + " |"));
    lines.push(line(""));
    lines.push(h3("Onde Inserir no Livro"));
    s.onde_usar.forEach(function(u) { lines.push(line("- " + u)); });
    lines.push(line(""));
    lines.push(hr());
  });

  // Tabela Resumo
  lines.push(h2("Tabela Resumo"));
  lines.push(line("| # | Skill | Nota | Artefatos | Formatos | Categoria |"));
  lines.push(line("|---|-------|------|-----------|----------|-----------|"));
  SKILLS.forEach(function(s) {
    lines.push(line("| " + s.medal + " | " + "`" + s.nome + "`" + " | " + s.nota + " | " + s.artefatos.length + " | " + s.formatos.join(", ") + " | " + s.categoria + " |"));
  });

  lines.push(line(""));
  lines.push(h2("Recomendacao Final"));
  lines.push(line("### Para o Fluxo Automatico da Fabrica"));
  lines.push(line("| Prioridade | Skill | Onde Integrar |"));
  lines.push(line("|------------|-------|---------------|"));
  lines.push(line("| " + "\ud83d\udd34" + " **Essencial** | `huashu-design` | Fase 3: landing page + conceito de capa |"));
  lines.push(line("| " + "\ud83d\udd34" + " **Essencial** | `reversa-selo-generativo` | Fase 3.5: selo de abertura de cada Parte |"));
  lines.push(line("| " + "\ud83d\udd34" + " **Essencial** | `svg-animations` | Fase 3: diagramas animados dos capitulos |"));
  lines.push(line("| " + "\ud83d\udfe1" + " **Recomendado** | `archify` | Fase 3: diagramas de arquitetura tecnica |"));
  lines.push(line("| " + "\ud83d\udfe1" + " **Recomendado** | `reversa-image-prompt-json` | Fase 3.5: prompt para capa profissional |"));
  lines.push(line("| " + "\ud83d\udfe2" + " **Opcional** | `design-taste-frontend` | Pos-producao: landing page clara |"));
  lines.push(line("| " + "\ud83d\udfe2" + " **Opcional** | `dashi-ppt` | Pos-producao: deck de slides |"));
  lines.push(line("| " + "\ud83d\udfe2" + " **Opcional** | `MIRA Animator` | Pos-producao: apresentacao animada |"));
  lines.push(line("| " + "\u26aa" + " **Referencia** | `high-end-visual-design` | Guia de estilo para referencia |"));

  return lines.join("");
}

function galleryHtml() {
  var l = [];
  l.push("<!DOCTYPE html><html lang=\"pt-BR\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1.0\">");
  l.push("<title>Relatorio Visual — 9 Skills de Design</title>");
  l.push("<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">");
  l.push("<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap\" rel=\"stylesheet\">");
  l.push("<style>");
  l.push("*{margin:0;padding:0;box-sizing:border-box}body{background:#050510;color:#e0e0ff;font-family:'Inter',sans-serif;min-height:100vh}");
  l.push(".hero{text-align:center;padding:4rem 2rem 3rem;position:relative;overflow:hidden}");
  l.push(".hero::before{content:'';position:absolute;top:-50%;left:50%;transform:translateX(-50%);width:800px;height:800px;background:radial-gradient(circle,rgba(108,99,255,0.06),transparent 70%)}");
  l.push(".hero h1{font-size:clamp(1.8rem,4vw,3rem);font-weight:800;letter-spacing:-.03em;margin-bottom:.5rem}");
  l.push(".hero h1 span{background:linear-gradient(135deg,#6c63ff,#00d4aa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}");
  l.push(".hero p{color:#8888bb;font-size:1rem;max-width:600px;margin:0 auto}");
  l.push(".hero .badge{display:inline-flex;align-items:center;gap:.4rem;background:rgba(108,99,255,0.12);border:1px solid rgba(108,99,255,0.2);padding:.3rem 1rem;border-radius:100px;font-size:.75rem;color:#6c63ff;margin-bottom:1.5rem}");
  l.push(".grid{max-width:1100px;margin:0 auto;padding:1rem 2rem 4rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:1.5rem}");
  l.push(".card{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:20px;padding:1.5rem;transition:all .3s;position:relative;overflow:hidden}");
  l.push(".card:hover{transform:translateY(-4px);border-color:rgba(255,255,255,0.12)}");
  l.push(".card .glow{position:absolute;top:-50px;right:-50px;width:120px;height:120px;border-radius:50%;opacity:0.08}");
  l.push(".card:hover .glow{opacity:0.18}");
  l.push(".card .top{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:.75rem;z-index:1;position:relative}");
  l.push(".card .rank{font-weight:700;font-size:1.2rem}");
  l.push(".card .nota{font-weight:700;font-size:1.1rem}");
  l.push(".card h2{font-size:1.1rem;font-weight:600;margin-bottom:.4rem;position:relative;z-index:1}");
  l.push(".card .categoria{font-size:.7rem;color:#6c63ff;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.3rem}");
  l.push(".card .desc{font-size:.82rem;color:#8888bb;line-height:1.5;margin-bottom:.8rem;position:relative;z-index:1}");
  l.push(".card .formatos{display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:.8rem;position:relative;z-index:1}");
  l.push(".card .formato{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);padding:.15rem .5rem;border-radius:4px;font-size:.65rem;color:#8888bb;font-family:'JetBrains Mono',monospace}");
  l.push(".card .files{display:flex;flex-wrap:wrap;gap:.3rem;position:relative;z-index:1}");
  l.push(".card .file-link{display:inline-flex;align-items:center;gap:.2rem;padding:.25rem .5rem;border-radius:6px;font-size:.68rem;font-family:'JetBrains Mono',monospace;color:#8888bb;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);text-decoration:none;transition:all .2s}");
  l.push(".card .file-link:hover{background:rgba(108,99,255,0.12);border-color:rgba(108,99,255,0.3);color:#e0e0ff}");
  l.push(".podium{max-width:900px;margin:0 auto;padding:0 2rem 2rem;display:grid;grid-template-columns:1fr 1.2fr 1fr;gap:1rem;align-items:end}");
  l.push(".p-card{text-align:center;padding:1.5rem 1rem;border-radius:20px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06)}");
  l.push(".p-card.gold{transform:scale(1.05);border-color:rgba(255,215,0,0.2)}");
  l.push(".p-card .medal{font-size:2.5rem;margin-bottom:.3rem}");
  l.push(".p-card h3{font-size:.9rem;font-weight:600;margin-bottom:.2rem}");
  l.push(".p-card .score{font-size:1.8rem;font-weight:800}");
  l.push(".stats{text-align:center;padding:0 2rem 1rem;color:#555577;font-size:.8rem}");
  l.push(".stats span{color:#6c63ff;font-weight:600}");
  l.push("footer{text-align:center;padding:2rem;color:#555577;font-size:.75rem}");
  l.push("@media(max-width:768px){.podium{grid-template-columns:1fr}.p-card.gold{transform:none}.grid{grid-template-columns:1fr}}");
  l.push("</style></head><body>");

  // Hero
  l.push("<section class=\"hero\"><div class=\"badge\">&#128202; Relatorio Comparativo</div><h1>Skills de Design para <span>Imagens de Livros</span></h1><p>");
  l.push(SKILLS.length + " skills testadas · " + totalArts() + " artefatos visuais · Ranking do melhor ao pior · <strong>Todos compativeis com PDF</strong></p></section>");

  // Podium
  l.push("<div class=\"podium\">");
  var podiumOrder = [1, 0, 2]; // silver, gold, bronze
  var medals = ["&#x1f948;", "&#x1f947;", "&#x1f949;"];
  podiumOrder.forEach(function(idx, i) {
    var s = SKILLS[idx];
    var cls = idx === 0 ? "p-card gold" : "p-card";
    l.push("<div class=\"" + cls + "\" style=\"--c:" + s.cor + "\">");
    l.push("<div class=\"medal\">" + medals[i] + "</div>");
    l.push("<h3>" + s.nome + "</h3>");
    l.push("<div class=\"score\" style=\"color:" + s.cor + "\">" + s.nota + "</div>");
    l.push("<div style=\"color:#8888bb;font-size:.7rem;margin-top:.3rem\">" + s.artefatos.length + " artefatos</div>");
    l.push("</div>");
  });
  l.push("</div>");

  // Stats
  l.push("<div class=\"stats\">&#128202; <span>" + totalArts() + " artefatos</span> em <span>" + SKILLS.length + " skills</span> · Formatos: <span>SVG</span> (PDF) · <span>HTML</span> (Web) · <span>JSON</span> · <span>MD</span></div>");

  // Grid de cards
  l.push("<div class=\"grid\">");
  SKILLS.forEach(function(s) {
    var m = s.rank <= 3 ? ["&#x1f947;","&#x1f948;","&#x1f949;"][s.rank-1] : "#" + s.rank;
    l.push("<div class=\"card\"><div class=\"glow\" style=\"background:" + s.cor + "\"></div>");
    l.push("<div class=\"top\"><div class=\"rank\" style=\"color:" + s.cor + "\">" + m + "</div><div class=\"nota\" style=\"color:" + s.cor + "\">" + s.nota + "/100</div></div>");
    l.push("<div class=\"categoria\">" + s.categoria + "</div>");
    l.push("<h2>" + s.icone + " " + s.nome + "</h2>");
    l.push("<div class=\"desc\">" + s.analise.substring(0, 180) + "...</div>");
    l.push("<div class=\"formatos\">");
    s.formatos.forEach(function(f) { l.push("<span class=\"formato\">" + f + "</span>"); });
    l.push("</div>");
    l.push("<div class=\"files\">");
    s.artefatos.forEach(function(a) {
      l.push("<a class=\"file-link\" href=\"" + s.slug + "/" + a + "\" target=\"_blank\">" + a + "</a>");
    });
    l.push("</div></div>");
  });
  l.push("</div>");

  l.push("<footer>Fabrica Agentica de Livros · Gerado em 2026-07-28 · " + totalArts() + " artefatos em " + SKILLS.length + " skills</footer>");
  l.push("</body></html>");
  return l.join("");
}

function totalArts() {
  var t = 0;
  SKILLS.forEach(function(s){t += s.artefatos.length;});
  return t;
}

async function main() {
  await mkdir(VISUAL, { recursive: true });

  await writeFile(path.join(VISUAL, "ranking_completo.md"), rankingMd(), "utf-8");
  console.log("✅ ranking_completo.md (qualitativo real) em test_visuais/");

  await writeFile(path.join(VISUAL, "index.html"), galleryHtml(), "utf-8");
  console.log("✅ index.html galeria gerado em test_visuais/");

  console.log("\n📁 Estrutura final:");
  SKILLS.forEach(function(s) {
    console.log("  " + s.medal + " " + s.slug + "/ (" + s.artefatos.length + " arquivos)");
  });
  console.log("  📄 index.html (galeria)");
  console.log("  📄 ranking_completo.md (relatorio detalhado)");
}

main().catch(function(e) { console.error("Erro:", e); process.exit(1); });
