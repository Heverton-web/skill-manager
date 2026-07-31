#!/usr/bin/env python3
"""
Compila cada serie ZP1-ZP4 (20 livros cada) em um mega-livro unico por serie.
Seguindo o fluxo de compilar-mega-planejamento.py / compilar-mega-livro.py.

Cada serie é uma jornada 'Do Zero ao Profissional': o mega-livro reune os 20
livros da série em um único volume com 20 partes e 320 capítulos renumerados.

Fluxo (por serie):
  1. Criar pasta limpa output/ZPx-mega-serie-ZPx/
  2. Ler sumarios macro dos 20 livros da serie
  3. Salvar sumario_macro.json unificado (20 partes, 320 capitulos)
  4. Concatenar e renumerar capitulos sequencialmente (1 a 320)
  5. Gerar prefacio + sumario + conclusao
  6. Montar livro_final.md
  7. Gerar PDF via Pandoc+Typst
  8. Validar

Uso: python compilar-mega-zp.py
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import date

# Caminhos dos executaveis (duplicados intencionalmente, mesmo padrao dos
# demais scripts compilar-mega-*.py, pois nomes com hifen impedem import direto)
PANDOC = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc-3.10\pandoc.exe"
TYPST = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc\typst.exe"
TEMPLATE = Path(__file__).parent / "templates" / "template.typ"

for cmd, nome in [(PANDOC, "Pandoc"), (TYPST, "Typst")]:
    if not os.path.exists(cmd):
        print(f"[ERRO] {nome} nao encontrado em: {cmd}")
        sys.exit(1)
if not TEMPLATE.exists():
    print(f"[ERRO] Template Typst nao encontrado em: {TEMPLATE}")
    sys.exit(1)

DIR_RAIZ = Path(__file__).parent / "output"

try:
    from dados_series_zp import (
        SLUGS_ZP,
        SERIES_ZP,
        LIVROS_ZP,
    )
except ImportError:
    print("[ERRO] dados_series_zp.py nao encontrado (leve os arquivos js/python/sql/git juntos).")
    sys.exit(1)


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


def compilar_serie(prefix, hoje):
    """Compila os livros de uma serie em um mega-livro unico."""
    serie_nome = SERIES_ZP.get(prefix, {}).get("nome", prefix)
    slugs_serie = [s for s in SLUGS_ZP if s.split("-")[0] == prefix]

    if not slugs_serie:
        print(f"  [AVISO] Serie {prefix} sem livros — pulando")
        return None

    SLUG_COMPILADO = f"{prefix}-mega-serie-{prefix}"
    dir_compilado = DIR_RAIZ / SLUG_COMPILADO
    dir_caps = dir_compilado / "capitulos"

    step(f"SERIE {prefix}: {serie_nome} ({len(slugs_serie)} livros) -> {SLUG_COMPILADO}")

    # --- Passo 1: pasta limpa ---
    if dir_compilado.exists():
        shutil.rmtree(dir_compilado)
    dir_caps.mkdir(parents=True, exist_ok=True)
    print(f"  Pasta: {dir_compilado}")

    # --- Passo 2: ler sumarios dos livros ---
    sumarios = []
    for slug in slugs_serie:
        s = coletar_sumario(slug)
        if s:
            sumarios.append((slug, s))
            qtd = sum(len(p.get("capitulos", [])) for p in s.get("partes", []))
            print(f"  + {slug}: {qtd} caps")
        else:
            print(f"  [AVISO] {slug}: sem sumario — sera ignorado")

    if not sumarios:
        print(f"  [ERRO] Nenhum sumario encontrado para a serie {prefix}!")
        return None

    # --- Construir sumario unificado ---
    titulo_base = f"Série {prefix}: {serie_nome} — Coleção Completa"

    introducao = (
        f"Este mega-livro reúne os {len(sumarios)} livros da série {prefix} — "
        f"{serie_nome}. É a jornada completa do assunto: cada parte corresponde a "
        "um livro original da série, do absoluto zero à proficiência profissional, "
        "com os capítulos renumerados sequencialmente para facilitar a navegação."
    )
    conclusao = (
        f"A série {prefix} — {serie_nome} — entrega um percurso completo e "
        "progressivo: dos fundamentos absolutos às práticas avançadas e à "
        "preparação para o mercado de trabalho. Este compilado em volume único "
        "oferece ao leitor uma referência consolidada para consulta contínua."
    )

    partes_unificadas = []
    contador_global = 0

    for idx, (slug, sumario) in enumerate(sumarios):
        # Titulo da parte = titulo do livro (titulo_obra do sumario, com fallback)
        titulo_parte = sumario.get("titulo_obra", "")
        if not titulo_parte:
            titulo_parte = LIVROS_ZP.get(slug, ("", "", "", "", "", ""))[1]
        if not titulo_parte:
            titulo_parte = slug

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
                "titulo_parte": titulo_parte,
                "capitulos": capitulos_parte
            })

    subtitulo = f"{len(sumarios)} livros | {contador_global} capítulos em um único volume"

    sumario_unificado = {
        "titulo_obra": titulo_base,
        "subtitulo": subtitulo,
        "slug_compilado": SLUG_COMPILADO,
        "serie": prefix,
        "data_compilacao": hoje.isoformat(),
        "introducao": introducao,
        "conclusao": conclusao,
        "partes": partes_unificadas
    }

    print(f"  Livros: {len(sumarios)} | Capitulos: {contador_global} | Partes: {len(partes_unificadas)}")

    # --- Passo 3: salvar sumario_macro.json ---
    sumario_path = dir_compilado / "sumario_macro.json"
    with open(sumario_path, "w", encoding="utf-8") as f:
        json.dump(sumario_unificado, f, indent=2, ensure_ascii=False)
    print(f"  Salvo: {sumario_path}")

    # --- Passo 4: concatenar e renumerar capitulos ---
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

    # --- Passo 5: gerar elementos extrusos ---
    prefacio = f"""# Prefácio

{introducao}

## Sobre este Compilado

- **{len(sumarios)} livros** reunidos em uma única obra
- **{contador_global} capítulos** organizados em **{len(partes_unificadas)} partes**
- Compilado gerado em **{hoje.strftime('%d/%m/%Y')}**

Cada parte corresponde a um livro original da série, do zero absoluto à
proficiência profissional. Os capítulos foram renumerados sequencialmente
para facilitar a navegação.

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

    # --- Passo 6: montar livro_final.md ---
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

    # --- Passo 7: gerar PDF via Pandoc+Typst ---
    pdf_path = dir_compilado / "livro_final.pdf"
    mb = 0

    try:
        comando = [
            PANDOC, str(md_path), "-o", str(pdf_path),
            "--pdf-engine", TYPST,
            "--template", str(TEMPLATE),
            "--toc", "--toc-depth", "2",
            "--number-sections",
            "--from", "markdown-citations",
            "--wrap", "preserve",
            "-V", f"title={titulo_base}",
            "-V", "author=Heverton Eduardo Peres",
            "-V", "subtitle=",
            "--resource-path", str(dir_compilado),
            "-V", f"date={hoje.strftime('%d/%m/%Y')}",
        ]

        print(f"  Executando Pandoc+Typst (pode levar varios minutos)...")
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=3600)

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
            return None

    except subprocess.TimeoutExpired:
        print(f"  [ERRO] Timeout!")
        return None
    except Exception as e:
        print(f"  [ERRO] {e}")
        return None

    # --- Passo 8: validacao ---
    erros = []
    for nome in ["livro_final.md", "sumario_macro.json", "livro_final.pdf", f"{SLUG_COMPILADO}.pdf"]:
        p = dir_compilado / nome
        if p.exists() and p.stat().st_size > 0:
            print(f"  [OK] {nome}: {p.stat().st_size/1024:.0f} KB")
        else:
            print(f"  [FALHA] {nome} ausente")
            erros.append(nome)

    caps = sorted(dir_caps.glob("cap_*.md"))
    print(f"  [OK] Capitulos individuais: {len(caps)}")
    if len(caps) != contador_global:
        print(f"  [FALHA] Esperava {contador_global} capitulos, encontrados {len(caps)}")
        erros.append("contagem_capitulos")
    if caps:
        nums = sorted([int(re.search(r'cap_(\d+)', p.stem).group(1)) for p in caps])
        if nums == list(range(1, len(nums) + 1)):
            print(f"  [OK] Numeracao: 1 a {len(nums)} sem saltos")
        else:
            print(f"  [FALHA] Numeracao inconsistente")
            erros.append("numeracao")

    print(f"\n  Resultado serie {prefix}: {'OK' if not erros else 'FALHA: ' + ', '.join(erros)}")
    return None if erros else (SLUG_COMPILADO, mb)


def main():
    hoje = date.today()
    step("MEGA-LIVROS POR SERIE (ZP1-ZP4) — DO ZERO AO PROFISSIONAL")

    resultados = []
    falhas = []

    for prefix in sorted(SERIES_ZP.keys()):
        r = compilar_serie(prefix, hoje)
        if r:
            resultados.append(r)
        else:
            falhas.append(prefix)

    step("RELATORIO FINAL")
    print(f"  Mega-livros criados: {len(resultados)}/{len(SERIES_ZP)}")
    for slug, mb in resultados:
        print(f"    [OK] {slug} ({mb:.1f} MB)")
    if falhas:
        print(f"  Falhas: {', '.join(falhas)}")
        sys.exit(1)
    print("  [OK] Todas as series compiladas com sucesso!")


if __name__ == "__main__":
    main()
