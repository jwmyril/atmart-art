/* ATM+ Art — installation sur l'ecran d'accueil.
   Le navigateur ne propose l'installation que s'il juge le site eligible :
   on n'affiche donc le bouton qu'au moment ou il nous le signale, jamais avant.
   Une fois refuse ou installe, on ne redemande pas. */
(function () {
  "use strict";
  var T = {
    fr: "Installer l'application", ht: "Enstale aplikasyon an",
    en: "Install the app", es: "Instalar la aplicación"
  };
  var KEY = "atmart_pwa_off";
  var prompt = null;

  function lang() {
    var l = document.documentElement.lang;
    return T[l] ? l : "fr";
  }

  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    prompt = e;
    try { if (localStorage.getItem(KEY)) return; } catch (x) {}
    show();
  });

  function show() {
    if (document.getElementById("pwa-btn")) return;
    var b = document.createElement("button");
    b.id = "pwa-btn";
    b.type = "button";
    b.textContent = "⬇ " + T[lang()];
    b.setAttribute("style",
      "position:fixed;right:1rem;bottom:1rem;z-index:80;border:none;cursor:pointer;" +
      "background:#2ec4b6;color:#06121f;font-family:inherit;font-weight:600;font-size:0.88rem;" +
      "padding:0.7rem 1.1rem;border-radius:999px;box-shadow:0 8px 24px rgba(0,0,0,0.45)");
    b.addEventListener("click", function () {
      if (!prompt) return;
      prompt.prompt();
      prompt.userChoice.then(function () {
        try { localStorage.setItem(KEY, "1"); } catch (x) {}
        b.remove();
        prompt = null;
      });
    });
    document.body.appendChild(b);
  }

  window.addEventListener("appinstalled", function () {
    try { localStorage.setItem(KEY, "1"); } catch (x) {}
    var b = document.getElementById("pwa-btn");
    if (b) b.remove();
  });
})();
