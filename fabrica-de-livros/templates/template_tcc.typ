// ── Paleta cromatica da obra ──────────────────────────────────────
#let paletas = (
  indigo:    (primaria: rgb("#1b2559"), secundaria: rgb("#3d55a5"), destaque: rgb("#f0b429"), clara: rgb("#eef1fa")),
  grafite:   (primaria: rgb("#22262b"), secundaria: rgb("#4a5259"), destaque: rgb("#59c1bd"), clara: rgb("#eef0f1")),
  vinho:     (primaria: rgb("#5b1420"), secundaria: rgb("#8c2b3c"), destaque: rgb("#e0a458"), clara: rgb("#f8eef0")),
  floresta:  (primaria: rgb("#123324"), secundaria: rgb("#2c6e49"), destaque: rgb("#d8f3a3"), clara: rgb("#eef5ef")),
  ambar:     (primaria: rgb("#432818"), secundaria: rgb("#99582a"), destaque: rgb("#ffe6a7"), clara: rgb("#f8f1e7")),
  oceano:    (primaria: rgb("#03254c"), secundaria: rgb("#1167b1"), destaque: rgb("#7fd6f7"), clara: rgb("#e9f3fa")),
)

#let chave-paleta = {
  let p = "$paleta$"
  if p == "" or not p in paletas { "indigo" } else { p }
}
#let cor = paletas.at(chave-paleta)

#set document(
  title: "$title$",
  author: "$author$",
  date: datetime.today(),
)

#set page(
  paper: "a4",
  margin: (top: 3cm, bottom: 2cm, left: 3cm, right: 2cm),
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 9pt, fill: cor.secundaria)
      align(center, "$title$")
    }
  },
  footer: context {
    set text(size: 9pt)
    align(center, [#counter(page).display("1") de #counter(page).final().first()])
  },
)

#set text(
  font: ("Times New Roman", "Liberation Serif"),
  size: 12pt,
  lang: "pt",
  region: "BR",
)

#set par(
  justify: true,
  leading: 0.75em,
  first-line-indent: 1.25cm,
)

#let horizontalrule = {
  v(1em)
  line(length: 100%, stroke: 1pt + cor.destaque)
  v(1em)
}

#show raw.where(block: true): block.with(
  width: 100%, fill: cor.clara, stroke: 0.5pt + cor.secundaria, inset: 8pt, radius: 4pt,
)
#show raw.where(block: false): box.with(
  fill: cor.clara, inset: (x: 3pt, y: 0pt), outset: (y: 3pt), radius: 2pt,
)

#show quote: it => block(
  width: 100%,
  fill: cor.clara,
  inset: (left: 12pt, right: 8pt, top: 8pt, bottom: 8pt),
  stroke: (left: 3pt + cor.destaque),
  radius: (right: 4pt),
  it,
)

#set image(width: 88%, fit: "contain")
#show figure: it => { set par(first-line-indent: 0cm); v(0.6em); align(center, it); v(0.6em) }
#show figure.caption: it => { set text(font: ("Inter", "sans-serif"), size: 10pt, fill: cor.secundaria, weight: "bold"); it }

// Regra geral de titulos: sempre fonte INTER e cores da paleta da capa
#show heading: set text(font: ("Inter", "Liberation Sans", "Arial", "sans-serif"))

// Titulos: nivel 1 = secao principal numerada (Introducao, Referencial Teorico N, ...)
#show heading.where(level: 1): it => {
  set par(first-line-indent: 0cm)
  set text(font: ("Inter", "sans-serif"), size: 14pt, weight: "bold", fill: cor.primaria)
  pagebreak()
  v(1cm)
  upper(it)
  v(0.3cm)
  line(length: 25%, stroke: 1.5pt + cor.destaque)
  v(0.8cm)
}
#show heading.where(level: 2): it => {
  set text(font: ("Inter", "sans-serif"), size: 12pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(0.75cm)
  it
  v(0.4cm)
}
#show heading.where(level: 3): it => {
  set text(font: ("Inter", "sans-serif"), size: 12pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(0.6cm)
  it
  v(0.3cm)
}

// ── CAPA (NBR 14724 — sem cor, sem marca comercial) ───────────────
#page(header: none, footer: none, numbering: none)[
  #set par(first-line-indent: 0cm, justify: false)
  #align(center)[
    $if(instituicao)$
    #text(size: 12pt)[$instituicao$]
    #v(0.3cm)
    $endif$
    $if(curso)$
    #text(size: 12pt)[$curso$]
    $endif$
    #v(4cm)
    #text(size: 13pt, weight: "bold")[$author$]
    #v(4cm)
    #text(size: 16pt, weight: "bold")[$title$]
    $if(subtitle)$
    #v(0.4cm)
    #text(size: 13pt)[$subtitle$]
    $endif$
  ]
  #v(1fr)
  #align(center)[
    $if(local)$$local$$else$Brasil$endif$
    #linebreak()
    $if(ano)$$ano$$else$#datetime.today().display("[year]")$endif$
  ]
]

// ── FOLHA DE ROSTO ─────────────────────────────────────────────────
#page(header: none, footer: none, numbering: none)[
  #set par(first-line-indent: 0cm, justify: false)
  #align(center)[
    #text(size: 13pt, weight: "bold")[$author$]
    #v(4cm)
    #text(size: 16pt, weight: "bold")[$title$]
  ]
  #v(1.5cm)
  #align(right, block(width: 9cm)[
    #set text(size: 11pt)
    #set par(justify: true, first-line-indent: 0cm)
    Trabalho de Conclusão de Curso apresentado
    $if(curso)$ao curso de $curso$$endif$
    como requisito parcial para obtenção do título de graduado.
    $if(orientador)$
    #v(0.5cm)
    Orientador(a): $orientador$
    $endif$
  ])
  #v(1fr)
  #align(center)[
    $if(local)$$local$$else$Brasil$endif$
    #linebreak()
    $if(ano)$$ano$$else$#datetime.today().display("[year]")$endif$
  ]
]

// ── FOLHA DE APROVACAO (NBR 14724) ────────────────────────────────
#page(header: none, footer: none, numbering: none)[
  #set par(first-line-indent: 0cm, justify: false)
  #align(center)[
    #text(size: 13pt, weight: "bold")[$author$]
    #v(1cm)
    #text(size: 14pt, weight: "bold")[$title$]
  ]
  #v(1cm)
  #block(width: 100%)[
    #set text(size: 11pt)
    #set par(justify: true, first-line-indent: 0cm)
    Trabalho de Conclusão de Curso aprovado como requisito parcial para obtenção do
    título de graduado, pela banca examinadora formada por:
  ]
  #v(2.5cm)
  #for i in range(3) [
    #line(length: 9cm, stroke: 0.5pt + black)
    #v(0.15cm)
    #text(size: 10.5pt)[Membro da banca examinadora]
    #v(1.5cm)
  ]
  #v(1fr)
  #align(center)[
    $if(local)$$local$$else$Brasil$endif$, $if(ano)$$ano$$else$#datetime.today().display("[year]")$endif$
  ]
]

// ── RESUMO (NBR 6028) ─────────────────────────────────────────────
$if(resumo)$
#page(header: none, footer: none, numbering: none)[
  #set par(first-line-indent: 0cm)
  #align(center, text(size: 13pt, weight: "bold")[RESUMO])
  #v(1cm)
  #par(justify: true, first-line-indent: 0cm)[$resumo$]
  #v(0.5cm)
  #if "$palavras_chave$" != "" [
    *Palavras-chave:* $palavras_chave$.
  ]
]
$endif$

// ── ABSTRACT ───────────────────────────────────────────────────────
$if(abstract_en)$
#page(header: none, footer: none, numbering: none)[
  #set par(first-line-indent: 0cm)
  #align(center, text(size: 13pt, weight: "bold")[ABSTRACT])
  #v(1cm)
  #par(justify: true, first-line-indent: 0cm)[$abstract_en$]
  #v(0.5cm)
  #if "$keywords_en$" != "" [
    *Keywords:* $keywords_en$.
  ]
]
$endif$

// ── SUMARIO (NBR 6027) ────────────────────────────────────────────
#outline(title: [Sumário], indent: 1.5cm, depth: 3)

// ── CONTEUDO PRINCIPAL (Introducao / Referencial Teorico / ... ) ─
$body$
