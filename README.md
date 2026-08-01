# art.atmart.ltd — entrée de marque ATM+ Art

Ce dépôt ne contient **pas** le site : il ne fait que renvoyer vers `atmart.ltd`,
qui reste le domaine canonique décidé le 31/07/2026.

- `art.atmart.ltd` → `https://atmart.ltd/atelier`
- `art.atmart.ltd/<n'importe quel chemin>` → `https://atmart.ltd/<le même chemin>`
  (via `404.html`, que GitHub Pages sert pour tout chemin inconnu)

Ainsi une carte imprimée « art.atmart.ltd » reste valable même si l'Atelier
change de page, et le QR déjà généré (`atmart.ltd/o/table-ancetres`) n'est pas
touché.

## Pourquoi un dépôt séparé

GitHub Pages n'accepte qu'un seul domaine personnalisé par dépôt. `atmart-site`
sert déjà `atmart.ltd` ; un sous-domaine exige donc son propre dépôt, même pour
une simple redirection. Même schéma que `lojik360.atmart.ltd`
(dépôt `jwmyril/lojik360-site`).

## Mise en service

1. **GitHub** — créer le dépôt public `jwmyril/atmart-art`, puis :

       git remote add origin https://github.com/jwmyril/atmart-art.git
       git push -u origin main

2. **GitHub** — dépôt → Settings → Pages → Source : branche `main`, dossier `/`.
   Custom domain : `art.atmart.ltd`. Cocher *Enforce HTTPS* dès que le
   certificat est émis (5 à 20 min).

3. **Porkbun** — DNS de `atmart.ltd`, ajouter :

   | Type  | Host  | Réponse              |
   |-------|-------|----------------------|
   | CNAME | `art` | `jwmyril.github.io`  |

## Vérification

    https://art.atmart.ltd                        -> atmart.ltd/atelier
    https://art.atmart.ltd/oeuvres/table-ancetres -> atmart.ltd/oeuvres/table-ancetres

## Limite connue

La redirection est **côté client** (GitHub Pages ne permet pas de 301 serveur).
Elle est immédiate pour un visiteur et suivie par les moteurs, mais ce n'est pas
un vrai 301. Les pages portent `noindex, follow` et un `canonical` vers
`atmart.ltd` : aucune copie concurrente ne sera indexée.
