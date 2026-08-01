#!/usr/bin/env python3
"""
Fase B (V4) — Validador de elementos pre-textuais do TCC (NBR 14724/6027/6028).

Diferente de auditar-obra.py (que audita por secao/capitulo), este script audita o
que so existe no DOCUMENTO INTEIRO. Importante: folha de aprovacao e sumario sao
gerados INCONDICIONALMENTE pelo `templates/template_tcc.typ` (nao ficam escritos no
`livro_final.md` — sao renderizados a partir de `-V` do Pandoc), entao a evidencia
verificavel por script e:
  1. `output/<slug>/tcc_metadados.json` tem resumo/palavras-chave/abstract/keywords
     preenchidos (conteudo que o `compilador-tcc` pode esquecer de gerar);
  2. `output/<slug>/livro_final.md` tem numeracao progressiva sem saltos (NBR 6024),
     que e escrita pelo redator-academico no corpo do texto;
  3. o PDF final foi de fato gerado usando `template_tcc.typ` (ou seja,
     `tcc_metadados.json` existe — sem ele, `compilar-para-pdf.py` cai no template
     de livro comercial).

Uso:
    python scripts/validar-abnt-tcc.py <slug>
    python scripts/validar-abnt-tcc.py <slug> --estrito
    python scripts/validar-abnt-tcc.py <slug> --json

Relatorio: output/<slug>/revisao/relatorio_abnt_tcc.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"


def checar_numeracao_sem_saltos(texto):
    """Verifica se os cabecalhos de nivel 1 numerados sao uma sequencia 1,2,3,...
    sem saltos nem repeticao (NBR 6024)."""
    nivel1 = [m.group(1) for m in re.finditer(r"^#\s*(\d+)\.?\s+\S", texto, re.MULTILINE)]
    nivel1_int = [int(n) for n in nivel1]
    esperado = list(range(1, len(nivel1_int) + 1))
    return nivel1_int == esperado, nivel1_int


def validar(slug):
    dir_livro = DIR_OUTPUT / slug
    livro_final = dir_livro / "livro_final.md"
    if not livro_final.exists():
        return None, f"livro_final.md nao encontrado em {dir_livro}"

    texto = livro_final.read_text(encoding="utf-8", errors="replace")
    numeracao_ok, sequencia = checar_numeracao_sem_saltos(texto)

    meta_path = dir_livro / "tcc_metadados.json"
    meta = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except ValueError:
            meta = {}

    def preenchido(chave):
        return bool((meta.get(chave) or "").strip())

    pdf_gerado = (dir_livro / "livro_final.pdf").exists()

    requisitos = [
        {"id": "TCC-PRE-METADADOS", "nome": "tcc_metadados.json existe (aciona template_tcc.typ)",
         "conforme": meta_path.exists(),
         "detalhe": "arquivo " + ("encontrado" if meta_path.exists() else "AUSENTE — compilar-para-pdf.py usaria o template comercial de livro")},
        {"id": "TCC-PRE-RESUMO", "nome": "Resumo em português presente (NBR 6028)",
         "conforme": preenchido("resumo"), "detalhe": "campo 'resumo' " + ("preenchido" if preenchido("resumo") else "AUSENTE/VAZIO")},
        {"id": "TCC-PRE-PALAVRAS", "nome": "Palavras-chave presentes",
         "conforme": preenchido("palavras_chave"), "detalhe": "campo 'palavras_chave' " + ("preenchido" if preenchido("palavras_chave") else "AUSENTE/VAZIO")},
        {"id": "TCC-PRE-ABSTRACT", "nome": "Abstract em inglês presente",
         "conforme": preenchido("abstract_en"), "detalhe": "campo 'abstract_en' " + ("preenchido" if preenchido("abstract_en") else "AUSENTE/VAZIO")},
        {"id": "TCC-PRE-KEYWORDS", "nome": "Keywords presentes",
         "conforme": preenchido("keywords_en"), "detalhe": "campo 'keywords_en' " + ("preenchido" if preenchido("keywords_en") else "AUSENTE/VAZIO")},
        {"id": "TCC-PRE-PDF", "nome": "PDF final gerado (folha de aprovação/sumário são estruturais do template)",
         "conforme": pdf_gerado, "detalhe": "livro_final.pdf " + ("encontrado" if pdf_gerado else "AUSENTE")},
        {"id": "TCC-NUM-GLOBAL", "nome": "Numeração progressiva sem saltos (NBR 6024)",
         "conforme": numeracao_ok,
         "detalhe": f"sequência de seções nível 1: {sequencia}" if sequencia else "nenhuma secao numerada encontrada"},
    ]

    nao_conformes = [r for r in requisitos if not r["conforme"]]
    veredito = "CONFORME" if not nao_conformes else "NAO CONFORME"

    relatorio = {
        "slug": slug,
        "veredito": veredito,
        "requisitos": requisitos,
    }
    return relatorio, None


def main():
    ap = argparse.ArgumentParser(description="Valida elementos pre-textuais do TCC (NBR 14724)")
    ap.add_argument("slug")
    ap.add_argument("--estrito", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    relatorio, erro = validar(args.slug)
    if erro:
        print(f"[ERRO] {erro}")
        return 1

    dir_rev = DIR_OUTPUT / args.slug / "revisao"
    dir_rev.mkdir(parents=True, exist_ok=True)
    destino = dir_rev / "relatorio_abnt_tcc.json"
    destino.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"VALIDACAO ABNT/TCC - {args.slug}")
    for r in relatorio["requisitos"]:
        marca = "OK  " if r["conforme"] else "FALHA"
        print(f"  [{marca}] {r['id']:<18} {r['nome']}")
        if not r["conforme"]:
            print(f"           -> {r['detalhe']}")
    print(f"\n  VEREDITO: {relatorio['veredito']}")
    print(f"  Relatorio: {destino.relative_to(DIR_PROJETO)}")

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    nao_conformes = [r for r in relatorio["requisitos"] if not r["conforme"]]
    if args.estrito and nao_conformes:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
