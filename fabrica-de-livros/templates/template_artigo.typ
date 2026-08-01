// Template ABNT para Artigo Cientifico - Fabrica Agentica de Publicacoes (V4)
// NBR 6022 (periodico) / NBR 12820 (evento), NBR 6028 (resumo)
// Formato compacto: sem capa, sem folha de rosto, sem sumario, secoes NAO
// quebram pagina (fluxo continuo, como em periodicos reais).
// NAO use --number-sections no Pandoc: cabecalhos ja trazem numeracao manual.

#set document(title: "$title$", author: "$author$", date: datetime.today())

#set page(
  paper: "a4",
  margin: (top: 3cm, bottom: 2cm, left: 3cm, right: 2cm),
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 9pt, fill: gray)
      align(center, "$title$")
    }
  },
  footer: context {
    set text(size: 9pt)
    align(center, [#counter(page).display("1") de #counter(page).final().first()])
  },
)

#set text(font: ("Times New Roman", "Liberation Serif"), size: 12pt, lang: "pt", region: "BR")
#set par(justify: true, leading: 0.75em, first-line-indent: 1.25cm)

#let horizontalrule = { v(1em); line(length: 100%, stroke: 0.5pt + gray); v(1em) }

#show raw.where(block: true): block.with(width: 100%, fill: luma(240), inset: 8pt, radius: 4pt)
#show raw.where(block: false): box.with(fill: luma(240), inset: (x: 3pt, y: 0pt), outset: (y: 3pt), radius: 2pt)

#set image(width: 88%, fit: "contain")
#show figure: it => { set par(first-line-indent: 0cm); v(0.6em); align(center, it); v(0.6em) }
#show figure.caption: it => { set text(size: 10pt, fill: luma(70)); it }

// Secoes NAO quebram pagina — fluxo continuo, tipico de periodico academico
#show heading.where(level: 1): it => {
  set par(first-line-indent: 0cm)
  set text(size: 13pt, weight: "bold")
  v(1cm)
  upper(it)
  v(0.5cm)
}
#show heading.where(level: 2): it => {
  set text(size: 12pt, weight: "bold")
  set par(first-line-indent: 0cm)
  v(0.6cm)
  it
  v(0.3cm)
}
#show heading.where(level: 3): it => {
  set text(size: 12pt, style: "italic")
  set par(first-line-indent: 0cm)
  v(0.5cm)
  it
  v(0.25cm)
}

// ── CABECALHO DO ARTIGO (titulo, autor, resumo, abstract — sem paginas separadas) ──
#align(center)[
  #text(size: 15pt, weight: "bold")[$title$]
  $if(subtitle)$
  #v(0.3cm)
  #text(size: 12pt)[$subtitle$]
  $endif$
  #v(0.6cm)
  #text(size: 11.5pt)[$author$]
]

$if(resumo)$
#v(1cm)
#block(width: 100%)[
  #set par(first-line-indent: 0cm, justify: true)
  *RESUMO*
  #v(0.3cm)
  $resumo$
  $if(palavras_chave)$
  #v(0.3cm)
  *Palavras-chave:* $palavras_chave$.
  $endif$
]
$endif$

$if(abstract_en)$
#v(0.8cm)
#block(width: 100%)[
  #set par(first-line-indent: 0cm, justify: true)
  *ABSTRACT*
  #v(0.3cm)
  $abstract_en$
  $if(keywords_en)$
  #v(0.3cm)
  *Keywords:* $keywords_en$.
  $endif$
]
$endif$

#v(1cm)
#line(length: 100%, stroke: 0.4pt + gray)
#v(0.5cm)

// ── CORPO (Introducao / Metodologia / Resultados / Conclusao / Referencias) ──
$body$
