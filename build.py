#!/usr/bin/env python3
"""Gera o site estático da Arke Analytica a partir de content/pt.json e content/en.json.

Uso: python3 build.py
Saída: index.html (redireciona por idioma), pt/, en/, sitemap.xml, robots.txt.
Para atualizar textos, projetos ou números, edite os JSON em content/ e rode de novo.
"""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).parent
BASE_URL = "https://klayverpaz.github.io/arke-analytica/"
EMAIL = "arkeanalytica@gmail.com"
# (número no formato wa.me, número como exibido)
WHATSAPP = [("558599500076", "+55 85 9950-0076"), ("558586081055", "+55 85 8608-1055")]
PRIVACY_SLUG = {"pt": "privacidade", "en": "privacy"}

ICONS = {
    "grid": '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
    "window": '<rect x="3" y="4.5" width="18" height="15" rx="2"/><path d="M3 9h18M6.5 6.8h.01M9 6.8h.01"/>',
    "flow": '<rect x="3" y="4" width="6" height="5" rx="1.2"/><rect x="15" y="15" width="6" height="5" rx="1.2"/><path d="M9 6.5h4.5a2 2 0 0 1 2 2V15M13 12.5l2.5 2.5 2.5-2.5"/>',
    "nodes": '<circle cx="5.5" cy="12" r="2.2"/><circle cx="18.5" cy="5.5" r="2.2"/><circle cx="18.5" cy="18.5" r="2.2"/><path d="M7.5 11l9-4.5M7.5 13l9 4.5"/>',
    "spark": '<path d="M12 3.5l1.9 5.1a2 2 0 0 0 1.2 1.2l5.1 1.9-5.1 1.9a2 2 0 0 0-1.2 1.2L12 19.9l-1.9-5.1a2 2 0 0 0-1.2-1.2l-5.1-1.9 5.1-1.9a2 2 0 0 0 1.2-1.2z"/>',
    "bars": '<path d="M4 20V11M10 20V4M16 20v-6M3 20.5h18"/><path d="M20.5 20V8.5"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6.5L20.5 7"/>',
    "scan": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    "doc": '<path d="M7 3.5h7l4 4V20a.5.5 0 0 1-.5.5h-10.500A.5.5 0 0 1 6.500 20V4a.5.5 0 0 1 .5-.5z"/><path d="M9.500 12h5M9.500 15.500h5"/>',
    "lock": '<rect x="5" y="10.500" width="14" height="10" rx="2"/><path d="M8.500 10.500V8a3.500 3.500 0 0 1 7 0v2.500"/>',
    "flag": '<path d="M6 21V4M6 4.500h11l-2 3.750 2 3.750H6"/>',
    "loop": '<path d="M4.500 12a7.500 7.500 0 0 1 13-5.100L19.500 9M19.500 4.500V9H15M19.500 12a7.500 7.500 0 0 1-13 5.100L4.500 15M4.500 19.500V15H9"/>',
    "up": '<path d="M7 17L17 7M9 7h8v8"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "whatsapp": '<path d="M12 3.5a8.5 8.5 0 0 0-7.3 12.8L3.5 20.5l4.3-1.1A8.5 8.5 0 1 0 12 3.5z"/><path d="M9 8.8c-.3 2.6 3.6 6.500 6.2 6.2l.9-1.300-1.800-1-.8.700c-1-.4-2.300-1.700-2.700-2.700l.7-.800-1-1.800z"/>',
}


def icon(name, cls="icon"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def wordmark():
    return '<span class="wordmark" aria-label="Arke Analytica"><span>ARKE</span><span class="wordmark-b">ANALYTICA</span></span>'


def head(c, root, path, alt_path, title=None, x_default="pt/"):
    title = title or c["meta"]["title"]
    pt_path, en_path = (path, alt_path) if c["code"] == "pt" else (alt_path, path)
    return f"""<!doctype html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(c['meta']['description'])}">
<link rel="canonical" href="{BASE_URL}{path}">
<link rel="alternate" hreflang="pt-BR" href="{BASE_URL}{pt_path}">
<link rel="alternate" hreflang="en" href="{BASE_URL}{en_path}">
<link rel="alternate" hreflang="x-default" href="{BASE_URL}{pt_path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(c['meta']['description'])}">
<meta property="og:url" content="{BASE_URL}{path}">
<meta property="og:locale" content="{c['lang'].replace('-', '_')}">
<meta name="theme-color" content="#060A14">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/site.css">
</head>
"""


def header(c, root, home, other_href):
    n = c["nav"]
    here = "#top" if home == "" else home
    pt_href, en_href = (here, other_href) if c["code"] == "pt" else (other_href, here)
    cur = c["code"]

    def lang_link(code, href, label):
        attr = ' aria-current="true"' if code == cur else ""
        return f'<a href="{href}" hreflang="{code}" lang="{code}" data-lang="{code}"{attr}>{label}</a>'

    return f"""<body>
<a class="skip" href="#main">{e(n['skip'])}</a>
<header class="site-header" id="top">
  <div class="container header-row">
    <a class="brand" href="{home or '#top'}">{wordmark()}</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">{e(n['menu'])}</button>
    <nav class="site-nav" id="site-nav" aria-label="{e(n['menu'])}">
      <div class="nav-pill">
        <a href="{home}#solucoes">{e(n['solutions'])}</a>
        <a href="{home}#projetos">{e(n['projects'])}</a>
        <a href="{home}#metodologia">{e(n['method'])}</a>
        <a href="{home}#contratacao">{e(n['model'])}</a>
      </div>
      <div class="header-end">
        <span class="lang" role="group" aria-label="{e(n['lang_label'])}">{lang_link('pt', pt_href, 'PT')}{lang_link('en', en_href, 'EN')}</span>
        <a class="btn btn-primary btn-sm" href="{home}#contato">{e(n['cta'])}</a>
      </div>
    </nav>
  </div>
</header>
"""


def footer(c, root, home, privacy_href):
    f = c["footer"]
    return f"""<footer class="site-footer">
  <div class="container footer-row">
    <div>
      {wordmark()}
      <p class="footer-desc">{e(c['meta']['descriptor'])}</p>
      <p class="muted">{e(f['tagline'])}</p>
    </div>
    <div class="footer-meta">
      <p>{e(f['place'])}</p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p><a href="{privacy_href}">{e(f['privacy'])}</a></p>
    </div>
  </div>
  <div class="container footer-legal"><p>© 2026 Arke Analytica. {e(f['rights'])}</p></div>
</footer>
<script src="{root}assets/js/site.js" defer></script>
</body>
</html>
"""


def section_head(s, center=False):
    lead = f'<p class="lead">{e(s["lead"])}</p>' if s.get("lead") else ""
    return f"""<div class="section-head{' center' if center else ''}" data-reveal>
      <p class="eyebrow">{e(s['eyebrow'])}</p>
      <h2>{e(s['title'])}</h2>
      {lead}
    </div>"""


def render_home(c):
    root = "../"
    h, pr, so, pj, sg, ch, me, mo, ct = (c[k] for k in ("hero", "proof", "solutions", "projects", "segments", "challenges", "method", "model", "contact"))
    f = ct["form"]
    privacy_href = c["privacy"]["slug"] + "/"
    out = [head(c, root, f"{c['code']}/", f"{c['other_code']}/"), header(c, root, "", f"../{c['other_code']}/")]

    rows = "".join(
        f'<li class="glass-row"><p class="glass-row-head"><strong>{e(r["name"])}</strong><span>{e(r["meta"])}</span></p>'
        f'<div class="glass-row-body"><p><span>{e(r["a_label"])}</span><b>{e(r["a"])}</b></p><i>{e(r["mid"])}</i>'
        f'<p class="end"><span>{e(r["b_label"])}</span><b>{e(r["b"])}</b></p></div></li>'
        for r in h["card"]["rows"])
    points = "".join(f'<li>{icon(pt_["icon"], "icon icon-sm")}<span>{e(pt_["text"])}</span></li>' for pt_ in h["points"])
    out.append(f"""<main id="main">
<section class="hero">
  <div class="flutes" aria-hidden="true"></div>
  <div class="container hero-inner">
    <aside class="glass hero-card" aria-label="{e(h['card']['label'])}">
      <p class="badge"><span class="badge-dot" aria-hidden="true"></span>{e(h['badge'])}</p>
      <ul>{rows}</ul>
      <p class="footnote">{e(h['footnote'])}</p>
    </aside>
    <div class="hero-main">
      <div class="hero-copy">
        <h1>{' '.join(f'<span>{e(part)}</span>' for part in h['title'].replace('. ', '.|').split('|'))}</h1>
        <p class="lead">{e(h['lead'])}</p>
      </div>
      <div class="actions">
        <a class="btn btn-primary" href="#contato">{e(h['cta'])} {icon('up', 'icon icon-sm')}</a>
        <a class="btn btn-text" href="#projetos">{e(h['secondary'])} {icon('up', 'icon icon-sm')}</a>
      </div>
    </div>
    <ul class="hero-points">{points}</ul>
  </div>
</section>
""")

    stats = "".join(f'<div class="stat"><dt>{e(s["value"])}</dt><dd>{e(s["label"])}</dd></div>' for s in pr["stats"])
    out.append(f"""<section class="section section-tight" id="autoridade">
  <div class="container">
    {section_head(pr)}
    <dl class="stats" data-reveal>{stats}</dl>
    <p class="footnote">{e(pr['note'])}</p>
  </div>
</section>
""")

    cards = "".join(f'<li class="card">{icon(i["icon"])}<h3>{e(i["title"])}</h3><p>{e(i["text"])}</p></li>' for i in so["items"])
    out.append(f"""<section class="section" id="solucoes">
  <div class="container">
    {section_head(so)}
    <ul class="grid grid-3" data-reveal>{cards}</ul>
  </div>
</section>
""")

    cases = []
    wide = 0
    lb = pj["labels"]
    for p in pj["items"]:
        media = ""
        if p.get("image"):
            media = f'<div class="case-media"><img src="{root}assets/img/{p["image"]}" width="{p["w"]}" height="{p["h"]}" alt="{e(p["alt"])}" loading="lazy"></div>'
        elif p.get("figure"):
            fg = p["figure"]
            lead_in = f'<span>{e(fg["from"])}</span>{icon("arrow")}' if fg.get("from") else ""
            media = (f'<div class="case-media case-figure"><p class="figure-line">{lead_in}<strong>{e(fg["to"])}</strong></p>'
                     f'<p class="muted">{e(fg["caption"])}</p></div>')
        rows = [(lb["challenge"], p["challenge"]), (lb["solution"], p["solution"])]
        if p.get("result"):
            rows.append((lb["result"], p["result"]))
        dl = "".join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in rows)
        cls = "case"
        if p.get("image"):
            wide += 1
            cls = "case case-wide" + (" case-flip" if wide % 2 == 0 else "")
        cases.append(f'<article class="{cls}">{media}<div class="case-body"><p class="tag">{e(p["segment"])}</p><h3>{e(p["title"])}</h3><dl>{dl}</dl></div></article>')
    out.append(f"""<section class="section" id="projetos">
  <div class="container">
    {section_head(pj)}
    <div class="cases" data-reveal>{''.join(cases)}</div>
  </div>
</section>
""")

    segs = "".join(f'<li class="segment"><span class="segment-n">{i:02d}</span><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p></li>' for i, s in enumerate(sg["items"], 1))
    out.append(f"""<section class="section" id="segmentos">
  <div class="container">
    {section_head(sg)}
    <ul class="segments" data-reveal>{segs}</ul>
  </div>
</section>
""")

    items = "".join(f'<li>{icon("check", "icon icon-sm")}<span>{e(i)}</span></li>' for i in ch["items"])
    out.append(f"""<section class="section" id="desafios">
  <div class="container split">
    {section_head(ch)}
    <div data-reveal>
      <ul class="checklist">{items}</ul>
      <p class="closing">{e(ch['closing'])}</p>
    </div>
  </div>
</section>
""")

    steps = []
    for i, s in enumerate(me["steps"], 1):
        outs = "".join(f"<li>{e(o)}</li>" for o in s["out"])
        steps.append(f'<li class="step"><span class="step-n">{i:02d}</span><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p>'
                     f'<p class="step-label">{e(me["deliverables"])}</p><ul>{outs}</ul></li>')
    out.append(f"""<section class="section" id="metodologia">
  <div class="container">
    {section_head(me)}
    <ol class="steps" data-reveal>{''.join(steps)}</ol>
    <p class="speed" data-reveal><span class="badge-dot" aria-hidden="true"></span>{e(me['speed'])}</p>
  </div>
</section>
""")

    terms = "".join(f'<li class="card"><h3>{e(i["title"])}</h3><p>{e(i["text"])}</p></li>' for i in mo["items"])
    out.append(f"""<section class="section" id="contratacao">
  <div class="container">
    {section_head(mo)}
    <ul class="grid grid-2" data-reveal>{terms}</ul>
    <div class="actions"><a class="btn btn-primary" href="#contato">{e(mo['cta'])}</a></div>
  </div>
</section>
""")

    budget = "".join(f"<option>{e(o)}</option>" for o in f["budget_options"])
    wa_links = "".join(
        f'<li><a class="contact-link" href="https://wa.me/{num}" target="_blank" rel="noopener" data-wa>{icon("whatsapp")}<span>{shown}</span></a></li>'
        for num, shown in WHATSAPP)
    msg = e(json.dumps({"intro": f["msg_intro"], "labels": f["msg_labels"], "skip": f["budget_options"][0]}, ensure_ascii=False))
    out.append(f"""<section class="section section-contact" id="contato">
  <div class="flutes" aria-hidden="true"></div>
  <div class="container contact-grid">
    <div data-reveal>
      <p class="eyebrow">{e(ct['eyebrow'])}</p>
      <h2 class="h-xl">{e(ct['title'])}</h2>
      <p class="lead">{e(ct['lead'])}</p>
      <p class="step-label">{e(ct['direct'])}</p>
      <ul class="contact-list">
        {wa_links}
        <li><a class="contact-link" href="mailto:{EMAIL}" aria-label="{e(ct['email_label'])}: {EMAIL}">{icon('mail')}<span>{EMAIL}</span></a></li>
      </ul>
    </div>
    <form class="form glass" id="contact-form" novalidate data-wa-number="{WHATSAPP[0][0]}" data-msg="{msg}" data-reveal>
      <div class="field"><label for="f-name">{e(f['name'])}</label><input id="f-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="f-company">{e(f['company'])}</label><input id="f-company" name="company" autocomplete="organization"></div>
      <div class="field"><label for="f-email">{e(f['email'])}</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="f-phone">{e(f['phone'])}</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field field-full"><label for="f-challenge">{e(f['challenge'])}</label><textarea id="f-challenge" name="challenge" rows="4" required></textarea></div>
      <div class="field"><label for="f-timeline">{e(f['timeline'])}</label><input id="f-timeline" name="timeline"></div>
      <div class="field"><label for="f-budget">{e(f['budget'])}</label><select id="f-budget" name="budget">{budget}</select></div>
      <div class="hp" aria-hidden="true"><label for="f-site">Website</label><input id="f-site" name="website" tabindex="-1" autocomplete="off"></div>
      <label class="consent field-full"><input type="checkbox" name="consent" required><span>{e(f['consent'])} <a href="{privacy_href}">{e(f['privacy'])}</a>.</span></label>
      <div class="field-full form-end">
        <button class="btn btn-primary" type="submit">{e(f['submit'])}</button>
        <p class="footnote">{e(f['hint'])}</p>
        <p class="form-status" role="status" aria-live="polite" data-error="{e(f['error'])}" data-sent="{e(f['sent'])}"></p>
      </div>
    </form>
  </div>
</section>
</main>
""")
    out.append(footer(c, root, "", privacy_href))
    return "".join(out)


def render_privacy(c, other):
    root = "../../"
    p = c["privacy"]
    path = f"{c['code']}/{p['slug']}/"
    alt = f"{other['code']}/{other['privacy']['slug']}/"
    body = "".join(f"<h2>{e(s['h'])}</h2>" + "".join(f"<p>{e(t)}</p>" for t in s["p"]) for s in p["sections"])
    return (head(c, root, path, alt, title=f"{p['title']} — Arke Analytica")
            + header(c, root, "../", f"../../{alt}")
            + f"""<main id="main" class="prose-page">
  <div class="container prose">
    <p><a href="../">← {e(p['back'])}</a></p>
    <h1>{e(p['title'])}</h1>
    <p class="muted">{e(p['updated'])}</p>
    {body}
  </div>
</main>
""" + footer(c, root, "../", "./"))


def render_root():
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Arke Analytica — Soluções Tecnológicas</title>
<meta name="description" content="Desenvolvimento de software sob medida. Custom software development.">
<link rel="canonical" href="{BASE_URL}pt/">
<link rel="alternate" hreflang="pt-BR" href="{BASE_URL}pt/">
<link rel="alternate" hreflang="en" href="{BASE_URL}en/">
<script>
(function () {{
  var lang = null;
  try {{ lang = localStorage.getItem('arke-lang'); }} catch (err) {{}}
  if (lang !== 'pt' && lang !== 'en') {{
    lang = /^pt/i.test(navigator.language || 'pt') ? 'pt' : 'en';
  }}
  location.replace(lang + '/' + location.hash);
}})();
</script>
<noscript><meta http-equiv="refresh" content="0; url=pt/"></noscript>
<style>body{{background:#080B12;color:#F5F7FB;font-family:system-ui,sans-serif;padding:48px 24px}}a{{color:#8FB1E0}}</style>
</head>
<body>
<p>Arke Analytica — <a href="pt/">Português</a> · <a href="en/">English</a></p>
</body>
</html>
"""


def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", rel)


def main():
    pt = json.loads((ROOT / "content/pt.json").read_text(encoding="utf-8"))
    en = json.loads((ROOT / "content/en.json").read_text(encoding="utf-8"))
    write("index.html", render_root())
    for c, other in ((pt, en), (en, pt)):
        write(f"{c['code']}/index.html", render_home(c))
        write(f"{c['code']}/{c['privacy']['slug']}/index.html", render_privacy(c, other))
    urls = ["pt/", "en/", f"pt/{pt['privacy']['slug']}/", f"en/{en['privacy']['slug']}/"]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{BASE_URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")


if __name__ == "__main__":
    main()
