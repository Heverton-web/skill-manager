#!/usr/bin/env python3
"""
Compila os livros da Fábrica em um MEGA-LIVRO único.

Por padrão compila TODOS os livros em output/ (cada pasta com
sumario_macro.json + capitulos/), renumerando os capítulos sequencialmente
e gerando um único PDF com Pandoc+Typst.

Cobre as 5 produções:
  - P:     Perfumaria (P1-P5, 50 livros)
  - W:     Web Fullstack (W1-W5, 50 livros)
  - IA:    IA e Agentes (IA1-IA5, 50 livros)
  - STACK: Stack Fullstack (FE/BE/BD/AP/DV, 50 livros)
  - AIDD:  AI-Driven Development (ai-driven-development)

Uso:
  python compilar-mega-total.py                    # todos os livros
  python compilar-mega-total.py --producao P       # só Perfumaria
  python compilar-mega-total.py --producao STACK   # só Stack Fullstack
"""

import os
import re
import sys
import json
import time
import stat
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

# Pastas que NÃO são livros (megas já compilados ou auxiliares)
EXCLUIR_PREFIXOS = (
    "mega-", "compilado-", "07-mega-", "00-mega-",
)
EXCLUIR_SLUGS = {"mega-livro-todos-aidd"}

# ── PRODUÇÕES (filtro opcional por prefixo) ───────────────────
PRODUCOES = {
    "P": {
        "nome": "Perfumaria e Fragrâncias",
        "slug": "perfumaria",
        "regex": r"^P\d-",
        "descricao": "Fundamentos da perfumaria, universo árabe e oriental, sazonalidade, aplicação e cuidado, e psicologia dos aromas.",
    },
    "W": {
        "nome": "Desenvolvimento Web Fullstack",
        "slug": "web-fullstack",
        "regex": r"^W\d-",
        "descricao": "Fundamentos da web, frontend moderno, backend, bancos de dados, DevOps e carreira fullstack.",
    },
    "IA": {
        "nome": "IA e Agentes Fullstack",
        "slug": "ia-agentes",
        "regex": r"^IA\d-",
        "descricao": "Arquitetura de agentes, ecossistema LLM, engenharia guiada por agentes, automação com IA e projetos práticos.",
    },
    "STACK": {
        "nome": "Stack Fullstack",
        "slug": "stack-fullstack",
        "regex": r"^(FE|BE|BD|AP|DV)-",
        "descricao": "Frontend, backend, bancos de dados, APIs e DevOps — a stack completa do desenvolvimento web.",
    },
    "AIDD": {
        "nome": "Série AIDD — AI-Driven Development",
        "slug": "aidd",
        "regex": r"^ai-driven-development$",
        "descricao": "A metodologia EITA e a engenharia de software guiada por agentes de IA.",
    },
}


def step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def limpar_pasta(path):
    """Remove recursivamente com tolerância a falhas transientes no Windows.

    Contorna o WinError 145 (pasta não vazia) e PermissionError de arquivos
    read-only, comuns quando um processo anterior foi interrompido no meio
    da criação da pasta (ex.: pipe fechado, timeout, antivírus/indexador).
    """
    if not path.exists():
        return True
    for tentativa in range(3):
        try:
            shutil.rmtree(path)
            return True
        except OSError:
            # Marcar arquivos como graváveis (causa comum de PermissionError)
            for p in path.rglob("*"):
                try:
                    if p.is_file():
                        p.chmod(stat.S_IWRITE)
                except OSError:
                    pass
            print(f"  [AVISO] rmtree falhou (tentativa {tentativa+1}/3), aguardando...")
            time.sleep(1)
    return False


def descobrir_livros(producao=None):
    """Descobre livros em output/ (pasta com sumario_macro.json + capitulos).

    Se ``producao`` for informado (chave de PRODUCOES), filtra pelos slugs
    que casam com o regex da produção. Caso contrário, retorna todos.
    """
    padrao = None
    if producao:
        if producao not in PRODUCOES:
            print(f"[ERRO] Produção desconhecida: {producao}")
            print(f"  Disponíveis: {', '.join(PRODUCOES.keys())}")
            sys.exit(1)
        padrao = re.compile(PRODUCOES[producao]["regex"])

    livros = []
    for d in sorted(DIR_RAIZ.iterdir()):
        if not d.is_dir():
            continue
        nome = d.name
        if nome in EXCLUIR_SLUGS or nome.startswith(EXCLUIR_PREFIXOS):
            continue
        if not (d / "sumario_macro.json").exists():
            continue
        caps = list((d / "capitulos").glob("cap_*.md")) if (d / "capitulos").exists() else []
        if not caps:
            # Livros antigos podem ter apenas livro_final.md (fallback)
            if not (d / "livro_final.md").exists():
                continue
        if padrao and not padrao.match(nome):
            continue
        livros.append(nome)
    return livros


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


def num_capitulo(valor):
    """Converte o número do capítulo para int com segurança (pode vir como str no sumário)."""
    try:
        return int(valor)
    except (TypeError, ValueError):
        return 0


def main():
    hoje = date.today()

    # ── ARGUMENTOS (filtro opcional por produção) ──────────────
    producao = None
    args = sys.argv[1:]
    if args:
        if args[0] == "--producao" and len(args) >= 2:
            producao = args[1].upper()
        else:
            print(f"[ERRO] Argumento inválido: {args}")
            print("  Uso: python compilar-mega-total.py [--producao P|W|IA|STACK|AIDD]")
            sys.exit(1)

    # Configuração da produção (ou total)
    if producao:
        if producao not in PRODUCOES:
            print(f"[ERRO] Produção desconhecida: {producao}")
            print(f"  Disponíveis: {', '.join(PRODUCOES.keys())}")
            sys.exit(1)
        cfg = PRODUCOES[producao]
        SLUG_COMPILADO = f"mega-livro-{cfg['slug']}-{hoje.isoformat()}"
        titulo_base = cfg["nome"] + " — A Coleção Completa"
    else:
        cfg = None
        SLUG_COMPILADO = f"mega-livro-total-{hoje.isoformat()}"
        titulo_base = "A Biblioteca Completa da Fábrica Agêntica de Livros"

    step(f"Criar pasta {SLUG_COMPILADO} (limpa)")
    dir_compilado = DIR_RAIZ / SLUG_COMPILADO
    dir_caps = dir_compilado / "capitulos"
    if dir_compilado.exists():
        if not limpar_pasta(dir_compilado):
            print(f"[ERRO] Não foi possível limpar {dir_compilado}. Feche arquivos abertos e tente novamente.")
            sys.exit(1)
    dir_caps.mkdir(parents=True, exist_ok=True)
    print(f"  Pasta: {dir_compilado}")

    # ── DESCUBRIR LIVROS ──────────────────────────────────────

    step("Descobrir livros no output/")

    slugs = descobrir_livros(producao)
    if not slugs:
        print("[ERRO] Nenhum livro encontrado em output/ para esta produção!")
        sys.exit(1)

    print(f"  Livros encontrados: {len(slugs)}")

    # ── LER SUMÁRIOS ──────────────────────────────────────────

    step("Ler sumários dos livros")

    sumarios = []
    for slug in slugs:
        s = coletar_sumario(slug)
        if s:
            qtd = sum(len(p.get("capitulos", [])) for p in s.get("partes", []))
            sumarios.append((slug, s))
            print(f"  + {slug}: {qtd} caps")
        else:
            print(f"  [AVISO] {slug}: sem sumario_macro.json (sera ignorado)")

    if not sumarios:
        print("[ERRO] Nenhum sumario encontrado!")
        sys.exit(1)

    # ── CONSTRUIR SUMÁRIO UNIFICADO ───────────────────────────

    step("Construir sumário unificado")

    subtitulo = (
        f"{len(sumarios)} Livros | {sum(len(p.get('capitulos', [])) for _, p in sumarios)} Capítulos"
    )

    partes_unificadas = []
    contador_global = 0

    for idx, (slug, sumario) in enumerate(sumarios):
        titulo_parte = sumario.get("titulo_obra", slug)
        sub = sumario.get("subtitulo", "")
        if sub and sub != slug and sub != titulo_parte:
            titulo_parte = f"{titulo_parte}: {sub}"

        capitulos_parte = []
        for parte in sumario.get("partes", []):
            for cap in parte.get("capitulos", []):
                contador_global += 1
                capitulos_parte.append({
                    "capitulo": contador_global,
                    "titulo": cap.get("titulo", ""),
                    "slug_origem": slug,
                    "cap_original": num_capitulo(cap.get("capitulo", 0))
                })

        if capitulos_parte:
            partes_unificadas.append({
                "parte": idx + 1,
                "titulo_parte": titulo_parte,
                "capitulos": capitulos_parte
            })

    total_caps = contador_global

    if cfg:
        introducao = (
            f"Esta mega-obra reúne a totalidade dos {len(sumarios)} livros da série "
            f"**{cfg['nome']}** produzidos pela Fábrica Agêntica de Livros. {cfg['descricao']}\\n\\n"
            f"Organizado em {len(partes_unificadas)} partes temáticas, com {total_caps} capítulos, "
            f"este volume é a referência definitiva para quem deseja dominar esta área com "
            f"profundidade e método."
        )
        conclusao = (
            f"Os {len(sumarios)} livros compilados neste volume da série {cfg['nome']} "
            f"representam um acervo completo e coerente. Todos seguem o rigor do método "
            f"EITA-V2 (Explica, Ilustra, Técnica, Aplica), garantindo ao leitor não apenas "
            f"compreensão conceitual, mas aplicação imediata no seu dia a dia.\\n\\n"
            f"Quem dominar estas {len(sumarios)} obras estará preparado para atuar com "
            f"excelência em qualquer frente desta área."
        )
    else:
        introducao = (
            f"Esta mega-obra reúne a totalidade dos {len(sumarios)} livros produzidos pela "
            f"Fábrica Agêntica de Livros: perfumaria e fragrâncias, desenvolvimento web fullstack, "
            f"IA e agentes de software, stack completa (frontend, backend, bancos de dados, APIs e "
            f"DevOps) e a série AI-Driven Development.\\n\\n"
            f"Organizado em {len(partes_unificadas)} partes temáticas, com {total_caps} capítulos, "
            f"este volume é a referência definitiva para quem deseja dominar arte, tecnologia e "
            f"engenharia de software."
        )
        conclusao = (
            f"Os {len(sumarios)} livros compilados neste volume representam um acervo singular: "
            f"do conhecimento sensorial da perfumaria à engenharia de software moderna. "
            f"Todos seguem o rigor do método EITA-V2 (Explica, Ilustra, Técnica, Aplica), "
            f"garantindo ao leitor não apenas compreensão conceitual, mas aplicação imediata "
            f"no seu dia a dia.\\n\\n"
            f"Quem dominar estas {len(sumarios)} áreas estará preparado para atuar com excelência "
            f"em qualquer frente — do frasco ao código, do produto à infraestrutura."
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
    print(f"  Capítulos: {total_caps}")
    print(f"  Partes: {len(partes_unificadas)}")

    # ── SALVAR SUMÁRIO ────────────────────────────────────────

    step("Salvar sumario_macro.json")
    sumario_path = dir_compilado / "sumario_macro.json"
    with open(sumario_path, "w", encoding="utf-8") as f:
        json.dump(sumario_unificado, f, indent=2, ensure_ascii=False)
    print(f"  Salvo: {sumario_path}")

    # ── CONCATENAR E RENUMERAR ────────────────────────────────

    step("Concatenar e renumerar capítulos")

    # Avisar livros descobertos que nao contribuiram com capitulos
    slugs_com_caps = set()
    for parte in partes_unificadas:
        slugs_com_caps.update(c["slug_origem"] for c in parte["capitulos"])
    for slug in slugs:
        if slug not in slugs_com_caps:
            print(f"  [AVISO] {slug}: descoberto mas sem capitulos no sumario (ignorado)")

    contador_gravado = 0
    capitulos_faltantes = 0
    for parte in partes_unificadas:
        for cap_info in parte["capitulos"]:
            contador_gravado += 1
            slug_origem = cap_info["slug_origem"]
            cap_original = num_capitulo(cap_info["cap_original"])

            cap_path = DIR_RAIZ / slug_origem / "capitulos" / f"cap_{cap_original:02d}.md"
            if not cap_path.exists():
                cap_path = DIR_RAIZ / slug_origem / "capitulos" / f"cap_{cap_original}.md"
            if not cap_path.exists():
                # Fallback: buscar por qualquer arquivo cap_N.md/cap_NN.md com esse número
                for cand in sorted((DIR_RAIZ / slug_origem / "capitulos").glob("cap_*.md"), reverse=True):
                    try:
                        if int(cand.stem.split("_")[1]) == cap_original:
                            cap_path = cand
                            break
                    except (IndexError, ValueError):
                        continue
            if not cap_path.exists():
                print(f"  [AVISO] Cap {slug_origem}/cap_{cap_original}.md nao encontrado")
                capitulos_faltantes += 1
                continue

            with open(cap_path, "r", encoding="utf-8") as f:
                conteudo = f.read()

            conteudo = extrair_frontmatter(conteudo)
            conteudo = renumerar_titulo(conteudo, contador_gravado)

            cap_destino = dir_caps / f"cap_{contador_gravado}.md"
            with open(cap_destino, "w", encoding="utf-8") as f:
                f.write(conteudo)

    print(f"  Capítulos processados: {contador_gravado}")

    # Validacao: soma dos capitulos do sumario vs arquivos copiados
    if capitulos_faltantes:
        print(f"  [FALHA] {capitulos_faltantes} capítulo(s) do sumário não encontrados no disco!")
        sys.exit(1)
    if contador_gravado != total_caps:
        print(f"  [FALHA] Contagem divergente: sumário lista {total_caps}, copiados {contador_gravado}")
        sys.exit(1)
    print(f"  [OK] Contagem confirmada: {contador_gravado} capítulos correspondem ao sumário")

    # ── GERAR ELEMENTOS TEXTUAIS ──────────────────────────────

    step("Gerar elementos textuais")

    prefacio = f"""# Prefácio

{introducao}

## Sobre este Compilado

- **{len(sumarios)} livros** reunidos em uma única obra
- **{total_caps} capítulos** organizados em **{len(partes_unificadas)} partes**
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

    step("Gerar PDF via Pandoc+Typst (pode levar vários minutos)")

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
        print(f"  Executando Pandoc+Typst (timeout 3600s)...")

        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=3600)

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
        print(f"  [ERRO] Timeout! O arquivo MD tem {md_mb:.1f} MB e excedeu 3600s")
        sys.exit(1)
    except Exception as e:
        print(f"  [ERRO] {e}")
        sys.exit(1)

    # ── VALIDAÇÃO ─────────────────────────────────────────────

    step("Validação final")

    erros = []
    for nome in ["livro_final.md", "sumario_macro.json", "livro_final.pdf", f"{SLUG_COMPILADO}.pdf"]:
        p = dir_compilado / nome
        if p.exists() and p.stat().st_size > 0:
            sz = p.stat().st_size / (1024*1024) if nome.endswith(".pdf") else p.stat().st_size / 1024
            unid = "MB" if nome.endswith(".pdf") else "KB"
            print(f"  [OK] {nome}: {sz:.1f} {unid}")
        else:
            print(f"  [FALHA] {nome} ausente")
            erros.append(nome)

    caps = sorted(dir_caps.glob("cap_*.md"))
    print(f"  [OK] Capítulos individuais: {len(caps)}")
    if caps:
        nums = sorted([int(re.search(r'cap_(\d+)', p.stem).group(1)) for p in caps])
        if nums == list(range(1, len(nums) + 1)):
            print(f"  [OK] Numeração: 1 a {len(nums)} sem saltos")
        else:
            print(f"  [FALHA] Numeração inconsistente")
            erros.append("numeracao")

    pdf_mb = pdf_path.stat().st_size / (1024*1024) if pdf_path.exists() else 0

    print(f"\n{'='*60}")
    print(f"  COMPILAÇÃO CONCLUÍDA")
    print(f"{'='*60}")
    print(f"  Pasta: output/{SLUG_COMPILADO}/")
    print(f"  PDF:   {SLUG_COMPILADO}.pdf ({pdf_mb:.1f} MB)")
    print(f"  Status: {'OK' if not erros else 'FALHA: '+', '.join(erros)}")
    print()

    if erros:
        sys.exit(1)


if __name__ == "__main__":
    main()
