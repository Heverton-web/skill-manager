#!/usr/bin/env python3
"""
Compila todos os livros AIDD (excluindo mega-livro existente) em um unico
mega-livro completo — seguindo o fluxo da skill compilador-mega-livro.

Fluxo:
  1. Criar pasta output/<slug>/ com rm -rf + mkdir -p
  2. Ler e unificar sumarios macro de todos os slugs
  3. Salvar sumario_macro.json unificado
  4. Concatenar e renumerar capitulos sequencialmente
  5. Gerar prefacio + sumario + conclusao
  6. Montar livro_final.md
  7. Gerar PDF via Pandoc+Typst
  8. Validar tudo

Uso: python compilar-mega-livro.py
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from pdf_typst import executar as _executar_typst

# Caminhos dos executaveis (duplicados de compilar-para-pdf.py intencionalmente
# pois o nome com hifen impede importacao direta via Python)
PANDOC = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc-3.10\pandoc.exe"
TYPST = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc\typst.exe"
TEMPLATE = Path(__file__).parent / "templates" / "template.typ"

# Verificar pre-requisitos
for cmd, nome in [(PANDOC, "Pandoc"), (TYPST, "Typst")]:
    if not os.path.exists(cmd):
        print(f"[ERRO] {nome} nao encontrado em: {cmd}")
        print(f"  Use o script compilar-para-pdf.py para diagnosticar.")
        sys.exit(1)
if not TEMPLATE.exists():
    print(f"[ERRO] Template Typst nao encontrado em: {TEMPLATE}")
    sys.exit(1)

DIR_RAIZ = Path(__file__).parent / "output"
DIR_PROJETO = Path(__file__).parent

# Todos os slugs AIDD exceto o mega-livro existente
SLUGS_AIDD = [
    "01-aidd-ai-driven-development",
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
]

SLUG_COMPILADO = f"compilado-completo-aidd-{date.today().isoformat()}"


def step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def coletar_sumario(slug):
    """Le o sumario_macro.json de um slug."""
    path = DIR_RAIZ / slug / "sumario_macro.json"
    if not path.exists():
        print(f"  [AVISO] sumario_macro.json nao encontrado para {slug}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extrair_frontmatter(texto):
    """Remove YAML frontmatter do markdown."""
    return re.sub(r'^---\n.*?\n---\n', '', texto, flags=re.DOTALL)


def renumerar_titulo_capitulo(conteudo, novo_numero):
    """Renumera o titulo do capitulo no markdown."""
    # Tenta varios padroes: "# Capitulo N — Titulo", "# Capitulo N: Titulo", "# Capitulo N Titulo"
    conteudo = re.sub(
        r'^# Cap[ií]tulo \d+[\s]*[—:–]?[\s]*',
        f'# Capítulo {novo_numero} — ',
        conteudo,
        flags=re.MULTILINE
    )
    return conteudo


def main():
    step(f"Passo 1: Criar pasta {SLUG_COMPILADO} (limpa)")

    dir_compilado = DIR_RAIZ / SLUG_COMPILADO
    dir_caps = dir_compilado / "capitulos"

    # Garantir pasta limpa
    if dir_compilado.exists():
        shutil.rmtree(dir_compilado)
    dir_caps.mkdir(parents=True, exist_ok=True)
    print(f"  Pasta criada: {dir_compilado}")

    # ---

    step("Passo 2: Ler e unificar sumarios macro")

    sumarios = []
    for slug in SLUGS_AIDD:
        s = coletar_sumario(slug)
        if s:
            sumarios.append((slug, s))
            print(f"  + {slug}: {len(s.get('partes', []))} parte(s)")

    if not sumarios:
        print("[ERRO] Nenhum sumario encontrado!")
        sys.exit(1)

    # Construir sumario unificado
    titulo_obra = f"Guia Completo de AI-Driven Development"
    subtitulo = "Compilado dos Livros da Fábrica Agêntica de Livros"

    total_livros = len(sumarios)

    partes_unificadas = []
    contador_global = 0

    for idx, (slug, sumario) in enumerate(sumarios):
        # Nome da parte = titulo do livro
        titulo_parte = sumario.get("titulo_obra", slug)

        # Se tiver subtitulo, incluir
        sub = sumario.get("subtitulo", "")
        if sub and sub != slug:
            titulo_parte = f"{titulo_parte}: {sub}"

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

    sumario_unificado = {
        "titulo_obra": titulo_obra,
        "subtitulo": subtitulo,
        "slug_compilado": SLUG_COMPILADO,
        "data_compilacao": date.today().isoformat(),
        "introducao": f"Este compilado reúne {total_livros} livros da Fábrica Agêntica de Livros, "
                       f"totalizando {contador_global} capítulos que abrangem desde fundamentos "
                       f"conceituais até padrões avançados de orquestração de agentes de IA.",
        "conclusao": "Ao longo desta obra completa, exploramos as múltiplas facetas do paradigma "
                     "AI-Driven Development. O conhecimento aqui consolidado forma uma base sólida "
                     "para qualquer profissional que deseja dominar a arte de orquestrar agentes de IA.",
        "partes": partes_unificadas
    }

    # Validar contagem vs arquivos reais
    for slug in SLUGS_AIDD:
        caps_reais = len(list((DIR_RAIZ / slug / "capitulos").glob("cap_*.md")))
        caps_sumario = sum(
            len(p.get("capitulos", []))
            for p in coletar_sumario(slug).get("partes", [])
        )
        if caps_reais != caps_sumario:
            print(f"  [AVISO] {slug}: sumario lista {caps_sumario} caps, mas ha {caps_reais} arquivos")

    print(f"  Total de livros: {total_livros}")
    print(f"  Total de capitulos: {contador_global}")
    print(f"  Total de partes: {len(partes_unificadas)}")

    # ---

    step("Passo 3: Salvar sumario_macro.json unificado")

    sumario_path = dir_compilado / "sumario_macro.json"
    with open(sumario_path, "w", encoding="utf-8") as f:
        json.dump(sumario_unificado, f, indent=2, ensure_ascii=False)
    print(f"  Salvo: {sumario_path}")

    # ---

    step("Passo 4: Concatenar e renumerar capitulos")

    capitulos_concatenados = []
    contador_gravado = 0

    for parte in partes_unificadas:
        for cap_info in parte["capitulos"]:
            contador_gravado += 1
            slug_origem = cap_info["slug_origem"]
            cap_original = cap_info["cap_original"]

            cap_path = DIR_RAIZ / slug_origem / "capitulos" / f"cap_{cap_original}.md"
            if not cap_path.exists():
                # Tentar paths alternativos
                cap_path = DIR_RAIZ / slug_origem / "capitulos" / f"cap_{cap_original:02d}.md"
                if not cap_path.exists():
                    print(f"  [AVISO] Capitulo nao encontrado: {slug_origem}/cap_{cap_original}.md")
                    continue

            with open(cap_path, "r", encoding="utf-8") as f:
                conteudo = f.read()

            # Remover frontmatter
            conteudo = extrair_frontmatter(conteudo)

            # Renumerar titulo do capitulo
            conteudo = renumerar_titulo_capitulo(conteudo, contador_gravado)

            # Salvar capitulo renumerado individualmente
            cap_destino = dir_caps / f"cap_{contador_gravado}.md"
            with open(cap_destino, "w", encoding="utf-8") as f:
                f.write(conteudo)

            capitulos_concatenados.append(conteudo)

    print(f"  Capitulos processados: {contador_gravado}")

    # ---

    step("Passo 5: Gerar elementos extrusos")

    # Prefacio
    prefacio_texto = f"""# Prefácio

{sumario_unificado['introducao']}

## Sobre esta Compilação

- **{total_livros} livros** reunidos em uma única obra
- **{contador_global} capítulos** organizados em **{len(partes_unificadas)} partes**
- Compilado gerado em **{date.today().strftime('%d/%m/%Y')}**

Cada parte corresponde a um livro original, mantendo sua identidade e estrutura interna.
Os capítulos foram renumerados sequencialmente para facilitar a navegação e referência cruzada.

## Como Navegar

Utilize o sumário abaixo para localizar rapidamente os temas de seu interesse.
Cada parte cobre um aspecto fundamental do ecossistema Freebuff:
conceitos, ferramentas, técnicas avançadas e padrões de orquestração.
"""

    # Sumario dinamico
    sumario_texto = "# Sumário\n\n"
    for parte in partes_unificadas:
        sumario_texto += f"- **Parte {parte['parte']} — {parte['titulo_parte']}**\n"
        for cap in parte["capitulos"]:
            sumario_texto += f"  - Capítulo {cap['capitulo']}: {cap['titulo']}\n"

    # Conclusao
    conclusao_texto = f"""# Conclusão

{sumario_unificado['conclusao']}

---

*Compilado gerado automaticamente pela Fábrica Agêntica de Livros em {date.today().strftime('%d/%m/%Y')}.*
"""

    # ---

    step("Passo 6: Montar livro_final.md")

    # Montar corpo completo
    corpo_partes = []
    for parte in partes_unificadas:
        # Titulo da parte
        corpo_partes.append(f"\n\n---\n\n# Parte {parte['parte']} — {parte['titulo_parte']}\n")

        # Coletar capitulos desta parte
        for cap in parte["capitulos"]:
            idx = cap["capitulo"]
            cap_path = dir_caps / f"cap_{idx}.md"
            if cap_path.exists():
                with open(cap_path, "r", encoding="utf-8") as f:
                    corpo_partes.append(f.read().strip())

    corpo_texto = "\n\n".join(corpo_partes)

    livro_final = f"""# {titulo_obra}

*{subtitulo}*

{prefacio_texto}

{sumario_texto}

---

{corpo_texto}

---

{conclusao_texto}
"""

    md_path = dir_compilado / "livro_final.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(livro_final)

    print(f"  livro_final.md salvo: {md_path}")
    print(f"  Tamanho: {md_path.stat().st_size / 1024:.1f} KB")

    # ---

    step("Passo 7: Gerar PDF via Pandoc+Typst")

    pdf_path = dir_compilado / "livro_final.pdf"

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
            "-V", f"title={titulo_obra}",
            "-V", "author=Heverton Eduardo Peres",
            "-V", "subtitle=",
            "--resource-path", str(dir_compilado),
            "-V", f"date={date.today().strftime('%d/%m/%Y')}",
        ]

        print(f"  Executando Pandoc+Typst (timeout: 600s)...")
        resultado = _executar_typst(comando, pdf_path, dir_compilado, TYPST,
                                    timeout=600)

        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            tamanho_kb = pdf_path.stat().st_size / 1024
            tamanho_mb = pdf_path.stat().st_size / (1024 * 1024)
            print(f"  [OK] PDF gerado: {pdf_path.name} ({tamanho_mb:.1f} MB / {tamanho_kb:.0f} KB)")

            # Copiar com nome do slug
            slug_pdf = dir_compilado / f"{SLUG_COMPILADO}.pdf"
            shutil.copy2(pdf_path, slug_pdf)
            print(f"  [OK] PDF copiado: {slug_pdf.name}")
        else:
            print(f"  [FALHA] PDF nao foi criado!")
            if resultado.stderr:
                erros = resultado.stderr.strip().split('\n')[-10:]
                for err in erros:
                    print(f"  STDERR: {err}")
            sys.exit(1)

    except subprocess.TimeoutExpired:
        print(f"  [ERRO] Timeout! Pandoc excedeu 600s")
        sys.exit(1)
    except Exception as e:
        print(f"  [ERRO] Excecao: {e}")
        sys.exit(1)

    # ---

    step("Passo 8: Validacao final")

    erros_validacao = []

    # Verificar existencia
    checks = {
        "livro_final.md": dir_compilado / "livro_final.md",
        "sumario_macro.json": dir_compilado / "sumario_macro.json",
        "livro_final.pdf": dir_compilado / "livro_final.pdf",
        f"{SLUG_COMPILADO}.pdf": dir_compilado / f"{SLUG_COMPILADO}.pdf",
    }

    for nome, path in checks.items():
        if path.exists() and path.stat().st_size > 0:
            size = path.stat().st_size / 1024
            print(f"  [OK] {nome}: {size:.1f} KB")
        else:
            print(f"  [FALHA] {nome}: AUSENTE ou VAZIO")
            erros_validacao.append(nome)

    # Verificar capitulos individuais
    caps_gerados = sorted(dir_caps.glob("cap_*.md"))
    quant_caps = len(caps_gerados)
    print(f"  [{'OK' if quant_caps == contador_global else 'FALHA'}] Capitulos individuais: {quant_caps} de {contador_global} esperados")
    if quant_caps != contador_global:
        erros_validacao.append(f"Capitulos: {quant_caps} vs {contador_global} esperados")

    # Verificar numeracao sem saltos
    numeros = sorted([
        int(re.search(r'cap_(\d+)', p.stem).group(1))
        for p in caps_gerados
    ])
    if numeros and numeros == list(range(1, len(numeros) + 1)):
        print(f"  [OK] Numeracao sequencial: 1 a {len(numeros)} sem saltos")
    else:
        print(f"  [FALHA] Numeracao com falhas!")
        erros_validacao.append("Numeracao com saltos")

    # ---

    step("RELATORIO FINAL")

    pdf_size = f"{pdf_path.stat().st_size / (1024*1024):.1f}" if pdf_path.exists() else "0"

    relatorio = f"""
{'='*60}
  COMPILACAO CONCLUIDA
{'='*60}

  Pasta:        output/{SLUG_COMPILADO}/
  Slug:         {SLUG_COMPILADO}
  Livros:       {total_livros}
  Capitulos:    {contador_global}
  PDF:          {SLUG_COMPILADO}.pdf ({pdf_size} MB)
  Markdown:     livro_final.md
  Sumario:      sumario_macro.json
  Numeracao:    1 a {contador_global} {'[OK]' if not any('saltos' in e for e in erros_validacao) else '[FALHA]'}
  Status:       {'OK' if not erros_validacao else 'FALHA: ' + ', '.join(erros_validacao)}

  Arquivos na pasta:
    - output/{SLUG_COMPILADO}/livro_final.pdf
    - output/{SLUG_COMPILADO}/{SLUG_COMPILADO}.pdf
    - output/{SLUG_COMPILADO}/livro_final.md
    - output/{SLUG_COMPILADO}/sumario_macro.json
    - output/{SLUG_COMPILADO}/capitulos/ (cap_1.md a cap_{contador_global}.md)
"""

    print(relatorio)

    if erros_validacao:
        sys.exit(1)
    else:
        print("  [OK] Compilacao validada com sucesso!")


if __name__ == "__main__":
    main()
