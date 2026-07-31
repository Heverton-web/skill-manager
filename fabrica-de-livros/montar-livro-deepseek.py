#!/usr/bin/env python3
"""
Compilador-abnt para o livro "Os Segredos Técnicos do DeepSeek".
Monta output/segredos-deepseek/livro_final.md com a estrutura ABNT completa:
titulo + subtitulo + prefacio + sumario + partes + capitulos + conclusao.

Uso: python montar-livro-deepseek.py
"""

import json
import sys
from pathlib import Path

SLUG = "segredos-deepseek"
DIR_LIVRO = Path(__file__).parent / "output" / SLUG
DIR_CAPS = DIR_LIVRO / "capitulos"


def main():
    sumario_path = DIR_LIVRO / "sumario_macro.json"
    if not sumario_path.exists():
        print(f"[ERRO] sumario_macro.json nao encontrado: {sumario_path}")
        sys.exit(1)

    with open(sumario_path, "r", encoding="utf-8") as f:
        sumario = json.load(f)

    titulo = sumario["titulo_obra"]
    subtitulo = sumario.get("subtitulo", "")
    introducao = sumario.get("introducao", "")
    conclusao = sumario.get("conclusao", "")
    partes = sumario.get("partes", [])

    total_caps = sum(len(p["capitulos"]) for p in partes)
    total_partes = len(partes)

    prefacio = f"""# Prefácio

{introducao}

## Sobre este Livro

- **{total_caps} capítulos** organizados em **{total_partes} partes**
- Estrutura pedagógica EITA-V2 em todos os capítulos (Introdução, Explica, Ilustra, Técnica, Aplica, Conclusão, Referências)
- Referências no formato ABNT, citadas como [N] ao longo do texto

## Como Navegar

Utilize o sumário abaixo para localizar rapidamente os temas de seu interesse.
Cada parte cobre um aspecto fundamental dos segredos técnicos do DeepSeek:
da origem da empresa à arquitetura, do treinamento de baixo custo ao raciocínio via RL.
"""

    sumario_texto = "# Sumário\n\n"
    for parte in partes:
        sumario_texto += f"- **Parte {parte['parte']} — {parte['titulo_parte']}**\n"
        for cap in parte["capitulos"]:
            sumario_texto += f"  - Capítulo {cap['capitulo']}: {cap['titulo']}\n"

    conc = f"""# Conclusão

{conclusao}

*Livro produzido pela Fábrica Agêntica de Livros via fluxo /criar-livro.*
"""

    corpo = []
    encontrados = 0
    for parte in partes:
        corpo.append(f"\n\n# Parte {parte['parte']} — {parte['titulo_parte']}\n")
        for cap in parte["capitulos"]:
            n = cap["capitulo"]
            cap_path = DIR_CAPS / f"cap_{n:02d}.md"
            if not cap_path.exists():
                cap_path = DIR_CAPS / f"cap_{n}.md"
            if cap_path.exists():
                corpo.append(cap_path.read_text(encoding="utf-8").strip())
                encontrados += 1
            else:
                print(f"  [ERRO] Capítulo {n} não encontrado: {cap_path}")

    if encontrados != total_caps:
        print(f"[ERRO] Foram encontrados {encontrados}/{total_caps} capítulos — abortando para garantir R1.")
        sys.exit(1)

    livro = f"""# {titulo}

*{subtitulo}*

{prefacio}

{sumario_texto}

{chr(10).join(corpo)}

{conc}
"""

    md_path = DIR_LIVRO / "livro_final.md"
    md_path.write_text(livro, encoding="utf-8")
    print(f"[OK] livro_final.md salvo: {md_path}")
    print(f"     Tamanho: {md_path.stat().st_size/1024:.0f} KB | Caracteres: {len(livro)}")
    print(f"     Partes: {total_partes} | Capítulos: {total_caps}")


if __name__ == "__main__":
    main()
