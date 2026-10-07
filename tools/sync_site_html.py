"""Synchronise public/ into editable, standalone HTML files.

Run python build.py first. The HTML forms use the included PHP mailer.
The existing site-html/ folder is archived before any files are replaced.
"""
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "public"
TARGET = ROOT / "site-html"
ARTIFACTS = ROOT / "artifacts"
PAGES = json.loads((ROOT / "src/data/pages.json").read_text(encoding="utf-8"))
ROUTES = {page["path"]: page["template"] for page in PAGES}
ORIGIN = "https://www.digital-buro.be"


def hashes(folder):
    return {
        path.relative_to(folder).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(folder.rglob("*")) if path.is_file()
    }


def local_url(value):
    if not value.startswith("/") or value.startswith("//"):
        return value
    parts = urlsplit(value)
    if parts.path in ROUTES:
        result = ROUTES[parts.path]
    elif (SOURCE / parts.path.lstrip("/")).is_file():
        result = parts.path.lstrip("/")
    else:
        raise ValueError("Unknown local URL: " + value)
    query = parts.query if not parts.path.startswith("/assets/") and parts.path not in {
        "/favicon.svg", "/favicon.ico", "/apple-touch-icon.png"
    } else ""
    return result + ("?" + query if query else "") + ("#" + parts.fragment if parts.fragment else "")


def metadata_url(value):
    if not value.startswith(ORIGIN):
        return value
    suffix = value[len(ORIGIN):]
    parts = urlsplit(suffix)
    if parts.path in ROUTES and parts.path != "/":
        return ORIGIN + "/" + local_url(suffix)
    return value


def attribute(match):
    name, quote, value = match.groups()
    if name.lower() == "srcset":
        value = re.sub(r"(^|,\s*)(/[^\s,]+)", lambda m: m[1] + local_url(m[2]), value)
    else:
        value = local_url(value)
    return name + "=" + quote + value + quote


def prepare(out):
    for directory in ("img", "fonts", "js", "licenses"):
        shutil.copytree(SOURCE / "assets" / directory, out / "assets" / directory)
    shutil.copy2(ROOT / "tools/site-html/send_contact.php", out / "send_contact.php")
    shutil.copy2(ROOT / "src/static/api/form-validation.php", out / "form-validation.php")
    (out / "assets/css").mkdir()
    css = (ROOT / "src/assets/css/style.css").read_text(encoding="utf-8-sig")
    css += "\n\n/* Current visual design and responsive adjustments. */\n"
    css += (ROOT / "src/assets/css/refresh.css").read_text(encoding="utf-8-sig")
    sys.path.insert(0, str(ROOT))
    from build import minify_css
    if minify_css(css) != (SOURCE / "assets/css/style.css").read_text(encoding="utf-8"):
        raise RuntimeError("Run python build.py first: the generated CSS is outdated")
    css += "\n\n/* Inline SVG definitions support direct opening of HTML files. */\n"
    css += ".site-icons { position: absolute; width: 0; height: 0; overflow: hidden; pointer-events: none; }\n"
    (out / "assets/css/style.css").write_text(css, encoding="utf-8", newline="\n")

    sprite = (SOURCE / "assets/img/icons.svg").read_text(encoding="utf-8").strip()
    sprite = sprite.replace(
        '<svg xmlns="http://www.w3.org/2000/svg">',
        '<svg class="site-icons" xmlns="http://www.w3.org/2000/svg" width="0" height="0" aria-hidden="true" focusable="false">', 1
    )
    if 'class="site-icons"' not in sprite:
        raise RuntimeError("Unexpected icon sprite markup")
    for page in PAGES:
        source_path = SOURCE / page.get("output", page["path"].lstrip("/") + "index.html")
        markup = source_path.read_text(encoding="utf-8")
        label = {"fr": "Accéder au formulaire", "nl": "Contactformulier", "en": "Contact form"}[page["lang"]]
        markup = re.sub(
            r'<noscript><p><a href="/api/contact\.php\?form=1">.*?</a></p></noscript>',
            '<noscript><p><a href="send_contact.php?form=1">' + label + '</a></p></noscript>', markup
        )
        markup = markup.replace('action="/api/contact.php"', 'action="send_contact.php"')
        markup = re.sub(r'<use href="/assets/img/icons\.svg(?:\?[^"#]*)?#([^"\s]+)"', r'<use href="#\1"', markup)
        markup = re.sub(r'''\b(href|src|srcset|action|poster)=(['"])(.*?)\2''', attribute, markup, flags=re.I)
        markup = re.sub(r'https://www\.digital-buro\.be[^"<>\s]*', lambda m: metadata_url(m[0]), markup)
        if page["template"] == "confidentialite.html":
            markup = markup.replace(
                'La protection anti-spam utilise un identifiant dérivé de votre adresse IP et les horaires d’envoi pour limiter les demandes répétées.',
                'La protection anti-spam utilise des empreintes des demandes, du numéro de téléphone et de l’adresse IP, ainsi que les horaires d’envoi, pour limiter les demandes répétées. Le registre ne contient ni vos coordonnées ni votre message en clair. Les entrées de plus de 24 heures sont retirées lors du traitement d’une nouvelle demande.'
            )
        # CSS loads the same font without an HTTP-only preload in file:// mode.
        markup = re.sub(r'<link rel="preload" href="assets/fonts/inter-var-latin\.woff2" as="font" type="font/woff2" crossorigin>\n', '', markup)
        markup = re.sub(r'(<body\b[^>]*>)', lambda m: m[1] + "\n<!-- Shared icon definitions for direct HTML opening. -->\n" + sprite, markup, count=1)
        if re.search(r"api/|\{%|\{\{", markup):
            raise RuntimeError("Non-standalone markup: " + page["template"])
        (out / page["template"]).write_text(markup, encoding="utf-8", newline="\n")

    for filename in ("favicon.svg", "favicon.ico", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "robots.txt"):
        shutil.copy2(SOURCE / filename, out / filename)
    manifest = json.loads((SOURCE / "site.webmanifest").read_text(encoding="utf-8"))
    manifest["start_url"] = "./index.html"
    manifest["scope"] = "./"
    for icon in manifest["icons"]:
        icon["src"] = icon["src"].lstrip("/")
    (out / "site.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sitemap = (SOURCE / "sitemap.xml").read_text(encoding="utf-8")
    sitemap = re.sub(r'https://www\.digital-buro\.be[^"<>\s]*', lambda m: metadata_url(m[0]), sitemap)
    (out / "sitemap.xml").write_text(sitemap, encoding="utf-8", newline="\n")
    if (TARGET / "README.md").exists():
        shutil.copy2(TARGET / "README.md", out / "README.md")

    js_path = out / "assets/js/main.js"
    js = js_path.read_text(encoding="utf-8")
    js = js.replace("fetch('/api/contact.php?token=1'", "fetch('send_contact.php?token=1'")
    original_token = ".then(function(j){if(!j.token)throw new Error('token');return j.token;})"
    waiting_token = ".then(function(j){if(!j.token)throw new Error('token');return new Promise(function(resolve){setTimeout(function(){resolve(j.token);},Math.max(0,Math.min(3000,Number(j.wait_ms)||0)));});})"
    if js.count(original_token) != 1:
        raise RuntimeError("Unexpected token implementation")
    js = js.replace(original_token, waiting_token)
    js = js.replace("if(res.status===403)tokenRequest=null;return {ok:res.ok&&j.ok,message:j.message};", "tokenRequest=null;return {ok:res.ok&&j.ok,message:j.message,status:res.status};")
    js = js.replace('else showStatus("error",LANG==="fr"&&res.message?res.message:messages.error);', 'else showStatus("error",LANG==="fr"&&res.message?res.message:res.status===429?messages.rate:res.status===409?messages.duplicate:messages.error);')
    js = js.replace("    function validateContact() {", '''    messages.rate=LANG==='en'?'Too many requests. Please wait before trying again or call 02 534 47 02.':LANG==='nl'?'Te veel aanvragen. Wacht even of bel 02 534 47 02.':'Trop de demandes rapprochées. Patientez ou appelez le 02 534 47 02.';
    messages.duplicate=LANG==='en'?'This request has already been sent. The shop will reply during opening hours.':LANG==='nl'?'Deze aanvraag is al verzonden. De winkel antwoordt tijdens de openingsuren.':'Cette demande a déjà été envoyée. Le magasin vous répondra pendant ses heures d’ouverture.';
    function validateContact() {''')
    js = js.replace("inactive tant que site.json ne contient", "inactive tant que les données de la page ne contiennent")
    if "/api/" in js or "send_contact.php?token=1" not in js or "wait_ms" not in js:
        raise RuntimeError("Unexpected form implementation; PHP integration failed")
    js_path.write_text(js, encoding="utf-8", newline="\n")


def main():
    if TARGET.resolve() != ROOT.resolve() / "site-html" or TARGET.is_symlink():
        raise RuntimeError("Unexpected synchronisation target")
    if TARGET.exists() and any(not path.resolve().is_relative_to(TARGET.resolve()) for path in TARGET.rglob("*")):
        raise RuntimeError("The target contains a link outside site-html/")
    ARTIFACTS.mkdir(exist_ok=True)
    (ROOT / ".deps").mkdir(exist_ok=True)
    original = hashes(SOURCE)
    with tempfile.TemporaryDirectory(prefix="digital-buro-html-sync-", dir=ROOT / ".deps") as staging:
        out = Path(staging)
        prepare(out)
        if original != hashes(SOURCE):
            raise RuntimeError("public/ was modified during synchronisation")
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup = ARTIFACTS / f"digital-buro-site-html-before-sync-{stamp}.zip"
        if TARGET.exists():
            with zipfile.ZipFile(backup, "w", zipfile.ZIP_DEFLATED) as archive:
                for path in sorted(TARGET.rglob("*")):
                    if path.is_file():
                        archive.write(path, path.relative_to(ROOT).as_posix())
            with zipfile.ZipFile(backup) as archive:
                if archive.testzip() is not None:
                    raise RuntimeError("Backup verification failed")
        shutil.copytree(out, TARGET, dirs_exist_ok=True)
        expected = hashes(out)
        for path in sorted(TARGET.rglob("*"), reverse=True):
            if path.is_file() and path.relative_to(TARGET).as_posix() not in expected:
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()
        if hashes(TARGET) != expected:
            raise RuntimeError("The synchronised folder differs from the prepared copy")
        report = {
            "synced_at": dt.datetime.now().astimezone().isoformat(),
            "pages": len(PAGES),
            "forms": "Contact and callback delivered through send_contact.php with server-side anti-spam",
            "backup": backup.relative_to(ROOT).as_posix() if backup.exists() else None,
            "source_hashes": original,
            "target_hashes": expected,
            "source_unchanged": original == hashes(SOURCE),
        }
        (ARTIFACTS / "site-html-sync-files.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Synchronised {len(PAGES)} standalone pages and {len(expected)} files into {TARGET}")
        if backup.exists():
            print(f"Previous copy saved in {backup}")


if __name__ == "__main__":
    main()
