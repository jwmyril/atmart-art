# -*- coding: utf-8 -*-
"""Fabrique le site autonome art.atmart.ltd a partir des pages Atelier d'atmart.ltd.

Pourquoi un script plutot qu'une copie manuelle : les feuilles de style, les
dictionnaires de langue et le moteur atelier.js restent maintenus dans
Atmart_website. Rejouer ce script resynchronise le sous-domaine sans reecrire
une ligne a la main. C'est la parade a la derive entre deux copies.

Ce qu'il fait :
  1. copie les ressources partagees et les images de l'Atelier ;
  2. copie les 13 pages, remplace l'entete et le pied par ceux du site autonome ;
  3. renvoie vers https://atmart.ltd tout lien qui pointe hors de l'Atelier ;
  4. pose la balise canonique art.atmart.ltd et les icones ATM+ Art ;
  5. branche le manifeste PWA et le service worker du sous-domaine.
"""
import re
import shutil
from pathlib import Path

SRC = Path(r"C:\Users\USUARIO\Power_BI_Claude\Atmart_website")
DST = Path(__file__).resolve().parent.parent

PAGES = ["atelier.html", "atelier-collection.html", "atelier-maison.html",
         "atelier-business.html", "atelier-institutions.html", "atelier-diaspora.html",
         "atelier-artistes.html", "impact.html", "oeuvre.html", "fiche.html",
         "faq.html", "conditions-vente.html", "processus-creation.html"]

ASSETS_FILES = ["style.css", "script.js", "i18n.js", "atelier.css", "atelier.js",
                "atelier-offres.js", "share.js"]
ASSETS_DIRS = ["i18n", "brand", "atelier"]

# ---------------------------------------------------------------- entete
HEADER = '''<header>
  <nav class="nav">
    <a href="./" class="logo"><img src="{p}assets/logo-96.png" alt="ATM+ Art" class="logo-img" />ATM<span>+ Art</span><small data-i18n="art.tag">art numérique · Haïti &amp; Caraïbe</small></a>
    <button class="nav-toggle" aria-label="Menu">☰</button>
    <ul class="nav-links">
      <li><a href="{p}./" data-i18n="nav.a_gal">Galerie</a></li>
      <li><a href="{p}atelier-collection.html" data-i18n="nav.a_col">La collection</a></li>
      <li class="nav-grp"><span data-i18n="art.nav_offres">Offres</span>
        <ul class="nav-sub">
          <li><a href="{p}atelier-maison.html"><span data-i18n="nav.a_mez">Pour la maison</span> <small data-i18n="nav.a_mez_s">affiches, originaux, cadeaux</small></a></li>
          <li><a href="{p}atelier-business.html"><span data-i18n="nav.a_biz">Pour le business</span> <small data-i18n="nav.a_biz_s">écrans &amp; licences</small></a></li>
          <li><a href="{p}atelier-institutions.html"><span data-i18n="nav.a_fin">Financer l'accès</span> <small data-i18n="nav.a_fin_s">parrainer une communauté</small></a></li>
          <li><a href="{p}impact.html"><span data-i18n="nav.a_imp">Recevoir une impression</span> <small data-i18n="nav.a_imp_s">programmes parrainés</small></a></li>
        </ul>
      </li>
      <li><a href="{p}atelier-diaspora.html" data-i18n="nav.a_dya">Diaspora</a></li>
      <li class="nav-grp"><span data-i18n="art.nav_plus">En savoir plus</span>
        <ul class="nav-sub">
          <li><a href="{p}processus-creation.html"><span data-i18n="nav.a_proc">Notre processus</span> <small data-i18n="nav.a_proc_s">comment une œuvre est faite</small></a></li>
          <li><a href="{p}atelier-artistes.html"><span data-i18n="nav.a_art">Artistes</span> <small data-i18n="nav.a_art_s">rejoindre le programme</small></a></li>
          <li><a href="{p}faq.html" data-i18n="art.nav_faq">Questions fréquentes</a></li>
          <li><a href="{p}conditions-vente.html" data-i18n="art.nav_cgv">Conditions de vente</a></li>
        </ul>
      </li>
      <li><a href="https://atmart.ltd" data-i18n="art.nav_atmart">Atmart ↗</a></li>
    </ul>
  </nav>
</header>'''

FOOTER = '''<footer>
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="./" class="logo">ATM<span>+ Art</span></a>
        <p style="margin-top:0.7rem" data-i18n="art.foot">Art numérique haïtien et caribéen : image, voix, mouvement, impression locale. Une ligne d'Atmart LLC.</p>
      </div>
      <div>
        <h4 data-i18n="art.foot_dec">Découvrir</h4>
        <ul>
          <li><a href="{p}./" data-i18n="nav.a_gal">Galerie</a></li>
          <li><a href="{p}atelier-collection.html" data-i18n="nav.a_col">La collection</a></li>
          <li><a href="{p}atelier-diaspora.html" data-i18n="nav.a_dya">Diaspora</a></li>
          <li><a href="{p}processus-creation.html" data-i18n="nav.a_proc">Notre processus</a></li>
        </ul>
      </div>
      <div>
        <h4 data-i18n="art.foot_off">Offres</h4>
        <ul>
          <li><a href="{p}atelier-maison.html" data-i18n="nav.a_mez">Pour la maison</a></li>
          <li><a href="{p}atelier-business.html" data-i18n="nav.a_biz">Pour le business</a></li>
          <li><a href="{p}atelier-institutions.html" data-i18n="nav.a_fin">Financer l'accès</a></li>
        </ul>
      </div>
      <div>
        <h4 data-i18n="foot.h_contact">Contact</h4>
        <ul>
          <li><a href="mailto:sales@atmart.ltd">sales@atmart.ltd</a></li>
          <li><a href="{p}faq.html" data-i18n="art.nav_faq">Questions fréquentes</a></li>
          <li><a href="{p}conditions-vente.html" data-i18n="art.nav_cgv">Conditions de vente</a></li>
        </ul>
      </div>
    </div>
    <p class="footer-note">© Atmart LLC — <span data-i18n="foot.rights">Tous droits réservés.</span></p>
  </div>
</footer>'''

HEAD_ICONS = '''  <link rel="icon" href="{p}assets/favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" href="{p}assets/logo-32.png" />
  <link rel="apple-touch-icon" href="{p}assets/logo-192.png" />'''


def clean_url(name: str) -> str:
    """URL canonique du site autonome."""
    if name == "index.html":
        return "https://art.atmart.ltd/"
    return "https://art.atmart.ltd/" + name[:-5]


def transforme(txt: str, name: str, prof: int = 0) -> str:
    p = "../" * prof

    # 1. entete et pied propres au site autonome
    txt = re.sub(r"<header>.*?</header>", HEADER.format(p=p).replace("\\", "\\\\"), txt, flags=re.S)
    txt = re.sub(r"<footer>.*?</footer>", FOOTER.format(p=p).replace("\\", "\\\\"), txt, flags=re.S)

    # 2. icones ATM+ Art a la place de celles d'Atmart
    txt = re.sub(r'  <link rel="icon"[^\n]*\n  <link rel="icon"[^\n]*\n  <link rel="apple-touch-icon"[^\n]*',
                 HEAD_ICONS.format(p=p).replace("\\", "\\\\"), txt, count=1)

    # 3. liens vers le reste d'Atmart : absolus, pour ne pas casser
    def abs_atmart(m):
        href, page = m.group(1), m.group(2)
        if page in PAGES or page == "index.html":
            return m.group(0)
        return f'{href}"https://atmart.ltd/{page}"'
    txt = re.sub(r'(href=)"([a-z0-9\-]+\.html)"', abs_atmart, txt)

    # 4. la galerie est la page d'accueil du sous-domaine
    txt = txt.replace('href="atelier.html"', f'href="{p}./"')
    txt = txt.replace('href="index.html"', 'href="https://atmart.ltd/"')
    if prof:
        txt = re.sub(r'(href|src)="(assets/|atelier|impact|oeuvre|fiche|faq|conditions|processus)',
                     lambda m: f'{m.group(1)}="{p}{m.group(2)}', txt)

    # 5. manifeste, canonique, service worker du sous-domaine
    txt = txt.replace('<link rel="manifest" href="manifest.webmanifest" />',
                      f'<link rel="manifest" href="{p}manifest.webmanifest" />')
    txt = re.sub(r'<link rel="canonical"[^>]*>', "", txt)
    txt = txt.replace("</title>", "</title>\n  <link rel=\"canonical\" href=\"" + clean_url(name) + "\" />", 1)
    txt = txt.replace('<script src="assets/launcher.js?v=3"></script>', "")
    txt = re.sub(r'<script src="[^"]*launcher\.js[^"]*"></script>', "", txt)
    txt = re.sub(r'navigator\.serviceWorker\.register\("[^"]*"\)',
                 'navigator.serviceWorker.register("/sw.js")', txt)
    return txt


def main():
    # ---- ressources
    (DST / "assets").mkdir(exist_ok=True)
    for f in ASSETS_FILES:
        shutil.copy2(SRC / "assets" / f, DST / "assets" / f)
    for d in ASSETS_DIRS:
        s, t = SRC / "assets" / d, DST / "assets" / d
        if t.exists():
            shutil.rmtree(t)
        shutil.copytree(s, t)
    print("ressources copiees")

    # ---- pages
    for name in PAGES:
        txt = (SRC / name).read_text(encoding="utf-8")
        out = "index.html" if name == "atelier.html" else name
        (DST / out).write_text(transforme(txt, out), encoding="utf-8")
    print(f"{len(PAGES)} pages ecrites (atelier.html -> index.html)")

    # ---- marque du site autonome dans les titres
    for f in sorted(DST.glob("*.html")):
        h = f.read_text(encoding="utf-8")
        h2 = re.sub(r"<title>(.*?)</title>",
                    lambda m: "<title>" + m.group(1).replace("Atelier ATM", "ATM+ Art")
                    .replace("| Atmart", "| ATM+ Art") + "</title>", h, flags=re.S)
        if h2 != h:
            f.write_text(h2, encoding="utf-8")
    print("titres remarques ATM+ Art")
    print("
Enchainer :  python tools/finaliser.py  puis  python tools/gen_oeuvres.py")


