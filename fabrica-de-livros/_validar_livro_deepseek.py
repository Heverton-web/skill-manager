#!/usr/bin/env python3
"""Valida conformidade R1-R10 do livro segredos-deepseek (fluxo /criar-livro)."""
import re
import sys
from pathlib import Path

SLUG = "segredos-deepseek"
DIR = Path(__file__).parent / "output" / SLUG
DIR_CAPS = DIR / "capitulos"

erros = []

# R1: 16+ capítulos
caps = sorted(DIR_CAPS.glob("cap_*.md"), key=lambda p: int(re.search(r'cap_(\d+)', p.stem).group(1)))
print(f"[R1] Capítulos: {len(caps)} {'OK' if len(caps) >= 16 else 'FALHA'}")
if len(caps) < 16:
    erros.append("R1")

# R3: 7 seções EITA por capítulo + R9: 3+ citações [N] + R4: 3+ referências
total_caracteres = 0
for cap in caps:
    texto = cap.read_text(encoding="utf-8")
    total_caracteres += len(texto)
    secoes = re.findall(r'^## [1-7]\. ', texto, re.MULTILINE)
    if len(secoes) < 7:
        print(f"[R3] {cap.name}: {len(secoes)}/7 seções FALHA")
        erros.append("R3")
    citacoes = len(re.findall(r'\[\d+\]', texto))
    if citacoes < 3:
        print(f"[R9] {cap.name}: {citacoes} citações FALHA")
        erros.append("R9")
    refs = len(re.findall(r'^\[\d+\]', texto, re.MULTILINE))
    if refs < 3:
        print(f"[R4] {cap.name}: {refs} refs FALHA")
        erros.append("R4")

# R2: livro_final.md com caracteres
md_path = DIR / "livro_final.md"
if md_path.exists():
    chars = len(md_path.read_text(encoding="utf-8"))
    print(f"[R2] livro_final.md: {chars:,} caracteres {'OK' if chars >= 35000 else 'FALHA'}")
    if chars < 35000:
        erros.append("R2")
else:
    print("[R2] livro_final.md ausente FALHA")
    erros.append("R2")

# R7: PDF
pdf = DIR / "livro_final.pdf"
if pdf.exists() and pdf.stat().st_size > 0:
    print(f"[R7] PDF: {pdf.stat().st_size/1024/1024:.1f} MB OK")
else:
    print("[R7] PDF ausente FALHA")
    erros.append("R7")

# R5: dossiê com 3+ papers
dossie = DIR / "pesquisa" / "dossie_segredos-deepseek.md"
if dossie.exists():
    n_papers = dossie.read_text(encoding="utf-8").count("arXiv:")
    print(f"[R5] Papers no dossiê: {n_papers} {'OK' if n_papers >= 3 else 'FALHA'}")
    if n_papers < 3:
        erros.append("R5")
else:
    print("[R5] Dossiê ausente FALHA")
    erros.append("R5")

print(f"\nTotal capítulos: {len(caps)} | Total caracteres: {total_caracteres:,}")
print(f"STATUS: {'CONFORME' if not erros else 'NAO CONFORME: ' + ', '.join(erros)}")
sys.exit(1 if erros else 0)
