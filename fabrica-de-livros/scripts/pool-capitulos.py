#!/usr/bin/env python3
"""
Upgrade 4 — Controle Dinamico de Concorrencia (Queue & Batching).

Em vez de instanciar 16+ subagentes de uma vez (risco de throttling TPM/RPM e
estouro de contexto), o Orquestrador Mestre despacha os capitulos em LOTES,
consultando este script para saber:

  - qual e o proximo lote a despachar (`--plano` / `--proximo-lote`)
  - quais capitulos continuam pendentes ou falharam (`--pendentes`)
  - quanto esperar antes de retentar um capitulo (backoff exponencial)

Estado persistido em: output/<slug>/capitulos/_pool_estado.json

Uso:
    python scripts/pool-capitulos.py <slug> --plano [--lote 4]
    python scripts/pool-capitulos.py <slug> --proximo-lote [--lote 4]
    python scripts/pool-capitulos.py <slug> --pendentes [--estrito]
    python scripts/pool-capitulos.py <slug> --registrar 7 --sucesso
    python scripts/pool-capitulos.py <slug> --registrar 7 --falha "timeout do subagente"
    python scripts/pool-capitulos.py <slug> --status
"""

import argparse
import json
import re
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

LOTE_PADRAO = 4
MAX_TENTATIVAS = 3
BACKOFF_BASE_S = 15
BACKOFF_MAX_S = 240

SECOES_MINIMAS = 7


def carregar_sumario(slug):
    caminho = DIR_OUTPUT / slug / "sumario_macro.json"
    if not caminho.exists():
        print(f"[ERRO] sumario_macro.json nao encontrado em {caminho.parent}")
        return None
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    capitulos = []
    for parte in dados.get("partes", []):
        for cap in parte.get("capitulos", []):
            capitulos.append({
                "capitulo": str(cap.get("capitulo")),
                "parte": str(parte.get("parte")),
                "titulo": cap.get("titulo", ""),
            })
    capitulos.sort(key=lambda c: int(re.sub(r"\D", "", c["capitulo"]) or 0))
    return capitulos


def caminho_estado(slug):
    return DIR_OUTPUT / slug / "capitulos" / "_pool_estado.json"


def carregar_estado(slug):
    p = caminho_estado(slug)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"slug": slug, "lote": LOTE_PADRAO, "capitulos": {}}


def gravar_estado(slug, estado):
    p = caminho_estado(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")


def arquivo_capitulo(slug, numero):
    dir_caps = DIR_OUTPUT / slug / "capitulos"
    for padrao in (f"cap_{int(numero):02d}.md", f"cap_{numero}.md"):
        p = dir_caps / padrao
        if p.exists():
            return p
    achados = [c for c in dir_caps.glob("cap_*.md")
               if re.search(r"cap_(\d+)", c.stem)
               and int(re.search(r"cap_(\d+)", c.stem).group(1)) == int(numero)]
    return achados[0] if achados else None


def capitulo_entregue(slug, numero):
    """Entregue = arquivo existe e tem as 7 secoes do EITA-V2 com corpo."""
    arq = arquivo_capitulo(slug, numero)
    if not arq:
        return False, "arquivo ausente"
    texto = arq.read_text(encoding="utf-8", errors="replace")
    secoes = len(set(re.findall(r"^##\s*([1-7])[\.\)]", texto, re.MULTILINE)))
    if secoes < SECOES_MINIMAS:
        return False, f"apenas {secoes}/7 secoes EITA"
    if len(texto) < 3000:
        return False, f"corpo curto ({len(texto)} caracteres)"
    return True, "ok"


def backoff(tentativas):
    return min(BACKOFF_BASE_S * (2 ** max(0, tentativas - 1)), BACKOFF_MAX_S)


def carregar_manifesto(slug, manifesto_rel):
    """Generalizacao (Fase E/V4): unidades de trabalho vindas de um manifesto
    (estrutura_artigos.json / estrutura_ebooks.json) em vez de sumario_macro.json.
    Cada unidade e 1 artigo/ebook inteiro, nao 1 capitulo dentro de uma obra."""
    caminho = DIR_OUTPUT / slug / manifesto_rel
    if not caminho.exists():
        print(f"[ERRO] Manifesto nao encontrado: {caminho}")
        return None
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    itens = dados.get("artigos") or dados.get("ebooks") or []
    unidades = [{
        "capitulo": str(item["indice"]),
        "parte": "-",
        "titulo": item.get("titulo", ""),
        "_diretorio": item.get("diretorio", ""),
    } for item in itens]
    unidades.sort(key=lambda c: int(c["capitulo"]))
    return unidades


def unidade_entregue(slug, diretorio):
    """Para manifesto: entregue = existe PDF ou EPUB no diretorio da unidade."""
    base = DIR_OUTPUT / slug / diretorio
    if (base / "livro_final.pdf").exists():
        return True, "ok"
    if list(base.glob("*.epub")):
        return True, "ok"
    return False, "PDF/EPUB ainda nao gerado"


def montar_visao(slug, tamanho_lote, manifesto_rel=None):
    capitulos = carregar_manifesto(slug, manifesto_rel) if manifesto_rel else carregar_sumario(slug)
    if capitulos is None:
        return None
    estado = carregar_estado(slug)
    estado["lote"] = tamanho_lote
    for cap in capitulos:
        num = cap["capitulo"]
        reg = estado["capitulos"].setdefault(
            num, {"tentativas": 0, "ultimo_erro": "", "estado": "pendente"})
        if manifesto_rel:
            ok, motivo = unidade_entregue(slug, cap["_diretorio"])
        else:
            ok, motivo = capitulo_entregue(slug, num)
        cap["tentativas"] = reg["tentativas"]
        cap["ultimo_erro"] = reg["ultimo_erro"]
        if ok:
            reg["estado"] = "concluido_autonomo"
            cap["estado"] = "concluido_autonomo"
            cap["motivo"] = ""
        else:
            esgotado = reg["tentativas"] >= MAX_TENTATIVAS
            reg["estado"] = "esgotado" if esgotado else "pendente"
            cap["estado"] = reg["estado"]
            cap["motivo"] = motivo
            cap["backoff_s"] = backoff(reg["tentativas"]) if reg["tentativas"] else 0
    gravar_estado(slug, estado)
    return capitulos


def em_lotes(itens, tamanho):
    return [itens[i:i + tamanho] for i in range(0, len(itens), tamanho)]


def imprimir_lote(indice, lote):
    coords = ", ".join(f"{{parte:{c['parte']}, capitulo:{c['capitulo']}}}" for c in lote)
    print(f"LOTE {indice}: {len(lote)} capitulo(s) -> {coords}")
    for c in lote:
        extra = ""
        if c.get("tentativas"):
            extra = f" | tentativa {c['tentativas'] + 1}/{MAX_TENTATIVAS}, aguardar {c.get('backoff_s', 0)}s"
        print(f"  cap {c['capitulo']:>2} [{c['estado']}] {c['titulo'][:64]}{extra}")


def main():
    ap = argparse.ArgumentParser(description="Pool de execucao paralela por lotes")
    ap.add_argument("slug")
    ap.add_argument("--lote", type=int, default=LOTE_PADRAO,
                    help=f"capitulos por lote (padrao {LOTE_PADRAO})")
    ap.add_argument("--plano", action="store_true", help="imprime o plano completo de lotes")
    ap.add_argument("--proximo-lote", action="store_true",
                    help="imprime apenas o proximo lote a despachar")
    ap.add_argument("--pendentes", action="store_true", help="lista capitulos pendentes/esgotados")
    ap.add_argument("--status", action="store_true", help="resumo do progresso")
    ap.add_argument("--registrar", metavar="CAP", help="registra o resultado de um capitulo")
    ap.add_argument("--sucesso", action="store_true")
    ap.add_argument("--falha", nargs="?", const="falha nao especificada", metavar="MOTIVO")
    ap.add_argument("--reset", action="store_true", help="zera o contador de tentativas")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--manifesto", metavar="CAMINHO", default=None,
                    help="relativo a output/<slug>/: usa estrutura_artigos.json ou "
                         "estrutura_ebooks.json em vez de sumario_macro.json "
                         "(cada unidade e 1 artigo/ebook inteiro, nao 1 capitulo)")
    ap.add_argument("--estrito", action="store_true",
                    help="com --pendentes: exit 1 se houver capitulo nao concluido")
    args = ap.parse_args()

    if not (DIR_OUTPUT / args.slug).exists():
        print(f"[ERRO] Livro nao encontrado: {DIR_OUTPUT / args.slug}")
        return 1

    if args.registrar:
        estado = carregar_estado(args.slug)
        reg = estado["capitulos"].setdefault(
            str(args.registrar), {"tentativas": 0, "ultimo_erro": "", "estado": "pendente"})
        reg["tentativas"] += 1
        if args.sucesso:
            reg["estado"] = "concluido_autonomo"
            reg["ultimo_erro"] = ""
            print(f"[OK] cap {args.registrar}: sucesso registrado "
                  f"(tentativa {reg['tentativas']})")
        else:
            reg["ultimo_erro"] = args.falha or "falha nao especificada"
            esgotado = reg["tentativas"] >= MAX_TENTATIVAS
            reg["estado"] = "esgotado" if esgotado else "pendente"
            espera = backoff(reg["tentativas"])
            print(f"[FALHA] cap {args.registrar}: {reg['ultimo_erro']} "
                  f"(tentativa {reg['tentativas']}/{MAX_TENTATIVAS})")
            if esgotado:
                print(f"  -> tentativas esgotadas; escalar para revisao manual")
            else:
                print(f"  -> retentar apos {espera}s (backoff exponencial)")
        gravar_estado(args.slug, estado)
        return 0

    if args.reset:
        estado = carregar_estado(args.slug)
        for reg in estado["capitulos"].values():
            reg["tentativas"] = 0
            reg["ultimo_erro"] = ""
        gravar_estado(args.slug, estado)
        print("[OK] Contadores de tentativa zerados")
        return 0

    capitulos = montar_visao(args.slug, args.lote, manifesto_rel=args.manifesto)
    if capitulos is None:
        return 1

    concluidos = [c for c in capitulos if c["estado"] == "concluido_autonomo"]
    pendentes = [c for c in capitulos if c["estado"] == "pendente"]
    esgotados = [c for c in capitulos if c["estado"] == "esgotado"]

    if args.json:
        print(json.dumps({
            "slug": args.slug, "lote": args.lote,
            "total": len(capitulos), "concluidos": len(concluidos),
            "pendentes": len(pendentes), "esgotados": len(esgotados),
            "capitulos": capitulos,
            "lotes_pendentes": em_lotes(pendentes, args.lote),
        }, ensure_ascii=False, indent=2))
        return 1 if (args.estrito and (pendentes or esgotados)) else 0

    if args.status or not (args.plano or args.proximo_lote or args.pendentes):
        print(f"POOL - {args.slug} (lote={args.lote}, max_tentativas={MAX_TENTATIVAS})")
        print(f"  total      : {len(capitulos)}")
        print(f"  concluidos : {len(concluidos)}")
        print(f"  pendentes  : {len(pendentes)}")
        print(f"  esgotados  : {len(esgotados)}")
        if esgotados:
            print("  capitulos esgotados: " + ", ".join(c["capitulo"] for c in esgotados))
        return 0

    if args.plano:
        lotes = em_lotes(capitulos, args.lote)
        print(f"PLANO DE DESPACHO - {args.slug}: {len(capitulos)} capitulo(s) "
              f"em {len(lotes)} lote(s) de ate {args.lote}")
        for i, lote in enumerate(lotes, 1):
            imprimir_lote(i, lote)
        print("\nRegra: despache um lote, aguarde TODOS os subagentes do lote, "
              "registre o resultado de cada capitulo, so entao despache o proximo lote.")
        return 0

    if args.proximo_lote:
        fila = pendentes
        if not fila:
            print("[OK] Nenhum capitulo pendente - Fase 2 completa. "
                  "Avance para a Fase 2.5 (auditoria + revisor-tecnico).")
            return 0
        imprimir_lote(1, fila[:args.lote])
        restantes = max(0, len(fila) - args.lote)
        print(f"\nRestam {restantes} capitulo(s) na fila depois deste lote.")
        return 0

    if args.pendentes:
        if not pendentes and not esgotados:
            print("[OK] Todos os capitulos concluidos e validados estruturalmente")
            return 0
        for i, lote in enumerate(em_lotes(pendentes, args.lote), 1):
            imprimir_lote(i, lote)
        if esgotados:
            print(f"\n[ESGOTADOS] {len(esgotados)} capitulo(s) atingiram "
                  f"{MAX_TENTATIVAS} tentativas:")
            for c in esgotados:
                print(f"  cap {c['capitulo']}: {c['ultimo_erro'] or c['motivo']}")
        return 1 if args.estrito else 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
