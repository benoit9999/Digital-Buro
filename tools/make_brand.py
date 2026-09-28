"""
Génère les éléments de marque à partir de la police Inter (contours vectorisés) :
  - src/assets/img/logo.svg          (logo encre, pour fond clair)
  - src/assets/img/logo-white.svg    (logo blanc, pour le pied de page sombre)
  - src/static/favicon.svg           (monogramme D-B)
  - src/static/favicon.ico, apple-touch-icon.png, icon-192.png, icon-512.png
  - src/assets/img/og-image.jpg      (image de partage réseaux sociaux 1200x630)

Usage : python tools/make_brand.py <dossier contenant Inter-Display-700.ttf, Inter-Text-*.ttf>
Ce script n'est à relancer que si l'on veut modifier le logo.
"""
import os
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "tools", "fonts")

INK = "#000000"
PAPER = "#ffffff"
EMBER = "#ff5900"
ABYSS = "#000710"


def glyph_run(font, text, tracking_em=0.0):
    """Retourne [(glyphName, x)] et la largeur totale, en unités de police."""
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    upem = font["head"].unitsPerEm
    x = 0
    run = []
    for ch in text:
        name = cmap[ord(ch)]
        run.append((name, x))
        x += hmtx[name][0] + tracking_em * upem
    return run, x - tracking_em * upem


def _num(n):
    s = f"{n:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def path_for(font, name, dx, scale, baseline):
    gs = font.getGlyphSet()
    pen = SVGPathPen(gs, ntos=_num)
    # y inversé (SVG) : (x, y) -> (dx + x*scale, baseline - y*scale)
    tpen = TransformPen(pen, (scale, 0, 0, -scale, dx, baseline))
    gs[name].draw(tpen)
    return pen.getCommands()


def wordmark_svg(font, color_text, color_dash, height=40):
    """Logo « Digital-Buro » : texte vectorisé, trait d'union remplacé par une barre ember."""
    upem = font["head"].unitsPerEm
    os2 = font["OS/2"]
    cap = os2.sCapHeight  # hauteur des capitales
    tracking = -0.02
    left, lw = glyph_run(font, "Digital", tracking)
    right, rw = glyph_run(font, "Buro", tracking)
    gap = 0.075 * upem          # espace de part et d'autre de la barre
    dash_w = 0.30 * upem
    dash_h = 0.115 * upem
    total = lw + gap + dash_w + gap + rw
    # on dimensionne pour que la hauteur des capitales = 72% de la hauteur du SVG
    scale = (height * 0.72) / cap
    baseline = height * 0.86
    width = total * scale
    paths = []
    for name, x in left:
        d = path_for(font, name, x * scale, scale, baseline)
        if d:
            paths.append(d)
    x0 = (lw + gap + dash_w + gap)
    for name, x in right:
        d = path_for(font, name, (x0 + x) * scale, scale, baseline)
        if d:
            paths.append(d)
    # barre ember centrée sur la hauteur d'x
    xh = os2.sxHeight
    dash_x = (lw + gap) * scale
    dash_y = baseline - (xh * 0.52) * scale - (dash_h * scale) / 2
    rx = dash_h * scale * 0.18
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.2f} {height}" '
        f'width="{width:.0f}" height="{height}" role="img" aria-label="Digital-Buro">'
        f'<path fill="{color_text}" d="{" ".join(paths)}"/>'
        f'<rect x="{dash_x:.2f}" y="{dash_y:.2f}" width="{dash_w*scale:.2f}" height="{dash_h*scale:.2f}" rx="{rx:.2f}" fill="{color_dash}"/>'
        "</svg>"
    )
    return svg, width, height


def monogram_svg(font, size=64):
    """Favicon : carré arrondi abyss, « D » et « B » blancs, barre ember entre les deux."""
    upem = font["head"].unitsPerEm
    cap = font["OS/2"].sCapHeight
    d_run, dw = glyph_run(font, "D")
    b_run, bw = glyph_run(font, "B")
    gap = 0.05 * upem
    dash_w = 0.26 * upem
    dash_h = 0.14 * upem
    total = dw + gap + dash_w + gap + bw
    scale = (size * 0.40) / cap
    ox = (size - total * scale) / 2
    baseline = size / 2 + cap * scale / 2
    parts = [path_for(font, "D", ox, scale, baseline)]
    bx = ox + (dw + gap + dash_w + gap) * scale
    parts.append(path_for(font, b_run[0][0], bx, scale, baseline))
    dash_x = ox + (dw + gap) * scale
    dash_y = size / 2 - dash_h * scale / 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
        f'<rect width="{size}" height="{size}" rx="{size*0.22:.1f}" fill="{ABYSS}"/>'
        f'<path fill="{PAPER}" d="{" ".join(parts)}"/>'
        f'<rect x="{dash_x:.2f}" y="{dash_y:.2f}" width="{dash_w*scale:.2f}" height="{dash_h*scale:.2f}" rx="1" fill="{EMBER}"/>'
        "</svg>"
    )


def monogram_png(ttf_path, size, radius_ratio=0.22, pad_ratio=0.0):
    """Version bitmap du monogramme (Pillow), rendue en 4x puis réduite pour un bon anti-crénelage."""
    S = size * 4
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    pad = int(S * pad_ratio)
    dr.rounded_rectangle([pad, pad, S - pad - 1, S - pad - 1], radius=int((S - 2 * pad) * radius_ratio), fill=ABYSS)
    inner = S - 2 * pad
    font = ImageFont.truetype(ttf_path, int(inner * 0.56))
    # mesure
    d_box = dr.textbbox((0, 0), "D", font=font)
    b_box = dr.textbbox((0, 0), "B", font=font)
    cap_h = d_box[3] - d_box[1]
    dw = d_box[2] - d_box[0]
    bw = b_box[2] - b_box[0]
    gap = inner * 0.035
    dash_w = inner * 0.12
    dash_h = inner * 0.065
    total = dw + gap + dash_w + gap + bw
    x = (S - total) / 2
    y_top = (S - cap_h) / 2
    dr.text((x - d_box[0], y_top - d_box[1]), "D", font=font, fill=PAPER)
    dx = x + dw + gap
    dr.rounded_rectangle([dx, S / 2 - dash_h / 2, dx + dash_w, S / 2 + dash_h / 2], radius=int(dash_h * 0.2), fill=EMBER)
    bx = dx + dash_w + gap
    dr.text((bx - b_box[0], y_top - b_box[1]), "B", font=font, fill=PAPER)
    return img.resize((size, size), Image.LANCZOS)


def og_image(fonts_dir, out):
    W, H = 1200, 630
    M = 64  # marge
    img = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(img)
    F = lambda name, size: ImageFont.truetype(os.path.join(fonts_dir, name), size)
    f_disp = F("Inter-Display-600.ttf", 56)
    f_sub = F("Inter-Text-500.ttf", 26)
    f_small = F("Inter-Text-500.ttf", 22)
    f_big = F("Inter-Display-600.ttf", 138)
    f_card = F("Inter-Text-500.ttf", 24)
    f_logo = F("Inter-Display-700.ttf", 40)
    # bandeau sombre en haut (comme la barre d'annonce)
    dr.rectangle([0, 0, W, 60], fill="#15191e")
    dr.text((M, 18), "Chaussée de Charleroi 257 · 1060 Saint-Gilles · 02 534 47 02", font=f_small, fill=PAPER)
    # logo
    x, y = M, 112
    dr.text((x, y), "Digital", font=f_logo, fill=INK)
    w1 = dr.textlength("Digital", font=f_logo)
    dr.rounded_rectangle([x + w1 + 5, y + 24, x + w1 + 5 + 22, y + 32], radius=2, fill=EMBER)
    dr.text((x + w1 + 32, y), "Buro", font=f_logo, fill=INK)
    # carte « 30+ » (à droite)
    w30 = dr.textlength("30", font=f_big)
    wplus = dr.textlength("+", font=f_big)
    cw = int(w30 + wplus + 64)
    cx, cy, ch = W - M - cw, 112, 406
    dr.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill="#f3f3f7")
    dr.text((cx + 30, cy + 40), "30", font=f_big, fill=INK)
    dr.text((cx + 30 + w30 - 4, cy + 40), "+", font=f_big, fill=EMBER)
    dr.text((cx + 32, cy + 300), "ans d’expérience", font=f_card, fill=INK)
    dr.text((cx + 32, cy + 336), "en bureautique", font=f_card, fill="#60646c")
    # titre (à gauche, largeur bornée par la carte)
    ty = 214
    for ln in ["Réparation d’imprimantes,", "PC & Mac à Saint-Gilles."]:
        dr.text((M, ty), ln, font=f_disp, fill=INK)
        ty += 68
    ty += 26
    for ln in ["Toutes marques · En atelier ou sur site", "Cartouches & toners · Bruxelles"]:
        dr.text((M, ty), ln, font=f_sub, fill="#60646c")
        ty += 38
    assert M + dr.textlength("Réparation d’imprimantes,", font=f_disp) < cx - 24, "titre trop large"
    img.save(out, "JPEG", quality=88, optimize=True, progressive=True)


def main():
    disp700 = TTFont(os.path.join(FONTS, "Inter-Display-700.ttf"))
    img_dir = os.path.join(ROOT, "src", "assets", "img")
    static_dir = os.path.join(ROOT, "src", "static")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)

    svg, w, h = wordmark_svg(disp700, INK, EMBER)
    open(os.path.join(img_dir, "logo.svg"), "w", encoding="utf-8").write(svg)
    svg_w, _, _ = wordmark_svg(disp700, PAPER, EMBER)
    open(os.path.join(img_dir, "logo-white.svg"), "w", encoding="utf-8").write(svg_w)
    print(f"logo.svg {w:.0f}x{h}")

    open(os.path.join(static_dir, "favicon.svg"), "w", encoding="utf-8").write(monogram_svg(disp700))

    ttf700 = os.path.join(FONTS, "Inter-Display-700.ttf")
    monogram_png(ttf700, 180, radius_ratio=0.0).convert("RGB").save(os.path.join(static_dir, "apple-touch-icon.png"))
    monogram_png(ttf700, 192).save(os.path.join(static_dir, "icon-192.png"))
    monogram_png(ttf700, 512).save(os.path.join(static_dir, "icon-512.png"))
    # icône « maskable » : zone de sécurité, fond plein
    monogram_png(ttf700, 512, radius_ratio=0.0).save(os.path.join(static_dir, "icon-maskable-512.png"))
    ico = monogram_png(ttf700, 64)
    ico.save(os.path.join(static_dir, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    og_image(FONTS, os.path.join(img_dir, "og-image.jpg"))
    print("ok")


if __name__ == "__main__":
    main()
