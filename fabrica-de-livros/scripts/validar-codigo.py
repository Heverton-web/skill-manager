#!/usr/bin/env python3
"""
Upgrade 3 — CI de Codigo dos Capitulos (Fabrica Agentica de Livros).

Extrai todos os blocos de codigo dos capitulos e valida a sintaxe de cada um em
processo isolado, SEM executar o codigo do livro (analise estatica apenas — nada
de rede, arquivos ou side effects).

Validadores por linguagem:
  python        -> ast.parse (compilador do proprio CPython)
  json          -> json.loads
  javascript    -> node --check (arquivo .mjs quando ha import/export)
  typescript    -> tsc --noEmit (se disponivel), senao NAO VERIFICADO
  bash/sh       -> bash -n
  powershell    -> parser do PowerShell (se disponivel)
  yaml          -> yaml.safe_load (se PyYAML disponivel)
  toml          -> tomllib
  html/xml      -> parser tolerante do stdlib
  sql/dockerfile/text/mermaid/diff/console -> NAO APLICAVEL (ignorado)

Uso:
    python scripts/validar-codigo.py <slug>
    python scripts/validar-codigo.py <slug> --capitulo 7
    python scripts/validar-codigo.py <slug> --md output/<slug>/livro_final.md
    python scripts/validar-codigo.py <slug> --estrito     # exit 1 se houver falha
    python scripts/validar-codigo.py <slug> --json

Relatorio: output/<slug>/validacao/relatorio_codigo.json
"""

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

RE_BLOCO = re.compile(
    r"^[ \t]*```[ \t]*(?P<lang>[A-Za-z0-9_+#\-\.]*)[ \t]*\n(?P<code>.*?)^[ \t]*```[ \t]*$",
    re.DOTALL | re.MULTILINE,
)

ALIASES = {
    "py": "python", "python3": "python",
    "js": "javascript", "node": "javascript", "mjs": "javascript", "cjs": "javascript",
    "jsx": "javascript",
    "ts": "typescript", "tsx": "typescript",
    "sh": "bash", "shell": "bash", "zsh": "bash",
    "ps1": "powershell", "pwsh": "powershell",
    "yml": "yaml",
    "jsonc": "json", "json5": "json",
}

NAO_APLICAVEL = {
    "", "text", "txt", "texto", "plaintext", "console", "output", "saida", "log",
    "diff", "patch", "sql", "dockerfile", "docker", "makefile", "ini", "cfg",
    "conf", "env", "mermaid", "plantuml", "markdown", "md", "csv", "tsv", "http",
    "graphql", "regex", "bnf", "pseudo", "pseudocodigo", "pseudocode", "asciiart",
    "tree", "terminal", "cmd", "prompt", "resultado", "tabela", "ascii",
}

# Marcadores de trecho intencionalmente incompleto — reportados como fragmento
RE_FRAGMENTO = re.compile(
    r"(^\s*\.\.\.\s*$)|(\.\.\.\s*(#|//)\s*)|(<seu[-_ ])|(<SEU[-_ ])|(\{\{\s*\w+\s*\}\})",
    re.MULTILINE,
)


def norm_lang(lang):
    lang = (lang or "").strip().lower()
    return ALIASES.get(lang, lang)


def _rodar(comando, entrada_arquivo=None, timeout=45):
    try:
        r = subprocess.run(comando, capture_output=True, text=True, timeout=timeout)
        if r.returncode == 0:
            return True, ""
        saida = (r.stderr or r.stdout or "").strip()
        return False, saida.split("\n")[0][:240] if saida else f"exit {r.returncode}"
    except FileNotFoundError:
        return None, "ferramenta ausente"
    except subprocess.TimeoutExpired:
        return False, f"timeout de {timeout}s"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:240]


def _temp(codigo, sufixo):
    fh = tempfile.NamedTemporaryFile("w", suffix=sufixo, delete=False, encoding="utf-8")
    fh.write(codigo)
    fh.close()
    return Path(fh.name)


def validar_python(codigo):
    try:
        ast.parse(codigo)
        return True, ""
    except SyntaxError as exc:
        return False, f"linha {exc.lineno}: {exc.msg}"


def validar_json(codigo):
    try:
        json.loads(codigo)
        return True, ""
    except ValueError as exc:
        return False, str(exc)[:240]


def validar_javascript(codigo):
    node = shutil.which("node")
    if not node:
        return None, "node ausente"
    esm = re.search(r"^\s*(import\s|export\s|export\{|await\s)", codigo, re.MULTILINE)
    arq = _temp(codigo, ".mjs" if esm else ".js")
    try:
        return _rodar([node, "--check", str(arq)])
    finally:
        arq.unlink(missing_ok=True)


def validar_typescript(codigo):
    tsc = shutil.which("tsc") or shutil.which("tsc.cmd")
    if not tsc:
        return None, "tsc ausente (npm i -g typescript para habilitar)"
    arq = _temp(codigo, ".ts")
    try:
        return _rodar([tsc, "--noEmit", "--skipLibCheck", "--target", "es2022",
                       "--moduleResolution", "bundler", "--module", "esnext", str(arq)])
    finally:
        arq.unlink(missing_ok=True)


def validar_bash(codigo):
    bash = shutil.which("bash")
    if not bash:
        return None, "bash ausente"
    arq = _temp(codigo, ".sh")
    try:
        return _rodar([bash, "-n", str(arq)])
    finally:
        arq.unlink(missing_ok=True)


def validar_powershell(codigo):
    ps = shutil.which("powershell") or shutil.which("pwsh")
    if not ps:
        return None, "powershell ausente"
    arq = _temp(codigo, ".ps1")
    script = (
        "$ErrorActionPreference='Stop';"
        "$t=$null;$e=$null;"
        f"[System.Management.Automation.Language.Parser]::ParseFile('{arq.as_posix()}',"
        "[ref]$t,[ref]$e) > $null;"
        "if($e.Count -gt 0){[Console]::Error.WriteLine($e[0].Message); exit 1}; exit 0"
    )
    try:
        return _rodar([ps, "-NoProfile", "-NonInteractive", "-Command", script])
    finally:
        arq.unlink(missing_ok=True)


def validar_yaml(codigo):
    try:
        import yaml  # type: ignore
    except ImportError:
        return None, "PyYAML ausente (pip install pyyaml para habilitar)"
    try:
        list(yaml.safe_load_all(codigo))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, str(exc).split("\n")[0][:240]


def validar_toml(codigo):
    try:
        import tomllib
    except ImportError:
        return None, "tomllib ausente"
    try:
        tomllib.loads(codigo)
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:240]


def validar_xml(codigo):
    from xml.etree import ElementTree
    try:
        ElementTree.fromstring(codigo)
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:240]


VALIDADORES = {
    "python": validar_python,
    "json": validar_json,
    "javascript": validar_javascript,
    "typescript": validar_typescript,
    "bash": validar_bash,
    "powershell": validar_powershell,
    "yaml": validar_yaml,
    "toml": validar_toml,
    "xml": validar_xml,
}


def linha_do_offset(texto, offset):
    return texto.count("\n", 0, offset) + 1


def validar_arquivo(caminho, rotulo, ignorar_fragmentos):
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    resultados = []
    for m in RE_BLOCO.finditer(texto):
        lang = norm_lang(m.group("lang"))
        codigo = m.group("code")
        registro = {
            "origem": rotulo,
            "linha": linha_do_offset(texto, m.start()),
            "linguagem": lang or "(sem tag)",
            "linhas_codigo": codigo.count("\n") + 1,
        }
        if lang in NAO_APLICAVEL:
            registro.update(status="nao_aplicavel", detalhe="linguagem sem validador")
            resultados.append(registro)
            continue
        if ignorar_fragmentos and RE_FRAGMENTO.search(codigo):
            registro.update(status="fragmento", detalhe="trecho com placeholder/elipse")
            resultados.append(registro)
            continue
        validador = VALIDADORES.get(lang)
        if validador is None:
            registro.update(status="nao_verificado", detalhe=f"sem validador para '{lang}'")
            resultados.append(registro)
            continue
        ok, detalhe = validador(codigo)
        if ok is None:
            registro.update(status="nao_verificado", detalhe=detalhe)
        elif ok:
            registro.update(status="ok", detalhe="")
        else:
            registro.update(status="falha", detalhe=detalhe)
        resultados.append(registro)
    return resultados


def main():
    ap = argparse.ArgumentParser(description="Valida a sintaxe dos blocos de codigo do livro")
    ap.add_argument("slug")
    ap.add_argument("--capitulo", help="valida apenas o capitulo N")
    ap.add_argument("--md", help="valida um markdown especifico em vez dos capitulos")
    ap.add_argument("--ignorar-fragmentos", action="store_true",
                    help="classifica trechos com placeholders como 'fragmento' em vez de validar")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se houver qualquer falha")
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON completo")
    args = ap.parse_args()

    dir_livro = DIR_OUTPUT / args.slug
    if not dir_livro.exists():
        print(f"[ERRO] Livro nao encontrado: {dir_livro}")
        return 1

    alvos = []
    if args.md:
        p = Path(args.md)
        if not p.exists():
            print(f"[ERRO] Arquivo nao encontrado: {p}")
            return 1
        alvos.append((p, p.name))
    else:
        caps = sorted((dir_livro / "capitulos").glob("cap_*.md"),
                      key=lambda p: int(re.search(r"cap_(\d+)", p.stem).group(1)))
        if args.capitulo:
            caps = [c for c in caps
                    if re.search(r"cap_(\d+)", c.stem).group(1).lstrip("0")
                    == str(args.capitulo).lstrip("0")]
        if not caps:
            print(f"[ERRO] Nenhum capitulo encontrado em {dir_livro / 'capitulos'}")
            return 1
        alvos = [(c, c.stem) for c in caps]

    todos = []
    for caminho, rotulo in alvos:
        todos.extend(validar_arquivo(caminho, rotulo, args.ignorar_fragmentos))

    resumo = {}
    for r in todos:
        resumo[r["status"]] = resumo.get(r["status"], 0) + 1
    por_linguagem = {}
    for r in todos:
        chave = r["linguagem"]
        por_linguagem.setdefault(chave, {"total": 0, "ok": 0, "falha": 0})
        por_linguagem[chave]["total"] += 1
        if r["status"] == "ok":
            por_linguagem[chave]["ok"] += 1
        elif r["status"] == "falha":
            por_linguagem[chave]["falha"] += 1

    falhas = [r for r in todos if r["status"] == "falha"]
    verificados = resumo.get("ok", 0) + len(falhas)
    taxa = (resumo.get("ok", 0) / verificados * 100) if verificados else 100.0

    relatorio = {
        "slug": args.slug,
        "total_blocos": len(todos),
        "resumo": resumo,
        "por_linguagem": por_linguagem,
        "taxa_aprovacao_pct": round(taxa, 1),
        "blocos": todos,
    }

    dir_val = dir_livro / "validacao"
    dir_val.mkdir(exist_ok=True)
    (dir_val / "relatorio_codigo.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"CI de Codigo - {args.slug}")
    print(f"  blocos analisados : {len(todos)}")
    for status in ("ok", "falha", "nao_verificado", "nao_aplicavel", "fragmento"):
        if status in resumo:
            print(f"  {status:<17}: {resumo[status]}")
    print(f"  taxa de aprovacao : {taxa:.1f}% (sobre {verificados} blocos verificaveis)")

    if falhas:
        print(f"\n[FALHA] {len(falhas)} bloco(s) com erro de sintaxe:")
        for f in falhas[:20]:
            print(f"  - {f['origem']}:{f['linha']} [{f['linguagem']}] {f['detalhe']}")
        if len(falhas) > 20:
            print(f"  ... e mais {len(falhas) - 20}")
    else:
        print("\n[OK] Nenhum erro de sintaxe nos blocos verificaveis")

    print(f"\nRelatorio: {(dir_val / 'relatorio_codigo.json').relative_to(DIR_PROJETO)}")

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    if args.estrito and falhas:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
