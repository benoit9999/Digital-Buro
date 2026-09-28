"""
Captures d'écran pleine page (Chrome headless) découpées en tranches lisibles.
Usage : python tools/shoot.py <url> <largeur> <sortie_sans_extension> [hauteur_totale]
Outil de développement uniquement (non déployé).
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def main():
    url, width, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    total_h = int(sys.argv[4]) if len(sys.argv) > 4 else 7000
    chrome = next(p for p in CHROME_CANDIDATES if os.path.exists(p))
    profile = os.path.join(tempfile.gettempdir(), "db-shoot-profile")
    full = out + "_full.png"
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
        f"--user-data-dir={profile}", f"--window-size={width},{total_h}",
        "--virtual-time-budget=4000", f"--screenshot={full}", url,
    ], check=True, capture_output=True, timeout=90)
    im = Image.open(full).convert("RGB")
    # rogner le blanc en bas (page plus courte que la fenêtre)
    px = im.load()
    w, h = im.size
    bottom = h
    for y in range(h - 1, 0, -8):
        row = [px[x, y] for x in range(0, w, 16)]
        if any(p != (255, 255, 255) for p in row):
            bottom = min(h, y + 16)
            break
    im = im.crop((0, 0, w, bottom))
    im.save(full)
    step = 1100 if width > 700 else 1400
    n = 0
    for top in range(0, bottom, step):
        n += 1
        im.crop((0, top, w, min(bottom, top + step))).save(f"{out}_{n}.png")
    print(f"{full} ({w}x{bottom}) → {n} tranches")


if __name__ == "__main__":
    main()
