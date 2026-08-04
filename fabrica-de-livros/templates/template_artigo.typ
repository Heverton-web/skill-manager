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

#set document(title: "$title$", author: "$author$", date: datetime.today())

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

#set text(font: ("Times New Roman", "Liberation Serif"), size: 12pt, lang: "pt", region: "BR")
#set par(justify: true, leading: 0.75em, first-line-indent: 1.25cm)

#let horizontalrule = { v(1em); line(length: 100%, stroke: 1pt + cor.destaque); v(1em) }

#show raw.where(block: true): block.with(width: 100%, fill: cor.clara, stroke: 0.5pt + cor.secundaria, inset: 8pt, radius: 4pt)
#show raw.where(block: false): box.with(fill: cor.clara, inset: (x: 3pt, y: 0pt), outset: (y: 3pt), radius: 2pt)

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

// Secoes NAO quebram pagina — fluxo continuo, tipico de periodico academico
#show heading.where(level: 1): it => {
  set par(first-line-indent: 0cm)
  set text(font: ("Inter", "sans-serif"), size: 13pt, weight: "bold", fill: cor.primaria)
  v(1cm)
  upper(it)
  v(0.2cm)
  line(length: 25%, stroke: 1.5pt + cor.destaque)
  v(0.5cm)
}
#show heading.where(level: 2): it => {
  set text(font: ("Inter", "sans-serif"), size: 12pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(0.6cm)
  it
  v(0.3cm)
}
#show heading.where(level: 3): it => {
  set text(font: ("Inter", "sans-serif"), size: 12pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(0.5cm)
  it
  v(0.25cm)
}

// ── CABECALHO DO ARTIGO (titulo, autor, resumo, abstract — sem paginas separadas) ──
#align(center)[
  #text(font: ("Inter", "sans-serif"), size: 16pt, weight: "bold", fill: cor.primaria)[$title$]
  $if(subtitle)$
  #v(0.3cm)
  #text(font: ("Inter", "sans-serif"), size: 12pt, fill: cor.secundaria)[$subtitle$]
  $endif$
  #v(0.6cm)
  #text(font: ("Inter", "sans-serif"), size: 11.5pt, fill: cor.secundaria)[$author$]
]

$if(resumo)$
#v(1cm)
#block(width: 100%)[
  #set par(first-line-indent: 0cm, justify: true)
  #text(font: ("Inter", "sans-serif"), weight: "bold", fill: cor.primaria)[RESUMO]
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
  #text(font: ("Inter", "sans-serif"), weight: "bold", fill: cor.primaria)[ABSTRACT]
  #v(0.3cm)
  $abstract_en$
  $if(keywords_en)$
  #v(0.3cm)
  *Keywords:* $keywords_en$.
  $endif$
]
$endif$

#v(1cm)
#line(length: 100%, stroke: 1pt + cor.destaque)
#v(0.5cm)

// ── CORPO (Introducao / Metodologia / Resultados / Conclusao / Referencias) ──
$body$
