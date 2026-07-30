#!/usr/bin/env python3
"""
Compila TODOS os livros da Fabrica em um mega-livro unico.
Adaptado de compilar-mega-camadas.py para escala total.

61 livros, ~976 capitulos, ~40+ MB de PDF.

Uso: python compilar-mega-completo.py
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import date

# ── PATHS ────────────────────────────────────────────────────

PANDOC = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc-3.10\pandoc.exe"
TYPST  = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc\typst.exe"
TEMPLATE = Path(__file__).parent / "templates" / "template.typ"

for cmd, nome in [(PANDOC, "Pandoc"), (TYPST, "Typst")]:
    if not os.path.exists(cmd):
        print(f"[ERRO] {nome} nao encontrado em: {cmd}")
        sys.exit(1)
if not TEMPLATE.exists():
    print(f"[ERRO] Template Typst nao encontrado em: {TEMPLATE}")
    sys.exit(1)

DIR_RAIZ = Path(__file__).parent / "output"

# ── LIVROS ────────────────────────────────────────────────────

TODOS_LIVROS = [
    # Serie C0-C5 (AIDD Core)
    ("00-eita-metodo",           "O Metodo EITA: Explica, Ilustra, Tecnica, Aplica"),
    ("C1-transicao-dev-aidd",    "Transicao: De Dev Tradicional a Engenheiro AIDD"),
    ("C2-camada-interface",      "Camada Interface: A Tela onde o Humano Encontra a Maquina"),
    ("C3-camada-harness",        "Camada Harness: O Motor de Orquestracao"),
    ("C4-camada-operarios",      "Camada Operarios: Skills, MCPs e Subagentes"),
    ("C5-camada-llm-core",       "Camada LLM Core: O Cerebro que Pensa"),

    # Serie D1-D5 (Application Layers)
    ("D1-frontend-aidd",         "Frontend com AIDD: A Camada que o Usuario Ve"),
    ("D2-backend-aidd",          "Backend com AIDD: Onde a Logica Mora"),
    ("D3-database-aidd",         "Database com AIDD: Dados e Persistencia"),
    ("D4-apis-aidd",             "APIs com AIDD: Contratos e Integracoes"),
    ("D5-aplicacao-completa-aidd", "Aplicacao Completa com AIDD"),

    # Serie E — Seguranca e Governanca
    ("E1-seguranca-auth",        "E1 — Autenticacao e Autorizacao com AIDD"),
    ("E2-seguranca-cripto",      "E2 — Criptografia e Protecao de Dados"),
    ("E3-seguranca-owasp",       "E3 — OWASP e Seguranca de Aplicacoes"),
    ("E4-seguranca-compliance",  "E4 — Governanca e Compliance"),
    ("E5-seguranca-redteam",     "E5 — Red Team com Agentes de IA"),

    # Serie F — DevOps e Infraestrutura
    ("F1-devops-cicd",           "F1 — CI/CD com Agentes de IA"),
    ("F2-devops-docker",         "F2 — Containerizacao e Docker"),
    ("F3-devops-kubernetes",     "F3 — Kubernetes e Orquestracao"),
    ("F4-devops-iac",            "F4 — Infraestrutura como Codigo"),
    ("F5-devops-observabilidade","F5 — Observabilidade e Monitoramento"),

    # Serie G — Testes e Qualidade
    ("G1-testes-unitarios",      "G1 — Testes Unitarios com Agentes de IA"),
    ("G2-testes-integracao",     "G2 — Testes de Integracao"),
    ("G3-testes-e2e",            "G3 — Testes E2E e Performance"),
    ("G4-testes-codereview",     "G4 — Code Review com Agentes de IA"),
    ("G5-testes-qualidade",      "G5 — Qualidade e Divida Tecnica"),

    # Serie H — Automacao e Robotica
    ("H1-automacao-rpa",         "H1 — RPA com Agentes de IA"),
    ("H2-automacao-pipeline",    "H2 — Pipelines de Automacao"),
    ("H3-automacao-iot",         "H3 — IoT e Agentes de IA"),
    ("H4-automacao-processos",   "H4 — Automacao de Processos"),
    ("H5-automacao-lowcode",     "H5 — Low-Code/No-Code"),

    # Serie I — Dados e Analytics
    ("I1-dados-engenharia",      "I1 — Engenharia de Dados"),
    ("I2-dados-analytics",       "I2 — Analytics e BI"),
    ("I3-dados-ml",              "I3 — Machine Learning"),
    ("I4-dados-streaming",       "I4 — Stream Processing"),
    ("I5-dados-governanca",      "I5 — Governanca de Dados"),

    # Serie J — Fintech
    ("J1-fintech-pagamentos",    "J1 — Pagamentos e Transacoes"),
    ("J2-fintech-regulatorio",   "J2 — Regulatorio e Compliance Financeiro"),
    ("J3-fintech-blockchain",    "J3 — Blockchain e Web3"),
    ("J4-fintech-openbanking",   "J4 — Open Banking e Open Finance"),
    ("J5-fintech-fraud",         "J5 — Prevencao a Fraudes"),

    # Serie K — Mobile
    ("K1-mobile-reactnative",    "K1 — React Native"),
    ("K2-mobile-flutter",        "K2 — Flutter"),
    ("K3-mobile-ios",            "K3 — iOS e Swift"),
    ("K4-mobile-android",        "K4 — Android e Kotlin"),
    ("K5-mobile-multiplataforma","K5 — Estrategias Multiplataforma"),

    # Serie L — Cloud
    ("L1-cloud-aws",             "L1 — AWS"),
    ("L2-cloud-azure",           "L2 — Azure"),
    ("L3-cloud-gcp",             "L3 — GCP"),
    ("L4-cloud-serverless",      "L4 — Serverless"),
    ("L5-cloud-multicloud",      "L5 — Estrategias Multi-Cloud"),

    # Serie M — Performance
    ("M1-performance-web",       "M1 — Web Performance"),
    ("M2-performance-api",       "M2 — API Performance"),
    ("M3-performance-banco",     "M3 — Database Performance"),
    ("M4-performance-mobile",    "M4 — Mobile Performance"),
    ("M5-performance-escala",    "M5 — Escala e Alta Disponibilidade"),

    # Serie N — Corporativo
    ("N1-corporativo-microservicos",  "N1 — Microservices"),
    ("N2-corporativo-eventos",        "N2 — Event-Driven Architecture"),
    ("N3-corporativo-legado",         "N3 — Modernizacao de Legado"),
    ("N4-corporativo-equipes",        "N4 — Gestao de Equipes AIDD"),
    ("N5-corporativo-governanca",     "N5 — Governanca Corporativa AIDD"),
]

SLUG_COMPILADO = f"mega-livro-completo-aidd-{date.today().isoformat()}"


def step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def coletar_sumario(slug):
    path = DIR_RAIZ / slug / "sumario_macro.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extrair_frontmatter(texto):
    return re.sub(r'^---\n.*?\n---\n', '', texto, flags=re.DOTALL)


def renumerar_titulo(conteudo, novo_numero):
    conteudo = re.sub(
        r'^# Cap[ií]tulo \d+[\s]*[—:–]?[\s]*',
        f'# Capítulo {novo_numero} — ',
        conteudo,
        flags=re.MULTILINE
    )
    return conteudo


def main():
    hoje = date.today()

    step(f"Criar pasta {SLUG_COMPILADO} (limpa)")
    dir_compilado = DIR_RAIZ / SLUG_COMPILADO
    dir_caps = dir_compilado / "capitulos"
    if dir_compilado.exists():
        shutil.rmtree(dir_compilado)
    dir_caps.mkdir(parents=True, exist_ok=True)
    print(f"  Pasta: {dir_compilado}")

    # ── LER SUMARIOS ──────────────────────────────────────────

    step("Ler sumarios dos livros")

    sumarios = []
    for slug, label in TODOS_LIVROS:
        s = coletar_sumario(slug)
        if s:
            sumarios.append((slug, label, s))
            qtd = sum(len(p.get("capitulos",[])) for p in s.get("partes",[]))
            print(f"  + {label}: {qtd} caps")
        else:
            print(f"  [AVISO] {slug} nao encontrado")

    if not sumarios:
        print("[ERRO] Nenhum sumario encontrado!")
        sys.exit(1)

    # ── CONSTUIR SUMARIO UNIFICADO ────────────────────────────

    step("Construir sumario unificado")

    titulo_base = "AI-Driven Development: A Enciclopedia Completa do Engenheiro AIDD"

    # Serao preenchidos apos o loop com valores reais
    introducao = None
    conclusao = None

    partes_unificadas = []
    contador_global = 0

    for idx, (slug, label, sumario) in enumerate(sumarios):
        capitulos_parte = []
        for parte in sumario.get("partes", []):
            for cap in parte.get("capitulos", []):
                contador_global += 1
                capitulos_parte.append({
                    "capitulo": contador_global,
                    "titulo": cap.get("titulo", ""),
                    "slug_origem": slug,
                    "cap_original": cap.get("capitulo", 0)
                })

        if capitulos_parte:
            partes_unificadas.append({
                "parte": idx + 1,
                "titulo_parte": label,
                "capitulos": capitulos_parte
            })

    subtitulo = f"{len(sumarios)} Livros | {contador_global} Capitulos | Guia Definitivo de Tecnicas, Tokens e Configuracoes"

    total_partes = len(partes_unificadas)
    introducao = (
        f"Esta mega-obra reune a totalidade dos {len(sumarios)} livros produzidos pela "
        f"Fabrica Agente de Livros sobre AI-Driven Development. Dos fundamentos do metodo "
        f"EITA e das 4 camadas classicas do AIDD, passando pelas camadas de aplicacao "
        f"(Frontend, Backend, Database, APIs), ate as 10 series especializadas: Seguranca, "
        f"DevOps, Testes, Automacao, Dados, Fintech, Mobile, Cloud, Performance e Corporativo.\n\n"
        f"Organizado em {total_partes} partes tematicas, com {contador_global} capitulos, "
        f"este volume e a referencia mais completa sobre como engenheiros de software podem "
        f"dominar o paradigma AIDD."
    )
    conclusao = (
        f"O ecossistema AIDD e vasto e esta em constante evolucao. Os {len(sumarios)} livros "
        f"compilados neste volume representam o estado-da-arte do conhecimento sobre AI-Driven "
        f"Development em 2026. Cada livro aborda uma area especifica com o rigor do metodo "
        f"EITA-V2, garantindo que o leitor nao apenas entenda os conceitos, mas consiga "
        f"aplica-los imediatamente no seu dia a dia.\n\n"
        f"O engenheiro AIDD que dominar estas {len(sumarios)} areas estara preparado para "
        f"liderar a transformacao que redefine o desenvolvimento de software."
    )

    sumario_unificado = {
        "titulo_obra": titulo_base,
        "subtitulo": subtitulo,
        "slug_compilado": SLUG_COMPILADO,
        "data_compilacao": hoje.isoformat(),
        "introducao": introducao,
        "conclusao": conclusao,
        "partes": partes_unificadas
    }

    print(f"  Livros: {len(sumarios)}")
    print(f"  Capitulos: {contador_global}")
    print(f"  Partes: {len(partes_unificadas)}")

    # ── SALVAR SUMARIO ────────────────────────────────────────

    step("Salvar sumario_macro.json")
    sumario_path = dir_compilado / "sumario_macro.json"
    with open(sumario_path, "w", encoding="utf-8") as f:
        json.dump(sumario_unificado, f, indent=2, ensure_ascii=False)
    print(f"  Salvo: {sumario_path}")

    # ── CONCATENAR E RENUMERAR ────────────────────────────────

    step("Concatenar e renumerar capitulos")

    contador_gravado = 0
    for parte in partes_unificadas:
        for cap_info in parte["capitulos"]:
            contador_gravado += 1
            slug_origem = cap_info["slug_origem"]
            cap_original = cap_info["cap_original"]

            cap_path = DIR_RAIZ / slug_origem / "capitulos" / f"cap_{cap_original}.md"
            if not cap_path.exists():
                cap_path = DIR_RAIZ / slug_origem / "capitulos" / f"cap_{cap_original:02d}.md"
            if not cap_path.exists():
                print(f"  [AVISO] Cap {slug_origem}/cap_{cap_original}.md nao encontrado")
                continue

            with open(cap_path, "r", encoding="utf-8") as f:
                conteudo = f.read()

            conteudo = extrair_frontmatter(conteudo)
            conteudo = renumerar_titulo(conteudo, contador_gravado)

            cap_destino = dir_caps / f"cap_{contador_gravado}.md"
            with open(cap_destino, "w", encoding="utf-8") as f:
                f.write(conteudo)

    print(f"  Capitulos processados: {contador_gravado}")

    # ── GERAR ELEMENTOS TEXTUAIS ──────────────────────────────

    step("Gerar elementos textuais")

    prefacio = f"""# Prefacio

{introducao}

## Sobre este Compilado

- **{len(sumarios)} livros** reunidos em uma unica obra
- **{contador_global} capitulos** organizados em **{len(partes_unificadas)} partes**
- Compilado gerado em **{hoje.strftime('%d/%m/%Y')}**

Cada parte corresponde a um livro original, mantendo sua identidade e estrutura interna.
Os capitulos foram renumerados sequencialmente para facilitar a navegacao.

## Como Navegar

Utilize o sumario abaixo para localizar rapidamente os temas de seu interesse.
"""

    sumario_texto = "# Sumario\n\n"
    for parte in partes_unificadas:
        sumario_texto += f"- **Parte {parte['parte']} — {parte['titulo_parte']}**\n"
        for cap in parte["capitulos"]:
            sumario_texto += f"  - Capitulo {cap['capitulo']}: {cap['titulo']}\n"

    conc = f"""# Conclusao

{conclusao}

*Compilado gerado pela Fabrica Agente de Livros em {hoje.strftime('%d/%m/%Y')}.*
"""

    # ── MONTAR LIVRO FINAL ────────────────────────────────────

    step("Montar livro_final.md")

    corpo_partes = []
    ultima_parte = 0
    for parte in partes_unificadas:
        parte_num = parte["parte"]
        if parte_num != ultima_parte:
            corpo_partes.append(f"\n\n# Parte {parte_num} — {parte['titulo_parte']}\n")
            ultima_parte = parte_num
        for cap in parte["capitulos"]:
            idx = cap["capitulo"]
            cap_path = dir_caps / f"cap_{idx}.md"
            if cap_path.exists():
                with open(cap_path, "r", encoding="utf-8") as f:
                    corpo_partes.append(f.read().strip())

    corpo_texto = "\n\n".join(corpo_partes)

    livro_final = f"""# {titulo_base}

*{subtitulo}*

{prefacio}

{sumario_texto}

{corpo_texto}

{conc}
"""

    md_path = dir_compilado / "livro_final.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(livro_final)

    md_kb = md_path.stat().st_size / 1024
    print(f"  livro_final.md: {md_kb:.0f} KB ({md_kb/1024:.1f} MB)")

    # ── GERAR PDF ─────────────────────────────────────────────

    step("Gerar PDF via Pandoc+Typst (pode levar varios minutos)")

    pdf_path = dir_compilado / "livro_final.pdf"

    try:
        comando = [
            PANDOC, str(md_path), "-o", str(pdf_path),
            "--pdf-engine", TYPST,
            "--template", str(TEMPLATE),
            "--toc", "--toc-depth", "3",
            "--number-sections",
            "--from", "markdown-citations",
            "--wrap", "preserve",
            "-V", f"title={titulo_base}",
            "-V", "author=Heverton Eduardo Peres",
            "-V", "subtitle=",
            "--resource-path", str(dir_compilado),
            "-V", f"date={hoje.strftime('%d/%m/%Y')}",
        ]

        md_mb = md_kb / 1024
        print(f"  MD fonte: {md_mb:.1f} MB")
        print(f"  Executando Pandoc+Typst (timeout 900s)...")

        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=900)

        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            mb = pdf_path.stat().st_size / (1024*1024)
            print(f"  [OK] PDF: {pdf_path.name} ({mb:.2f} MB)")

            slug_pdf = dir_compilado / f"{SLUG_COMPILADO}.pdf"
            shutil.copy2(pdf_path, slug_pdf)
            print(f"  [OK] Copiado: {slug_pdf.name} ({slug_pdf.stat().st_size/(1024*1024):.2f} MB)")
        else:
            print(f"  [FALHA] PDF nao criado!")
            if resultado.stderr:
                errs = resultado.stderr.strip().split('\n')
                for err in errs[-10:]:
                    print(f"  STDERR: {err}")
            sys.exit(1)

    except subprocess.TimeoutExpired:
        print(f"  [ERRO] Timeout! O arquivo MD tem {md_mb:.1f} MB e excedeu 900s")
        sys.exit(1)
    except Exception as e:
        print(f"  [ERRO] {e}")
        sys.exit(1)

    # ── VALIDACAO ─────────────────────────────────────────────

    step("Validacao final")

    erros = []
    for nome in ["livro_final.md","sumario_macro.json","livro_final.pdf",f"{SLUG_COMPILADO}.pdf"]:
        p = dir_compilado / nome
        if p.exists() and p.stat().st_size > 0:
            sz = p.stat().st_size / (1024*1024) if nome.endswith(".pdf") else p.stat().st_size / 1024
            unid = "MB" if nome.endswith(".pdf") else "KB"
            print(f"  [OK] {nome}: {sz:.1f} {unid}")
        else:
            print(f"  [FALHA] {nome} ausente")
            erros.append(nome)

    caps = sorted(dir_caps.glob("cap_*.md"))
    print(f"  [OK] Capitulos individuais: {len(caps)}")
    if caps:
        nums = sorted([int(re.search(r'cap_(\d+)', p.stem).group(1)) for p in caps])
        if nums == list(range(1, len(nums)+1)):
            print(f"  [OK] Numeracao: 1 a {len(nums)} sem saltos")
        else:
            print(f"  [FALHA] Numeracao inconsistente")
            erros.append("numeracao")

    pdf_mb = pdf_path.stat().st_size / (1024*1024) if pdf_path.exists() else 0

    print(f"\n{'='*60}")
    print(f"  COMPILACAO CONCLUIDA")
    print(f"{'='*60}")
    print(f"  Pasta: output/{SLUG_COMPILADO}/")
    print(f"  PDF:   {SLUG_COMPILADO}.pdf ({pdf_mb:.1f} MB)")
    print(f"  Status: {'OK' if not erros else 'FALHA: '+', '.join(erros)}")
    print()

    if erros:
        sys.exit(1)


if __name__ == "__main__":
    main()
