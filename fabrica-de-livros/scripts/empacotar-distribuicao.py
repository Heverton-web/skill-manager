#!/usr/bin/env python3
"""Empacota a obra final em uma pasta de distribuicao autocontida.

Copia o PDF do livro, os PDFs dos artigos derivados, os EPUBs (com capas) e
gera README.md e LICENSE ("Todos os direitos reservados"). Deterministico e
reexecutavel: falha com exit 1 se qualquer artefato obrigatorio estiver ausente.

Uso:
    python scripts/empacotar-distribuicao.py <slug-livro-mae>
"""

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

AUTOR = "Heverton Eduardo Peres"
ANO = date.today().year

LICENSE = f"""LICENCA — TODOS OS DIREITOS RESERVADOS
{ANO} Heverton Eduardo Peres

Todos os direitos reservados. Nenhuma parte desta obra (incluindo, sem
limitacao, o texto integral, os capitulos, as ilustracoes, as capas graficas,
os diagramas e os arquivos PDF/EPUB) pode ser reproduzida, armazenada em
sistema de recuperacao ou transmitida, sob qualquer forma ou por qualquer meio
— eletronico, mecanico, fotocopia, gravacao ou outro — sem a autorizacao
previa, por escrito, do autor.

A distribuicao deste pacote (pasta de distribuicao) em sua forma integral e
permitida para fins de avaliacao e uso pessoal. Qualquer uso comercial,
publicacao, revenda ou republicacao parcial ou integral exige contrato de
licenciamento firmado com o autor.

Para licenciamento e permissoes, contate o autor.
"""


def carregar_manifesto_ebooks(slug):
    caminho = DIR_OUTPUT / slug / "ebooks" / "estrutura_ebooks.json"
    if not caminho.exists():
        return None
    return json.loads(caminho.read_text(encoding="utf-8"))


def carregar_manifesto_artigos(slug):
    caminho = DIR_OUTPUT / slug / "artigos" / "estrutura_artigos.json"
    if not caminho.exists():
        return None
    return json.loads(caminho.read_text(encoding="utf-8"))


def montar_readme(slug, tema, tamanho, pdf_bytes, ebooks, artigos):
    linhas = []
    linhas.append(f"# {tema}")
    linhas.append("")
    linhas.append(f"**Autor:** {AUTOR}  ·  **Tamanho da obra:** {tamanho}  ·  "
                  f"**Licença:** Todos os direitos reservados")
    linhas.append("")
    linhas.append("## Conteúdo do pacote")
    linhas.append("")
    linhas.append("| Arquivo | Descrição |")
    linhas.append("|---|---|")
    linhas.append(f"| `livro_final.pdf` | Obra completa em PDF (ABNT, {pdf_bytes} KB) |")
    for a in artigos:
        i = a["indice"]
        nome = a["titulo"]
        if len(nome) > 72:
            nome = nome[:69].rstrip() + "…"
        linhas.append(f"| `artigos/artigo_{i}.pdf` | Artigo {i}: {nome} |")
    for e in ebooks:
        i = e["indice"]
        nome = e["titulo"]
        linhas.append(f"| `ebooks/ebook_{i}.epub` | E-book {i}: {nome} |")
    linhas.append("")
    linhas.append("## Sobre a obra")
    linhas.append("")
    linhas.append("Esta obra explora o **AI Driven Development (AIDD)** a partir do "
                  "modelo das 4 camadas — **Tela, Harness, LLM e Tools** — que sustentam "
                  "o loop plan-act-observe dos agentes de software. O livro principal "
                  "percorre fundamentos, prática das camadas, mundo real (multiagentes, "
                  "segurança) e o profissional do futuro (métricas, liderança).")
    linhas.append("")
    linhas.append("## Como usar")
    linhas.append("")
    linhas.append("- **PDF**: abra `livro_final.pdf` em qualquer leitor (impressão, "
                  "anotação e distribuição).")
    linhas.append("- **Artigos**: cada `artigos/artigo_*.pdf` é um recorte autônomo da obra "
                  "(2 capítulos do livro-mãe, formato ABNT) — ideal para leitura focada.")
    linhas.append("- **EPUBs**: cada `ebooks/ebook_*.epub` é reflowable — compatível com "
                  "Kindle, Kobo, Apple Books, Google Play Livros e leitores EPUB em geral.")
    linhas.append("")
    linhas.append("## Licença")
    linhas.append("")
    linhas.append("© " + str(ANO) + " " + AUTOR + ". Todos os direitos reservados. "
                  "Consulte `LICENSE` para os termos completos.")
    linhas.append("")
    return "\n".join(linhas)


def empacotar(slug):
    dir_obra = DIR_OUTPUT / slug
    pdf_orig = dir_obra / "livro_final.pdf"
    if not pdf_orig.exists():
        print(f"[ERRO] livro_final.pdf nao encontrado em {dir_obra}")
        return 1

    manifesto = carregar_manifesto_ebooks(slug)
    if manifesto is None or not manifesto.get("ebooks"):
        print(f"[ERRO] ebooks/estrutura_ebooks.json ausente ou vazio para {slug}")
        return 1

    manifesto_artigos = carregar_manifesto_artigos(slug)
    artigos = (manifesto_artigos or {}).get("artigos", [])

    config = {}
    config_path = dir_obra / "esboco" / "config_obra.json"
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))

    dest = dir_obra / "distribuicao"
    dest_ebooks = dest / "ebooks"
    dest_capas = dest_ebooks / "capas"
    dest_artigos = dest / "artigos"

    # Limpa destino para empacotamento idempotente (ANTES de criar subdirs)
    if dest.exists():
        shutil.rmtree(dest)
    for d in (dest, dest_ebooks, dest_capas, dest_artigos):
        d.mkdir(parents=True, exist_ok=True)

    # 1. PDF principal
    shutil.copy2(pdf_orig, dest / "livro_final.pdf")
    print(f"  [OK] livro_final.pdf ({pdf_orig.stat().st_size // 1024} KB)")

    # 1.5. Artigos derivados
    falhas = []
    artigos_copiados = []
    for a in artigos:
        i = a["indice"]
        dir_art = dir_obra / "artigos" / f"artigo_{i}"
        pdf_art = dir_art / f"artigo_{i}.pdf"
        if pdf_art.exists():
            shutil.copy2(pdf_art, dest_artigos / f"artigo_{i}.pdf")
            artigos_copiados.append(a)
            print(f"  [OK] artigos/artigo_{i}.pdf ({pdf_art.stat().st_size // 1024} KB)")
        else:
            falhas.append(f"artigos/artigo_{i}/artigo_{i}.pdf")
            print(f"  [AVISO] artigos/artigo_{i}.pdf ausente — pacote incompleto!")

    # 2. EPUBs + capas
    ebooks_copiados = []
    for e in manifesto["ebooks"]:
        i = e["indice"]
        dir_eb = dir_obra / "ebooks" / f"ebook_{i}"
        epub = dir_eb / f"ebook_{i}.epub"
        if epub.exists():
            shutil.copy2(epub, dest_ebooks / f"ebook_{i}.epub")
            ebooks_copiados.append(e)
            print(f"  [OK] ebooks/ebook_{i}.epub ({epub.stat().st_size // 1024} KB)")
        else:
            falhas.append(f"ebooks/ebook_{i}.epub")
            print(f"  [AVISO] ebooks/ebook_{i}.epub ausente — pacote incompleto!")
        capa = dir_eb / "imagens" / "capa.png"
        if capa.exists():
            shutil.copy2(capa, dest_capas / f"capa_ebook_{i}.png")
            print(f"  [OK] ebooks/capas/capa_ebook_{i}.png")
        else:
            falhas.append(f"ebooks/ebook_{i}/imagens/capa.png")
            print(f"  [AVISO] capa do ebook_{i} ausente — pacote incompleto!")

    # 3. README + LICENSE (lista apenas arquivos efetivamente copiados)
    tema = config.get("tema") or manifesto.get("slug_livro_mae", slug)
    readme = montar_readme(slug, tema, config.get("tamanho_obra", "G"),
                           pdf_orig.stat().st_size // 1024, ebooks_copiados,
                           artigos_copiados)
    (dest / "README.md").write_text(readme, encoding="utf-8")
    (dest / "LICENSE").write_text(LICENSE, encoding="utf-8")
    print("  [OK] README.md")
    print("  [OK] LICENSE (todos os direitos reservados)")

    if falhas:
        print(f"\n[ERRO] Pacote INCOMPLETO — ausentes: {', '.join(falhas)}")
        return 1
    print(f"\nCONCLUIDO: pacote em {dest.relative_to(DIR_PROJETO)}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Empacota a obra em pasta de distribuicao")
    ap.add_argument("slug_livro_mae")
    args = ap.parse_args()
    return empacotar(args.slug_livro_mae)


if __name__ == "__main__":
    sys.exit(main())
