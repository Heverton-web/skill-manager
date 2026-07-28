import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { gerarHtmlDoLivro } from "./template_livro.js";
import { converterHtmlParaPdf } from "./cloudconvert.js";

function carregarChaveApi() {
  if (process.env.CLOUDCONVERT_API_KEY) return process.env.CLOUDCONVERT_API_KEY;
  return null;
}

async function tentarCarregarEnvLocal() {
  if (process.env.CLOUDCONVERT_API_KEY) return;
  try {
    const conteudo = await readFile(new URL("./.env", import.meta.url), "utf-8");
    for (const linha of conteudo.split("\n")) {
      const l = linha.trim();
      if (!l || l.startsWith("#")) continue;
      const idx = l.indexOf("=");
      if (idx === -1) continue;
      const chave = l.slice(0, idx).trim();
      const valor = l.slice(idx + 1).trim();
      if (chave && !process.env[chave]) process.env[chave] = valor;
    }
  } catch {
    // .env local nao existe - segue apenas com variaveis de ambiente do sistema
  }
}

await tentarCarregarEnvLocal();

const server = new McpServer({
  name: "fabrica-pdf-gen",
  version: "1.0.0",
});

server.tool(
  "markdown_para_pdf",
  "Converte um manuscrito Markdown (tipicamente livro_final.md, ja com imagens SVG referenciadas) em um PDF de livro visualmente estruturado — capa, folha de rosto, sumário paginado com numeração real, cabeçalho corrente com o nome do capítulo, tipografia serifada — usando a API real do CloudConvert (engine Chrome). Requer a variável de ambiente CLOUDCONVERT_API_KEY (ou um arquivo .env ao lado deste servidor) com uma API key gratuita obtida em https://cloudconvert.com/api/v2.",
  {
    caminho_markdown: z.string().describe("Caminho absoluto do arquivo .md a converter (ex.: livro_final.md)"),
    caminho_pdf_saida: z.string().describe("Caminho absoluto onde o PDF final deve ser salvo"),
    titulo_obra: z.string().describe("Título da obra, usado na folha de rosto e nos metadados do PDF"),
    subtitulo: z.string().optional().describe("Subtítulo opcional exibido na folha de rosto"),
  },
  async ({ caminho_markdown, caminho_pdf_saida, titulo_obra, subtitulo }) => {
    const apiKey = carregarChaveApi();
    if (!apiKey) {
      return {
        isError: true,
        content: [
          {
            type: "text",
            text:
              "CLOUDCONVERT_API_KEY não configurada. Para usar este MCP: (1) crie uma conta gratuita em " +
              "https://cloudconvert.com/register (25 minutos de conversão grátis por dia); (2) gere uma API key em " +
              "https://cloudconvert.com/dashboard/api/v2/keys (permissão 'task.read' e 'task.write'); (3) salve-a " +
              "em um arquivo .env ao lado de index.js (CLOUDCONVERT_API_KEY=sua_chave) ou exporte a variável de " +
              "ambiente antes de iniciar esta sessão. Nenhuma chamada foi feita à API.",
          },
        ],
      };
    }

    const markdown = await readFile(caminho_markdown, "utf-8");
    const diretorioBase = path.dirname(caminho_markdown);

    const html = await gerarHtmlDoLivro({ markdown, diretorioBase, tituloObra: titulo_obra, subtitulo });

    const { bytes, tamanho } = await converterHtmlParaPdf({
      apiKey,
      htmlConteudo: html,
      nomeArquivo: `${path.basename(caminho_markdown, ".md")}.html`,
    });

    await writeFile(caminho_pdf_saida, bytes);

    return {
      content: [
        {
          type: "text",
          text: `PDF gerado com sucesso via CloudConvert: ${caminho_pdf_saida} (${tamanho} bytes).`,
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
