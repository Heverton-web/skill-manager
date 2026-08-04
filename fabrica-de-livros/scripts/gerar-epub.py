#!/usr/bin/env python3
"""
Fase D (V4) — Geracao de E-book em EPUB reflowable (padrao de mercado, sem ABNT).

Converte o `livro_final.md` de um ebook derivado (ja com tom adaptado pela skill
`redator-ebook` e o CTA final) diretamente para EPUB via Pandoc — sem passar por
Typst/PDF (o EPUB e reflowable por natureza, formato-nativo do Pandoc).

Degradacao graciosa: sem capa (`capa.png`/`capa.jpg` ausente), gera o EPUB sem
imagem de capa e reporta a pendencia — nunca bloqueia a entrega (mesmo principio
do renderizar-diagramas.py com o mmdc ausente).

Uso:
    python scripts/gerar-epub.py <slug-do-ebook>
    python scripts/gerar-epub.py <slug-livro-mae>/ebooks/ebook_2
    python scripts/gerar-epub.py <slug> --pdf-tambem   # gera PDF alem do EPUB
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

PANDOC = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc-3.10\pandoc.exe"


def achar_capa(dir_ebook):
    for nome in ("capa.png", "capa.jpg", "capa.jpeg"):
        p = dir_ebook / "imagens" / nome
        if p.exists():
            return p
        p = dir_ebook / nome
        if p.exists():
            return p
    return None


def gerar(slug, gerar_pdf_tambem=False):
    dir_ebook = DIR_OUTPUT / slug
    md_path = dir_ebook / "livro_final.md"
    if not md_path.exists():
        print(f"[ERRO] livro_final.md nao encontrado em {dir_ebook}")
        return 1

    meta_path = dir_ebook / "ebook_metadados.json"
    meta = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except ValueError:
            meta = {}

    sumario_path = dir_ebook / "sumario_macro.json"
    titulo = meta.get("titulo") or slug
    if sumario_path.exists():
        try:
            titulo = json.loads(sumario_path.read_text(encoding="utf-8")).get("titulo_obra", titulo)
        except ValueError:
            pass
    autor = meta.get("autor", "Heverton Eduardo Peres")

    nome_arquivo = Path(slug).name
    epub_path = dir_ebook / f"{nome_arquivo}.epub"
    capa = achar_capa(dir_ebook)

    comando = [
        PANDOC, str(md_path), "-o", str(epub_path),
        "--toc", "--toc-depth", "2",
        "--metadata", f"title={titulo}",
        "--metadata", f"author={autor}",
        "--metadata", "lang=pt-BR",
        "--resource-path", str(dir_ebook),
    ]
    if capa:
        comando += [f"--epub-cover-image={capa}"]

    resultado = subprocess.run(comando, capture_output=True, text=True, timeout=180)

    ok_epub = epub_path.exists() and epub_path.stat().st_size > 0
    if ok_epub:
        tamanho_kb = epub_path.stat().st_size / 1024
        print(f"[OK] EPUB gerado: {epub_path.name} ({tamanho_kb:.1f} KB)")
        if not capa:
            print("[AVISO] Sem capa (imagens/capa.png ausente) — R-EBK-2 pendente. "
                  "Gere uma capa 1:1,6 (ex.: 1600x2560px) e recompile.")
    else:
        erro = (resultado.stderr or resultado.stdout or "").strip()
        print(f"[FALHA] EPUB nao foi gerado")
        for linha in erro.split("\n")[-6:]:
            if linha.strip():
                print(f"  STDERR: {linha.strip()}")
        return 1

    if gerar_pdf_tambem:
        pdf_path = dir_ebook / f"{nome_arquivo}.pdf"
        # Usar Pandoc -> .typ -> Typst para PDF com template ABNT
        typ_path = dir_ebook / "_ebook_compilado.typ"
        template_typ = DIR_PROJETO / "templates" / "template.typ"
        
        # Gerar .typ
        typst_cmd = [
            PANDOC, str(md_path), "-o", str(typ_path),
            "--to=typst",
            f"--template={template_typ}",
            "--wrap=preserve",
            "--resource-path", str(dir_ebook),
            "-V", f"title={titulo}",
            "-V", f"author={autor}",
        ]
        
        # Incluir capa se existir
        capa_para_pdf = achar_capa(dir_ebook)
        if capa_para_pdf:
            # Copiar capa para imagens/capa_livro.png para o template encontrar
            capa_dest = dir_ebook / "imagens" / "capa_livro.png"
            capa_dest.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(capa_para_pdf, capa_dest)
            # Passar caminho relativo para o template
            typst_cmd += ["-V", "capa_imagem=imagens/capa_livro.png"]
        else:
            typst_cmd += ["-V", "sem_capa_grafica=1"]
        
        subprocess.run(typst_cmd, capture_output=True, text=True, timeout=180)
        
        # Compilar com Typst
        if typ_path.exists():
            typst_compile = ["typst", "compile", "--root", str(dir_ebook), str(typ_path), str(pdf_path)]
            resultado_typst = subprocess.run(typst_compile, capture_output=True, text=True, timeout=180)
            
            if pdf_path.exists() and pdf_path.stat().st_size > 0:
                tamanho_kb = pdf_path.stat().st_size / 1024
                print(f"[OK] PDF gerado: {pdf_path.name} ({tamanho_kb:.1f} KB)")
            else:
                # Fallback: PDF simples via Pandoc
                pdf_comando = [PANDOC, str(md_path), "-o", str(pdf_path),
                               "--toc", "--metadata", f"title={titulo}", 
                               "--metadata", f"author={autor}",
                               "--resource-path", str(dir_ebook)]
                subprocess.run(pdf_comando, capture_output=True, text=True, timeout=180)
                if pdf_path.exists():
                    print(f"[OK] PDF gerado (fallback): {pdf_path.name}")
            
            # Limpar .typ temporário
            typ_path.unlink(missing_ok=True)

    return 0


def main():
    ap = argparse.ArgumentParser(description="Gera EPUB de um ebook derivado do livro-mae")
    ap.add_argument("slug")
    ap.add_argument("--pdf-tambem", action="store_true",
                    help="tambem gera um PDF simples (sem template ABNT) alem do EPUB")
    args = ap.parse_args()
    return gerar(args.slug, args.pdf_tambem)


if __name__ == "__main__":
    sys.exit(main())
