#!/usr/bin/env python3
"""
ORGANIZADOR COMPLETO da pasta output/
1. Remove duplicatas e versoes antigas
2. Corrige nome do autor nos scripts
3. Gera mega-livros por serie
4. Gera ULTRA LIVRO final com todos os livros
"""

import os
import sys
import re
import json
import shutil
import subprocess
import concurrent.futures
from pathlib import Path
from datetime import date

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PANDOC = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc-3.10\pandoc.exe"
TYPST  = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc\typst.exe"
TEMPLATE = Path(__file__).parent / "templates" / "template.typ"

DIR_RAIZ = Path(__file__).parent / "output"

# ══════════════════════════════════════════════════════════════
# DEFINICAO DAS SERIES
# ══════════════════════════════════════════════════════════════

SERIES = {
    "00": ("EITA Method", [("00-eita-metodo", "O Metodo EITA")]),

    "A": ("Segredos Freebuff", [
        ("A1-segredos-freebuff", "Segredos Freebuff"),
        ("A2-segredos-mimocode", "Segredos MimoCode"),
        ("A3-segredos-oh-my-pi", "Segredos Oh My P!"),
        ("A4-segredos-opencode", "Segredos OpenCode"),
        ("A5-opencode-personalizacoes-escondidas", "OpenCode: Personalizacoes Escondidas"),
    ]),

    "B": ("Agentes CLI", [
        ("B1-modelos-avancados-terminal", "Modelos Avancados de Terminal"),
        ("B2-fluxos-profissionais", "Fluxos Profissionais"),
        ("B3-llms-freetiers", "LLMs Free Tiers"),
        ("B4-revolucao-agentes-cli", "Revolucao dos Agentes CLI"),
        ("B5-roteamento-llms-gratuito", "Roteamento de LLMs Gratuito"),
    ]),

    "C": ("AIDD Core", [
        ("C1-transicao-dev-aidd", "Transicao Dev Tradicional para AIDD"),
        ("C2-camada-interface", "Camada Interface"),
        ("C3-camada-harness", "Camada Harness"),
        ("C4-camada-operarios", "Camada Operarios"),
        ("C5-camada-llm-core", "Camada LLM Core"),
    ]),

    "D": ("Application Layers", [
        ("D1-frontend-aidd", "Frontend com AIDD"),
        ("D2-backend-aidd", "Backend com AIDD"),
        ("D3-database-aidd", "Database com AIDD"),
        ("D4-apis-aidd", "APIs com AIDD"),
        ("D5-aplicacao-completa-aidd", "Aplicacao Completa com AIDD"),
    ]),

    "E": ("Seguranca e Governanca", [
        ("E1-seguranca-auth", "Autenticacao e Autorizacao"),
        ("E2-seguranca-cripto", "Criptografia e Protecao de Dados"),
        ("E3-seguranca-owasp", "OWASP e Seguranca"),
        ("E4-seguranca-compliance", "Governanca e Compliance"),
        ("E5-seguranca-redteam", "Red Team"),
    ]),

    "F": ("DevOps e Infraestrutura", [
        ("F1-devops-cicd", "CI/CD"),
        ("F2-devops-docker", "Containerizacao e Docker"),
        ("F3-devops-kubernetes", "Kubernetes"),
        ("F4-devops-iac", "Infraestrutura como Codigo"),
        ("F5-devops-observabilidade", "Observabilidade e Monitoramento"),
    ]),

    "G": ("Testes e Qualidade", [
        ("G1-testes-unitarios", "Testes Unitarios"),
        ("G2-testes-integracao", "Testes de Integracao"),
        ("G3-testes-e2e", "Testes E2E e Performance"),
        ("G4-testes-codereview", "Code Review"),
        ("G5-testes-qualidade", "Qualidade e Divida Tecnica"),
    ]),

    "H": ("Automacao e Robotica", [
        ("H1-automacao-rpa", "RPA"),
        ("H2-automacao-pipeline", "Pipelines de Automacao"),
        ("H3-automacao-iot", "IoT"),
        ("H4-automacao-processos", "Automacao de Processos"),
        ("H5-automacao-lowcode", "Low-Code/No-Code"),
    ]),

    "I": ("Dados e Analytics", [
        ("I1-dados-engenharia", "Engenharia de Dados"),
        ("I2-dados-analytics", "Analytics e BI"),
        ("I3-dados-ml", "Machine Learning"),
        ("I4-dados-streaming", "Stream Processing"),
        ("I5-dados-governanca", "Governanca de Dados"),
    ]),

    "J": ("Fintech", [
        ("J1-fintech-pagamentos", "Pagamentos e Transacoes"),
        ("J2-fintech-regulatorio", "Regulatorio Financeiro"),
        ("J3-fintech-blockchain", "Blockchain e Web3"),
        ("J4-fintech-openbanking", "Open Banking e Open Finance"),
        ("J5-fintech-fraud", "Prevencao a Fraudes"),
    ]),

    "K": ("Mobile", [
        ("K1-mobile-reactnative", "React Native"),
        ("K2-mobile-flutter", "Flutter"),
        ("K3-mobile-ios", "iOS e Swift"),
        ("K4-mobile-android", "Android e Kotlin"),
        ("K5-mobile-multiplataforma", "Multiplataforma"),
    ]),

    "L": ("Cloud", [
        ("L1-cloud-aws", "AWS"),
        ("L2-cloud-azure", "Azure"),
        ("L3-cloud-gcp", "GCP"),
        ("L4-cloud-serverless", "Serverless"),
        ("L5-cloud-multicloud", "Multi-Cloud"),
    ]),

    "M": ("Performance", [
        ("M1-performance-web", "Web Performance"),
        ("M2-performance-api", "API Performance"),
        ("M3-performance-banco", "Database Performance"),
        ("M4-performance-mobile", "Mobile Performance"),
        ("M5-performance-escala", "Escala e Alta Disponibilidade"),
    ]),

    "N": ("Corporativo", [
        ("N1-corporativo-microservicos", "Microservices"),
        ("N2-corporativo-eventos", "Event-Driven Architecture"),
        ("N3-corporativo-legado", "Modernizacao de Legado"),
        ("N4-corporativo-equipes", "Gestao de Equipes AIDD"),
        ("N5-corporativo-governanca", "Governanca Corporativa"),
    ]),
}


def step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def fix_author_in_scripts():
    """Fix Heberton Peres -> Heverton Eduardo Peres in all Python scripts."""
    step("Corrigir nome do autor nos scripts Python")
    
    scripts = [
        "gerar-livros-aidd.py",
        "compilar-para-pdf.py",
        "compilar-mega-camadas.py",
        "compilar-mega-livro.py",
        "compilar-mega-completo.py",
    ]
    
    fixes = 0
    for script_name in scripts:
        path = Path(__file__).parent / script_name
        if not path.exists():
            print(f"  [SKIP] {script_name} nao encontrado")
            continue
        
        content = path.read_text("utf-8")
        old_count = content.count("Heberton Peres")
        if old_count > 0:
            content = content.replace("Heberton Peres", "Heverton Eduardo Peres")
            path.write_text(content, "utf-8")
            fixes += old_count
            print(f"  [FIX] {script_name}: {old_count} ocorrencias corrigidas")
        else:
            print(f"  [OK] {script_name}: ja esta correto")
    
    print(f"\n  Total: {fixes} correcoes em scripts")
    return fixes


def remove_duplicates():
    """
    Remove directories that are duplicates:
    - Old 01-14 books (replaced by C1-C5)
    - Orphan duplicates (without prefix, e.g. segredos-* when A*-segredos-* exists)
    - A-opencode-personalizacoes-escondidas (A5- is the canonical one)
    """
    step("Arquivar versoes antigas e remover duplicatas")
    
    # Create _archive directory for old books
    archive_dir = DIR_RAIZ / "_archive"
    archive_dir.mkdir(exist_ok=True)
    
    # Collect all canonical slugs
    canonical = set()
    for prefix, (serie_name, books) in SERIES.items():
        for slug, label in books:
            canonical.add(slug)
    
    # Also keep known compilations
    canonical.add("C6-mega-livro-completo-aidd")
    canonical.add("00-mega-livro-todos-aidd")
    
    # Move old 01-14 books to _archive
    old_books = [
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
    ]
    for old in old_books:
        old_path = DIR_RAIZ / old
        if old_path.exists():
            dest = archive_dir / old
            if dest.exists():
                shutil.rmtree(dest)
            old_path.rename(dest)
            print(f"  [ARCHIVED] {old} -> _archive/")
    
    # Duplicates to remove (orphan -> canonical mapping)
    dups_to_remove = {
        # Without prefix -> With prefix (Series A)
        "segredos-freebuff": "A1-segredos-freebuff",
        "segredos-mimocode": "A2-segredos-mimocode",
        "segredos-oh-my-pi": "A3-segredos-oh-my-pi",
        "segredos-opencode": "A4-segredos-opencode",
        "A-opencode-personalizacoes-escondidas": "A5-opencode-personalizacoes-escondidas",
        
        # Without prefix -> With prefix (Series B)
        "modelos-avancados-terminal": "B1-modelos-avancados-terminal",
        "fluxos-profissionais": "B2-fluxos-profissionais",
        "llms-freetiers": "B3-llms-freetiers",
        "revolucao-agentes-cli": "B4-revolucao-agentes-cli",
        "roteamento-llms-gratuito": "B5-roteamento-llms-gratuito",
        
        # Old compilations (remove outdated)
        "compilado-completo-aidd-2026-07-30": None,
    }
    
    removed = 0
    kept = 0
    for dup, canonical_slug in dups_to_remove.items():
        dup_path = DIR_RAIZ / dup
        if dup_path.exists():
            size = sum(f.stat().st_size for f in dup_path.rglob('*') if f.is_file()) / 1024
            shutil.rmtree(dup_path)
            print(f"  [REMOVED] {dup} ({size:.0f} KB)")
            removed += 1
        else:
            kept += 1
    
    print(f"\n  Removidos: {removed} | Ja inexistentes: {kept}")


def regenerate_book_pdfs():
    """
    Regenerate all PDFs using compilar-para-pdf.py to fix author name.
    """
    step("Regenerar PDFs com nome do autor corrigido")
    
    # Get all canonical slugs
    all_slugs = []
    for prefix, (serie_name, books) in SERIES.items():
        for slug, label in books:
            all_slugs.append(slug)
    
    # Also regenerate known compilations
    all_slugs.extend(["00-mega-livro-todos-aidd", "C6-mega-livro-completo-aidd"])
    
    # Regenerate each book (parallel, up to 4 at a time)
    success = 0
    failed = 0
    total = len(all_slugs)
    
    def regenerate_one(slug):
        dir_livro = DIR_RAIZ / slug
        if not dir_livro.exists():
            return slug, False, "diretorio nao encontrado"
        
        caps_dir = dir_livro / "capitulos"
        md_path = dir_livro / "livro_final.md"
        
        if not caps_dir.exists() or not md_path.exists():
            return slug, False, "capitulos ou md ausentes"
        
        pdf_path = dir_livro / "livro_final.pdf"
        
        # Get titulo from sumario for Pandoc metadata
        titulo = slug.replace('-', ' ').title()
        sumario_path = dir_livro / "sumario_macro.json"
        if sumario_path.exists():
            try:
                with open(sumario_path, "r", encoding="utf-8") as f:
                    sj = json.load(f)
                    titulo = sj.get("titulo_obra", titulo)
            except:
                pass
        
        cmd = [
            PANDOC, str(md_path), "-o", str(pdf_path),
            "--pdf-engine", TYPST,
            "--template", str(TEMPLATE),
            "--toc", "--toc-depth", "3",
            "--number-sections",
            "--from", "markdown-citations",
            "--wrap", "preserve",
            "-V", f"title={titulo}",
            "-V", "author=Heverton Eduardo Peres",
            "-V", "subtitle=",
            "--resource-path", str(dir_livro),
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if pdf_path.exists() and pdf_path.stat().st_size > 0:
                kb = pdf_path.stat().st_size / 1024
                slug_pdf = dir_livro / f"{slug}.pdf"
                shutil.copy2(pdf_path, slug_pdf)
                return slug, True, f"{kb:.0f} KB"
            else:
                err = result.stderr.strip().split('\n')[-1:]
                return slug, False, f"Falha: {err}"
        except subprocess.TimeoutExpired:
            return slug, False, "Timeout"
        except Exception as e:
            return slug, False, str(e)[:60]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(regenerate_one, slug): slug for slug in all_slugs}
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            slug, ok, msg = future.result()
            if ok:
                success += 1
                print(f"  [{i}/{total}] {slug}: {msg}")
            else:
                failed += 1
                print(f"  [{i}/{total}] {slug}: {msg}")
    
    print(f"\n  PDFs regenerados: {success}/{total} ({failed} falhas)")
    return success, failed


def create_series_megabooks():
    """
    Create a mega-livro for each series.
    """
    step("Criar mega-livros por serie")
    
    hoje = date.today()
    created = []
    
    for prefix in sorted(SERIES.keys()):
        serie_name, books = SERIES[prefix]
        slug_prefix = f"{prefix.upper()}-" if prefix != "00" else "00-"
        
        dir_comp = DIR_RAIZ / f"{slug_prefix}mega-serie-{prefix}"
        if dir_comp.exists():
            shutil.rmtree(dir_comp)
        dir_comp.mkdir(parents=True, exist_ok=True)
        
        # Collect capitulos
        all_caps = []
        cap_counter = 0
        partes = []
        
        for slug, label in books:
            livro_dir = DIR_RAIZ / slug
            caps_dir = livro_dir / "capitulos"
            sumario_path = livro_dir / "sumario_macro.json"
            
            if not caps_dir.exists():
                continue
            
            sumario = {}
            if sumario_path.exists():
                with open(sumario_path, "r", encoding="utf-8") as f:
                    sumario = json.load(f)
            
            caps = sorted(caps_dir.glob("cap_*.md"), 
                         key=lambda p: int(re.search(r'cap_(\d+)', p.stem).group(1)))
            
            parte_caps = []
            for i, cap_path in enumerate(caps):
                cap_counter += 1
                content = cap_path.read_text("utf-8")
                content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                content = re.sub(
                    r'^# Cap[ií]tulo \d+[\s]*[—:–]?[\s]*',
                    f'# Capitulo {cap_counter} - ',
                    content, flags=re.MULTILINE
                )
                
                new_path = dir_comp / "capitulos" / f"cap_{cap_counter}.md"
                new_path.parent.mkdir(exist_ok=True)
                new_path.write_text(content, "utf-8")
                
                # Get original title
                orig_num = int(re.search(r'cap_(\d+)', cap_path.stem).group(1))
                titulo = ""
                if sumario:
                    for p in sumario.get("partes", []):
                        for c in p.get("capitulos", []):
                            if c["capitulo"] == orig_num:
                                titulo = c.get("titulo", "")
                                break
                parte_caps.append({"capitulo": cap_counter, "titulo": titulo or cap_path.stem})
            
            if parte_caps:
                partes.append({
                    "parte": len(partes) + 1,
                    "titulo_parte": f"Serie {prefix}: {serie_name} - {label}",
                    "capitulos": parte_caps
                })
        
        titulo = f"Serie {prefix}: {serie_name} - Colecao Completa"
        subtitulo = f"{len(books)} livros | {cap_counter} capitulos"
        
        livro = f"# {titulo}\n\n*{subtitulo}*\n\n"
        livro += f"## Sumario\n\n"
        for p in partes:
            livro += f"- **{p['titulo_parte']}**\n"
            for c in p['capitulos']:
                livro += f"  - Capitulo {c['capitulo']}: {c['titulo']}\n"
        livro += "\n\n"
        for p in partes:
            livro += f"\n\n# {p['titulo_parte']}\n"
            for c in p['capitulos']:
                cp = dir_comp / "capitulos" / f"cap_{c['capitulo']}.md"
                if cp.exists():
                    livro += "\n" + cp.read_text("utf-8") + "\n"
        livro += f"\n\n*Produzido pela Fabrica Agente de Livros em {hoje}.*\n"
        
        md_path = dir_comp / "livro_final.md"
        md_path.write_text(livro, "utf-8")
        
        # Save sumario_macro.json
        sumario_json = {
            "titulo_obra": titulo,
            "subtitulo": subtitulo,
            "slug": f"{slug_prefix}mega-serie-{prefix}",
            "introducao": f"Serie {prefix}: {serie_name} completa.",
            "conclusao": f"Todos os {len(books)} livros da serie foram compilados.",
            "partes": partes
        }
        sumario_path = dir_comp / "sumario_macro.json"
        with open(sumario_path, "w", encoding="utf-8") as f:
            json.dump(sumario_json, f, indent=2, ensure_ascii=False)
        
        # Generate PDF
        pdf_path = dir_comp / "livro_final.pdf"
        cmd = [
            PANDOC, str(md_path), "-o", str(pdf_path),
            "--pdf-engine", TYPST,
            "--template", str(TEMPLATE),
            "--toc", "--toc-depth", "3",
            "--number-sections",
            "--from", "markdown-citations",
            "--wrap", "preserve",
            "-V", f"title={titulo}",
            "-V", "author=Heverton Eduardo Peres",
            "-V", "subtitle=",
            "--resource-path", str(dir_comp),
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if pdf_path.exists():
                slug_pdf = dir_comp / f"{slug_prefix}mega-serie-{prefix}.pdf"
                shutil.copy2(pdf_path, slug_pdf)
                mb = pdf_path.stat().st_size / (1024*1024)
                print(f"  [OK] Serie {prefix}: {mb:.1f} MB | {cap_counter} caps")
                created.append((prefix, mb))
        except Exception as e:
            print(f"  [FALHA] Serie {prefix}: {e}")
    
    print(f"\n  Mega-livros criados: {len(created)}/{len(SERIES)}")
    return created


def create_ultra_livro():
    """
    Create the ULTRA LIVRO: all series compiled in order.
    """
    step("Criar ULTRA LIVRO com todos os livros")
    
    hoje = date.today()
    dir_ultra = DIR_RAIZ / f"ultra-livro-completo-aidd-{hoje.isoformat()}"
    if dir_ultra.exists():
        shutil.rmtree(dir_ultra)
    dir_ultra.mkdir(parents=True, exist_ok=True)
    
    all_parts = []
    cap_counter = 0
    
    for prefix in sorted(SERIES.keys()):
        serie_name, books = SERIES[prefix]
        
        for slug, label in books:
            livro_dir = DIR_RAIZ / slug
            caps_dir = livro_dir / "capitulos"
            sumario_path = livro_dir / "sumario_macro.json"
            
            if not caps_dir.exists():
                continue
            
            sumario = {}
            if sumario_path.exists():
                with open(sumario_path, "r", encoding="utf-8") as f:
                    sumario = json.load(f)
            
            caps = sorted(caps_dir.glob("cap_*.md"),
                         key=lambda p: int(re.search(r'cap_(\d+)', p.stem).group(1)))
            
            parte_caps = []
            for cap_path in caps:
                cap_counter += 1
                content = cap_path.read_text("utf-8")
                content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                content = re.sub(
                    r'^# Cap[ií]tulo \d+[\s]*[—:–]?[\s]*',
                    f'# Capitulo {cap_counter} - ',
                    content, flags=re.MULTILINE
                )
                
                new_path = dir_ultra / "capitulos" / f"cap_{cap_counter}.md"
                new_path.parent.mkdir(exist_ok=True)
                new_path.write_text(content, "utf-8")
                
                orig_num = int(re.search(r'cap_(\d+)', cap_path.stem).group(1))
                titulo = ""
                if sumario:
                    for p in sumario.get("partes", []):
                        for c in p.get("capitulos", []):
                            if c["capitulo"] == orig_num:
                                titulo = c.get("titulo", "")
                                break
                parte_caps.append({"capitulo": cap_counter, "titulo": titulo or cap_path.stem})
            
            if parte_caps:
                all_parts.append({
                    "parte": len(all_parts) + 1,
                    "titulo_parte": f"Serie {prefix}: {serie_name} - {label}",
                    "capitulos": parte_caps
                })
    
    total_livros = sum(len(books) for _, (_, books) in SERIES.items())
    
    titulo = "ULTRA LIVRO: AI-Driven Development - A Colecao Completa do Engenheiro AIDD"
    subtitulo = f"{total_livros} livros | {len(all_parts)} partes | {cap_counter} capitulos"
    
    introducao = (
        f"Esta obra definitiva reune todos os {total_livros} livros produzidos pela "
        f"Fabrica Agente de Livros sobre AI-Driven Development, organizados em "
        f"{len(all_parts)} partes e {cap_counter} capitulos. "
        f"Dos fundamentos do metodo EITA ate as series especializadas de Seguranca, "
        f"DevOps, Testes, Automacao, Dados, Fintech, Mobile, Cloud, Performance e "
        f"Corporativo - este e o guia mais completo sobre AIDD ja produzido."
    )
    conclusao = (
        f"O ecossistema AIDD e vasto e esta em constante evolucao. Este ULTRA LIVRO "
        f"compila {total_livros} obras em {cap_counter} capitulos, cobrindo todas as areas "
        f"que um engenheiro AIDD precisa dominar. Cada obra segue o rigor do metodo "
        f"EITA-V2, garantindo aprendizado profundo e aplicavel imediatamente."
    )
    
    livro = f"""# {titulo}

*{subtitulo}*

## Prefacio

{introducao}

### Sobre este ULTRA LIVRO

- **{total_livros} livros** em uma unica obra
- **{cap_counter} capitulos** em **{len(all_parts)} partes**
- Gerado em **{hoje}**
- Autor: **Heverton Eduardo Peres**

### Organizacao

Este ULTRA LIVRO esta organizado por series, na ordem:
"""
    for prefix in sorted(SERIES.keys()):
        serie_name, books = SERIES[prefix]
        livro += f"- **Serie {prefix}**: {serie_name} ({len(books)} livros)\n"
    
    livro += "\n## Sumario\n\n"
    for p in all_parts:
        livro += f"- **{p['titulo_parte']}**\n"
        for c in p['capitulos']:
            livro += f"  - Capitulo {c['capitulo']}: {c['titulo']}\n"
    
    livro += "\n"
    for p in all_parts:
        livro += f"\n# {p['titulo_parte']}\n"
        for c in p['capitulos']:
            cp = dir_ultra / "capitulos" / f"cap_{c['capitulo']}.md"
            if cp.exists():
                livro += "\n" + cp.read_text("utf-8") + "\n"
    
    livro += f"""\n\n# Conclusao

{conclusao}

*Ultra Livro produzido pela Fabrica Agente de Livros em {hoje}.*
"""
    
    md_path = dir_ultra / "livro_final.md"
    md_path.write_text(livro, "utf-8")
    print(f"  MD: {md_path.stat().st_size/1024:.0f} KB ({md_path.stat().st_size/(1024*1024):.1f} MB)")
    
    # Generate PDF
    pdf_path = dir_ultra / "livro_final.pdf"
    cmd = [
        PANDOC, str(md_path), "-o", str(pdf_path),
        "--pdf-engine", TYPST,
        "--template", str(TEMPLATE),
        "--toc", "--toc-depth", "3",
        "--number-sections",
        "--from", "markdown-citations",
        "--wrap", "preserve",
        "-V", f"title={titulo}",
        "-V", "author=Heverton Eduardo Peres",
        "-V", "subtitle=",
        "--resource-path", str(dir_ultra),
        "-V", f"date={hoje}",
    ]
    
    print(f"  Gerando PDF via Pandoc+Typst...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            slug_pdf = dir_ultra / f"ultra-livro-completo-aidd-{hoje.isoformat()}.pdf"
            shutil.copy2(pdf_path, slug_pdf)
            mb = pdf_path.stat().st_size / (1024*1024)
            print(f"  [OK] ULTRA LIVRO PDF: {mb:.2f} MB")
            print(f"  [OK] Capitulos: {cap_counter}")
            return True, mb
        else:
            print(f"  [FALHA] PDF nao criado!")
            if result.stderr:
                for err in result.stderr.strip().split('\n')[-5:]:
                    print(f"  STDERR: {err}")
            return False, 0
    except subprocess.TimeoutExpired:
        print(f"  [ERRO] Timeout! O arquivo MD tem {md_path.stat().st_size/(1024*1024):.1f} MB")
        return False, 0
    except Exception as e:
        print(f"  [ERRO] {e}")
        return False, 0


def main():
    print("=" * 60)
    print("  ORGANIZADOR COMPLETO DA PASTA OUTPUT")
    print("=" * 60)
    print()
    print("  Este script vai:")
    print("  1. Remover duplicatas e versoes antigas")
    print("  2. Corrigir nome do autor em todos os scripts")
    print("  3. Regenerar PDFs com autor correto")
    print("  4. Criar mega-livros por serie")
    print("  5. Criar ULTRA LIVRO final")
    print()
    
    # Step 1: Fix author in scripts
    fix_author_in_scripts()
    
    # Step 2: Remove duplicates
    remove_duplicates()
    
    # Step 3: Regenerate PDFs
    regenerate_book_pdfs()
    
    # Step 4: Create series mega-books
    create_series_megabooks()
    
    # Step 5: Create ULTRA LIVRO
    create_ultra_livro()
    
    print()
    print("=" * 60)
    print("  ORGANIZACAO CONCLUIDA!")
    print("=" * 60)


if __name__ == "__main__":
    main()
