#!/usr/bin/env python3
"""
Gera capa de ebook no padrão Editora Agêntica: flat 2D, sem orbs, sem mockup de terminal.
Mesmo estilo do livro Oh My Pi.

Padrão:
- Fundo #0d1117
- Barra colorida topo (8px) + rodapé (6px)
- Padding lateral: 80px
- Título e autor à esquerda, número da edição e ano à direita
- Título Inter 900 72px
- Autor Inter 600 18px
- Cargo Inter 600 11px (cor do accent)
"""
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERRO] playwright não instalado")
    sys.exit(1)


def gerar_capa_ebook(
    titulo,
    subtitulo,
    cor_acento,
    edicao,
    dir_saida,
):
    """Gera capa no padrão exato: flat 2D, código flutuante à direita, terminal à esquerda."""
    
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600;700;900&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ 
    width: 1200px; height: 1600px; 
    background: #0d1117; 
    font-family: 'Inter', sans-serif; 
    position: relative; 
    overflow: hidden;
  }}
  
  /* Barras topo e rodapé */
  .top-bar {{ position: absolute; top: 0; left: 0; width: 100%; height: 8px; background: {cor_acento}; }}
  .bottom-bar {{ position: absolute; bottom: 0; left: 0; width: 100%; height: 6px; background: {cor_acento}; }}
  
  /* Container principal com padding generoso */
  .content {{
    position: absolute;
    top: 50px;
    bottom: 50px;
    left: 80px;
    right: 80px;
    display: flex;
    flex-direction: column;
  }}
  
  .header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 30px;
  }}
  .editora-icon {{ 
    width: 44px; height: 44px; 
    border: 2px solid {cor_acento}; 
    border-radius: 10px; 
    display: flex; align-items: center; justify-content: center; 
    font-size: 20px; color: {cor_acento}; font-weight: 700; 
    font-family: 'JetBrains Mono', monospace; 
  }}
  .editora-text {{ font-size: 14px; font-weight: 600; color: #8b949e; letter-spacing: 3px; text-transform: uppercase; }}
  
  .main {{
    flex: 1;
    display: flex;
    gap: 40px;
    min-height: 0;
  }}
  
  .left {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-width: 0;
  }}
  
  .right {{
    width: 350px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    padding-top: 20px;
    min-width: 0;
  }}
  
  /* Título: Inter 900 72px - COR DO ACCENT */
  .title {{ 
    font-family: 'Inter', sans-serif;
    font-size: 72px; 
    font-weight: 900; 
    color: {cor_acento}; 
    line-height: 1.05;
    letter-spacing: -1px;
    margin-bottom: 12px;
  }}
  .subtitle {{ font-size: 18px; font-weight: 300; color: #8b949e; margin-bottom: 16px; }}
  .divider {{ width: 80px; height: 4px; background: {cor_acento}; margin-bottom: 16px; }}
  
  /* Autor: Inter 600 18px */
  .author-name {{ 
    font-family: 'Inter', sans-serif;
    font-size: 18px; 
    font-weight: 600; 
    color: #e6edf3; 
    margin-bottom: 4px; 
  }}
  /* Cargo: Inter 600 11px cor accent */
  .author-role {{ 
    font-family: 'Inter', sans-serif;
    font-size: 11px; 
    color: {cor_acento}; 
    letter-spacing: 2px; 
    text-transform: uppercase; 
    font-weight: 600; 
  }}
  
  .edicao {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {cor_acento};
    text-align: right;
  }}
</style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="bottom-bar"></div>
  <div class="content">
    <div class="header">
      <div class="editora-icon">&gt;_</div>
      <div class="editora-text">Editora Agêntica</div>
    </div>
    
    <div class="main">
      <div class="left">
        <div class="title">{titulo}</div>
        <div class="subtitle">{subtitulo}</div>
        <div class="divider"></div>
        <div class="author-name">Heverton Eduardo Peres</div>
        <div class="author-role">Engenheiro de Software & Maker</div>
      </div>

      <div class="right">
        <div class="edicao">{edicao}</div>
      </div>
    </div>
  </div>
</body>
</html>'''
    
    dir_saida = Path(dir_saida)
    dir_saida.mkdir(parents=True, exist_ok=True)
    (dir_saida / "imagens").mkdir(exist_ok=True)
    
    html_file = dir_saida / "capa.html"
    html_file.write_text(html, encoding="utf-8")
    
    png_file = dir_saida / "imagens" / "capa.png"
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 1600})
        page.goto(f"file:///{html_file.resolve().as_posix()}")
        page.wait_for_timeout(2000)
        page.screenshot(path=str(png_file))
        browser.close()
    
    print(f"[OK] {png_file.name} ({png_file.stat().st_size // 1024} KB)")
    return png_file


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("titulo")
    ap.add_argument("subtitulo")
    ap.add_argument("--cor", default="#58a6ff")
    ap.add_argument("--edicao", default="1ª Edição · 2026")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    gerar_capa_ebook(
        titulo=args.titulo,
        subtitulo=args.subtitulo,
        cor_acento=args.cor,
        edicao=args.edicao,
        dir_saida=args.output,
    )
