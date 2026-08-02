#!/usr/bin/env python3
"""Formata a secao de Referencias Bibliograficas (ABNT) com 1 entrada por linha.

Problema que resolve: no Markdown, linhas consecutivas SEM linha em branco sao
fundidas em UM paragrafo pelo Pandoc/Typst. Assim, as N referencias de um
capitulo (cada uma em sua propria linha na fonte) viravam um bloco continuo no
PDF — violando a NBR 6023 (apresentacao em entradas separadas).

Correcao: insere uma linha em branco entre cada entrada da secao
"Referencias" (numerada "[N]" no livro, autor-data nos artigos), preservando o
restante do arquivo. Idempotente e deterministico.

Uso:
    python scripts/formatar-referencias.py <slug-livro-mae>
    python scripts/formatar-referencias.py <slug-livro-mae> --tambem-artigos
    python scripts/formatar-referencias.py <slug-livro-mae> --tambem-livro-final
    (sem flags, formata apenas output/<slug>/capitulos/cap_*.md)
"""

import argparse
import re
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

RE_SECAO_REFS = re.compile(
    r"(?m)^#{1,3}\s*(?:\d+[\.\)]?\s*)?Refer[êe]ncias(?:\s+Bibliogr[áa]ficas)?\s*$\n")

# Entrada de referencia: linha que NAO comeca com heading, bloco de codigo,
# lista, citacao em bloco nem e vazia — e termina com pontuacao de fechamento.
RE_LINHA_REFERENCIA = re.compile(
    r"^(?!(?:#{1,6}\s|```|[-*+]\s|>\s|\d+\.\s|$))"
    r".*[\.,:\)\]\`\*\?\!]$")


def reformatar_secao(corpo):
    """Devolve o corpo da secao com uma linha em branco entre cada entrada."""
    if not corpo.strip():
        return corpo
    linhas = corpo.split("\n")
    saida = []
    prev_era_referencia = False
    for linha in linhas:
        if not linha.strip():
            saida.append("")
            prev_era_referencia = False
            continue
        eh_referencia = bool(RE_LINHA_REFERENCIA.match(linha))
        if eh_referencia and prev_era_referencia:
            saida.append("")
        saida.append(linha)
        prev_era_referencia = eh_referencia
    return "\n".join(saida).rstrip("\n") + "\n"


def formatar_arquivo(caminho, modificar=True):
    texto = caminho.read_text(encoding="utf-8")
    ocorrencias = list(RE_SECAO_REFS.finditer(texto))
    if not ocorrencias:
        return 0, False

    alterado = False
    # Processa de tras para frente para nao invalidar offsets
    for m in reversed(ocorrencias):
        fim_heading = m.end()
        # Corpo da secao: ate o proximo heading (ou fim do arquivo)
        resto = texto[fim_heading:]
        prox = re.search(r"(?m)^#{1,3}\s", resto)
        fim_sec = fim_heading + (prox.start() if prox else len(resto))

        corpo = texto[fim_heading:fim_sec]
        novo_corpo = reformatar_secao(corpo)
        if novo_corpo != corpo:
            texto = texto[:fim_heading] + novo_corpo + texto[fim_sec:]
            alterado = True

    if alterado and modificar:
        caminho.write_text(texto, encoding="utf-8")
    return len(ocorrencias), alterado


def main():
    ap = argparse.ArgumentParser(description="Formata referencias ABNT com 1 entrada por linha")
    ap.add_argument("slug")
    ap.add_argument("--tambem-artigos", action="store_true",
                    help="formata tambem artigos/artigo_*/capitulos/*.md")
    ap.add_argument("--tambem-livro-final", action="store_true",
                    help="formata tambem livro_final.md (compilado)")
    args = ap.parse_args()

    dir_obra = DIR_OUTPUT / args.slug
    alvos = sorted((dir_obra / "capitulos").glob("cap_*.md"))

    if args.tambem_artigos:
        for dir_artigo in sorted((dir_obra / "artigos").glob("artigo_*")):
            alvos += sorted((dir_artigo / "capitulos").glob("cap_*.md"))

    if args.tambem_livro_final:
        alvo_lf = dir_obra / "livro_final.md"
        if alvo_lf.exists():
            alvos.append(alvo_lf)
        else:
            print(f"  [AVISO] livro_final.md nao existe em {dir_obra} — "
                  f"o compilador usa o caminho legado (_livro_compilado.md)")

    total_sec = total_alt = 0
    for caminho in alvos:
        n, alt = formatar_arquivo(caminho)
        total_sec += n
        total_alt += 1 if alt else 0
        if n:
            estado = "alterado" if alt else "ok (ja formatado)"
            print(f"  [OK] {caminho.relative_to(DIR_OUTPUT)}: {n} secao(es) — {estado}")

    print(f"\nCONCLUIDO: {len(alvos)} arquivo(s), {total_sec} secao(es) de referencias, "
          f"{total_alt} arquivo(s) modificado(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
