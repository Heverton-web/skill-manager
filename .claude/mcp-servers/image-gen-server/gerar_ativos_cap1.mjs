import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { writeFile, mkdir } from "node:fs/promises";
import path from "node:path";

const OUT = "C:\\Users\\trcnologia\\Desktop\\proj_livros\\output\\livro_piloto\\imagens";

const transport = new StdioClientTransport({ command: "node", args: ["index.js"] });
const client = new Client({ name: "diretor-arte-harness", version: "1.0.0" });
await client.connect(transport);

async function gerar(nomeArquivo, args) {
  const result = await client.callTool({ name: "gerar_imagem", arguments: args });
  const svg = result.content?.[0]?.text || "";
  await mkdir(OUT, { recursive: true });
  await writeFile(path.join(OUT, nomeArquivo), svg, "utf-8");
  console.log("gravado:", nomeArquivo, "(", svg.length, "bytes )");
}

await gerar("cap_1_diagrama_1.svg", {
  tipo: "diagrama",
  titulo: "Transporte MCP: da mensagem a ferramenta",
  elementos: ["Cliente MCP", "Transporte (stdio/HTTP)", "Servidor MCP", "Ferramenta/Recurso"],
});

await gerar("cap_1_diagrama_2.svg", {
  tipo: "diagrama",
  titulo: "Ciclo de vida da ferramenta",
  elementos: ["initialize", "tools/list", "agente decide", "tools/call", "resultado"],
});

await gerar("cap_1_diagrama_3.svg", {
  tipo: "diagrama",
  titulo: "Colapso de fronteiras de confianca",
  elementos: ["Dado", "Metadado", "Instrucao executavel"],
});

await gerar("capa.svg", {
  tipo: "capa",
  titulo: "Arquitetura de Agentes: Model Context Protocol na Pratica",
  descricao: "Como servidores MCP viram o motor de ferramentas de sistemas multi-agente",
});

await gerar("contracapa.svg", {
  tipo: "contracapa",
  titulo: "Arquitetura de Agentes: Model Context Protocol na Pratica",
  descricao: "Um guia tecnico sobre como agentes de IA descobrem e acionam ferramentas externas atraves de um protocolo aberto e comum, cobrindo transporte, ciclo de vida de ferramentas e os riscos de confianca que a adocao em escala introduz.",
  elementos: [
    "Protocolo: JSON-RPC 2.0",
    "Transportes: stdio e Streamable HTTP",
    "Formato: Markdown + SVG",
    "Capitulo piloto: 1 de 1",
    "Producao: Fabrica Agentica de Livros",
  ],
});

await client.close();
