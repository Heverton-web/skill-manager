#!/usr/bin/env python3
"""
Compila os 5 livros da Serie AIDD em um mega-livro unico.
Inclui o livro de transicao + as 4 camadas.
Usa o mesmo fluxo do compilar-mega-livro.py.

Fluxo:
  1. Criar pasta limpa
  2. Ler sumarios macro dos 5 livros
  3. Salvar sumario_macro.json unificado
  4. Concatenar e renumerar 80 capitulos sequencialmente
  5. Gerar prefacio + sumario + conclusao
  6. Montar livro_final.md
  7. Gerar PDF via Pandoc+Typst

Uso: python compilar-mega-camadas.py
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import date

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

SLUGS_CAMADAS = [
    ("00-eita-metodo",           "O Método EITA: Explica, Ilustra, Técnica, Aplica"),
    ("C1-transicao-dev-aidd",    "A Transição: De Dev Tradicional a Engenheiro AIDD"),
    ("C2-camada-interface",      "Camada 1 — Interface: A Tela"),
    ("C3-camada-harness",        "Camada 2 — Harness: O Motor de Orquestração"),
    ("C4-camada-operarios",      "Camada 3 — Operários: Skills, MCPs e Subagentes"),
    ("C5-camada-llm-core",       "Camada 4 — LLM Core: O Cérebro que Pensa"),
]

SLUG_COMPILADO = f"07-mega-livro-completo-aidd-{date.today().isoformat()}"


def step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def coletar_sumario(slug):
    path = DIR_RAIZ / slug / "sumario_macro.json"
    if not path.exists():
        print(f"  [AVISO] sumario nao encontrado para {slug}")
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

    # ---

    step("Ler sumarios dos 5 livros")

    sumarios = []
    for slug, label in SLUGS_CAMADAS:
        s = coletar_sumario(slug)
        if s:
            sumarios.append((slug, label, s))
            qtd = sum(len(p.get("capitulos",[])) for p in s.get("partes",[]))
            print(f"  + {label}: {qtd} caps")

    if not sumarios:
        print("[ERRO] Nenhum sumario encontrado!")
        sys.exit(1)

    # ---

    step("Construir sumario unificado")

    titulo_base = "AI-Driven Development: Guia Completo do Engenheiro AIDD"
    subtitulo = "Transição, Interface, Harness, Operários e LLM Core — A Série Completa em um Único Volume"

    introducao = (
        "Este mega-livro reúne os 5 livros da série AIDD: a obra de transição que mostra "
        "o caminho do desenvolvimento tradicional para o AIDD, seguida pelos 4 livros que "
        "exploram em profundidade cada camada do ecossistema. "
        "Organizado da visão geral até o núcleo de raciocínio, ele fornece ao engenheiro "
        "de software um domínio completo sobre técnicas de utilização, economia de tokens "
        "e configurações avançadas de cada camada."
    )
    conclusao = (
        "A transição para o AIDD não é uma ameaça — é uma promoção. O domínio das 4 camadas "
        "— Interface, Harness, Operários e LLM Core — combinado com a compreensão da jornada "
        "de transformação apresentada no livro de abertura, forma o conhecimento essencial "
        "para qualquer engenheiro que deseja liderar a nova era do desenvolvimento de software. "
        "Este compilado oferece uma referência completa para quem quer orquestrar agentes "
        "de IA com maestria."
    )

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

    sumario_unificado = {
        "titulo_obra": titulo_base,
        "subtitulo": subtitulo,
        "slug_compilado": SLUG_COMPILADO,
        "data_compilacao": hoje.isoformat(),
        "introducao": introducao,
        "conclusao": conclusao,
        "partes": partes_unificadas
    }

    total_livros = len(sumarios)
    print(f"  Livros: {total_livros}")
    print(f"  Capitulos: {contador_global}")
    print(f"  Partes: {len(partes_unificadas)}")

    # ---

    step("Salvar sumario_macro.json")
    sumario_path = dir_compilado / "sumario_macro.json"
    with open(sumario_path, "w", encoding="utf-8") as f:
        json.dump(sumario_unificado, f, indent=2, ensure_ascii=False)
    print(f"  Salvo: {sumario_path}")

    # ---

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

    # ---

    step("Gerar elementos extrusos")

    prefacio = f"""# Prefácio

{introducao}

## Sobre este Compilado

- **{total_livros} livros** reunidos em uma única obra
- **{contador_global} capítulos** organizados em **{len(partes_unificadas)} partes**
- Compilado gerado em **{hoje.strftime('%d/%m/%Y')}**

Cada parte corresponde a um livro original, mantendo sua identidade e estrutura interna.
Os capítulos foram renumerados sequencialmente para facilitar a navegação.

## Como Navegar

Utilize o sumário abaixo para localizar rapidamente os temas de seu interesse.
"""

    sumario_texto = "# Sumário\n\n"
    for parte in partes_unificadas:
        sumario_texto += f"- **Parte {parte['parte']} — {parte['titulo_parte']}**\n"
        for cap in parte["capitulos"]:
            sumario_texto += f"  - Capítulo {cap['capitulo']}: {cap['titulo']}\n"

    conc = f"""# Conclusão

{conclusao}

*Compilado gerado pela Fábrica Agêntica de Livros em {hoje.strftime('%d/%m/%Y')}.*
"""

    # ---

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
    print(f"  livro_final.md: {md_path.stat().st_size/1024:.0f} KB")

    # ---

    step("Gerar PDF via Pandoc+Typst")

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

        print(f"  Executando Pandoc+Typst...")
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=600)

        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            mb = pdf_path.stat().st_size / (1024*1024)
            print(f"  [OK] PDF: {pdf_path.name} ({mb:.1f} MB)")

            slug_pdf = dir_compilado / f"{SLUG_COMPILADO}.pdf"
            shutil.copy2(pdf_path, slug_pdf)
            print(f"  [OK] Copiado: {slug_pdf.name}")
        else:
            print(f"  [FALHA] PDF nao criado!")
            if resultado.stderr:
                for err in resultado.stderr.strip().split('\n')[-5:]:
                    print(f"  STDERR: {err}")
            sys.exit(1)

    except subprocess.TimeoutExpired:
        print(f"  [ERRO] Timeout!")
        sys.exit(1)
    except Exception as e:
        print(f"  [ERRO] {e}")
        sys.exit(1)

    # ---

    step("Validacao final")

    erros = []
    for nome in ["livro_final.md","sumario_macro.json","livro_final.pdf",f"{SLUG_COMPILADO}.pdf"]:
        p = dir_compilado / nome
        if p.exists() and p.stat().st_size > 0:
            print(f"  [OK] {nome}: {p.stat().st_size/1024:.0f} KB")
        else:
            print(f"  [FALHA] {nome} ausente")
            erros.append(nome)

    caps = sorted(dir_caps.glob("cap_*.md"))
    print(f"  [OK] Capítulos individuais: {len(caps)}")
    if caps:
        nums = sorted([int(re.search(r'cap_(\d+)', p.stem).group(1)) for p in caps])
        if nums == list(range(1, len(nums)+1)):
            print(f"  [OK] Numeração: 1 a {len(nums)} sem saltos")
        else:
            print(f"  [FALHA] Numeração inconsistente")
            erros.append("numeracao")

    print(f"\n{'='*60}")
    print(f"  COMPILACAO CONCLUIDA")
    print(f"{'='*60}")
    print(f"  Pasta: output/{SLUG_COMPILADO}/")
    print(f"  PDF:   {SLUG_COMPILADO}.pdf ({pdf_path.stat().st_size/(1024*1024):.1f} MB)")
    print(f"  Status: {'OK' if not erros else 'FALHA: '+', '.join(erros)}")
    print()

    if erros:
        sys.exit(1)


if __name__ == "__main__":
    main()
