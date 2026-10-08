"""Export the licensed courier photo and client software composition for cards."""
import io
import json
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def main():
    photos = json.loads((ROOT / "src/data/site.json").read_text(encoding="utf-8"))["photos"]
    cache = ROOT / ".deps/service-photo-originals"
    cache.mkdir(parents=True, exist_ok=True)
    for key in ("livraison", "logiciels"):
        photo = photos[key]
        original = (ROOT / "tools/source-images/logiciels-client-edited.png" if key == "logiciels"
                    else cache / "livraison.jpg")
        if not original.exists():
            request = urllib.request.Request(photo["download"], headers={"User-Agent": "DigitalBuro/1.0"})
            with urllib.request.urlopen(request, timeout=45) as response:
                original.write_bytes(response.read())
        with Image.open(original) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
        for width in photo["widths"]:
            size = (width, width * 5 // 8)
            export = (ImageOps.pad(image, size, Image.Resampling.LANCZOS, color="white")
                      if photo.get("contain") else ImageOps.fit(image, size, Image.Resampling.LANCZOS))
            for quality in range(85, 39, -5):
                buffer = io.BytesIO()
                export.save(buffer, "WEBP", quality=quality, method=6)
                if buffer.tell() <= 150_000:
                    break
            if buffer.tell() > 150_000:
                raise ValueError(f"Image too large: {key}-{width}")
            target = ROOT / f"src/assets/img/photos/{photo['file']}-{width}.webp"
            target.write_bytes(buffer.getvalue())
            print(f"{target.name}: {buffer.tell()} bytes")


if __name__ == "__main__":
    main()
