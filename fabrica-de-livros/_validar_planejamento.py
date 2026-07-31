#!/usr/bin/env python3
"""Validação final das 5 séries de planejamento (MK1-MK5): livros, capítulos e PDFs."""
from pathlib import Path
from collections import Counter

out = Path(__file__).parent / "output"
SERIES = ("MK1", "MK2", "MK3", "MK4", "MK5")

slugs = sorted(
    d.name for d in out.iterdir()
    if d.is_dir() and d.name[:3] in SERIES
)

print(f"Livros das 5 séries: {len(slugs)}")
print(f"Por série: {dict(Counter(s[:3] for s in slugs))}")

sem_16 = []
sem_pdf = []
sem_md = []
total_caps = 0
total_kb = 0

for s in slugs:
    dir_livro = out / s
    caps = list((dir_livro / "capitulos").glob("cap_*.md"))
    total_caps += len(caps)
    if len(caps) != 16:
        sem_16.append((s, len(caps)))
    md = dir_livro / "livro_final.md"
    if not md.exists():
        sem_md.append(s)
    else:
        total_kb += md.stat().st_size / 1024
    pdf = dir_livro / f"{s}.pdf"
    if not pdf.exists():
        sem_pdf.append(s)

print(f"Total de capítulos: {total_caps}")
print(f"Livros sem 16 capítulos: {sem_16 or 'NENHUM'}")
print(f"Livros sem livro_final.md: {sem_md or 'NENHUM'}")
print(f"Livros sem PDF: {sem_pdf or 'NENHUM'}")
print(f"Soma dos Markdowns: {total_kb/1024:.1f} MB")
