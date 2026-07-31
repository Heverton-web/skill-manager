#!/usr/bin/env python3
"""
Gera o CATÁLOGO GERAL das obras da Fábrica Agêntica de Livros em Markdown.

Lê os sumario_macro.json de todos os livros em output/ e monta um catálogo
organizado por série (Perfumaria, Web Fullstack, IA e Agentes, Stack Fullstack,
AIDD), com os caminhos dos PDFs de cada obra.

Uso: python gerar-catalogo.py
"""

import json
import re
from pathlib import Path
from datetime import date

DIR_RAIZ = Path(__file__).parent / "output"
SAIDA = Path(__file__).parent / "CATALOGO_LIVROS.md"

EXCLUIR_PREFIXOS = ("mega-", "compilado-", "07-mega-", "00-mega-")
EXCLUIR_SLUGS = {"mega-livro-todos-aidd"}

# Ordem das séries no catálogo: (prefixo, nome da série, descrição)
SERIES_ORDEM = [
    ("P",  "Perfumaria e Fragrâncias", "Fundamentos da perfumaria, universo árabe e oriental, sazonalidade, aplicação e cuidado, psicologia dos aromas."),
    ("W",  "Desenvolvimento Web Fullstack", "Fundamentos da web, frontend moderno, backend, bancos de dados, DevOps e carreira fullstack."),
    ("IA", "IA e Agentes Fullstack", "Arquitetura de agentes, ecossistema LLM, engenharia guiada por agentes, automação com IA e projetos práticos."),
    ("FE", "Stack Fullstack — Frontend", "HTML5, CSS moderno, JavaScript, TypeScript, React, Next.js, estado, formulários, testes e performance."),
    ("BE", "Stack Fullstack — Backend", "Node.js, Express/Fastify, Clean Architecture, SOLID, WebSockets, filas, segurança e microsserviços."),
    ("BD", "Stack Fullstack — Banco de Dados", "SQL, índices, ORMs, NoSQL, Redis, full-text search, migrações, segurança, backup e vetores."),
    ("AP", "Stack Fullstack — APIs", "REST, OpenAPI, GraphQL, webhooks, rate limiting, resiliência, testes de contrato, SSE, gateways e monetização."),
    ("DV", "Stack Fullstack — DevOps", "Docker, Compose, Linux, CI/CD, VPS, proxy reverso, PM2, observabilidade, IaC e deploy."),
]


def coletar_sumario(slug):
    path = DIR_RAIZ / slug / "sumario_macro.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def descobrir_livros():
    livros = []
    for d in sorted(DIR_RAIZ.iterdir()):
        if not d.is_dir():
            continue
        nome = d.name
        if nome in EXCLUIR_SLUGS or nome.startswith(EXCLUIR_PREFIXOS):
            continue
        if not (d / "sumario_macro.json").exists():
            continue
        livros.append(nome)
    return livros


def classificar(slug):
    """Classifica um slug em uma das séries do catálogo.

    Formatos reais de slug:
      - Perfumaria:  P1-01-..., P2-..., P3-..., P4-..., P5-...  -> grupo P
      - Web:         W1-..., W2-..., W3-..., W4-..., W5-...     -> grupo W
      - IA:          IA1-..., IA2-..., IA3-..., IA4-..., IA5-... -> grupo IA
      - Stack:       FE-..., BE-..., BD-..., AP-..., DV-...      -> grupo FE/BE/BD/AP/DV
    """
    for prefixo, _, _ in SERIES_ORDEM:
        if re.match(rf"^{re.escape(prefixo)}\d*-", slug):
            return prefixo
    # AIDD
    if slug == "ai-driven-development":
        return "AIDD"
    return "OUTRAS"


def formatar_tamanho(bytes_val):
    if bytes_val >= 1024 * 1024:
        return f"{bytes_val / (1024*1024):.1f} MB"
    return f"{bytes_val / 1024:.0f} KB"


def main():
    hoje = date.today()
    livros = descobrir_livros()

    # Agrupar por série
    grupos = {}
    for slug in livros:
        serie = classificar(slug)
        grupos.setdefault(serie, []).append(slug)

    # Ordenar grupos conforme SERIES_ORDEM + AIDD + OUTRAS
    ordem_chaves = [p[0] for p in SERIES_ORDEM] + ["AIDD", "OUTRAS"]
    chaves = [k for k in ordem_chaves if k in grupos]

    total_caps = 0
    total_pdf = 0

    linhas = []
    linhas.append("# 📚 Catálogo Geral das Obras — Fábrica Agêntica de Livros")
    linhas.append("")
    linhas.append(f"*Catálogo gerado em {hoje.strftime('%d/%m/%Y')}*")
    linhas.append("")
    linhas.append(f"**Total: {len(livros)} livros** organizados em séries temáticas. "
                  "Todos seguem o framework EITA-V2 (Explica, Ilustra, Técnica, Aplica) "
                  "com 16 capítulos (4 partes × 4 capítulos) e referências ABNT.")
    linhas.append("")
    linhas.append("---")
    linhas.append("")

    for chave in chaves:
        slugs_serie = sorted(grupos[chave])
        nome_serie, descricao = "", ""
        if chave in [p[0] for p in SERIES_ORDEM]:
            nome_serie = next(p[1] for p in SERIES_ORDEM if p[0] == chave)
            descricao = next(p[2] for p in SERIES_ORDEM if p[0] == chave)
        elif chave == "AIDD":
            nome_serie = "Série AIDD — AI-Driven Development"
            descricao = "A metodologia EITA e a engenharia de software guiada por agentes de IA."
        else:
            nome_serie = "Outras Obras"
            descricao = "Obras avulsas."

        linhas.append(f"## {nome_serie}")
        linhas.append("")
        if descricao:
            linhas.append(f"*{descricao}*")
            linhas.append("")
        linhas.append(f"**{len(slugs_serie)} livros**")
        linhas.append("")
        linhas.append("| # | Obra | PDF | Tamanho | Capítulos |")
        linhas.append("|---|------|-----|---------|-----------|")

        for i, slug in enumerate(slugs_serie, 1):
            sumario = coletar_sumario(slug)
            titulo = sumario.get("titulo_obra", slug) if sumario else slug
            caps = sum(len(p.get("capitulos", [])) for p in (sumario.get("partes", []) if sumario else [])) if sumario else 0
            total_caps += caps

            pdf_path = DIR_RAIZ / slug / "livro_final.pdf"
            if pdf_path.exists():
                total_pdf += 1
                tamanho = formatar_tamanho(pdf_path.stat().st_size)
                link = f"[PDF](output/{slug}/livro_final.pdf)"
            else:
                tamanho = "—"
                link = "—"

            # Sanitizar título para célula de tabela (escapar | e quebras)
            titulo_cell = titulo.replace("|", "\\|").replace("\n", " ").strip()
            linhas.append(f"| {i} | {titulo_cell} | {link} | {tamanho} | {caps} |")

        linhas.append("")
        linhas.append("---")
        linhas.append("")

    # Bloco final
    linhas.append("## 📄 Mega-Livro Total")
    linhas.append("")
    mega_dirs = sorted([d for d in DIR_RAIZ.iterdir() if d.is_dir() and d.name.startswith("mega-livro-total-")], reverse=True)
    if mega_dirs:
        mega = mega_dirs[0]
        pdf_mega = mega / "livro_final.pdf"
        if pdf_mega.exists():
            linhas.append(f"- **A Biblioteca Completa da Fábrica Agêntica de Livros** — reúne as {len(livros)} obras "
                          f"em um único volume de {formatar_tamanho(pdf_mega.stat().st_size)}.")
            linhas.append(f"- 📄 [Mega-Livro PDF](output/{mega.name}/livro_final.pdf)")
            linhas.append(f"- 📝 [Sumário unificado](output/{mega.name}/sumario_macro.json)")
    linhas.append("")
    linhas.append("---")
    linhas.append("")
    linhas.append("## 📊 Resumo")
    linhas.append("")
    linhas.append("| Série | Livros |")
    linhas.append("|-------|--------|")
    for chave in chaves:
        nome_serie = next((p[1] for p in SERIES_ORDEM if p[0] == chave), "AIDD" if chave == "AIDD" else "Outras")
        linhas.append(f"| {nome_serie} | {len(grupos[chave])} |")
    linhas.append(f"| **Total** | **{len(livros)}** |")
    linhas.append("")
    linhas.append(f"*{total_caps} capítulos | {total_pdf} PDFs disponíveis*")
    linhas.append("")
    linhas.append("---")
    linhas.append("")
    linhas.append("*Gerado automaticamente pela Fábrica Agêntica de Livros.*")

    conteudo = "\n".join(linhas)
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print(f"Catálogo gerado: {SAIDA}")
    print(f"  Livros: {len(livros)}")
    print(f"  Capítulos: {total_caps}")
    print(f"  PDFs disponíveis: {total_pdf}")
    print(f"  Séries: {chaves}")


if __name__ == "__main__":
    main()
