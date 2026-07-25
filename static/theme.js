/* The Bridge — theme toggle + KaTeX auto-render bootstrap.
   Vanilla JS, no dependencies beyond KaTeX (loaded from CDN in each page). */

(function () {
  var KEY = "bridge-theme";
  var root = document.documentElement;

  // Apply saved preference as early as possible.
  try {
    var saved = localStorage.getItem(KEY);
    if (saved === "light" || saved === "dark") {
      root.setAttribute("data-theme", saved);
    }
  } catch (e) { /* localStorage may be unavailable */ }

  function currentTheme() {
    var attr = root.getAttribute("data-theme");
    if (attr) return attr;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function setTheme(t) {
    root.setAttribute("data-theme", t);
    try { localStorage.setItem(KEY, t); } catch (e) {}
    updateLabel(t);
  }

  function updateLabel(t) {
    var btn = document.querySelector(".theme-toggle");
    if (!btn) return;
    var dark = t === "dark";
    btn.textContent = dark ? "☀ Light" : "☾ Dark";
    btn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
  }

  function renderMath() {
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$",  right: "$",  display: false },
          { left: "\\(", right: "\\)", display: false },
          { left: "\\[", right: "\\]", display: true }
        ],
        throwOnError: false
      });
      return true;
    }
    return false;
  }

  function tryRenderMath() {
    if (!renderMath()) {
      var attempts = 0;
      var timer = setInterval(function () {
        attempts++;
        if (renderMath() || attempts > 100) {
          clearInterval(timer);
        }
      }, 50);
    }
  }

  function init() {
    var btn = document.querySelector(".theme-toggle");
    if (btn) {
      updateLabel(currentTheme());
      btn.addEventListener("click", function () {
        setTheme(currentTheme() === "dark" ? "light" : "dark");
      });
    }

    tryRenderMath();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.addEventListener("load", tryRenderMath);
})();
