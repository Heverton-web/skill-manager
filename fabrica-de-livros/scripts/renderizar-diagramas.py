#!/usr/bin/env python3
"""
Upgrade 2 — Suporte nativo a diagramas Mermaid (Fabrica Agentica de Livros).

Extrai blocos ```mermaid dos capitulos / do livro_final.md, renderiza em PNG de
alta resolucao via mermaid-cli (mmdc) e devolve um Markdown com os blocos
substituidos por figuras — pronto para o pipeline Pandoc + Typst.

NAO destrutivo: o arquivo de origem nunca e sobrescrito. A versao renderizada
vai para `_livro_render.md` (ou o caminho passado em --saida).

Idempotente: o nome do PNG deriva do hash do codigo do diagrama, entao rodar de
novo nao re-renderiza diagramas inalterados.

Degradacao graciosa: se o mmdc nao estiver instalado ou um diagrama tiver
sintaxe invalida, o bloco permanece como bloco de codigo (o Typst o renderiza
como codigo) e a falha e reportada — a compilacao do livro nunca e bloqueada.

Uso:
    python scripts/renderizar-diagramas.py <slug>
    python scripts/renderizar-diagramas.py <slug> --md output/<slug>/livro_final.md
    python scripts/renderizar-diagramas.py <slug> --capitulos --validar
    python scripts/renderizar-diagramas.py <slug> --formato svg --escala 2

Legenda opcional: primeira linha do bloco mermaid com a diretiva
    %% legenda: Fluxo de ingestao de eventos
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

RE_BLOCO = re.compile(
    r"^(?P<indent>[ \t]*)```(?P<lang>mermaid|plantuml)[ \t]*\n(?P<code>.*?)^[ \t]*```[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
RE_LEGENDA = re.compile(r"^\s*%%\s*legenda:\s*(.+)$", re.MULTILINE | re.IGNORECASE)


def caminho_rel(caminho):
    """Caminho relativo ao projeto quando possivel; absoluto caso contrario."""
    try:
        return str(Path(caminho).resolve().relative_to(DIR_PROJETO))
    except ValueError:
        return str(caminho)


def achar_mmdc():
    """Localiza o mermaid-cli. Retorna lista de argumentos base ou None."""
    for nome in ("mmdc.cmd", "mmdc", "mmdc.ps1"):
        caminho = shutil.which(nome)
        if caminho and not caminho.endswith(".ps1"):
            return [caminho]
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if npx:
        return [npx, "-y", "@mermaid-js/mermaid-cli"]
    return None


def config_puppeteer():
    """Config de puppeteer com --no-sandbox (necessario em CI/containers)."""
    cfg = {"args": ["--no-sandbox", "--disable-dev-shm-usage"]}
    tmp = Path(tempfile.gettempdir()) / "fabrica_puppeteer.json"
    tmp.write_text(json.dumps(cfg), encoding="utf-8")
    return tmp


def renderizar_um(base_mmdc, codigo, destino, formato, escala, cfg_puppeteer, tema="neutral"):
    """Renderiza um diagrama. Retorna (ok, mensagem_erro)."""
    with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(codigo)
        origem = Path(fh.name)
    try:
        comando = base_mmdc + [
            "-i", str(origem),
            "-o", str(destino),
            "-b", "white",
            "-t", tema,
            "--puppeteerConfigFile", str(cfg_puppeteer),
        ]
        if formato == "png":
            comando += ["-s", str(escala)]
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=120)
        if destino.exists() and destino.stat().st_size > 0:
            return True, ""
        saida = (resultado.stderr or resultado.stdout or "").strip()
        return False, saida.split("\n")[-1][:220] if saida else "mmdc nao produziu arquivo"
    except subprocess.TimeoutExpired:
        return False, "timeout de 120s no mmdc"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:220]
    finally:
        origem.unlink(missing_ok=True)


def processar_texto(texto, contexto, dir_imagens, dir_relativo, base_mmdc,
                    formato, escala, cfg_puppeteer, contador_inicial=0, tema="neutral"):
    """Substitui blocos mermaid por figuras. Retorna (novo_texto, relatorio)."""
    relatorio = {"total": 0, "renderizados": 0, "cache": 0, "falhas": [], "ignorados": []}
    contador = contador_inicial

    def substituir(m):
        nonlocal contador
        lang = m.group("lang")
        codigo = m.group("code")
        indent = m.group("indent")
        relatorio["total"] += 1

        if lang == "plantuml":
            relatorio["ignorados"].append(
                {"contexto": contexto, "motivo": "plantuml sem renderizador configurado"})
            return m.group(0)

        legenda_match = RE_LEGENDA.search(codigo)
        legenda = legenda_match.group(1).strip() if legenda_match else None
        codigo_limpo = RE_LEGENDA.sub("", codigo).strip()
        if not codigo_limpo:
            relatorio["ignorados"].append({"contexto": contexto, "motivo": "bloco mermaid vazio"})
            return m.group(0)

        contador += 1
        digest = hashlib.sha1(codigo_limpo.encode("utf-8")).hexdigest()[:10]
        nome = f"dia_{contexto}_{contador:02d}_{digest}.{formato}"
        destino = dir_imagens / nome

        if destino.exists() and destino.stat().st_size > 0:
            relatorio["cache"] += 1
        else:
            if base_mmdc is None:
                relatorio["falhas"].append(
                    {"contexto": contexto, "arquivo": nome, "erro": "mmdc nao encontrado"})
                return m.group(0)
            ok, erro = renderizar_um(base_mmdc, codigo_limpo, destino, formato,
                                     escala, cfg_puppeteer, tema)
            if not ok:
                relatorio["falhas"].append({"contexto": contexto, "arquivo": nome, "erro": erro})
                return m.group(0)
            relatorio["renderizados"] += 1

        # A legenda NAO leva prefixo "Figura N": Pandoc/Typst numeram a figura
        texto_legenda = legenda or "Diagrama do capitulo"
        caminho_md = f"{dir_relativo}/{nome}" if dir_relativo else nome
        return f"{indent}![{texto_legenda}]({caminho_md})"

    return RE_BLOCO.sub(substituir, texto), relatorio


def validar_apenas(texto, contexto, base_mmdc, cfg_puppeteer, tema="neutral"):
    """Valida a sintaxe dos blocos mermaid sem gravar figuras definitivas."""
    relatorio = {"total": 0, "validos": 0, "falhas": []}
    for m in RE_BLOCO.finditer(texto):
        if m.group("lang") != "mermaid":
            continue
        relatorio["total"] += 1
        codigo = RE_LEGENDA.sub("", m.group("code")).strip()
        if base_mmdc is None:
            relatorio["falhas"].append({"contexto": contexto, "erro": "mmdc nao encontrado"})
            continue
        with tempfile.TemporaryDirectory() as tmpdir:
            destino = Path(tmpdir) / "check.svg"
            ok, erro = renderizar_um(base_mmdc, codigo, destino, "svg", 1, cfg_puppeteer, tema)
        if ok:
            relatorio["validos"] += 1
        else:
            relatorio["falhas"].append({"contexto": contexto, "erro": erro})
    return relatorio


def main():
    ap = argparse.ArgumentParser(description="Renderiza diagramas Mermaid do livro")
    ap.add_argument("slug")
    ap.add_argument("--md", help="markdown de entrada (padrao: output/<slug>/livro_final.md)")
    ap.add_argument("--saida", help="markdown de saida (padrao: output/<slug>/_livro_render.md)")
    ap.add_argument("--capitulos", action="store_true",
                    help="processa cada capitulos/cap_*.md em vez do livro_final.md")
    ap.add_argument("--validar", action="store_true",
                    help="apenas valida a sintaxe dos diagramas (nao grava figuras)")
    ap.add_argument("--formato", choices=("png", "svg"), default="png")
    ap.add_argument("--escala", type=int, default=3, help="escala do PNG (padrao 3 = 300dpi aprox.)")
    ap.add_argument("--tema", default="neutral",
                    choices=("neutral", "default", "base", "forest", "dark"))
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se houver qualquer falha")
    args = ap.parse_args()

    dir_livro = DIR_OUTPUT / args.slug
    if not dir_livro.exists():
        print(f"[ERRO] Livro nao encontrado: {dir_livro}")
        return 1

    base_mmdc = achar_mmdc()
    if base_mmdc is None:
        print("[AVISO] mermaid-cli (mmdc) nao encontrado. "
              "Instale com: npm install -g @mermaid-js/mermaid-cli")
    cfg = config_puppeteer()

    dir_imagens = dir_livro / "imagens" / "diagramas"
    dir_imagens.mkdir(parents=True, exist_ok=True)

    consolidado = {"slug": args.slug, "modo": "", "arquivos": [],
                   "total": 0, "renderizados": 0, "cache": 0,
                   "falhas": [], "ignorados": [], "validos": 0}

    if args.capitulos or args.validar:
        caps = sorted((dir_livro / "capitulos").glob("cap_*.md"),
                      key=lambda p: int(re.search(r"cap_(\d+)", p.stem).group(1)))
        if not caps:
            print(f"[ERRO] Nenhum capitulo em {dir_livro / 'capitulos'}")
            return 1
        consolidado["modo"] = "validar" if args.validar else "capitulos"
        for cap in caps:
            texto = cap.read_text(encoding="utf-8", errors="replace")
            ctx = re.search(r"cap_(\d+)", cap.stem).group(1)
            if args.validar:
                rel = validar_apenas(texto, ctx, base_mmdc, cfg, args.tema)
                consolidado["total"] += rel["total"]
                consolidado["validos"] += rel["validos"]
                consolidado["falhas"].extend(rel["falhas"])
                marca = "OK" if not rel["falhas"] else "FALHA"
                print(f"  cap_{ctx}: {rel['total']} diagrama(s), {rel['validos']} valido(s) [{marca}]")
            else:
                novo, rel = processar_texto(texto, ctx, dir_imagens, "../imagens/diagramas",
                                            base_mmdc, args.formato, args.escala, cfg,
                                            tema=args.tema)
                destino = cap.parent / f"_{cap.stem}_render.md"
                destino.write_text(novo, encoding="utf-8")
                consolidado["arquivos"].append(caminho_rel(destino))
                for chave in ("total", "renderizados", "cache"):
                    consolidado[chave] += rel[chave]
                consolidado["falhas"].extend(rel["falhas"])
                consolidado["ignorados"].extend(rel["ignorados"])
                print(f"  cap_{ctx}: {rel['total']} diagrama(s) "
                      f"({rel['renderizados']} novo(s), {rel['cache']} em cache)")
    else:
        entrada = Path(args.md).resolve() if args.md else dir_livro / "livro_final.md"
        if not entrada.exists():
            print(f"[ERRO] Markdown nao encontrado: {entrada}")
            return 1
        saida = Path(args.saida).resolve() if args.saida else dir_livro / "_livro_render.md"
        texto = entrada.read_text(encoding="utf-8", errors="replace")
        novo, rel = processar_texto(texto, "livro", dir_imagens, "imagens/diagramas",
                                    base_mmdc, args.formato, args.escala, cfg, tema=args.tema)
        saida.write_text(novo, encoding="utf-8")
        consolidado["modo"] = "livro"
        consolidado["arquivos"].append(caminho_rel(saida))
        for chave in ("total", "renderizados", "cache"):
            consolidado[chave] += rel[chave]
        consolidado["falhas"].extend(rel["falhas"])
        consolidado["ignorados"].extend(rel["ignorados"])
        print(f"[OK] {saida.name}: {rel['total']} diagrama(s) "
              f"({rel['renderizados']} novo(s), {rel['cache']} em cache)")

    if consolidado["falhas"]:
        print(f"[AVISO] {len(consolidado['falhas'])} diagrama(s) com falha "
              f"(bloco mantido como codigo):")
        for f in consolidado["falhas"][:5]:
            print(f"  - {f.get('contexto')}: {f.get('erro')}")
    if consolidado["ignorados"]:
        print(f"[INFO] {len(consolidado['ignorados'])} bloco(s) ignorado(s)")

    dir_rel = dir_livro / "validacao"
    dir_rel.mkdir(exist_ok=True)
    (dir_rel / "relatorio_diagramas.json").write_text(
        json.dumps(consolidado, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(consolidado, ensure_ascii=False, indent=2))

    if args.estrito and consolidado["falhas"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
