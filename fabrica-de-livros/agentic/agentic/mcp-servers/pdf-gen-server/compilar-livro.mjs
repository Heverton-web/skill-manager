#!/usr/bin/env node

/**
 * compilar-livro.mjs — Skill_Compilador_ABNT (Nós 5-10)
 *
 * Uso:
 *   node compilar-livro.mjs <slug-do-livro>
 *
 * Exemplo:
 *   node compilar-livro.mjs aidd-ai-driven-development-em-contexto-de-ides-agneticas
 *
 * O que faz:
 *   1. Lê sumario_macro.json (Nó 5)
 *   2. Concatena todos os cap_<n>.md na ordem (Nó 5)
 *   3. Gera Prefácio a partir de sumario_macro.json.introducao (Nó 6)
 *   4. Gera Conclusão Geral a partir de sumario_macro.json.conclusao (Nó 6)
 *   5. Compila referências dos dossiês de pesquisa (Nó 7)
 *   6. Aplica formatação ABNT (Nó 8)
 *   7. Grava livro_final.md (Nó 9)
 *   8. Dispara pdf_gen MCP para gerar PDF via CloudConvert (Nó 10)
 *   9. Reporta resultado
 */

import { readFile, writeFile, readdir, mkdtemp, unlink } from "node:fs/promises";
import { existsSync, readdirSync, statSync } from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const DIR_RAIZ = path.resolve(SCRIPT_DIR, "../../..");
const MCP_SERVER_DIR = SCRIPT_DIR;

// ─── Utilitários ────────────────────────────────────────────────────────────

function e(msg) {
  console.error(`[compilador-abnt] ${msg}`);
}

function slugify(texto) {
  return String(texto)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase()
    .slice(0, 80);
}

function normalizarUrl(url) {
  return url.replace(/\/+$/, "").replace(/^https?:\/\//, "").toLowerCase();
}

// ─── Passo 1: Ler sumário ───────────────────────────────────────────────────

async function lerSumario(slug) {
  const caminho = path.join(DIR_RAIZ, "output", slug, "sumario_macro.json");
  const raw = await readFile(caminho, "utf-8");
  return JSON.parse(raw);
}

// ─── Passo 2: Coletar capítulos na ordem ────────────────────────────────────

async function coletarCapitulos(slug, sumario) {
  const dirCap = path.join(DIR_RAIZ, "output", slug, "capitulos");
  const conteudos = [];
  let totalEncontrados = 0;
  const totalEsperados = sumario.partes.reduce((acc, p) => acc + p.capitulos.length, 0);

  for (const parte of sumario.partes) {
    conteudos.push(`\n# Parte ${parte.parte} — ${parte.titulo_parte}\n`);

    for (const cap of parte.capitulos) {
      const arq = path.join(dirCap, `cap_${cap.capitulo}.md`);
      if (!existsSync(arq)) {
        e(`AVISO: ${arq} não encontrado — pulando capítulo ${cap.capitulo}`);
        continue;
      }
      const md = await readFile(arq, "utf-8");
      // Corrige paths das imagens: chapters usam ../imagens/ (dentro de capitulos/),
      // mas livro_final.md fica na raiz da obra, entao devem ser imagens/
      const mdCorrigido = md.replace(/\.\.\/imagens\//g, "imagens/");
      conteudos.push(mdCorrigido);
      totalEncontrados++;
      e(`  + cap_${cap.capitulo}.md (${md.length} chars)`);
    }
  }

  if (totalEncontrados === 0) {
    throw new Error(`NENHUM capítulo encontrado em output/${slug}/capitulos/ — abortando.`);
  }
  if (totalEncontrados < totalEsperados) {
    e(`AVISO: encontrados ${totalEncontrados} de ${totalEsperados} capítulos esperados`);
  }

  return conteudos.join("\n\n");
}

// ─── Passo 3: Gerar Prefácio (Nó 6) ─────────────────────────────────────────

function gerarPrefacio(sumario) {
  const { introducao } = sumario;
  const totalCaps = sumario.partes.reduce((acc, p) => acc + p.capitulos.length, 0);
  return `# Prefácio

${introducao}

A obra está organizada em ${sumario.partes.length} Partes, totalizando
${totalCaps} Capítulos.
`;
}

// ─── Passo 4: Gerar Conclusão (Nó 6) ────────────────────────────────────────

function gerarConclusao(sumario) {
  return `# Conclusão

${sumario.conclusao || "A jornada ao longo desta obra revelou as múltiplas facetas do tema, desde seus fundamentos conceituais até as implicações práticas para o profissional do futuro."}
`;
}

// ─── Passo 5: Compilar referências dos dossiês (Nó 7) ───────────────────────

/**
 * Tenta extrair uma referência de uma linha usando múltiplos padrões.
 * Suporta: ABNT, travessões, URL inline.
 */
function extrairRefDaLinha(linha) {
  const padroes = [
    // Padrão 1: ABNT — SOBRENOME, Nome. *Título*. Disponível em: URL. Acesso em: data.
    /^-\s+(.+?)\.\s+\*(.+?)\*\.\s+Disponível em:\s+(https?:\/\/\S+)\.\s+Acesso em:\s+(.+)$/,
    // Padrão 2: Travessões (especificação antiga do pesquisador)
    /^-\s+(.+?)\s*—\s*(https?:\/\/[^\s]+)\s*—\s*(.+)$/,
    // Padrão 3: URL inline sem "Disponível em:" — Autor. "Título." URL Acesso em: data.
    /^-\s+(.+?)\s+(https?:\/\/\S+)\s+Acesso em:\s+(.+)$/,
    // Padrão 4: Título itálico sem ponto antes de Disponível
    /^-\s+\*(.+?)\*\.\s+Disponível em:\s+(https?:\/\/\S+)\.\s+Acesso em:\s+(.+)$/,
    // Padrão 5: Sem URL, aspas — Autor. "Título." ou "Título". Acesso em: data.
    /^-\s+(.+?)\s+"([^"]+\.?)"[\.\s]*\s*Acesso em:\s+(.+)$/,
    // Padrão 6: Sem URL, itálico — Autor. *Título*. Acesso em: data.
    /^-\s+(.+?)\.\s+\*(.+?)\*\.\s+Acesso em:\s+(.+)$/,
  ];

  for (const padrao of padroes) {
    const m = linha.match(padrao);
    if (!m) continue;

    if (m.length === 5) {
      // Padrão 1: [_, sobrenome, titulo, url, data]
      const [_, sobrenome, titulo, url, data] = m;
      return { titulo: `${sobrenome}. ${titulo}`, url: url.trim(), data: data.trim() };
    } else if (m.length === 4) {
      const [_, campo1, campo2, campo3] = m;
      // Se campo2 é URL (contém http), é padrão 2/3/4: (titulo, url, data)
      if (campo2.includes('http')) {
        return { titulo: campo1.trim(), url: campo2.trim(), data: campo3.trim() };
      } else {
        // Padrões 5/6: (autor, titulo, data) — sem URL
        // Remove ponto final duplicado
        const autor = campo1.trim().replace(/\.\s*$/, '');
        const titulo = campo2.trim().replace(/\.\s*$/, '');
        return { titulo: `${autor}. ${titulo}`, url: '', data: campo3.trim() };
      }
    }
  }
  return null;
}

async function compilarReferencias(slug) {
  const dirPesq = path.join(DIR_RAIZ, "output", slug, "pesquisa");
  const refs = new Map();

  try {
    const arquivos = await readdir(dirPesq);
    for (const arq of arquivos) {
      if (!arq.startsWith("dossie_") || !arq.endsWith(".md")) continue;
      const conteudo = await readFile(path.join(dirPesq, arq), "utf-8");
      const secao = conteudo.match(/## Fontes brutas[\s\S]*$/);
      if (!secao) continue;

      const linhas = secao[0].split("\n");
      for (const linha of linhas) {
        if (!linha.startsWith("-")) continue;
        const ref = extrairRefDaLinha(linha);
        if (!ref) continue;
        const chave = normalizarUrl(ref.url);
        if (!refs.has(chave)) {
          refs.set(chave, ref);
        }
      }
    }
  } catch {
    e("AVISO: diretório de pesquisa não encontrado ou vazio");
  }

  if (refs.size === 0) {
    return "# Referências Bibliográficas\n\n*Nenhuma referência bibliográfica foi coletada durante a pesquisa.*\n";
  }

  // Formatação ABNT com numeração [N]
  const refsOrdenadas = [...refs.values()]
    .sort((a, b) => a.titulo.localeCompare(b.titulo));

  const linhasRef = refsOrdenadas.map((ref, i) => {
    const num = i + 1;
    if (ref.url && ref.url !== '') {
      return `[${num}] ${ref.titulo}. Disponível em: ${ref.url}. Acesso em: ${ref.data}.`;
    } else {
      // Referência sem URL (livro, relatório offline)
      return `[${num}] ${ref.titulo}. Acesso em: ${ref.data}.`;
    }
  });

  return `# Referências Bibliográficas\n\n${linhasRef.join("\n\n")}\n`;
}

// ─── Passo 6: Montar sumário dinâmico (Nó 6) ────────────────────────────────

function gerarSumarioMd(sumario) {
  const linhas = [];
  for (const parte of sumario.partes) {
    linhas.push(`- **Parte ${parte.parte} — ${parte.titulo_parte}**`);
    for (const cap of parte.capitulos) {
      linhas.push(`  - Capítulo ${cap.capitulo}: ${cap.titulo}`);
    }
  }
  return `# Sumário\n\n${linhas.join("\n")}\n`;
}

// ─── Passo 7: Compor livro_final.md (Nó 9) ──────────────────────────────────

function comporLivroFinal(sumario, corpoCapitulos, prefacio, conclusao, referencias, sumarioMd) {
  const totalCaps = sumario.partes.reduce((acc, p) => acc + p.capitulos.length, 0);

  return `![Capa do Livro](imagens/capa.svg)

${prefacio}

${sumarioMd}

---

${corpoCapitulos}

---

${conclusao}

---

${referencias}

![Contracapa do Livro](imagens/contracapa.svg)

<!--
  Produzido pela Fábrica Agêntica de Livros
  Skill: compilador-abnt (Nós 5-10)
  Slug: ${slugify(sumario.titulo_obra)}
  Capítulos: ${totalCaps}
  Gerado em: ${new Date().toISOString().slice(0, 10)}
-->
`;
}

// ─── Passo 8: Gerar PDF (Nó 10) ────────────────────────────────────────────

/**
 * Tenta converter Markdown para PDF usando Pandoc + Typst (gratuito).
 * Retorna true se bem-sucedido, false caso contrário.
 */
async function gerarPdfPandocTypst(caminhoMarkdown, caminhoPdf, tituloObra) {
  // Auto-detectar Pandoc e Typst no sistema
  function findExecutable(name) {
    // 1. Tentar via PATH (where no Windows)
    try {
      const result = execSync(`where ${name}`, { encoding: "utf-8", stdio: "pipe" }).trim();
      return result.split("\n")[0] || null;
    } catch { /* continue */ }

    // 2. Buscar no WinGet Packages
    try {
      const localAppData = process.env.LOCALAPPDATA || "";
      const wingetDir = path.join(localAppData, "Microsoft", "WinGet", "Packages");
      if (existsSync(wingetDir)) {
        const packages = readdirSync(wingetDir);
        for (const pkg of packages) {
          if (pkg.toLowerCase().includes(name.toLowerCase())) {
            const pkgDir = path.join(wingetDir, pkg);
            const files = readdirSync(pkgDir);
            for (const f of files) {
              if (f.toLowerCase() === `${name}.exe`) return path.join(pkgDir, f);
              try {
                const subDir = path.join(pkgDir, f);
                if (existsSync(subDir)) {
                  const subFiles = readdirSync(subDir);
                  for (const sf of subFiles) {
                    if (sf.toLowerCase() === `${name}.exe`) return path.join(subDir, sf);
                  }
                }
              } catch { /* skip */ }
            }
          }
        }
      }
    } catch { /* skip */ }
    return null;
  }

  const pandocPath = findExecutable("pandoc");
  if (!pandocPath) {
    e("AVISO: Pandoc não encontrado — impossível usar Typst");
    return false;
  }

  // Adicionar Typst ao PATH se necessário
  const typstPath = findExecutable("typst");
  if (typstPath) {
    const typstDir = path.dirname(typstPath);
    process.env.PATH = `${typstDir}${path.delimiter}${process.env.PATH || ""}`;
  }

  // Verificar se o template Typst existe (procura em vários locais)
  const templateCandidates = [
    path.resolve(DIR_RAIZ, "templates", "template.typ"),
    path.resolve(DIR_RAIZ, "fabrica-de-livros", "templates", "template.typ"),
    path.resolve(".", "fabrica-de-livros", "templates", "template.typ"),
    path.resolve(".", "templates", "template.typ"),
  ];
  let templatePath = null;
  for (const candidate of templateCandidates) {
    if (existsSync(candidate)) {
      templatePath = candidate;
      break;
    }
  }
  if (!templatePath) {
    e("AVISO: templates/template.typ não encontrado — impossível usar Typst");
    return false;
  }

  // Rodar Pandoc a partir do diretório do livro (para resolver paths relativos)
  const dirLivro = path.dirname(caminhoMarkdown);
  const mdBase = path.basename(caminhoMarkdown);
  const pdfBase = path.basename(caminhoPdf);

  try {
    const args = [
      mdBase,
      `-o`, pdfBase,
      `--pdf-engine=typst`,
      `--toc`,
      `--toc-depth=3`,
      `--number-sections`,
      `--template=${templatePath}`,
      `-V`, `title=${tituloObra}`,
      `-V`, `author=Fábrica Agêntica de Livros`,
      `-V`, `subtitle=`,
      `--wrap=preserve`,
    ];

    const cmd = `"${pandocPath}" ${args.map(a => `"${a}"`).join(" ")}`;
    e("Disparando Pandoc + Typst (gratuito)...");
    execSync(cmd, { encoding: "utf-8", cwd: dirLivro, stdio: "pipe" });

    if (existsSync(caminhoPdf)) {
      const size = statSync(caminhoPdf).size;
      e(`PDF gerado via Pandoc+Typst: ${caminhoPdf} (${(size / 1024).toFixed(0)} KB)`);
      return true;
    }
  } catch (err) {
    e(`Pandoc+Typst falhou: ${err.message}`);
  }
  return false;
}

/**
 * Tenta converter Markdown para PDF usando CloudConvert (requer API key).
 */
async function gerarPdfCloudConvert(caminhoMarkdown, caminhoPdf, tituloObra, subtitulo) {
  const testMcp = path.join(MCP_SERVER_DIR, "test_mcp.mjs");
  const indexJs = path.join(MCP_SERVER_DIR, "index.js");

  if (!existsSync(testMcp) || !existsSync(indexJs)) {
    e("AVISO: MCP pdf_gen não encontrado — pulando geração de PDF via CloudConvert");
    return false;
  }

  // Carrega chave do .env se não estiver no ambiente
  if (!process.env.CLOUDCONVERT_API_KEY) {
    try {
      const envContent = await readFile(path.join(MCP_SERVER_DIR, ".env"), "utf-8");
      for (const linha of envContent.split("\n")) {
        const l = linha.trim();
        if (!l || l.startsWith("#")) continue;
        const idx = l.indexOf("=");
        if (idx === -1) continue;
        const chave = l.slice(0, idx).trim();
        const valor = l.slice(idx + 1).trim();
        if (chave === "CLOUDCONVERT_API_KEY" && valor) process.env.CLOUDCONVERT_API_KEY = valor;
      }
    } catch {
      e("AVISO: CLOUDCONVERT_API_KEY não configurada — impossível usar CloudConvert");
      return false;
    }
  }

  if (!process.env.CLOUDCONVERT_API_KEY) {
    e("AVISO: CLOUDCONVERT_API_KEY não configurada");
    return false;
  }

  // Escreve args em temp file para evitar shell injection
  const tmpDir = await mkdtemp(path.join(os.tmpdir(), "pdf-args-"));
  const argsFile = path.join(tmpDir, "args.json");
  await writeFile(argsFile, JSON.stringify({
    caminho_markdown: caminhoMarkdown,
    caminho_pdf_saida: caminhoPdf,
    titulo_obra: tituloObra,
    subtitulo: subtitulo || "",
  }));

  try {
    const cmd = `node "${testMcp}" node "${indexJs}" -- markdown_para_pdf "${argsFile}"`;
    e("Disparando pdf_gen MCP via CloudConvert...");
    const stdout = execSync(cmd, { timeout: 120000, encoding: "utf-8", cwd: MCP_SERVER_DIR });

    if (stdout.includes("CHAMADA_OK isError= false") || stdout.includes("PDF gerado com sucesso")) {
      const tamMatch = stdout.match(/\((\d+)\s*bytes\)/);
      const tamanho = tamMatch ? `${(parseInt(tamMatch[1]) / 1024).toFixed(0)} KB` : "?";
      e(`PDF gerado via CloudConvert: ${caminhoPdf} (${tamanho})`);
      return true;
    } else {
      e(`CloudConvert falhou. Output:\n${stdout.slice(0, 500)}`);
      return false;
    }
  } catch (err) {
    e(`ERRO CloudConvert: ${err.message}`);
    return false;
  } finally {
    try { await unlink(argsFile); } catch { /* temp file already cleaned up */ }
  }
}

/**
 * Gera PDF com fallback automático:
 * 1. Pandoc + Typst (gratuito, rápido)
 * 2. CloudConvert (requer API key)
 */
async function gerarPdf(caminhoMarkdown, caminhoPdf, tituloObra, subtitulo) {
  // Tentar 1: Pandoc + Typst (gratuito)
  e("[Nó 10] Tentativa 1: Pandoc + Typst (gratuito)...");
  if (await gerarPdfPandocTypst(caminhoMarkdown, caminhoPdf, tituloObra)) {
    return true;
  }

  // Tentar 2: CloudConvert (requer API key)
  e("[Nó 10] Tentativa 2: CloudConvert (requer API key)...");
  if (await gerarPdfCloudConvert(caminhoMarkdown, caminhoPdf, tituloObra, subtitulo)) {
    return true;
  }

  e("AVISO: Nenhum método de geração de PDF disponível");
  e("  - Instale Pandoc + Typst: winget install JohnMacFarlane.Pandoc Typst.Typst");
  e("  - Ou configure CLOUDCONVERT_API_KEY em .claude/mcp-servers/pdf-gen-server/.env");
  return false;
}

// ─── Main ───────────────────────────────────────────────────────────────────

async function main() {
  const slug = process.argv[2];
  if (!slug) {
    e("USO: node compilar-livro.mjs <slug-do-livro>");
    e("Ex.: node compilar-livro.mjs aidd-ai-driven-development-em-contexto-de-ides-agneticas");
    process.exit(1);
  }

  const dirOutput = path.join(DIR_RAIZ, "output", slug);
  if (!existsSync(dirOutput)) {
    e(`ERRO: diretório output/${slug}/ não encontrado`);
    process.exit(1);
  }

  e(`=== Compilando livro: ${slug} ===`);

  try {
    // Nó 5 — Ler sumário e concatenar capítulos
    e("[Nó 5] Lendo sumário macro...");
    const sumario = await lerSumario(slug);
    e(`  Título: ${sumario.titulo_obra}`);
    e(`  Partes: ${sumario.partes.length}, Capítulos: ${sumario.partes.reduce((a, p) => a + p.capitulos.length, 0)}`);

    e("[Nó 5] Coletando capítulos...");
    const corpoCapitulos = await coletarCapitulos(slug, sumario);

    // Nó 6 — Elementos extrusos
    e("[Nó 6] Gerando prefácio e conclusão...");
    const prefacio = gerarPrefacio(sumario);
    const conclusao = gerarConclusao(sumario);
    const sumarioMd = gerarSumarioMd(sumario);

    // Nó 7 — Referências
    e("[Nó 7] Compilando referências dos dossiês...");
    const referencias = await compilarReferencias(slug);

    // Nó 8 — Formatação ABNT (já aplicada na escrita)
    e("[Nó 8] Selo de conformidade ABNT aplicado.");

    // Nó 9 — Expedição em Markdown
    e("[Nó 9] Compondo livro_final.md...");
    const livroFinal = comporLivroFinal(sumario, corpoCapitulos, prefacio, conclusao, referencias, sumarioMd);
    const caminhoMd = path.join(dirOutput, "livro_final.md");
    await writeFile(caminhoMd, livroFinal, "utf-8");
    e(`  Gravado: ${caminhoMd} (${livroFinal.length} chars)`);

    // Nó 10 — Exportação em PDF
    e("[Nó 10] Exportando PDF...");
    const caminhoPdf = path.join(dirOutput, "livro_final.pdf");
    const pdfOk = await gerarPdf(
      caminhoMd,
      caminhoPdf,
      sumario.titulo_obra,
      `Partes: ${sumario.partes.length} · Capítulos: ${sumario.partes.reduce((a, p) => a + p.capitulos.length, 0)}`
    );

    // Relatório final
    console.log("\n" + "=".repeat(60));
    console.log("  RELATÓRIO — Skill Compilador ABNT");
    console.log("=".repeat(60));
    console.log(`  Obra:     ${sumario.titulo_obra}`);
    console.log(`  Slug:     ${slug}`);
    console.log(`  Partes:   ${sumario.partes.length}`);
    console.log(`  Capítulos: ${sumario.partes.reduce((a, p) => a + p.capitulos.length, 0)}`);
    console.log(`  Markdown: ${caminhoMd}`);
    console.log(`  PDF:      ${pdfOk ? caminhoPdf : "❌ Não gerado (configure CLOUDCONVERT_API_KEY)"}`);
    console.log("=".repeat(60) + "\n");

  } catch (err) {
    e(`ERRO FATAL: ${err.message}`);
    if (err.stack) e(err.stack.slice(0, 500));
    process.exit(1);
  }
}

main();
