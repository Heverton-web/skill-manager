import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const PALETA = {
  fundo: "#0f1720",
  fundoAlt: "#1c2a3a",
  destaque: "#e8b94a",
  texto: "#f5f2ea",
  textoSuave: "#b9c2cc",
  linha: "#3a4a5a",
};

function escapeXml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function quebrarLinhas(texto, maxCharsPorLinha) {
  const palavras = String(texto).split(/\s+/).filter(Boolean);
  const linhas = [];
  let atual = "";
  for (const palavra of palavras) {
    const candidata = atual ? atual + " " + palavra : palavra;
    if (candidata.length > maxCharsPorLinha && atual) {
      linhas.push(atual);
      atual = palavra;
    } else {
      atual = candidata;
    }
  }
  if (atual) linhas.push(atual);
  return linhas;
}

function textoMultilinha(x, yInicial, linhas, tamanhoFonte, opts = {}) {
  const {
    fill = PALETA.texto,
    fontFamily = "Georgia, 'Times New Roman', serif",
    fontWeight = "normal",
    anchor = "start",
    lineHeightMul = 1.35,
  } = opts;
  const lh = tamanhoFonte * lineHeightMul;
  return linhas
    .map(
      (linha, i) =>
        `<text x="${x}" y="${yInicial + i * lh}" font-size="${tamanhoFonte}" font-family="${fontFamily}" font-weight="${fontWeight}" fill="${fill}" text-anchor="${anchor}">${escapeXml(linha)}</text>`
    )
    .join("\n");
}

function renderCapa({ titulo, descricao, largura = 1000, altura = 1500 }) {
  const linhasTitulo = quebrarLinhas(titulo, 18);
  const linhasSub = quebrarLinhas(descricao || "", 40);
  const yTituloInicio = altura * 0.42;

  return `<svg viewBox="0 0 ${largura} ${altura}" width="${largura}" height="${altura}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="${PALETA.fundoAlt}"/>
      <stop offset="100%" stop-color="${PALETA.fundo}"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="${largura}" height="${altura}" fill="url(#bgGrad)"/>
  <rect x="40" y="40" width="${largura - 80}" height="${altura - 80}" fill="none" stroke="${PALETA.destaque}" stroke-width="3"/>
  <rect x="60" y="60" width="${largura - 120}" height="${altura - 120}" fill="none" stroke="${PALETA.linha}" stroke-width="1"/>
  <line x1="${largura / 2 - 60}" y1="${yTituloInicio - 70}" x2="${largura / 2 + 60}" y2="${yTituloInicio - 70}" stroke="${PALETA.destaque}" stroke-width="4"/>
  ${textoMultilinha(largura / 2, yTituloInicio, linhasTitulo, 54, { anchor: "middle", fontWeight: "bold" })}
  <line x1="${largura / 2 - 60}" y1="${yTituloInicio + linhasTitulo.length * 54 * 1.35 + 30}" x2="${largura / 2 + 60}" y2="${yTituloInicio + linhasTitulo.length * 54 * 1.35 + 30}" stroke="${PALETA.destaque}" stroke-width="4"/>
  ${textoMultilinha(largura / 2, yTituloInicio + linhasTitulo.length * 54 * 1.35 + 80, linhasSub, 24, { anchor: "middle", fill: PALETA.textoSuave, fontFamily: "Arial, sans-serif" })}
  <text x="${largura / 2}" y="${altura - 90}" font-size="18" font-family="Arial, sans-serif" fill="${PALETA.textoSuave}" text-anchor="middle" letter-spacing="4">FABRICA AGENTICA DE LIVROS</text>
</svg>`;
}

function renderContracapa({ titulo, descricao, elementos = [], largura = 1000, altura = 1500 }) {
  const linhasSinopse = quebrarLinhas(descricao || "", 55);
  const specsY = altura - 260;
  return `<svg viewBox="0 0 ${largura} ${altura}" width="${largura}" height="${altura}" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="${largura}" height="${altura}" fill="${PALETA.fundo}"/>
  <rect x="40" y="40" width="${largura - 80}" height="${altura - 80}" fill="none" stroke="${PALETA.linha}" stroke-width="2"/>
  <text x="80" y="130" font-size="30" font-family="Georgia, serif" font-weight="bold" fill="${PALETA.destaque}">${escapeXml(titulo)}</text>
  <line x1="80" y1="150" x2="${largura - 80}" y2="150" stroke="${PALETA.linha}" stroke-width="1"/>
  ${textoMultilinha(80, 200, linhasSinopse, 22, { fontFamily: "Arial, sans-serif" })}
  <text x="80" y="${specsY}" font-size="16" font-family="Arial, sans-serif" font-weight="bold" fill="${PALETA.textoSuave}" letter-spacing="2">ESPECIFICACOES</text>
  ${elementos
    .slice(0, 6)
    .map(
      (e, i) =>
        `<text x="80" y="${specsY + 34 + i * 28}" font-size="17" font-family="Arial, sans-serif" fill="${PALETA.texto}">&#8226; ${escapeXml(e)}</text>`
    )
    .join("\n")}
</svg>`;
}

function renderDiagrama({ titulo, elementos = [], largura = 1200, altura = 500 }) {
  const itens = elementos.length ? elementos : ["Entrada", "Processamento", "Saida"];
  const margem = 60;
  const gap = 40;
  const larguraUtil = largura - margem * 2;
  const boxW = (larguraUtil - gap * (itens.length - 1)) / itens.length;
  const boxH = 130;
  const y = altura / 2 - boxH / 2 + 20;

  const boxes = itens
    .map((item, i) => {
      const x = margem + i * (boxW + gap);
      const linhas = quebrarLinhas(item, 16);
      const textoY = y + boxH / 2 - ((linhas.length - 1) * 20) / 2;
      return `
  <rect x="${x}" y="${y}" width="${boxW}" height="${boxH}" rx="10" fill="${PALETA.fundoAlt}" stroke="${PALETA.destaque}" stroke-width="2"/>
  ${textoMultilinha(x + boxW / 2, textoY, linhas, 18, { anchor: "middle", fontFamily: "Arial, sans-serif", fontWeight: "600" })}
  <text x="${x + boxW / 2}" y="${y - 16}" font-size="14" font-family="Arial, sans-serif" fill="${PALETA.textoSuave}" text-anchor="middle">${i + 1}</text>`;
    })
    .join("\n");

  const setas = itens
    .slice(0, -1)
    .map((_, i) => {
      const x1 = margem + (i + 1) * boxW + i * gap;
      const x2 = x1 + gap;
      const yc = y + boxH / 2;
      return `<line x1="${x1}" y1="${yc}" x2="${x2 - 8}" y2="${yc}" stroke="${PALETA.destaque}" stroke-width="3" marker-end="url(#seta)"/>`;
    })
    .join("\n");

  return `<svg viewBox="0 0 ${largura} ${altura}" width="${largura}" height="${altura}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="seta" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="${PALETA.destaque}"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="${largura}" height="${altura}" fill="${PALETA.fundo}"/>
  <text x="${largura / 2}" y="40" font-size="22" font-family="Georgia, serif" font-weight="bold" fill="${PALETA.texto}" text-anchor="middle">${escapeXml(titulo)}</text>
  ${setas}
  ${boxes}
</svg>`;
}

const server = new McpServer({
  name: "fabrica-image-gen",
  version: "1.0.0",
});

server.tool(
  "gerar_imagem",
  "Renderiza um ativo visual (capa, contracapa ou diagrama conceitual) em SVG determinístico para a Fábrica Agêntica de Livros. Não usa API paga de geração de imagem — motor de layout local. Retorna o SVG como texto para o chamador salvar em disco.",
  {
    tipo: z.enum(["capa", "contracapa", "diagrama"]).describe("Tipo de ativo visual a renderizar"),
    titulo: z.string().describe("Título da obra (capa/contracapa) ou do diagrama"),
    descricao: z.string().optional().describe("Sinopse (contracapa), subtítulo (capa) ou não usado em diagrama"),
    elementos: z
      .array(z.string())
      .optional()
      .describe("Lista ordenada de etapas/labels (diagrama) ou especificações técnicas (contracapa)"),
    largura: z.number().optional(),
    altura: z.number().optional(),
  },
  async ({ tipo, titulo, descricao, elementos, largura, altura }) => {
    let svg;
    if (tipo === "capa") {
      svg = renderCapa({ titulo, descricao, largura, altura });
    } else if (tipo === "contracapa") {
      svg = renderContracapa({ titulo, descricao, elementos, largura, altura });
    } else {
      svg = renderDiagrama({ titulo, elementos, largura, altura });
    }
    return {
      content: [{ type: "text", text: svg }],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
