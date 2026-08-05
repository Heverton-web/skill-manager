#!/usr/bin/env python3
"""
Fase A (V4) — Parametros compartilhados por tipo de obra.

Modulo importado por auditar-obra.py, arquiteto (via scripts), validar-abnt-tcc.py,
fatiar-obra.py e gerar-epub.py. Centraliza:
  - leitura de output/<slug>/config_obra.json (schema da Fase 0 / `/esbocar`; <slug>
    inclui o prefixo de tipo, ex. livros/<slug-livro>, tccs/<slug-tcc>)
  - tabela de tamanhos de livro (P/M/G) -> capitulos e caracteres minimos
  - padroes de citacao por tipo de obra (numerica [N] vs autor-data)
  - valores-padrao para obras V3 sem esboco/ (retrocompatibilidade)

Uso como biblioteca:
    from parametros_obra import carregar_config, TAMANHOS, RE_CITACAO_NUMERICA, \
        RE_CITACAO_AUTOR_DATA, citacao_regex, minimos_livro

Uso como CLI (inspecao rapida):
    python scripts/parametros_obra.py <slug>
    python scripts/parametros_obra.py <slug> --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

TIPOS_VALIDOS = ("livro", "tcc", "artigo", "ebook")

# Tabela de tamanhos de LIVRO (Fase 0, pergunta Q5). Caracteres ~2.500/pagina ABNT.
TAMANHOS = {
    "P": {"partes": 1, "capitulos": 4, "paginas": 40, "caracteres": 100_000},
    "M": {"partes": 3, "capitulos": 9, "paginas": 90, "caracteres": 180_000},
    "G": {"partes": 5, "capitulos": 10, "paginas": 150, "caracteres": 375_000},
    # Tier mega-obra: fora do fluxo padrao de /esbocar, criado sob demanda
    # explicita do operador quando G (maior preset padrao) nao cobre o escopo.
    "GG": {"partes": 10, "capitulos": 50, "paginas": 1000, "caracteres": 2_500_000},
}
TAMANHO_PADRAO = "M"

# Retrocompatibilidade: obras V3 sem esboco/config_obra.json usam os minimos originais
MIN_CAPITULOS_V3 = 16
MIN_CARACTERES_V3 = 175_000
MIN_REFS_V3 = 3

DEFAULTS_POR_TIPO = {
    "livro": {"min_refs": MIN_REFS_V3},
    "tcc": {"min_refs": 8},
    "artigo": {"min_refs": 5},
    "ebook": {"min_refs": 0},
}

# Citacao numerica (livro/ebook): [1], [23]...
RE_CITACAO_NUMERICA = re.compile(r"\[\d{1,3}\]")

# Citacao autor-data (TCC/artigo, NBR 10520): parenteses "(SOBRENOME, 2024)" ou
# "(SOBRENOME; SOBRENOME2, 2024)" ou narrativa "Sobrenome (2024)".
RE_CITACAO_AUTOR_DATA = re.compile(
    r"\([A-ZÀ-Ý][A-ZÀ-Ýa-zà-ÿ\'\-]+(?:\s*;\s*[A-ZÀ-Ý][A-ZÀ-Ýa-zà-ÿ\'\-]+)*,\s*\d{4}[a-z]?\)"
    r"|[A-ZÀ-Ý][A-Za-zà-ÿ\'\-]+\s*\(\d{4}[a-z]?\)"
)

# Entrada de referencia ABNT autor-data: linha comecando com SOBRENOME e contendo um ano
RE_REF_AUTOR_DATA = re.compile(
    r"^([A-ZÀ-Ý][A-ZÀ-Ýa-zà-ÿ\'\-]+(?:\s*;\s*[A-ZÀ-Ý][A-ZÀ-Ýa-zà-ÿ\'\-]+)*)"
    r".*?(\d{4})", re.MULTILINE
)

# Numeracao progressiva de secao (NBR 6024): "1", "1.1", "2.3.4"...
RE_NUMERACAO_PROGRESSIVA = re.compile(r"^#{1,6}\s*(\d+(?:\.\d+)*)\.?\s+\S", re.MULTILINE)


def usa_citacao_autor_data(tipo_obra):
    return tipo_obra in ("tcc", "artigo")


def citacao_regex(tipo_obra):
    return RE_CITACAO_AUTOR_DATA if usa_citacao_autor_data(tipo_obra) else RE_CITACAO_NUMERICA


def minimos_livro(tamanho):
    return TAMANHOS.get((tamanho or TAMANHO_PADRAO).upper(), TAMANHOS[TAMANHO_PADRAO])


def caminho_config(slug):
    return DIR_OUTPUT / slug / "config_obra.json"


def carregar_config(slug):
    """Le config_obra.json; devolve defaults retrocompativeis se nao existir (obra V3)."""
    caminho = caminho_config(slug)
    if not caminho.exists():
        return {
            "tema": slug,
            "tipo_obra": "livro",
            "min_referencias_por_capitulo": MIN_REFS_V3,
            "tamanho_obra": None,
            "gerar_artigos": False,
            "qtd_artigos": 0,
            "gerar_ebooks": False,
            "qtd_ebooks": 0,
            "_origem": "default_v3_sem_esboco",
        }
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados.setdefault("tipo_obra", "livro")
    dados.setdefault("min_referencias_por_capitulo",
                     DEFAULTS_POR_TIPO.get(dados["tipo_obra"], {}).get("min_refs", MIN_REFS_V3))
    dados.setdefault("tamanho_obra", TAMANHO_PADRAO if dados["tipo_obra"] == "livro" else None)
    dados.setdefault("gerar_artigos", False)
    dados.setdefault("qtd_artigos", 0)
    dados.setdefault("gerar_ebooks", False)
    dados.setdefault("qtd_ebooks", 0)
    dados["_origem"] = "esboco"
    return dados


def gravar_config(slug, config):
    caminho = caminho_config(slug)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    limpo = {k: v for k, v in config.items() if not k.startswith("_")}
    caminho.write_text(json.dumps(limpo, ensure_ascii=False, indent=2), encoding="utf-8")
    return caminho


def validar_config(config):
    """Valida config_obra.json contra as faixas da Fase 0. Retorna lista de erros (vazia = ok)."""
    erros = []
    tipo = config.get("tipo_obra")
    if tipo not in TIPOS_VALIDOS[:2]:  # Fase 0 so pergunta livro|tcc; artigo/ebook sao derivados
        erros.append(f"tipo_obra deve ser 'livro' ou 'tcc', recebido: {tipo!r}")
    refs = config.get("min_referencias_por_capitulo")
    if not isinstance(refs, int) or not (5 <= refs <= 20):
        erros.append(f"min_referencias_por_capitulo deve estar entre 5 e 20, recebido: {refs!r}")
    if tipo == "livro":
        tam = config.get("tamanho_obra")
        if tam not in TAMANHOS:
            erros.append(f"tamanho_obra deve ser P, M, G ou GG quando tipo_obra=livro, recebido: {tam!r}")
    if config.get("gerar_artigos"):
        qtd = config.get("qtd_artigos")
        if not isinstance(qtd, int) or not (1 <= qtd <= 5):
            erros.append(f"qtd_artigos deve estar entre 1 e 5, recebido: {qtd!r}")
    if config.get("gerar_ebooks"):
        qtd = config.get("qtd_ebooks")
        if not isinstance(qtd, int) or not (1 <= qtd <= 10):
            erros.append(f"qtd_ebooks deve estar entre 1 e 10, recebido: {qtd!r}")
    return erros


def main():
    ap = argparse.ArgumentParser(description="Parametros de obra por tipo (Fase 0 / V4)")
    ap.add_argument("slug")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--validar", action="store_true", help="valida config_obra.json e retorna exit 1 se invalido")
    args = ap.parse_args()

    config = carregar_config(args.slug)

    if args.validar:
        erros = validar_config(config)
        if erros:
            for e in erros:
                print(f"[ERRO] {e}")
            return 1
        print("[OK] config_obra.json valido")
        return 0

    if args.json:
        print(json.dumps(config, ensure_ascii=False, indent=2))
        return 0

    for k, v in config.items():
        print(f"{k:<32}: {v}")
    if config["tipo_obra"] == "livro":
        m = minimos_livro(config.get("tamanho_obra"))
        print(f"\nMinimos derivados (tamanho {config.get('tamanho_obra')}): "
              f"{m['capitulos']} capitulos, {m['partes']} partes, "
              f"{m['caracteres']:,} caracteres".replace(",", "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
