const API_BASE = "https://api.cloudconvert.com/v2";
const SELETOR_PRONTO = 'body[data-pagedjs-pronto="true"]';

async function chamarApi(caminho, apiKey, opcoes = {}) {
  const resp = await fetch(`${API_BASE}${caminho}`, {
    ...opcoes,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      ...(opcoes.headers || {}),
    },
  });
  const corpo = await resp.json();
  if (!resp.ok) {
    const detalhe = corpo?.message || JSON.stringify(corpo);
    throw new Error(`CloudConvert API respondeu ${resp.status}: ${detalhe}`);
  }
  return corpo.data ?? corpo;
}

export async function converterHtmlParaPdf({ apiKey, htmlConteudo, nomeArquivo = "livro.html" }) {
  const job = await chamarApi("/jobs", apiKey, {
    method: "POST",
    body: JSON.stringify({
      tasks: {
        "enviar-html": { operation: "import/upload" },
        "converter-pdf": {
          operation: "convert",
          input: "enviar-html",
          input_format: "html",
          output_format: "pdf",
          engine: "chrome",
          print_background: true,
          wait_for_element: SELETOR_PRONTO,
          zoom: 1,
        },
        "exportar-pdf": {
          operation: "export/url",
          input: "converter-pdf",
        },
      },
    }),
  });

  const tarefaUpload = job.tasks.find((t) => t.name === "enviar-html");
  const form = tarefaUpload.result.form;
  const formData = new FormData();
  for (const [chave, valor] of Object.entries(form.parameters)) {
    formData.append(chave, valor);
  }
  formData.append("file", new Blob([htmlConteudo], { type: "text/html" }), nomeArquivo);

  const respUpload = await fetch(form.url, { method: "POST", body: formData });
  if (!respUpload.ok) {
    throw new Error(`Falha ao enviar HTML para o CloudConvert: HTTP ${respUpload.status}`);
  }

  const jobFinal = await chamarApi(`/jobs/${job.id}/wait`, apiKey, { method: "GET" });

  const tarefaExport = jobFinal.tasks.find((t) => t.name === "exportar-pdf");
  if (tarefaExport.status !== "finished") {
    const tarefaErro = jobFinal.tasks.find((t) => t.status === "error");
    throw new Error(
      `Conversão no CloudConvert falhou: ${tarefaErro?.message || tarefaExport.message || "erro desconhecido"}`
    );
  }

  const arquivo = tarefaExport.result.files[0];
  const respPdf = await fetch(arquivo.url);
  if (!respPdf.ok) {
    throw new Error(`Falha ao baixar o PDF gerado: HTTP ${respPdf.status}`);
  }
  const bytes = Buffer.from(await respPdf.arrayBuffer());
  return { bytes, tamanho: bytes.length, urlOrigem: arquivo.url };
}
