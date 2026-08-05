#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from PIL import Image

DIR_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_PROJETO / "scripts"))

import importlib
gerar_padrao = importlib.import_module("gerar-capa-ebook-padrao")
gerar_capa_ebook = gerar_padrao.gerar_capa_ebook


def gerar_thumbnail(caminho_capa, largura=300):
    nome_thumb = caminho_capa.stem.replace("capa", "thumbnail") + caminho_capa.suffix
    destino = caminho_capa.with_name(nome_thumb)
    with Image.open(caminho_capa) as img:
        altura = round(img.height * (largura / img.width))
        thumb = img.resize((largura, altura), Image.LANCZOS)
        thumb.convert("RGB").save(destino, "PNG", optimize=True)
    return destino


eb_dir = DIR_PROJETO / "output" / "ebooks" / "marketing-na-era-digital--eb-01-fundamentos-o-novo-territorio"

titulo = "MARKETING NA ERA DIGITAL"
subtitulo = "Fundamentos & O Novo Território: Estratégia, Jornada e Canais"
cor = "#f0933b"  # Laranja Marketing / Growth

cmd = "marketing-suite analyze --domain digital-routes"
output = [
    "Funnel: Attract -> Engage -> Convert -> Retain",
    "Traffic: 125k visitors | CTR: 4.8% | LTV/CAC: 4.2x",
    "SEO & Organic Reach: 98/100 | ROI: +312%"
]

marketing_side = """<span class="kw">STRATEGY</span>: Digital Routes<br>
<span class="str">DOMAINS</span>: 10 Pillars<br>
-------------------<br>
<span class="hl">01. INTENT & SEARCH</span><br>
<span class="cm">SEO, Content & Demand</span><br>
<span class="hl">02. SOCIAL LANDSCAPE</span><br>
<span class="cm">Community & Branding</span><br>
<span class="hl">03. CONVERSION PORTS</span><br>
<span class="str">Offers, CRO & Copy</span><br>
<span class="hl">04. RETENTION & LTV</span><br>
<span class="cm">Email & Customer Unit</span><br>
-------------------<br>
<span class="fn">ROI Target</span>: <span class="str">+350%</span>"""

png_capa = gerar_capa_ebook(
    titulo=titulo,
    subtitulo=subtitulo,
    cor_acento=cor,
    terminal_cmd=cmd,
    terminal_output=output,
    code_snippet=marketing_side,
    dir_saida=eb_dir,
)
thumb = gerar_thumbnail(png_capa)
print(f"[OK] Capa de Marketing gerada com sucesso: {png_capa}")
