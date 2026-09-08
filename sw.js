// ATM+ Art — service worker du sous-domaine art.atmart.ltd
// Objectif : une galerie consultable meme avec une connexion instable, et
// installable sur l'ecran d'accueil. Les images sont lourdes : elles sont
// servies depuis le cache en priorite, les pages depuis le reseau.
const CACHE = "atm-art-v1";

// Coquille de l'application : ce qu'il faut pour que le site s'ouvre hors ligne.
const CORE = [
  "/", "/index.html",
  "/atelier-collection.html", "/atelier-maison.html", "/atelier-business.html",
  "/atelier-institutions.html", "/atelier-diaspora.html", "/atelier-artistes.html",
  "/impact.html", "/oeuvre.html", "/fiche.html", "/faq.html",
  "/conditions-vente.html", "/processus-creation.html",
  "/oeuvres/table-ancetres.html",
  "/hors-connexion.html",
  "/assets/style.css", "/assets/atelier.css", "/assets/script.js",
  "/assets/i18n.js", "/assets/atelier.js", "/assets/atelier-offres.js",
  "/assets/i18n/ht.json", "/assets/i18n/en.json", "/assets/i18n/es.json",
  "/assets/atelier/oeuvres.json", "/assets/atelier/collection.json",
  "/assets/atelier/impact.json", "/assets/atelier/fiches/table-ancetres.json",
  "/assets/logo-192.png", "/assets/logo-512.png", "/assets/favicon.ico"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE)
      // addAll echoue en bloc des qu'un fichier manque : on tolere les absences
      .then((c) => Promise.all(CORE.map((u) => c.add(u).catch(() => null))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;

  // Les oeuvres et les mockups ne changent pas : cache d'abord, c'est ce qui
  // rend la galerie utilisable sur une connexion faible.
  const media = /\.(jpg|jpeg|png|webp|mp4|ico|svg)$/i.test(url.pathname);
  if (media) {
    e.respondWith(
      caches.match(e.request).then((hit) => hit || fetch(e.request).then((r) => {
        const copy = r.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy));
        return r;
      }).catch(() => hit))
    );
    return;
  }

  // Pages et donnees : le reseau fait foi, le cache sert de filet.
  e.respondWith(
    fetch(e.request)
      .then((r) => {
        const copy = r.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy));
        return r;
      })
      .catch(() =>
        caches.match(e.request, { ignoreSearch: true }).then((hit) => {
          if (hit) return hit;
          if (e.request.mode === "navigate") return caches.match("/hors-connexion.html");
          return new Response("", { status: 504, statusText: "Hors connexion" });
        })
      )
  );
});
