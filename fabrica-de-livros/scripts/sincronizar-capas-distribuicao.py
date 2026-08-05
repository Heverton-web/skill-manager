#!/usr/bin/env python3
"""
Sincroniza as capas de e-book do padrão HTML/Playwright
(output/ebooks/<slug-mae>--eb-NN-.../imagens/capa.png) para a pasta de
distribuição do livro-mãe (output/livros/<slug-mae>/distribuicao/ebooks/capas/),
que é o material realmente entregue/consultado.

Sem essa sincronização, atualizar o gerador padrão não muda o que está em
distribuicao/ — os dois diretórios não têm nenhuma outra ligação no pipeline.

Fonte da verdade: derivados.json de cada livro-mãe (mesmo manifesto usado por
empacotar-distribuicao.py). Isso cobre e-books cujo slug NÃO segue o padrão
`--eb-NN-` (ex.: code-review-graph-guide). O scan por regex fica como fallback
para e-books que existam em output/ebooks mas ainda não estejam no manifesto.
"""
import json
import re
import sys
from pathlib import Path

from PIL import Image

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_EBOOKS = DIR_PROJETO / "output" / "ebooks"
DIR_LIVROS = DIR_PROJETO / "output" / "livros"

PADRAO_EB = re.compile(r"^(?P<mae>.+)--eb-(?P<indice>\d+)-")


def gerar_thumbnail(caminho_capa, largura=300):
    nome_thumb = caminho_capa.stem.replace("capa", "thumbnail") + caminho_capa.suffix
    destino = caminho_capa.with_name(nome_thumb)
    with Image.open(caminho_capa) as img:
        altura = round(img.height * (largura / img.width))
        thumb = img.resize((largura, altura), Image.LANCZOS)
        thumb.convert("RGB").save(destino, "PNG", optimize=True)
    return destino


def sincronizar_capa(eb_dir, slug_mae, indice, capa):
    """Copia uma capa para distribuicao/<mae>/ebooks/capas/capa_ebook_<i>.png."""
    dir_mae = DIR_LIVROS / slug_mae
    if not dir_mae.exists():
        print(f"[AVISO] livro-mãe {slug_mae} não encontrado em output/livros, pulando {eb_dir.name}")
        return False

    destino_dir = dir_mae / "distribuicao" / "ebooks" / "capas"
    destino_dir.mkdir(parents=True, exist_ok=True)
    destino = destino_dir / f"capa_ebook_{indice}.png"
    destino.write_bytes(capa.read_bytes())
    thumb = gerar_thumbnail(destino)

    print(f"[OK] {eb_dir.name} -> {destino.relative_to(DIR_PROJETO)} ({thumb.name})")
    return True


def main():
    sincronizados = 0
    processados = set()  # (slug_mae, indice) já sincronizados via derivados.json

    # 1) Fonte primária: derivados.json de cada livro-mãe
    for dir_mae in sorted(DIR_LIVROS.iterdir()):
        if not dir_mae.is_dir():
            continue
        caminho = dir_mae / "derivados.json"
        if not caminho.exists():
            continue
        try:
            derivados = json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for eb in derivados.get("ebooks", {}).get("itens", []):
            indice = eb.get("indice")
            diretorio = eb.get("diretorio")
            if not indice or not diretorio:
                continue
            eb_dir = DIR_EBOOKS / Path(diretorio).name
            origem = eb_dir / "imagens" / "capa.png"
            if not origem.exists():
                print(f"[AVISO] sem capa.png em {eb_dir.name}, pulando")
                continue
            if sincronizar_capa(eb_dir, dir_mae.name, indice, origem):
                processados.add((dir_mae.name, indice))
                sincronizados += 1

    # 2) Fallback: scan por regex em output/ebooks (e-books fora do manifesto)
    for eb_dir in sorted(d for d in DIR_EBOOKS.iterdir() if d.is_dir()):
        m = PADRAO_EB.match(eb_dir.name)
        if not m:
            continue
        slug_mae = m.group("mae")
        indice = int(m.group("indice"))
        if (slug_mae, indice) in processados:
            continue
        origem = eb_dir / "imagens" / "capa.png"
        if not origem.exists():
            print(f"[AVISO] sem capa.png em {eb_dir.name}, pulando")
            continue
        if sincronizar_capa(eb_dir, slug_mae, indice, origem):
            sincronizados += 1

    print(f"\n[SUCESSO] {sincronizados} capa(s) de e-book sincronizada(s) para distribuicao/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
