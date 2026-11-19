(function () {
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var vh = function () { return window.innerHeight; };

  // progress of an element that is taller than the viewport (0 at its top hitting the top, 1 at its bottom hitting the bottom)
  function pinProgress(el) {
    var r = el.getBoundingClientRect(), span = r.height - vh();
    return span > 0 ? clamp(-r.top / span, 0, 1) : 0;
  }

  // ---- scroll-scrubbed frame sequences ----
  var scenes = [].slice.call(document.querySelectorAll(".scene")).map(function (el) {
    var n = +el.dataset.frames, seq = el.dataset.seq, canvas = el.querySelector("canvas"), ctx = canvas.getContext("2d");
    var frames = [], loaded = 0, last = -1;
    for (var i = 1; i <= n; i++) {
      var im = new Image();
      im.decoding = "async";
      im.src = "seq/" + seq + "/" + String(i).padStart(3, "0") + ".jpg";
      im.onload = function () { loaded++; if (last < 0) draw(0); };
      frames.push(im);
    }
    function size() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2), b = canvas.getBoundingClientRect();
      canvas.width = Math.round(b.width * dpr); canvas.height = Math.round(b.height * dpr); last = -1;
    }
    function draw(i) {
      var im = frames[i];
      if (!im || !im.complete || !im.naturalWidth) return;
      if (i === last) return; last = i;
      var cw = canvas.width, ch = canvas.height, s = Math.min(cw / im.naturalWidth, ch / im.naturalHeight);
      var w = im.naturalWidth * s, h = im.naturalHeight * s;
      ctx.fillStyle = "#f4f2ee"; ctx.fillRect(0, 0, cw, ch);
      ctx.drawImage(im, (cw - w) / 2, (ch - h) / 2, w, h);
    }
    size();
    return { el: el, n: n, draw: draw, size: size, steps: [].slice.call(el.querySelectorAll(".step")) };
  });

  // ---- hero, world gallery, progress bar, reveals ----
  var hero = document.querySelector(".hero"), heroImg = document.querySelector(".hero-img"), heroTitle = document.querySelector(".hero-title");
  var world = document.querySelector(".world"), track = document.querySelector(".world-track");
  var bar = document.querySelector(".progress");
  var marquee = document.querySelector(".marquee-track");

  function frame() {
    var y = window.scrollY;
    if (bar) bar.style.transform = "scaleX(" + clamp(y / (document.documentElement.scrollHeight - vh()), 0, 1) + ")";
    if (hero && !reduce) {
      var hp = clamp(y / hero.offsetHeight, 0, 1);
      heroImg.style.transform = "scale(" + (1 + hp * 0.25) + ") translateY(" + hp * 6 + "%)";
      heroTitle.style.transform = "scale(" + (1 + hp * 1.4) + ")";
      heroTitle.style.opacity = 1 - hp * 1.6;
    }
    if (marquee && !reduce) marquee.style.transform = "translateX(" + (-(y * 0.35) % (marquee.scrollWidth / 2)) + "px)";
    scenes.forEach(function (s) {
      var p = pinProgress(s.el);
      s.draw(reduce ? s.n - 1 : Math.round(p * (s.n - 1)));
      s.steps.forEach(function (st) { st.classList.toggle("on", p >= +st.dataset.from - 0.001 && p < +st.dataset.to + (st === s.steps[s.steps.length - 1] ? 1 : 0)); });
    });
    if (world && track && !reduce && window.innerWidth > 820) {
      var wp = pinProgress(world);
      track.style.transform = "translateX(" + -wp * (track.scrollWidth - window.innerWidth + 64) + "px)";
    }
    ticking = false;
  }
  var ticking = false;
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", function () { scenes.forEach(function (s) { s.size(); }); onScroll(); });
  frame();

  // reveal on enter
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: 0.15 }) : null;
  [].slice.call(document.querySelectorAll(".reveal")).forEach(function (el, i) {
    el.style.transitionDelay = (el.classList.contains("card") ? (i % 5) * 80 : 0) + "ms";
    io ? io.observe(el) : el.classList.add("in");
  });

  // magnetic buttons + card tilt (pointer devices only)
  if (!reduce && matchMedia("(hover: hover)").matches) {
    [].slice.call(document.querySelectorAll(".btn")).forEach(function (b) {
      b.addEventListener("mousemove", function (e) { var r = b.getBoundingClientRect(); b.style.transform = "translate(" + (e.clientX - r.left - r.width / 2) * 0.15 + "px," + (e.clientY - r.top - r.height / 2) * 0.25 + "px)"; });
      b.addEventListener("mouseleave", function () { b.style.transform = ""; });
    });
    [].slice.call(document.querySelectorAll(".card-img")).forEach(function (c) {
      c.addEventListener("mousemove", function (e) { var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5; c.style.transform = "perspective(800px) rotateY(" + x * 8 + "deg) rotateX(" + -y * 8 + "deg)"; });
      c.addEventListener("mouseleave", function () { c.style.transform = ""; });
    });
  }
})();
