#!/usr/bin/env python3
"""
Fase C (V4) — Fatiamento do livro-mae em N Artigos Cientificos (ou N E-books).

Artigos e ebooks NAO pesquisam do zero: reaproveitam o dossie/sumario ja
produzidos para o livro-mae (Upgrade 6 da V3 — RAG). Este script apenas particiona
o `sumario_macro.json` do livro-mae em N recortes tematicos e cria a estrutura de
pastas de cada unidade derivada, sem duplicar o indice RAG (o subagente de cada
artigo/ebook consulta `indexar-dossie.py <slug-do-livro-mae> --buscar ...`
diretamente — o slug do livro-mae, nao o do artigo/ebook).

Layout gerado (modo --artigos; artigos e ebooks vivem no TOPO de output/, nao
aninhados sob o livro-mae, para permitir listar todos os artigos/ebooks de
qualquer livro em um so lugar):
    output/artigos/<slug-livro-mae>--art-<NN>-<slug-titulo>/
        sumario_macro.json     (schema IMRaD: 1 parte, 4 secoes fixas; carrega
                                 slug_livro_mae para referencia cruzada)
        config_obra.json       (tipo_obra=artigo, min_referencias_por_capitulo)
        capitulos/ revisao/    (vazias, preenchidas na Fase 2; validacao/ so e
                                 criada quando ha algo a validar)
    output/<slug-livro-mae>/derivados.json   (manifesto de artigos E ebooks do livro)

Uso:
    python scripts/fatiar-obra.py <slug-livro-mae> --artigos [--qtd N]
    python scripts/fatiar-obra.py <slug-livro-mae> --ebooks [--qtd N]
    (--qtd omitido: le qtd_artigos/qtd_ebooks de <slug-livro-mae>/config_obra.json)

    <slug-livro-mae> inclui o prefixo de tipo do livro-mae, ex. "livros/meu-livro".
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

SECOES_ARTIGO_FIXAS = ["Introdução", "Metodologia", "Resultados e Discussão", "Conclusão"]


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))


def slugificar(texto, max_len=40):
    t = sem_acento(texto).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:max_len].rstrip("-") or "recorte"


def carregar_derivados(dir_mae):
    caminho = dir_mae / "derivados.json"
    if caminho.exists():
        return json.loads(caminho.read_text(encoding="utf-8"))
    return {"slug_livro_mae": dir_mae.name, "artigos": {"total": 0, "itens": []},
            "ebooks": {"total": 0, "itens": []}}


def carregar_sumario_mae(slug):
    caminho = DIR_OUTPUT / slug / "sumario_macro.json"
    if not caminho.exists():
        return None
    return json.loads(caminho.read_text(encoding="utf-8"))


def capitulos_lineares(sumario):
    """Achata partes/capitulos do sumario-mae em uma lista ordenada."""
    lista = []
    for parte in sumario.get("partes", []):
        for cap in parte.get("capitulos", []):
            lista.append({
                "parte": parte.get("parte"),
                "capitulo": cap.get("capitulo"),
                "titulo": cap.get("titulo", ""),
                "objetivo": cap.get("objetivo", ""),
            })
    return lista


def particionar(lista, n):
    """Divide a lista em n grupos contiguos o mais equilibrados possivel."""
    if n <= 0:
        return []
    tamanho = max(1, len(lista) // n)
    grupos, resto = [], list(lista)
    for i in range(n - 1):
        grupos.append(resto[:tamanho])
        resto = resto[tamanho:]
    grupos.append(resto)  # ultimo grupo leva o restante (inclui sobra da divisao)
    return [g for g in grupos if g] or [lista[:1]]


def titulo_recorte(capitulos):
    return " & ".join(c["titulo"] for c in capitulos[:2]) or "Recorte tematico"


def gerar_artigos(slug, qtd, min_refs):
    dir_mae = DIR_OUTPUT / slug
    slug_mae_simples = dir_mae.name
    sumario = carregar_sumario_mae(slug)
    if sumario is None:
        print(f"[ERRO] sumario_macro.json nao encontrado para {slug}")
        return 1

    capitulos = capitulos_lineares(sumario)
    if not capitulos:
        print(f"[ERRO] livro-mae {slug} nao tem capitulos no sumario")
        return 1

    grupos = particionar(capitulos, qtd)
    dir_artigos_topo = DIR_OUTPUT / "artigos"
    dir_artigos_topo.mkdir(parents=True, exist_ok=True)

    derivados = carregar_derivados(dir_mae)
    itens_artigos = []

    for i, grupo in enumerate(grupos, 1):
        titulo = f"{titulo_recorte(grupo)} — Um Recorte de {sumario.get('titulo_obra', slug_mae_simples)}"
        slug_artigo = f"{slug_mae_simples}--art-{i:02d}-{slugificar(titulo_recorte(grupo))}"
        dir_artigo = dir_artigos_topo / slug_artigo
        for sub in ("capitulos", "revisao"):
            (dir_artigo / sub).mkdir(parents=True, exist_ok=True)

        sumario_artigo = {
            "titulo_obra": titulo,
            "tipo_obra": "artigo",
            "slug_livro_mae": slug_mae_simples,
            "capitulos_fonte_livro_mae": [c["capitulo"] for c in grupo],
            "introducao": f"Recorte investigativo sobre: {', '.join(c['titulo'] for c in grupo)}.",
            "partes": [{
                "parte": "I",
                "titulo_parte": "Artigo",
                "capitulos": [
                    {"capitulo": str(j + 1), "titulo": nome,
                     "objetivo": f"Seção IMRaD '{nome}' do artigo",
                     "pilares_previstos": [g["titulo"] for g in grupo][:3] or ["tema principal"]}
                    for j, nome in enumerate(SECOES_ARTIGO_FIXAS)
                ],
            }],
            "conclusao": "Síntese do recorte investigativo.",
        }
        (dir_artigo / "sumario_macro.json").write_text(
            json.dumps(sumario_artigo, ensure_ascii=False, indent=2), encoding="utf-8")

        config_artigo = {
            "tema": titulo, "tipo_obra": "artigo",
            "livro_mae": slug_mae_simples,
            "min_referencias_por_capitulo": min_refs,
            "tamanho_obra": None, "gerar_artigos": False, "qtd_artigos": 0,
            "gerar_ebooks": False, "qtd_ebooks": 0,
        }
        (dir_artigo / "config_obra.json").write_text(
            json.dumps(config_artigo, ensure_ascii=False, indent=2), encoding="utf-8")

        itens_artigos.append({
            "indice": i,
            "titulo": titulo,
            "slug": slug_artigo,
            "diretorio": f"artigos/{slug_artigo}",
            "capitulos_fonte_livro_mae": [c["capitulo"] for c in grupo],
        })
        print(f"  [OK] {slug_artigo}: {titulo}")

    derivados["slug_livro_mae"] = slug_mae_simples
    derivados["artigos"] = {"total": len(itens_artigos), "itens": itens_artigos}
    (dir_mae / "derivados.json").write_text(
        json.dumps(derivados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[OK] {len(grupos)} artigo(s) planejado(s) em {dir_artigos_topo.relative_to(DIR_PROJETO)}")
    print("Cada artigo consulta o dossie do livro-mae via RAG:")
    print(f"  python scripts/indexar-dossie.py {slug} --buscar \"<termos>\" --topo 4")
    return 0


def gerar_ebooks(slug, qtd):
    """Fatiamento por Parte (ou agrupamento de capitulos) para N e-books (Fase D)."""
    dir_mae = DIR_OUTPUT / slug
    slug_mae_simples = dir_mae.name
    sumario = carregar_sumario_mae(slug)
    if sumario is None:
        print(f"[ERRO] sumario_macro.json nao encontrado para {slug}")
        return 1

    partes = sumario.get("partes", [])
    if not partes:
        print(f"[ERRO] livro-mae {slug} nao tem partes no sumario")
        return 1

    # Se qtd_ebooks == numero de partes, 1 ebook por parte; senao, particiona
    # a lista linear de capitulos como nos artigos.
    if qtd == len(partes):
        grupos = [{"titulo_parte": p.get("titulo_parte", ""), "capitulos": p.get("capitulos", [])}
                  for p in partes]
    else:
        lineares = capitulos_lineares(sumario)
        grupos = [{"titulo_parte": titulo_recorte(g), "capitulos": g}
                  for g in particionar(lineares, qtd)]

    dir_ebooks_topo = DIR_OUTPUT / "ebooks"
    dir_ebooks_topo.mkdir(parents=True, exist_ok=True)

    derivados = carregar_derivados(dir_mae)
    itens_ebooks = []

    for i, grupo in enumerate(grupos, 1):
        capitulos_fonte = [c["capitulo"] for c in grupo["capitulos"]]
        titulo = grupo["titulo_parte"] or f"E-book {i}"
        slug_ebook = f"{slug_mae_simples}--eb-{i:02d}-{slugificar(titulo)}"
        dir_ebook = dir_ebooks_topo / slug_ebook
        for sub in ("capitulos", "revisao"):
            (dir_ebook / sub).mkdir(parents=True, exist_ok=True)

        sumario_ebook = {
            "titulo_obra": titulo,
            "tipo_obra": "ebook",
            "slug_livro_mae": slug_mae_simples,
            "capitulos_fonte_livro_mae": capitulos_fonte,
        }
        (dir_ebook / "sumario_macro.json").write_text(
            json.dumps(sumario_ebook, ensure_ascii=False, indent=2), encoding="utf-8")

        config_ebook = {
            "tema": titulo, "tipo_obra": "ebook",
            "livro_mae": slug_mae_simples,
            "min_referencias_por_capitulo": 0,
            "tamanho_obra": None, "gerar_artigos": False, "qtd_artigos": 0,
            "gerar_ebooks": False, "qtd_ebooks": 0,
        }
        (dir_ebook / "config_obra.json").write_text(
            json.dumps(config_ebook, ensure_ascii=False, indent=2), encoding="utf-8")

        itens_ebooks.append({
            "indice": i, "titulo": titulo,
            "slug": slug_ebook,
            "diretorio": f"ebooks/{slug_ebook}",
            "capitulos_fonte_livro_mae": capitulos_fonte,
        })
        print(f"  [OK] {slug_ebook}: {titulo} (capitulos-fonte: {capitulos_fonte})")

    derivados["slug_livro_mae"] = slug_mae_simples
    derivados["ebooks"] = {"total": len(itens_ebooks), "itens": itens_ebooks}
    (dir_mae / "derivados.json").write_text(
        json.dumps(derivados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[OK] {len(grupos)} e-book(s) planejado(s) em {dir_ebooks_topo.relative_to(DIR_PROJETO)}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Fatia o livro-mae em N artigos ou N ebooks")
    ap.add_argument("slug")
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--artigos", action="store_true")
    grupo.add_argument("--ebooks", action="store_true")
    ap.add_argument("--qtd", type=int, default=None)
    args = ap.parse_args()

    config_path = DIR_OUTPUT / args.slug / "config_obra.json"
    config = {}
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))

    if args.artigos:
        qtd = args.qtd or config.get("qtd_artigos") or 3
        min_refs = config.get("min_referencias_por_capitulo", 5)
        return gerar_artigos(args.slug, qtd, min_refs)

    qtd = args.qtd or config.get("qtd_ebooks") or 3
    return gerar_ebooks(args.slug, qtd)


if __name__ == "__main__":
    sys.exit(main())
