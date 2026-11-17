/* Google Analytics 4, loaded only after the visitor accepts. No cookies and no requests to Google before that.
   The choice is kept in localStorage under "lg-analytics" ("yes" or "no"). */
(function () {
  var ID = "G-98HH6WZC6V";
  var KEY = "lg-analytics";
  var choice = null;
  try { choice = window.localStorage.getItem(KEY); } catch (e) {}

  function load() {
    if (window.__lgGa) return;
    window.__lgGa = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", ID);
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + ID;
    document.head.appendChild(s);
    document.addEventListener("click", function (ev) {
      var a = ev.target && ev.target.closest ? ev.target.closest("a[href]") : null;
      if (!a) return;
      var h = a.getAttribute("href") || "";
      var name = null;
      if (h.indexOf("/api/") > -1 || /\.(json|csv|zip)($|\?)/.test(h)) name = "data_download";
      else if (/zenodo\.org|huggingface\.co|kaggle\.com|github\.com/.test(h)) name = "dataset_outbound_click";
      else if (h.indexOf("linkedin.com") > -1 || h.indexOf("/newsletter") > -1) name = "newsletter_click";
      else if (h.indexOf("mailto:") === 0) name = "contact_click";
      if (name) window.gtag("event", name, { link_url: h, page_path: location.pathname });
    }, true);
  }

  function banner() {
    var b = document.createElement("div");
    b.setAttribute("role", "region");
    b.setAttribute("aria-label", "Analytics choice");
    b.style.cssText = "position:fixed;left:16px;right:16px;bottom:16px;z-index:50;max-width:560px;margin:0 auto;background:#141413;color:#f7f5f0;" +
      "padding:16px 18px;font:15px/1.45 system-ui,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.25)";
    var p = document.createElement("p");
    p.style.cssText = "margin:0 0 12px";
    p.textContent = "This site would like to count visits with Google Analytics. Nothing is sent unless you accept.";
    var row = document.createElement("div");
    row.style.cssText = "display:flex;gap:10px;flex-wrap:wrap";
    function btn(label, primary, value) {
      var x = document.createElement("button");
      x.type = "button";
      x.textContent = label;
      x.style.cssText = "font:inherit;cursor:pointer;padding:8px 16px;border:1px solid #f7f5f0;" +
        (primary ? "background:#f7f5f0;color:#141413" : "background:transparent;color:#f7f5f0");
      x.addEventListener("click", function () {
        try { window.localStorage.setItem(KEY, value); } catch (e) {}
        b.remove();
        if (value === "yes") load();
      });
      return x;
    }
    row.appendChild(btn("Accept", true, "yes"));
    row.appendChild(btn("Decline", false, "no"));
    b.appendChild(p);
    b.appendChild(row);
    document.body.appendChild(b);
  }

  if (choice === "yes") load();
  else if (choice !== "no") {
    if (document.body) banner();
    else document.addEventListener("DOMContentLoaded", banner);
  }
})();
