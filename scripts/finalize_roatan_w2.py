#!/usr/bin/env python3
"""Phase 38B finalize: trailing-slash dirs, inline HTML, sitemap, Workers Assets hardening.

Runs after build-roatan-site / world2_extend / generate_schedule_pages.
Does not alter schedule call data — only chrome/links around existing schedule HTML.
Does not write Pages config.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://roatanexcursionplanner.com"
DATE = "2026-09-15"

EDITORIAL_SLUGS = [
    "about",
    "best-roatan-excursions",
    "contact",
    "glass-bottom-boat-tours-roatan",
    "mahogany-bay-vs-coxen-hole",
    "methodology",
    "one-day-in-roatan",
    "privacy",
    "roatan-beach-breaks",
    "roatan-cruise-port-guide",
    "roatan-excursions-for-first-time-visitors",
    "roatan-family-excursions",
    "roatan-faq",
    "roatan-private-tours",
    "roatan-reef-vs-beach",
    "roatan-sloth-and-monkey-tours",
    "roatan-snorkelling-tours",
    "roatan-wildlife-encounters",
    "roatan-zipline-excursions",
    "terms",
    "west-bay-beach-excursions",
]

# Honest glass-bottom imagery: no false "through the windows" claim
ALT_FIXES = {
    'alt="Tropical fish viewed through glass-bottom boat windows over the Mesoamerican Reef at Roatan Honduras"':
        'alt="Aerial view of shallow turquoise reef water off Roatan, Honduras — scenery glass-bottom boat tours typically visit"',
    'aria-label="Tropical fish viewed through glass-bottom boat windows over the Mesoamerican Reef at Roatan Honduras"':
        'aria-label="Aerial view of shallow turquoise reef water off Roatan, Honduras — scenery glass-bottom boat tours typically visit"',
}


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def soft_copy(text: str) -> str:
    text = text.replace(
        "West Bay Beach consistently ranks among the Caribbean's best strips",
        "West Bay Beach is one of Roatan's most popular cruise-day beaches",
    )
    text = text.replace(
        "West Bay Beach consistently ranks among the Caribbean’s best strips",
        "West Bay Beach is one of Roatan's most popular cruise-day beaches",
    )
    return text


def apply_alt_fixes(text: str) -> str:
    for old, new in ALT_FIXES.items():
        text = text.replace(old, new)
    # Prefer distinct aerial reef asset over byte-identical snorkel duplicate
    text = text.replace("images/glass-bottom-boat.png", "images/west-bay-beach.png")
    text = text.replace("/images/glass-bottom-boat.png", "/images/west-bay-beach.png")
    return text


def html_to_slash(html: str) -> str:
    """Rewrite flat *.html hrefs to apex-relative trailing-slash URLs."""
    html = re.sub(
        r'(href|src)="(?:\./)?index\.html"',
        r'\1="/"',
        html,
    )
    html = re.sub(
        r"(href|src)='(?:\./)?index\.html'",
        r"\1='/'",
        html,
    )

    def repl(m: re.Match[str]) -> str:
        attr, slug = m.group(1), m.group(2)
        if slug == "index":
            return f'{attr}="/"'
        return f'{attr}="/{slug}/"'

    html = re.sub(
        r'(href|src)="(?:\.\./)*(?!https?:|/|#|mailto:|tel:)([a-z0-9][a-z0-9\-]*)\.html"',
        repl,
        html,
        flags=re.I,
    )
    html = re.sub(
        r'href="(?:\.\./)*ship-schedule/"',
        'href="/ship-schedule/"',
        html,
    )
    html = re.sub(
        r'href="(?:\.\./)*ship-schedule/([^"]+)"',
        r'href="/ship-schedule/\1"',
        html,
    )
    html = re.sub(
        r'(src|href)="(?:\.\./)*images/',
        r'\1="/images/',
        html,
    )
    return html


def rewrite_tree(subdir: str) -> int:
    n = 0
    base = ROOT / subdir
    if not base.exists():
        return 0
    for path in base.rglob("*.html"):
        original = path.read_text(encoding="utf-8")
        updated = apply_alt_fixes(soft_copy(html_to_slash(original)))
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            n += 1
    return n


def normalize_canonical(html: str, canon_path: str) -> str:
    if canon_path in ("", "/"):
        url = f"{DOMAIN}/"
    else:
        slug = canon_path.strip("/")
        url = f"{DOMAIN}/{slug}/"
    html = re.sub(
        r'<link rel="canonical" href="[^"]*"\s*/?>',
        f'<link rel="canonical" href="{url}" />',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:url" content="[^"]*"\s*/?>',
        f'<meta property="og:url" content="{url}" />',
        html,
        count=1,
    )
    html = re.sub(
        rf'"{re.escape(DOMAIN)}/([^"]+?)\.html"',
        lambda m: f'"{DOMAIN}/{m.group(1)}/"',
        html,
    )
    return html


def convert_shell_to_dir(slug: str) -> bool:
    flat = ROOT / f"{slug}.html"
    if not flat.exists():
        return False
    text = flat.read_text(encoding="utf-8")
    text = normalize_canonical(text, slug)
    text = apply_alt_fixes(soft_copy(html_to_slash(text)))
    text = re.sub(
        r'(href|src)="(?!https?:|/|#)(js/|css/|images/)',
        r'\1="../\2',
        text,
    )
    text = re.sub(r'data-base=""', 'data-base=".."', text)
    out = ROOT / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    flat.unlink()
    return True


def attr(body_tag: str, name: str) -> str | None:
    m = re.search(rf'\b{name}="([^"]*)"', body_tag)
    return m.group(1) if m else None


def inline_shell(rel_path: str) -> bool:
    text = read(rel_path)
    m = re.search(r"<body([^>]*)>(.*?)</body>", text, re.S | re.I)
    if not m:
        return False
    body_attrs, body_inner = m.group(1), m.group(2)
    if 'data-static="1"' in body_attrs and 'data-inlined="true"' in body_inner:
        return False

    hero_rel = attr(body_attrs, "data-hero") or ""
    trust_rel = attr(body_attrs, "data-trust-strip") or ""
    content_rel = attr(body_attrs, "data-content") or ""
    is_schedule = rel_path.startswith("ship-schedule/")

    nav = read("partials/nav.html") if (ROOT / "partials/nav.html").exists() else ""
    footer = read("partials/footer.html") if (ROOT / "partials/footer.html").exists() else ""
    hero = read(hero_rel) if hero_rel and (ROOT / hero_rel).exists() else ""
    trust = read(trust_rel) if trust_rel and (ROOT / trust_rel).exists() else ""
    content = read(content_rel) if content_rel and (ROOT / content_rel).exists() else ""

    if is_schedule:
        main_m = re.search(
            r'<main id="page-content"[^>]*>(.*?)</main>', body_inner, re.S | re.I
        )
        if main_m and main_m.group(1).strip():
            content = main_m.group(1)

    attrs = body_attrs
    attrs = re.sub(r'\sdata-base="[^"]*"', "", attrs)
    attrs = re.sub(r'\sdata-hero="[^"]*"', "", attrs)
    attrs = re.sub(r'\sdata-trust-strip="[^"]*"', "", attrs)
    attrs = re.sub(r'\sdata-content="[^"]*"', "", attrs)
    if "data-static=" not in attrs:
        attrs += ' data-static="1"'

    scripts = ['<script src="/js/site.js" defer></script>']
    if is_schedule and (ROOT / "js/schedule-search.js").exists():
        scripts.append('<script src="/js/schedule-search.js" defer></script>')

    for frag_name, frag in [
        ("nav", nav),
        ("footer", footer),
        ("hero", hero),
        ("trust", trust),
        ("content", content),
    ]:
        frag = html_to_slash(apply_alt_fixes(soft_copy(frag)))
        frag = re.sub(r'(src|href)="(?:\.\./)*images/', r'\1="/images/', frag)
        # Hero CSS url('images/...') → absolute
        frag = re.sub(r"url\('(?:\.\./)*images/", "url('/images/", frag)
        frag = re.sub(r'url\("(?:\.\./)*images/', 'url("/images/', frag)
        if frag_name == "nav":
            nav = frag
        elif frag_name == "footer":
            footer = frag
        elif frag_name == "hero":
            hero = frag
        elif frag_name == "trust":
            trust = frag
        else:
            content = frag

    new_body = f"""<body{attrs}>
  <div id="site-nav" data-inlined="true">{nav}</div>
  <div id="page-hero" data-inlined="true">{hero}</div>
  <div id="page-trust-strip" data-inlined="true">{trust}</div>
  <main id="page-content">{content}</main>
  <div id="site-footer" data-inlined="true">{footer}</div>
  {"".join(scripts)}
</body>
</html>
"""
    prefix = text[: m.start()]
    if rel_path != "index.html":
        prefix = re.sub(
            r'(href|src)="(?!https?:|/|#)([^"]+)"',
            lambda mm: f'{mm.group(1)}="/{mm.group(2).lstrip("./").lstrip("../")}"',
            prefix,
        )
        prefix = re.sub(r'(href|src)="(?:\.\./)+', r'\1="/', prefix)
        prefix = prefix.replace('href="//', 'href="/').replace('src="//', 'src="/')
        # Fix nested schedule ../js paths already handled; collapse /../
        prefix = re.sub(r'/(?:[^/"\']+/)?\.\./', "/", prefix)

    out = prefix + new_body
    if out.count("</html>") > 1:
        out = out.rsplit("</html>", 1)[0] + "</html>\n"
    write(rel_path, out)
    return True


def write_sitemap() -> int:
    entries: list[tuple[str, str, str]] = [("/", "1.0", "weekly")]
    for slug in EDITORIAL_SLUGS:
        if (ROOT / slug / "index.html").exists():
            pri = "0.8"
            if slug in ("about", "contact", "methodology"):
                pri = "0.5"
            if slug in ("privacy", "terms"):
                pri = "0.3"
            if slug in ("best-roatan-excursions", "roatan-cruise-port-guide", "west-bay-beach-excursions"):
                pri = "0.9"
            entries.append((f"/{slug}/", pri, "monthly"))

    sched_json = ROOT / "data" / "generated" / "schedule-sitemap.json"
    if sched_json.exists():
        raw = json.loads(sched_json.read_text(encoding="utf-8"))
        for item in raw:
            if isinstance(item, (list, tuple)) and len(item) >= 1:
                path = item[0]
                pri = item[1] if len(item) > 1 else "0.7"
                freq = item[2] if len(item) > 2 else "monthly"
            elif isinstance(item, dict):
                path = item.get("path") or item.get("loc", "")
                pri = item.get("priority", "0.7")
                freq = item.get("changefreq", "monthly")
            else:
                continue
            path = str(path).replace(DOMAIN, "")
            if not path.startswith("/"):
                path = "/" + path
            if not path.endswith("/"):
                path += "/"
            entries.append((path, str(pri), str(freq)))
    else:
        for path in sorted((ROOT / "ship-schedule").rglob("index.html")):
            rel = "/" + str(path.parent.relative_to(ROOT)).replace("\\", "/") + "/"
            entries.append((rel, "0.7", "monthly"))

    seen: set[str] = set()
    unique: list[tuple[str, str, str]] = []
    for loc, pri, freq in entries:
        if loc in seen:
            continue
        seen.add(loc)
        unique.append((loc, pri, freq))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, pri, freq in unique:
        lines += [
            "  <url>",
            f"    <loc>{DOMAIN}{loc}</loc>",
            f"    <lastmod>{DATE}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{pri}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")
    return len(unique)


def write_404() -> None:
    write(
        "404.html",
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page not found | Roatan Excursion Planner</title>
  <meta name="description" content="The requested Roatan Excursion Planner page was not found." />
  <meta name="robots" content="noindex, follow" />
  <link rel="canonical" href="{DOMAIN}/404" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{DOMAIN}/404" />
  <meta property="og:title" content="Page not found | Roatan Excursion Planner" />
  <meta property="og:description" content="The requested Roatan Excursion Planner page was not found." />
  <meta property="og:image" content="{DOMAIN}/images/hero-roatan.png" />
  <meta property="og:site_name" content="Roatan Excursion Planner" />
  <meta name="twitter:card" content="summary_large_image" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body class="bg-white text-gray-800 antialiased" data-page="404" data-static="1">
  <div id="site-nav" data-inlined="true"><nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 border-b border-emerald-100 shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-12">
      <a href="/" class="flex items-center gap-2">
        <span class="font-display font-semibold text-emerald-900 text-base leading-tight">Roatan<br/><span class="text-[10px] font-body font-normal text-teal-600 tracking-widest uppercase">Excursion Planner</span></span>
      </a>
      <div class="hidden lg:flex items-center gap-5 text-sm font-medium">
        <a href="/" class="text-gray-600 hover:text-emerald-700 transition-colors">Home</a>
        <a href="/best-roatan-excursions/" class="text-gray-600 hover:text-emerald-700 transition-colors">Excursions</a>
        <a href="/west-bay-beach-excursions/" class="text-gray-600 hover:text-emerald-700 transition-colors">West Bay</a>
        <a href="/ship-schedule/" class="text-gray-600 hover:text-emerald-700 transition-colors">Ship Schedule</a>
        <a href="/contact/" class="text-gray-600 hover:text-emerald-700 transition-colors">Contact</a>
      </div>
    </div>
  </div>
</nav></div>
  <main id="page-content" class="pt-16">
    <section class="pt-10 pb-20 bg-white">
      <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="section-label mx-auto mb-3">404</p>
        <h1 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-4">Page not found</h1>
        <p class="text-gray-600 leading-relaxed mb-8">That URL is not part of the Roatan cruise planning guide. Try the home page, port guide, West Bay Beach, or ship schedule.</p>
        <div class="flex flex-col sm:flex-row gap-3 justify-center flex-wrap">
          <a href="/" class="btn-ocean inline-flex items-center justify-center text-white font-semibold px-6 py-3 rounded-full text-sm no-underline">Roatan home</a>
          <a href="/roatan-cruise-port-guide/" class="btn-outline inline-flex items-center justify-center font-semibold px-6 py-3 rounded-full text-sm no-underline border border-emerald-700 text-emerald-800">Port guide</a>
          <a href="/west-bay-beach-excursions/" class="btn-outline inline-flex items-center justify-center font-semibold px-6 py-3 rounded-full text-sm no-underline border border-emerald-700 text-emerald-800">West Bay</a>
          <a href="/ship-schedule/" class="btn-outline inline-flex items-center justify-center font-semibold px-6 py-3 rounded-full text-sm no-underline border border-emerald-700 text-emerald-800">Ship schedule</a>
        </div>
      </div>
    </section>
  </main>
  <div id="site-footer" data-inlined="true"><footer class="bg-gray-900 text-gray-400 py-10">
  <div class="max-w-7xl mx-auto px-4 text-sm text-center">
    <p class="mb-2 font-display font-semibold text-white">Roatan Excursion Planner</p>
    <p class="mb-4">Independent planning guide for Roatan cruise passengers. Not a booking desk.</p>
    <p><a class="text-emerald-200 hover:text-white" href="mailto:hello@roatanexcursionplanner.com">hello@roatanexcursionplanner.com</a></p>
  </div>
</footer></div>
</body>
</html>
""",
    )


def fix_home_index() -> None:
    path = ROOT / "index.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = normalize_canonical(text, "/")
    text = apply_alt_fixes(soft_copy(html_to_slash(text)))
    path.write_text(text, encoding="utf-8")


def fix_schedule_editorial_links() -> None:
    for path in (ROOT / "ship-schedule").rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        updated = apply_alt_fixes(soft_copy(html_to_slash(text)))
        updated = re.sub(
            r'href="(?:\.\./)+([a-z0-9\-]+)\.html"',
            r'href="/\1/"',
            updated,
            flags=re.I,
        )
        updated = normalize_canonical(
            updated,
            "/" + str(path.parent.relative_to(ROOT)).replace("\\", "/") + "/",
        )
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def fix_glass_bottom_asset() -> None:
    """Remove misleading byte-identical snorkel duplicate; keep file as west-bay copy for any stale refs."""
    src = ROOT / "images" / "west-bay-beach.png"
    dst = ROOT / "images" / "glass-bottom-boat.png"
    if src.exists() and dst.exists():
        if src.read_bytes() != dst.read_bytes():
            # If already distinct, leave; else replace snorkel duplicate
            snorkel = ROOT / "images" / "roatan-snorkelling.png"
            if snorkel.exists() and dst.read_bytes() == snorkel.read_bytes():
                shutil.copyfile(src, dst)
                print("  replaced glass-bottom-boat.png (was snorkel duplicate) with west-bay-beach.png bytes")
        else:
            print("  glass-bottom-boat.png already matches west-bay-beach.png")


def remove_template_shell() -> None:
    tpl = ROOT / "template.html"
    if tpl.exists():
        tpl.unlink()
        print("  removed public template.html from deploy tree (source remains via git history / rebuild)")


def write_workers_config() -> None:
    """Restore hardened Workers Assets config after generative build overwrites."""
    write(
        "wrangler.jsonc",
        """{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "roatan-excursion-planner",
  "main": "worker.js",
  "compatibility_date": "2026-06-04",
  "workers_dev": true,
  "observability": { "enabled": true },
  "assets": {
    "directory": ".",
    "binding": "ASSETS",
    "html_handling": "force-trailing-slash",
    "not_found_handling": "404-page",
    "run_worker_first": true
  },
  "routes": [
    {
      "pattern": "roatanexcursionplanner.com/*",
      "zone_name": "roatanexcursionplanner.com"
    },
    {
      "pattern": "www.roatanexcursionplanner.com/*",
      "zone_name": "roatanexcursionplanner.com"
    }
  ]
}
""",
    )
    write(
        "package.json",
        """{
  "name": "roatan-excursion-planner",
  "private": true,
  "scripts": {
    "sync:schedules": "node scripts/sync-schedules.mjs",
    "qa:schedules": "node scripts/qa-schedules.mjs",
    "build:schedules": "python3 scripts/generate_schedule_pages.py",
    "build": "python3 scripts/build-roatan-site.py && python3 scripts/world2_extend_roatan.py && python3 scripts/generate_schedule_pages.py && python3 scripts/finalize_roatan_w2.py",
    "build:all": "npm run sync:schedules && npm run qa:schedules && npm run build",
    "assemble": "python3 scripts/finalize_roatan_w2.py",
    "deploy": "wrangler deploy",
    "preview": "python3 -m http.server 8900"
  },
  "devDependencies": {
    "wrangler": "^4.94.0"
  }
}
""",
    )
    write(
        "deploy.sh",
        """#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f node_modules/.bin/wrangler ]]; then
  npm install
fi

echo "Building Roatan Excursion Planner (World 2.0 finalize)..."
npm run build

echo "Deploying Roatan Excursion Planner to Cloudflare Workers Assets..."
npx wrangler deploy

echo "Done. Check https://roatanexcursionplanner.com/ shortly."
""",
    )
    (ROOT / "deploy.sh").chmod(0o755)
    write(
        ".assetsignore",
        """\
.git
.gitignore
.wrangler
node_modules
scripts/
content/
partials/
data/
**/__pycache__
*.pyc
.DS_Store
deploy.sh
package-lock.json
package.json
wrangler.jsonc
wrangler.toml
worker.js
template.html
*.md
!images/ATTRIBUTION.md
.assetsignore
.env
.env.*
*.log
*.py
*.mjs
agent-transcripts
""",
    )
    print("  restored wrangler.jsonc, package.json, deploy.sh, .assetsignore")


def main() -> None:
    print("38B finalize: glass-bottom asset honesty…")
    fix_glass_bottom_asset()

    print("38B finalize: rewrite content/partials…")
    print(f"  content files touched: {rewrite_tree('content')}")
    print(f"  partials touched: {rewrite_tree('partials')}")

    print("38B finalize: convert flat shells → slug/index.html…")
    for slug in EDITORIAL_SLUGS:
        if convert_shell_to_dir(slug):
            print(f"  moved {slug}.html → {slug}/index.html")

    fix_home_index()
    fix_schedule_editorial_links()
    remove_template_shell()

    print("38B finalize: assemble server-visible HTML…")
    shells: list[str] = []
    for path in ROOT.rglob("index.html"):
        if any(part.startswith(".") for part in path.parts):
            continue
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if 'id="site-nav"' in text or "data-content=" in text:
            shells.append(str(path.relative_to(ROOT)))
    changed = 0
    for rel in sorted(set(shells)):
        if inline_shell(rel):
            print(f"  inlined {rel}")
            changed += 1
    print(f"  assembled {changed} pages")

    count = write_sitemap()
    print(f"38B finalize: sitemap locs = {count}")
    write_404()
    print("38B finalize: 404.html written")
    write_workers_config()
    print("38B finalize: Workers Assets config restored")
    print("Done.")


if __name__ == "__main__":
    main()
