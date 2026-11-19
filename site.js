(function () {
  var launch = new Date(document.body.dataset.launch).getTime();
  function isOpen() { return Date.now() >= launch; }

  // countdown
  var cd = document.querySelector(".countdown");
  function tick() {
    if (!cd) return;
    var t = Math.max(0, launch - Date.now()), s = Math.floor(t / 1000);
    if (t === 0) { cd.textContent = "pre-orders are open"; var w = document.querySelector(".when"); if (w) w.textContent = "shop the drop below"; return; }
    cd.querySelector("[data-d]").textContent = Math.floor(s / 86400);
    cd.querySelector("[data-h]").textContent = String(Math.floor(s / 3600) % 24).padStart(2, "0");
    cd.querySelector("[data-m]").textContent = String(Math.floor(s / 60) % 60).padStart(2, "0");
    cd.querySelector("[data-s]").textContent = String(s % 60).padStart(2, "0");
    setTimeout(tick, 1000);
  }
  tick();

  // signup -> Klaviyo client subscriptions API
  document.querySelectorAll("form.signup").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = form.querySelector(".msg"), email = form.email.value.trim(), phone = form.phone.value.replace(/[\s()-]/g, "");
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { msg.textContent = "that email doesn't look right"; return; }
      if (phone && phone.charAt(0) === "0") phone = "+44" + phone.slice(1);
      if (phone && !/^\+\d{8,15}$/.test(phone)) { msg.textContent = "use your full mobile, e.g. +44 7..."; return; }
      var cfg = window.FJ || {};
      if (!cfg.klaviyoCompanyId || !cfg.klaviyoListId) { msg.textContent = "list opens very soon, check back in a bit"; return; }
      var subs = { email: { marketing: { consent: "SUBSCRIBED" } } };
      var attrs = { email: email, subscriptions: subs };
      if (phone && form.sms.checked) { attrs.phone_number = phone; subs.sms = { marketing: { consent: "SUBSCRIBED" } }; }
      var body = { data: { type: "subscription", attributes: { custom_source: "finaljudgment.store", profile: { data: { type: "profile", attributes: attrs } } },
        relationships: { list: { data: { type: "list", id: cfg.klaviyoListId } } } } };
      msg.textContent = "adding you...";
      fetch("https://a.klaviyo.com/client/subscriptions?company_id=" + encodeURIComponent(cfg.klaviyoCompanyId), {
        method: "POST", headers: { "content-type": "application/vnd.api+json", revision: "2024-10-15" }, body: JSON.stringify(body)
      }).then(function (r) {
        if (r.ok || r.status === 202) { msg.textContent = "you're in. watch your texts on 27.11."; form.reset(); if (window.fbq) fbq("track", "Lead"); }
        else msg.textContent = "something went wrong, try again";
      }).catch(function () { msg.textContent = "something went wrong, try again"; });
    });
  });

  // pre-order buttons -> Stripe Payment Links
  var page = document.querySelector("main.product");
  if (page) {
    var slug = page.dataset.slug, form = page.querySelector("form.buy"), btn = form.querySelector(".buy-btn"), msg = form.querySelector(".msg");
    var links = ((window.FJ || {}).stripe || {})[slug] || {};
    if (isOpen()) { btn.disabled = false; btn.textContent = "Pre-order"; }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var key = form.size ? form.size.value : (form.size_top.value && form.size_bottom.value ? form.size_top.value + "/" + form.size_bottom.value : "");
      if (!key) { msg.textContent = "pick a size first"; return; }
      var url = links[key];
      if (!url) { msg.textContent = "checkout opens 27.11, 09:00 GMT"; return; }
      if (window.fbq) fbq("track", "InitiateCheckout");
      location.href = url;
    });
  }
})();
