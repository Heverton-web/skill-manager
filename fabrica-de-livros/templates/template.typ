// Template ABNT para Livros - Fabrica Agentica de Livros
// Compativel com Pandoc + Typst

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
      set text(size: 9pt, fill: gray)
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

// Definicao do horizontal rule (Pandoc gera #horizontalrule como texto)
#let horizontalrule = {
  v(1em)
  line(length: 100%, stroke: 0.5pt + gray)
  v(1em)
}

// Estilo de blocos de codigo
#show raw.where(block: true): block.with(
  width: 100%,
  fill: luma(240),
  inset: 8pt,
  radius: 4pt,
)

// Estilo de codigo inline
#show raw.where(block: false): box.with(
  fill: luma(240),
  inset: (x: 3pt, y: 0pt),
  outset: (y: 3pt),
  radius: 2pt,
)

// Estilo de titulos - nivel 1 (com suporte a Parte)
#show heading.where(level: 1): it => {
  set par(first-line-indent: 0cm)
  let isParte = type(it.body) == str and it.body.starts-with("Parte")
  pagebreak()
  if isParte {
    set text(size: 20pt, weight: "bold")
    v(3cm)
    it
    v(2cm)
  } else {
    set text(size: 16pt, weight: "bold")
    v(2cm)
    it
    v(1cm)
  }
}

// Estilo de titulos - nivel 2
#show heading.where(level: 2): it => {
  set text(size: 14pt, weight: "bold")
  set par(first-line-indent: 0cm)
  v(1cm)
  it
  v(0.5cm)
}

// Estilo de titulos - nivel 3
#show heading.where(level: 3): it => {
  set text(size: 12pt, weight: "bold")
  set par(first-line-indent: 0cm)
  v(0.75cm)
  it
  v(0.5cm)
}

// Capa
#{
  set page(header: none, footer: none)
  set par(first-line-indent: 0cm)
  align(center + horizon)[
    #v(4cm)
    #text(size: 28pt, weight: "bold")["$title$"]
    #{
      let sub = "$subtitle$"
      if sub != "" [
        #v(0.5cm)
        #text(size: 16pt)[#sub]
      ]
    }
    #v(2cm)
    #text(size: 14pt)["$author$"]
    #v(1cm)
    #text(size: 12pt, fill: gray)[#datetime.today().display("[day] de [month repr:long] de [year]")]
  ]
  pagebreak()
}

// Sumario
#outline(title: [Sumario], indent: 1.5cm, depth: 3)

// Conteudo principal
$body$

// Referencias Bibliograficas (se existirem)
#pagebreak()
