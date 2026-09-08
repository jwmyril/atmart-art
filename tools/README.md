# Chaîne de fabrication du site art.atmart.ltd

Les pages et les ressources viennent d'`Atmart_website`. Ne jamais éditer les
fichiers copiés à la main : ils seraient écrasés à la prochaine synchronisation.
Corriger la source, puis rejouer les trois scripts **dans cet ordre** :

    python tools/sync_depuis_atmart.py   # copie ressources + pages, entête/pied autonomes
    python tools/finaliser.py            # langues, PWA, partage social, sitemap
    python tools/gen_oeuvres.py          # /oeuvres/<slug> et /o/<slug>

Ce qui appartient en propre à ce dépôt et n'est jamais écrasé :
`CNAME`, `manifest.webmanifest`, `sw.js`, `hors-connexion.html`, `404.html`,
`assets/pwa.js`, `assets/logo*`, `assets/favicon.ico`, `logo-source.png`.

## Deux règles de domaine

- **Adresse canonique** : `https://art.atmart.ltd/oeuvres/<slug>`.
- **URL courte imprimée** : `https://atmart.ltd/o/<slug>` — celle gravée dans le
  QR déjà généré. Elle ne change jamais ; `atmart.ltd` la redirige vers la fiche.
