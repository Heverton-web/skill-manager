#!/usr/bin/env python3
"""
Upgrade 1 (motor determinístico) — Auditoria da Obra / Fase 2.5.

Auditor objetivo que roda ANTES da compilacao final e alimenta a skill
`revisor-tecnico` com evidencia dura em vez de impressao subjetiva. Verifica os
requisitos contratuais automatizaveis (R1-R4 e R9-R14; R5-R8 dependem de
julgamento e sao checados pelo pesquisador/compilador/revisor) e detecta os tres
defeitos que o revisor humano
mais procura:

  1. Sobreposicao de conteudo entre capitulos (paragrafos quase identicos)
  2. Inconsistencia terminologica (mesmo termo escrito de formas diferentes)
  3. Capitulos truncados / com marcador de pendencia

Uso:
    python scripts/auditar-obra.py <slug>
    python scripts/auditar-obra.py <slug> --estrito       # exit 1 se NAO CONFORME
    python scripts/auditar-obra.py <slug> --json
    python scripts/auditar-obra.py <slug> --limiar-similaridade 0.5

Fase A (V4) — tipos de obra alem de livro:
    python scripts/auditar-obra.py <slug> --tipo tcc
    python scripts/auditar-obra.py <slug> --tipo artigo --min-refs 5
    (se omitido, --tipo/--min-refs/--tamanho sao lidos de
     output/<slug>/esboco/config_obra.json; sem esboco, assume livro/V3)

Relatorio: output/<slug>/revisao/relatorio_auditoria.json
"""

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import parametros_obra as PO

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

# Defaults V3 (livro, sem esboco/config_obra.json) — ver parametros_obra.py para
# os minimos de TCC/artigo/tamanho de livro (P/M/G).
MIN_CAPITULOS = PO.MIN_CAPITULOS_V3
MIN_CARACTERES = PO.MIN_CARACTERES_V3
MIN_REFS_CAPITULO = PO.MIN_REFS_V3
MIN_CITACOES_CAPITULO = 3
MIN_DIAGRAMAS_CAPITULO = 1
MIN_BLOCOS_CODIGO_CAPITULO = 1

SECOES_EITA = [
    (1, "Introdução"), (2, "Explica"), (3, "Ilustra"), (4, "Técnica"),
    (5, "Aplica"), (6, "Conclusão"), (7, "Referências"),
]

RE_CODIGO = re.compile(r"^[ \t]*```.*?^[ \t]*```[ \t]*$", re.DOTALL | re.MULTILINE)
RE_MERMAID = re.compile(r"^[ \t]*```[ \t]*mermaid", re.MULTILINE | re.IGNORECASE)
RE_CITACAO = re.compile(r"\[\d{1,3}\]")
RE_HR = re.compile(r"^[ \t]*(-{3,}|\*{3,}|_{3,})[ \t]*$", re.MULTILINE)
RE_PENDENCIA = re.compile(
    r"(\bTODO\b|\bFIXME\b|\bTBD\b|lorem ipsum|\[inserir|\[completar|"
    r"placeholder|continua no próximo|a ser escrito|XXX)", re.IGNORECASE)

# Termos tecnicos candidatos: palavras com maiuscula interna, siglas, hifenizados
RE_TERMO = re.compile(r"\b[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9]*(?:[-\.][A-Za-zÀ-ÿ0-9]+)*\b")


def sem_acento(texto):
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


def cabecalho_secao(numero, nome):
    """Regex tolerante para `## 1. Introdução` (aceita variacao de acento/caixa)."""
    alvo = sem_acento(nome).lower()[:6]
    return re.compile(rf"^##\s*{numero}[\.\)]?\s*(?P<t>.+)$", re.MULTILINE), alvo


def dividir_secoes(texto):
    """Retorna dict {numero_secao: corpo} conforme o template EITA-V2."""
    secoes = {}
    marcas = []
    for m in re.finditer(r"^##\s*(\d)[\.\)]?\s*(.+)$", texto, re.MULTILINE):
        marcas.append((int(m.group(1)), m.group(2).strip(), m.start(), m.end()))
    for i, (num, titulo, _ini, fim) in enumerate(marcas):
        prox = marcas[i + 1][2] if i + 1 < len(marcas) else len(texto)
        secoes[num] = {"titulo": titulo, "corpo": texto[fim:prox]}
    return secoes


def shingles(paragrafo, n=6):
    palavras = sem_acento(paragrafo).lower().split()
    if len(palavras) < n:
        return set()
    return {" ".join(palavras[i:i + n]) for i in range(len(palavras) - n + 1)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / (len(a) + len(b) - inter)


def paragrafos_relevantes(texto, minimo_palavras=40):
    limpo = RE_CODIGO.sub("", texto)
    saida = []
    for par in re.split(r"\n\s*\n", limpo):
        par = par.strip()
        if par.startswith("#") or par.startswith("|") or par.startswith(">"):
            continue
        if len(par.split()) >= minimo_palavras:
            saida.append(par)
    return saida


def auditar_capitulo(caminho):
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    numero = re.search(r"cap_(\d+)", caminho.stem).group(1)
    corpo_sem_codigo = RE_CODIGO.sub("", texto)
    secoes = dividir_secoes(texto)

    faltantes = []
    for num, nome in SECOES_EITA:
        alvo = sem_acento(nome).lower()[:6]
        atual = secoes.get(num)
        if atual is None or alvo not in sem_acento(atual["titulo"]).lower():
            faltantes.append(f"{num}. {nome}")

    corpo_refs = secoes.get(7, {}).get("corpo", "")
    refs = RE_CITACAO.findall(corpo_refs)
    refs_unicas = sorted(set(refs), key=lambda x: int(x.strip("[]")))

    # Citacoes inline: fora da secao 7
    corpo_texto = corpo_sem_codigo
    if corpo_refs:
        corpo_texto = corpo_sem_codigo.replace(RE_CODIGO.sub("", corpo_refs), "")
    citacoes_inline = RE_CITACAO.findall(corpo_texto)

    secao_ilustra = secoes.get(3, {}).get("corpo", "")
    diagramas_ilustra = len(RE_MERMAID.findall(secao_ilustra))
    diagramas_total = len(RE_MERMAID.findall(texto))

    secao_tecnica = secoes.get(4, {}).get("corpo", "")
    blocos_codigo = len([m for m in RE_CODIGO.finditer(secao_tecnica)])

    # Horizontal rules fora de frontmatter (R9)
    sem_frontmatter = re.sub(r"\A---\n.*?\n---\n", "", texto, flags=re.DOTALL)
    hrs = len(RE_HR.findall(RE_CODIGO.sub("", sem_frontmatter)))

    pendencias = sorted({m.group(0) for m in RE_PENDENCIA.finditer(corpo_sem_codigo)})

    # Truncamento: ultima linha nao termina com pontuacao de fechamento
    linhas = [l.strip() for l in texto.strip().split("\n") if l.strip()]
    ultima = linhas[-1] if linhas else ""
    truncado = not re.search(r"[\.\!\?\:\)\]\`\|]$", ultima)

    # Referencias fantasma: [N] citada no texto sem entrada na secao 7
    numeros_inline = {int(c.strip("[]")) for c in citacoes_inline}
    numeros_refs = {int(c.strip("[]")) for c in refs_unicas}
    orfas = sorted(numeros_inline - numeros_refs)
    nao_citadas = sorted(numeros_refs - numeros_inline)

    return {
        "capitulo": numero,
        "arquivo": caminho.name,
        "caracteres": len(texto),
        "palavras": len(corpo_sem_codigo.split()),
        "secoes_faltantes": faltantes,
        "referencias": len(refs_unicas),
        "citacoes_inline": len(citacoes_inline),
        "diagramas_ilustra": diagramas_ilustra,
        "diagramas_total": diagramas_total,
        "blocos_codigo_tecnica": blocos_codigo,
        "horizontal_rules": hrs,
        "pendencias": pendencias,
        "truncado": truncado,
        "ultima_linha": ultima[-90:],
        "refs_orfas": orfas,
        "refs_nao_citadas": nao_citadas,
        "_texto": texto,
    }


def _sobrenome_norm(sobrenome):
    return sem_acento(sobrenome).lower().replace(";", "").strip()


def extrair_citacoes_autor_data(texto):
    """Extrai (sobrenome_normalizado, ano) de citacoes NBR 10520 no corpo do texto.

    Heuristico (igual em espirito ao shingle/jaccard ja usado no auditor): cobre
    os formatos mais comuns — parenteses "(SOBRENOME, 2024)"/"(A; B, 2024)" e
    narrativa "Sobrenome (2024)" — mas pode gerar falsos positivos com parenteses
    que por acaso tem Maiuscula+virgula+ano sem ser citacao real.
    """
    achados = set()
    for m in PO.RE_CITACAO_AUTOR_DATA.finditer(texto):
        bruto = m.group(0)
        ano_m = re.search(r"\d{4}[a-z]?", bruto)
        if not ano_m:
            continue
        ano = ano_m.group(0)
        nomes = re.sub(r"[\(\)]", "", bruto)
        nomes = re.sub(r",?\s*\d{4}[a-z]?\)?", "", nomes)
        for nome in re.split(r";", nomes):
            nome = re.sub(r"\(.*", "", nome).strip()
            if nome:
                achados.add((_sobrenome_norm(nome.split()[0] if " " in nome else nome), ano))
    return achados


def extrair_referencias_autor_data(corpo_refs):
    """Extrai (sobrenome_normalizado, ano) de cada entrada da secao de Referencias."""
    achados = set()
    for linha in corpo_refs.split("\n"):
        linha = linha.strip()
        if not linha:
            continue
        m = PO.RE_REF_AUTOR_DATA.match(linha)
        if not m:
            continue
        sobrenomes, ano = m.group(1), m.group(2)
        for nome in re.split(r";", sobrenomes):
            nome = nome.strip()
            if nome:
                achados.add((_sobrenome_norm(nome), ano))
    return achados


def auditar_secao_academica(caminho, tipo, min_refs):
    """Auditoria por secao/capitulo para TCC e Artigo (citacao autor-data, NBR 6024).

    Retorna um dict com o mesmo formato-base de auditar_capitulo() (chaves
    'capitulo'/'_texto' compativeis com detectar_sobreposicao/terminologia), mais
    os campos especificos do fluxo academico.
    """
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    numero = re.search(r"cap_(\d+)|sec_(\d+)", caminho.stem)
    numero = next(g for g in numero.groups() if g) if numero else caminho.stem
    corpo_sem_codigo = RE_CODIGO.sub("", texto)

    # Secao de referencias: ultimo heading do tipo "Referencias" (com ou sem "Bibliograficas")
    m_refs = re.search(
        r"^#{1,3}\s*Refer[êe]ncias(?:\s+Bibliogr[áa]ficas)?\s*$\n(.*)",
        texto, re.MULTILINE | re.IGNORECASE | re.DOTALL)
    corpo_refs = m_refs.group(1) if m_refs else ""
    corpo_texto = corpo_sem_codigo[:m_refs.start()] if m_refs else corpo_sem_codigo

    citacoes = extrair_citacoes_autor_data(corpo_texto)
    referencias = extrair_referencias_autor_data(corpo_refs)

    numeracao_progressiva = bool(PO.RE_NUMERACAO_PROGRESSIVA.search(texto))

    sem_frontmatter = re.sub(r"\A---\n.*?\n---\n", "", texto, flags=re.DOTALL)
    hrs = len(RE_HR.findall(RE_CODIGO.sub("", sem_frontmatter)))

    pendencias = sorted({m.group(0) for m in RE_PENDENCIA.finditer(corpo_sem_codigo)})

    linhas = [l.strip() for l in texto.strip().split("\n") if l.strip()]
    ultima = linhas[-1] if linhas else ""
    truncado = not re.search(r"[\.\!\?\:\)\]\`\|]$", ultima)

    orfas = sorted(citacoes - referencias)
    nao_citadas = sorted(referencias - citacoes)

    return {
        "capitulo": numero,
        "arquivo": caminho.name,
        "caracteres": len(texto),
        "palavras": len(corpo_sem_codigo.split()),
        "numeracao_progressiva": numeracao_progressiva,
        "referencias": len(referencias),
        "citacoes_inline": len(citacoes),
        "horizontal_rules": hrs,
        "pendencias": pendencias,
        "truncado": truncado,
        "ultima_linha": ultima[-90:],
        "refs_orfas": [f"{s} ({a})" for s, a in orfas],
        "refs_nao_citadas": [f"{s} ({a})" for s, a in nao_citadas],
        "_texto": texto,
    }


def detectar_sobreposicao(capitulos, limiar):
    """Paragrafos quase identicos entre capitulos diferentes."""
    indice = []
    for cap in capitulos:
        for par in paragrafos_relevantes(cap["_texto"]):
            sh = shingles(par)
            if sh:
                indice.append((cap["capitulo"], par, sh))

    # Bucketiza por shingle para nao comparar tudo com tudo
    buckets = defaultdict(list)
    for i, (_cap, _par, sh) in enumerate(indice):
        for s in list(sh)[:12]:
            buckets[s].append(i)

    pares_vistos = set()
    achados = []
    for lista in buckets.values():
        if len(lista) < 2:
            continue
        for a in range(len(lista)):
            for b in range(a + 1, len(lista)):
                i, j = lista[a], lista[b]
                if indice[i][0] == indice[j][0]:
                    continue
                chave = (min(i, j), max(i, j))
                if chave in pares_vistos:
                    continue
                pares_vistos.add(chave)
                sim = jaccard(indice[i][2], indice[j][2])
                if sim >= limiar:
                    achados.append({
                        "capitulo_a": indice[i][0],
                        "capitulo_b": indice[j][0],
                        "similaridade": round(sim, 3),
                        "trecho": indice[i][1][:180],
                    })

    # Deduplica: o mesmo paragrafo repetido varias vezes gera pares redundantes
    unicos = {}
    for a in achados:
        chave = (a["capitulo_a"], a["capitulo_b"], a["trecho"][:80])
        if chave not in unicos or a["similaridade"] > unicos[chave]["similaridade"]:
            unicos[chave] = a
    achados = sorted(unicos.values(), key=lambda x: -x["similaridade"])
    return achados[:40]


def detectar_inconsistencia_terminologica(capitulos, minimo_ocorrencias=4):
    """Mesmo termo grafado de formas diferentes ao longo da obra."""
    variantes = defaultdict(lambda: defaultdict(int))
    for cap in capitulos:
        texto = RE_CODIGO.sub("", cap["_texto"])
        for m in RE_TERMO.finditer(texto):
            termo = m.group(0)
            if len(termo) < 4 or termo.isdigit():
                continue
            chave = sem_acento(termo).lower().replace("-", "").replace(".", "")
            variantes[chave][termo] += 1

    achados = []
    for chave, formas in variantes.items():
        if len(formas) < 2:
            continue
        total = sum(formas.values())
        if total < minimo_ocorrencias:
            continue
        # Ignora variacao natural de inicio de frase (Titulo vs titulo)
        so_caixa_inicial = {f.lower() for f in formas}
        if len(so_caixa_inicial) == 1:
            continue
        achados.append({
            "termo_normalizado": chave,
            "variantes": dict(sorted(formas.items(), key=lambda x: -x[1])),
            "ocorrencias": total,
        })
    achados.sort(key=lambda x: -x["ocorrencias"])
    return achados[:25]


def montar_requisitos_livro(capitulos, caracteres_obra, min_capitulos, min_caracteres, min_refs):
    def falhas(pred):
        return [c["capitulo"] for c in capitulos if pred(c)]

    return [
        {"id": "R1", "nome": f"Minimo {min_capitulos} capitulos",
         "conforme": len(capitulos) >= min_capitulos,
         "detalhe": f"{len(capitulos)} capitulo(s) (minimo {min_capitulos})"},
        {"id": "R2", "nome": f"Minimo {round(min_caracteres/2500)} paginas (~{min_caracteres:,} caracteres)".replace(",", "."),
         "conforme": caracteres_obra >= min_caracteres,
         "detalhe": f"{caracteres_obra:,} caracteres (minimo {min_caracteres:,})".replace(",", ".")},
        {"id": "R3", "nome": "7 secoes EITA-V2 por capitulo",
         "conforme": not falhas(lambda c: c["secoes_faltantes"]),
         "detalhe": "capitulos incompletos: " + (", ".join(falhas(lambda c: c["secoes_faltantes"])) or "nenhum")},
        {"id": "R4", "nome": f"Minimo {min_refs} referencias ABNT por capitulo",
         "conforme": not falhas(lambda c: c["referencias"] < min_refs),
         "detalhe": "capitulos abaixo: " + (", ".join(falhas(lambda c: c["referencias"] < min_refs)) or "nenhum")},
        {"id": "R9", "nome": "Ausencia de horizontal rules nos capitulos",
         "conforme": not falhas(lambda c: c["horizontal_rules"] > 0),
         "detalhe": "capitulos com ---: " + (", ".join(falhas(lambda c: c["horizontal_rules"] > 0)) or "nenhum")},
        {"id": "R10", "nome": f"Minimo {MIN_CITACOES_CAPITULO} citacoes inline [N] por capitulo",
         "conforme": not falhas(lambda c: c["citacoes_inline"] < MIN_CITACOES_CAPITULO),
         "detalhe": "capitulos abaixo: " + (", ".join(falhas(lambda c: c["citacoes_inline"] < MIN_CITACOES_CAPITULO)) or "nenhum")},
        {"id": "R11", "nome": f"Minimo {MIN_DIAGRAMAS_CAPITULO} diagrama Mermaid na secao Ilustra",
         "conforme": not falhas(lambda c: c["diagramas_ilustra"] < MIN_DIAGRAMAS_CAPITULO),
         "detalhe": "capitulos sem diagrama: " + (", ".join(falhas(lambda c: c["diagramas_ilustra"] < MIN_DIAGRAMAS_CAPITULO)) or "nenhum")},
        {"id": "R12", "nome": "Bloco de codigo na secao Tecnica",
         "conforme": not falhas(lambda c: c["blocos_codigo_tecnica"] < MIN_BLOCOS_CODIGO_CAPITULO),
         "detalhe": "capitulos sem codigo: " + (", ".join(falhas(lambda c: c["blocos_codigo_tecnica"] < MIN_BLOCOS_CODIGO_CAPITULO)) or "nenhum")},
        {"id": "R13", "nome": "Sem truncamento nem pendencias (TODO/placeholder)",
         "conforme": not falhas(lambda c: c["truncado"] or c["pendencias"]),
         "detalhe": "capitulos suspeitos: " + (", ".join(falhas(lambda c: c["truncado"] or c["pendencias"])) or "nenhum")},
        {"id": "R14", "nome": "Rastreabilidade [N] texto <-> referencias",
         "conforme": not falhas(lambda c: c["refs_orfas"]),
         "detalhe": "capitulos com citacao orfa: " + (", ".join(falhas(lambda c: c["refs_orfas"])) or "nenhum")},
    ]


def montar_requisitos_academico(capitulos, tipo, min_refs):
    """Requisitos verificaveis por secao/capitulo para TCC/Artigo/Ebook.

    Elementos pre-textuais (folha de aprovacao, resumo, abstract) sao verificados
    pelo `scripts/validar-abnt-tcc.py` sobre o documento compilado, nao aqui.
    Ebook nao exige numeracao progressiva nem citacao (padrao de mercado, sem ABNT).
    """
    def falhas(pred):
        return [c["capitulo"] for c in capitulos if pred(c)]

    prefixo = tipo.upper()
    requisitos = []

    if tipo != "ebook":
        requisitos += [
            {"id": f"{prefixo}-NUM", "nome": "Numeracao progressiva de secoes (NBR 6024)",
             "conforme": not falhas(lambda c: not c["numeracao_progressiva"]),
             "detalhe": "secoes sem numeracao: " + (", ".join(falhas(lambda c: not c["numeracao_progressiva"])) or "nenhuma")},
            {"id": f"{prefixo}-REF", "nome": f"Minimo {min_refs} referencias por secao (NBR 6023)",
             "conforme": not falhas(lambda c: c["referencias"] < min_refs),
             "detalhe": "secoes abaixo: " + (", ".join(falhas(lambda c: c["referencias"] < min_refs)) or "nenhuma")},
            {"id": f"{prefixo}-CIT", "nome": "Citacoes autor-data presentes (NBR 10520)",
             "conforme": not falhas(lambda c: c["citacoes_inline"] < 1),
             "detalhe": "secoes sem citacao: " + (", ".join(falhas(lambda c: c["citacoes_inline"] < 1)) or "nenhuma")},
        ]

    requisitos += [
        {"id": f"{prefixo}-HR", "nome": "Ausencia de horizontal rules nas secoes",
         "conforme": not falhas(lambda c: c["horizontal_rules"] > 0),
         "detalhe": "secoes com ---: " + (", ".join(falhas(lambda c: c["horizontal_rules"] > 0)) or "nenhuma")},
        {"id": f"{prefixo}-TRUNC", "nome": "Sem truncamento nem pendencias (TODO/placeholder)",
         "conforme": not falhas(lambda c: c["truncado"] or c["pendencias"]),
         "detalhe": "secoes suspeitas: " + (", ".join(falhas(lambda c: c["truncado"] or c["pendencias"])) or "nenhuma")},
    ]

    if tipo != "ebook":
        requisitos.append(
            {"id": f"{prefixo}-RASTRO", "nome": "Rastreabilidade citacao <-> referencias",
             "conforme": not falhas(lambda c: c["refs_orfas"]),
             "detalhe": "secoes com citacao orfa: " + (", ".join(falhas(lambda c: c["refs_orfas"])) or "nenhuma")})

    return requisitos


def main():
    ap = argparse.ArgumentParser(description="Auditoria contratual da obra (Fase 2.5)")
    ap.add_argument("slug")
    ap.add_argument("--tipo", choices=("livro", "tcc", "artigo", "ebook"), default=None,
                    help="por padrao, lido de output/<slug>/esboco/config_obra.json")
    ap.add_argument("--min-refs", type=int, default=None,
                    help="override do minimo de referencias (padrao: config_obra.json)")
    ap.add_argument("--tamanho", choices=("P", "M", "G"), default=None,
                    help="override do tamanho do livro (padrao: config_obra.json)")
    ap.add_argument("--limiar-similaridade", type=float, default=0.45,
                    help="limiar de Jaccard para acusar sobreposicao (padrao 0.45)")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se a obra estiver NAO CONFORME")
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON completo")
    args = ap.parse_args()

    dir_livro = DIR_OUTPUT / args.slug
    dir_caps = dir_livro / "capitulos"
    if not dir_caps.exists():
        print(f"[ERRO] Capitulos nao encontrados: {dir_caps}")
        return 1

    config = PO.carregar_config(args.slug)
    tipo = args.tipo or config["tipo_obra"]
    min_refs = args.min_refs or config["min_referencias_por_capitulo"]
    tamanho = args.tamanho or config.get("tamanho_obra")
    minimos = PO.minimos_livro(tamanho) if tipo == "livro" and config.get("_origem") == "esboco" else None

    caminhos = sorted(dir_caps.glob("cap_*.md"),
                      key=lambda p: int(re.search(r"cap_(\d+)", p.stem).group(1)))
    caminhos = [c for c in caminhos if not c.stem.startswith("_")]
    if not caminhos:
        print(f"[ERRO] Nenhum cap_*.md em {dir_caps}")
        return 1

    if tipo == "livro":
        capitulos = [auditar_capitulo(c) for c in caminhos]
    else:
        capitulos = [auditar_secao_academica(c, tipo, min_refs) for c in caminhos]

    livro_final = dir_livro / "livro_final.md"
    caracteres_obra = (len(livro_final.read_text(encoding="utf-8", errors="replace"))
                       if livro_final.exists()
                       else sum(c["caracteres"] for c in capitulos))

    sobreposicao = detectar_sobreposicao(capitulos, args.limiar_similaridade)
    terminologia = detectar_inconsistencia_terminologica(capitulos)

    # ── Requisitos contratuais ────────────────────────────────────
    if tipo == "livro":
        min_capitulos = minimos["capitulos"] if minimos else MIN_CAPITULOS
        min_caracteres = minimos["caracteres"] if minimos else MIN_CARACTERES
        requisitos = montar_requisitos_livro(capitulos, caracteres_obra,
                                             min_capitulos, min_caracteres, min_refs)
    else:
        requisitos = montar_requisitos_academico(capitulos, tipo, min_refs)

    nao_conformes = [r for r in requisitos if not r["conforme"]]
    veredito = "CONFORME" if not nao_conformes else "NAO CONFORME"

    relatorio = {
        "slug": args.slug,
        "tipo_obra": tipo,
        "veredito": veredito,
        "total_capitulos": len(capitulos),
        "caracteres_obra": caracteres_obra,
        "paginas_estimadas": round(caracteres_obra / 2500, 1),
        "requisitos": requisitos,
        "sobreposicao_entre_capitulos": sobreposicao,
        "inconsistencia_terminologica": terminologia,
        "capitulos": [{k: v for k, v in c.items() if k != "_texto"} for c in capitulos],
    }

    dir_rev = dir_livro / "revisao"
    dir_rev.mkdir(exist_ok=True)
    destino = dir_rev / "relatorio_auditoria.json"
    destino.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── Saida humana compacta ─────────────────────────────────────
    print(f"AUDITORIA DA OBRA - {args.slug}")
    print(f"  capitulos: {len(capitulos)} | caracteres: {caracteres_obra:,}".replace(",", ".")
          + f" | ~{relatorio['paginas_estimadas']} paginas")
    print("")
    for r in requisitos:
        marca = "OK  " if r["conforme"] else "FALHA"
        print(f"  [{marca}] {r['id']:<4} {r['nome']}")
        if not r["conforme"]:
            print(f"           -> {r['detalhe']}")
    print("")
    if sobreposicao:
        print(f"  [ALERTA] {len(sobreposicao)} par(es) de paragrafos sobrepostos entre capitulos:")
        for s in sobreposicao[:5]:
            print(f"    cap {s['capitulo_a']} <-> cap {s['capitulo_b']} "
                  f"(sim={s['similaridade']}): {s['trecho'][:90]}...")
    else:
        print("  [OK] Nenhuma sobreposicao relevante entre capitulos")
    if terminologia:
        print(f"  [ALERTA] {len(terminologia)} termo(s) com grafia inconsistente:")
        for t in terminologia[:5]:
            formas = ", ".join(f"{k}({v})" for k, v in list(t["variantes"].items())[:4])
            print(f"    {t['termo_normalizado']}: {formas}")
    else:
        print("  [OK] Terminologia consistente")

    print(f"\n  VEREDITO: {veredito}")
    print(f"  Relatorio: {destino.relative_to(DIR_PROJETO)}")

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    if args.estrito and nao_conformes:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
