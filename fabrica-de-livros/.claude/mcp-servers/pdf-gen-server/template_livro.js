import { readFile } from "node:fs/promises";
import path from "node:path";
import { Marked } from "marked";

const MIME_POR_EXT = {
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
};

function slugify(texto) {
  return String(texto)
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60);
}

async function embutirImagemBase64(caminhoRelativo, diretorioBase) {
  const caminhoAbs = path.resolve(diretorioBase, caminhoRelativo);
  const ext = path.extname(caminhoAbs).toLowerCase();
  const mime = MIME_POR_EXT[ext] || "application/octet-stream";
  const bytes = await readFile(caminhoAbs);
  return `data:${mime};base64,${bytes.toString("base64")}`;
}

async function localizarImagemOpcional(diretorioBase, nomesCandidatos) {
  for (const nome of nomesCandidatos) {
    try {
      return await embutirImagemBase64(nome, diretorioBase);
    } catch {
      // tenta o proximo candidato
    }
  }
  return null;
}

const CSS_LIVRO = `
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

  :root {
    --cor-primaria: #1b2559;
    --cor-secundaria: #3d55a5;
    --cor-destaque: #f0b429;
    --cor-clara: #eef1fa;
  }

  @page {
    size: A4;
    margin: 2.4cm 1.8cm 2.6cm 1.8cm;
    @top-center { content: string(titulo-capitulo); font-family: 'Inter', Georgia, sans-serif; font-size: 8.5pt; color: var(--cor-secundaria); letter-spacing: 0.3px; font-variant: small-caps; }
    @bottom-center { content: counter(page); font-family: 'Inter', Georgia, sans-serif; font-size: 9pt; color: var(--cor-secundaria); }
    @bottom-left { content: 'AIDD — AI-Driven Development'; font-family: 'Inter', sans-serif; font-size: 7pt; color: var(--cor-secundaria); }
  }
  @page capa { margin: 0; }
  @page contracapa { margin: 0; }
  @page :first { @bottom-left { content: none; } }

  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
  }

  h1, h2, h3, h4, h5, h6, .subtitulo, nav.sumario h2, nav.sumario li.parte, .titulo-parte, .titulo-capitulo, .titulo-secao-final {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  }

  .pagina-capa, .pagina-contracapa {
    page: capa;
    break-after: avoid;
    width: 100%;
    height: 100vh;
  }
  .pagina-contracapa { page: contracapa; break-before: page; break-after: avoid; }
  .pagina-capa img, .pagina-contracapa img {
    width: 100%; height: 100%; object-fit: cover; display: block;
  }

  .folha-rosto {
    break-before: page;
    break-after: avoid;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0 3cm;
  }
  .folha-rosto .linha-superior {
    width: 80px; height: 3px; background: var(--cor-destaque); margin-bottom: 1.5em;
  }
  .folha-rosto h1 { font-size: 28pt; color: var(--cor-primaria); margin-bottom: 0.3em; line-height: 1.2; font-weight: 800; }
  .folha-rosto .linha-divisoria {
    width: 60px; height: 2px; background: var(--cor-destaque); margin: 0.8em auto;
  }
  .folha-rosto .subtitulo { font-size: 13pt; color: var(--cor-secundaria); font-weight: 600; margin-bottom: 0.3em; }
  .folha-rosto .descricao { font-size: 9.5pt; color: #6b6b6b; max-width: 70%; line-height: 1.5; margin-top: 0.5em; }
  .folha-rosto .selo { margin-top: 4em; font-size: 8pt; letter-spacing: 3px; color: var(--cor-secundaria); text-transform: uppercase; font-weight: 600; }

  nav.sumario { break-before: page; break-after: avoid; padding-top: 0.5cm; }
  nav.sumario h2 { font-size: 20pt; color: var(--cor-primaria); border-bottom: 2px solid var(--cor-destaque); padding-bottom: 0.3em; margin-bottom: 0.8em; letter-spacing: 1px; font-weight: 700; }
  nav.sumario ul { list-style: none; padding-left: 0; margin: 0; }
  nav.sumario li.parte { font-weight: bold; margin-top: 1em; font-size: 12pt; color: var(--cor-primaria); }
  nav.sumario li.capitulo { margin-left: 1.8em; margin-top: 0.4em; font-size: 10.5pt; }
  nav.sumario a { color: inherit; text-decoration: none; display: block; position: relative; }
  nav.sumario a::after {
    content: target-counter(attr(href), page);
    position: absolute; right: 0; top: 0; color: var(--cor-secundaria); font-weight: bold;
  }
  nav.sumario a .preenchimento {
    border-bottom: 1px dotted var(--cor-secundaria);
    position: absolute;
    left: 0; right: 1.8em; bottom: 0.3em;
  }

  main h1.titulo-parte {
    break-before: page;
    font-size: 14pt;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--cor-primaria);
    text-align: center;
    margin-top: 28vh;
    padding: 0.8em 0;
    border-top: 2px solid var(--cor-destaque);
    border-bottom: 2px solid var(--cor-destaque);
    font-weight: 700;
  }
  main h1.titulo-capitulo {
    string-set: titulo-capitulo content();
    break-before: page;
    font-size: 22pt;
    color: var(--cor-primaria);
    border-bottom: 2px solid var(--cor-destaque);
    padding-bottom: 0.25em;
    margin-top: 0;
    margin-bottom: 0.6em;
    font-weight: 800;
    letter-spacing: 0.5px;
  }
  main h1.titulo-secao-final {
    string-set: titulo-capitulo content();
    break-before: page;
    font-size: 20pt;
    color: var(--cor-primaria);
    border-bottom: 2px solid var(--cor-destaque);
    padding-bottom: 0.3em;
    margin-top: 0;
    font-weight: 700;
  }
  main h2 { font-size: 14pt; margin-top: 1.6em; margin-bottom: 0.4em; color: var(--cor-secundaria); border-bottom: 1px solid var(--cor-clara); padding-bottom: 0.2em; font-weight: 700; letter-spacing: 0.3px; }
  main h3 { font-size: 12pt; margin-top: 1.2em; margin-bottom: 0.3em; color: var(--cor-secundaria); font-weight: 600; }
  main p { text-align: justify; orphans: 3; widows: 3; margin: 0.5em 0; }
  .titulo-capitulo + p::first-letter {
    font-size: 3.2em; float: left; line-height: 0.8;
    margin-right: 0.12em; margin-top: 0.08em;
    font-weight: bold; color: var(--cor-primaria);
    font-family: 'Inter', sans-serif;
  }
  main img {
    max-width: 95%; display: block; margin: 1.5em auto;
    page-break-inside: avoid; border: 1.5px solid var(--cor-secundaria);
    border-radius: 4px; padding: 4px; background: var(--cor-clara);
  }
  main pre {
    background: var(--cor-clara); border: 1px solid var(--cor-secundaria); border-radius: 4px;
    padding: 0; font-size: 9pt; font-family: 'Consolas', 'Courier New', monospace;
    white-space: pre-wrap; word-wrap: break-word; page-break-inside: avoid;
    line-height: 1.4;
  }
  main code { font-family: 'Consolas', 'Courier New', monospace; font-size: 0.9em; background: var(--cor-clara); padding: 0.1em 0.3em; border-radius: 2px; }
  main pre code { background: none; padding: 0; display: block; }
  main pre.numbered { counter-reset: cl; padding: 0.6em 0; }
  main pre.numbered .cl {
    display: block; padding: 0 0.8em 0 0;
    white-space: pre-wrap; word-break: break-word;
    counter-increment: cl;
  }
  main pre.numbered .cl::before {
    content: counter(cl);
    display: inline-block; width: 2.8em; text-align: right;
    padding-right: 0.8em; margin-right: 0.8em;
    border-right: 1px solid var(--cor-secundaria);
    color: var(--cor-secundaria); font-size: 8pt;
    user-select: none;
  }
  main pre.numbered .cl:first-child { padding-top: 0; }
  main pre.numbered .cl:last-child { padding-bottom: 0; }
  main hr { border: none; border-top: 1.5px solid var(--cor-destaque); margin: 2em 0; }
  main table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 10pt; page-break-inside: avoid; }
  main thead { border-bottom: 2px solid var(--cor-destaque); }
  main th { background: var(--cor-clara); border: 1px solid var(--cor-secundaria); padding: 0.5em 0.6em; font-weight: bold; text-align: left; font-size: 10pt; color: var(--cor-primaria); font-family: 'Inter', sans-serif; }
  main td { border: 1px solid var(--cor-secundaria); padding: 0.4em 0.6em; }
  main tr:nth-child(even) { background: var(--cor-clara); }
  main tr:nth-child(odd) { background: #ffffff; }
  main blockquote {
    border-left: 4px solid var(--cor-destaque); margin: 1em 0; padding: 0.6em 1em;
    background: var(--cor-clara); font-style: italic; color: var(--cor-primaria);
    page-break-inside: avoid;
  }
  main ul, main ol { margin: 0.5em 0; padding-left: 1.5em; }
  main li { margin: 0.3em 0; }
`;

const SCRIPT_PAGEDJS = `
  window.PagedPolyfill = window.PagedPolyfill || {};
  class HandlerFimRenderizacao extends Paged.Handler {
    afterRendered() {
      document.body.setAttribute('data-pagedjs-pronto', 'true');
    }
  }
  Paged.registerHandlers(HandlerFimRenderizacao);
`;

function extrairSumarioEstrutura(headings) {
  const itens = [];
  for (const h of headings) {
    if (h.level !== 1) continue;
    if (/^Parte\s/i.test(h.texto)) itens.push({ tipo: "parte", texto: h.texto, id: h.id });
    else if (/^Cap[ií]tulo\s/i.test(h.texto)) itens.push({ tipo: "capitulo", texto: h.texto, id: h.id });
    else if (
      /^Pref[áa]cio/i.test(h.texto) ||
      /^Conclus[ãa]o Geral/i.test(h.texto) ||
      /^Refer[êe]ncias/i.test(h.texto)
    ) {
      itens.push({ tipo: "capitulo", texto: h.texto, id: h.id });
    }
  }
  return itens;
}

function montarSumarioHtml(itens) {
  const lis = itens
    .map((item) => {
      const classe = item.tipo === "parte" ? "parte" : "capitulo";
      // Itens do tipo "parte" nao tem link porque sao separadores visuais,
      // nao secoes clicaveis — o target-counter nao funcionaria.
      if (item.tipo === "parte") {
        return `<li class="parte"><span>${item.texto}</span></li>`;
      }
      return `<li class="capitulo"><a href="#${item.id}"><span class="preenchimento"></span>${item.texto}</a></li>`;
    })
    .join("\n");
  return `<nav class="sumario"><h2>Sumário</h2><ul>${lis}</ul></nav>`;
}

export async function gerarHtmlDoLivro({ markdown, diretorioBase, tituloObra, subtitulo }) {
  const headings = [];
  const marked = new Marked({
    async: false,
    renderer: {
      // Marked v13 invoca renderers fornecidos como objeto plano com a API
      // posicional legada: (textoJaRenderizadoInline, depth, rawText).
      heading(texto, depth) {
        const id = `h-${slugify(texto)}-${headings.length}`;
        headings.push({ level: depth, texto, id });
        let classe = "";
        if (depth === 1) {
          if (/^Parte\s/i.test(texto)) classe = ' class="titulo-parte"';
          else if (/^Cap[ií]tulo\s/i.test(texto)) classe = ' class="titulo-capitulo"';
          else classe = ' class="titulo-secao-final"';
        }
        return `<h${depth} id="${id}"${classe}>${texto}</h${depth}>\n`;
      },
    },
  });

  // O titulo da obra (primeiro "# ..." do manuscrito) ja e exibido na folha de rosto
  // dedicada — remove essa unica ocorrencia do corpo para nao duplicar o titulo.
  let markdownComImagens = markdown.replace(/^#\s+.+$/m, "");

  // Resolve e embute imagens referenciadas no markdown como base64 antes do parse,
  // porque o parser padrao nao suporta renderer assincrono de imagem.
  const referencias = [...markdownComImagens.matchAll(/!\[([^\]]*)\]\(([^)]+)\)/g)];
  for (const ref of referencias) {
    const [tagCompleta, alt, caminho] = ref;
    if (/^https?:\/\//.test(caminho) || caminho.startsWith("data:")) continue;  // Capa e contracapa ja recebem secao dedicada de pagina inteira (ver mais abaixo);
      // remove a referencia solta do corpo para nao duplicar a imagem no PDF.
      if (/(^|[/\\])(capa|contracapa)\.(svg|png|jpe?g)$/i.test(caminho)) {
        markdownComImagens = markdownComImagens.replace(tagCompleta, "");
        continue;
      }
      // Selos generativos: mantem a referencia (sera exibida entre Partes)
      if (/selo_parte_/i.test(caminho)) {
        continue; // deixa a imagem no fluxo normal
      }
    try {
      const dataUri = await embutirImagemBase64(caminho, diretorioBase);
      markdownComImagens = markdownComImagens.replace(tagCompleta, `![${alt}](${dataUri})`);
    } catch {
      // Fallback: tenta resolver sem o prefixo ../ (caso o path esteja incorreto
      // porque o merge dos capitulos nao corrigiu ../imagens/ para imagens/)
      const fallbackPath = caminho.replace(/^(?:\.\.\/)+/, "");
      if (fallbackPath !== caminho) {
        try {
          const dataUri = await embutirImagemBase64(fallbackPath, diretorioBase);
          markdownComImagens = markdownComImagens.replace(tagCompleta, `![${alt}](${dataUri})`);
        } catch {
          // mantem a referencia original se ambos os paths falharem
        }
      }
    }
  }

  let corpoHtml = marked.parse(markdownComImagens);

  // Remove o "## Sumario" estatico do corpo (sera substituido pelo sumario paginado real).
  corpoHtml = corpoHtml.replace(/<h2[^>]*>Sum[áa]rio<\/h2>[\s\S]*?(?=<hr|<h1)/i, "");

  // Adiciona numeração de linhas em blocos de código
  corpoHtml = corpoHtml.replace(
    /<pre><code([^>]*)>([\s\S]*?)<\/code><\/pre>/g,
    (match, codeAttrs, codeContent) => {
      // Preserva entidades HTML (marked já escapou < > &)
      // Divide o conteudo em linhas preservando a ultima linha vazia
      const linhas = codeContent.split('\n');
      // Se a ultima linha for vazia, remove (common trailing newline)
      if (linhas.length > 1 && linhas[linhas.length - 1].trim() === '') {
        linhas.pop();
      }
      const linhasHtml = linhas
        .map((linha) => `<span class="cl">${linha || ' '}</span>`)
        .join('\n');
      return `<pre class="numbered"><code${codeAttrs}>\n${linhasHtml}\n</code></pre>`;
    }
  );

  const itensSumario = extrairSumarioEstrutura(headings);
  const sumarioHtml = montarSumarioHtml(itensSumario);

  const capaDataUri = await localizarImagemOpcional(diretorioBase, [
    "imagens/capa.svg",
    "../imagens/capa.svg",
    "capa.svg",
  ]);
  const contracapaDataUri = await localizarImagemOpcional(diretorioBase, [
    "imagens/contracapa.svg",
    "../imagens/contracapa.svg",
    "contracapa.svg",
  ]);

  return `<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>${tituloObra}</title>
<style>${CSS_LIVRO}</style>
</head>
<body>
${capaDataUri ? `<section class="pagina-capa"><img src="${capaDataUri}" alt="Capa"></section>` : ""}
<section class="folha-rosto">
  <div class="linha-superior"></div>
  <h1>${tituloObra}</h1>
  <div class="linha-divisoria"></div>
  ${subtitulo ? `<div class="subtitulo">${subtitulo}</div>` : ""}
  <div class="descricao">Um guia completo sobre AI-Driven Development: coding agents, Context Engineering, Spec-Driven Development, MCP, orquestração multi-agente e o novo perfil profissional da engenharia de software.</div>
  <div class="selo">Fábrica Agêntica de Livros</div>
</section>
${sumarioHtml}
<main>
${corpoHtml}
</main>
${contracapaDataUri ? `<section class="pagina-contracapa"><img src="${contracapaDataUri}" alt="Contracapa"></section>` : ""}
<script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>
<script>${SCRIPT_PAGEDJS}</script>
</body>
</html>`;
}
