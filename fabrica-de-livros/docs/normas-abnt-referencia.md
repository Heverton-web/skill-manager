# Normas ABNT de Referência (V4)

Fonte única citada por `SPEC_TCC.md`, `SPEC_ARTIGO.md` e pelas skills
`redator-academico`/`compilador-tcc`/`compilador-artigo` — evita duplicar o texto
da norma em cada spec.

| Norma | O que regula | Onde se aplica na Fábrica |
|---|---|---|
| **NBR 14724** | Estrutura de TCC/monografia/dissertação/tese: pré-textual, textual, pós-textual | `SPEC_TCC.md`, `compilador-tcc`, `template_tcc.typ` |
| **NBR 6022** | Artigo em publicação periódica técnica/científica | `SPEC_ARTIGO.md`, `compilador-artigo` |
| **NBR 12820** | Artigo em congresso/simpósio/reunião | `SPEC_ARTIGO.md` (formato alternativo de evento) |
| **NBR 6029** | Estrutura de livros e folhetos (editoração) | `SPEC.md` (livro), `template.typ` |
| **NBR 6023** | Elaboração de referências bibliográficas | Livro (`[N]`), TCC/Artigo (autor-data) |
| **NBR 10520** | Citações no corpo do texto (numérica ou autor-data) | Livro usa numérica; TCC/Artigo usam autor-data |
| **NBR 6024** | Numeração progressiva de seções (`1`, `1.1`, `1.1.1`...) | TCC, Artigo — `redator-academico`, `auditar-obra.py --tipo tcc\|artigo` |
| **NBR 6027** | Elaboração de sumários | Livro, TCC — gerado automaticamente pelo `outline()` do Typst |
| **NBR 6028** | Resumos (extensão, estilo, palavras-chave) | TCC, Artigo — `compilador-tcc`/`compilador-artigo` |

## Notas de aplicação

- **E-book não segue nenhuma destas normas** — é padrão de mercado (ver
  `SPEC_EBOOK.md`), intencionalmente fora desta tabela.
- **Citação dupla convenção:** o livro comercial (`redator-eita`) usa `[N]`
  numérico por tradição editorial e por já estar integrado ao motor de
  auditoria desde a V3; TCC e Artigo usam autor-data por ser a convenção mais
  comum em produção acadêmica brasileira sob a NBR 10520 (que permite ambas).
- **Numeração progressiva não se aplica ao livro comercial** — o `--number-sections`
  do Pandoc numera automaticamente os títulos do livro em estilo próprio
  (não é NBR 6024); TCC/Artigo escrevem a numeração manualmente no texto e o
  Pandoc **não** deve renumerar (por isso `--number-sections` é omitido nesses
  dois tipos — ver `compilar-para-pdf.py`).
