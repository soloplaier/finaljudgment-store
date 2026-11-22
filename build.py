#!/usr/bin/env python3
"""Builds the static Final Judgment site. Edit PRODUCTS / config.js, then run: python3 build.py"""
import os, html

LAUNCH = "2026-12-25T09:00:00Z"
PIXEL = "1747577036687004"
IG = "https://www.instagram.com/finaljudgementt/"
EMAIL = "iudiciumfinale@gmail.com"
NOTE = "Digital rendering. Final product may vary slightly."
SHIP = "Pre-order. Made to order, target dispatch late January 2027. Cancel any time before it ships for a full refund."

PRODUCTS = [
  dict(slug="tracksuit", name="“Final Judgment” Tracksuit", price=195, was=210, imgs=6,
       blurb="The full set: faux fur zip hoodie and sword flared joggers. Pick a size for each piece.",
       details=["Cropped faux fur zip hoodie + sword flared joggers", "White sword embroidery down both sleeves and both legs",
                "Detachable faux fur hood trim on 6 snap buttons", "Heavyweight black fleece, matte"],
       sets=True),
  dict(slug="hoodie", name="“Final Judgment” Faux Fur Zip Hoodie", price=125, imgs=8,
       blurb="Cropped, boxy zip hoodie with a blonde faux fur hood that snaps off.",
       details=["Faux fur hood trim, detachable on 6 snap buttons", "White sword and “Final Judgement” script down each sleeve",
                "Script on the chest, silver full-length zip, kangaroo pocket", "Cropped boxy fit, ribbed cuffs and hem"]),
  dict(slug="joggers", name="“Final Judgment” Sword Flared Joggers", price=85, imgs=6,
       blurb="Heavy black fleece joggers that flare from the knee.",
       details=["White sword and script down the outer side of each leg", "Wide flared leg from the knee",
                "Elastic waist with black drawcord, side pockets", "Script logo on the right back pocket"]),
  dict(slug="polo-black", name="“Guardian Angel” Polo, Black", price=70, imgs=7,
       blurb="Black polo with gold embroidery and white 33s.",
       details=["Embroidered gold crest, angel and “Final Judgment” script", "White 33 on both sleeves and large 33 on the back",
                "Thin gold stripes down each side of the back", "Three-button placket, classic collar"]),
  dict(slug="polo-white", name="“Guardian Angel” Polo, White", price=70, imgs=7,
       blurb="White polo with gold embroidery and black 33s.",
       details=["Embroidered gold crest, angel and “Final Judgment” script", "Black 33 on both sleeves and large 33 on the back",
                "Thin gold stripes down each side of the back", "Three-button placket, classic collar"]),
]
SIZES = ["S", "M", "L", "XL"]

POLO_CHART = [("Shoulder", "44", "46", "48.5", "50"), ("Chest", "104", "108", "112", "116"), ("Length", "69", "71", "73.5", "77.5"),
              ("Sleeve", "20", "20.5", "21.5", "22.5"), ("Sleeve opening", "19", "20.5", "21.5", "23")]
HOODIE_M = [("Chest width (flat)", "63.5"), ("Body length", "58"), ("Sleeve", "53")]
JOGGERS_M = [("Waist (flat, relaxed)", "38"), ("Rise", "35.5"), ("Inseam", "80"), ("Leg opening", "28.5")]

def size_guide(slug):
    def m_table(rows, title):
        r = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
        return f'<p class="small"><strong>{title}</strong>, size M, cm</p><table class="sizes"><tr><th></th><th>M</th></tr>{r}</table>'
    if slug.startswith("polo"):
        r = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in POLO_CHART)
        return f'<table class="sizes"><tr><th>cm, laid flat</th><th>S</th><th>M</th><th>L</th><th>XL</th></tr>{r}</table><p class="small">Regular fit. Between sizes, go up one.</p>'
    note = '<p class="small">Cropped, boxy fit. Measurements from the tech pack for size M; full S to XL grading is being confirmed with the factory. Message us on Instagram for your size.</p>'
    if slug == "hoodie": return m_table(HOODIE_M, "Hoodie") + note
    if slug == "joggers": return m_table(JOGGERS_M, "Joggers") + note
    return m_table(HOODIE_M, "Hoodie") + m_table(JOGGERS_M, "Joggers") + note

def head(title, desc, depth=0, path="", image="img/hero-1.jpg"):
    p = "../" * depth
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://finaljudgment.store/{image}"><meta property="og:type" content="website"><meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://finaljudgment.store/{path}">
<link rel="icon" href="{p}img/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}style.css">
<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','{PIXEL}');fbq('track','PageView');</script>
<script src="{p}config.js"></script><script defer src="{p}site.js"></script><script defer src="{p}motion.js"></script>
</head><body data-launch="{LAUNCH}">
<header class="top"><a href="{p}index.html" class="brand"><img src="{p}img/logo.png" alt="Final Judgment"></a>
<nav><a href="{p}index.html#drop">Drop</a><a href="{p}index.html#list">Join the list</a></nav></header>
"""

def foot(depth=0):
    p = "../" * depth
    return f"""<footer class="foot">
<div class="foot-links"><a href="{p}policies/shipping.html">Shipping</a><a href="{p}policies/returns.html">Returns</a>
<a href="{p}policies/terms.html">Terms</a><a href="{p}policies/privacy.html">Privacy</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a>
<a href="mailto:{EMAIL}">Contact</a></div>
<p class="small">&copy; 2026 Final Judgment. All images are digital renderings.</p></footer>
</body></html>"""

SIGNUP = """<section id="list" class="list">
<h2 class="big reveal">Join the list</h2>
<p>Early access when pre-orders open, and nothing else. Text first, email second.</p>
<form class="signup" novalidate>
<input type="email" name="email" placeholder="email" autocomplete="email" required>
<input type="tel" name="phone" placeholder="mobile (+44 7...)" autocomplete="tel">
<label class="consent"><input type="checkbox" name="sms" checked> Text me about drops. Msg &amp; data rates may apply. Reply STOP to opt out.</label>
<button type="submit">I'm in</button>
<p class="msg" role="status"></p>
</form>
<p class="small">By joining you agree to our <a href="policies/privacy.html">privacy policy</a>. Unsubscribe any time.</p>
</section>"""

def card(p):
    was = f' <s>&pound;{p["was"]}</s>' if p.get("was") else ""
    return f"""<a class="card reveal" href="products/{p['slug']}.html"><span class="card-img"><img src="img/{p['slug']}-1.jpg" alt="{html.escape(p['name'])}" loading="lazy"><img class="alt" src="img/{p['slug']}-2.jpg" alt="" loading="lazy"></span>
<span class="name">{p['name']}</span><span class="price">&pound;{p['price']}{was}</span></a>"""

def scene(sid, seq, kicker, title, lines, href, cta):
    steps = "".join(f'<p class="step" data-from="{i/len(lines):.2f}" data-to="{(i+1)/len(lines):.2f}">{l}</p>' for i, l in enumerate(lines))
    return f"""<section class="scene" id="{sid}" data-seq="{seq}" data-frames="61">
<div class="scene-pin">
<div class="scene-media"><canvas></canvas></div>
<div class="scene-copy"><p class="eyebrow">{kicker}</p><h2>{title}</h2><div class="steps">{steps}</div>
<a class="btn ghost" href="{href}">{cta}</a></div>
</div></section>"""

MARQUEE = '<div class="marquee" aria-hidden="true"><div class="marquee-track">' + ("<span>FINAL JUDGMENT</span><span class=\"star\">&#10022;</span><span>REVELATIONS</span><span class=\"star\">&#10022;</span>" * 6) + "</div></div>"

def index():
    world = "".join(f'<figure class="w-item"><img src="img/world-{i}.jpg" alt="" loading="lazy"></figure>' for i in range(1, 6))
    return head("Final Judgment | Revelations", "Revelations. Pre-orders open 25.12, 09:00 GMT. Faux fur tracksuit and Guardian Angel polos.") + f"""
<div class="progress" aria-hidden="true"></div>
<main>
<section class="hero">
<div class="hero-media"><img class="hero-img" src="img/hero-1.jpg" alt="Final Judgment stars on a rooftop at blue hour"></div>
<div class="hero-copy">
<p class="eyebrow">the drop</p><h1 class="hero-title">Revelations</h1>
<div class="countdown" aria-live="polite"><span data-d>--</span>d <span data-h>--</span>h <span data-m>--</span>m <span data-s>--</span>s</div>
<p class="when">pre-orders open 25.12 &middot; 09:00 GMT</p>
<a class="btn" href="#list">Get early access</a>
</div>
<div class="scroll-cue" aria-hidden="true">scroll</div></section>
{MARQUEE}
{scene("s-tracksuit", "hero", "the set", "The Tracksuit", ["two pieces. one verdict.", "a sword down each leg.", "faux fur on the hood.", "&pound;195 for the set."], "products/tracksuit.html", "See the tracksuit")}
{scene("s-fur", "fur", "the hoodie", "Hood up.", ["blonde faux fur.", "6 snap buttons.", "fur on. fur off.", "sword down both sleeves."], "products/hoodie.html", "See the hoodie")}
{scene("s-polo", "polo", "the polo", "Guardian Angel", ["gold crest. gold script.", "the angel with the sword.", "33 on both sleeves.", "black or white."], "products/polo-white.html", "See the polo")}
<section class="world"><div class="world-pin"><h2 class="world-title">The world</h2><div class="world-track">{world}</div></div></section>
<section id="drop" class="drop"><h2 class="big reveal">The pieces</h2><div class="grid">{''.join(card(p) for p in PRODUCTS)}</div></section>
{SIGNUP}
</main>""" + foot()

def simple_card(p):
    was = f' <s>&pound;{p["was"]}</s>' if p.get("was") else ""
    return f"""<a class="card" href="products/{p['slug']}.html"><img src="img/{p['slug']}-1.jpg" alt="{html.escape(p['name'])}" loading="lazy">
<span class="name">{p['name']}</span><span class="price">&pound;{p['price']}{was}</span></a>"""

def early_access():
    """The bio-link page: the original simple early access layout."""
    return head("Final Judgment | Early access", "Revelations. Pre-orders open 25.12, 09:00 GMT. Join the list for early access.", 0, "revelations") + f"""
<main>
<section class="hero">
<img class="hero-img" src="img/hero-1.jpg" alt="Final Judgment stars on a rooftop at blue hour">
<div class="hero-copy">
<p class="eyebrow">the drop</p><h1>Revelations</h1>
<div class="countdown" aria-live="polite"><span data-d>--</span>d <span data-h>--</span>h <span data-m>--</span>m <span data-s>--</span>s</div>
<p class="when">pre-orders open 25.12 &middot; 09:00 GMT</p>
<a class="btn" href="#list">Get early access</a>
</div></section>
<section id="drop" class="drop"><h2>The pieces</h2><div class="grid">{''.join(simple_card(p) for p in PRODUCTS)}</div></section>
{SIGNUP.replace('<h2 class="big reveal">Join the list</h2>', '<h2>Join the list</h2>')}
</main>""" + foot()

import json
def jsonld(p):
    d = {"@context": "https://schema.org", "@type": "Product", "name": p["name"].replace("\u201c", "").replace("\u201d", ""),
         "image": [f"https://finaljudgment.store/img/{p['slug']}-{i}.jpg" for i in range(1, 4)], "description": p["blurb"],
         "brand": {"@type": "Brand", "name": "Final Judgment"},
         "offers": {"@type": "Offer", "priceCurrency": "GBP", "price": str(p["price"]), "availability": "https://schema.org/PreOrder",
                    "url": f"https://finaljudgment.store/products/{p['slug']}.html"}}
    return '<script type="application/ld+json">' + json.dumps(d) + "</script>\n"

def product(p):
    imgs = "".join(f'<img src="../img/{p["slug"]}-{i}.jpg" alt="{html.escape(p["name"])} view {i}" loading="{"eager" if i==1 else "lazy"}">' for i in range(1, p["imgs"]+1))
    def sel(label, name):
        opts = "".join(f'<option value="{s}">{s}</option>' for s in SIZES)
        return f'<label class="size">{label}<select name="{name}"><option value="">choose</option>{opts}</select></label>'
    sizes = sel("Hoodie size", "size_top") + sel("Joggers size", "size_bottom") if p.get("sets") else sel("Size", "size")
    was = f' <s>&pound;{p["was"]}</s>' if p.get("was") else ""
    det = "".join(f"<li>{d}</li>" for d in p["details"])
    return head(f'{p["name"]} | Final Judgment', p["blurb"], 1, f'products/{p["slug"]}.html', f'img/{p["slug"]}-1.jpg') + jsonld(p) + f"""
<main class="product" data-slug="{p['slug']}">
<div class="gallery">{imgs}</div>
<div class="info">
<h1>{p['name']}</h1><p class="price">&pound;{p['price']}{was}</p>
<p>{p['blurb']}</p>
<form class="buy">{sizes}
<button type="submit" class="btn buy-btn" disabled>Pre-orders open 25.12</button>
<p class="msg" role="status"></p></form>
<p class="small">{SHIP}</p>
<ul class="details">{det}</ul>
<details><summary>Size guide</summary>{size_guide(p["slug"])}</details>
<details><summary>Shipping &amp; returns</summary><p class="small">UK &pound;3.50, EU &pound;10, US/CA &pound;14. 14-day returns once it arrives. <a href="../policies/shipping.html">Shipping</a> &middot; <a href="../policies/returns.html">Returns</a></p></details>
<p class="small note">{NOTE}</p>
</div></main>
<section class="list-mini"><a class="btn ghost" href="../index.html#list">Get a text when it opens</a></section>""" + foot(1)

def md_to_html(md):
    out, inlist, intable = [], False, False
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "): continue
            if not intable: out.append("<table>"); intable = True; tag = "th"
            else: tag = "td"
            out.append("<tr>" + "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in cells) + "</tr>"); continue
        if intable: out.append("</table>"); intable = False
        if s.startswith("- "):
            if not inlist: out.append("<ul>"); inlist = True
            out.append(f"<li>{html.escape(s[2:])}</li>"); continue
        if inlist: out.append("</ul>"); inlist = False
        if s.startswith("### "): out.append(f"<h3>{html.escape(s[4:])}</h3>")
        elif s.startswith("## "): out.append(f"<h2>{html.escape(s[3:])}</h2>")
        elif s: out.append(f"<p>{html.escape(s)}</p>")
    if inlist: out.append("</ul>")
    if intable: out.append("</table>")
    return "\n".join(out)

def policy(slug, title, md):
    return head(f"{title} | Final Judgment", title, 1) + f'<main class="policy">{md_to_html(md)}</main>' + foot(1)

if __name__ == "__main__":
    os.makedirs("products", exist_ok=True); os.makedirs("policies", exist_ok=True)
    open("index.html", "w").write(index())
    open("revelations.html", "w").write(early_access().replace('href="index.html#drop"', 'href="#drop"').replace('href="index.html#list"', 'href="#list"').replace('class="brand"', 'class="brand"'))
    for p in PRODUCTS: open(f"products/{p['slug']}.html", "w").write(product(p))
    for f in os.listdir("policies_src"):
        if f.endswith(".md"):
            md = open(f"policies_src/{f}").read(); title = md.splitlines()[0].lstrip("# ").strip()
            open(f"policies/{f[:-3]}.html", "w").write(policy(f[:-3], title, md))
    nf = head("Not found | Final Judgment", "Page not found") + '<main class="notfound"><div><h1>Nothing here.</h1><p class="small">The page moved or never existed.</p><a class="btn" href="/">Back to the drop</a></div></main>' + foot()
    for a in ['="img/', '="style.css', '="config.js', '="site.js', '="motion.js', '="index.html', '="policies/']: nf = nf.replace(a, a[:2] + "/" + a[2:])
    open("404.html", "w").write(nf)
    urls = ["", "revelations"] + [f"products/{p['slug']}.html" for p in PRODUCTS] + [f"policies/{f[:-3]}.html" for f in os.listdir("policies_src") if f.endswith(".md")]
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>https://finaljudgment.store/{u}</loc></url>" for u in urls) + "</urlset>\n")
    open("robots.txt", "w").write("User-agent: *\nAllow: /\nSitemap: https://finaljudgment.store/sitemap.xml\n")
    print("built")
