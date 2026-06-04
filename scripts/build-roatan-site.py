#!/usr/bin/env python3
"""Generate Roatan Excursion Planner static site files."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://roatanexcursionplanner.com"
SITE = "Roatan Excursion Planner"
DATE = "2026-06-04"
BEST_EXCURSIONS_IMG = "images/best-roatan-excursions.png"
BEST_EXCURSIONS_ALT = "Three-toed sloth hanging from a tree branch at a Roatan Honduras wildlife park on a cruise shore excursion"
PORT_GUIDE_IMG = "images/roatan-cruise-port.png"
PORT_GUIDE_ALT = "Aerial view of two cruise ships docked at Mahogany Bay cruise port in Roatan, Honduras, with turquoise Caribbean water and lush green tropical hills"
ONE_DAY_IMG = "images/one-day-in-roatan.png"
ONE_DAY_ALT = "Wonder of the Seas cruise ship docked at Roatan Honduras tropical port, framed by palm trees and lush green hills"
HOME_HERO_IMG = "images/hero-roatan.png"
HOME_HERO_ALT = "Three-toed sloth in crystal-clear turquoise water at Roatan Honduras, with lush tropical palm shoreline above the surface"
WEST_BAY_IMG = "images/west-bay-beach.png"
WEST_BAY_ALT = "Aerial view of West Bay Beach Roatan Honduras with turquoise reef water, white sand and palm-lined resorts along the coastline"
SNORKELLING_IMG = "images/roatan-snorkelling.png"
SNORKELLING_ALT = "Snorkeller swimming over coral reef with tropical fish in clear turquoise water at Roatan Honduras Mesoamerican Reef"
PRIVATE_TOUR_IMG = "images/roatan-private-tours.png"
PRIVATE_TOUR_ALT = "Port of Roatan sign with cruise ship docked at the cruise terminal, Honduras"
WILDLIFE_PARK_IMG = "images/roatan-wildlife-park.png"
WILDLIFE_PARK_ALT = "Spider monkeys playing on tire swings at a Roatan Honduras wildlife park for cruise passengers"
GLASS_BOTTOM_IMG = "images/glass-bottom-boat.png"
GLASS_BOTTOM_ALT = "Tropical fish viewed through glass-bottom boat windows over the Mesoamerican Reef at Roatan Honduras"


def page_shell(
    *,
    title: str,
    description: str,
    keywords: str,
    canonical_path: str,
    data_page: str,
    hero: str,
    content: str,
    preload: str = "images/hero-roatan.png",
    schema: dict | None = None,
    trust: bool = True,
) -> str:
    canon = f"{DOMAIN}/{canonical_path}".rstrip("/") if canonical_path else f"{DOMAIN}/"
    schema_block = ""
    if schema:
        schema_block = (
            f'  <script type="application/ld+json">\n'
            f"{json.dumps(schema, indent=2)}\n"
            f"  </script>\n"
        )
    trust_attr = '\n  data-trust-strip="partials/trust-strip.html"' if trust else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canon}" />
  <link rel="preload" as="image" href="{preload}" fetchpriority="high" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{DOMAIN}/{preload}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />

{schema_block}
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/site.css" />
</head>
<body
  class="bg-white text-gray-800 antialiased"
  data-page="{data_page}"
  data-base=""
  data-hero="{hero}"
  data-content="{content}"{trust_attr}
>

  <div id="site-nav"></div>
  <div id="page-hero"></div>
  <div id="page-trust-strip"></div>
  <main id="page-content"></main>
  <div id="site-footer"></div>

  <script src="js/site.js"></script>
</body>
</html>
"""


def write(path: str, content: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  wrote {path}")


def cruise_snapshot(
    *,
    time_in_port: str,
    best_for: str,
    walking: str,
    family: str,
    return_ship: str,
    popular: str,
) -> str:
    return f"""<aside class="cruise-snapshot mb-10" aria-label="Cruise passenger snapshot">
  <h3 class="font-display font-bold text-lg text-gray-900 mb-4">Cruise Passenger Snapshot</h3>
  <dl class="cruise-snapshot__grid">
    <div class="cruise-snapshot__item"><dt>Typical Time In Port</dt><dd>{time_in_port}</dd></div>
    <div class="cruise-snapshot__item"><dt>Best For</dt><dd>{best_for}</dd></div>
    <div class="cruise-snapshot__item"><dt>Walking Required</dt><dd>{walking}</dd></div>
    <div class="cruise-snapshot__item"><dt>Family Friendly</dt><dd>{family}</dd></div>
    <div class="cruise-snapshot__item"><dt>Return To Ship Friendly</dt><dd>{return_ship}</dd></div>
    <div class="cruise-snapshot__item"><dt>Popular Excursion Types</dt><dd>{popular}</dd></div>
  </dl>
</aside>"""


def _hero_wave() -> str:
    return '<div class="absolute bottom-0 left-0 right-0"><svg viewBox="0 0 1440 48" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="site-hero__wave" aria-hidden="true"><path d="M0 24 C360 48 1080 0 1440 24 L1440 48 L0 48 Z" fill="white"/></svg></div>'


def _hero_inner(
    eyebrow: str,
    title: str,
    lead: str,
    image: str,
    aria: str,
    breadcrumb: str = "",
    cta: tuple[str, str] | None = None,
    tags: list[str] | None = None,
) -> str:
    bc = ""
    if breadcrumb:
        bc = f"""<nav class="site-hero__breadcrumb flex items-center gap-2 mb-4 text-xs text-white/60" aria-label="Breadcrumb">
        <a href="index.html" class="hover:text-white transition-colors">Home</a>
        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-white/80">{breadcrumb}</span>
      </nav>"""
    cta_html = ""
    if cta:
        cta_html = f'<a href="{cta[0]}" class="btn-ocean inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">{cta[1]}</a>'
    tags_html = ""
    if tags:
        tags_html = '<div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">' + "".join(
            f'<span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">{t}</span>'
            for t in tags
        ) + "</div>"
    return f"""<section class="site-hero">
  <div class="absolute inset-0 hero-bg-custom" style="background-image: linear-gradient(135deg, rgba(6, 78, 59, 0.78) 0%, rgba(13, 148, 136, 0.55) 55%, rgba(0, 0, 0, 0.4) 100%), url('{image}');" role="img" aria-label="{aria}"></div>
  <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl">
      {bc}
      <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">{eyebrow}</span>
      </div>
      <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">{title}</h1>
      <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">{lead}</p>
      <div class="site-hero__actions flex flex-col sm:flex-row gap-3">{cta_html}</div>
      {tags_html}
    </div>
  </div>
  {_hero_wave()}
</section>"""


def _card_grid(cards: list[tuple]) -> str:
    items = []
    for img, alt, title, desc, link, label in cards:
        items.append(f"""<div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-emerald-50 flex flex-col">
      <div class="card-media h-44 relative overflow-hidden">
        <img src="{img}" alt="{alt}" width="600" height="352" loading="lazy" decoding="async" />
      </div>
      <div class="p-6 flex flex-col flex-1">
        <h3 class="text-lg font-display font-semibold text-gray-900 mb-2">{title}</h3>
        <p class="text-sm text-gray-500 leading-relaxed flex-1">{desc}</p>
        <a href="{link}" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">{label}</a>
      </div>
    </div>""")
    return '<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">' + "".join(items) + "</div>"


def _internal_links() -> str:
    return """<nav class="mt-10 pt-8 border-t border-gray-100" aria-label="Related Roatan guides">
  <p class="text-sm font-semibold text-gray-900 mb-3">Plan your port day</p>
  <div class="flex flex-wrap gap-3 text-sm">
    <a href="roatan-cruise-port-guide.html" class="text-emerald-700 hover:text-emerald-900 font-medium">Port Guide</a>
    <span class="text-gray-300">·</span>
    <a href="best-roatan-excursions.html" class="text-emerald-700 hover:text-emerald-900 font-medium">Best Excursions</a>
    <span class="text-gray-300">·</span>
    <a href="roatan-wildlife-encounters.html" class="text-emerald-700 hover:text-emerald-900 font-medium">Wildlife</a>
    <span class="text-gray-300">·</span>
    <a href="west-bay-beach-excursions.html" class="text-emerald-700 hover:text-emerald-900 font-medium">Beaches</a>
    <span class="text-gray-300">·</span>
    <a href="roatan-private-tours.html" class="text-emerald-700 hover:text-emerald-900 font-medium">Private Tours</a>
    <span class="text-gray-300">·</span>
    <a href="roatan-faq.html" class="text-emerald-700 hover:text-emerald-900 font-medium">FAQ</a>
  </div>
</nav>"""


# --- Heroes ---

def _hero_home() -> str:
    return f"""  <section class="site-hero">
    <div
      class="absolute inset-0 hero-bg"
      style="background-image: linear-gradient(135deg, rgba(6, 78, 59, 0.78) 0%, rgba(13, 148, 136, 0.55) 55%, rgba(0, 0, 0, 0.4) 100%), url('{HOME_HERO_IMG}');"
      role="img"
      aria-label="{HOME_HERO_ALT}"
    ></div>
    <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="max-w-3xl">
        <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">Honduras · Bay Islands</span>
        </div>
        <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">
          Plan Your Perfect<br/><span class="text-emerald-300">Roatan Port Day</span>
        </h1>
        <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">
          Sloths, monkeys, West Bay Beach and Mesoamerican Reef snorkelling — the experiences cruise passengers actually book in Roatan, timed for your ship schedule.
        </p>
        <div class="site-hero__actions flex flex-col sm:flex-row gap-3">
          <a href="best-roatan-excursions.html" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Explore Excursions</a>
          <a href="roatan-sloth-and-monkey-tours.html" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Wildlife Tours</a>
        </div>
        <div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Sloths</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Monkeys</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">West Bay Beach</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Snorkelling</span>
        </div>
      </div>
    </div>
    {_hero_wave()}
  </section>"""


def _comparison_table() -> str:
    rows = [
        ("Sloth &amp; Monkey Tours", "3–4 hrs", "Families, first-timers", "20–40 min", "roatan-sloth-and-monkey-tours.html"),
        ("West Bay Beach", "4–6 hrs", "Beach lovers", "25–45 min", "west-bay-beach-excursions.html"),
        ("Snorkelling", "3–5 hrs", "Reef &amp; marine life", "15–30 min to boat", "roatan-snorkelling-tours.html"),
        ("Private Tours", "4–8 hrs", "Custom pacing", "Door-to-door", "roatan-private-tours.html"),
        ("Zipline", "2–4 hrs", "Adventure seekers", "30–50 min", "roatan-zipline-excursions.html"),
        ("Glass Bottom Boats", "2–3 hrs", "Non-swimmers", "15–25 min", "glass-bottom-boat-tours-roatan.html"),
    ]
    body = ""
    for name, dur, best, travel, link in rows:
        body += f"""<tr class="border-b border-emerald-50 hover:bg-emerald-50/50">
      <td class="py-4 pr-4 font-semibold text-gray-900"><a href="{link}" class="text-emerald-700 hover:text-emerald-900">{name}</a></td>
      <td class="py-4 px-3 text-gray-600">{dur}</td>
      <td class="py-4 px-3 text-gray-600">{best}</td>
      <td class="py-4 px-3 text-gray-600">{travel}</td>
      <td class="py-4 pl-3"><a href="{link}" class="text-teal-600 font-medium text-xs whitespace-nowrap">Full guide →</a></td>
    </tr>"""
    return f"""<div class="overflow-x-auto rounded-3xl border border-emerald-100 shadow-sm">
  <table class="w-full text-sm text-left min-w-[640px]">
    <thead class="bg-emerald-800 text-white">
      <tr>
        <th class="py-4 px-4 font-semibold rounded-tl-3xl">Excursion Type</th>
        <th class="py-4 px-3 font-semibold">Typical Duration</th>
        <th class="py-4 px-3 font-semibold">Best For</th>
        <th class="py-4 px-3 font-semibold">From Port</th>
        <th class="py-4 px-4 font-semibold rounded-tr-3xl">Details</th>
      </tr>
    </thead>
    <tbody class="bg-white">{body}</tbody>
  </table>
</div>"""


def _hero_excursions() -> str:
    return _hero_inner(
        "Cruise Port · Roatan Honduras",
        "Best Roatan<br/><span class=\"text-emerald-300\">Cruise Excursions</span>",
        "Compare sloth parks, West Bay Beach, reef snorkelling, ziplines, glass-bottom boats and private tours built for your ship schedule.",
        BEST_EXCURSIONS_IMG,
        BEST_EXCURSIONS_ALT,
        breadcrumb="Best Excursions",
    )


def _hero_port() -> str:
    return _hero_inner(
        "Mahogany Bay &amp; Coxen Hole",
        "Roatan<br/><span class=\"text-emerald-300\">Cruise Port Guide</span>",
        "Terminal layout, taxis, safety, currency, weather and how to choose shore excursions on the Bay Islands.",
        PORT_GUIDE_IMG,
        PORT_GUIDE_ALT,
        breadcrumb="Port Guide",
        cta=("best-roatan-excursions.html", "View Shore Excursions →"),
        tags=["🚢 Mahogany Bay", "⚓ Coxen Hole", "🌴 Jungle Tours", "🏖️ West Bay"],
    )


def _hero_one_day() -> str:
    return _hero_inner(
        "Sample Port Day Timeline",
        "One Perfect Day<br/><span class=\"text-emerald-300\">in Roatan</span>",
        "Hour-by-hour itinerary from gangway to departure — wildlife morning, West Bay afternoon, with return-to-ship buffer.",
        ONE_DAY_IMG,
        ONE_DAY_ALT,
        breadcrumb="One Day in Roatan",
    )


def _hero_sloth() -> str:
    return _hero_inner(
        "Jungle Wildlife · Roatan",
        "Sloth &amp; Monkey<br/><span class=\"text-emerald-300\">Tours</span>",
        "Hold sloths, meet capuchin monkeys and explore tropical gardens on the island's most popular cruise excursions.",
        WILDLIFE_PARK_IMG,
        WILDLIFE_PARK_ALT,
        breadcrumb="Sloth & Monkey Tours",
    )


def _hero_west_bay() -> str:
    return _hero_inner(
        "Bay Islands · Honduras",
        "West Bay Beach<br/><span class=\"text-emerald-300\">Excursions</span>",
        "Powder-white sand and calm Caribbean water on Roatan's top-rated beach — chair rentals, snorkel and cruise-friendly returns.",
        WEST_BAY_IMG,
        WEST_BAY_ALT,
        breadcrumb="West Bay Beach",
    )


def _hero_snorkelling() -> str:
    return _hero_inner(
        "Mesoamerican Reef · Roatan",
        "Roatan <span class=\"text-emerald-300\">Snorkelling</span><br/>Tours",
        "Second-largest barrier reef in the world — boat snorkel, reef parks and clear water with gear and guides included.",
        SNORKELLING_IMG,
        SNORKELLING_ALT,
        breadcrumb="Snorkelling Tours",
    )


def _hero_private() -> str:
    return _hero_inner(
        "Custom Shore Excursions",
        "Private Roatan Tours<br/><span class=\"text-teal-300\">Your Way</span>",
        "Your driver, your stops — combine wildlife parks, West Bay, snorkel boats and scenic overlooks at your group's pace.",
        PRIVATE_TOUR_IMG,
        PRIVATE_TOUR_ALT,
        breadcrumb="Private Tours",
    )


def _hero_zipline() -> str:
    return _hero_inner(
        "Jungle Canopy · Roatan",
        "Roatan <span class=\"text-emerald-300\">Zipline</span><br/>Excursions",
        "Fly through tropical canopy on multi-line courses with safety harnesses and guides who know cruise return times.",
        "images/zipline.svg",
        "Zipline canopy tour through Roatan Honduras jungle for cruise passengers",
        breadcrumb="Zipline Excursions",
    )


def _hero_wildlife() -> str:
    return _hero_inner(
        "Bay Islands Nature",
        "Roatan <span class=\"text-emerald-300\">Wildlife</span><br/>Encounters",
        "Sloths, monkeys, iguanas, birds and reef life — the wildlife experiences that define a Roatan port day.",
        WILDLIFE_PARK_IMG,
        WILDLIFE_PARK_ALT,
        breadcrumb="Wildlife Encounters",
    )


def _hero_beach_breaks() -> str:
    return _hero_inner(
        "Relax &amp; Swim · Roatan",
        "Roatan <span class=\"text-emerald-300\">Beach Breaks</span>",
        "Organised beach days with transport, chairs and calm water — West Bay, Sandy Bay and resort strips timed for your ship.",
        WEST_BAY_IMG,
        WEST_BAY_ALT,
        breadcrumb="Beach Breaks",
    )


def _hero_family() -> str:
    return _hero_inner(
        "All Ages Welcome",
        "Roatan <span class=\"text-emerald-300\">Family</span><br/>Excursions",
        "Gentle wildlife parks, calm snorkel spots and beach clubs that work for kids, grandparents and everyone in between.",
        WILDLIFE_PARK_IMG,
        WILDLIFE_PARK_ALT,
        breadcrumb="Family Excursions",
    )


def _hero_first_time() -> str:
    return _hero_inner(
        "First Cruise Stop Here?",
        "First-Time Visitor<br/><span class=\"text-emerald-300\">Guide</span>",
        "Not sure what to book? Match your interests to the right Roatan excursion in one glance.",
        HOME_HERO_IMG,
        HOME_HERO_ALT,
        breadcrumb="First-Time Visitors",
    )


def _hero_glass_bottom() -> str:
    return _hero_inner(
        "Reef Without Getting Wet",
        "Glass Bottom Boat<br/><span class=\"text-emerald-300\">Tours</span>",
        "See coral, fish and reef formations from a shaded boat — ideal for non-swimmers and mixed-age groups.",
        GLASS_BOTTOM_IMG,
        GLASS_BOTTOM_ALT,
        breadcrumb="Glass Bottom Boats",
    )


def _hero_faq() -> str:
    return _hero_inner(
        "Cruise Passenger Planning",
        "Roatan Cruise<br/><span class=\"text-emerald-300\">Excursions FAQ</span>",
        "Port timing, terminals, currency, taxis, wildlife tours and booking independent vs ship excursions.",
        HOME_HERO_IMG,
        HOME_HERO_ALT,
        breadcrumb="FAQ",
    )


def _snapshot_default(**overrides: str) -> str:
    defaults = dict(
        time_in_port="7–10 hours (typical)",
        best_for="Wildlife, beaches, reef snorkelling",
        walking="Low at terminals; varies by tour",
        family="Excellent — parks and calm beaches",
        return_ship="Most operators allow 60–90 min buffer",
        popular="Sloth tours, West Bay, snorkelling, private vans",
    )
    defaults.update(overrides)
    return cruise_snapshot(**defaults)


def _content_home() -> str:
    cards = _card_grid([
        (WILDLIFE_PARK_IMG, WILDLIFE_PARK_ALT, "Sloth & Monkey Tours", "Hold sloths and meet monkeys at jungle parks — Roatan's signature cruise experience.", "roatan-sloth-and-monkey-tours.html", "Wildlife Tours"),
        (WEST_BAY_IMG, WEST_BAY_ALT, "West Bay Beach", "Top-rated Caribbean sand with calm snorkel-friendly water west of the port.", "west-bay-beach-excursions.html", "Beach Guide"),
        (SNORKELLING_IMG, SNORKELLING_ALT, "Snorkelling Tours", "Boat trips to the Mesoamerican Reef with gear, guides and cruise-friendly returns.", "roatan-snorkelling-tours.html", "Snorkelling"),
        (PRIVATE_TOUR_IMG, PRIVATE_TOUR_ALT, "Private Tours", "Custom vans combining wildlife, beaches and reef stops at your group's pace.", "roatan-private-tours.html", "Private Tours"),
    ])
    return f"""<section class="pt-8 pb-16 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
      <div>
        <div class="inline-flex items-center gap-2 text-emerald-700 text-xs font-semibold tracking-widest uppercase mb-3"><div class="w-8 h-px bg-emerald-400"></div>Bay Islands Cruise Port</div>
        <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">Why Cruise Passengers<br/><span class="text-emerald-700">Choose Roatan</span></h2>
        <p class="text-gray-600 leading-relaxed mb-5">Roatan pairs lush Honduran jungle with world-class reef access. Most ships dock at <strong>Mahogany Bay</strong> or <strong>Coxen Hole</strong>, putting sloth sanctuaries, zipline parks and West Bay Beach within a short van ride — perfect for a single port day.</p>
        <p class="text-gray-600 leading-relaxed mb-8">Excursions are built around typical <strong>7–10 hour</strong> calls, with operators planning buffer time before your all-aboard.</p>
        <a href="best-roatan-excursions.html" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Browse All Excursions</a>
      </div>
      <a href="best-roatan-excursions.html" class="info-image block rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden card-hover" aria-label="Best Roatan cruise excursions — sloth wildlife tour">
        <img src="{BEST_EXCURSIONS_IMG}" alt="{BEST_EXCURSIONS_ALT}" width="800" height="600" loading="lazy" decoding="async" />
      </a>
    </div></div></section>
    <section class="py-20 bg-emerald-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-14"><h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900">Popular Roatan Excursion Types</h2>
      <p class="mt-4 text-gray-500 max-w-xl mx-auto">Wildlife, beaches, reef adventures and private tours — matched to your ship schedule.</p></div>
      {cards}
    </div></section>
    <section class="py-20 bg-emerald-900"><div class="max-w-3xl mx-auto px-4 text-center">
      <h2 class="text-3xl font-display font-bold text-white mb-4">Ready for Your Roatan Port Day?</h2>
      <p class="text-emerald-100 mb-8">Compare excursions, read the port guide and check FAQs before you book.</p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="best-roatan-excursions.html" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Browse Excursions</a>
        <a href="roatan-faq.html" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Read FAQs</a>
      </div>
    </div></section>"""


def _content_best() -> str:
    return f"""<section class="pt-8 pb-12 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="max-w-3xl mx-auto text-center mb-12">
        <div class="inline-flex items-center gap-2 text-emerald-700 text-xs font-semibold tracking-widest uppercase mb-3"><div class="w-8 h-px bg-emerald-400"></div>Compare &amp; Choose</div>
        <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">Best Roatan Cruise Excursions</h2>
        <p class="text-gray-600 leading-relaxed">Use this comparison table to match your port day with the right experience. Most tours pick up at <strong>Mahogany Bay</strong> or <strong>Coxen Hole</strong> and return with 60–90 minutes of buffer before all aboard.</p>
      </div>
      {_comparison_table()}
      <div class="mt-12 max-w-3xl mx-auto">{_internal_links()}</div>
    </div></section>"""


def _content_port() -> str:
    snap = _snapshot_default(
        walking="Minimal inside terminals; taxis to town",
        popular="Sloth parks, West Bay, snorkel boats, private tours",
    )
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
      <p class="text-gray-600 leading-relaxed text-center">Roatan receives major cruise lines at two main terminals on the south side of the island. Calls typically run <strong>7–10 hours</strong> — enough for a wildlife park, reef snorkel and a West Bay beach afternoon if you plan transfers carefully.</p>
    </div></section>
    {snap}
    <section id="terminals" class="py-16 bg-gray-50 scroll-mt-12"><div class="max-w-7xl mx-auto px-4">
      <h2 class="text-2xl font-display font-bold text-gray-900 text-center mb-10">Where Ships Dock</h2>
      <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-10 max-w-5xl mx-auto">
        <img src="{PORT_GUIDE_IMG}" alt="{PORT_GUIDE_ALT}" width="1200" height="514" loading="lazy" decoding="async" />
      </div>
      <div class="grid lg:grid-cols-2 gap-8">
        <div class="bg-white rounded-3xl p-8 border border-emerald-100 shadow-sm">
          <h3 class="font-display text-xl font-bold mb-3">Mahogany Bay Cruise Center</h3>
          <p class="text-sm text-gray-600 leading-relaxed">Purpose-built terminal with shops, Wi‑Fi and organised tour desks. Walking village and taxi rank at the exit. Most wildlife and beach vans meet here.</p>
        </div>
        <div class="bg-white rounded-3xl p-8 border border-emerald-100 shadow-sm">
          <h3 class="font-display text-xl font-bold mb-3">Coxen Hole (Town Pier)</h3>
          <p class="text-sm text-gray-600 leading-relaxed">Downtown Roatan port near local markets and banks. Shorter transfer to some west-side beaches; busier traffic at peak call times.</p>
        </div>
      </div>
    </div></section>
    <section id="getting-around" class="py-16 bg-white scroll-mt-12"><div class="max-w-7xl mx-auto px-4">
      <h2 class="text-2xl font-display font-bold text-center mb-10">Walking, Taxis &amp; Safety</h2>
      <div class="grid md:grid-cols-3 gap-6 text-sm">
        <div class="bg-white rounded-3xl p-6 border border-emerald-100 shadow-sm"><strong class="text-gray-900 block mb-2">Walking</strong><p class="text-gray-600">Mahogany Bay's village is walkable from the pier. Coxen Hole connects to downtown shops — stay in busy areas. Excursion zones (parks, West Bay) need a van or taxi.</p></div>
        <div class="bg-white rounded-3xl p-6 border border-emerald-100 shadow-sm"><strong class="text-gray-900 block mb-2">Taxis</strong><p class="text-gray-600">Licensed taxis queue at both terminals. Agree fares in USD before leaving; many drivers offer hourly island tours. Allow extra time on multi-ship days.</p></div>
        <div class="bg-white rounded-3xl p-6 border border-emerald-100 shadow-sm"><strong class="text-gray-900 block mb-2">Safety</strong><p class="text-gray-600">Stick to organised tours and official taxis in port. Secure valuables, avoid isolated areas alone, and follow crew advice — standard practice for Caribbean cruise ports.</p></div>
      </div>
    </div></section>
    <section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4">
      <h2 class="text-2xl font-display font-bold text-center mb-8">Quick Answers</h2>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 text-sm">
        <div class="bg-emerald-50 rounded-2xl p-6"><strong class="text-gray-900">Currency</strong><p class="mt-2 text-gray-600">Honduran lempira (HNL) is official; <strong>US dollars</strong> are widely accepted at excursions, taxis and beach clubs.</p></div>
        <div class="bg-teal-50 rounded-2xl p-6"><strong class="text-gray-900">Language</strong><p class="mt-2 text-gray-600">Spanish is national; English is common in tourism and at both cruise terminals.</p></div>
        <div class="bg-emerald-50 rounded-2xl p-6"><strong class="text-gray-900">Weather</strong><p class="mt-2 text-gray-600">Tropical year-round; brief showers possible. Reef snorkel visibility is usually best on calm mornings.</p></div>
      </div>
    </div></section>
    <section class="py-16 bg-emerald-50"><div class="max-w-7xl mx-auto px-4 text-center">
      <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Best Excursions from the Port</h2>
      <p class="text-gray-600 text-sm max-w-2xl mx-auto mb-8">On a typical 7–10 hour call, cruise guests most often book sloth and monkey parks, West Bay Beach breaks, reef snorkel boats, ziplines, glass-bottom boats or private combo tours.</p>
      <a href="best-roatan-excursions.html" class="btn-ocean inline-flex text-white font-semibold px-8 py-3 rounded-full text-sm shadow-lg">Compare All Excursions</a>
      <p class="mt-8"><a href="one-day-in-roatan.html" class="text-emerald-700 font-semibold text-sm">See sample one-day itinerary →</a></p>
      <div class="mt-10 max-w-3xl mx-auto text-left">{_internal_links()}</div>
    </div></section>"""


def _content_one_day() -> str:
    snap = _snapshot_default(best_for="Wildlife + beach combo days")
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
      <p class="text-gray-600 leading-relaxed">This sample timeline fits a typical <strong>7–10 hour</strong> Roatan call. Adjust for your ship's actual arrival and all-aboard times.</p>
      <div class="info-image rounded-3xl aspect-[4/3] shadow-xl overflow-hidden mt-8 max-w-3xl mx-auto">
        <img src="{ONE_DAY_IMG}" alt="{ONE_DAY_ALT}" width="800" height="600" loading="lazy" decoding="async" />
      </div>
      <p class="mt-6 text-sm"><a href="roatan-cruise-port-guide.html" class="text-emerald-700 font-medium hover:text-emerald-900">Read the port guide →</a></p>
    </div></section>
    {snap}
    <section id="itinerary" class="py-16 bg-emerald-50"><div class="max-w-3xl mx-auto px-4">
      <h2 class="text-2xl font-display font-bold text-gray-900 text-center mb-10">Classic Roatan Port Day</h2>
      <ol class="space-y-4">
        <li class="flex gap-4 bg-white rounded-2xl p-5 border border-emerald-100 shadow-sm"><span class="font-bold text-emerald-700 shrink-0">08:00</span><div><strong>Arrive</strong><p class="text-sm text-gray-600 mt-1">Clear gangway at Mahogany Bay or Coxen Hole; meet pre-booked van or walk to taxi rank.</p></div></li>
        <li class="flex gap-4 bg-white rounded-2xl p-5 border border-emerald-100 shadow-sm"><span class="font-bold text-emerald-700 shrink-0">09:00</span><div><strong>Wildlife Park</strong><p class="text-sm text-gray-600 mt-1">Sloth hold, monkey encounter and garden walk — allow 2–3 hours including transfer.</p></div></li>
        <li class="flex gap-4 bg-white rounded-2xl p-5 border border-emerald-100 shadow-sm"><span class="font-bold text-emerald-700 shrink-0">12:00</span><div><strong>Lunch</strong><p class="text-sm text-gray-600 mt-1">Eat near the park or grab beach snacks en route to West Bay.</p></div></li>
        <li class="flex gap-4 bg-white rounded-2xl p-5 border border-emerald-100 shadow-sm"><span class="font-bold text-emerald-700 shrink-0">13:00</span><div><strong>West Bay Beach</strong><p class="text-sm text-gray-600 mt-1">Swim, snorkel off the sand or relax in chairs — 2–3 hours is ideal.</p></div></li>
        <li class="flex gap-4 bg-white rounded-2xl p-5 border border-emerald-100 shadow-sm"><span class="font-bold text-emerald-700 shrink-0">15:30</span><div><strong>Return to Port</strong><p class="text-sm text-gray-600 mt-1">Drive back with traffic buffer; souvenir stop optional if time allows.</p></div></li>
        <li class="flex gap-4 bg-white rounded-2xl p-5 border border-emerald-100 shadow-sm"><span class="font-bold text-emerald-700 shrink-0">17:00</span><div><strong>Departure</strong><p class="text-sm text-gray-600 mt-1">Board with margin before published all-aboard — never cut it close on ship days.</p></div></li>
      </ol>
      <div class="mt-10">{_internal_links()}</div>
    </div></section>"""


def _content_excursion_page(
    intro: str,
    bullets: list[str],
    snapshot_kwargs: dict,
    img: str,
    alt: str,
) -> str:
    bl = "".join(f"<li class=\"flex gap-2 text-sm text-gray-600\"><span class=\"text-emerald-600\">✓</span>{b}</li>" for b in bullets)
    snap = _snapshot_default(**snapshot_kwargs)
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
      <div>
        <p class="text-gray-600 leading-relaxed mb-6">{intro}</p>
        <ul class="space-y-3 mb-8">{bl}</ul>
      </div>
      <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
        <img src="{img}" alt="{alt}" width="600" height="450" loading="lazy" decoding="async" />
      </div>
    </div></div></section>
    {snap}
    <section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{_internal_links()}</div></section>"""


def _content_sloth() -> str:
    return _content_excursion_page(
        "Sloth and monkey tours are the most-booked Roatan shore excursions. Parks and sanctuaries let you hold sloths under staff supervision, feed or observe monkeys, and walk tropical trails — usually as a half-day trip with hotel-style pickup at the cruise terminals.",
        [
            "Book morning departures to pair with an afternoon beach.",
            "Follow staff instructions — wildlife welfare rules apply.",
            "Wear closed shoes for garden paths; bring cash for photos or snacks.",
            "Combine with a private van if your group wants West Bay the same day.",
        ],
        dict(best_for="Wildlife lovers and families", walking="Light walking on paths", popular="Sloth sanctuaries, monkey encounters"),
        WILDLIFE_PARK_IMG,
        WILDLIFE_PARK_ALT,
    )


def _content_west_bay() -> str:
    return _content_excursion_page(
        "West Bay Beach consistently ranks among the Caribbean's best strips — white sand, gradual entry and snorkel-friendly reef close to shore. Cruise excursions include transport, often chair rental and time to swim before a scheduled return to Mahogany Bay or Coxen Hole.",
        [
            "Allow 25–45 minutes each way from port depending on traffic.",
            "Reef-safe sunscreen protects the Mesoamerican Reef.",
            "Chair vendors and beach bars accept USD at most locations.",
            "Pair with morning wildlife if you want a full island sampler.",
        ],
        dict(best_for="Beach and snorkel from shore", walking="Short walk on sand", popular="West Bay beach breaks, combo tours"),
        WEST_BAY_IMG,
        WEST_BAY_ALT,
    )


def _content_snorkelling() -> str:
    return _content_excursion_page(
        "Roatan sits on the Mesoamerican Reef — the hemisphere's second-largest barrier system. Snorkel boats depart from marinas near the port, supplying masks, fins and a guide who knows currents and cruise return deadlines.",
        [
            "Half-day sails suit most 7–10 hour port calls.",
            "Beginners welcome; listen to crew safety briefings.",
            "Bring a rash guard instead of sunscreens that harm coral.",
            "Glass-bottom boats are an alternative if you prefer not to swim.",
        ],
        dict(best_for="Reef lovers and active swimmers", walking="Boat boarding; optional swim", popular="Reef snorkel, two-stop snorkel sails"),
        SNORKELLING_IMG,
        SNORKELLING_ALT,
    )


def _content_private() -> str:
    return _content_excursion_page(
        "Private vans and SUVs let your group design the day — wildlife park first, West Bay after lunch, scenic stop at a viewpoint, or a snorkel marina drop-off. Drivers who work with cruise guests understand all-aboard pressure and traffic on ship days.",
        [
            "Split cost across families to rival per-person coach pricing.",
            "Share your must-see list when booking — routes are flexible.",
            "Confirm vehicle size for your party and luggage.",
            "Agree on return time in writing or by message.",
        ],
        dict(best_for="Groups wanting custom pacing", walking="Minimal — vehicle-based", popular="Private wildlife + beach combos"),
        PRIVATE_TOUR_IMG,
        PRIVATE_TOUR_ALT,
    )


def _content_zipline() -> str:
    return _content_excursion_page(
        "Jungle zipline courses thread through Roatan's canopy with harnessed lines, platforms and trained guides. Most excursions run 2–4 hours including safety briefing and transfer — leaving afternoon time for a beach if your ship stays late.",
        [
            "Wear closed-toe shoes and secure sunglasses.",
            "Not ideal for guests with serious mobility limitations.",
            "Morning slots avoid afternoon tropical showers.",
            "Check weight/height restrictions when booking.",
        ],
        dict(best_for="Thrill seekers", walking="Short hikes between platforms", popular="Multi-line canopy courses"),
        "images/zipline.svg",
        "Zipline canopy tour Roatan Honduras jungle cruise excursion",
    )


def _content_wildlife() -> str:
    cards = _card_grid([
        (WILDLIFE_PARK_IMG, WILDLIFE_PARK_ALT, "Sloths", "Supervised holds and photo opportunities at licensed parks.", "roatan-sloth-and-monkey-tours.html", "Sloth Tours"),
        (WILDLIFE_PARK_IMG, WILDLIFE_PARK_ALT, "Monkeys", "Spider monkey encounters with staff-led safety briefings.", "roatan-sloth-and-monkey-tours.html", "Monkey Tours"),
        (WILDLIFE_PARK_IMG, WILDLIFE_PARK_ALT, "Island Fauna", "Iguanas, parrots and garden species on guided walks.", "roatan-wildlife-encounters.html", "Learn More"),
        (SNORKELLING_IMG, SNORKELLING_ALT, "Reef Life", "Turtles, rays and tropical fish on snorkel excursions.", "roatan-snorkelling-tours.html", "Snorkelling"),
    ])
    snap = _snapshot_default(best_for="Animal lovers and families", popular="Sloths, monkeys, iguanas, reef snorkel")
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
      <p class="text-gray-600 leading-relaxed text-center">Roatan wildlife spans jungle sanctuaries and reef ecosystems. Cruise guests usually combine a land park with either snorkel or beach time on the same port day.</p>
    </div></section>
    <section class="py-12 bg-emerald-50"><div class="max-w-7xl mx-auto px-4">{cards}</div></section>
    {snap}
    <section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{_internal_links()}</div></section>"""


def _content_beach_breaks() -> str:
    return _content_excursion_page(
        "Organised beach breaks handle transport, timing and often chair rental so you do not negotiate taxis on a busy pier day. West Bay is the headline stop; Sandy Bay and resort beaches offer alternatives when West Bay crowds peak.",
        [
            "Confirm whether lunch and chairs are included.",
            "Bring reef-safe sunscreen and water shoes for rocky entries.",
            "Watch your return van time — beaches are relaxing enough to lose track.",
        ],
        dict(best_for="Relaxation-focused guests", walking="Low — sand and pier walks", popular="West Bay breaks, resort beach clubs"),
        WEST_BAY_IMG,
        WEST_BAY_ALT,
    )


def _content_family() -> str:
    return _content_excursion_page(
        "Families gravitate to gentle wildlife parks, calm West Bay water and snorkel boats with life jackets. Avoid over-stacking the day — kids tire; two stops (park + beach) beat three rushed attractions.",
        [
            "Sloth parks suit toddlers with carrier-friendly paths.",
            "Snorkel operators often offer junior gear — ask when booking.",
            "Private vans simplify nap timing and snack stops.",
            "Ziplines may have age/weight minimums — verify ahead.",
        ],
        dict(best_for="Kids, parents and grandparents", family="Excellent with age-appropriate picks", popular="Wildlife parks, West Bay, gentle snorkel"),
        WILDLIFE_PARK_IMG,
        WILDLIFE_PARK_ALT,
    )


def _content_first_time() -> str:
    snap = _snapshot_default(best_for="Matching interests to tours", popular="See recommendations below")
    recs = [
        ("🦥", "Want animals?", "Sloth & monkey sanctuaries are Roatan's must-do.", "roatan-sloth-and-monkey-tours.html", "Sloth & Monkey Tours", "premium-icon--emerald"),
        ("🏖️", "Want a beach?", "West Bay offers calm swim and shore snorkel.", "west-bay-beach-excursions.html", "West Bay Beach", "premium-icon--emerald"),
        ("🐠", "Want the reef?", "Boat snorkel hits the Mesoamerican Reef.", "roatan-snorkelling-tours.html", "Snorkelling Tours", "premium-icon--emerald"),
        ("🚐", "Want flexibility?", "Private vans stitch stops your way.", "roatan-private-tours.html", "Private Tours", "premium-icon--emerald"),
    ]
    cards = ""
    for icon, heading, text, link, label, pclass in recs:
        cards += f"""<a href="{link}" class="card-hover block bg-white rounded-3xl p-8 border border-emerald-100 shadow-md text-center group">
      <div class="{pclass} w-16 h-16 rounded-2xl flex items-center justify-center text-2xl mx-auto mb-4 shadow-lg">{icon}</div>
      <h3 class="font-display font-bold text-lg text-gray-900 mb-2">{heading}</h3>
      <p class="text-sm text-gray-500 mb-4">{text}</p>
      <span class="text-emerald-700 font-semibold text-sm group-hover:text-emerald-900">{label} →</span>
    </a>"""
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
      <p class="text-gray-600 leading-relaxed">First time in Roatan? Start with what excites you most — the island rewards focused plans over trying to do everything.</p>
    </div></section>
    <section class="py-16 bg-emerald-50"><div class="max-w-7xl mx-auto px-4">
      <h2 class="text-2xl font-display font-bold text-center text-gray-900 mb-10">Match Your Interests</h2>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">{cards}</div>
    </div></section>
    {snap}
    <section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">
      <p class="text-sm text-gray-500 text-center mb-6">New to cruise port planning? Read the <a href="roatan-cruise-port-guide.html" class="text-emerald-700 font-medium">port guide</a> and <a href="one-day-in-roatan.html" class="text-emerald-700 font-medium">sample itinerary</a>.</p>
      {_internal_links()}
    </div></section>"""


def _content_glass_bottom() -> str:
    return _content_excursion_page(
        "Glass-bottom boats let you view coral, sponges and reef fish without entering the water — popular with non-swimmers, older guests and anyone who wants a shaded reef experience. Trips are shorter than full snorkel sails, leaving room for shopping or a wildlife stop.",
        [
            "Morning departures often have calmer water for viewing.",
            "Bring binoculars if you have them — optional but fun.",
            "Still apply reef-safe policies — no touching coral from boats.",
        ],
        dict(best_for="Non-swimmers and mixed ages", walking="Minimal — boat only", popular="Glass-bottom reef tours"),
        GLASS_BOTTOM_IMG,
        GLASS_BOTTOM_ALT,
    )


def _content_faq() -> str:
    return f"""<section class="py-16 bg-white"><div class="max-w-3xl mx-auto px-4 space-y-4">
      <details class="faq-item rounded-2xl border border-emerald-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">How much time do cruise ships spend in Roatan?</summary>
        <p class="mt-4 text-sm text-gray-500">Most calls are 7 to 10 hours. Half-day wildlife or snorkel tours fit easily; combining park + West Bay needs an early start and a late all-aboard.</p></details>
      <details class="faq-item rounded-2xl border border-emerald-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Mahogany Bay vs Coxen Hole — which terminal?</summary>
        <p class="mt-4 text-sm text-gray-500">Your cruise line assigns the pier. Mahogany Bay has a dedicated village; Coxen Hole is closer to downtown. Confirm pickup location when booking independent tours.</p></details>
      <details class="faq-item rounded-2xl border border-emerald-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">What currency should I bring?</summary>
        <p class="mt-4 text-sm text-gray-500">Honduran lempira is official, but US dollars are widely accepted for excursions, taxis and beach vendors. Small change helps for tips.</p></details>
      <details class="faq-item rounded-2xl border border-emerald-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Are sloth and monkey tours ethical?</summary>
        <p class="mt-4 text-sm text-gray-500">Choose licensed parks with trained staff, clear animal-welfare rules and supervised contact. Avoid operators that allow unsupervised handling or stressed animals.</p></details>
      <details class="faq-item rounded-2xl border border-emerald-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Is Roatan safe for independent exploration?</summary>
        <p class="mt-4 text-sm text-gray-500">Tourist zones and organised excursions are heavily visited. Use official taxis, book reputable operators, avoid isolated areas alone, and secure valuables — as in any busy port.</p></details>
      <details class="faq-item rounded-2xl border border-emerald-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Ship excursion or book independently?</summary>
        <p class="mt-4 text-sm text-gray-500">Ship tours guarantee the vessel waits if the operator is late. Established Roatan operators plan returns with buffer — read reviews and confirm policies before paying.</p></details>
      {_internal_links()}
    </div></section>"""


def _faq_schema() -> dict:
    qa = [
        ("How much time do cruise ships spend in Roatan?", "Most calls are 7 to 10 hours. Half-day wildlife or snorkel tours fit easily; combining park and West Bay needs an early start."),
        ("Mahogany Bay vs Coxen Hole — which terminal?", "Your cruise line assigns the pier. Confirm pickup location when booking independent tours."),
        ("What currency should I bring?", "Honduran lempira is official; US dollars are widely accepted for excursions, taxis and beach vendors."),
        ("Are sloth and monkey tours ethical?", "Choose licensed parks with trained staff and supervised contact. Avoid operators with stressed animals."),
        ("Is Roatan safe for independent exploration?", "Use official taxis and reputable operators; secure valuables as in any busy cruise port."),
        ("Ship excursion or book independently?", "Ship tours guarantee the vessel waits if late; reputable local operators plan returns with buffer time."),
    ]
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in qa
        ],
    }


def main() -> None:
    print("Building Roatan site…")

    write(
        "partials/nav.html",
        """<nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 border-b border-emerald-100 shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-12">
      <a href="index.html" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full btn-ocean flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 110-5 2.5 2.5 0 010 5z"/>
          </svg>
        </div>
        <span class="font-display font-semibold text-emerald-900 text-base leading-tight">Roatan<br/><span class="text-[10px] font-body font-normal text-teal-600 tracking-widest uppercase">Excursion Planner</span></span>
      </a>
      <div class="hidden lg:flex items-center gap-5 text-sm font-medium">
        <a href="index.html" data-nav="home" class="text-gray-600 hover:text-emerald-700 transition-colors">Home</a>
        <a href="best-roatan-excursions.html" data-nav="excursions" class="text-gray-600 hover:text-emerald-700 transition-colors">Excursions</a>
        <a href="roatan-wildlife-encounters.html" data-nav="wildlife" class="text-gray-600 hover:text-emerald-700 transition-colors">Wildlife</a>
        <a href="west-bay-beach-excursions.html" data-nav="beaches" class="text-gray-600 hover:text-emerald-700 transition-colors">Beaches</a>
        <a href="roatan-snorkelling-tours.html" data-nav="snorkelling" class="text-gray-600 hover:text-emerald-700 transition-colors">Snorkelling</a>
        <a href="roatan-private-tours.html" data-nav="private" class="text-gray-600 hover:text-emerald-700 transition-colors">Private Tours</a>
        <a href="roatan-cruise-port-guide.html" data-nav="port" class="text-gray-600 hover:text-emerald-700 transition-colors">Port Guide</a>
      </div>
      <a href="best-roatan-excursions.html" class="hidden md:inline-flex items-center gap-2 btn-ocean text-white text-sm font-semibold px-4 py-2 rounded-full shadow-md">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        Book a Tour
      </a>
      <button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-emerald-50" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
</nav>
""",
    )

    write(
        "partials/footer.html",
        f"""  <footer class="bg-gray-900 text-gray-400 py-14">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
        <div class="sm:col-span-2 lg:col-span-1">
          <a href="index.html" class="font-display font-semibold text-white text-lg">{SITE}</a>
          <p class="mt-3 text-sm leading-relaxed">Planning guide for cruise visitors to Roatan, Honduras. Not affiliated with any cruise line.</p>
        </div>
        <div>
          <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Excursions</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="best-roatan-excursions.html" class="hover:text-white transition-colors">All Excursions</a></li>
            <li><a href="roatan-sloth-and-monkey-tours.html" class="hover:text-white transition-colors">Sloth &amp; Monkey Tours</a></li>
            <li><a href="west-bay-beach-excursions.html" class="hover:text-white transition-colors">West Bay Beach</a></li>
            <li><a href="roatan-snorkelling-tours.html" class="hover:text-white transition-colors">Snorkelling</a></li>
            <li><a href="roatan-zipline-excursions.html" class="hover:text-white transition-colors">Zipline</a></li>
            <li><a href="glass-bottom-boat-tours-roatan.html" class="hover:text-white transition-colors">Glass Bottom Boats</a></li>
            <li><a href="roatan-private-tours.html" class="hover:text-white transition-colors">Private Tours</a></li>
            <li><a href="roatan-beach-breaks.html" class="hover:text-white transition-colors">Beach Breaks</a></li>
            <li><a href="roatan-family-excursions.html" class="hover:text-white transition-colors">Family Excursions</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Resources</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="roatan-cruise-port-guide.html" class="hover:text-white transition-colors">Port Guide</a></li>
            <li><a href="one-day-in-roatan.html" class="hover:text-white transition-colors">One Day in Roatan</a></li>
            <li><a href="roatan-wildlife-encounters.html" class="hover:text-white transition-colors">Wildlife Guide</a></li>
            <li><a href="roatan-excursions-for-first-time-visitors.html" class="hover:text-white transition-colors">First-Time Visitors</a></li>
            <li><a href="roatan-faq.html" class="hover:text-white transition-colors">FAQ</a></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">
        <p>&copy; 2026 {SITE}. Verify times and prices with operators before booking.</p>
      </div>
    </div>
  </footer>
""",
    )

    write(
        "partials/trust-strip.html",
        """<section class="trust-strip" aria-label="Roatan cruise excursion highlights">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <ul class="trust-strip__list">
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Wildlife &amp; Adventure</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> West Bay Beach</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Reef Snorkelling</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Cruise-Friendly Returns</li>
    </ul>
  </div>
</section>
""",
    )

    heroes = {
        "hero-home.html": _hero_home(),
        "hero-excursions.html": _hero_excursions(),
        "hero-port-guide.html": _hero_port(),
        "hero-one-day.html": _hero_one_day(),
        "hero-sloth.html": _hero_sloth(),
        "hero-west-bay.html": _hero_west_bay(),
        "hero-snorkelling.html": _hero_snorkelling(),
        "hero-private.html": _hero_private(),
        "hero-zipline.html": _hero_zipline(),
        "hero-wildlife.html": _hero_wildlife(),
        "hero-beach-breaks.html": _hero_beach_breaks(),
        "hero-family.html": _hero_family(),
        "hero-first-time.html": _hero_first_time(),
        "hero-glass-bottom.html": _hero_glass_bottom(),
        "hero-faq.html": _hero_faq(),
    }
    for name, html in heroes.items():
        write(f"partials/{name}", html)

    contents = {
        "home.html": _content_home(),
        "best-roatan-excursions.html": _content_best(),
        "roatan-cruise-port-guide.html": _content_port(),
        "one-day-in-roatan.html": _content_one_day(),
        "roatan-sloth-and-monkey-tours.html": _content_sloth(),
        "west-bay-beach-excursions.html": _content_west_bay(),
        "roatan-snorkelling-tours.html": _content_snorkelling(),
        "roatan-private-tours.html": _content_private(),
        "roatan-zipline-excursions.html": _content_zipline(),
        "roatan-wildlife-encounters.html": _content_wildlife(),
        "roatan-beach-breaks.html": _content_beach_breaks(),
        "roatan-family-excursions.html": _content_family(),
        "roatan-excursions-for-first-time-visitors.html": _content_first_time(),
        "glass-bottom-boat-tours-roatan.html": _content_glass_bottom(),
        "roatan-faq.html": _content_faq(),
    }
    for name, html in contents.items():
        write(f"content/{name}", html)

    pages = [
        dict(file="index.html", title=f"{SITE} | Sloths, West Bay &amp; Reef Tours from the Cruise Port", description="Plan the best Roatan cruise excursions — sloth and monkey tours, West Bay Beach, Mesoamerican Reef snorkelling, ziplines and private shore trips from Mahogany Bay and Coxen Hole.", keywords="Roatan cruise excursions, Roatan shore excursions, Mahogany Bay tours, Coxen Hole cruise port, Honduras cruise excursions", path="", data_page="home", hero="partials/hero-home.html", content="content/home.html", preload=HOME_HERO_IMG, schema={"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": f"{DOMAIN}/", "description": "Planning guide for Roatan cruise shore excursions in Honduras"}),
        dict(file="best-roatan-excursions.html", title="Best Roatan Excursions | Compare Cruise Port Tours", description="Compare the best Roatan cruise excursions — sloth and monkey tours, West Bay Beach, snorkelling, ziplines, glass-bottom boats and private tours with cruise-friendly timing.", keywords="best Roatan excursions, Roatan shore excursions, cruise port tours Roatan, West Bay excursions, sloth tours Roatan", path="best-roatan-excursions.html", data_page="excursions", hero="partials/hero-excursions.html", content="content/best-roatan-excursions.html", preload=BEST_EXCURSIONS_IMG),
        dict(file="roatan-cruise-port-guide.html", title="Roatan Cruise Port Guide | Mahogany Bay &amp; Coxen Hole", description="Complete Roatan cruise port guide — Mahogany Bay and Coxen Hole terminals, taxis, safety, lempira and USD, weather and top shore excursions for cruise passengers.", keywords="Roatan cruise port guide, Mahogany Bay cruise port, Coxen Hole pier, Roatan port day, Honduras cruise port", path="roatan-cruise-port-guide.html", data_page="port", hero="partials/hero-port-guide.html", content="content/roatan-cruise-port-guide.html", preload=PORT_GUIDE_IMG),
        dict(file="one-day-in-roatan.html", title="One Day in Roatan from a Cruise Ship | Port Itinerary", description="How to spend one day in Roatan on a cruise stop — sample timeline from 08:00 arrival through wildlife, lunch, West Bay Beach and 17:00 departure with return-to-ship buffer.", keywords="one day in Roatan cruise, Roatan port day itinerary, Roatan cruise stop planning, Honduras one day cruise", path="one-day-in-roatan.html", data_page="port", hero="partials/hero-one-day.html", content="content/one-day-in-roatan.html", preload=ONE_DAY_IMG),
        dict(file="roatan-sloth-and-monkey-tours.html", title="Roatan Sloth &amp; Monkey Tours | Cruise Port Wildlife Excursions", description="Roatan sloth and monkey tours for cruise passengers — sanctuary visits, supervised encounters and jungle parks with pickup at Mahogany Bay and Coxen Hole.", keywords="Roatan sloth tours, monkey tours Roatan, sloth encounter cruise excursion, Roatan wildlife park", path="roatan-sloth-and-monkey-tours.html", data_page="wildlife", hero="partials/hero-sloth.html", content="content/roatan-sloth-and-monkey-tours.html", preload=WILDLIFE_PARK_IMG),
        dict(file="west-bay-beach-excursions.html", title="West Bay Beach Excursions | Roatan Cruise Beach Days", description="West Bay Beach excursions from Roatan cruise port — transport, chair rental, calm Caribbean water and shore snorkel on Honduras' top-rated beach.", keywords="West Bay Beach Roatan, Roatan beach excursion cruise, West Bay cruise port, Roatan beach day", path="west-bay-beach-excursions.html", data_page="beaches", hero="partials/hero-west-bay.html", content="content/west-bay-beach-excursions.html", preload=WEST_BAY_IMG),
        dict(file="roatan-snorkelling-tours.html", title="Roatan Snorkelling Tours | Mesoamerican Reef Cruise Excursions", description="Roatan snorkelling tours on the Mesoamerican Reef — boat trips, gear and guides with cruise-friendly returns from Mahogany Bay and Coxen Hole.", keywords="Roatan snorkelling tours, Roatan reef snorkel cruise, Mesoamerican Reef excursion, Honduras snorkel cruise", path="roatan-snorkelling-tours.html", data_page="snorkelling", hero="partials/hero-snorkelling.html", content="content/roatan-snorkelling-tours.html", preload=SNORKELLING_IMG),
        dict(file="roatan-private-tours.html", title="Roatan Private Tours | Custom Cruise Shore Excursions", description="Private Roatan tours for cruise passengers — custom wildlife, West Bay and snorkel combinations with flexible timing for your group from the cruise port.", keywords="Roatan private tours, private Roatan shore excursion, custom Honduras cruise tour, Roatan private van cruise", path="roatan-private-tours.html", data_page="private", hero="partials/hero-private.html", content="content/roatan-private-tours.html", preload=PRIVATE_TOUR_IMG),
        dict(file="roatan-zipline-excursions.html", title="Roatan Zipline Excursions | Jungle Canopy Cruise Tours", description="Roatan zipline excursions through tropical canopy — multi-line courses, safety gear and cruise-friendly half-day adventures from the port.", keywords="Roatan zipline excursion, canopy tour Roatan cruise, jungle zipline Honduras cruise port", path="roatan-zipline-excursions.html", data_page="excursions", hero="partials/hero-zipline.html", content="content/roatan-zipline-excursions.html", preload="images/zipline.svg"),
        dict(file="roatan-wildlife-encounters.html", title="Roatan Wildlife Encounters | Sloths, Monkeys &amp; Reef Life", description="Roatan wildlife encounters for cruise guests — sloths, monkeys, iguanas, tropical birds and reef species on organised shore excursions.", keywords="Roatan wildlife encounters, Roatan animals cruise excursion, Honduras wildlife tour Roatan", path="roatan-wildlife-encounters.html", data_page="wildlife", hero="partials/hero-wildlife.html", content="content/roatan-wildlife-encounters.html", preload=WILDLIFE_PARK_IMG),
        dict(file="roatan-beach-breaks.html", title="Roatan Beach Breaks | Organised Cruise Beach Excursions", description="Roatan beach breaks for cruise passengers — West Bay and resort beaches with transport, chairs and timed returns to Mahogany Bay and Coxen Hole.", keywords="Roatan beach breaks cruise, organised beach day Roatan, cruise beach excursion Honduras", path="roatan-beach-breaks.html", data_page="beaches", hero="partials/hero-beach-breaks.html", content="content/roatan-beach-breaks.html", preload=WEST_BAY_IMG),
        dict(file="roatan-family-excursions.html", title="Roatan Family Excursions | Kid-Friendly Cruise Port Tours", description="Family-friendly Roatan excursions — gentle wildlife parks, calm beaches and snorkel boats suited to kids and grandparents on a cruise port day.", keywords="Roatan family excursions, kid friendly Roatan cruise tours, family shore excursion Honduras", path="roatan-family-excursions.html", data_page="wildlife", hero="partials/hero-family.html", content="content/roatan-family-excursions.html", preload=WILDLIFE_PARK_IMG),
        dict(file="roatan-excursions-for-first-time-visitors.html", title="Roatan Excursions for First-Time Visitors | Cruise Port Picks", description="First time in Roatan? Match animals to sloth tours, beaches to West Bay, reef lovers to snorkelling and flexible groups to private tours — with cruise snapshot.", keywords="first time Roatan cruise, Roatan excursions beginners, what to do Roatan cruise port", path="roatan-excursions-for-first-time-visitors.html", data_page="excursions", hero="partials/hero-first-time.html", content="content/roatan-excursions-for-first-time-visitors.html", preload=HOME_HERO_IMG),
        dict(file="glass-bottom-boat-tours-roatan.html", title="Glass Bottom Boat Tours Roatan | Reef Views Without Diving", description="Glass bottom boat tours in Roatan — view Mesoamerican Reef coral and fish from a shaded boat, ideal for non-swimmers on a cruise port day.", keywords="glass bottom boat Roatan, Roatan reef boat tour cruise, non swimmer reef tour Roatan", path="glass-bottom-boat-tours-roatan.html", data_page="snorkelling", hero="partials/hero-glass-bottom.html", content="content/glass-bottom-boat-tours-roatan.html", preload=GLASS_BOTTOM_IMG),
        dict(file="roatan-faq.html", title="Roatan Cruise Excursions FAQ | Port Day Planning Answers", description="FAQ for Roatan cruise excursions — port timing, Mahogany Bay vs Coxen Hole, currency, sloth tours, taxis, beaches and booking independent vs ship excursions.", keywords="Roatan cruise excursions FAQ, Roatan port questions, Honduras cruise port FAQ", path="roatan-faq.html", data_page="port", hero="partials/hero-faq.html", content="content/roatan-faq.html", preload=HOME_HERO_IMG, schema=_faq_schema()),
    ]

    for p in pages:
        write(
            p["file"],
            page_shell(
                title=p["title"],
                description=p["description"],
                keywords=p["keywords"],
                canonical_path=p["path"],
                data_page=p["data_page"],
                hero=p["hero"],
                content=p["content"],
                preload=p.get("preload", HOME_HERO_IMG),
                schema=p.get("schema"),
            ),
        )

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")

    urls = [
        ("", "1.0", "weekly"),
        ("best-roatan-excursions.html", "0.9", "monthly"),
        ("roatan-cruise-port-guide.html", "0.8", "monthly"),
        ("one-day-in-roatan.html", "0.8", "monthly"),
        ("roatan-sloth-and-monkey-tours.html", "0.8", "monthly"),
        ("west-bay-beach-excursions.html", "0.8", "monthly"),
        ("roatan-snorkelling-tours.html", "0.8", "monthly"),
        ("roatan-private-tours.html", "0.8", "monthly"),
        ("roatan-zipline-excursions.html", "0.8", "monthly"),
        ("roatan-wildlife-encounters.html", "0.8", "monthly"),
        ("roatan-beach-breaks.html", "0.8", "monthly"),
        ("roatan-family-excursions.html", "0.8", "monthly"),
        ("roatan-excursions-for-first-time-visitors.html", "0.8", "monthly"),
        ("glass-bottom-boat-tours-roatan.html", "0.8", "monthly"),
        ("roatan-faq.html", "0.7", "monthly"),
    ]
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, priority, freq in urls:
        url = f"{DOMAIN}/{loc}" if loc else f"{DOMAIN}/"
        sitemap_lines += ["  <url>", f"    <loc>{url}</loc>", f"    <lastmod>{DATE}</lastmod>", f"    <changefreq>{freq}</changefreq>", f"    <priority>{priority}</priority>", "  </url>"]
    sitemap_lines.append("</urlset>")
    write("sitemap.xml", "\n".join(sitemap_lines) + "\n")

    write(
        "template.html",
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page Title | {SITE}</title>
  <meta name="description" content="Write a unique meta description for this page (150–160 characters)." />
  <link rel="canonical" href="{DOMAIN}/page-slug.html" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="js/tailwind-config.js"></script>
  <link rel="stylesheet" href="css/site.css" />
</head>
<body class="bg-white text-gray-800 antialiased" data-page="excursions" data-hero="partials/hero-excursions.html" data-content="content/page-starter.html">
  <div id="site-nav"></div>
  <div id="page-hero"></div>
  <main id="page-content"></main>
  <div id="site-footer"></div>
  <script src="js/site.js"></script>
</body>
</html>
""",
    )

    write(
        "package.json",
        """{
  "name": "roatan-excursion-planner",
  "private": true,
  "scripts": {
    "build": "python3 scripts/build-roatan-site.py",
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
        "wrangler.jsonc",
        """{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "roatan-excursion-planner",
  "compatibility_date": "2026-06-04",
  "observability": { "enabled": true },
  "assets": { "directory": "." },
  "routes": [
    {
      "pattern": "roatanexcursionplanner.com",
      "custom_domain": true
    }
  ]
}
""",
    )

    write(
        "deploy.sh",
        f"""#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f node_modules/.bin/wrangler ]]; then
  npm install
fi

echo "Deploying {SITE} to Cloudflare..."
npx wrangler deploy

echo "Done. Check {DOMAIN}/ shortly."
""",
    )

    deploy = ROOT / "deploy.sh"
    deploy.chmod(0o755)

    print("Done.")


if __name__ == "__main__":
    main()
