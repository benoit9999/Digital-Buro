"""Create the share-image SVG with the client’s exact PNG logo.

After this script, rasterize og-source.svg with sharp to update og-image.jpg.
The original PNG remains unchanged.
"""
import base64
import json
from pathlib import Path

from fontTools.ttLib import TTFont
from make_brand import glyph_run, path_for

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "src/assets/img"


def prepare_share_image():
    site = json.loads((ROOT / "src/data/site.json").read_text(encoding="utf-8"))
    font = TTFont(ROOT / "tools/fonts/Inter-Display-700.ttf")
    logo = base64.b64encode((ROOT / "src" / site["logo"].lstrip("/")).read_bytes()).decode("ascii")

    def text_paths(label, x, baseline, size, color):
        run, _ = glyph_run(font, label, -0.028)
        scale = size / font["head"].unitsPerEm
        paths = " ".join(path_for(font, name, x + dx * scale, scale, baseline) for name, dx in run)
        return f'<path fill="{color}" d="{paths}"/>'

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
        '<title>Digital-Buro · Ma Campagne · Avenue Louise</title>'
        '<rect width="1200" height="630" fill="#f3f3f7"/>'
        '<rect x="780" width="420" height="630" fill="#0b1f4d"/>'
        f'<image x="50" y="30" width="350" height="110" href="data:image/png;base64,{logo}"/>'
    )
    for label, x, y, size, color in [
        ("Vente & réparation", 65, 255, 66, "#0b1f4d"),
        ("d’imprimantes", 65, 350, 72, "#0b1f4d"),
        ("PC · Mac · Consommables", 65, 435, 30, "#60646c"),
        ("Quartier Ma Campagne · Bruxelles", 65, 500, 30, "#0b1f4d"),
        ("À deux pas de l’avenue Louise", 65, 550, 28, "#0b1f4d"),
        (f"+{site['experience_years']}", 825, 285, 115, "#ffffff"),
        ("ans d’expérience", 820, 344, 31, "#ffffff"),
        (f"+{site['google']['review_count']}", 850, 470, 67, "#ffffff"),
        ("avis Google", 850, 520, 29, "#ffffff"),
    ]:
        svg += text_paths(label, x, y, size, color)
    (IMG / "og-source.svg").write_text(svg + "</svg>\n", encoding="utf-8")
    font.close()
    print("Share-image SVG generated with the client logo, location and current figures.")


if __name__ == "__main__":
    prepare_share_image()
