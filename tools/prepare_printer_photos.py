"""Download the official printer images recorded in site.json and export WebP.

Requires Pillow. Originals are cached in .deps and never served by the website.
The whole product is kept on white, with no enlargement beyond the source.
"""
import io
import json
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src/assets/img/photos"
CACHE = ROOT / ".deps/printer-assets"


def prepare(key, photo):
    cached = CACHE / f"{photo['file']}-original"
    if not cached.exists():
        request = urllib.request.Request(
            photo["download"], headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(request, timeout=35) as response:
            data = response.read()
        # Validate the image before keeping it in the cache.
        Image.open(io.BytesIO(data)).verify()
        cached.write_bytes(data)

    with Image.open(cached) as original:
        image = ImageOps.exif_transpose(original).convert("RGBA")
    background = Image.new("RGBA", image.size, "white")
    background.alpha_composite(image)
    image = background.convert("RGB")

    exports = []
    for width in photo["widths"]:
        height = width * 5 // 8
        inset = max(8, width // 28)
        bounds = (min(width - inset * 2, image.width), min(height - inset * 2, image.height))
        product = ImageOps.contain(image, bounds, Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (width, height), "white")
        canvas.paste(product, ((width - product.width) // 2, (height - product.height) // 2))
        for quality in range(85, 39, -5):
            buffer = io.BytesIO()
            canvas.save(buffer, "WEBP", quality=quality, method=6)
            if buffer.tell() <= 150_000:
                break
        if buffer.tell() > 150_000:
            raise ValueError(f"Image trop lourde : {photo['file']}-{width}")
        target = OUT / f"{photo['file']}-{width}.webp"
        target.write_bytes(buffer.getvalue())
        exports.append(f"{width}px/{buffer.tell() / 1024:.1f} Kio")
    print(f"{key}: {photo['brand']} {photo['model']} — {', '.join(exports)}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    site = json.loads((ROOT / "src/data/site.json").read_text(encoding="utf-8"))
    for key, photo in site["photos"].items():
        if photo.get("product"):
            prepare(key, photo)


if __name__ == "__main__":
    main()
