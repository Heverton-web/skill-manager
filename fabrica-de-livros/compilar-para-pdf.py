#!/usr/bin/env python3
"""
Compila livro_final.md com conteudo real dos capitulos e converte para PDF.
Usa Pandoc + Typst com template ABNT para gerar PDF profissional.

Uso: python compilar-para-pdf.py [slug1 slug2 ...]
     (omita slugs para processar todos os livros cadastrados)
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# ── CARREGAR 50 LIVROS DAS SÉRIES E-N ──────────────────────────
try:
    from dados_series import SLUGS_EXTRA
except ImportError:
    SLUGS_EXTRA = []

DIR_RAIZ = Path(__file__).parent / "output"
DIR_PROJETO = Path(__file__).parent

PANDOC = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc-3.10\pandoc.exe"
TYPST = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc\typst.exe"
TEMPLATE = DIR_PROJETO / "templates" / "template.typ"

SLUGS = [
    # Serie Agentes CLI
    "revolucao-agentes-cli",
    "modelos-avancados-terminal",
    "roteamento-llms-gratuito",
    "fluxos-profissionais",
    # Serie LLMs (nota: diretorio real com prefixo B3-)
    "llms-freetiers",  # symlink aponta para B3-llms-freetiers no disco local
    # Serie Segredos
    "segredos-opencode",
    "segredos-freebuff",
    "segredos-oh-my-pi",
    "segredos-mimocode",
    # Serie AIDD
    "00-mega-livro-todos-aidd",
    "01-aidd-ai-driven-development",
    "01-transicao-dev-aidd",
    "02-harness-camada-orquestracao",
    "03-harness-suas-camadas",
    "04-motor-cognitivo-llm-core",
    "05-economia-tokens-cache",
    "06-rules-restricoes-globais",
    "07-specs-spec-driven",
    "08-skills-conhecimento-sob-demanda",
    "09-prompts-engenharia-interacao",
    "10-subagentes-workflows-paralelos",
    "11-mcp-rag",
    "12-guardrails-governanca",
    "13-higiene-contexto",
    "14-arvore-decisao-auditoria",
    "A-opencode-personalizacoes-escondidas",
    # Serie Camadas AIDD
    "00-eita-metodo",
    "C1-transicao-dev-aidd",
    "C2-camada-interface",
    "C3-camada-harness",
    "C4-camada-operarios",
    "C5-camada-llm-core",
]

# Estender com as 10 series (50 livros)
SLUGS.extend(SLUGS_EXTRA)


def copiar_pdf_com_nome_slug(slug, dir_livro):
    """Copia livro_final.pdf para <slug>.pdf no mesmo diretorio."""
    import shutil
    origem = dir_livro / "livro_final.pdf"
    destino = dir_livro / f"{slug}.pdf"
    if origem.exists():
        shutil.copy2(origem, destino)
        tamanho_kb = destino.stat().st_size / 1024
        print(f"  [OK] PDF copiado: {destino.name} ({tamanho_kb:.1f} KB)")
        return True
    return False


def extrair_frontmatter(texto):
    """Extrai YAML frontmatter do markdown."""
    match = re.match(r'^---\n(.*?)\n---\n', texto, re.DOTALL)
    if match:
        return match.group(1), texto[match.end():]
    return '', texto


def converter_md_direto(slug, dir_livro, md_path, pdf_path):
    """Converte livro_final.md pre-compilado diretamente para PDF via Pandoc+Typst."""
    print(f"  Convertendo MD pre-compilado -> PDF...")
    
    # Extrair titulo do sumario
    titulo = slug
    sumario_path = dir_livro / "sumario_macro.json"
    if sumario_path.exists():
        import json
        with open(sumario_path, 'r', encoding='utf-8') as f:
            try:
                sumario = json.load(f)
                titulo = sumario.get('titulo_obra', slug)
            except:
                pass
    
    try:
        comando = [
            PANDOC,
            str(md_path),
            "-o", str(pdf_path),
            "--pdf-engine", TYPST,
            "--template", str(TEMPLATE),
            "--toc",
            "--toc-depth", "3",
            "--number-sections",
            "--from", "markdown-citations",
            "--wrap", "preserve",
            "-V", f"title={titulo}",
            "-V", "author=Heverton Eduardo Peres",
            "-V", "subtitle=",
            "--resource-path", str(dir_livro),
        ]

        resultado = subprocess.run(
            comando,
            capture_output=True, text=True, timeout=300  # 5 min para mega-livro
        )

        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            tamanho_kb = pdf_path.stat().st_size / 1024
            print(f"  [OK] PDF gerado: {pdf_path.name} ({tamanho_kb:.1f} KB)")
            copiar_pdf_com_nome_slug(slug, dir_livro)
            return True
        else:
            print(f"  [FALHA] PDF nao foi criado")
            if resultado.stderr:
                erros = resultado.stderr.strip().split('\n')[-5:]
                for err in erros:
                    print(f"  STDERR: {err}")
            return False

    except subprocess.TimeoutExpired:
        print(f"  [ERRO] Timeout - conversao excedeu 300s")
        return False
    except Exception as e:
        print(f"  [ERRO] Falha na conversao: {e}")
        return False


def compilar_livro(slug):
    """Compila livro com capitulos reais e gera PDF profissional via Pandoc+Typst."""
    dir_livro = DIR_RAIZ / slug
    dir_caps = dir_livro / "capitulos"
    dir_imagens = dir_livro / "imagens"

    # Caminho do PDF final
    pdf_path = dir_livro / "livro_final.pdf"

    print(f"\n{'='*60}")
    print(f"  COMPILANDO: {slug}")
    print(f"{'='*60}")

    # Ler todos os capitulos ordenados
    caps = sorted(
        dir_caps.glob("cap_*.md"),
        key=lambda p: int(re.search(r'cap_(\d+)', p.stem).group(1))
    )

    md_precompilado = dir_livro / "livro_final.md"
    
    if not caps:
        # Fallback: usar livro_final.md ja compilado (AIDD books)
        if md_precompilado.exists():
            print(f"  Usando livro_final.md pre-compilado (sem capitulos individuais)")
            # Usar diretamente o MD existente
            return converter_md_direto(slug, dir_livro, md_precompilado, pdf_path)
        else:
            print(f"  [SKIP] {slug}: nenhum capitulo ou livro_final.md encontrado")
            return False

    print(f"  Capitulos encontrados: {len(caps)}")

    # Montar conteudo completo: introducao + capitulos + conclusao
    partes = []

    # 1. Introducao
    intro_path = dir_livro / "introducao.md"
    if intro_path.exists():
        with open(intro_path, 'r', encoding='utf-8') as f:
            partes.append(f.read())
        print(f"  + Introducao incluida")

    # 2. Capitulos (sanitizar frontmatter interno e adicionar)
    for cap_path in caps:
        with open(cap_path, 'r', encoding='utf-8') as f:
            conteudo = f.read().strip()
        # Remover qualquer frontmatter YAML interno que possa conflitar
        conteudo = re.sub(r'^---\n.*?\n---\n', '', conteudo, flags=re.DOTALL)
        partes.append(conteudo)

    # 3. Conclusao
    conclusao_path = dir_livro / "conclusao.md"
    if conclusao_path.exists():
        with open(conclusao_path, 'r', encoding='utf-8') as f:
            partes.append(f.read().strip())
        print(f"  + Conclusao incluida")

    # Juntar tudo - Typst/Pandoc cuidam das quebras de pagina naturalmente
    # (o template ja insere pagebreak antes de cada h1)
    todo_conteudo = '\n\n'.join(partes)

    # Extrair titulo do sumario_macro.json para metadados
    titulo = slug
    sumario_path = dir_livro / "sumario_macro.json"
    if sumario_path.exists():
        import json
        with open(sumario_path, 'r', encoding='utf-8') as f:
            try:
                sumario = json.load(f)
                titulo = sumario.get('titulo_obra', slug)
            except:
                pass

    # Criar frontmatter YAML completo para o Pandoc
    frontmatter = f"""---
title: "{titulo}"
author: "Heverton Eduardo Peres"
date: "Julho 2026"
lang: pt-BR
---
"""

    # Montar MD final
    md_final = frontmatter + '\n' + todo_conteudo

    # Salvar MD compilado
    md_compilado = dir_livro / "_livro_compilado.md"
    with open(md_compilado, 'w', encoding='utf-8') as f:
        f.write(md_final)

    # Converter para PDF via Pandoc + Typst
    print(f"  Convertendo MD -> PDF (Pandoc + Typst)...")

    try:
        comando = [
            PANDOC,
            str(md_compilado),
            "-o", str(pdf_path),
            "--pdf-engine", TYPST,
            "--template", str(TEMPLATE),
            "--toc",
            "--toc-depth", "3",
            "--number-sections",
            "--from", "markdown-citations",
            "--wrap", "preserve",
            "-V", f"title={titulo}",
            "-V", "author=Heverton Eduardo Peres",
            "-V", "subtitle=",
            "--resource-path", str(dir_livro),
        ]

        resultado = subprocess.run(
            comando,
            capture_output=True, text=True, timeout=180
        )

        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            tamanho_kb = pdf_path.stat().st_size / 1024
            print(f"  [OK] PDF gerado: {pdf_path.name} ({tamanho_kb:.1f} KB)")
            copiar_pdf_com_nome_slug(slug, dir_livro)

            # Limpar temporario
            if md_compilado.exists():
                md_compilado.unlink()

            return True
        else:
            print(f"  [FALHA] PDF nao foi criado")
            if resultado.stderr:
                # Mostrar apenas os ultimos erros relevantes
                erros = resultado.stderr.strip().split('\n')[-5:]
                for err in erros:
                    print(f"  STDERR: {err}")
            return False

    except subprocess.TimeoutExpired:
        print(f"  [ERRO] Timeout - conversao excedeu 180s")
        return False
    except Exception as e:
        print(f"  [ERRO] Falha na conversao: {e}")
        return False


def main():
    slugs_alvo = sys.argv[1:] if len(sys.argv) > 1 else []

    # Verificar pre-requisitos
    for cmd, nome in [(PANDOC, "Pandoc"), (TYPST, "Typst")]:
        if not os.path.exists(cmd):
            print(f"[ERRO] {nome} nao encontrado em: {cmd}")
            sys.exit(1)

    if not TEMPLATE.exists():
        print(f"[ERRO] Template Typst nao encontrado em: {TEMPLATE}")
        sys.exit(1)

    # Verificar se temos slugs validos
    if slugs_alvo:
        slugs = [s for s in SLUGS if s in slugs_alvo]
        if not slugs:
            print(f"Slug(s) nao encontrado(s). Disponiveis: {', '.join(SLUGS)}")
            sys.exit(1)
    else:
        slugs = SLUGS

    print(f"Iniciando compilacao de {len(slugs)} livro(s)...")
    print(f"  Pandoc: {PANDOC}")
    print(f"  Typst: {TYPST}")
    print(f"  Template: {TEMPLATE}")

    sucessos = 0
    falhas = 0

    for slug in slugs:
        if compilar_livro(slug):
            sucessos += 1
        else:
            falhas += 1

    print(f"\n{'='*60}")
    print(f"  RESUMO: {sucessos} OK, {falhas} falha(s)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
