from __future__ import annotations

import html
import shutil
from pathlib import Path
try:
    from .content import EXPERIENCE, LANES, PROJECTS, SITE
except ImportError:
    from content import EXPERIENCE, LANES, PROJECTS, SITE


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
FEATURED_PROJECT_SLUGS = (
    "financial-process-automation-scraping",
    "gcp-lakehouse-dbt-bigquery",
    "erp-to-bigquery-finance-analytics",
    "meta-ads-to-bigquery-pipeline",
    "dagster-dbt-orchestration-pipeline",
    "ai-automation-engineer-workflows",
)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def clean_dist() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)


def repo_url(repo: str) -> str:
    return f"https://github.com/brunoluizmendes/{repo}"


def cta_url() -> str:
    return SITE["calendly_url"] or SITE["upwork_url"]


def t(language: str, en: str, pt: str) -> str:
    return en if language == "en" else pt


def lane_by_key() -> dict[str, dict]:
    return {lane["key"]: lane for lane in LANES}


def grouped_projects() -> list[tuple[dict, list[dict]]]:
    mapping = lane_by_key()
    return [(lane, [project for project in PROJECTS if project["lane"] == lane["key"]]) for lane in LANES]


def featured_projects() -> list[dict]:
    featured = [project for project in PROJECTS if project["slug"] in FEATURED_PROJECT_SLUGS]
    return sorted(featured, key=lambda item: FEATURED_PROJECT_SLUGS.index(item["slug"]))


def project_lane(project: dict) -> dict:
    return lane_by_key()[project["lane"]]


def route_prefix(language: str) -> str:
    return "" if language == "en" else "/pt"


def language_href(language: str, route: str) -> str:
    if language == "en":
        return f"/pt{route}" if route != "/" else "/pt/"
    return route[3:] if route.startswith("/pt") else "/"


def page_title(language: str, custom_title: str | None = None) -> str:
    base = SITE["name"]
    if custom_title:
        return f"{custom_title} | {base}"
    return f"{base} | {t(language, SITE['role_en'], SITE['role_pt'])}"


def page_description(language: str, custom_description: str | None = None) -> str:
    return custom_description or t(language, SITE["subheadline_en"], SITE["subheadline_pt"])


def theme_bootstrap_script() -> str:
    return """<script>
(() => {
  const key = "b-tech-theme-v2";
  let theme = "light";
  try {
    const stored = window.localStorage.getItem(key);
    if (stored === "light" || stored === "dark") {
      theme = stored;
    }
  } catch (error) {
    theme = "light";
  }
  document.documentElement.setAttribute("data-theme", theme);
})();
</script>"""


def head_markup(language: str, route: str, title: str | None = None, description: str | None = None) -> str:
    canonical = f"{SITE['site_url']}{route}"
    alternate_language = "pt-BR" if language == "en" else "en"
    alternate_route = language_href(language, route)
    alternate_canonical = f"{SITE['site_url']}{alternate_route}"
    locale = "en_US" if language == "en" else "pt_BR"
    locale_alternate = "pt_BR" if language == "en" else "en_US"
    page_title_text = html.escape(page_title(language, title))
    page_description_text = html.escape(page_description(language, description))
    return f"""<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title_text}</title>
  <meta name="description" content="{page_description_text}">
  <meta name="robots" content="index,follow">
  <meta name="theme-color" content="{SITE['palette']['secondary']}" id="theme-color-meta">
  <meta property="og:title" content="{page_title_text}">
  <meta property="og:description" content="{page_description_text}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{locale}">
  <meta property="og:locale:alternate" content="{locale_alternate}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE['site_url']}/assets/og-card.svg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{page_title_text}">
  <meta name="twitter:description" content="{page_description_text}">
  <meta name="twitter:image" content="{SITE['site_url']}/assets/og-card.svg">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="{language}" href="{canonical}">
  <link rel="alternate" hreflang="{alternate_language}" href="{alternate_canonical}">
  <link rel="alternate" hreflang="x-default" href="{SITE['site_url']}/">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="manifest" href="/site.webmanifest">
  {theme_bootstrap_script()}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/styles.css">
  <script defer src="/assets/app.js"></script>
</head>"""


def email_icon_markup() -> str:
    email = SITE.get("email")
    if not email:
        return ""
    return f'<a href="mailto:{html.escape(email)}" class="header-social-icon" aria-label="Email">{icon("mail")}</a>'


def header_markup(language: str, route: str) -> str:
    home = route_prefix(language) or "/"
    if home == "":
        home = "/"
    nav_items = [
        (f"{home}#services", t(language, "Services", "Servicos")),
        (f"{home}#contact", t(language, "Contact", "Contato")),
    ]
    nav = "".join(
        f'<a href="{href}" class="nav-link">{html.escape(label)}</a>' for href, label in nav_items
    )
    switch_to = language_href(language, route)
    switch_label = "PT" if language == "en" else "EN"
    current_label = "EN" if language == "en" else "PT"
    theme_to_light = t(language, "Switch to light mode", "Mudar para modo claro")
    theme_to_dark = t(language, "Switch to dark mode", "Mudar para modo escuro")
    return f"""<header class="site-header" data-open="false">
  <div class="header-start">
    <a href="{SITE['calendly_url']}" class="button button-primary button-compact header-cta" target="_blank" rel="noreferrer">{html.escape(t(language, 'Book a call', 'Agendar conversa'))}<span class="header-cta-dot" aria-hidden="true"></span></a>
    <div class="header-socials">
      <a href="{SITE['linkedin_url']}" class="header-social-icon" target="_blank" rel="noreferrer" aria-label="LinkedIn">{icon('linkedin')}</a>
      {email_icon_markup()}
      <a href="{SITE['github_url']}" class="header-social-icon" target="_blank" rel="noreferrer" aria-label="GitHub">{icon('github')}</a>
    </div>
  </div>
  <a class="brand" href="{home}">
    <img src="/assets/brand-mark.svg" alt="{html.escape(SITE['logo_alt'])}" class="brand-mark">
    <span class="brand-text">
      <strong>{html.escape(SITE['name'])}</strong>
      <span>{html.escape(t(language, SITE['role_en'], SITE['role_pt']))}</span>
    </span>
  </a>
  <div class="header-end">
  <button class="menu-toggle" type="button" aria-label="{html.escape(t(language, 'Toggle navigation', 'Abrir navegacao'))}">
    <span class="menu-toggle-icon menu-toggle-open" aria-hidden="true">{icon('menu')}</span>
    <span class="menu-toggle-icon menu-toggle-close" aria-hidden="true">{icon('close')}</span>
  </button>
  <nav class="site-nav">
    {nav}
    <button
      class="theme-switch"
      type="button"
      data-theme-toggle
      data-label-dark="{html.escape(theme_to_dark)}"
      data-label-light="{html.escape(theme_to_light)}"
      aria-label="{html.escape(theme_to_light)}"
    >
      <span class="theme-option theme-option-dark" aria-hidden="true">{theme_moon_icon()}</span>
      <span class="theme-option theme-option-light" aria-hidden="true">{theme_sun_icon()}</span>
    </button>
    <a href="{switch_to}" class="lang-switch" hreflang="{switch_label.lower()}">
      <span class="lang-current">{current_label}</span>
      <span class="lang-next">{switch_label}</span>
    </a>
    <span class="header-clock" data-clock aria-hidden="true"></span>
  </nav>
  </div>
</header>"""


def footer_markup(language: str) -> str:
    primary_label = t(language, "Book a call", "Agendar uma conversa")
    secondary_label = t(language, "Connect on LinkedIn", "Conectar no LinkedIn")
    closing_en = "Have a system in mind?"
    closing_pt = "Tem um sistema em mente?"
    next_step_en = "Book a 20-minute call to walk through the problem — no deck, no obligation."
    next_step_pt = "Agende uma call de 20 minutos para conversar sobre o problema — sem apresentacao, sem compromisso."
    return f"""<footer class="site-footer" id="contact">
  {svg_blob(BLOB_FOOTER_PATH, "blobFooter", "footer-blob")}
  <div class="footer-halftone halftone" aria-hidden="true"></div>
  <div class="footer-grid">
    <div>
      <p class="eyebrow">{html.escape(t(language, 'Contact', 'Contato'))}</p>
      <h2>{html.escape(t(language, closing_en, closing_pt))}</h2>
      <p class="footer-copy">{html.escape(t(language, SITE['about_en'], SITE['about_pt']))}</p>
      <p class="footer-next-step">{html.escape(t(language, next_step_en, next_step_pt))}</p>
    </div>
    <div class="footer-actions">
      <a href="{SITE['calendly_url']}" class="button button-primary" target="_blank" rel="noreferrer">{html.escape(primary_label)}{icon('arrow-up-right', 'icon icon-inline')}</a>
      <a href="{SITE['linkedin_url']}" class="button button-secondary" target="_blank" rel="noreferrer">{html.escape(secondary_label)}{icon('arrow-up-right', 'icon icon-inline')}</a>
    </div>
  </div>
  <div class="footer-meta">
    <div class="footer-links">
      <a href="{SITE['linkedin_url']}" target="_blank" rel="noreferrer">LinkedIn</a>
      <a href="{SITE['upwork_url']}" target="_blank" rel="noreferrer">Upwork</a>
    </div>
    <p>© 2026 {html.escape(SITE['name'])}</p>
  </div>
  {ascii_strip_markup()}
</footer>"""


def ascii_strip_markup() -> str:
    pattern = "!!((%%@@**::  "
    line = html.escape((pattern * 40)[:520])
    return f'<div class="ascii-strip" aria-hidden="true">{line}</div>'


def theme_sun_icon() -> str:
    return """<svg class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="4.2"></circle>
  <path d="M12 2.8v2.4"></path>
  <path d="M12 18.8v2.4"></path>
  <path d="M2.8 12h2.4"></path>
  <path d="M18.8 12h2.4"></path>
  <path d="m5.5 5.5 1.7 1.7"></path>
  <path d="m16.8 16.8 1.7 1.7"></path>
  <path d="m5.5 18.5 1.7-1.7"></path>
  <path d="m16.8 7.2 1.7-1.7"></path>
</svg>"""


def theme_moon_icon() -> str:
    return """<svg class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <path d="M20.2 14.3A8.7 8.7 0 1 1 9.7 3.8a7.2 7.2 0 0 0 10.5 10.5z"></path>
</svg>"""


ICONS: dict[str, str] = {
    "menu": '<line x1="4" x2="20" y1="7" y2="7"></line><line x1="4" x2="20" y1="12" y2="12"></line><line x1="4" x2="20" y1="17" y2="17"></line>',
    "close": '<path d="M18 6 6 18"></path><path d="m6 6 12 12"></path>',
    "arrow-right": '<path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path>',
    "arrow-up-right": '<path d="M7 7h10v10"></path><path d="M7 17 17 7"></path>',
    "external": '<path d="M15 3h6v6"></path><path d="M10 14 21 3"></path><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M3 5v14a9 3 0 0 0 18 0V5"></path><path d="M3 12a9 3 0 0 0 18 0"></path>',
    "target": '<circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle>',
    "wallet": '<path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"></path><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"></path><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"></path>',
    "bot": '<path d="M12 8V4H8"></path><rect width="16" height="12" x="4" y="8" rx="2"></rect><path d="M2 14h2"></path><path d="M20 14h2"></path><path d="M15 13v2"></path><path d="M9 13v2"></path>',
    "search": '<circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path>',
    "terminal": '<path d="m4 17 6-6-6-6"></path><path d="M12 19h8"></path>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path><path d="m9 12 2 2 4-4"></path>',
    "package-check": '<path d="m16 16 2 2 4-4"></path><path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l1.5-.87"></path><path d="m3.3 7 8.7 5 8.7-5"></path><path d="M12 22V12"></path>',
    "check": '<path d="M20 6 9 17l-5-5"></path>',
    "sparkle": '<path d="m12 3-1.9 4.9L5 9.8l4.9 1.9L12 17l1.9-5.1L19 9.9l-5.1-1.9Z"></path><path d="M5 3v4"></path><path d="M19 17v4"></path><path d="M3 5h4"></path><path d="M17 19h4"></path>',
    "github": '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"></path>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect width="4" height="12" x="2" y="9"></rect><circle cx="4" cy="4" r="2"></circle>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"></rect><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>',
}


def icon(name: str, css_class: str = "icon") -> str:
    body = ICONS[name]
    return (
        f'<svg class="{css_class}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
    )


BLOB_FOOTER_PATH = (
    "M300,44 C398,30 472,120 452,222 C432,324 494,428 410,486 "
    "C326,544 208,522 148,438 C88,354 74,232 138,146 C202,60 202,58 300,44 Z"
)


def svg_blob(path: str, gradient_id: str, css_class: str) -> str:
    return f"""<svg class="{css_class}" viewBox="0 0 640 640" aria-hidden="true">
  <defs>
    <linearGradient id="{gradient_id}" x1="10%" y1="0%" x2="95%" y2="100%">
      <stop offset="0%" stop-color="#1A1440"/>
      <stop offset="55%" stop-color="#2E2B7A"/>
      <stop offset="100%" stop-color="#4F62E3"/>
    </linearGradient>
    <radialGradient id="{gradient_id}-hl" cx="32%" cy="26%" r="45%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <path d="{path}" fill="url(#{gradient_id})"/>
  <path d="{path}" fill="url(#{gradient_id}-hl)" style="mix-blend-mode: screen"/>
</svg>"""


def project_card(language: str, project: dict, detailed: bool = False, compact: bool = False) -> str:
    detail_href = f"{route_prefix(language)}/projects/{project['slug']}/"
    repo_href = repo_url(project["repo"])
    title = html.escape(project["title"])
    category = html.escape(t(language, project["category_en"], project["category_pt"]))
    tagline = html.escape(t(language, project["tagline_en"], project["tagline_pt"]))
    summary = html.escape(t(language, project["summary_en"], project["summary_pt"]))
    stack = "".join(f"<li>{html.escape(item)}</li>" for item in project["stack"][:4])
    class_name = "project-card project-card-detailed" if detailed else "project-card"
    if compact:
        class_name += " project-card-compact"
    tagline_markup = "" if compact else f'<p class="project-tagline">{tagline}</p>'
    stack_markup = "" if compact else f'<ul class="stack-list">{stack}</ul>'
    return f"""<article class="{class_name}" data-reveal>
  <div class="project-card-top">
    <p class="project-category">{category}</p>
    <h3>{title}</h3>
    {tagline_markup}
  </div>
  <p class="project-summary">{summary}</p>
  {stack_markup}
  <div class="project-links">
    <a href="{detail_href}" class="inline-link">{html.escape(t(language, 'View case', 'Ver case'))}{icon('arrow-right', 'icon icon-inline')}</a>
    <a href="{repo_href}" class="inline-link" target="_blank" rel="noreferrer">GitHub{icon('external', 'icon icon-inline')}</a>
  </div>
</article>"""


def status_panel_markup(language: str) -> str:
    guarantees = [
        t(language, "No silent pipeline breaks", "Sem quebra silenciosa de pipeline"),
        t(language, "No rework from duplicate data", "Sem retrabalho por dado duplicado"),
        t(language, "Alerts before the incident, not after", "Alerta antes do incidente, nao depois"),
        t(language, "Handoff without an emergency call", "Handoff sem call de emergencia"),
    ]
    rows = "".join(
        f"""<li>
  <span class="status-job">{html.escape(item)}</span>
  <span class="status-ok">{icon('check', 'icon icon-sm')}</span>
</li>"""
        for item in guarantees
    )
    return f"""<div class="status-card" data-reveal>
  <div class="status-card-head">
    <span class="status-dot" aria-hidden="true"></span>
    <span>{html.escape(t(language, 'What this avoids', 'O que isso evita'))}</span>
  </div>
  <ul class="status-list">{rows}</ul>
</div>"""


def founder_photo_markup(language: str) -> str:
    photo = SITE.get("founder_photo")
    if not photo:
        return ""
    alt = html.escape(t(language, f"Photo of {SITE['founder_name']}", f"Foto de {SITE['founder_name']}"))
    return f'<img src="{html.escape(photo)}" alt="{alt}" class="founder-photo" loading="lazy">'


def hero_markup(language: str) -> str:
    primary_label = t(language, "Book a call", "Agendar uma conversa")
    secondary_label = t(language, "Connect on LinkedIn", "Conectar no LinkedIn")
    status_label = t(language, "Open to new projects", "Disponivel para novos projetos")
    bio = t(language, SITE.get("founder_bio_en"), SITE.get("founder_bio_pt"))
    bio_markup = f'<p class="hero-bio">{html.escape(bio)}</p>' if bio else ""
    photo_markup = founder_photo_markup(language)
    return f"""<section class="hero hero-centered">
  <div class="founder-intro" data-reveal>
    {photo_markup}
    <p class="founder-pill">{html.escape(t(language, SITE['founder_intro_pill_en'], SITE['founder_intro_pill_pt']))}</p>
  </div>
  <h1 class="hero-name" data-reveal style="--typing-chars: {len(SITE['founder_name'])}">{html.escape(SITE['founder_name'])}</h1>
  <p class="hero-role" data-reveal>{html.escape(t(language, SITE['role_en'], SITE['role_pt']))}</p>
  <span class="hero-divider" aria-hidden="true"></span>
  {bio_markup}
  <p class="hero-contact-line" data-reveal>
    <span class="hero-status"><span class="hero-status-dot" aria-hidden="true"></span>{html.escape(status_label)}</span>
    <span class="hero-contact-sep">&middot;</span>
    <a href="{cta_url()}" class="hero-contact-link" target="_blank" rel="noreferrer">{html.escape(primary_label)}</a>
    <span class="hero-contact-sep">&middot;</span>
    <a href="{SITE['linkedin_url']}" class="hero-contact-link" target="_blank" rel="noreferrer">{html.escape(secondary_label)}</a>
  </p>
</section>"""


def proof_strip_markup(language: str) -> str:
    stats = "".join(
        f"""<div class="stat">
  <strong>{html.escape(item['value'])}</strong>
  <span>{html.escape(t(language, item['label_en'], item['label_pt']))}</span>
</div>"""
        for item in SITE["stats"]
    )
    terminal_lines = (
        (
            "$ problem",
            "pipeline breaks silently at 3am",
            "$ what we fix",
            "logs -- retries -- alerts before it's a fire",
            "$ how",
            "python -- dbt -- warehouses -- automation",
        )
        if language == "en"
        else (
            "$ problema",
            "pipeline quebra silencioso as 3h",
            "$ o que a gente resolve",
            "logs -- retries -- alerta antes do incendio",
            "$ como",
            "python -- dbt -- warehouses -- automacao",
        )
    )
    return f"""<section class="section section-proof-strip" id="proof">
  <div class="section-heading">
    <p class="eyebrow">{html.escape(t(language, 'What actually ships', 'O que realmente sai do forno'))}</p>
    <h2>{html.escape(t(language, SITE['headline_en'], SITE['headline_pt']))}</h2>
    <p>{html.escape(t(language, SITE['subheadline_en'], SITE['subheadline_pt']))}</p>
    <p class="hero-location">{html.escape(t(language, SITE['location_en'], SITE['location_pt']))}</p>
  </div>
  <div class="proof-strip-grid">
    {status_panel_markup(language)}
    <div class="terminal-card" data-reveal>
      <div class="terminal-head">
        <span></span><span></span><span></span>
      </div>
      <code>
        <span>{html.escape(terminal_lines[0])}</span>
        <span>{html.escape(terminal_lines[1])}</span>
        <span>{html.escape(terminal_lines[2])}</span>
        <span>{html.escape(terminal_lines[3])}</span>
        <span>{html.escape(terminal_lines[4])}</span>
        <span>{html.escape(terminal_lines[5])}</span>
      </code>
    </div>
  </div>
  <div class="stat-grid">{stats}</div>
</section>"""


def services_markup(language: str) -> str:
    cards = "".join(
        f"""<article class="service-card" data-reveal>
  <span class="service-icon">{icon(item['icon'])}</span>
  <h3>{html.escape(t(language, item['title_en'], item['title_pt']))}</h3>
  <p>{html.escape(t(language, item['body_en'], item['body_pt']))}</p>
</article>"""
        for item in SITE["services"]
    )
    return f"""<section class="section section-services" id="services">
  <div class="section-heading">
    <p class="eyebrow">{html.escape(t(language, 'Areas of work', 'Frentes de atuacao'))}</p>
    <h2>{html.escape(t(language, 'Four problems, one engineer', 'Quatro frentes, um engenheiro'))}</h2>
  </div>
  <div class="service-grid">{cards}</div>
</section>"""


def project_sections_markup(language: str) -> str:
    cards = "".join(project_card(language, project, compact=True) for project in featured_projects())
    proof = "".join(f"<li>{html.escape(item)}</li>" for item in SITE["proof_ribbon"])
    return f"""<section class="section section-projects" id="projects">
  <div class="section-heading">
    <p class="eyebrow">{html.escape(t(language, 'Proof, not claims', 'Prova, nao promessa'))}</p>
    <h2>{html.escape(t(language, 'Selected projects', 'Projetos selecionados'))}</h2>
    <p>{html.escape(t(language, 'Six repositories that show the delivery pattern: clean schemas, replay-safe pipelines, and a handoff another engineer can pick up.', 'Seis repositorios que mostram o padrao de entrega: schemas limpos, pipelines seguros para replay e um handoff que outro engenheiro consegue assumir.'))}</p>
  </div>
  <div class="project-grid">{cards}</div>
  <p class="eyebrow proof-ribbon-caption">{html.escape(t(language, 'Stack behind the projects above', 'Stack por tras dos projetos acima'))}</p>
  <ul class="proof-ribbon">{proof}</ul>
  <div class="section-actions">
    <a href="{route_prefix(language)}/projects/" class="button button-secondary">{html.escape(t(language, 'View all projects', 'Ver todos os projetos'))}{icon('arrow-right', 'icon icon-inline')}</a>
  </div>
</section>"""


def experience_timeline_markup(language: str) -> str:
    if not EXPERIENCE:
        return ""
    rows = "".join(
        f"""<article class="experience-row" data-reveal>
  <span class="experience-step">{html.escape(item.get('step', ''))}</span>
  <div class="experience-row-body">
    <h3>{html.escape(t(language, item['role_en'], item['role_pt']))}</h3>
    <p class="experience-company">{html.escape(item['company'])}</p>
    <p class="experience-period">{html.escape(item['period'])}</p>
    <p>{html.escape(t(language, item.get('summary_en', ''), item.get('summary_pt', '')))}</p>
  </div>
</article>"""
        for item in EXPERIENCE
    )
    return f"""<section class="section section-experience" id="experience">
  <div class="section-heading">
    <p class="eyebrow">{html.escape(t(language, 'Track record', 'Trajetoria'))}</p>
    <h2>{html.escape(t(language, 'Where this came from', 'De onde isso veio'))}</h2>
  </div>
  <div class="experience-timeline">{rows}</div>
</section>"""


def process_markup(language: str) -> str:
    cards = "".join(
        f"""<article class="process-card" data-reveal>
  <div class="process-card-head">
    <span class="process-icon">{icon(item['icon'])}</span>
    <span class="process-step">{item['step']}</span>
  </div>
  <h3>{html.escape(t(language, item['title_en'], item['title_pt']))}</h3>
  <p>{html.escape(t(language, item['body_en'], item['body_pt']))}</p>
</article>"""
        for item in SITE["process"]
    )
    return f"""<section class="section section-process" id="process">
  <div class="section-heading">
    <p class="eyebrow">{html.escape(t(language, 'How an engagement runs', 'Como um projeto acontece'))}</p>
    <h2>{html.escape(t(language, 'From first call to handoff', 'Da primeira call ao handoff'))}</h2>
  </div>
  <div class="process-grid">{cards}</div>
</section>"""


def home_markup(language: str) -> str:
    return f"""<main>
  {hero_markup(language)}
  {proof_strip_markup(language)}
  {services_markup(language)}
  {project_sections_markup(language)}
  {experience_timeline_markup(language)}
  {process_markup(language)}
</main>"""


def project_profile(language: str, project: dict) -> dict[str, list[str] | str]:
    lane = project["lane"]
    profiles = {
        "platform": {
            "posture_en": "Cost-aware warehouse operations",
            "posture_pt": "Operacao de warehouse com foco em custo",
            "buyer_en": [
                "Turns platform work into a visible backlog with cost, runtime, and handoff clarity.",
                "Fits teams that need warehouse performance without creating a larger platform burden.",
                "Keeps dbt and operational telemetry aligned so internal teams can keep iterating.",
            ],
            "buyer_pt": [
                "Transforma trabalho de plataforma em backlog visivel com clareza de custo, runtime e handoff.",
                "Atende times que precisam de performance de warehouse sem criar uma operacao de plataforma maior.",
                "Mantem dbt e telemetria operacional alinhados para o time interno continuar evoluindo.",
            ],
        },
        "finance": {
            "posture_en": "Audit-friendly automation delivery",
            "posture_pt": "Automacao com postura auditavel",
            "buyer_en": [
                "Reduces manual finance work while preserving reconciliation and traceability.",
                "Useful when recurring browser or ERP workflows need operational control, not just scripts.",
                "Keeps downstream accounting, BI, and ops consumers working with validated outputs.",
            ],
            "buyer_pt": [
                "Reduz trabalho manual em financas sem perder conciliacao nem rastreabilidade.",
                "Serve para fluxos recorrentes de portal ou ERP que precisam de controle operacional, nao so scripts.",
                "Mantem accounting, BI e operacao consumindo dados validados no downstream.",
            ],
        },
        "marketing": {
            "posture_en": "Attribution-ready marketing data",
            "posture_pt": "Dados de marketing prontos para atribuicao",
            "buyer_en": [
                "Connects media, analytics, and CRM flows without duplicate syncs or broken attribution.",
                "Works well for growth teams that need reporting and activation from the same delivery path.",
                "Keeps hourly or daily operations visible with retry, dead-letter, and replay-safe behavior.",
            ],
            "buyer_pt": [
                "Conecta midia, analytics e CRM sem sync duplicado nem atribuicao quebrada.",
                "Funciona bem para times de growth que precisam de reporting e ativacao na mesma entrega.",
                "Mantem operacao horaria ou diaria visivel com retry, dead-letter e replay seguro.",
            ],
        },
        "automation": {
            "posture_en": "Controlled AI and signal workflows",
            "posture_pt": "Fluxos de AI e sinais com controle",
            "buyer_en": [
                "Frames AI and signal automation as an operations system, not a demo.",
                "Useful when teams want faster execution but still need logs, contracts, and rollback-safe flows.",
                "Helps connect inbound signals, decisions, and downstream actions in a maintainable way.",
            ],
            "buyer_pt": [
                "Enquadra AI e automacao de sinais como sistema operacional, nao como demo.",
                "Serve quando o time quer acelerar execucao, mas ainda precisa de logs, contratos e rollback seguro.",
                "Ajuda a conectar sinais de entrada, decisoes e acoes de downstream de forma sustentavel.",
            ],
        },
    }
    profile = profiles[lane]
    return {
        "posture": t(language, profile["posture_en"], profile["posture_pt"]),
        "buyer_points": list(t(language, en, pt) for en, pt in zip(profile["buyer_en"], profile["buyer_pt"])),
    }


def project_control_points(language: str, project: dict) -> list[str]:
    items = [
        (
            "Structured logs, validation steps, and predictable run behavior.",
            "Logs estruturados, validacoes e execucao previsivel.",
        ),
        (
            "Replay-safe processing paths designed to reduce duplicate work and broken publishes.",
            "Fluxos seguros para replay, pensados para reduzir duplicidade e publish quebrado.",
        ),
        (
            "Repository structure that another engineer can extend without re-learning the whole system.",
            "Estrutura de repositorio que outro engenheiro consegue evoluir sem reaprender o sistema todo.",
        ),
    ]
    return [t(language, en, pt) for en, pt in items]


def project_detail_markup(language: str, project: dict) -> str:
    repo_href = repo_url(project["repo"])
    lane = project_lane(project)
    profile = project_profile(language, project)
    deliverables = "".join(
        f"<li>{html.escape(t(language, en, pt))}</li>"
        for en, pt in zip(project["deliverables_en"], project["deliverables_pt"])
    )
    stack_items = ''.join(f'<li>{html.escape(item)}</li>' for item in project['stack'])
    headline_stack = ''.join(f'<li>{html.escape(item)}</li>' for item in project['stack'][:4])
    buyer_points = "".join(f"<li>{html.escape(item)}</li>" for item in profile["buyer_points"])
    control_points = "".join(f"<li>{html.escape(item)}</li>" for item in project_control_points(language, project))
    proof_cards = (
        {
            "title": t(language, "Delivery lane", "Frente de entrega"),
            "value": t(language, lane["title_en"], lane["title_pt"]),
            "body": t(language, lane["body_en"], lane["body_pt"]),
        },
        {
            "title": t(language, "Repository scope", "Escopo do repositorio"),
            "value": t(language, f"{len(project['deliverables_en'])} core delivery blocks", f"{len(project['deliverables_pt'])} blocos centrais"),
            "body": t(language, "A compact build with practical deliverables and visible operating behavior.", "Uma entrega compacta com blocos praticos e comportamento operacional visivel."),
        },
        {
            "title": t(language, "Operating posture", "Postura operacional"),
            "value": str(profile["posture"]),
            "body": t(language, "Built with the same logging, retries, and validation you would expect from a workload running in production.", "Construido com os mesmos logs, retries e validacoes que voce esperaria de uma carga real de producao."),
        },
    )
    proof_markup = "".join(
        f"""<article class="detail-proof-card" data-reveal>
  <p class="detail-proof-kicker">{html.escape(item['title'])}</p>
  <strong>{html.escape(item['value'])}</strong>
  <span>{html.escape(item['body'])}</span>
</article>"""
        for item in proof_cards
    )
    related = "".join(
        project_card(language, item, detailed=True) for item in PROJECTS if item["lane"] == project["lane"] and item["slug"] != project["slug"]
    )
    return f"""<main class="detail-page">
  <section class="detail-hero" data-reveal>
    <div>
      <p class="eyebrow">{html.escape(t(language, project['category_en'], project['category_pt']))}</p>
      <h1>{html.escape(project['title'])}</h1>
      <p class="detail-tagline">{html.escape(t(language, project['tagline_en'], project['tagline_pt']))}</p>
      <div class="hero-actions">
        <a href="{repo_href}" class="button button-primary" target="_blank" rel="noreferrer">{icon('external', 'icon icon-inline-lead')}GitHub</a>
        <a href="{SITE['calendly_url']}" class="button button-secondary" target="_blank" rel="noreferrer">{html.escape(t(language, 'Book a call', 'Agendar conversa'))}{icon('arrow-up-right', 'icon icon-inline')}</a>
      </div>
      <ul class="detail-stack-preview">{headline_stack}</ul>
    </div>
    <div class="detail-panel">
      <div class="detail-chip">{html.escape(t(language, 'Problem', 'Problema'))}</div>
      <p>{html.escape(t(language, project['problem_en'], project['problem_pt']))}</p>
      <div class="detail-chip">{html.escape(t(language, 'Solution', 'Solucao'))}</div>
      <p>{html.escape(t(language, project['solution_en'], project['solution_pt']))}</p>
      <div class="detail-chip">{html.escape(t(language, 'Outcome', 'Resultado'))}</div>
      <p>{html.escape(t(language, project['outcome_en'], project['outcome_pt']))}</p>
    </div>
  </section>
  <section class="section detail-proof-grid">
    {proof_markup}
  </section>
  <section class="section detail-content">
    <div class="detail-grid detail-grid-rich">
      <article class="detail-card" data-reveal>
        <h2>{html.escape(t(language, 'What ships in this repository', 'O que entra neste repositorio'))}</h2>
        <ul class="detail-list">{deliverables}</ul>
      </article>
      <article class="detail-card" data-reveal>
        <h2>{html.escape(t(language, 'Stack and operating model', 'Stack e modelo operacional'))}</h2>
        <ul class="stack-list">{stack_items}</ul>
        <p>{html.escape(t(language, project['summary_en'], project['summary_pt']))}</p>
      </article>
      <article class="detail-card detail-card-emphasis" data-reveal>
        <h2>{html.escape(t(language, 'Why buyers pick this type of build', 'Por que esse tipo de entrega vende'))}</h2>
        <ul class="detail-list">{buyer_points}</ul>
      </article>
      <article class="detail-card" data-reveal>
        <h2>{html.escape(t(language, 'How delivery stays reliable', 'Como a entrega fica confiavel'))}</h2>
        <ul class="detail-list">{control_points}</ul>
      </article>
    </div>
  </section>
  <section class="section detail-related">
    <div class="section-heading">
      <p class="eyebrow">{html.escape(t(language, 'More in this delivery lane', 'Mais nesta frente de entrega'))}</p>
      <h2>{html.escape(t(language, 'Related work', 'Trabalhos relacionados'))}</h2>
    </div>
    <div class="project-grid">{related}</div>
  </section>
</main>"""


def projects_index_markup(language: str) -> str:
    cards = "".join(project_card(language, project, detailed=True) for project in PROJECTS)
    return f"""<main class="projects-index">
  <section class="section-heading section-heading-page" data-reveal>
    <p class="eyebrow">{html.escape(t(language, 'Project archive', 'Arquivo de projetos'))}</p>
    <h1>{html.escape(t(language, 'Systems, integrations, and automation builds', 'Sistemas, integracoes e automacoes entregues'))}</h1>
    <p>{html.escape(t(language, 'Each project links to the GitHub repository and a short case page with delivery context.', 'Cada projeto aponta para o repositorio no GitHub e para uma pagina curta com contexto de entrega.'))}</p>
  </section>
  <section class="project-grid project-grid-wide">{cards}</section>
</main>"""


def page_shell(language: str, route: str, body: str, title: str | None = None, description: str | None = None) -> str:
    lang = "en" if language == "en" else "pt-BR"
    body_class = "page-home" if route in {"/", "/pt/"} else "page-inner"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
{head_markup(language, route, title, description)}
<body class="{body_class}">
  <div class="page-background">
    <div class="gradient gradient-a"></div>
    <div class="gradient gradient-b"></div>
    <div class="grid-overlay"></div>
  </div>
  {header_markup(language, route)}
  {body}
  {footer_markup(language)}
</body>
</html>"""


def svg_logo() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-labelledby="title desc">
  <title id="title">B Tecnologia brand mark</title>
  <desc id="desc">A stylized indigo-blue B with a deep navy dot.</desc>
  <rect width="512" height="512" rx="128" fill="none"/>
  <circle cx="150" cy="365" r="40" fill="{SITE['palette']['secondary']}"/>
  <text x="165" y="350" font-size="300" font-weight="700" font-family="Space Grotesk, Arial, sans-serif" fill="{SITE['palette']['primary']}">B</text>
</svg>"""


def svg_og_card() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0a10"/>
      <stop offset="100%" stop-color="{SITE['palette']['secondary']}"/>
    </linearGradient>
    <radialGradient id="glow" cx="70%" cy="20%" r="80%">
      <stop offset="0%" stop-color="{SITE['palette']['primary']}" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="{SITE['palette']['primary']}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect width="1200" height="630" fill="url(#glow)"/>
  <circle cx="222" cy="434" r="42" fill="{SITE['palette']['secondary']}"/>
  <text x="240" y="390" font-size="330" font-weight="700" font-family="Space Grotesk, Arial, sans-serif" fill="{SITE['palette']['primary']}">B</text>
  <text x="520" y="220" font-size="34" fill="#f4efff" font-family="IBM Plex Mono, monospace">Data Engineering + AI Systems</text>
  <text x="520" y="320" font-size="72" font-weight="700" fill="#ffffff" font-family="Space Grotesk, Arial, sans-serif">B Tecnologia</text>
  <text x="520" y="390" font-size="34" fill="#ded8f4" font-family="IBM Plex Sans, sans-serif">Production-ready pipelines, integrations, and automation systems.</text>
</svg>"""



def site_css() -> str:
    return """
:root {
  color-scheme: dark;

  /* surfaces */
  --bg: #0a0a10;
  --card: rgba(255, 255, 255, 0.045);
  --card-strong: rgba(255, 255, 255, 0.075);
  --border: rgba(255, 255, 255, 0.11);
  --border-strong: rgba(255, 255, 255, 0.2);

  /* text */
  --text: #f3f3f6;
  --text-soft: rgba(243, 243, 246, 0.74);
  --text-muted: rgba(243, 243, 246, 0.52);

  /* accent: single, disciplined use only */
  --accent: #4f62e3;
  --accent-strong: #7b8af0;
  --accent-soft: rgba(79, 98, 227, 0.14);
  --accent-border: rgba(79, 98, 227, 0.35);
  --on-accent: #ffffff;
  --positive: #35d488;

  --shadow: 0 20px 48px rgba(0, 0, 0, 0.35);
  --shadow-sm: 0 8px 22px rgba(0, 0, 0, 0.24);

  /* radius */
  --radius-sm: 12px;
  --radius-md: 18px;
  --radius-lg: 24px;
  --radius-full: 999px;

  /* spacing scale */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-20: 5rem;
  --space-24: 6rem;

  /* type scale */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-md: 1.0625rem;
  --text-lg: 1.25rem;
  --text-xl: 1.5rem;
  --text-2xl: 1.875rem;
  --text-3xl: clamp(2rem, 3.4vw, 2.5rem);
  --text-4xl: clamp(2.5rem, 4.2vw, 3.25rem);
  --text-5xl: clamp(2.75rem, 5.6vw, 4.25rem);
  --text-hero: clamp(3.5rem, 9vw, 7.5rem);

  --content: 1160px;
  --theme-color: #0a0a10;
  --header-surface: rgba(10, 10, 16, 0.78);
  --grid-line: rgba(255, 255, 255, 0.035);
  --terminal-code: #b9c3ff;
  --focus-ring: rgba(79, 98, 227, 0.55);
  --button-secondary-bg: rgba(255, 255, 255, 0.07);
  --button-ghost-color: rgba(243, 243, 246, 0.78);
  --theme-switch-bg: rgba(255, 255, 255, 0.06);
  --theme-switch-thumb: rgba(255, 255, 255, 0.16);
  --theme-switch-text: rgba(243, 243, 246, 0.64);
}

html[data-theme="light"] {
  color-scheme: light;
  --bg: #ffffff;
  --card: rgba(15, 15, 20, 0.025);
  --card-strong: rgba(15, 15, 20, 0.045);
  --border: rgba(15, 15, 20, 0.11);
  --border-strong: rgba(15, 15, 20, 0.2);
  --text: #111116;
  --text-soft: rgba(17, 17, 22, 0.72);
  --text-muted: rgba(17, 17, 22, 0.5);
  --accent: #3548c9;
  --accent-strong: #4f62e3;
  --accent-soft: rgba(53, 72, 201, 0.08);
  --accent-border: rgba(53, 72, 201, 0.25);
  --on-accent: #ffffff;
  --positive: #16a35f;
  --shadow: 0 20px 48px rgba(15, 23, 42, 0.08);
  --shadow-sm: 0 8px 22px rgba(15, 23, 42, 0.06);
  --theme-color: #ffffff;
  --header-surface: rgba(255, 255, 255, 0.86);
  --grid-line: rgba(15, 15, 20, 0.045);
  --terminal-code: #2c3aa0;
  --focus-ring: rgba(53, 72, 201, 0.45);
  --button-secondary-bg: rgba(15, 15, 20, 0.04);
  --button-ghost-color: #3548c9;
  --theme-switch-bg: rgba(15, 15, 20, 0.04);
  --theme-switch-thumb: rgba(15, 15, 20, 0.09);
  --theme-switch-text: rgba(17, 17, 22, 0.58);
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: "IBM Plex Sans", sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}

a {
  color: inherit;
  text-decoration: none;
}

img {
  max-width: 100%;
  display: block;
}

:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 3px;
  border-radius: 6px;
}

.icon {
  width: 1.05em;
  height: 1.05em;
  flex-shrink: 0;
}

.icon-inline {
  width: 0.95em;
  height: 0.95em;
  margin-left: 0.4em;
}

.icon-inline-lead {
  width: 0.95em;
  height: 0.95em;
  margin-right: 0.4em;
}

.icon-sm {
  width: 0.9em;
  height: 0.9em;
  margin-right: 0.35em;
}

.page-background {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: -1;
}

.gradient {
  position: absolute;
  border-radius: 999px;
  filter: blur(90px);
  opacity: 0.5;
}

.gradient-a {
  width: 34rem;
  height: 34rem;
  top: -12rem;
  right: -10rem;
  background: radial-gradient(circle, var(--accent-soft), rgba(79, 98, 227, 0));
}

.gradient-b {
  width: 26rem;
  height: 26rem;
  left: -10rem;
  top: 30rem;
  background: radial-gradient(circle, var(--border), transparent);
  opacity: 0.3;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(var(--grid-line) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), transparent 88%);
}

.site-header,
main,
.site-footer {
  width: min(calc(100% - 2rem), var(--content));
  margin: 0 auto;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  margin-top: 1rem;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
  background: var(--header-surface);
  border: 1px solid var(--border);
  backdrop-filter: blur(16px);
  border-radius: var(--radius-full);
}

.header-start {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  justify-self: start;
}

.header-cta {
  gap: 0.5rem;
}

.header-cta-dot {
  width: 0.4rem;
  height: 0.4rem;
  border-radius: 999px;
  background: var(--on-accent);
  opacity: 0.8;
}

.header-socials {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.header-social-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.2rem;
  height: 2.2rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  color: var(--text-soft);
  transition: border-color 160ms ease, color 160ms ease;
}

.header-social-icon:hover {
  border-color: var(--border-strong);
  color: var(--text);
}

.header-social-icon .icon {
  width: 1rem;
  height: 1rem;
}

.header-end {
  display: flex;
  align-items: center;
  justify-self: end;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  border-radius: var(--radius-full);
  justify-self: center;
}

.brand-mark {
  width: 2.6rem;
  height: 2.6rem;
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
}

.brand-text strong {
  font-family: "Space Grotesk", sans-serif;
  font-size: var(--text-sm);
  font-weight: 600;
}

.brand-text span {
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.site-nav {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.nav-link,
.lang-switch,
.theme-switch {
  color: var(--text-soft);
  font-size: var(--text-sm);
}

.nav-link {
  padding: 0.3rem 0.1rem;
  display: inline-block;
  transition: color 160ms ease, letter-spacing 200ms ease;
}

.nav-link:hover {
  letter-spacing: 0.03em;
}

.nav-link:hover,
.lang-switch:hover,
.theme-switch:hover,
.inline-link:hover,
.footer-links a:hover {
  color: var(--text);
}

.button-compact {
  min-height: 2.4rem;
  padding: 0 1rem;
  font-size: var(--text-xs);
}

.lang-switch {
  display: inline-flex;
  gap: 0.4rem;
  align-items: center;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  transition: border-color 160ms ease, color 160ms ease;
}

.lang-switch:hover {
  border-color: var(--border-strong);
}

.header-clock {
  font-family: "IBM Plex Mono", monospace;
  font-size: var(--text-xs);
  color: var(--text-muted);
  letter-spacing: 0.02em;
}

.theme-switch {
  position: relative;
  display: inline-grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: center;
  width: 5rem;
  padding: 0.22rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  background: var(--theme-switch-bg);
  cursor: pointer;
  overflow: hidden;
}

.theme-switch::after {
  content: "";
  position: absolute;
  top: 0.22rem;
  left: 0.22rem;
  width: calc(50% - 0.22rem);
  height: calc(100% - 0.44rem);
  border-radius: var(--radius-full);
  background: var(--theme-switch-thumb);
  transition: transform 180ms ease;
}

html[data-theme="light"] .theme-switch::after {
  transform: translateX(100%);
}

.theme-option {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.32rem 0.2rem;
  color: var(--theme-switch-text);
}

html[data-theme="dark"] .theme-option-dark,
html[data-theme="light"] .theme-option-light {
  color: var(--text);
}

.theme-icon {
  width: 1rem;
  height: 1rem;
}

.lang-current {
  color: var(--text);
}

.menu-toggle {
  display: none;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border);
  background: transparent;
  border-radius: var(--radius-full);
  padding: 0;
  width: 2.6rem;
  height: 2.6rem;
  color: var(--text);
  transition: border-color 160ms ease;
}

.menu-toggle-icon {
  width: 1.2rem;
  height: 1.2rem;
  display: none;
}

.menu-toggle-open {
  display: block;
}

.site-header[data-open="true"] .menu-toggle-open {
  display: none;
}

.site-header[data-open="true"] .menu-toggle-close {
  display: block;
}

.hero,
.section,
.section-heading-page,
.site-footer,
.detail-hero {
  position: relative;
  z-index: 1;
}

.hero,
.site-footer {
  overflow: hidden;
}

.hero-centered {
  padding: var(--space-24) 0 var(--space-16);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 46rem;
  margin: 0 auto;
}

.footer-blob {
  position: absolute;
  pointer-events: none;
  bottom: -8rem;
  left: -9rem;
  width: 26rem;
  height: 26rem;
  filter: blur(4px);
  opacity: 0.45;
}

html[data-theme="light"] .footer-blob {
  opacity: 0.14;
}

.halftone {
  position: absolute;
  width: 20rem;
  height: 20rem;
  background-image: radial-gradient(circle, var(--accent) 1.4px, transparent 1.6px);
  background-size: 15px 15px;
  opacity: 0.3;
  pointer-events: none;
}

.footer-halftone {
  top: -3rem;
  right: -3rem;
  -webkit-mask-image: radial-gradient(circle at 100% 0%, rgba(0, 0, 0, 0.9), transparent 70%);
  mask-image: radial-gradient(circle at 100% 0%, rgba(0, 0, 0, 0.9), transparent 70%);
}

html[data-theme="light"] .halftone {
  opacity: 0.16;
}

.eyebrow {
  margin: 0 0 var(--space-4);
  font-family: "IBM Plex Mono", monospace;
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--accent);
}

.founder-intro {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin: 0 0 var(--space-3);
}

.founder-photo {
  width: 2.4rem;
  height: 2.4rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-strong);
  object-fit: cover;
}

.founder-pill {
  display: inline-flex;
  align-items: center;
  padding: 0.4rem 0.85rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--border);
  background: var(--card);
  font-size: var(--text-xs);
  color: var(--text-soft);
}

@keyframes hero-name-typing {
  from {
    width: 0;
  }
  to {
    width: calc(var(--typing-chars) * 1ch);
  }
}

@keyframes hero-name-caret {
  0%, 100% {
    border-color: transparent;
  }
  50% {
    border-color: var(--accent);
  }
}

.hero-name {
  display: inline-block;
  margin: 0 0 var(--space-2);
  font-size: var(--text-hero);
  line-height: 1;
  max-width: none;
  overflow: hidden;
  white-space: nowrap;
  vertical-align: bottom;
  border-right: 0.05em solid transparent;
  width: calc(var(--typing-chars) * 1ch);
  animation:
    hero-name-typing 1.6s steps(var(--typing-chars), end) 0.3s both,
    hero-name-caret 0.85s step-end infinite;
}

.hero-role {
  margin: 0;
  font-family: "IBM Plex Mono", monospace;
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
}

.hero-divider {
  width: 1px;
  height: 2.5rem;
  margin: var(--space-6) 0;
  background: var(--border-strong);
}

.hero-bio {
  max-width: 46ch;
  margin: 0 0 var(--space-6);
  font-size: var(--text-lg);
  color: var(--text);
}

.hero-contact-line {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  font-family: "IBM Plex Mono", monospace;
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
}

.hero-status {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
}

.hero-status-dot {
  width: 0.4rem;
  height: 0.4rem;
  border-radius: 999px;
  background: var(--positive);
}

.hero-contact-sep {
  color: var(--border-strong);
}

.hero-contact-link {
  color: var(--accent);
  transition: color 160ms ease;
}

.hero-contact-link:hover {
  color: var(--accent-strong);
}

h1,
h2 {
  margin: 0 0 var(--space-4);
  font-family: "Fraunces", serif;
  letter-spacing: -0.01em;
  font-weight: 600;
}

h3 {
  margin: 0 0 var(--space-4);
  font-family: "Space Grotesk", sans-serif;
  letter-spacing: -0.02em;
  font-weight: 700;
}

h1 {
  font-size: var(--text-5xl);
  line-height: 1;
  max-width: 12ch;
}

h2 {
  font-size: var(--text-4xl);
  line-height: 1.05;
}

h3 {
  font-size: var(--text-lg);
  font-weight: 600;
}

.hero-text,
.section-heading p,
.service-card p,
.project-summary,
.project-tagline,
.detail-panel p,
.detail-card p,
.footer-copy {
  color: var(--text-soft);
  font-size: var(--text-md);
  line-height: 1.65;
}

.hero-location,
.footer-next-step,
.micro-note {
  color: var(--text-muted);
  font-size: var(--text-sm);
  margin-top: var(--space-3);
}

.hero-actions,
.project-links,
.footer-actions,
.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}

.hero-actions {
  margin-top: var(--space-6);
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 3rem;
  padding: 0 1.3rem;
  border-radius: var(--radius-full);
  border: 1px solid transparent;
  font-weight: 600;
  font-size: var(--text-sm);
  cursor: pointer;
  transition: transform 160ms ease, border-color 160ms ease, background-color 160ms ease, box-shadow 160ms ease, color 160ms ease;
}

.button:active {
  transform: translateY(0) scale(0.98);
}

.button-primary {
  background: linear-gradient(135deg, var(--accent-strong), var(--accent));
  color: var(--on-accent);
  box-shadow: 0 10px 26px rgba(79, 98, 227, 0.28);
}

.button-primary:hover {
  background: var(--accent-strong);
  box-shadow: 0 12px 32px rgba(79, 98, 227, 0.38);
  transform: translateY(-1px);
}

.button-secondary {
  background: var(--button-secondary-bg);
  border-color: var(--border);
  color: var(--text);
}

.button-secondary:hover {
  border-color: var(--border-strong);
  background: var(--card-strong);
  transform: translateY(-1px);
}

.button-ghost {
  border-color: var(--border);
  color: var(--button-ghost-color);
}

.button-ghost:hover {
  border-color: var(--accent-border);
  color: var(--accent);
}

.proof-ribbon-caption {
  margin-top: var(--space-12);
}

.proof-ribbon {
  list-style: none;
  margin: var(--space-6) 0 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
}

.proof-ribbon li,
.stack-list li,
.detail-chip,
.project-category {
  display: inline-flex;
  align-items: center;
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.proof-strip-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
  margin-top: var(--space-8);
}

.terminal-card,
.status-card,
.detail-panel,
.service-card,
.process-card,
.project-card,
.detail-card,
.experience-row {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.service-card,
.process-card,
.project-card {
  transition: border-color 200ms ease, transform 200ms ease, background-color 200ms ease;
}

.service-card:hover {
  border-color: var(--accent-border);
  transform: translateY(-3px);
}

.service-card:hover .service-icon {
  background: linear-gradient(135deg, var(--accent-strong), var(--accent));
  color: var(--on-accent);
}

.process-card:hover {
  border-color: var(--border-strong);
  transform: translateY(-3px);
}

.project-card:hover {
  border-color: var(--border-strong);
  background: var(--card-strong);
  transform: translateY(-3px);
}

.status-card {
  padding: var(--space-5) var(--space-6);
}

.status-card-head {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: var(--space-4);
  font-size: var(--text-sm);
  color: var(--text-soft);
}

.status-dot {
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 999px;
  background: var(--positive);
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--positive) 18%, transparent);
}

.status-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: var(--space-3);
}

.status-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--border);
  font-family: "IBM Plex Mono", monospace;
  font-size: var(--text-xs);
}

.status-list li:first-child {
  padding-top: 0;
  border-top: 0;
}

.status-job {
  color: var(--text-soft);
}

.status-ok {
  display: inline-flex;
  align-items: center;
  color: var(--positive);
}

.terminal-card {
  padding: var(--space-5) var(--space-6);
}

.terminal-head {
  display: flex;
  gap: 0.45rem;
  margin-bottom: var(--space-4);
}

.terminal-head span {
  width: 0.7rem;
  height: 0.7rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
}

.terminal-head span:first-child {
  background: #ff4c96;
}

.terminal-head span:nth-child(2) {
  background: #ffd166;
}

.terminal-head span:last-child {
  background: #73f3a1;
}

.terminal-card code {
  display: grid;
  gap: 0.55rem;
  font-family: "IBM Plex Mono", monospace;
  font-size: var(--text-sm);
  color: var(--terminal-code);
  white-space: pre-wrap;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
  margin-top: var(--space-6);
}

.stat {
  padding: var(--space-5);
  border-radius: var(--radius-md);
  background: var(--card);
  border: 1px solid var(--border);
  transition: border-color 200ms ease;
}

.stat:hover {
  border-color: var(--border-strong);
}

.stat strong {
  display: block;
  font-family: "Space Grotesk", sans-serif;
  font-size: var(--text-2xl);
  margin-bottom: 0.35rem;
}

.stat span {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.section {
  padding: var(--space-24) 0 0;
}

.section-heading,
.section-heading-page {
  max-width: 42rem;
  margin-bottom: var(--space-10);
}

.section-actions {
  display: flex;
  justify-content: center;
  margin-top: var(--space-6);
}

.service-grid,
.process-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.service-card,
.process-card,
.detail-card {
  padding: var(--space-6);
}

.service-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.6rem;
  height: 2.6rem;
  margin-bottom: var(--space-5);
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, var(--accent-soft), rgba(79, 98, 227, 0.24));
  color: var(--accent);
  transition: background 200ms ease, color 200ms ease;
}

html[data-theme="light"] .service-icon {
  background: linear-gradient(135deg, var(--accent-soft), rgba(53, 72, 201, 0.18));
}

.service-icon .icon {
  width: 1.2rem;
  height: 1.2rem;
}

.process-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-5);
}

.process-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.6rem;
  height: 2.6rem;
  border-radius: var(--radius-sm);
  background: var(--card-strong);
  color: var(--text-soft);
}

.process-icon .icon {
  width: 1.2rem;
  height: 1.2rem;
}

.process-step {
  font-family: "Space Grotesk", sans-serif;
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--accent);
  opacity: 0.55;
}

.experience-timeline {
  display: grid;
  gap: var(--space-4);
}

.experience-row {
  display: grid;
  grid-template-columns: 3.5rem 1fr;
  gap: var(--space-5);
  padding: var(--space-6);
}

.experience-step {
  font-family: "Space Grotesk", sans-serif;
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--accent);
  opacity: 0.55;
}

.experience-row-body h3 {
  margin-bottom: var(--space-1);
}

.experience-company {
  color: var(--text);
  font-weight: 600;
}

.experience-period {
  font-family: "IBM Plex Mono", monospace;
  font-size: var(--text-xs);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.project-grid,
.project-grid-wide {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.project-card {
  padding: var(--space-6);
  min-height: 100%;
}

.project-card-detailed {
  background: var(--card-strong);
}

.project-card-compact .project-card-top {
  margin-bottom: 0.7rem;
}

.project-card-compact .project-summary {
  margin-bottom: 0;
}

.project-card-top {
  margin-bottom: var(--space-4);
}

.project-category {
  margin-bottom: var(--space-4);
  color: var(--accent);
  background: var(--accent-soft);
  border-color: var(--accent-border);
}

.project-tagline {
  margin-bottom: 0;
}

.project-summary {
  margin: 0 0 var(--space-4);
}

.stack-list,
.detail-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
}

.detail-list {
  display: grid;
  gap: var(--space-3);
}

.detail-list li {
  position: relative;
  padding-left: 1.3rem;
  color: var(--text-soft);
}

.detail-list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.62rem;
  width: 0.4rem;
  height: 0.4rem;
  border-radius: 999px;
  background: var(--accent);
}

.project-links {
  margin-top: var(--space-5);
}

.inline-link {
  display: inline-flex;
  align-items: center;
  font-weight: 600;
  font-size: var(--text-sm);
  color: var(--text);
  transition: color 160ms ease;
}

.inline-link .icon-inline {
  transition: transform 160ms ease;
}

.inline-link:hover .icon-inline {
  transform: translate(2px, -2px);
}

.detail-page,
.projects-index {
  padding-top: var(--space-10);
}

.detail-hero {
  padding: var(--space-12) 0 0;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: var(--space-4);
  align-items: stretch;
}

.detail-tagline {
  max-width: 44rem;
  color: var(--text-soft);
  font-size: var(--text-md);
}

.detail-stack-preview {
  list-style: none;
  padding: 0;
  margin: var(--space-5) 0 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.detail-stack-preview li {
  padding: 0.45rem 0.75rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text-soft);
  font-size: var(--text-xs);
}

.detail-panel {
  padding: var(--space-6);
}

.detail-chip {
  margin-bottom: var(--space-3);
}

.detail-proof-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-4);
}

.detail-proof-card {
  padding: var(--space-5);
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--card);
  box-shadow: var(--shadow-sm);
}

.detail-proof-kicker {
  margin: 0 0 var(--space-3);
  font-family: "IBM Plex Mono", monospace;
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.detail-proof-card strong {
  display: block;
  font-family: "Space Grotesk", sans-serif;
  font-size: var(--text-lg);
  line-height: 1.2;
  margin-bottom: 0.45rem;
}

.detail-proof-card span {
  color: var(--text-soft);
  font-size: var(--text-sm);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.detail-grid-rich {
  align-items: stretch;
}

.detail-card h2 {
  margin-bottom: var(--space-4);
  font-size: var(--text-xl);
}

.detail-card-emphasis {
  background: var(--accent-soft);
  border-color: var(--accent-border);
}

.site-footer {
  margin-top: var(--space-24);
  padding: var(--space-8) 0 var(--space-12);
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: var(--space-6);
  padding: var(--space-8);
  border-radius: var(--radius-lg);
  background: var(--card);
  border: 1px solid var(--border);
  align-items: center;
}

.footer-meta {
  display: flex;
  justify-content: space-between;
  gap: var(--space-4);
  align-items: center;
  padding-top: var(--space-5);
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.ascii-strip {
  margin-top: var(--space-8);
  height: 3.2rem;
  overflow: hidden;
  font-family: "IBM Plex Mono", monospace;
  font-size: var(--text-xs);
  line-height: 1.3;
  letter-spacing: 0.05em;
  word-break: break-all;
  color: var(--border-strong);
  opacity: 0.6;
}

[data-reveal] {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 600ms ease, transform 600ms ease;
}

[data-reveal].is-visible {
  opacity: 1;
  transform: translateY(0);
}

.service-grid [data-reveal]:nth-child(2),
.process-grid [data-reveal]:nth-child(2),
.project-grid [data-reveal]:nth-child(2),
.project-grid-wide [data-reveal]:nth-child(2),
.detail-proof-grid [data-reveal]:nth-child(2) {
  transition-delay: 70ms;
}

.service-grid [data-reveal]:nth-child(3),
.process-grid [data-reveal]:nth-child(3),
.project-grid [data-reveal]:nth-child(3),
.project-grid-wide [data-reveal]:nth-child(3),
.detail-proof-grid [data-reveal]:nth-child(3) {
  transition-delay: 140ms;
}

.service-grid [data-reveal]:nth-child(4),
.process-grid [data-reveal]:nth-child(4),
.project-grid [data-reveal]:nth-child(4),
.project-grid-wide [data-reveal]:nth-child(4) {
  transition-delay: 210ms;
}

@media (max-width: 980px) {
  .detail-hero,
  .footer-grid,
  .detail-proof-grid,
  .detail-grid,
  .service-grid,
  .process-grid,
  .project-grid,
  .project-grid-wide,
  .proof-strip-grid {
    grid-template-columns: 1fr;
  }

  .lane-heading,
  .footer-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .site-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    border-radius: 28px;
    align-items: center;
  }

  .header-socials {
    display: none;
  }

  .header-end {
    display: contents;
  }

  .menu-toggle {
    display: block;
  }

  .site-nav {
    display: none;
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    padding-top: 0.5rem;
  }

  .theme-switch {
    width: 100%;
    max-width: 8rem;
  }

  .site-header[data-open="true"] .site-nav {
    display: flex;
  }

}

@media (max-width: 640px) {
  .site-header,
  main,
  .site-footer {
    width: min(calc(100% - 1.2rem), var(--content));
  }

  h1 {
    font-size: clamp(2.1rem, 10vw, 3.1rem);
  }

  .brand-text span {
    display: none;
  }

  .hero-name {
    display: block;
    width: auto;
    max-width: 100%;
    white-space: normal;
    overflow: visible;
    border-right: none;
    animation: none;
  }

}

@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }

  [data-reveal] {
    opacity: 1;
    transform: none;
    transition: none;
  }

  .button,
  .nav-link,
  .lang-switch,
  .theme-switch,
  .theme-switch::after {
    transition: none;
  }

  .hero-name {
    animation: none;
  }
}
""".strip()


def site_js() -> str:
    return """
const themeKey = "b-tech-theme-v2";
const root = document.documentElement;
const themeToggle = document.querySelector("[data-theme-toggle]");
const themeMeta = document.querySelector("#theme-color-meta");

const applyTheme = (theme) => {
  const nextTheme = theme === "light" ? "light" : "dark";
  root.setAttribute("data-theme", nextTheme);
  if (themeMeta) {
    themeMeta.setAttribute("content", nextTheme === "light" ? "#ffffff" : "#12173A");
  }
  if (themeToggle) {
    const nextLabel = nextTheme === "light"
      ? themeToggle.getAttribute("data-label-dark")
      : themeToggle.getAttribute("data-label-light");
    themeToggle.setAttribute("aria-label", nextLabel || "Toggle theme");
  }
  try {
    window.localStorage.setItem(themeKey, nextTheme);
  } catch (error) {
    // Ignore storage errors and keep the current session theme.
  }
};

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    const nextTheme = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    applyTheme(nextTheme);
  });
  applyTheme(root.getAttribute("data-theme") || "light");
}

const header = document.querySelector(".site-header");
const toggle = document.querySelector(".menu-toggle");

if (header && toggle) {
  toggle.addEventListener("click", () => {
    const next = header.getAttribute("data-open") === "true" ? "false" : "true";
    header.setAttribute("data-open", next);
  });
}

const clockEl = document.querySelector("[data-clock]");

if (clockEl) {
  const updateClock = () => {
    clockEl.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };
  updateClock();
  setInterval(updateClock, 15000);
}

const revealItems = document.querySelectorAll("[data-reveal]");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

""".strip()


def render_home_page(language: str, route: str) -> str:
    return page_shell(language, route, home_markup(language))


def render_project_page(language: str, project: dict) -> str:
    route = f"{route_prefix(language)}/projects/{project['slug']}/"
    description = t(language, project["summary_en"], project["summary_pt"])
    return page_shell(language, route, project_detail_markup(language, project), project["title"], description)


def render_projects_index(language: str) -> str:
    route = f"{route_prefix(language)}/projects/"
    return page_shell(
        language,
        route,
        projects_index_markup(language),
        t(language, "Project Archive", "Arquivo de Projetos"),
        t(
            language,
            "Data engineering, analytics, and automation systems delivered by B Tecnologia.",
            "Sistemas de engenharia de dados, analytics e automacao entregues pela B Tecnologia.",
        ),
    )


def render_404() -> str:
    body = f"""<main class="detail-page">
  <section class="detail-hero">
    <div>
      <p class="eyebrow">404</p>
      <h1>Page not found</h1>
      <p class="detail-tagline">The route you asked for does not exist. Use the links below to get back to the site.</p>
      <div class="hero-actions">
        <a href="/" class="button button-primary">Go home</a>
        <a href="/projects/" class="button button-secondary">View projects</a>
      </div>
    </div>
    <div class="detail-panel">
      <div class="detail-chip">Next step</div>
      <p>If you arrived here from a message or proposal, the homepage and project archive contain the current B Tecnologia links.</p>
    </div>
  </section>
</main>"""
    return page_shell("en", "/404.html", body, "Page not found")


def sitemap() -> str:
    routes = ["/", "/projects/", "/pt/", "/pt/projects/"]
    for project in PROJECTS:
        routes.append(f"/projects/{project['slug']}/")
        routes.append(f"/pt/projects/{project['slug']}/")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for route in routes:
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE['site_url']}{route}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)


def robots_txt() -> str:
    return f"User-agent: *\nAllow: /\nSitemap: {SITE['site_url']}/sitemap.xml\n"


def webmanifest() -> str:
    return """{
  "name": "B Tecnologia",
  "short_name": "BTech",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0a0a10",
  "theme_color": "#12173A",
  "icons": [
    {
      "src": "/assets/favicon.svg",
      "sizes": "any",
      "type": "image/svg+xml"
    }
  ]
}"""


def build_pages() -> None:
    clean_dist()

    write_text(DIST / "index.html", render_home_page("en", "/"))
    write_text(DIST / "pt" / "index.html", render_home_page("pt", "/pt/"))
    write_text(DIST / "projects" / "index.html", render_projects_index("en"))
    write_text(DIST / "pt" / "projects" / "index.html", render_projects_index("pt"))

    for project in PROJECTS:
        write_text(DIST / "projects" / project["slug"] / "index.html", render_project_page("en", project))
        write_text(DIST / "pt" / "projects" / project["slug"] / "index.html", render_project_page("pt", project))

    write_text(DIST / "404.html", render_404())
    write_text(DIST / "robots.txt", robots_txt())
    write_text(DIST / "sitemap.xml", sitemap())
    write_text(DIST / "site.webmanifest", webmanifest())
    write_text(DIST / ".nojekyll", "")
    write_text(DIST / "assets" / "styles.css", site_css())
    write_text(DIST / "assets" / "app.js", site_js())
    write_text(DIST / "assets" / "brand-mark.svg", svg_logo())
    write_text(DIST / "assets" / "favicon.svg", svg_logo())
    write_text(DIST / "assets" / "og-card.svg", svg_og_card())


if __name__ == "__main__":
    build_pages()
