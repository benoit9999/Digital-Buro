#!/usr/bin/env python3
"""
Générateur statique du site Digital-Buro.

    python build.py            → génère le site dans ./public
    python build.py --serve    → génère puis sert ./public sur http://localhost:8080

Contenu :   src/pages/*.html        (une page = un gabarit Jinja2)
SEO :       src/data/pages.json     (titres, descriptions, fil d'Ariane, langues)
Données :   src/data/site.json      (coordonnées, horaires, services, marques, suivi)
Mise en page / composants : src/templates/

Dépendance unique : Jinja2  (pip install -r requirements.txt)
"""
import datetime as dt
import hashlib
import html
import json
import re
import filecmp
import os
import shutil
import sys
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "public"
STAGE = Path(tempfile.gettempdir()) / "digital-buro-build"

# ---------------------------------------------------------------------------
# Textes d'interface par langue
# ---------------------------------------------------------------------------
I18N = {
    "fr": {
        "skip": "Aller au contenu",
        "home": "Accueil",
        "home_url": "/",
        "quote_url": "/contact/#formulaire",
        "cta": "Demander un devis",
        "call": "Appeler",
        "call_full": "Appeler le 02 534 47 02",
        "directions": "Itinéraire",
        "menu_open": "Ouvrir le menu",
        "menu_close": "Fermer le menu",
        "nav_label": "Navigation principale",
        "nav_anchors": [],
        "breadcrumb": "Fil d’Ariane",
        "hours_short": "Lun–ven 10h30–18h · Sam 11h–17h",
        "hours_title": "Horaires",
        "addr_full": "Chaussée de Charleroi 257, 1060 Saint-Gilles",
        "closed": "Fermé",
        "reviews_label": "plus de 440 avis Google",
        "map_title": "Plan d’accès à Digital-Buro, Chaussée de Charleroi 257 à Saint-Gilles",
        "map_show": "Afficher la carte",
        "map_note": "La carte Google Maps ne se charge qu’à votre demande.",
        "tagline": "Votre meilleur partenaire bureautique & digital. Plus de 30 ans d’expérience au service des particuliers et des entreprises.",
        "brussels": "Bruxelles",
        "f_repairs": "Réparations",
        "f_guide": "Comment fonctionne une imprimante",
        "f_shop": "Magasin",
        "f_shop_links": [
            ["Cartouches & toners", "/cartouches-toners/"],
            ["Vente de matériel", "/vente-materiel/"],
            ["Entreprises & réseaux", "/entreprises/"],
            ["À propos", "/a-propos/"],
            ["Contact & accès", "/contact/"],
        ],
        "f_weekdays": "Lun – ven",
        "transport": "Tram 92 · arrêt Ma Campagne",
        "vat": "TVA",
        "legal_nav": "Informations légales",
        "legal": "Mentions légales",
        "privacy": "Confidentialité",
        "cookies_manage": "Gérer les cookies",
        "consent_title": "Mesure d’audience",
        "consent_text": "Avec votre accord, nous utilisons des cookies Google pour mesurer l’efficacité de nos annonces. Refuser n’a aucun effet sur votre navigation.",
        "consent_more": "En savoir plus",
        "consent_accept": "Accepter",
        "consent_reject": "Refuser",
        "svc_names": {},
        "status": {
            "open": "Ouvert maintenant · jusqu’à {close}",
            "today": "Fermé · ouvre aujourd’hui à {open}",
            "tomorrow": "Fermé · ouvre demain à {open}",
            "later": "Fermé · ouvre {day} à {open}",
            "days": ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
        },
        "form": {
            "sending": "Envoi en cours…",
            "ok": "Merci ! Votre demande est bien envoyée. Nous vous répondons au plus vite (pendant les heures d’ouverture).",
            "error": "L’envoi n’a pas fonctionné. Réessayez, ou contactez-nous directement au 02 534 47 02 ou par e-mail.",
            "invalid": "Merci de compléter les champs obligatoires.",
        },
    },
    "nl": {
        "skip": "Naar de inhoud",
        "home": "Home",
        "home_url": "/nl/",
        "quote_url": "/nl/#contact",
        "cta": "Offerte aanvragen",
        "call": "Bellen",
        "call_full": "Bel 02 534 47 02",
        "directions": "Route",
        "menu_open": "Menu openen",
        "menu_close": "Menu sluiten",
        "nav_label": "Hoofdnavigatie",
        "nav_anchors": [["Diensten", "#diensten"], ["Inkt & toner", "#inkt-toner"], ["Over ons", "#over-ons"], ["Contact", "#contact"]],
        "breadcrumb": "Kruimelpad",
        "hours_short": "Ma–vr 10.30–18.00 · Za 11.00–17.00",
        "hours_title": "Openingsuren",
        "addr_full": "Charleroise Steenweg 257, 1060 Sint-Gillis",
        "closed": "Gesloten",
        "reviews_label": "meer dan 440 Google-reviews",
        "map_title": "Kaart naar Digital-Buro, Charleroise Steenweg 257 in Sint-Gillis",
        "map_show": "Kaart tonen",
        "map_note": "De Google Maps-kaart wordt pas geladen als u erom vraagt.",
        "tagline": "Uw partner voor kantoor en informatica, met meer dan 30 jaar ervaring.",
        "brussels": "Brussel",
        "f_repairs": "Herstellingen",
        "f_guide": "Hoe werkt een printer? (FR)",
        "f_shop": "Winkel",
        "f_shop_links": [
            ["Inktpatronen & toners", "/nl/#inkt-toner"],
            ["Verkoop & bedrijven", "/nl/#diensten"],
            ["Over ons", "/nl/#over-ons"],
            ["Contact", "/nl/#contact"],
        ],
        "f_weekdays": "Ma – vr",
        "transport": "Tram 92 · halte Ma Campagne",
        "vat": "btw",
        "legal_nav": "Juridische informatie",
        "legal": "Wettelijke vermeldingen",
        "privacy": "Privacy",
        "cookies_manage": "Cookies beheren",
        "consent_title": "Advertentiemeting",
        "consent_text": "Met uw toestemming gebruiken we Google-cookies om de doeltreffendheid van onze advertenties te meten. Weigeren heeft geen invloed op uw bezoek.",
        "consent_more": "Meer info",
        "consent_accept": "Aanvaarden",
        "consent_reject": "Weigeren",
        "svc_names": {"imprimante": "Printerherstelling", "ordinateur": "Pc- en laptopherstelling", "mac": "Mac-herstelling"},
        "status": {
            "open": "Nu open · tot {close}",
            "today": "Gesloten · opent vandaag om {open}",
            "tomorrow": "Gesloten · opent morgen om {open}",
            "later": "Gesloten · opent {day} om {open}",
            "days": ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"],
        },
        "form": {},
    },
    "en": {
        "skip": "Skip to content",
        "home": "Home",
        "home_url": "/en/",
        "quote_url": "/en/#contact",
        "cta": "Get a quote",
        "call": "Call",
        "call_full": "Call 02 534 47 02",
        "directions": "Directions",
        "menu_open": "Open menu",
        "menu_close": "Close menu",
        "nav_label": "Main navigation",
        "nav_anchors": [["Services", "#services"], ["Ink & toner", "#ink-toner"], ["About", "#about"], ["Contact", "#contact"]],
        "breadcrumb": "Breadcrumb",
        "hours_short": "Mon–Fri 10:30–18:00 · Sat 11:00–17:00",
        "hours_title": "Opening hours",
        "addr_full": "Chaussée de Charleroi 257, 1060 Saint-Gilles",
        "closed": "Closed",
        "reviews_label": "440+ Google reviews",
        "map_title": "Map to Digital-Buro, Chaussée de Charleroi 257, Saint-Gilles",
        "map_show": "Show the map",
        "map_note": "The Google Maps map only loads when you ask for it.",
        "tagline": "Your office & IT partner in Brussels, with over 30 years of experience.",
        "brussels": "Brussels",
        "f_repairs": "Repairs",
        "f_guide": "How printers work (FR)",
        "f_shop": "Shop",
        "f_shop_links": [
            ["Ink & toner", "/en/#ink-toner"],
            ["Sales & businesses", "/en/#services"],
            ["About us", "/en/#about"],
            ["Contact", "/en/#contact"],
        ],
        "f_weekdays": "Mon – Fri",
        "transport": "Tram 92 · Ma Campagne stop",
        "vat": "VAT",
        "legal_nav": "Legal information",
        "legal": "Legal notice",
        "privacy": "Privacy",
        "cookies_manage": "Manage cookies",
        "consent_title": "Ad measurement",
        "consent_text": "With your consent, we use Google cookies to measure how well our ads perform. Declining has no effect on your visit.",
        "consent_more": "Learn more",
        "consent_accept": "Accept",
        "consent_reject": "Decline",
        "svc_names": {"imprimante": "Printer repair", "ordinateur": "PC & laptop repair", "mac": "Mac repair"},
        "status": {
            "open": "Open now · until {close}",
            "today": "Closed · opens today at {open}",
            "tomorrow": "Closed · opens tomorrow at {open}",
            "later": "Closed · opens {day} at {open}",
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        },
        "form": {},
    },
}
LANG_TAG = {"fr": "fr-BE", "nl": "nl-BE", "en": "en"}
OG_LOCALE = {"fr": "fr_BE", "nl": "nl_BE", "en": "en_GB"}


def hfmt(value, lang="fr"):
    """'10:30' → '10h30' (fr), '10.30' (nl), '10:30' (en) ; '18:00' → '18h' (fr)."""
    if not value:
        return ""
    h, m = value.split(":")
    if lang == "fr":
        return f"{int(h)}h" if m == "00" else f"{int(h)}h{m}"
    if lang == "nl":
        return f"{int(h)}.{m}"
    return f"{int(h)}:{m}"


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------
def short_hash(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()[:10]


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip()


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def typography(markup: str, lang: str) -> str:
    """Typographie : espaces insécables à la française (avant : ; ! ? », après «)
    et numéros de téléphone jamais coupés. Ne touche ni aux balises, ni aux scripts."""
    nbsp = " "
    parts = re.split(r"(<[^>]+>)", markup)
    skip = False
    for i, part in enumerate(parts):
        if part.startswith("<"):
            tag = part[1:8].lower()
            if tag.startswith(("script", "style")):
                skip = True
            elif tag.startswith(("/script", "/style")):
                skip = False
            continue
        if skip or not part.strip():
            continue
        if lang == "fr":
            part = re.sub(r"[  ]([:;!?»])", nbsp + r"\1", part)
            part = part.replace("« ", "«" + nbsp)
        part = re.sub(r"\b(0\d) (\d{3}) (\d{2}) (\d{2})\b", r"\1" + nbsp + r"\2" + nbsp + r"\3" + nbsp + r"\4", part)
        parts[i] = part
    return "".join(parts)


# ---------------------------------------------------------------------------
# Données structurées (JSON-LD)
# ---------------------------------------------------------------------------
def business_node(site):
    url = site["url"]
    days = [h["schema"] for h in site["hours"] if h["open"]]
    specs = {}
    for h in site["hours"]:
        if h["open"]:
            specs.setdefault((h["open"], h["close"]), []).append(h["schema"])
    return {
        "@type": ["ComputerStore", "OfficeEquipmentStore"],
        "@id": f"{url}/#business",
        "name": site["name"],
        "alternateName": "DIGITAL-BURO",
        "legalName": site["legal_name"],
        "description": "Magasin de bureautique et d’informatique à Saint-Gilles (Bruxelles) : réparation "
                       "d’imprimantes, de photocopieurs, de PC et de Mac toutes marques, cartouches "
                       "et toners, vente, installation et maintenance de matériel.",
        "slogan": "Votre meilleur partenaire bureautique & digital",
        "url": f"{url}/",
        "logo": f"{url}/icon-512.png",
        "image": [
            f"{url}/assets/img/vitrine-digital-buro-saint-gilles.webp",
            f"{url}/assets/img/og-image.jpg",
        ],
        "telephone": site["phone_display_intl"],
        "faxNumber": "+32 2 534 53 51",
        "email": site["email"],
        "vatID": site["vat_compact"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": site["street"],
            "addressLocality": site["city"],
            "addressRegion": site["region"],
            "postalCode": site["postal"],
            "addressCountry": site["country"],
        },
        "geo": {"@type": "GeoCoordinates", "latitude": site["lat"], "longitude": site["lng"]},
        "hasMap": site["google"]["maps_url"],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": d if len(d) > 1 else d[0], "opens": o, "closes": c}
            for (o, c), d in specs.items()
        ],
        "areaServed": [{"@type": "City", "name": a} for a in site["areas"]]
                      + [{"@type": "AdministrativeArea", "name": "Région de Bruxelles-Capitale"}],
        "currenciesAccepted": "EUR",
        "knowsLanguage": "fr",
        "sameAs": [site["google"]["cid_url"]],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Services de Digital-Buro",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{url}{s['url']}"}}
                for s in site["services"]
            ],
        },
    }


def build_jsonld(site, page, rendered_html):
    url = site["url"]
    page_url = f"{url}{page['path']}"
    lang_tag = LANG_TAG[page["lang"]]
    graph = [business_node(site)]
    if page["path"] in ("/", "/nl/", "/en/"):
        graph.append({
            "@type": "WebSite",
            "@id": f"{url}/#website",
            "url": f"{url}/",
            "name": "Digital-Buro",
            "inLanguage": ["fr-BE", "nl-BE", "en"],
            "publisher": {"@id": f"{url}/#business"},
        })
    page_type = {"about": "AboutPage", "contact": "ContactPage"}.get(page["type"], "WebPage")
    webpage = {
        "@type": page_type,
        "@id": f"{page_url}#webpage",
        "url": page_url,
        "name": page["title"],
        "description": page["description"],
        "inLanguage": lang_tag,
        "isPartOf": {"@id": f"{url}/#website"},
        "about": {"@id": f"{url}/#business"},
    }
    crumbs = page.get("breadcrumb")
    if crumbs:
        webpage["breadcrumb"] = {"@id": f"{page_url}#breadcrumb"}
        graph.append({
            "@type": "BreadcrumbList",
            "@id": f"{page_url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": name, "item": f"{url}{href}"}
                for i, (name, href) in enumerate(crumbs)
            ],
        })
    graph.append(webpage)

    if page["type"] == "service":
        graph.append({
            "@type": "Service",
            "@id": f"{page_url}#service",
            "name": page["service_name"],
            "serviceType": page["service_name"],
            "description": page["description"],
            "url": page_url,
            "provider": {"@id": f"{url}/#business"},
            "areaServed": [{"@type": "City", "name": a} for a in site["areas"][:5]]
                          + [{"@type": "AdministrativeArea", "name": "Région de Bruxelles-Capitale"}],
            "availableChannel": {
                "@type": "ServiceChannel",
                "servicePhone": {"@type": "ContactPoint", "telephone": site["phone_display_intl"], "contactType": "customer service"},
                "serviceLocation": {"@id": f"{url}/#business"},
            },
        })
    if page["type"] == "article":
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", rendered_html, flags=re.S)
        graph.append({
            "@type": "Article",
            "@id": f"{page_url}#article",
            "headline": strip_tags(h1.group(1)) if h1 else page["title"],
            "description": page["description"],
            "inLanguage": lang_tag,
            "datePublished": page.get("published"),
            "dateModified": page.get("modified", page.get("published")),
            "author": {"@id": f"{url}/#business"},
            "publisher": {"@id": f"{url}/#business"},
            "image": f"{url}/assets/img/og-image.jpg",
            "mainEntityOfPage": {"@id": f"{page_url}#webpage"},
        })

    faqs = []
    for block in re.findall(r'<details class="faq__item" data-faq.*?</details>', rendered_html, flags=re.S):
        q = re.search(r'<summary class="faq__q">(.*?)<svg', block, flags=re.S)
        a = re.search(r'<div class="faq__a">(.*?)</div>\s*</details>', block, flags=re.S)
        if q and a:
            faqs.append((strip_tags(q.group(1)), strip_tags(a.group(1))))
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "@id": f"{page_url}#faq",
            "inLanguage": lang_tag,
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })
    data = {"@context": "https://schema.org", "@graph": graph}
    # json.dumps + échappement de « </ » pour rester valide dans une balise <script>
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
def main():
    site = json.loads((SRC / "data" / "site.json").read_text(encoding="utf-8"))
    pages = json.loads((SRC / "data" / "pages.json").read_text(encoding="utf-8"))
    services = {s["key"]: s for s in site["services"]}
    tracking = site.get("tracking", {})
    tracking_enabled = bool(tracking.get("google_ads_id") or tracking.get("ga4_id"))

    out = STAGE
    if out.resolve() != (Path(tempfile.gettempdir()) / "digital-buro-build").resolve():
        raise RuntimeError("Dossier temporaire inattendu")
    if out.exists():
        shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)

    # 1. Ressources statiques
    shutil.copytree(SRC / "assets", out / "assets", dirs_exist_ok=True)
    css_path = out / "assets" / "css" / "style.css"
    css_path.write_text(minify_css(css_path.read_text(encoding="utf-8") + "\n" + (out / "assets/css/refresh.css").read_text(encoding="utf-8-sig")), encoding="utf-8")
    for item in (SRC / "static").iterdir():
        dest = out / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    versions = {
        "brand": short_hash(out / "favicon.svg"),
        "refresh": short_hash(out / "assets/css/refresh.css"),
        "refresh_js": short_hash(out / "assets/js/refresh.js"),
        "css": short_hash(css_path),
        "js": short_hash(out / "assets" / "js" / "main.js"),
        "icons": short_hash(out / "assets" / "img" / "icons.svg"),
    }

    env = Environment(
        loader=FileSystemLoader([str(SRC / "templates"), str(SRC / "pages")]),
        autoescape=False,
        undefined=StrictUndefined,
        trim_blocks=False,
        lstrip_blocks=False,
    )
    env.filters["hfmt"] = hfmt

    today = dt.date.today().isoformat()
    report = []
    built_paths = set()

    missing = [p["template"] for p in pages if not (SRC / "pages" / p["template"]).is_file()]
    if missing:
        print("⚠  Gabarits absents (pages ignorées) :", ", ".join(missing))
        pages = [p for p in pages if p["template"] not in missing]

    for page in pages:
        lang = page["lang"]
        t = I18N[lang]
        page = {
            "noindex": False,
            "alternates": None,
            "breadcrumb": None,
            "og_title": None,
            **page,
            "lang_tag": LANG_TAG[lang],
            "og_locale": OG_LOCALE[lang],
        }
        runtime = {
            "lang": lang,
            "hours": [[h["open"], h["close"]] for h in site["hours"]],
            "status": t["status"],
            "form": t.get("form", {}),
            "tracking": tracking if tracking_enabled else None,
        }
        ctx = {
            "site": site,
            "page": page,
            "t": t,
            "services": services,
            "v": versions,
            "year": dt.date.today().year,
            "tracking_enabled": tracking_enabled,
            "runtime_json": json.dumps(runtime, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"),
        }
        tpl = env.get_template(page["template"])
        rendered = tpl.render(**ctx)
        rendered = rendered.replace("__JSONLD__", build_jsonld(site, page, rendered), 1)
        # nettoyage des lignes vides laissées par les balises Jinja
        rendered = re.sub(r"\n[ \t]*\n+", "\n", rendered)
        rendered = typography(rendered, lang)

        if page.get("output"):
            dest = out / page["output"]
        else:
            dest = out / page["path"].strip("/") / "index.html" if page["path"] != "/" else out / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(rendered, encoding="utf-8")
        built_paths.add(page["path"])
        report.append((page, rendered))

    # 2. sitemap.xml
    urls = []
    for page, _ in report:
        if page.get("noindex"):
            continue
        alts = ""
        if page.get("alternates"):
            for l, p in page["alternates"].items():
                alts += f'\n    <xhtml:link rel="alternate" hreflang="{ {"fr": "fr-BE", "nl": "nl-BE", "en": "en"}[l] }" href="{site["url"]}{p}"/>'
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{site["url"]}/"/>'
        urls.append(f"  <url>\n    <loc>{site['url']}{page['path']}</loc>\n    <lastmod>{today}</lastmod>{alts}\n  </url>")
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n</urlset>\n",
        encoding="utf-8",
    )

    # 3. robots.txt
    (out / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: " + site["url"] + "/sitemap.xml\n",
        encoding="utf-8",
    )

    # 4. Manifeste
    (out / "site.webmanifest").write_text(json.dumps({
        "name": "Digital-Buro — Réparation informatique & imprimantes",
        "short_name": "Digital-Buro",
        "lang": "fr-BE",
        "start_url": "/",
        "display": "browser",
        "background_color": "#ffffff",
        "theme_color": "#ffffff",
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # 5. Contrôles qualité
    problems = check(report, built_paths, out)
    sync_dir(out, OUT)
    print(f"\n{len(report)} pages générées dans {OUT}\n")
    print(f"{'Page':<58} {'Titre':>6} {'Desc.':>6}  H1")
    for page, rendered in report:
        h1 = len(re.findall(r"<h1[\s>]", rendered))
        print(f"{page['path']:<58} {len(page['title']):>6} {len(page['description']):>6}  {h1}")
    if problems:
        print("\n⚠  Points à vérifier :")
        for p in problems:
            print("   -", p)
    else:
        print("\n✓ Aucun lien cassé, un seul H1 par page, titres et descriptions uniques.")


def sync_dir(src: Path, dst: Path):
    """Copie src vers dst sans supprimer dst (robuste aux verrous Windows / OneDrive) :
    fichiers nouveaux ou modifiés copiés, fichiers obsolètes supprimés."""
    dst.mkdir(parents=True, exist_ok=True)
    wanted = set()
    for root_dir, _, files in os.walk(src):
        rel = Path(root_dir).relative_to(src)
        (dst / rel).mkdir(parents=True, exist_ok=True)
        for f in files:
            s_file = Path(root_dir) / f
            d_file = dst / rel / f
            wanted.add(d_file.resolve())
            if not d_file.exists() or not filecmp.cmp(s_file, d_file, shallow=False):
                shutil.copy2(s_file, d_file)
    for root_dir, dirs, files in os.walk(dst, topdown=False):
        for f in files:
            d_file = (Path(root_dir) / f).resolve()
            if d_file not in wanted:
                try:
                    d_file.unlink()
                except OSError:
                    print("   (fichier verrouillé, non supprimé :", d_file, ")")
        for d in dirs:
            try:
                (Path(root_dir) / d).rmdir()  # ne supprime que les dossiers vides
            except OSError:
                pass


def check(report, built_paths, root):
    problems = []
    titles, descs = {}, {}
    for page, rendered in report:
        path = page["path"]
        titles.setdefault(page["title"], []).append(path)
        descs.setdefault(page["description"], []).append(path)
        n_h1 = len(re.findall(r"<h1[\s>]", rendered))
        if n_h1 != 1:
            problems.append(f"{path} : {n_h1} balises <h1>")
        if len(page["title"]) > 70:
            problems.append(f"{path} : titre long ({len(page['title'])} car.)")
        if not 110 <= len(page["description"]) <= 165 and not page.get("noindex"):
            problems.append(f"{path} : description de {len(page['description'])} car. (idéal 110–160)")
        for img in re.findall(r"<img\b[^>]*>", rendered):
            if " alt=" not in img:
                problems.append(f"{path} : image sans attribut alt → {img[:80]}")
        for href in re.findall(r'(?:href|src)="(/[^"#?]*)', rendered):
            target = root / href.lstrip("/")
            if href in built_paths or (target.is_file()) or (target / "index.html").is_file():
                continue
            msg = f"{path} : lien interne introuvable → {href}"
            if msg not in problems:
                problems.append(msg)
        for anchor in re.findall(r'href="#([^"]+)"', rendered):
            if f'id="{anchor}"' not in rendered:
                problems.append(f"{path} : ancre introuvable → #{anchor}")
    for title, paths in titles.items():
        if len(paths) > 1:
            problems.append(f"Titre dupliqué sur {paths}")
    for d, paths in descs.items():
        if len(paths) > 1:
            problems.append(f"Description dupliquée sur {paths}")
    return problems


if __name__ == "__main__":
    main()
    if "--serve" in sys.argv:
        import functools
        import http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        port = 8080
        print(f"\n→ http://localhost:{port}  (Ctrl+C pour arrêter)")
        http.server.ThreadingHTTPServer(("", port), handler).serve_forever()
