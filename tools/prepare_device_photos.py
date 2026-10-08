"""Prepare the licensed desktop PC and photocopier photos recorded in site.json.

Originals stay in .deps; responsive WebP files preserve a common 4:3 frame.
The photocopier is fitted in full so its feeder and paper drawers stay visible.
"""
import io
import json
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".deps/device-photo-originals"
OUT = ROOT / "src/assets/img/photos"


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    photos = json.loads((ROOT / "src/data/site.json").read_text(encoding="utf-8"))["photos"]
    for key in ("ordinateur-fixe", "photocopieur"):
        photo = photos[key]
        original = CACHE / f"{photo['file']}.jpg"
        if not original.exists():
            request = urllib.request.Request(
                photo["download"], headers={"User-Agent": "DigitalBuro-PhotoPreparation/1.0"}
            )
            with urllib.request.urlopen(request, timeout=35) as response:
                data = response.read()
            Image.open(io.BytesIO(data)).verify()
            original.write_bytes(data)
        with Image.open(original) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
        for width in photo["widths"]:
            size = (width, width * 3 // 4)
            if photo.get("contain"):
                export = ImageOps.pad(image, size, Image.Resampling.LANCZOS, color="white")
            else:
                export = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            for quality in range(85, 39, -5):
                buffer = io.BytesIO()
                export.save(buffer, "WEBP", quality=quality, method=6)
                if buffer.tell() <= 150_000:
                    break
            if buffer.tell() > 150_000:
                raise ValueError(f"Image too large: {key}-{width}")
            (OUT / f"{photo['file']}-{width}.webp").write_bytes(buffer.getvalue())
            print(f"{key}: {width}px, {buffer.tell() / 1024:.1f} KiB")


if __name__ == "__main__":
    main()
