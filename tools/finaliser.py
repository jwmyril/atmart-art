# -*- coding: utf-8 -*-
"""Derniere passe sur le site autonome : PWA, langues, partage, sitemap.

A rejouer apres sync_depuis_atmart.py.
"""
import json
import re
from pathlib import Path

DST = Path(__file__).resolve().parent.parent

# --- libelles propres au site autonome, dans les trois langues non françaises
CLES = {
    "ht": {
        "art.tag": "atizana nimerik · Ayiti ak Karayib la",
        "art.nav_offres": "Òf",
        "art.nav_plus": "Konnen plis",
        "art.nav_faq": "Kesyon moun poze souvan",
        "art.nav_cgv": "Kondisyon vant",
        "art.nav_atmart": "Atmart ↗",
        "art.foot": "Atizana nimerik ayisyen ak karayibeyen : imaj, vwa, mouvman, enprime lokal. Se yon liy Atmart LLC.",
        "art.foot_dec": "Dekouvri",
        "art.foot_off": "Òf",
    },
    "en": {
        "art.tag": "digital art · Haiti & the Caribbean",
        "art.nav_offres": "Offers",
        "art.nav_plus": "Learn more",
        "art.nav_faq": "Frequent questions",
        "art.nav_cgv": "Terms of sale",
        "art.nav_atmart": "Atmart ↗",
        "art.foot": "Haitian and Caribbean digital art: image, voice, movement, local printing. A line by Atmart LLC.",
        "art.foot_dec": "Discover",
        "art.foot_off": "Offers",
    },
    "es": {
        "art.tag": "arte digital · Haití y el Caribe",
        "art.nav_offres": "Ofertas",
        "art.nav_plus": "Saber más",
        "art.nav_faq": "Preguntas frecuentes",
        "art.nav_cgv": "Condiciones de venta",
        "art.nav_atmart": "Atmart ↗",
        "art.foot": "Arte digital haitiano y caribeño: imagen, voz, movimiento, impresión local. Una línea de Atmart LLC.",
        "art.foot_dec": "Descubrir",
        "art.foot_off": "Ofertas",
    },
}
for lang, add in CLES.items():
    p = DST / "assets" / "i18n" / f"{lang}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d.update(add)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"i18n {lang} : {len(d)} cles")

# --- PWA + partage social sur chaque page
pages = sorted([p for p in DST.glob("*.html") if p.name != "hors-connexion.html"]) + \
        sorted((DST / "oeuvres").glob("*.html"))
for p in pages:
    prof = 1 if p.parent.name == "oeuvres" else 0
    base = "../" if prof else ""
    t = p.read_text(encoding="utf-8")

    # l'image de partage doit vivre sur le sous-domaine, pas sur atmart.ltd
    t = t.replace("https://atmart.ltd/assets/atelier/", "https://art.atmart.ltd/assets/atelier/")
    if "og:image" not in t:
        t = t.replace("</title>", "</title>\n  <meta property=\"og:image\" "
                      "content=\"https://art.atmart.ltd/assets/logo-512.png\" />", 1)
    if "og:site_name" not in t:
        t = t.replace("</title>", "</title>\n  <meta property=\"og:site_name\" content=\"ATM+ Art\" />", 1)

    # bouton d'installation
    if "pwa.js" not in t:
        t = t.replace("</body>", f'<script src="{base}assets/pwa.js?v=1"></script>\n</body>', 1)
    # le service worker doit etre enregistre meme sur les pages qui ne le faisaient pas
    if "serviceWorker" not in t:
        t = t.replace("</body>", '<script>if("serviceWorker" in navigator)'
                      '{navigator.serviceWorker.register("/sw.js");}</script>\n</body>', 1)
    p.write_text(t, encoding="utf-8")
print(f"{len(pages)} pages : PWA + partage")

# --- sitemap
URLS = ["", "atelier-collection", "atelier-maison", "atelier-business",
        "atelier-institutions", "atelier-diaspora", "atelier-artistes", "impact",
        "processus-creation", "faq", "conditions-vente", "oeuvres/table-ancetres"]
body = "\n".join(
    f"  <url><loc>https://art.atmart.ltd/{u}</loc><changefreq>weekly</changefreq></url>"
    for u in URLS)
(DST / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n",
    encoding="utf-8")
print(f"sitemap : {len(URLS)} URL")
