#!/usr/bin/env python3
"""
Gera ilustrações 2D flat ÚNICAS para cada capítulo usando HTML/CSS + Playwright.

Diferente da versão anterior, esta lê o conteúdo de cada capítulo e gera
ilustrações contextualizadas, não o mesmo template genérico.

Uso:
    python scripts/gerar-ilustracoes.py <slug>                    # todos os capítulos
    python scripts/gerar-ilustracoes.py <slug> --capitulo 5       # um capítulo
    python scripts/gerar-ilustracoes.py <slug> --validar          # apenas verificar
"""

import argparse
import hashlib
import re
import sys
import tempfile
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    TEM_PLAYWRIGHT = True
except ImportError:
    TEM_PLAYWRIGHT = False

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

# ── Cores padrão Editora Agêntica ──────────────────────────────────
COR_FUNDO = "#0d1117"
COR_FUNDO_BOX = "#161b22"
COR_BORDA = "#30363d"
COR_TEXTO = "#e6edf3"
COR_TEXTO2 = "#8b949e"
COR_VERDE = "#2ecc9a"
COR_AZUL = "#58a6ff"
COR_AMARELO = "#f0b429"
COR_ROXO = "#a855f7"

# ── Mapa de conceitos por capítulo (extraído do sumário_macro) ──────
CONCEITOS_CAPITULOS = {
    1: {
        "titulo": "O que é um Coding Agent",
        "tema": "agentes",
        "itens": ["LLM", "Ferramentas", "Contexto", "Loop"],
        "cor_acento": COR_VERDE,
    },
    2: {
        "titulo": "Instalação e Configuração",
        "tema": "setup",
        "itens": ["npm", "API Key", "Provider", "Profile"],
        "cor_acento": COR_AZUL,
    },
    3: {
        "titulo": "Primeiras Interações: Prompting Eficaz",
        "tema": "prompts",
        "itens": ["Contexto", "Instrução", "Restrições", "Formato"],
        "cor_acento": COR_AMARELO,
    },
    4: {
        "titulo": "Ferramentas do Agente",
        "tema": "ferramentas",
        "itens": ["read", "edit", "bash", "grep", "glob"],
        "cor_acento": COR_ROXO,
    },
    5: {
        "titulo": "Sub-agentes: Paralelismo e Tarefas",
        "tema": "paralelismo",
        "itens": ["Task", "Actor", "Spawn", "Wait", "Send"],
        "cor_acento": COR_VERDE,
    },
    6: {
        "titulo": "Memória e Sessões",
        "tema": "memoria",
        "itens": ["Sessão", "Checkpoint", "Memory", "Context"],
        "cor_acento": COR_AZUL,
    },
    7: {
        "titulo": "Plugins: Expandindo o Agente",
        "tema": "plugins",
        "itens": ["Install", "Hooks", "Extensions", "Config"],
        "cor_acento": COR_AMARELO,
    },
    8: {
        "titulo": "Skills: Conhecimento Especializado",
        "tema": "skills",
        "itens": ["SKILL.md", "Trigger", "Compose", "Load"],
        "cor_acento": COR_ROXO,
    },
    9: {
        "titulo": "Automação de Pipelines",
        "tema": "automacao",
        "itens": ["Cron", "Workflow", "CI/CD", "Hook"],
        "cor_acento": COR_VERDE,
    },
    10: {
        "titulo": "O Futuro dos Coding Agents",
        "tema": "futuro",
        "itens": ["Autônomo", "Multi-modal", "Self-improving", "MCP"],
        "cor_acento": COR_AZUL,
    },
}


def criar_html_ilustracao(cap_num, conceitos):
    """Gera HTML único baseado nos conceitos do capítulo."""
    titulo = conceitos["titulo"]
    itens = conceitos["itens"]
    cor = conceitos["cor_acento"]
    tema = conceitos["tema"]

    # Layout variado por tema
    if tema == "agentes":
        # Arquitetura: caixas conectadas
        boxes_html = ""
        for i, item in enumerate(itens):
            x = 100 + i * 260
            boxes_html += f'''
            <div style="position:absolute; left:{x}px; top:280px; width:220px; 
                        background:{COR_FUNDO_BOX}; border:2px solid {cor}; border-radius:12px;
                        padding:20px; text-align:center;">
                <div style="color:{cor}; font-size:14px; font-weight:600; margin-bottom:8px;">{item}</div>
                <div style="width:60px; height:4px; background:{cor}; margin:0 auto; border-radius:2px;"></div>
            </div>'''
            if i < len(itens) - 1:
                boxes_html += f'''
                <div style="position:absolute; left:{x + 220}px; top:295px; 
                            color:{COR_VERDE}; font-size:24px;">→</div>'''

        conteudo = f'''
        <h2 style="position:absolute; top:80px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <p style="position:absolute; top:140px; left:60px; color:{COR_TEXTO2}; font-size:18px;">
            Arquitetura de um coding agent moderno
        </p>
        {boxes_html}
        <div style="position:absolute; bottom:120px; left:60px; right:60px; 
                    border-top:1px solid {COR_BORDA}; padding-top:20px;">
            <span style="color:{COR_VERDE}; font-size:14px;">●</span>
            <span style="color:{COR_TEXTO2}; font-size:14px; margin-left:8px;">
                Cada componente trabalha em conjunto para criar um agente autônomo
            </span>
        </div>'''

    elif tema == "setup":
        # Terminal com comandos
        conteudo = f'''
        <h2 style="position:absolute; top:60px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <div style="position:absolute; top:160px; left:60px; width:500px;
                    background:{COR_FUNDO_BOX}; border:1px solid {COR_BORDA}; border-radius:12px;
                    padding:20px; font-family:monospace;">
            <div style="color:{COR_TEXTO2}; font-size:13px; margin-bottom:12px;">
                <span style="color:{COR_VERDE};">$</span> npm install -g omp
            </div>
            <div style="color:{COR_TEXTO2}; font-size:13px; margin-bottom:12px;">
                <span style="color:{COR_VERDE};">$</span> omp --model claude
            </div>
            <div style="color:{COR_TEXTO2}; font-size:13px; margin-bottom:12px;">
                <span style="color:{COR_AMARELO};">✓</span> <span style="color:{COR_VERDE};">Pronto!</span>
            </div>
        </div>
        <div style="position:absolute; top:160px; right:60px; width:300px;">
            {"".join(f'<div style="margin-bottom:16px; padding:16px; background:{COR_FUNDO_BOX}; border-radius:8px; border-left:3px solid {cor};"><div style="color:{cor}; font-size:14px; font-weight:600;">{item}</div></div>' for item in itens)}
        </div>'''

    elif tema == "prompts":
        # Fluxo de prompt
        conteudo = f'''
        <h2 style="position:absolute; top:60px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <div style="position:absolute; top:180px; left:60px; display:flex; gap:40px;">
            {"".join(f'''
            <div style="text-align:center;">
                <div style="width:100px; height:100px; border-radius:50%; background:{COR_FUNDO_BOX}; 
                            border:2px solid {cor}; display:flex; align-items:center; justify-content:center;
                            margin:0 auto 12px;">
                    <span style="color:{cor}; font-size:28px;">{i+1}</span>
                </div>
                <div style="color:{COR_TEXTO}; font-size:14px; font-weight:600;">{item}</div>
            </div>''' for i, item in enumerate(itens))}
        </div>
        <div style="position:absolute; bottom:100px; left:60px; right:60px; padding:20px;
                    background:{COR_FUNDO_BOX}; border-radius:8px; border:1px solid {COR_BORDA};">
            <span style="color:{cor}; font-weight:600;">Dica:</span>
            <span style="color:{COR_TEXTO2};"> Um bom prompt é como uma boa receita — claro, específico e completo.</span>
        </div>'''

    elif tema == "ferramentas":
        # Grid de ferramentas
        cores = [COR_VERDE, COR_AZUL, COR_AMARELO, COR_ROXO, COR_VERDE]
        conteudo = f'''
        <h2 style="position:absolute; top:60px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <div style="position:absolute; top:160px; left:60px; display:grid; 
                    grid-template-columns:repeat(3, 1fr); gap:20px; width:600px;">
            {"".join(f'''
            <div style="background:{COR_FUNDO_BOX}; border:2px solid {cores[i]}; border-radius:12px;
                        padding:20px; text-align:center;">
                <div style="color:{cores[i]}; font-size:24px; margin-bottom:8px;">⚡</div>
                <div style="color:{COR_TEXTO}; font-size:16px; font-weight:600;">{item}</div>
            </div>''' for i, item in enumerate(itens))}
        </div>'''

    elif tema == "paralelismo":
        # Sub-agentes ramificando
        conteudo = f'''
        <h2 style="position:absolute; top:60px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <div style="position:absolute; top:200px; left:50%; transform:translateX(-50%); text-align:center;">
            <div style="width:140px; height:60px; background:{COR_FUNDO_BOX}; border:2px solid {cor};
                        border-radius:8px; margin:0 auto; display:flex; align-items:center; justify-content:center;">
                <span style="color:{cor}; font-weight:600;">Orquestrador</span>
            </div>
            <div style="color:{COR_VERDE}; font-size:32px; margin:16px 0;">↓ ↓ ↓</div>
            <div style="display:flex; gap:60px; justify-content:center;">
                {"".join(f'''
                <div style="width:120px; height:50px; background:{COR_FUNDO_BOX}; border:2px solid {COR_AZUL};
                            border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <span style="color:{COR_AZUL}; font-size:13px;">{item}</span>
                </div>''' for item in itens[:3])}
            </div>
        </div>'''

    elif tema == "memoria":
        # Camadas de memória
        conteudo = f'''
        <h2 style="position:absolute; top:60px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <div style="position:absolute; top:180px; left:60px;">
            {"".join(f'''
            <div style="margin-bottom:16px; padding:20px 40px; background:{COR_FUNDO_BOX}; 
                        border-left:4px solid {cor}; border-radius:0 8px 8px 0; width:500px;">
                <span style="color:{cor}; font-weight:600; font-size:18px;">{item}</span>
                <span style="color:{COR_TEXTO2}; font-size:14px; margin-left:12px;">{'Volátil' if i == 0 else 'Persistente' if i == 1 else 'Híbrido' if i == 2 else 'Distribuído'}</span>
            </div>''' for i, item in enumerate(itens))}
        </div>'''

    elif tema == "plugins":
        # Ecossistema modular
        conteudo = f'''
        <h2 style="position:absolute; top:60px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <div style="position:absolute; top:200px; left:50%; transform:translateX(-50%);">
            <div style="width:120px; height:120px; border-radius:50%; background:{COR_FUNDO_BOX}; 
                        border:3px solid {cor}; display:flex; align-items:center; justify-content:center;
                        margin:0 auto;">
                <span style="color:{cor}; font-size:14px; font-weight:600;">Core</span>
            </div>
            <div style="display:flex; gap:40px; margin-top:30px;">
                {"".join(f'''
                <div style="text-align:center;">
                    <div style="width:80px; height:80px; border-radius:50%; background:{COR_FUNDO_BOX}; 
                                border:2px solid {COR_AZUL}; display:flex; align-items:center; justify-content:center;">
                        <span style="color:{COR_AZUL}; font-size:11px;">{item}</span>
                    </div>
                </div>''' for item in itens)}
            </div>
        </div>'''

    elif tema == "skills":
        # Biblioteca de conhecimento
        conteudo = f'''
        <h2 style="position:absolute; top:60px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <div style="position:absolute; top:180px; left:60px; display:grid;
                    grid-template-columns:repeat(2, 1fr); gap:20px; width:500px;">
            {"".join(f'''
            <div style="background:{COR_FUNDO_BOX}; border:1px solid {COR_BORDA}; border-radius:8px;
                        padding:16px; border-top:3px solid {cor};">
                <div style="color:{cor}; font-size:14px; font-weight:600;">{item}</div>
                <div style="color:{COR_TEXTO2}; font-size:12px; margin-top:4px;">
                    {'Carrega sob demanda' if i == 0 else 'Ativa por palavra-chave' if i == 1 else 'Combina workflows' if i == 2 else 'Invoca via /skill'}
                </div>
            </div>''' for i, item in enumerate(itens))}
        </div>'''

    elif tema == "automacao":
        # Pipeline linear
        conteudo = f'''
        <h2 style="position:absolute; top:60px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <div style="position:absolute; top:220px; left:60px; display:flex; align-items:center; gap:20px;">
            {"".join(f'''
            <div style="text-align:center;">
                <div style="width:100px; height:100px; border-radius:12px; background:{COR_FUNDO_BOX};
                            border:2px solid {cor}; display:flex; align-items:center; justify-content:center;">
                    <span style="color:{cor}; font-size:14px; font-weight:600;">{item}</span>
                </div>
            </div>
            <div style="color:{COR_VERDE}; font-size:28px;">→</div>
            ''' for i, item in enumerate(itens))}
            <div style="width:100px; height:100px; border-radius:12px; background:{cor};
                        display:flex; align-items:center; justify-content:center;">
                <span style="color:{COR_FUNDO}; font-size:14px; font-weight:700;">Deploy</span>
            </div>
        </div>'''

    elif tema == "futuro":
        # Timeline
        conteudo = f'''
        <h2 style="position:absolute; top:60px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <div style="position:absolute; top:200px; left:60px; right:60px;">
            <div style="height:4px; background:{COR_BORDA}; border-radius:2px; margin-bottom:40px;"></div>
            <div style="display:flex; justify-content:space-between;">
                {"".join(f'''
                <div style="text-align:center; width:120px;">
                    <div style="width:16px; height:16px; border-radius:50%; background:{cor};
                                margin:0 auto -22px; position:relative; z-index:1;"></div>
                    <div style="margin-top:30px; color:{COR_TEXTO}; font-size:14px; font-weight:600;">{item}</div>
                </div>''' for item in itens)}
            </div>
        </div>'''

    else:
        # Fallback genérico
        conteudo = f'''
        <h2 style="position:absolute; top:60px; left:60px; color:{COR_TEXTO}; font-size:36px;">
            {titulo}
        </h2>
        <div style="position:absolute; top:200px; left:60px;">
            {"".join(f'<div style="margin-bottom:12px; color:{COR_TEXTO}; font-size:18px;">• {item}</div>' for item in itens)}
        </div>'''

    html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:1200px; height:800px; background:{COR_FUNDO}; font-family:'Segoe UI',Arial,sans-serif; 
         position:relative; overflow:hidden; }}
</style></head><body>
{conteudo}
</body></html>'''

    return html


def renderizar_png(html_content, caminho_png):
    """Renderiza HTML para PNG usando Playwright."""
    if not TEM_PLAYWRIGHT:
        print("  [AVISO] Playwright nao instalado")
        return False

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_content)
        caminho_html = f.name

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1200, "height": 800})
            page.goto(f"file:///{caminho_html.replace(chr(92), '/')}")
            page.wait_for_timeout(500)
            page.screenshot(path=str(caminho_png))
            browser.close()
        return True
    except Exception as e:
        print(f"  [ERRO] {e}")
        return False
    finally:
        Path(caminho_html).unlink(missing_ok=True)


def gerar_ilustracoes_capitulo(slug, num_cap, cor_acento=None):
    """Gera ilustração única para um capítulo."""
    dir_obra = DIR_OUTPUT / slug
    dir_ilust = dir_obra / "imagens" / "ilustracoes"
    dir_ilust.mkdir(parents=True, exist_ok=True)

    conceitos = CONCEITOS_CAPITULOS.get(num_cap)
    if not conceitos:
        print(f"  [AVISO] Cap {num_cap:02d} sem conceitos definidos")
        return 0

    # Usar cor do accent se fornecida, senão usar a cor do capítulo
    if cor_acento:
        conceitos["cor_acento"] = cor_acento

    html = criar_html_ilustracao(num_cap, conceitos)
    png = dir_ilust / f"ilust_{num_cap:02d}_1.png"
    
    if renderizar_png(html, png):
        print(f"  [OK] ilust_{num_cap:02d}_1.png ({conceitos['tema']}, {conceitos['cor_acento']})")
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description="Gera ilustracoes 2D flat unicas por capitulo")
    ap.add_argument("slug")
    ap.add_argument("--capitulo", type=int, default=None)
    ap.add_argument("--cor", default=None, help="Cor de accent para todas as ilustracoes (ex: #58a6ff)")
    ap.add_argument("--validar", action="store_true")
    args = ap.parse_args()

    dir_obra = DIR_OUTPUT / args.slug
    if not dir_obra.exists():
        print(f"[ERRO] Obra nao encontrada: {dir_obra}")
        return 1

    if args.validar:
        dir_ilust = dir_obra / "imagens" / "ilustracoes"
        if dir_ilust.exists():
            ilusts = list(dir_ilust.glob("ilust_*.png"))
            print(f"Ilustracoes: {len(ilusts)}")
            for i in ilusts:
                print(f"  {i.name}")
        else:
            print("Nenhuma ilustracao")
        return 0

    caps = [args.capitulo] if args.capitulo else range(1, 11)
    total = 0
    for n in caps:
        print(f"Capitulo {n:02d}...")
        total += gerar_ilustracoes_capitulo(args.slug, n, args.cor)

    print(f"\nCONCLUIDO: {total} ilustracao(oes) unica(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
