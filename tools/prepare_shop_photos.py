"""Export the client’s photos as WebP without cropping their 4:3 frame.

python tools/prepare_shop_photos.py --source-dir C:/path/to/photos
Pillow is required. The source JPEGs are never modified.
"""
import argparse
import io
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src/assets/img/photos"
PHOTOS = {
    "photo_interieur.jpeg": "magasin-interieur",
    "photo_exterieur.jpeg": "magasin-exterieur",
    "photo_cartouche.jpeg": "magasin-cartouches",
}
WIDTHS = (400, 800, 1200)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=Path.home() / "Downloads")
    parser.add_argument("--only", choices=PHOTOS.values(), help="Export only the selected photo")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, key in PHOTOS.items():
        if args.only and key != args.only:
            continue
        with Image.open(args.source_dir / filename) as original:
            image = ImageOps.exif_transpose(original).convert("RGB")
        if image.size[0] * 3 != image.size[1] * 4:
            raise ValueError(f"Expected a 4:3 source: {filename}")
        if image.width < max(WIDTHS):
            raise ValueError(f"Source is too small: {filename}")
        for width in WIDTHS:
            resized = image.resize((width, width * 3 // 4), Image.Resampling.LANCZOS)
            for quality in range(85, 39, -5):
                buffer = io.BytesIO()
                resized.save(buffer, "WEBP", quality=quality, method=6)
                if buffer.tell() <= 150_000:
                    break
            if buffer.tell() > 150_000:
                raise ValueError(f"WebP exceeds 150 kB: {key}-{width}")
            target = OUT / f"{key}-{width}.webp"
            target.write_bytes(buffer.getvalue())
            print(f"{target.name}: {width} × {width * 3 // 4}, {buffer.tell() / 1024:.1f} KiB")


if __name__ == "__main__":
    main()
