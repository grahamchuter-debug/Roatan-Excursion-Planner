#!/usr/bin/env python3
"""World 2.0 content extensions for Roatan Excursion Planner.

Runs after build-roatan-site.py. Destination-specific decision architecture for
reef vs beach and Mahogany Bay vs Coxen Hole logistics. Softens wildlife and
buffer claims. Does not modify Cozumel or other masters.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://roatanexcursionplanner.com"
SITE = "Roatan Excursion Planner"
DATE = "2026-09-04"
ACCENT = "text-emerald-300"

_spec = importlib.util.spec_from_file_location(
    "build_roatan", ROOT / "scripts" / "build-roatan-site.py"
)
_build = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_build)

page_shell = _build.page_shell
cruise_snapshot = _build.cruise_snapshot
_hero_inner = _build._hero_inner
write = _build.write
HOME_HERO_IMG = _build.HOME_HERO_IMG
HOME_HERO_ALT = _build.HOME_HERO_ALT
PORT_GUIDE_IMG = _build.PORT_GUIDE_IMG
PORT_GUIDE_ALT = _build.PORT_GUIDE_ALT
WEST_BAY_IMG = _build.WEST_BAY_IMG
WEST_BAY_ALT = _build.WEST_BAY_ALT
SNORKELLING_IMG = _build.SNORKELLING_IMG
SNORKELLING_ALT = _build.SNORKELLING_ALT
WILDLIFE_PARK_IMG = _build.WILDLIFE_PARK_IMG
WILDLIFE_PARK_ALT = _build.WILDLIFE_PARK_ALT
ONE_DAY_IMG = _build.ONE_DAY_IMG
ONE_DAY_ALT = _build.ONE_DAY_ALT
BEST_EXCURSIONS_IMG = _build.BEST_EXCURSIONS_IMG
BEST_EXCURSIONS_ALT = _build.BEST_EXCURSIONS_ALT
_hero_wave = _build._hero_wave


def soft_claims_in_text(html: str) -> str:
    replacements = [
        (
            r"Most operators allow 60[--]90 min buffer",
            "Build your own buffer; confirm operator return plan",
        ),
        (
            r"return with 60[--]90 minutes of buffer before all aboard",
            "return with a sensible buffer before all aboard (confirm with the operator)",
        ),
        (
            r"Operators usually allow 60[--]90 min buffer",
            "Build your own buffer; confirm operator return plan",
        ),
        (
            r"Ship-sold tours often include a wait-if-late policy from the cruise line.",
            "Ship-sold tours often include a wait-if-late policy from the cruise line.",
        ),
        (
            r"Ship tours guarantee wait-if-late; reputable locals plan buffer returns\.",
            "Ship-sold tours often include wait-if-late; confirm independent operator policies and build your own buffer.",
        ),
        (
            r"Hold sloths and meet monkeys at jungle parks[^\.]*\.",
            "Supervised park visits where sloth and monkey encounters are possible - confirm current welfare rules with the operator.",
        ),
        (
            r"Hold sloths, meet capuchin monkeys and explore tropical gardens on the island's most popular cruise excursions\.",
            "Visit licensed parks where supervised sloth and monkey encounters may be offered - rules and availability vary by operator.",
        ),
        (
            r"let you hold sloths under staff supervision, feed or observe monkeys",
            "may include supervised sloth time and monkey observation under staff rules",
        ),
        (
            r"Well-regarded Caribbean sand",
            "Well-known Caribbean sand",
        ),
        (
            r"Well-regarded beach",
            "popular beach stretch",
        ),
        (
            r"world-class reef access",
            "Mesoamerican Reef access close to many west-side stops",
        ),
        (
            r"Sloth hold, monkey encounter and garden walk",
            "Wildlife park visit (encounters vary) and garden walk",
        ),
        (
            r"Supervised holds and photo opportunities at licensed parks\.",
            "Supervised encounters may be offered at licensed parks - confirm rules and whether handling is allowed.",
        ),
        (
            r"Spider monkey encounters with staff-led safety briefings\.",
            "Monkey observation or supervised encounters may be offered with staff briefings - not guaranteed on every visit.",
        ),
        (
            r"Book a Tour",
            "Plan your day",
        ),
    ]
    out = html
    for pat, repl in replacements:
        out = re.sub(pat, repl, out)
    # Strip em dashes in editorial copy (keep generated schedule comments alone if present)
    out = out.replace("\u2014", " - ").replace("\u2013", "-")
    return out


def soft_all_content() -> None:
    for folder in (ROOT / "content", ROOT / "partials"):
        if not folder.exists():
            continue
        for path in folder.glob("*.html"):
            original = path.read_text(encoding="utf-8")
            updated = soft_claims_in_text(original)
            if updated != original:
                path.write_text(updated, encoding="utf-8")
                print(f"  softened {path.relative_to(ROOT)}")


def internal_links() -> str:
    return """<nav class="mt-10 pt-8 border-t border-gray-100" aria-label="Related Roatan guides">
  <p class="text-sm font-semibold text-gray-900 mb-3">Plan your Roatan port day</p>
  <div class="flex flex-wrap gap-3 text-sm">
    <a href="roatan-cruise-port-guide.html" class="text-emerald-700 hover:text-emerald-900 font-medium">Port Guide</a>
    <span class="text-gray-300">·</span>
    <a href="best-roatan-excursions.html" class="text-emerald-700 hover:text-emerald-900 font-medium">Best Excursions</a>
    <span class="text-gray-300">·</span>
    <a href="roatan-reef-vs-beach.html" class="text-emerald-700 hover:text-emerald-900 font-medium">Reef vs Beach</a>
    <span class="text-gray-300">·</span>
    <a href="mahogany-bay-vs-coxen-hole.html" class="text-emerald-700 hover:text-emerald-900 font-medium">Mahogany Bay vs Coxen Hole</a>
    <span class="text-gray-300">·</span>
    <a href="ship-schedule/" class="text-emerald-700 hover:text-emerald-900 font-medium">Ship Schedule</a>
    <span class="text-gray-300">·</span>
    <a href="roatan-faq.html" class="text-emerald-700 hover:text-emerald-900 font-medium">FAQ</a>
  </div>
</nav>"""


def concierge_panel() -> str:
    return """<section class="py-14 bg-white" id="concierge" aria-labelledby="concierge-heading">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="concierge-panel">
      <h2 id="concierge-heading" class="font-display font-bold text-2xl sm:text-3xl mb-3">Need help shaping your Roatan day?</h2>
      <p class="text-white/90 text-sm sm:text-base leading-relaxed mb-4">
        Tell us your ship, call date, and whether you lean reef snorkelling, West Bay sand, a wildlife park visit or a private island loop.
        We are an independent planning resource - not the cruise line and not a ticket marketplace.
      </p>
      <p class="text-white/80 text-sm leading-relaxed mb-5">
        email <a href="mailto:hello@roatanexcursionplanner.com">hello@roatanexcursionplanner.com</a> with your ship, date and preferences.
        We do not promise instant replies or 24/7 staffing.
      </p>
      <div class="flex flex-col sm:flex-row gap-3">
        <a href="mailto:hello@roatanexcursionplanner.com" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-6 py-3 rounded-full text-sm no-underline">Email the Roatan planner</a>
        <a href="best-roatan-excursions.html" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-6 py-3 rounded-full text-sm no-underline">Compare excursion types</a>
      </div>
    </div>
  </div>
</section>"""


def snapshot(**overrides: str) -> str:
    defaults = dict(
        time_in_port="7-10 hours (typical)",
        best_for="Reef snorkel, West Bay, wildlife parks",
        walking="Low at terminals; varies by tour",
        family="Strong with age-appropriate picks",
        return_ship="Build your own buffer; confirm operator return plan",
        popular="West Bay, reef boats, wildlife parks, private vans",
    )
    defaults.update(overrides)
    return cruise_snapshot(**defaults)


def write_nav() -> None:
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
        <a href="west-bay-beach-excursions.html" data-nav="beaches" class="text-gray-600 hover:text-emerald-700 transition-colors">West Bay</a>
        <a href="roatan-snorkelling-tours.html" data-nav="snorkelling" class="text-gray-600 hover:text-emerald-700 transition-colors">Snorkelling</a>
        <a href="ship-schedule/" data-nav="schedule" class="text-gray-600 hover:text-emerald-700 transition-colors">Ship Schedule</a>
        <a href="roatan-cruise-port-guide.html" data-nav="port" class="text-gray-600 hover:text-emerald-700 transition-colors">Port Guide</a>
      </div>
      <a href="contact.html" class="hidden md:inline-flex items-center gap-2 btn-ocean text-white text-sm font-semibold px-4 py-2 rounded-full shadow-md">
        Contact planner
      </a>
      <button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-emerald-50" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
</nav>
""",
    )


def write_footer() -> None:
    write(
        "partials/footer.html",
        f"""  <footer class="bg-gray-900 text-gray-400 py-14">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
        <div class="sm:col-span-2 lg:col-span-1">
          <a href="index.html" class="font-display font-semibold text-white text-lg">{SITE}</a>
          <p class="mt-3 text-sm leading-relaxed">Independent planning guide for cruise visitors to Roatan, Honduras. Not affiliated with any cruise line.</p>
        </div>
        <div>
          <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Excursions</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="best-roatan-excursions.html" class="hover:text-white transition-colors">All Excursions</a></li>
            <li><a href="west-bay-beach-excursions.html" class="hover:text-white transition-colors">West Bay Beach</a></li>
            <li><a href="roatan-snorkelling-tours.html" class="hover:text-white transition-colors">Snorkelling</a></li>
            <li><a href="roatan-sloth-and-monkey-tours.html" class="hover:text-white transition-colors">Wildlife Parks</a></li>
            <li><a href="roatan-reef-vs-beach.html" class="hover:text-white transition-colors">Reef vs Beach</a></li>
            <li><a href="mahogany-bay-vs-coxen-hole.html" class="hover:text-white transition-colors">Mahogany Bay vs Coxen Hole</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Resources</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="roatan-cruise-port-guide.html" class="hover:text-white transition-colors">Port Guide</a></li>
            <li><a href="ship-schedule/" class="hover:text-white transition-colors">Ship Schedule</a></li>
            <li><a href="one-day-in-roatan.html" class="hover:text-white transition-colors">One Day in Roatan</a></li>
            <li><a href="roatan-faq.html" class="hover:text-white transition-colors">FAQ</a></li>
            <li><a href="methodology.html" class="hover:text-white transition-colors">Methodology</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Legal</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="about.html" class="hover:text-white transition-colors">About</a></li>
            <li><a href="contact.html" class="hover:text-white transition-colors">Contact</a></li>
            <li><a href="privacy.html" class="hover:text-white transition-colors">Privacy</a></li>
            <li><a href="terms.html" class="hover:text-white transition-colors">Terms</a></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">
        <p>&copy; 2026 {SITE}. Confirm times with your cruise line and operators. No fabricated prices or ratings on this site.</p>
      </div>
    </div>
  </footer>
""",
    )


def hero_home() -> str:
    return f"""  <section class="site-hero">
    <div class="absolute inset-0 hero-bg" style="background-image: linear-gradient(135deg, rgba(6, 78, 59, 0.78) 0%, rgba(13, 148, 136, 0.55) 55%, rgba(0, 0, 0, 0.4) 100%), url('{HOME_HERO_IMG}');" role="img" aria-label="{HOME_HERO_ALT}"></div>
    <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="max-w-3xl">
        <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">Honduras · Bay Islands</span>
        </div>
        <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">
          Roatan<br/><span class="{ACCENT}">Excursion Planner</span>
        </h1>
        <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">
          Step ashore on Roatan and choose reef time on the Mesoamerican Barrier, West Bay sand, or a supervised wildlife park visit - planned around your ship and a sensible return window.
        </p>
        <div class="site-hero__actions flex flex-col sm:flex-row gap-3">
          <a href="roatan-reef-vs-beach.html" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Reef or beach day?</a>
          <a href="ship-schedule/" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Find your ship</a>
        </div>
        <div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Mesoamerican Reef</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">West Bay</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Wildlife parks</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Two arrival facilities</span>
        </div>
      </div>
    </div>
    {_hero_wave()}
  </section>"""


def content_home() -> str:
    snap = snapshot()
    return f"""<section class="pt-8 pb-6 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
  <p class="section-label mx-auto">Bay Islands cruise call</p>
  <h2 class="text-2xl sm:text-3xl font-display font-bold text-gray-900 mb-3">Roatan is reef, beach and island logistics</h2>
  <p class="text-gray-600 text-sm sm:text-base leading-relaxed">Ships may use <strong>Mahogany Bay</strong> or <strong>Coxen Hole</strong> - confirm your facility with the cruise line. From either side of the south coast you can chase Mesoamerican Reef snorkelling, West Bay sand, or a wildlife park visit where animal encounters are possible but never promised.</p>
</div></section>
<section class="pb-10 bg-white"><div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="decision-grid">
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Reef / snorkel day</h3><p>Boat trips or shore snorkel toward the Mesoamerican Reef - gear, guides and return timing matter more than brochure fish counts.</p><a href="roatan-snorkelling-tours.html" class="text-emerald-700 font-semibold text-sm">Snorkelling →</a></div>
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Beach day</h3><p>West Bay for sand, calm entry and optional shore snorkel when you want swimming over boat time.</p><a href="west-bay-beach-excursions.html" class="text-emerald-700 font-semibold text-sm">West Bay →</a></div>
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Wildlife park</h3><p>Licensed parks may offer supervised sloth or monkey encounters. Treat sightings and handling as chance-based and rule-bound.</p><a href="roatan-sloth-and-monkey-tours.html" class="text-emerald-700 font-semibold text-sm">Wildlife parks →</a></div>
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Reef vs beach</h3><p>Honest trade-offs between boat reef time and lounger time on a typical 7-10 hour call.</p><a href="roatan-reef-vs-beach.html" class="text-emerald-700 font-semibold text-sm">Compare →</a></div>
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Which facility?</h3><p>Mahogany Bay and Coxen Hole are different arrival points. Do not assume one dock for every ship.</p><a href="mahogany-bay-vs-coxen-hole.html" class="text-emerald-700 font-semibold text-sm">Facilities →</a></div>
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Find your ship</h3><p>Search Roatan call dates, then leave a sensible return window before all aboard.</p><a href="ship-schedule/" class="text-emerald-700 font-semibold text-sm">Ship schedule →</a></div>
  </div>
</div></section>
<section class="py-12 bg-emerald-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <p class="section-label">Arrival orientation</p>
    <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Two facilities, one island day</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Cruise documents name your arrival facility. Mahogany Bay is a purpose-built cruise centre; Coxen Hole sits nearer town markets. Transfer times to West Bay and wildlife parks vary with traffic - confirm pickup with your operator for the pier you actually use.</p>
    <a href="mahogany-bay-vs-coxen-hole.html" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Mahogany Bay vs Coxen Hole</a>
  </div>
  <div class="info-image rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden">
    <img src="{PORT_GUIDE_IMG}" alt="{PORT_GUIDE_ALT}" width="800" height="600" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="pb-4 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-10">
    <p class="section-label mx-auto">Signature choices</p>
    <h2 class="text-3xl font-display font-bold text-gray-900 mb-3">Three Roatan days cruise guests compare most</h2>
  </div>
  <div class="grid sm:grid-cols-3 gap-6">
    <div class="bg-white rounded-3xl overflow-hidden shadow-md border border-emerald-50 flex flex-col">
      <div class="card-media h-44"><img src="{SNORKELLING_IMG}" alt="{SNORKELLING_ALT}" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Reef snorkel</h3><p class="text-sm text-gray-500 flex-1">Boat-based Mesoamerican Reef time with gear and a timed return window.</p><a href="roatan-snorkelling-tours.html" class="mt-5 text-emerald-700 font-semibold text-sm">Snorkelling →</a></div>
    </div>
    <div class="bg-white rounded-3xl overflow-hidden shadow-md border border-emerald-50 flex flex-col">
      <div class="card-media h-44"><img src="{WEST_BAY_IMG}" alt="{WEST_BAY_ALT}" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">West Bay Beach</h3><p class="text-sm text-gray-500 flex-1">Sand, swimming and optional shore snorkel west of the south-coast facilities.</p><a href="west-bay-beach-excursions.html" class="mt-5 text-emerald-700 font-semibold text-sm">West Bay →</a></div>
    </div>
    <div class="bg-white rounded-3xl overflow-hidden shadow-md border border-emerald-50 flex flex-col">
      <div class="card-media h-44"><img src="{WILDLIFE_PARK_IMG}" alt="{WILDLIFE_PARK_ALT}" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Wildlife parks</h3><p class="text-sm text-gray-500 flex-1">Park visits where sloth or monkey encounters may be offered under staff rules.</p><a href="roatan-sloth-and-monkey-tours.html" class="mt-5 text-emerald-700 font-semibold text-sm">Wildlife →</a></div>
    </div>
  </div>
  <p class="text-center mt-8"><a href="best-roatan-excursions.html" class="text-emerald-700 font-semibold text-sm">Full comparison →</a></p>
</div></section>
<section class="py-12 bg-emerald-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <p class="section-label">Ship planning</p>
    <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Match the day to your Roatan call</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Browse arrivals by month, note your all-aboard window, then choose reef, beach or park intensity. Schedules can change - treat published times as planning aids and build your own buffer.</p>
    <a href="ship-schedule/" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm">Find your ship schedule</a>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="{ONE_DAY_IMG}" alt="{ONE_DAY_ALT}" width="800" height="600" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="py-16 cta-gradient"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-white mb-4">Still deciding?</h2>
  <p class="text-white/85 text-sm mb-6">Compare reef versus beach, or email the Roatan planner with your ship and date.</p>
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    <a href="roatan-reef-vs-beach.html" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Reef vs beach</a>
    <a href="contact.html" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Contact planner</a>
  </div>
</div></section>
{concierge_panel()}"""


def content_reef_vs_beach() -> str:
    snap = snapshot(
        best_for="Choosing boat reef time vs West Bay sand",
        walking="Boat low-moderate; beach short sand walks",
        popular="Snorkel boats vs West Bay beach breaks",
    )
    return f"""<section class="pt-8 pb-6 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
  <p class="text-gray-600 leading-relaxed mb-4">On a typical Roatan call, many guests choose between a <strong>reef / snorkel day</strong> and a <strong>West Bay beach day</strong>. Both can be excellent. They spend hours differently.</p>
  <p class="text-gray-600 leading-relaxed">Reef boats maximise underwater time with gear and a guide. Beach days maximise swimming, shade and optional shore snorkel without a fixed boat itinerary.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-emerald-50"><div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-2xl font-display font-bold text-gray-900 text-center mb-8">Reef day vs beach day</h2>
  <div class="grid md:grid-cols-2 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-emerald-100">
      <div class="card-media rounded-2xl overflow-hidden aspect-[16/10] mb-4">
        <img src="{SNORKELLING_IMG}" alt="{SNORKELLING_ALT}" width="600" height="375" loading="lazy" decoding="async" />
      </div>
      <h3 class="font-display font-bold text-lg mb-3">Reef / snorkel day</h3>
      <ul class="space-y-2 text-gray-600">
        <li>Boat trips toward Mesoamerican Reef sites with supplied gear</li>
        <li>Better when underwater time matters more than loungers</li>
        <li>Visibility and marine life vary with weather and season</li>
        <li>Confirm return window in writing with the operator</li>
      </ul>
      <p class="mt-4"><a href="roatan-snorkelling-tours.html" class="text-emerald-700 font-semibold">Snorkelling →</a> · <a href="glass-bottom-boat-tours-roatan.html" class="text-emerald-700 font-semibold">Glass-bottom →</a></p>
    </div>
    <div class="bg-white rounded-3xl p-6 border border-emerald-100">
      <div class="card-media rounded-2xl overflow-hidden aspect-[16/10] mb-4">
        <img src="{WEST_BAY_IMG}" alt="{WEST_BAY_ALT}" width="600" height="375" loading="lazy" decoding="async" />
      </div>
      <h3 class="font-display font-bold text-lg mb-3">West Bay beach day</h3>
      <ul class="space-y-2 text-gray-600">
        <li>Sand, swimming and optional shore snorkel near resorts</li>
        <li>Better when shade and flexible pacing matter</li>
        <li>Transfer time from either facility depends on traffic</li>
        <li>Pair with a morning park visit only if the call is long enough</li>
      </ul>
      <p class="mt-4"><a href="west-bay-beach-excursions.html" class="text-emerald-700 font-semibold">West Bay →</a> · <a href="roatan-beach-breaks.html" class="text-emerald-700 font-semibold">Beach breaks →</a></p>
    </div>
  </div>
  <div class="mt-10 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>
{concierge_panel()}"""


def content_mahogany_vs_coxen() -> str:
    snap = snapshot(
        best_for="Understanding Roatan arrival facilities before booking pickups",
        walking="Minimal inside terminals; tours need transport",
        popular="Confirm facility on cruise documents - do not guess",
    )
    return f"""<section class="pt-8 pb-6 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
  <p class="text-gray-600 leading-relaxed mb-4"><strong>Mahogany Bay</strong> and <strong>Coxen Hole</strong> are related Roatan arrival facilities on the south side of the island. They are not interchangeable meeting points. Ships may use different facilities - this site does not assign specific ships to docks.</p>
  <p class="text-gray-600 leading-relaxed">Confirm your facility on cruise documents or the ship app before you book a pickup. Operators who support both still need the correct gate or taxi rank.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-emerald-50"><div class="max-w-5xl mx-auto px-4">
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8 max-w-5xl mx-auto">
    <img src="{PORT_GUIDE_IMG}" alt="{PORT_GUIDE_ALT}" width="1200" height="514" loading="lazy" decoding="async" />
  </div>
  <div class="grid md:grid-cols-2 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-emerald-100">
      <h3 class="font-display font-bold text-lg mb-3">Mahogany Bay Cruise Center</h3>
      <ul class="space-y-2 text-gray-600">
        <li>Purpose-built cruise village with shops and organised tour desks</li>
        <li>Walking village and taxi rank at the exit on a typical call</li>
        <li>Many west-side beach and park vans meet here when the ship uses this facility</li>
      </ul>
    </div>
    <div class="bg-white rounded-3xl p-6 border border-emerald-100">
      <h3 class="font-display font-bold text-lg mb-3">Coxen Hole (town pier)</h3>
      <ul class="space-y-2 text-gray-600">
        <li>Downtown-adjacent port near markets and banks</li>
        <li>Different walking distances and traffic patterns than Mahogany Bay</li>
        <li>Some west-side transfers can be shorter - still confirm with your operator</li>
      </ul>
    </div>
  </div>
  <p class="mt-8 text-sm text-gray-600 leading-relaxed">Excursion types (reef, West Bay, wildlife parks) can work from either facility when logistics are booked correctly. The schedule hub lists Roatan calls without inventing a pier split - use it for dates, then verify the facility with your cruise line.</p>
  <p class="mt-4"><a href="roatan-cruise-port-guide.html" class="text-emerald-700 font-semibold">Port guide →</a> · <a href="ship-schedule/" class="text-emerald-700 font-semibold">Ship schedule →</a></p>
  <div class="mt-10 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>
{concierge_panel()}"""


def content_port() -> str:
    snap = snapshot(
        walking="Minimal inside terminals; taxis to town and west side",
        popular="Confirm facility, then beach, reef or park plans",
        best_for="Orienting at Mahogany Bay or Coxen Hole before west-side plans",
    )
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <p class="text-gray-600 leading-relaxed text-sm">Roatan is a <strong>pier port</strong> with more than one cruise facility. Calls typically run <strong>7-10 hours</strong>. Confirm whether you arrive at <strong>Mahogany Bay</strong> or <strong>Coxen Hole</strong> before locking a pickup point.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-emerald-50"><div class="max-w-7xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold text-center mb-8">Where ships arrive</h2>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8 max-w-5xl mx-auto">
    <img src="{PORT_GUIDE_IMG}" alt="{PORT_GUIDE_ALT}" width="1200" height="514" loading="lazy" decoding="async" />
  </div>
  <div class="grid lg:grid-cols-2 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-emerald-100"><h3 class="font-display font-bold text-lg mb-2">Mahogany Bay</h3><p class="text-gray-600">Purpose-built cruise centre. Confirm meeting points inside the complex with your operator.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-emerald-100"><h3 class="font-display font-bold text-lg mb-2">Coxen Hole</h3><p class="text-gray-600">Town pier with different layout and traffic. Do not assume the same taxi rank as Mahogany Bay.</p></div>
  </div>
  <p class="text-center mt-8"><a href="mahogany-bay-vs-coxen-hole.html" class="text-emerald-700 font-semibold text-sm">Facility comparison →</a>
  <span class="text-gray-300 mx-2">·</span>
  <a href="ship-schedule/" class="text-emerald-700 font-semibold text-sm">Ship schedule →</a></p>
  <div class="mt-10 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>
{concierge_panel()}"""


def content_sloth() -> str:
    snap = snapshot(
        best_for="Families considering supervised wildlife park visits",
        walking="Light walking on park paths",
        popular="Licensed parks - encounters vary by rules and day",
    )
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6">Wildlife park visits are a popular Roatan shore option. Licensed parks may offer supervised sloth time and monkey observation under staff rules. Treat encounters as chance-based and confirm whether handling is allowed on the day you visit.</p>
    <ul class="space-y-3 mb-8">
      <li class="flex gap-2 text-sm text-gray-600"><span class="text-emerald-600">✓</span>Morning departures leave room for an afternoon beach if the call is long enough</li>
      <li class="flex gap-2 text-sm text-gray-600"><span class="text-emerald-600">✓</span>Follow staff instructions - welfare rules apply and can change</li>
      <li class="flex gap-2 text-sm text-gray-600"><span class="text-emerald-600">✓</span>Wear closed shoes for garden paths; bring cash for optional extras</li>
      <li class="flex gap-2 text-sm text-gray-600"><span class="text-emerald-600">✓</span>Confirm pickup for Mahogany Bay or Coxen Hole - do not guess the facility</li>
    </ul>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="{WILDLIFE_PARK_IMG}" alt="{WILDLIFE_PARK_ALT}" width="600" height="450" loading="lazy" decoding="async" />
  </div>
</div></div></section>
{snap}
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>
{concierge_panel()}"""


def content_wildlife() -> str:
    snap = snapshot(best_for="Comparing park visits with reef wildlife from boats")
    return f"""<section class="pt-8 pb-6 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-4">Roatan wildlife for cruise guests usually means <strong>licensed park visits</strong> (where supervised encounters may be offered) and <strong>reef life</strong> seen while snorkelling. Neither is a guarantee of specific animals on a given day.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-emerald-50"><div class="max-w-5xl mx-auto px-4 text-sm">
  <div class="grid md:grid-cols-2 gap-6">
    <div class="bg-white rounded-3xl p-6 border border-emerald-100">
      <h3 class="font-display font-bold text-lg mb-2">Park visits</h3>
      <p class="text-gray-600 mb-3">Sloth and monkey experiences, when offered, follow staff rules. Confirm inclusions and whether handling is permitted.</p>
      <a href="roatan-sloth-and-monkey-tours.html" class="text-emerald-700 font-semibold">Wildlife parks →</a>
    </div>
    <div class="bg-white rounded-3xl p-6 border border-emerald-100">
      <h3 class="font-display font-bold text-lg mb-2">Reef life</h3>
      <p class="text-gray-600 mb-3">Fish and coral viewing depends on site, weather and visibility. Glass-bottom boats suit non-swimmers.</p>
      <a href="roatan-snorkelling-tours.html" class="text-emerald-700 font-semibold">Snorkelling →</a>
    </div>
  </div>
  <div class="mt-10 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>
{concierge_panel()}"""


def content_about() -> str:
    return f"""<section class="pt-10 pb-16 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">About Roatan Excursion Planner</h2>
  <p class="text-gray-600 leading-relaxed mb-4">Roatan sits on the Mesoamerican Reef with West Bay sand and wildlife parks a transfer away from south-coast cruise facilities. This site exists to make reef, beach and logistics trade-offs clear before you spend the call.</p>
  <p class="text-gray-600 leading-relaxed mb-4">We write for passengers weighing snorkel boats against West Bay, and for guests who need honest language about Mahogany Bay versus Coxen Hole. We are not a cruise line, ticket marketplace or port authority.</p>
  <p class="text-gray-600 leading-relaxed mb-4">Ship schedules here are synced from the Caribbean Shore Excursions authority import for Roatan only. Arrival and departure times can still change; confirm with your cruise line.</p>
  <p class="text-gray-600 leading-relaxed mb-8">Network context: <a href="https://caribbeanshoreexcursion.com/" class="text-emerald-700 font-medium">Caribbean Shore Excursions</a>. Destination detail for Roatan lives on this site.</p>
  {internal_links()}
</div></section>
{concierge_panel()}"""


def content_contact() -> str:
    return f"""<section class="pt-10 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Contact</h2>
  <p class="text-gray-600 leading-relaxed mb-4">If you want help narrowing a Roatan port day, include your ship name, call date, arrival facility if known, and whether you prefer reef snorkelling, West Bay, a wildlife park visit or a private loop.</p>
  <p class="text-gray-600 leading-relaxed mb-6"><a class="text-emerald-700 font-semibold" href="mailto:hello@roatanexcursionplanner.com">hello@roatanexcursionplanner.com</a>. Replies are handled when we can - this is a planning concierge, not a booking desk.</p>
  <ul class="space-y-2 text-sm text-gray-600 mb-8">
    <li><a class="text-emerald-700 font-semibold" href="ship-schedule/">Find your ship schedule</a></li>
    <li><a class="text-emerald-700 font-semibold" href="best-roatan-excursions.html">Compare excursion types</a></li>
    <li><a class="text-emerald-700 font-semibold" href="mahogany-bay-vs-coxen-hole.html">Mahogany Bay vs Coxen Hole</a></li>
    <li><a class="text-emerald-700 font-semibold" href="roatan-reef-vs-beach.html">Reef vs beach decision</a></li>
  </ul>
  {internal_links()}
</div></section>
{concierge_panel()}"""


def content_privacy() -> str:
    return """<section class="pt-10 pb-16 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Privacy</h2>
  <p class="text-gray-600 leading-relaxed mb-4">This is a static planning website. In this phase we do not operate a booking engine, payment system, or passenger account database.</p>
  <p class="text-gray-600 leading-relaxed mb-4">Messages sent to hello@roatanexcursionplanner.com are used only to respond about Roatan port-day planning. We will not sell contact details.</p>
  <p class="text-gray-600 leading-relaxed mb-4">Standard web server and CDN logs may record technical request data as part of delivering the site securely. We do not add analytics trackers in this build.</p>
  <p class="text-gray-600 leading-relaxed">If our contact or tooling practices change, this page will be updated before those features go live.</p>
</div></section>"""


def content_terms() -> str:
    return """<section class="pt-10 pb-16 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Terms of use</h2>
  <p class="text-gray-600 leading-relaxed mb-4">Content on Roatan Excursion Planner is provided for general information and planning. It is not a contract of carriage, not travel insurance, and not a guarantee of excursion availability, wildlife encounters, weather or on-time return to your ship.</p>
  <p class="text-gray-600 leading-relaxed mb-4">Cruise schedules, pier operations and excursion details can change. Confirm final arrangements with your cruise line and any operator you choose.</p>
  <p class="text-gray-600 leading-relaxed mb-4">We are independent of cruise lines and of Roatan port operators. Mentions of beaches, parks or reefs are for orientation and do not imply partnership unless we say so explicitly.</p>
  <p class="text-gray-600 leading-relaxed">You are responsible for leaving enough time to reboard, for following local rules, and for checking any medical or activity requirements before water or adventure activities.</p>
</div></section>"""


def content_methodology() -> str:
    return f"""<section class="pt-10 pb-16 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">How we assess Roatan excursions</h2>
  <p class="text-gray-600 leading-relaxed mb-4">We judge options the way a cruise passenger has to: against call length, arrival facility logistics, transfer time to West Bay or reef boats, and how much return buffer you need before all aboard.</p>
  <div class="space-y-4 text-sm text-gray-600 mb-8">
    <div class="bg-emerald-50 rounded-2xl p-5 border border-emerald-100"><h3 class="font-display font-bold text-gray-900 mb-2">Cruise timing first</h3><p>A packed wildlife-plus-beach mash-up is the wrong answer on a short call. We favour options that leave a realistic return window.</p></div>
    <div class="bg-teal-50 rounded-2xl p-5 border border-teal-100"><h3 class="font-display font-bold text-gray-900 mb-2">Facility honesty</h3><p>Mahogany Bay and Coxen Hole are different arrival points. We do not invent which ships use which dock.</p></div>
    <div class="bg-emerald-50 rounded-2xl p-5 border border-emerald-100"><h3 class="font-display font-bold text-gray-900 mb-2">No invented proof</h3><p>We do not invent star ratings, review counts, guaranteed wildlife or fabricated prices.</p></div>
    <div class="bg-teal-50 rounded-2xl p-5 border border-teal-100"><h3 class="font-display font-bold text-gray-900 mb-2">Schedule integrity</h3><p>Call lists are generated from the Caribbean authority import for Roatan, then checked for count and record-level match before pages are built.</p></div>
  </div>
  {internal_links()}
</div></section>
{concierge_panel()}"""


NEW_PAGES = [
    dict(
        file="roatan-reef-vs-beach.html",
        title="Roatan Reef vs Beach Day | Cruise Decision Guide",
        description="Compare a Roatan reef snorkel day with a West Bay beach day on a cruise call - honest trade-offs for Mesoamerican Reef time versus sand.",
        keywords="Roatan reef vs beach, West Bay vs snorkelling, Roatan cruise decision",
        path="roatan-reef-vs-beach.html",
        data_page="excursions",
        hero="partials/hero-reef-vs-beach.html",
        content="content/roatan-reef-vs-beach.html",
        preload=SNORKELLING_IMG,
    ),
    dict(
        file="mahogany-bay-vs-coxen-hole.html",
        title="Mahogany Bay vs Coxen Hole | Roatan Cruise Facilities",
        description="Honest comparison of Mahogany Bay and Coxen Hole for Roatan cruise passengers - confirm your facility before booking pickups.",
        keywords="Mahogany Bay vs Coxen Hole, Roatan cruise port facilities, Roatan pier comparison",
        path="mahogany-bay-vs-coxen-hole.html",
        data_page="port",
        hero="partials/hero-mahogany-vs-coxen.html",
        content="content/mahogany-bay-vs-coxen-hole.html",
        preload=PORT_GUIDE_IMG,
    ),
    dict(
        file="about.html",
        title="About Roatan Excursion Planner | Independent Port Planning",
        description="About Roatan Excursion Planner - independent planning guidance for cruise passengers calling at Roatan, Honduras.",
        keywords="about Roatan Excursion Planner, Roatan cruise planning",
        path="about.html",
        data_page="contact",
        hero="partials/hero-port-guide.html",
        content="content/about.html",
        preload=PORT_GUIDE_IMG,
    ),
    dict(
        file="contact.html",
        title="Contact Roatan Excursion Planner | Concierge",
        description="Contact the Roatan Excursion Planner at hello@roatanexcursionplanner.com for port-day planning help.",
        keywords="contact Roatan Excursion Planner, Roatan cruise concierge",
        path="contact.html",
        data_page="contact",
        hero="partials/hero-port-guide.html",
        content="content/contact.html",
        preload=PORT_GUIDE_IMG,
    ),
    dict(
        file="privacy.html",
        title="Privacy | Roatan Excursion Planner",
        description="Privacy policy for Roatan Excursion Planner - static planning site practices.",
        keywords="privacy Roatan Excursion Planner",
        path="privacy.html",
        data_page="contact",
        hero="partials/hero-port-guide.html",
        content="content/privacy.html",
        preload=PORT_GUIDE_IMG,
    ),
    dict(
        file="terms.html",
        title="Terms of Use | Roatan Excursion Planner",
        description="Terms of use for Roatan Excursion Planner planning content.",
        keywords="terms Roatan Excursion Planner",
        path="terms.html",
        data_page="contact",
        hero="partials/hero-port-guide.html",
        content="content/terms.html",
        preload=PORT_GUIDE_IMG,
    ),
    dict(
        file="methodology.html",
        title="How We Assess Roatan Excursions | Methodology",
        description="How Roatan Excursion Planner assesses cruise excursion options - timing, honest claims and schedule integrity.",
        keywords="Roatan excursion methodology, how we choose Roatan tours",
        path="methodology.html",
        data_page="contact",
        hero="partials/hero-port-guide.html",
        content="content/methodology.html",
        preload=PORT_GUIDE_IMG,
    ),
]


def merge_sitemap(extra: list[tuple[str, str, str]]) -> None:
    sitemap_path = ROOT / "sitemap.xml"
    existing: list[tuple[str, str, str]] = []
    if sitemap_path.exists():
        text = sitemap_path.read_text(encoding="utf-8")
        locs = re.findall(r"<loc>(.*?)</loc>", text)
        freqs = re.findall(r"<changefreq>(.*?)</changefreq>", text)
        pris = re.findall(r"<priority>(.*?)</priority>", text)
        for i, loc in enumerate(locs):
            path = loc.replace(DOMAIN + "/", "").replace(DOMAIN, "")
            if path == "/":
                path = ""
            freq = freqs[i] if i < len(freqs) else "monthly"
            pri = pris[i] if i < len(pris) else "0.5"
            existing.append((path, pri, freq))

    by_path = {p: (pri, freq) for p, pri, freq in existing}
    for path, pri, freq in extra:
        by_path[path] = (pri, freq)

    frag = ROOT / "data" / "generated" / "schedule-sitemap.json"
    if frag.exists():
        try:
            for path, pri, freq in json.loads(frag.read_text(encoding="utf-8")):
                by_path[path] = (pri, freq)
        except json.JSONDecodeError:
            pass

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, (pri, freq) in sorted(by_path.items(), key=lambda x: (x[0] != "", x[0])):
        url = f"{DOMAIN}/{path}" if path else f"{DOMAIN}/"
        lines += [
            "  <url>",
            f"    <loc>{url}</loc>",
            f"    <lastmod>{DATE}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{pri}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")


def write_package_json() -> None:
    write(
        "package.json",
        """{
  "name": "roatan-excursion-planner",
  "private": true,
  "scripts": {
    "sync:schedules": "node scripts/sync-schedules.mjs",
    "qa:schedules": "node scripts/qa-schedules.mjs",
    "build:schedules": "python3 scripts/generate_schedule_pages.py",
    "build": "python3 scripts/build-roatan-site.py && python3 scripts/world2_extend_roatan.py && python3 scripts/generate_schedule_pages.py",
    "build:all": "npm run sync:schedules && npm run qa:schedules && npm run build",
    "deploy": "wrangler deploy",
    "preview": "python3 -m http.server 8900"
  },
  "devDependencies": {
    "wrangler": "^4.94.0"
  }
}
""",
    )


def ensure_decision_css() -> None:
    css_path = ROOT / "css" / "site.css"
    css = css_path.read_text(encoding="utf-8")
    if ".decision-grid" not in css:
        css += """
.section-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #0d9488;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}
.decision-grid {
  display: grid;
  gap: 1rem;
}
@media (min-width: 640px) {
  .decision-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 1024px) {
  .decision-grid { grid-template-columns: repeat(3, 1fr); }
}
.decision-card {
  background: #fff;
  border: 1px solid #d1fae5;
  border-radius: 1.25rem;
  padding: 1.25rem 1.35rem;
}
.decision-card h3 {
  font-size: 1.05rem;
  margin-bottom: 0.4rem;
}
.decision-card p {
  font-size: 0.875rem;
  color: #4b5563;
  line-height: 1.55;
  margin-bottom: 0.75rem;
}
.concierge-panel {
  background: linear-gradient(135deg, #064e3b 0%, #0d9488 100%);
  border-radius: 1.5rem;
  padding: 2rem;
  color: #fff;
}
"""
        css_path.write_text(css, encoding="utf-8")
        print("  updated css/site.css with decision styles")


def main() -> None:
    print("World 2.0 extending Roatan Excursion Planner…")
    ensure_decision_css()
    write_nav()
    write_footer()
    write("partials/hero-home.html", hero_home())
    write(
        "partials/hero-reef-vs-beach.html",
        _hero_inner(
            "Roatan decision",
            f"Reef Day vs<br/><span class=\"{ACCENT}\">Beach Day</span>",
            "Mesoamerican Reef snorkel time versus West Bay sand - choose how to spend a Roatan cruise call.",
            SNORKELLING_IMG,
            SNORKELLING_ALT,
            breadcrumb="Reef vs Beach",
        ),
    )
    write(
        "partials/hero-mahogany-vs-coxen.html",
        _hero_inner(
            "Arrival facilities",
            f"Mahogany Bay vs<br/><span class=\"{ACCENT}\">Coxen Hole</span>",
            "Two Roatan cruise facilities - confirm yours before booking pickups. We do not assign ships to docks.",
            PORT_GUIDE_IMG,
            PORT_GUIDE_ALT,
            breadcrumb="Mahogany Bay vs Coxen Hole",
        ),
    )

    write("content/home.html", content_home())
    write("content/roatan-cruise-port-guide.html", content_port())
    write("content/roatan-reef-vs-beach.html", content_reef_vs_beach())
    write("content/mahogany-bay-vs-coxen-hole.html", content_mahogany_vs_coxen())
    write("content/roatan-sloth-and-monkey-tours.html", content_sloth())
    write("content/roatan-wildlife-encounters.html", content_wildlife())
    write("content/about.html", content_about())
    write("content/contact.html", content_contact())
    write("content/privacy.html", content_privacy())
    write("content/terms.html", content_terms())
    write("content/methodology.html", content_methodology())

    soft_all_content()

    for p in NEW_PAGES:
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
            ),
        )

    write(
        "index.html",
        page_shell(
            title=f"{SITE} | Reef, West Bay &amp; Port Logistics",
            description="Independent Roatan Excursion Planner for cruise passengers - Mesoamerican Reef snorkelling, West Bay Beach, wildlife park visits and honest Mahogany Bay versus Coxen Hole logistics.",
            keywords="Roatan excursion planner, Roatan cruise excursions, West Bay Beach, Mesoamerican Reef, Mahogany Bay, Coxen Hole",
            canonical_path="",
            data_page="home",
            hero="partials/hero-home.html",
            content="content/home.html",
            schema={
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": SITE,
                "url": f"{DOMAIN}/",
                "description": "Planning guide for Roatan cruise shore excursions in Honduras",
            },
        ),
    )

    extra = [
        ("roatan-reef-vs-beach.html", "0.8", "monthly"),
        ("mahogany-bay-vs-coxen-hole.html", "0.8", "monthly"),
        ("about.html", "0.5", "yearly"),
        ("contact.html", "0.5", "yearly"),
        ("privacy.html", "0.3", "yearly"),
        ("terms.html", "0.3", "yearly"),
        ("methodology.html", "0.5", "yearly"),
    ]
    merge_sitemap(extra)
    write_package_json()
    print("World 2.0 extend done.")


if __name__ == "__main__":
    main()
