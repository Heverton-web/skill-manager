#!/usr/bin/env python3
"""
Upgrade 6 — RAG Local do Dossie de Pesquisa (Fabrica Agentica de Livros).

Indexa os dossies de `output/<slug>/pesquisa/dossie_*.md` em blocos e permite
busca por relevancia (TF-IDF + cosseno, 100% Python puro, sem dependencias).

Objetivo: o `subagente-redator-capitulo` NAO precisa mais carregar o dossie
completo no contexto — ele consulta apenas os blocos relevantes ao seu capitulo.

Uso:
    python scripts/indexar-dossie.py <slug> --indexar
    python scripts/indexar-dossie.py <slug> --buscar "cache semantico latencia" --topo 5
    python scripts/indexar-dossie.py <slug> --buscar "..." --topo 5 --chars 1200
    python scripts/indexar-dossie.py <slug> --stats

Saida do indice: output/<slug>/pesquisa/indice_dossie.json
"""

import argparse
import json
import math
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

TAMANHO_BLOCO_ALVO = 900      # caracteres por bloco (alvo)
TAMANHO_BLOCO_MAX = 1600      # corte duro

STOPWORDS = {
    "a", "ao", "aos", "aquela", "aquelas", "aquele", "aqueles", "aquilo", "as",
    "ate", "com", "como", "da", "das", "de", "dela", "delas", "dele", "deles",
    "depois", "do", "dos", "e", "ela", "elas", "ele", "eles", "em", "entre",
    "era", "eram", "essa", "essas", "esse", "esses", "esta", "estas", "este",
    "estes", "eu", "foi", "foram", "ha", "isso", "isto", "ja", "la", "lhe",
    "lhes", "mais", "mas", "me", "mesmo", "meu", "meus", "minha", "minhas",
    "muito", "na", "nao", "nas", "nem", "no", "nos", "nossa", "nossas",
    "nosso", "nossos", "num", "numa", "o", "os", "ou", "para", "pela",
    "pelas", "pelo", "pelos", "por", "qual", "quando", "que", "quem", "se",
    "sem", "ser", "sera", "seu", "seus", "so", "sob", "sobre", "sua", "suas",
    "tambem", "te", "tem", "tinha", "um", "uma", "voce", "voces",
}


def normalizar(texto):
    """Minusculas, sem acento, sem pontuacao."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower()


def tokenizar(texto):
    tokens = re.findall(r"[a-z0-9][a-z0-9\-_\.]{1,}", normalizar(texto))
    return [t.strip(".-_") for t in tokens if t not in STOPWORDS and len(t) > 2]


def extrair_urls(texto):
    return sorted(set(re.findall(r"https?://[^\s\)\]\>\"']+", texto)))


def dividir_em_blocos(texto, arquivo):
    """Divide o dossie em blocos coerentes: quebra por heading, agrupa paragrafos."""
    blocos = []
    titulo_corrente = "(sem titulo)"
    buffer = []
    tamanho = 0

    def descarregar():
        nonlocal buffer, tamanho
        if not buffer:
            return
        conteudo = "\n\n".join(buffer).strip()
        if conteudo:
            blocos.append({
                "arquivo": arquivo,
                "titulo": titulo_corrente,
                "texto": conteudo,
                "urls": extrair_urls(conteudo),
            })
        buffer = []
        tamanho = 0

    # Em blocos de codigo nao quebramos no meio
    linhas = texto.split("\n")
    paragrafo = []
    dentro_codigo = False
    paragrafos = []
    heading_do_paragrafo = []
    heading_atual = "(sem titulo)"

    for linha in linhas:
        if linha.lstrip().startswith("```"):
            dentro_codigo = not dentro_codigo
            paragrafo.append(linha)
            continue
        if not dentro_codigo and re.match(r"^#{1,6}\s+", linha):
            if paragrafo:
                paragrafos.append("\n".join(paragrafo).strip())
                heading_do_paragrafo.append(heading_atual)
                paragrafo = []
            heading_atual = re.sub(r"^#{1,6}\s+", "", linha).strip()
            continue
        if not dentro_codigo and linha.strip() == "":
            if paragrafo:
                paragrafos.append("\n".join(paragrafo).strip())
                heading_do_paragrafo.append(heading_atual)
                paragrafo = []
            continue
        paragrafo.append(linha)

    if paragrafo:
        paragrafos.append("\n".join(paragrafo).strip())
        heading_do_paragrafo.append(heading_atual)

    for par, head in zip(paragrafos, heading_do_paragrafo):
        if not par:
            continue
        if head != titulo_corrente and buffer:
            descarregar()
        titulo_corrente = head
        if tamanho + len(par) > TAMANHO_BLOCO_MAX and buffer:
            descarregar()
            titulo_corrente = head
        buffer.append(par)
        tamanho += len(par)
        if tamanho >= TAMANHO_BLOCO_ALVO:
            descarregar()
            titulo_corrente = head

    descarregar()
    return blocos


def construir_indice(slug):
    dir_pesquisa = DIR_OUTPUT / slug / "pesquisa"
    if not dir_pesquisa.exists():
        print(f"[ERRO] Diretorio de pesquisa nao encontrado: {dir_pesquisa}")
        return None

    fontes = sorted(dir_pesquisa.glob("dossie*.md")) + sorted(dir_pesquisa.glob("*.md"))
    vistos = set()
    arquivos = []
    for f in fontes:
        if f.name in vistos or f.name == "indice_dossie.json":
            continue
        vistos.add(f.name)
        arquivos.append(f)

    if not arquivos:
        print(f"[ERRO] Nenhum dossie .md em {dir_pesquisa}")
        return None

    blocos = []
    for arq in arquivos:
        texto = arq.read_text(encoding="utf-8", errors="replace")
        for bloco in dividir_em_blocos(texto, arq.name):
            bloco["id"] = f"B{len(blocos) + 1:04d}"
            bloco["tokens"] = dict(Counter(tokenizar(bloco["titulo"] + " " + bloco["texto"])))
            blocos.append(bloco)

    total = len(blocos)
    docfreq = Counter()
    for bloco in blocos:
        for termo in bloco["tokens"]:
            docfreq[termo] += 1

    idf = {t: math.log((total + 1) / (df + 0.5)) for t, df in docfreq.items()}

    # Pre-computa norma dos vetores TF-IDF
    for bloco in blocos:
        peso = {t: (1 + math.log(f)) * idf.get(t, 0.0) for t, f in bloco["tokens"].items()}
        bloco["norma"] = math.sqrt(sum(v * v for v in peso.values())) or 1.0

    indice = {
        "slug": slug,
        "arquivos": [a.name for a in arquivos],
        "total_blocos": total,
        "idf": idf,
        "blocos": blocos,
    }

    destino = dir_pesquisa / "indice_dossie.json"
    destino.write_text(json.dumps(indice, ensure_ascii=False), encoding="utf-8")
    kb = destino.stat().st_size / 1024
    print(f"[OK] Indice gerado: {destino.relative_to(DIR_PROJETO)} "
          f"({total} blocos, {len(arquivos)} dossie(s), {kb:.1f} KB)")
    return indice


def carregar_indice(slug, auto_indexar=True):
    caminho = DIR_OUTPUT / slug / "pesquisa" / "indice_dossie.json"
    if not caminho.exists():
        if not auto_indexar:
            print(f"[ERRO] Indice inexistente. Rode: python scripts/indexar-dossie.py {slug} --indexar")
            return None
        return construir_indice(slug)
    return json.loads(caminho.read_text(encoding="utf-8"))


def buscar(slug, consulta, topo=5, chars=900):
    indice = carregar_indice(slug)
    if not indice:
        return 1

    termos = Counter(tokenizar(consulta))
    if not termos:
        print("[ERRO] Consulta sem termos uteis apos normalizacao")
        return 1

    idf = indice["idf"]
    peso_q = {t: (1 + math.log(f)) * idf.get(t, math.log(len(indice["blocos"]) + 1))
              for t, f in termos.items()}
    norma_q = math.sqrt(sum(v * v for v in peso_q.values())) or 1.0

    pontuados = []
    for bloco in indice["blocos"]:
        tokens = bloco["tokens"]
        acumulado = 0.0
        for termo, pq in peso_q.items():
            f = tokens.get(termo)
            if f:
                acumulado += pq * (1 + math.log(f)) * idf.get(termo, 0.0)
        if acumulado > 0:
            pontuados.append((acumulado / (norma_q * bloco["norma"]), bloco))

    pontuados.sort(key=lambda x: -x[0])
    if not pontuados:
        print("[AVISO] Nenhum bloco relevante encontrado para a consulta")
        return 0

    print(f"# Blocos relevantes do dossie ({min(topo, len(pontuados))} de {len(pontuados)})")
    for score, bloco in pontuados[:topo]:
        trecho = bloco["texto"]
        if len(trecho) > chars:
            trecho = trecho[:chars].rstrip() + " [...]"
        print(f"\n## {bloco['id']} | {bloco['titulo']} | {bloco['arquivo']} | score={score:.3f}")
        print(trecho)
        if bloco["urls"]:
            print("FONTES: " + " ; ".join(bloco["urls"][:4]))
    return 0


def stats(slug):
    indice = carregar_indice(slug, auto_indexar=False)
    if not indice:
        return 1
    print(f"slug: {indice['slug']}")
    print(f"dossies: {', '.join(indice['arquivos'])}")
    print(f"blocos: {indice['total_blocos']}")
    print(f"termos no vocabulario: {len(indice['idf'])}")
    urls = sorted({u for b in indice["blocos"] for u in b["urls"]})
    print(f"urls unicas: {len(urls)}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="RAG local do dossie de pesquisa")
    ap.add_argument("slug")
    ap.add_argument("--indexar", action="store_true", help="(re)constroi o indice")
    ap.add_argument("--buscar", metavar="CONSULTA", help="busca blocos relevantes")
    ap.add_argument("--topo", type=int, default=5, help="numero de blocos retornados")
    ap.add_argument("--chars", type=int, default=900, help="tamanho maximo do trecho por bloco")
    ap.add_argument("--stats", action="store_true", help="mostra estatisticas do indice")
    args = ap.parse_args()

    if args.indexar:
        return 0 if construir_indice(args.slug) else 1
    if args.buscar:
        return buscar(args.slug, args.buscar, args.topo, args.chars)
    if args.stats:
        return stats(args.slug)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
