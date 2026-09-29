/* Digital-Buro — interactions du site (aucune dépendance) */
(function () {
  "use strict";

  var dataEl = document.getElementById("site-data");
  var DATA = {};
  try { DATA = JSON.parse(dataEl ? dataEl.textContent : "{}"); } catch (e) { DATA = {}; }
  var LANG = DATA.lang || "fr";

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* ------------------------------------------------------------------
     Heure de Bruxelles & statut d'ouverture
     ------------------------------------------------------------------ */
  function brusselsNow() {
    var parts = new Intl.DateTimeFormat("en-GB", {
      timeZone: "Europe/Brussels", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23"
    }).formatToParts(new Date());
    var get = function (type) {
      for (var i = 0; i < parts.length; i++) { if (parts[i].type === type) return parts[i].value; }
      return "0";
    };
    var day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].indexOf(get("weekday"));
    var hour = parseInt(get("hour"), 10) % 24;
    return { day: day, minutes: hour * 60 + parseInt(get("minute"), 10) };
  }
  function toMinutes(s) { var p = s.split(":"); return parseInt(p[0], 10) * 60 + parseInt(p[1], 10); }
  function fmtTime(s) {
    var p = s.split(":"), h = String(parseInt(p[0], 10)), m = p[1];
    if (LANG === "fr") return m === "00" ? h + "h" : h + "h" + m;
    if (LANG === "nl") return h + "." + m;
    return h + ":" + m;
  }
  function tpl(str, vars) {
    return str.replace(/\{(\w+)\}/g, function (_, k) { return vars[k] != null ? vars[k] : ""; });
  }
  function openingStatus() {
    var hours = DATA.hours, S = DATA.status;
    if (!hours || !S) return null;
    var now = brusselsNow();
    if (now.day < 0) return null;
    var today = hours[now.day];
    if (today[0] && now.minutes >= toMinutes(today[0]) && now.minutes < toMinutes(today[1])) {
      return { state: "open", text: tpl(S.open, { close: fmtTime(today[1]) }), day: now.day };
    }
    if (today[0] && now.minutes < toMinutes(today[0])) {
      return { state: "closed", text: tpl(S.today, { open: fmtTime(today[0]) }), day: now.day };
    }
    for (var i = 1; i <= 7; i++) {
      var d = (now.day + i) % 7, h = hours[d];
      if (h[0]) {
        var key = i === 1 ? "tomorrow" : "later";
        return { state: "closed", text: tpl(S[key], { open: fmtTime(h[0]), day: S.days[d] }), day: now.day };
      }
    }
    return null;
  }
  function renderStatus() {
    var st = openingStatus();
    if (!st) return;
    $$("[data-status]").forEach(function (el) {
      el.setAttribute("data-state", st.state);
      var txt = $("[data-status-text]", el);
      if (txt) txt.textContent = st.text;
    });
    $$("[data-hours-table] tr").forEach(function (tr) {
      tr.classList.toggle("is-today", parseInt(tr.getAttribute("data-day"), 10) === st.day);
    });
  }
  renderStatus();
  setInterval(renderStatus, 60000);

  /* ------------------------------------------------------------------
     En-tête : filet au défilement, barre d'appel mobile
     ------------------------------------------------------------------ */
  var header = $("[data-header]");
  var callbar = $("[data-callbar]");
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("is-scrolled", y > 8);
    if (callbar) callbar.classList.toggle("is-visible", y > 280);
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  // Default header state already matches the top of the page. Read geometry only
  // after the browser has painted, including when restoring a scroll position.
  window.requestAnimationFrame(function () { window.requestAnimationFrame(onScroll); });

  /* ------------------------------------------------------------------
     Menu déroulant « Réparations »
     ------------------------------------------------------------------ */
  $$("[data-dropdown]").forEach(function (item) {
    var btn = $("button", item);
    var timer = null, hoverOpenedAt = 0;
    function set(open) {
      item.setAttribute("data-open", open ? "true" : "false");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    }
    btn.addEventListener("click", function () {
      if (Date.now() - hoverOpenedAt < 400) return; // ouvert par le survol juste avant le clic
      set(item.getAttribute("data-open") !== "true");
    });
    item.addEventListener("pointerenter", function (e) {
      if (e.pointerType !== "mouse") return;
      clearTimeout(timer);
      if (item.getAttribute("data-open") !== "true") { hoverOpenedAt = Date.now(); set(true); }
    });
    item.addEventListener("pointerleave", function (e) {
      if (e.pointerType !== "mouse") return;
      timer = setTimeout(function () { set(false); }, 140);
    });
    item.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { set(false); btn.focus(); }
    });
    item.addEventListener("focusout", function (e) {
      if (!item.contains(e.relatedTarget)) set(false);
    });
    document.addEventListener("click", function (e) {
      if (!item.contains(e.target)) set(false);
    });
  });

  /* ------------------------------------------------------------------
     Menu mobile
     ------------------------------------------------------------------ */
  var toggle = $("[data-menu-toggle]");
  var menu = $("[data-mobile-menu]");
  function setMenu(open) {
    if (!toggle || !menu) return;
    if (open && header) menu.style.setProperty("--menu-top", Math.max(0, header.getBoundingClientRect().bottom) + "px");
    menu.classList.toggle("is-open", open);
    document.body.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? toggle.getAttribute("data-label-close") : toggle.getAttribute("data-label-open"));
    var use = $("use", toggle);
    if (use) {
      var base = (use.getAttribute("href") || "").split("#")[0];
      use.setAttribute("href", base + (open ? "#close" : "#menu"));
    }
  }
  if (toggle && menu) {
    toggle.addEventListener("click", function () { setMenu(!menu.classList.contains("is-open")); });
    $$("[data-menu-close], a", menu).forEach(function (a) {
      a.addEventListener("click", function () { setMenu(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("is-open")) { setMenu(false); toggle.focus(); }
    });
    window.addEventListener("resize", function () {
      if (menu.classList.contains("is-open") && window.innerWidth >= 1100) setMenu(false);
    });
  }

  /* ------------------------------------------------------------------
     Carte Google Maps : chargée uniquement à la demande (vie privée + vitesse)
     ------------------------------------------------------------------ */
  $$("[data-map-load]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var facade = btn.closest("[data-map]");
      if (!facade) return;
      var iframe = document.createElement("iframe");
      iframe.src = facade.getAttribute("data-map");
      iframe.title = facade.getAttribute("data-map-title") || "Google Maps";
      iframe.className = "map-frame";
      iframe.loading = "lazy";
      iframe.referrerPolicy = "no-referrer-when-downgrade";
      iframe.setAttribute("allowfullscreen", "");
      facade.replaceWith(iframe);
    });
  });

  /* ------------------------------------------------------------------
     Formulaire de contact
     ------------------------------------------------------------------ */
  document.documentElement.classList.add("js");
  $$("[data-contact-form]").forEach(function(form) {
    var params = new URLSearchParams(location.search), F = DATA.form || {};
    ["appareil", "sujet"].forEach(function(key) {
      var field = form.elements[key], value = params.get(key);
      if (!field || !value) return;
      if (field.tagName === "SELECT") {
        var option = Array.from(field.options).find(function(o) { return o.value === value || o.textContent.toLowerCase().includes(value.toLowerCase()); });
        if (option) field.value=option.value;
      } else field.value=value.slice(0,160);
    });
    if(form.elements.ts) form.elements.ts.value=String(Date.now());
    var statusBox=$("[data-form-status]",form), submitBtn=$("[type=submit]",form);
    var messages = LANG === "en" ? {sending:"Sending…",ok:"Thank you. Your request has been sent.",error:"Sending failed. Please call 02 534 47 02.",contact:"Enter a phone number or an email address.",phone:"Enter a valid phone number."} : LANG === "nl" ? {sending:"Verzenden…",ok:"Bedankt. Uw aanvraag is verzonden.",error:"Verzenden mislukt. Bel 02 534 47 02.",contact:"Vul een telefoonnummer of e-mailadres in.",phone:"Vul een geldig telefoonnummer in."} : {sending:"Envoi en cours…",ok:"Merci ! Votre demande est bien envoyée.",error:"L’envoi a échoué. Appelez le 02 534 47 02.",contact:"Indiquez un téléphone ou une adresse e-mail.",phone:"Indiquez un numéro de téléphone valide."};
    function showStatus(kind,message) {
      statusBox.className="form__status is-visible form__status--"+kind;
      statusBox.textContent=message;statusBox.setAttribute("role",kind==="error"?"alert":"status");
    }
    function validateContact() {
      var phone=form.elements.telephone,email=form.elements.email;
      if(phone)phone.setCustomValidity("");if(email)email.setCustomValidity("");
      if(phone && phone.value.trim() && (!/^[+()0-9 .-]{7,40}$/.test(phone.value.trim()) || phone.value.replace(/[^0-9]/g, "").length < 7))phone.setCustomValidity(messages.phone);
      if(email && !email.value.trim() && !phone.value.trim())phone.setCustomValidity(messages.contact);
    }
    ["telephone","email"].forEach(function(key){if(form.elements[key]) form.elements[key].addEventListener("input",validateContact);});
    if(params.get("erreur"))showStatus("error",messages.error);
    form.addEventListener("submit",function(e) {
      validateContact();
      if(!form.checkValidity()){e.preventDefault();form.reportValidity();return;}
      if(!window.fetch || !window.FormData)return;
      e.preventDefault();if(submitBtn.disabled)return;
      submitBtn.disabled=true;submitBtn.classList.add("is-sending");form.setAttribute("aria-busy","true");
      var old=submitBtn.innerHTML;submitBtn.textContent=messages.sending;
      var controller=new AbortController(),timeout=setTimeout(function(){controller.abort();},15000);
      fetch(form.action,{method:"POST",body:new FormData(form),headers:{Accept:"application/json"},signal:controller.signal})
      .then(function(res){return res.json().then(function(j){return {ok:res.ok&&j.ok,message:j.message};});})
      .then(function(res){if(res.ok){form.reset();if(form.elements.ts)form.elements.ts.value=String(Date.now());showStatus("ok",messages.ok);track("form");}else showStatus("error",LANG==="fr"&&res.message?res.message:messages.error);})
      .catch(function(){showStatus("error",messages.error);})
      .finally(function(){clearTimeout(timeout);submitBtn.disabled=false;submitBtn.classList.remove("is-sending");submitBtn.innerHTML=old;form.removeAttribute("aria-busy");});
    });
  });

  /* ------------------------------------------------------------------
     Mesure (Google Ads / GA4) — inactive tant que site.json ne contient
     pas d'identifiant ; ne se charge qu'après consentement explicite.
     ------------------------------------------------------------------ */
  var T = DATA.tracking;
  var KEY = "db-consent";
  function readConsent() { try { return window.localStorage.getItem(KEY); } catch (e) { return null; } }
  function writeConsent(v) { try { window.localStorage.setItem(KEY, v); } catch (e) { /* stockage indisponible */ } }
  function loadGtag() {
    if (!T || window.__dbGtag) return;
    window.__dbGtag = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("consent", "default", {
      ad_storage: "granted", ad_user_data: "granted", ad_personalization: "denied", analytics_storage: "granted"
    });
    window.gtag("js", new Date());
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(T.google_ads_id || T.ga4_id);
    document.head.appendChild(s);
    if (T.google_ads_id) window.gtag("config", T.google_ads_id);
    if (T.ga4_id) window.gtag("config", T.ga4_id);
  }
  function track(kind) {
    if (!T || typeof window.gtag !== "function") return;
    var label = kind === "call" ? T.conversion_label_call : kind === "form" ? T.conversion_label_form : "";
    if (T.google_ads_id && label) window.gtag("event", "conversion", { send_to: T.google_ads_id + "/" + label });
    if (T.ga4_id) window.gtag("event", kind === "form" ? "generate_lead" : "contact_" + kind);
  }
  document.addEventListener("click", function (e) {
    var el = e.target.closest ? e.target.closest("[data-track]") : null;
    if (el) track(el.getAttribute("data-track"));
  });
  if (T) {
    var banner = $("[data-consent]");
    var choice = readConsent();
    if (choice === "granted") loadGtag();
    else if (!choice && banner) banner.hidden = false;
    if (banner) {
      $("[data-consent-accept]", banner).addEventListener("click", function () {
        writeConsent("granted"); banner.hidden = true; loadGtag();
      });
      $("[data-consent-reject]", banner).addEventListener("click", function () {
        writeConsent("denied"); banner.hidden = true;
        if (typeof window.gtag === "function") {
          window.gtag("consent", "update", {
            ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied"
          });
        }
      });
    }
    $$("[data-consent-open]").forEach(function (b) {
      b.addEventListener("click", function () { if (banner) banner.hidden = false; });
    });
    // page de remerciement (envoi du formulaire sans JavaScript) : conversion
    var conv = $("[data-conversion]");
    if (conv) track(conv.getAttribute("data-conversion"));
  }
})();
