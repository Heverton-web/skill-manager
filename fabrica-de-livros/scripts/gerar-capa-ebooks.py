#!/usr/bin/env python3
"""Gera capa grafica para os e-books derivados do livro-mae (1:1,6, 1600x2560px)
e para o proprio livro-mae (A4, 1600x2263px) — mesmo padrao visual da serie.

Zera a pendencia R-EBK-2 (capa ausente) do fluxo gerar-epub.py. Deterministico
(seed fixa), usa apenas Pillow + fontes do Windows — sem servicos externos.

Uso:
    python scripts/gerar-capa-ebooks.py <slug-livro-mae>               # capas dos ebooks
    python scripts/gerar-capa-ebooks.py <slug-livro-mae> --ebook 3     # um ebook so
    python scripts/gerar-capa-ebooks.py <slug-livro-mae> --livro-mae   # capa A4 do livro-mae
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"
FONT_DIR = Path(r"C:\Windows\Fonts")

LARGURA, ALTURA = 1600, 2560        # proporcao 1:1,6 (padrao de e-commerce de ebooks)
LARGURA_A4, ALTURA_A4 = 1600, 2263  # proporcao A4 (1:1,414) para a capa do livro-mae

# Paletas (fundo superior, fundo inferior, cor de destaque, cor de texto)
PALETAS = [
    ("#0b1020", "#1b2a4a", "#5b8def", "#f4f7ff"),  # 1 - azul profundo
    ("#14081d", "#2d1145", "#b06df0", "#faf5ff"),  # 2 - roxo
    ("#04140f", "#0e3328", "#2ecc9a", "#eafff7"),  # 3 - verde esmeralda
    ("#1a0d04", "#3d2107", "#f0933b", "#fff6ea"),  # 4 - laranja/cobre
    ("#140d2e", "#32206b", "#7c6cf0", "#f1eeff"),  # 5 - indigo
    ("#1d0505", "#4a1210", "#e05d5d", "#fff0f0"),  # 6 - vermelho vinho
    ("#061a20", "#0d3b48", "#37c3d6", "#eafcff"),  # 7 - ciano petroleo
    ("#101418", "#26313c", "#8fa8c0", "#f2f7fc"),  # 8 - grafite aço
]

# Paleta padrao EDITORA AGENTICA: fundo matte escuro (#0d1117/#0f172a)
# com destaque verde-terminal — sem faixas laterais, capa 2D flat.
PALETA_EDITORA = ("#0d1117", "#0f172a", "#2ecc9a", "#f0f6ff")

FONTES = {
    "bold": FONT_DIR / "arialbd.ttf",
    "regular": FONT_DIR / "arial.ttf",
    "light": FONT_DIR / "calibril.ttf",
}


def fonte(nome, tamanho):
    caminho = FONTES[nome]
    if caminho.exists():
        return ImageFont.truetype(str(caminho), tamanho)
    return ImageFont.load_default()


def hex_para_rgb(hexstr):
    hexstr = hexstr.lstrip("#")
    return tuple(int(hexstr[i:i + 2], 16) for i in (0, 2, 4))


def interpolar(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def pintar_fundo_gradiente(draw, c_topo, c_base, largura=LARGURA, altura=ALTURA):
    for y in range(altura):
        cor = interpolar(c_topo, c_base, y / altura)
        draw.line([(0, y), (largura, y)], fill=cor)


def pintar_orbes(imagem, c_destaque, raio_base=560, alpha=46,
                 largura=LARGURA, altura=ALTURA):
    """Dois 'orbes' translucidos para dar profundidade sem depender de blur caro."""
    fator = altura / ALTURA
    for (cx, cy, raio, a) in [
        (largura * 0.82, altura * 0.20, raio_base * fator, alpha),
        (largura * 0.10, altura * 0.78, raio_base * 0.8 * fator, alpha - 12),
    ]:
        orbe = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        od = ImageDraw.Draw(orbe)
        cor_rgba = c_destaque + (a,)
        od.ellipse([cx - raio, cy - raio, cx + raio, cy + raio], fill=cor_rgba)
        imagem.alpha_composite(orbe)


def pintar_lombada_decorativa(draw, c_destaque, largura=LARGURA, altura=ALTURA):
    """Faixa lateral esquerda fina com padrao de 4 blocos (as 4 camadas)."""
    sx = largura / LARGURA
    sy = altura / ALTURA
    x, y0 = 90 * sx, altura * 0.24
    passo = 96 * sy
    for i in range(6):
        altura_bloco = (26 + (i % 3) * 10) * sy
        cor = interpolar(c_destaque, (255, 255, 255), 0.35 if i % 2 else 0.0)
        draw.rounded_rectangle(
            [x, y0 + i * passo, x + 14 * sx, y0 + i * passo + altura_bloco],
            radius=7 * sy, fill=cor)


def pintar_ilustracao_terminal(draw, cx, y0, c_destaque, sx=1.0, sy=1.0,
                               rotulo="terminal"):
    """Ilustracao vetorial 2D tematica: janela de terminal do harness (CLI).

    Desenhada apenas com primitivas Pillow (retangulos, elipses, texto) —
    flat 2D, sem sombras 3D nem gradientes complexos. O rotulo da barra
    vem da propria obra (nunca texto hardcoded de outro livro).
    """
    larg = int(1010 * sx)
    alt = int(560 * sy)
    x0 = int(cx - larg / 2)
    x1 = x0 + larg
    y1 = int(y0 + alt)
    cor_jan = (13, 18, 25, 255)
    cor_bar = (23, 30, 42, 255)
    f_ttl = fonte("regular", int(30 * sy))
    f_prm = fonte("bold", int(34 * sy))
    f_sta = fonte("regular", int(24 * sy))

    # Janela do terminal
    draw.rounded_rectangle([x0, y0, x1, y1], radius=int(26 * sy), fill=cor_jan,
                           outline=interpolar(c_destaque, (255, 255, 255), 0.45),
                           width=int(4 * sx))
    # Barra de titulo com os tres pontos classicos
    tb_h = int(72 * sy)
    draw.rounded_rectangle([x0, y0, x1, y0 + tb_h], radius=int(26 * sy), fill=cor_bar)
    draw.rectangle([x0, y0 + tb_h - int(26 * sy), x1, y0 + tb_h], fill=cor_bar)
    for i, cor in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        px = x0 + int((36 + i * 54) * sx)
        py = y0 + int(tb_h / 2)
        r = int(10 * sy)
        draw.ellipse([px - r, py - r, px + r, py + r], fill=cor)
    draw.text((x0 + int(220 * sx), y0 + int(20 * sy)),
              f"{rotulo} — harness de codigo", font=f_ttl, fill=(190, 205, 224, 255))

    # Linha de prompt
    ly = y0 + tb_h + int(58 * sy)
    draw.text((x0 + int(58 * sx), ly), f"> {rotulo} run \"refatore o modulo de auth\"",
              font=f_prm, fill=c_destaque)
    # Linhas de saida (barras de codigo)
    for i, frac in enumerate([0.84, 0.64, 0.74, 0.48]):
        by = ly + int((76 + i * 64) * sy)
        bw = int((1010 - 116) * sx * frac)
        draw.rounded_rectangle([x0 + int(58 * sx), by, x0 + int(58 * sx) + bw,
                                by + int(24 * sy)], radius=int(12 * sy),
                               fill=(40, 52, 70, 255))
    # Barra de status inferior
    syb = y1 - int(58 * sy)
    draw.rounded_rectangle([x0 + int(58 * sx), syb, x1 - int(58 * sx), syb + int(30 * sy)],
                           radius=int(15 * sy),
                           fill=interpolar(c_destaque, (0, 0, 0), 0.65))
    draw.text((x0 + int(70 * sx), syb + int(5 * sy)),
              "tokens 1.2k  ·  modo build  ·  ~28s", font=f_sta,
              fill=(170, 190, 215, 255))


def quebrar_titulo(texto, fonte_t, max_largura):
    linhas = []
    for paragrafo in texto.split("\n"):
        palavras = paragrafo.split()
        linha_atual = ""
        for palavra in palavras:
            teste = (linha_atual + " " + palavra).strip()
            if fonte_t.getlength(teste) <= max_largura or not linha_atual:
                linha_atual = teste
            else:
                linhas.append(linha_atual)
                linha_atual = palavra
        if linha_atual:
            linhas.append(linha_atual)
    return linhas


def gerar_capa(indice, titulo, autor, slug_ebook, largura=LARGURA, altura=ALTURA,
               subtitulo=None, rodape=None, nome_arquivo="capa.png",
               selo=None, camadas=None, chancela=None, caixa_alta=False,
               sem_lombada=False, ilustracao=False, paleta=None,
               rotulo_ilustracao=None):
    if paleta is None:
        paleta = PALETAS[(indice - 1) % len(PALETAS)]
    c_topo, c_base, c_destaque, c_texto = [hex_para_rgb(x) for x in paleta]
    if caixa_alta:
        titulo = titulo.upper()
    subtitulo = subtitulo or ""
    sx = largura / LARGURA
    sy = altura / ALTURA

    imagem = Image.new("RGBA", (largura, altura), c_topo + (255,))
    draw = ImageDraw.Draw(imagem)

    pintar_fundo_gradiente(draw, c_topo, c_base, largura, altura)
    pintar_orbes(imagem, c_destaque, largura=largura, altura=altura)
    if not sem_lombada:
        pintar_lombada_decorativa(draw, c_destaque, largura, altura)

    # Moldura fina
    cor_moldura = interpolar(c_destaque, (255, 255, 255), 0.6)
    draw.rounded_rectangle([40 * sx, 40 * sy, largura - 40 * sx, altura - 40 * sy],
                           radius=24 * sy, outline=cor_moldura, width=4)

    margem = 150 * sx
    area_titulo_x = margem
    area_titulo_w = largura - 2 * margem

    # Chancela da editora (topo) — padrao EDITORA AGENTICA
    y_titulo_inicio = 300 * sy
    if chancela:
        f_chan = fonte("bold", int(46 * sy))
        draw.text((margem, 150 * sy), chancela.upper(), font=f_chan,
                  fill=interpolar(c_destaque, (255, 255, 255), 0.55))
        draw.line([(margem, 244 * sy), (margem + 300 * sx, 244 * sy)],
                  fill=c_destaque, width=8)
        y_titulo_inicio = 360 * sy

    # Selo (topo) — opcional, so aparece se a obra pertencer a uma serie nomeada
    if selo:
        f_selo = fonte("bold", int(44 * sy))
        draw.text((margem, 220 * sy), selo.upper(), font=f_selo,
                  fill=interpolar(c_destaque, (255, 255, 255), 0.5))
        draw.line([(margem, 310 * sy), (margem + 260 * sx, 310 * sy)], fill=c_destaque, width=8)
        y_titulo_inicio = 430 * sy

    # Titulo principal
    f_titulo = fonte("bold", int(128 * sy))
    linhas = quebrar_titulo(titulo, f_titulo, area_titulo_w)
    if len(linhas) > 4:
        f_titulo = fonte("bold", int(104 * sy))
        linhas = quebrar_titulo(titulo, f_titulo, area_titulo_w)
    y = y_titulo_inicio
    altura_linha = 150 * sy
    for linha in linhas[:5]:
        draw.text((area_titulo_x, y), linha, font=f_titulo, fill=c_texto)
        y += altura_linha

    # Divisa
    y += 20 * sy
    draw.line([(margem, y), (margem + 200 * sx, y)], fill=c_destaque, width=8)
    y += 70 * sy

    # Subtitulo — opcional, derivado da obra (nunca texto fixo de outro livro)
    if subtitulo:
        f_sub = fonte("light", int(52 * sy))
        linhas_sub = quebrar_titulo(subtitulo, f_sub, area_titulo_w)[:3]
        for linha in linhas_sub:
            draw.text((area_titulo_x, y), linha, font=f_sub,
                      fill=interpolar(c_texto, (0, 0, 0), 0.25))
            y += 66 * sy
        y += 24 * sy

    # Camadas/tags — opcional, so se a obra fornecer
    if camadas:
        f_camadas = fonte("bold", int(44 * sy))
        draw.text((area_titulo_x, y), camadas, font=f_camadas,
                  fill=interpolar(c_destaque, (255, 255, 255), 0.35))
        y += 80 * sy

    # Ilustracao vetorial 2D tematica (padrao EDITORA AGENTICA)
    if ilustracao:
        y_ilust = max(y + 60 * sy, altura * 0.52)
        pintar_ilustracao_terminal(draw, largura / 2, y_ilust, c_destaque,
                                   sx, sy, rotulo=rotulo_ilustracao or "terminal")

    # Rodape: autor
    f_autor = fonte("regular", int(56 * sy))
    nome = rodape or f"{autor}  ·  Volume {indice}"
    draw.text((margem, altura - 340 * sy), nome, font=f_autor, fill=c_texto)

    destino = DIR_OUTPUT / slug_ebook / "imagens"
    destino.mkdir(parents=True, exist_ok=True)
    caminho = destino / nome_arquivo
    imagem.convert("RGB").save(caminho, "PNG")
    return caminho


def gerar_thumbnail(caminho_capa, largura=300):
    """Miniatura da capa (mesma proporcao, redimensionada) para catalogo/loja/preview."""
    nome_thumb = caminho_capa.stem.replace("capa", "thumbnail") + caminho_capa.suffix
    destino = caminho_capa.with_name(nome_thumb)
    with Image.open(caminho_capa) as img:
        altura = round(img.height * (largura / img.width))
        thumb = img.resize((largura, altura), Image.LANCZOS)
        thumb.convert("RGB").save(destino, "PNG", optimize=True)
    return destino


def gerar_capa_livro_mae(slug_livro_mae):
    """Capa A4 do livro-mae no padrao EDITORA AGENTICA: 2D flat, fundo matte
    escuro, chancela, titulo em caixa alta, ilustracao tematica e autor
    obrigatorio no rodape. Sem lombadas 3D nem faixas laterais."""
    dir_obra = DIR_OUTPUT / slug_livro_mae
    sumario = {}
    sum_path = dir_obra / "sumario_macro.json"
    if sum_path.exists():
        try:
            sumario = json.loads(sum_path.read_text(encoding="utf-8"))
        except ValueError:
            sumario = {}
    titulo = sumario.get("titulo_obra") or slug_livro_mae
    # Titulo curto (antes de ":") em caixa alta + subtitulo derivado da obra
    titulo_curto = titulo
    subtitulo = sumario.get("subtitulo") or ""
    if ":" in titulo:
        titulo_curto, resto = titulo.split(":", 1)
        subtitulo = (subtitulo or resto.strip())
    autor = "Heverton Eduardo Peres"
    caminho = gerar_capa(
        1, titulo_curto, autor, slug_livro_mae,
        largura=LARGURA_A4, altura=ALTURA_A4,
        subtitulo=subtitulo,
        rodape=autor,
        nome_arquivo="capa_livro.png",
        chancela="EDITORA AGÊNTICA",
        caixa_alta=True,
        sem_lombada=True,
        ilustracao=True,
        paleta=PALETA_EDITORA,
        rotulo_ilustracao=titulo_curto.lower(),
    )
    thumb = gerar_thumbnail(caminho)
    print(f"  [OK] livro-mae: capa A4 {caminho.relative_to(DIR_PROJETO)} "
          f"({LARGURA_A4}x{ALTURA_A4}px) + thumbnail {thumb.name}")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Gera capas graficas da serie (ebooks 1:1,6 e livro-mae A4)")
    ap.add_argument("slug_livro_mae")
    ap.add_argument("--ebook", type=int, default=None,
                    help="indice do ebook (default: todos)")
    ap.add_argument("--livro-mae", action="store_true",
                    help="gera apenas a capa A4 do livro-mae (imagens/capa_livro.png)")
    args = ap.parse_args()

    if args.livro_mae:
        return gerar_capa_livro_mae(args.slug_livro_mae)

    dir_mae = DIR_OUTPUT / args.slug_livro_mae
    derivados = json.loads((dir_mae / "derivados.json").read_text(encoding="utf-8"))
    ebooks = derivados.get("ebooks", {}).get("itens", [])

    alvos = ebooks if args.ebook is None else [
        e for e in ebooks if e["indice"] == args.ebook]
    if not alvos:
        print(f"[ERRO] Nenhum ebook encontrado (ebook={args.ebook})")
        return 1

    for e in alvos:
        i = e["indice"]
        dir_ebook = DIR_OUTPUT / e["diretorio"]
        meta = {}
        meta_path = dir_ebook / "ebook_metadados.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        titulo = meta.get("titulo") or e.get("titulo") or f"E-book {i}"
        autor = meta.get("autor", "Heverton Eduardo Peres")
        subtitulo = meta.get("subtitulo") or e.get("subtitulo") or ""
        selo = meta.get("selo_serie") or derivados.get("selo_serie")
        caminho = gerar_capa(i, titulo, autor, e["diretorio"],
                             subtitulo=subtitulo, selo=selo)
        thumb = gerar_thumbnail(caminho)
        print(f"  [OK] ebook_{i}: capa {caminho.relative_to(DIR_PROJETO)} + thumbnail {thumb.name}")

    print("CONCLUIDO: capas 1:1,6 + thumbnails geradas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
