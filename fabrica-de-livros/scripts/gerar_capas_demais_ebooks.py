#!/usr/bin/env python3
"""
Gera capas no padrão EXATO do code-review-graph (HTML + CSS + Playwright)
para TODOS os e-books em output/ebooks (EXCETO a série code-review-graph).
"""

import json
import sys
from pathlib import Path
from PIL import Image

DIR_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_PROJETO / "scripts"))

import importlib
gerar_padrao = importlib.import_module("gerar-capa-ebook-padrao")
gerar_capa_ebook = gerar_padrao.gerar_capa_ebook


def gerar_thumbnail(caminho_capa, largura=300):
    nome_thumb = caminho_capa.stem.replace("capa", "thumbnail") + caminho_capa.suffix
    destino = caminho_capa.with_name(nome_thumb)
    with Image.open(caminho_capa) as img:
        altura = round(img.height * (largura / img.width))
        thumb = img.resize((largura, altura), Image.LANCZOS)
        thumb.convert("RGB").save(destino, "PNG", optimize=True)
    return destino


CONFIGS_SERIE = {
    "ai-driven-development": {"cor": "#2ecc9a"},
    "marketing-na-era-digital": {"cor": "#f0933b"},
    "sdlc-ai-first": {"cor": "#37c3d6"},
}

DEFAULT_CFG = {"cor": "#b06df0"}
EDICAO_PADRAO = "1ª Edição · 2026"


def main():
    dir_ebooks = DIR_PROJETO / "output" / "ebooks"
    ebook_dirs = sorted([d for d in dir_ebooks.iterdir() if d.is_dir()])

    # code-review-graph tem cor/titulo/subtitulo por ebook (nao um unico accent de
    # serie) e foi atualizado a parte — nao reprocessar aqui por cima.
    ebooks_alvo = [d for d in ebook_dirs if not d.name.startswith("code-review-graph")]

    print(f"Gerando capas no modelo PADRÃO (HTML/Playwright) para {len(ebooks_alvo)} e-books...")

    for idx, eb_dir in enumerate(ebooks_alvo, 1):
        meta_path = eb_dir / "ebook_metadados.json"
        sum_path = eb_dir / "sumario_macro.json"
        meta = {}
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        elif sum_path.exists():
            try:
                meta = json.loads(sum_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        titulo = meta.get("titulo") or meta.get("titulo_obra") or eb_dir.name.split("--")[-1].replace("-", " ").title()
        subtitulo = meta.get("subtitulo") or ""

        cfg = DEFAULT_CFG
        for prefix, config in CONFIGS_SERIE.items():
            if eb_dir.name.startswith(prefix):
                cfg = config
                break

        png_capa = gerar_capa_ebook(
            titulo=titulo.upper(),
            subtitulo=subtitulo,
            cor_acento=cfg["cor"],
            edicao=meta.get("edicao") or EDICAO_PADRAO,
            dir_saida=eb_dir,
        )
        thumb = gerar_thumbnail(png_capa)
        print(f"[{idx}/{len(ebooks_alvo)}] [OK] {eb_dir.name} -> {png_capa.name} ({thumb.name})")

    print("\n[SUCESSO] Capas atualizadas no modelo padrão HTML/Playwright!")


if __name__ == "__main__":
    main()
