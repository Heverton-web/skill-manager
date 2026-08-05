"""Verifica rastreabilidade [N] entre corpo e secao 7 dos capitulos."""
import re
import sys
from pathlib import Path

BASE = Path("output") / "livros" / "a-pilha-agentica-livro-1-antes-do-prompt" / "capitulos"
RE_CIT = re.compile(r"\[(\d{1,3})\]")
RE_COD = re.compile(r"^[ \t]*```.*?^[ \t]*```[ \t]*$", re.DOTALL | re.MULTILINE)

args = sys.argv[1:] or ["1", "2"]
for n in args:
    p = BASE / f"cap_{int(n):02d}.md"
    if not p.exists():
        print(f"cap {n}: AUSENTE")
        continue
    t = p.read_text(encoding="utf-8")
    corpo, sep, refs = t.partition("## 7.")
    corpo = RE_COD.sub("", corpo)
    cit = {int(c) for c in RE_CIT.findall(corpo)}
    entradas = {int(c) for c in RE_CIT.findall(refs.split("\n")[0] + "\n" + refs) if refs}
    # entradas na secao 7: linhas que comecam com [N]
    entradas = set()
    for linha in refs.splitlines():
        m = re.match(r"^\s*\[(\d{1,3})\]", linha)
        if m:
            entradas.add(int(m.group(1)))
    orfas = sorted(cit - entradas)
    nao_citadas = sorted(entradas - cit)
    ordem = list(entradas)
    print(f"cap {n}: citacoes_no_corpo={len(cit)} entradas_secao7={len(entradas)} "
          f"orfas={orfas} nao_citadas={nao_citadas} ordem_ok={ordem == sorted(ordem)}")
