import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { gerarHtmlDoLivro } from "./template_livro.js";

const caminhoMd = process.argv[2];
const saida = process.argv[3];
const markdown = await readFile(caminhoMd, "utf-8");
const html = await gerarHtmlDoLivro({
  markdown,
  diretorioBase: path.dirname(caminhoMd),
  tituloObra: "Arquitetura de Agentes: Model Context Protocol na Pratica",
  subtitulo: "Como servidores MCP viram o motor de ferramentas de sistemas multi-agente",
});
await writeFile(saida, html, "utf-8");
console.log("HTML gerado:", saida, "(", html.length, "bytes )");
console.log("Contem tag <img> com base64:", (html.match(/<img src="data:/g) || []).length);
console.log("Contem nav.sumario:", html.includes('<nav class="sumario">'));
console.log("Contem script pagedjs:", html.includes("paged.polyfill.js"));
