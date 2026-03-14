from __future__ import annotations

import html
import shutil
from pathlib import Path
from urllib.parse import quote

try:
    from .content import LANES, PROJECTS, SITE
except ImportError:
    from content import LANES, PROJECTS, SITE


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def clean_dist() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)


def repo_url(repo: str) -> str:
    return f"https://github.com/brunoluizmendes/{repo}"


def mailto_url(subject: str) -> str:
    return f"mailto:{SITE['email']}?subject={quote(subject)}"


def cta_url() -> str:
    return SITE["calendly_url"] or mailto_url("Upwork portfolio inquiry")


def t(language: str, en: str, pt: str) -> str:
    return en if language == "en" else pt


def lane_by_key() -> dict[str, dict]:
    return {lane["key"]: lane for lane in LANES}


def grouped_projects() -> list[tuple[dict, list[dict]]]:
    mapping = lane_by_key()
    return [(lane, [project for project in PROJECTS if project["lane"] == lane["key"]]) for lane in LANES]


def route_prefix(language: str) -> str:
    return "" if language == "en" else "/pt"


def language_href(language: str, route: str) -> str:
    if language == "en":
        return f"/pt{route}" if route != "/" else "/pt/"
    return route[3:] if route.startswith("/pt") else "/"


def page_title(language: str, custom_title: str | None = None) -> str:
    base = "Bruno Luiz Mendes"
    if custom_title:
        return f"{custom_title} | {base}"
    return f"{base} | {t(language, SITE['role_en'], SITE['role_pt'])}"


def page_description(language: str, custom_description: str | None = None) -> str:
    return custom_description or t(language, SITE["subheadline_en"], SITE["subheadline_pt"])


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
  <meta name="theme-color" content="{SITE['palette']['secondary']}">
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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/styles.css">
  <script defer src="/assets/app.js"></script>
</head>"""


def header_markup(language: str, route: str) -> str:
    home = route_prefix(language) or "/"
    if home == "":
        home = "/"
    nav_items = [
        (f"{home}#services", t(language, "Services", "Servicos")),
        (f"{home}#projects", t(language, "Projects", "Projetos")),
        (f"{home}#process", t(language, "Process", "Processo")),
        (f"{home}#contact", t(language, "Contact", "Contato")),
    ]
    nav = "".join(
        f'<a href="{href}" class="nav-link">{html.escape(label)}</a>' for href, label in nav_items
    )
    switch_to = language_href(language, route)
    switch_label = "PT" if language == "en" else "EN"
    current_label = "EN" if language == "en" else "PT"
    return f"""<header class="site-header" data-open="false">
  <a class="brand" href="{home}">
    <img src="/assets/brand-mark.svg" alt="{html.escape(SITE['logo_alt'])}" class="brand-mark">
    <span class="brand-text">
      <strong>{html.escape(SITE['name'])}</strong>
      <span>{html.escape(t(language, SITE['role_en'], SITE['role_pt']))}</span>
    </span>
  </a>
  <button class="menu-toggle" type="button" aria-label="{html.escape(t(language, 'Toggle navigation', 'Abrir navegacao'))}">
    <span></span><span></span><span></span>
  </button>
  <nav class="site-nav">
    {nav}
    <a href="{SITE['upwork_url']}" class="nav-link nav-link-cta" target="_blank" rel="noreferrer">Upwork</a>
    <a href="{switch_to}" class="lang-switch" hreflang="{switch_label.lower()}">
      <span class="lang-current">{current_label}</span>
      <span class="lang-next">{switch_label}</span>
    </a>
  </nav>
</header>"""


def footer_markup(language: str) -> str:
    book_label = t(language, "Book intro call", "Agendar conversa")
    book_url = cta_url()
    note = t(
        language,
        "Calendly will be plugged in here. For now, this button falls back to email.",
        "O Calendly vai entrar aqui depois. Por enquanto, este botao cai para email.",
    )
    return f"""<footer class="site-footer" id="contact">
  <div class="footer-grid">
    <div>
      <p class="eyebrow">{html.escape(t(language, 'Available for', 'Disponivel para'))}</p>
      <h2>{html.escape(t(language, 'Data Engineering + AI Automation', 'Data Engineering + AI Automation'))}</h2>
      <p class="footer-copy">{html.escape(t(language, SITE['about_en'], SITE['about_pt']))}</p>
    </div>
    <div class="footer-actions">
      <a href="{book_url}" class="button button-primary">{html.escape(book_label)}</a>
      <a href="{SITE['upwork_url']}" class="button button-secondary" target="_blank" rel="noreferrer">Upwork</a>
      <a href="mailto:{SITE['email']}" class="button button-ghost">{SITE['email']}</a>
      <p class="footer-note">{html.escape(note)}</p>
    </div>
  </div>
  <div class="footer-meta">
    <div class="footer-links">
      <a href="{SITE['github_url']}" target="_blank" rel="noreferrer">GitHub</a>
      <a href="{SITE['linkedin_url']}" target="_blank" rel="noreferrer">LinkedIn</a>
      <a href="{SITE['upwork_url']}" target="_blank" rel="noreferrer">Upwork</a>
    </div>
    <p>© 2026 Bruno Luiz Mendes</p>
  </div>
</footer>"""


def project_card(language: str, project: dict, detailed: bool = False) -> str:
    detail_href = f"{route_prefix(language)}/projects/{project['slug']}/"
    repo_href = repo_url(project["repo"])
    title = html.escape(project["title"])
    category = html.escape(t(language, project["category_en"], project["category_pt"]))
    tagline = html.escape(t(language, project["tagline_en"], project["tagline_pt"]))
    summary = html.escape(t(language, project["summary_en"], project["summary_pt"]))
    stack = "".join(f"<li>{html.escape(item)}</li>" for item in project["stack"][:4])
    class_name = "project-card project-card-detailed" if detailed else "project-card"
    return f"""<article class="{class_name}" data-reveal>
  <div class="project-card-top">
    <p class="project-category">{category}</p>
    <h3>{title}</h3>
    <p class="project-tagline">{tagline}</p>
  </div>
  <p class="project-summary">{summary}</p>
  <ul class="stack-list">{stack}</ul>
  <div class="project-links">
    <a href="{detail_href}" class="inline-link">{html.escape(t(language, 'View case', 'Ver case'))}</a>
    <a href="{repo_href}" class="inline-link" target="_blank" rel="noreferrer">GitHub</a>
  </div>
</article>"""


def hero_markup(language: str) -> str:
    actions = []
    primary_label = t(language, "Book intro call", "Agendar conversa")
    secondary_label = t(language, "Hire me on Upwork", "Me contratar no Upwork")
    tertiary_label = t(language, "LinkedIn", "LinkedIn")
    actions.append(f'<a href="{cta_url()}" class="button button-primary">{html.escape(primary_label)}</a>')
    actions.append(
        f'<a href="{SITE["upwork_url"]}" class="button button-secondary" target="_blank" rel="noreferrer">{html.escape(secondary_label)}</a>'
    )
    actions.append(
        f'<a href="{SITE["linkedin_url"]}" class="button button-ghost" target="_blank" rel="noreferrer">{html.escape(tertiary_label)}</a>'
    )
    proof = "".join(f"<span>{html.escape(item)}</span>" for item in SITE["proof_ribbon"])
    stats = "".join(
        f"""<div class="stat">
  <strong>{html.escape(item['value'])}</strong>
  <span>{html.escape(t(language, item['label_en'], item['label_pt']))}</span>
</div>"""
        for item in SITE["stats"]
    )
    callout = t(
        language,
        "Calendly button is reserved in the layout. Until the link is live, it falls back to email.",
        "O botao de Calendly ja esta previsto no layout. Ate o link entrar, ele cai para email.",
    )
    return f"""<section class="hero">
  <div class="hero-copy" data-reveal>
    <p class="eyebrow">{html.escape(t(language, SITE['role_en'], SITE['role_pt']))}</p>
    <h1>{html.escape(t(language, SITE['headline_en'], SITE['headline_pt']))}</h1>
    <p class="hero-text">{html.escape(t(language, SITE['subheadline_en'], SITE['subheadline_pt']))}</p>
    <p class="hero-location">{html.escape(t(language, SITE['location_en'], SITE['location_pt']))}</p>
    <div class="hero-actions">{''.join(actions)}</div>
    <p class="micro-note">{html.escape(callout)}</p>
    <div class="proof-ribbon">{proof}</div>
  </div>
  <div class="hero-visual" data-reveal>
    <div class="brand-stage">
      <div class="brand-orb orb-primary"></div>
      <div class="brand-orb orb-secondary"></div>
      <div class="brand-panel">
        <img src="/assets/brand-mark.svg" alt="{html.escape(SITE['logo_alt'])}" class="hero-logo">
      </div>
    </div>
    <div class="terminal-card">
      <div class="terminal-head">
        <span></span><span></span><span></span>
      </div>
      <code>
        <span>$ pipeline stack</span>
        <span>python -- dbt -- observability -- automation</span>
        <span>$ buyer fit</span>
        <span>lean teams that need senior execution</span>
      </code>
    </div>
  </div>
  <div class="hero-stats">{stats}</div>
</section>"""


def services_markup(language: str) -> str:
    cards = "".join(
        f"""<article class="service-card" data-reveal>
  <p class="service-number">{item['eyebrow']}</p>
  <h3>{html.escape(t(language, item['title_en'], item['title_pt']))}</h3>
  <p>{html.escape(t(language, item['body_en'], item['body_pt']))}</p>
</article>"""
        for item in SITE["services"]
    )
    return f"""<section class="section section-services" id="services">
  <div class="section-heading">
    <p class="eyebrow">{html.escape(t(language, 'What I build', 'O que eu construo'))}</p>
    <h2>{html.escape(t(language, 'Freelance delivery focused on systems that keep working', 'Entrega freelancer focada em sistemas que continuam funcionando'))}</h2>
  </div>
  <div class="service-grid">{cards}</div>
</section>"""


def project_sections_markup(language: str) -> str:
    sections = []
    for lane, projects in grouped_projects():
        cards = "".join(project_card(language, project) for project in projects)
        sections.append(
            f"""<section class="lane-block" data-reveal>
  <div class="lane-heading">
    <p class="eyebrow">{html.escape(t(language, lane['title_en'], lane['title_pt']))}</p>
    <p>{html.escape(t(language, lane['body_en'], lane['body_pt']))}</p>
  </div>
  <div class="project-grid">{cards}</div>
</section>"""
        )
    return f"""<section class="section section-projects" id="projects">
  <div class="section-heading">
    <p class="eyebrow">{html.escape(t(language, 'Portfolio built for buyer confidence', 'Portfolio feito para gerar confianca no comprador'))}</p>
    <h2>{html.escape(t(language, '11 public projects that show how I actually ship', '11 projetos publicos que mostram como eu realmente entrego'))}</h2>
    <p>{html.escape(t(language, 'Every project below links to the GitHub repo and a short case page with context.', 'Cada projeto abaixo aponta para o repositorio no GitHub e para uma pagina curta com contexto.'))}</p>
  </div>
  {''.join(sections)}
</section>"""


def process_markup(language: str) -> str:
    cards = "".join(
        f"""<article class="process-card" data-reveal>
  <h3>{html.escape(t(language, item['title_en'], item['title_pt']))}</h3>
  <p>{html.escape(t(language, item['body_en'], item['body_pt']))}</p>
</article>"""
        for item in SITE["process"]
    )
    return f"""<section class="section section-process" id="process">
  <div class="section-heading">
    <p class="eyebrow">{html.escape(t(language, 'How I work', 'Como eu trabalho'))}</p>
    <h2>{html.escape(t(language, 'Senior-style execution without platform-team ceremony', 'Execucao de senior sem cerimonia de time de plataforma'))}</h2>
    <p>{html.escape(t(language, SITE['about_en'], SITE['about_pt']))}</p>
  </div>
  <div class="process-grid">{cards}</div>
</section>"""


def home_markup(language: str) -> str:
    intro_title = t(language, "Data systems that sell reliability", "Sistemas de dados que vendem confiabilidade")
    intro_body = t(
        language,
        "This landing is designed for Upwork buyers who need technical confidence quickly: clear offer, real code, and visible proof of execution.",
        "Esta landing foi feita para compradores do Upwork que precisam de confianca tecnica rapido: oferta clara, codigo real e prova visivel de execucao.",
    )
    return f"""<main>
  <section class="intro-strip" data-reveal>
    <p class="eyebrow">Bruno Luiz Mendes</p>
    <div>
      <h2>{html.escape(intro_title)}</h2>
      <p>{html.escape(intro_body)}</p>
    </div>
  </section>
  {hero_markup(language)}
  {services_markup(language)}
  {project_sections_markup(language)}
  {process_markup(language)}
</main>"""


def project_detail_markup(language: str, project: dict) -> str:
    repo_href = repo_url(project["repo"])
    deliverables = "".join(
        f"<li>{html.escape(t(language, en, pt))}</li>"
        for en, pt in zip(project["deliverables_en"], project["deliverables_pt"])
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
        <a href="{repo_href}" class="button button-primary" target="_blank" rel="noreferrer">GitHub</a>
        <a href="{SITE['upwork_url']}" class="button button-secondary" target="_blank" rel="noreferrer">Upwork</a>
        <a href="mailto:{SITE['email']}" class="button button-ghost">{SITE['email']}</a>
      </div>
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
  <section class="section detail-content">
    <div class="detail-grid">
      <article class="detail-card" data-reveal>
        <h2>{html.escape(t(language, 'What ships in this repository', 'O que entra neste repositorio'))}</h2>
        <ul class="detail-list">{deliverables}</ul>
      </article>
      <article class="detail-card" data-reveal>
        <h2>{html.escape(t(language, 'Stack and operating model', 'Stack e modelo operacional'))}</h2>
        <ul class="stack-list">{''.join(f'<li>{html.escape(item)}</li>' for item in project['stack'])}</ul>
        <p>{html.escape(t(language, project['summary_en'], project['summary_pt']))}</p>
      </article>
    </div>
  </section>
  <section class="section detail-related">
    <div class="section-heading">
      <p class="eyebrow">{html.escape(t(language, 'More in this delivery lane', 'Mais nesta frente de entrega'))}</p>
      <h2>{html.escape(t(language, 'Related portfolio work', 'Trabalhos relacionados do portfolio'))}</h2>
    </div>
    <div class="project-grid">{related}</div>
  </section>
</main>"""


def projects_index_markup(language: str) -> str:
    cards = "".join(project_card(language, project, detailed=True) for project in PROJECTS)
    return f"""<main class="projects-index">
  <section class="section-heading section-heading-page" data-reveal>
    <p class="eyebrow">{html.escape(t(language, 'Project archive', 'Arquivo de projetos'))}</p>
    <h1>{html.escape(t(language, 'All public portfolio repositories', 'Todos os repositorios publicos do portfolio'))}</h1>
    <p>{html.escape(t(language, 'Every card links to the GitHub repo and a short case page that explains buyer fit and delivery shape.', 'Cada card aponta para o GitHub e para uma pagina curta que explica encaixe comercial e formato de entrega.'))}</p>
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
  <title id="title">Bruno Luiz Mendes brand mark</title>
  <desc id="desc">A stylized magenta B with an indigo dot.</desc>
  <rect width="512" height="512" rx="128" fill="none"/>
  <circle cx="150" cy="365" r="40" fill="{SITE['palette']['secondary']}"/>
  <text x="165" y="350" font-size="300" font-weight="700" font-family="Space Grotesk, Arial, sans-serif" fill="{SITE['palette']['primary']}">B</text>
</svg>"""


def svg_og_card() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#09051d"/>
      <stop offset="100%" stop-color="#1D057D"/>
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
  <text x="520" y="220" font-size="34" fill="#f4efff" font-family="IBM Plex Mono, monospace">Data + AI Automation Freelancer</text>
  <text x="520" y="320" font-size="72" font-weight="700" fill="#ffffff" font-family="Space Grotesk, Arial, sans-serif">Bruno Luiz Mendes</text>
  <text x="520" y="390" font-size="34" fill="#ded8f4" font-family="IBM Plex Sans, sans-serif">Production-style pipelines, integrations, observability, and automation.</text>
</svg>"""


def site_css() -> str:
    return """
:root {
  --bg: #09051d;
  --bg-elevated: #120b33;
  --bg-soft: rgba(231, 231, 231, 0.08);
  --card: rgba(19, 12, 51, 0.78);
  --card-strong: rgba(25, 16, 61, 0.94);
  --text: #f5efff;
  --text-soft: rgba(245, 239, 255, 0.76);
  --text-muted: rgba(245, 239, 255, 0.58);
  --line: rgba(231, 231, 231, 0.12);
  --primary: #fe017f;
  --primary-soft: rgba(254, 1, 127, 0.18);
  --secondary: #1d057d;
  --neutral: #c3c2c3;
  --shadow: 0 24px 64px rgba(0, 0, 0, 0.32);
  --radius: 28px;
  --radius-sm: 18px;
  --content: 1160px;
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
}

a {
  color: inherit;
  text-decoration: none;
}

img {
  max-width: 100%;
  display: block;
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
  filter: blur(60px);
  opacity: 0.55;
}

.gradient-a {
  width: 36rem;
  height: 36rem;
  top: -10rem;
  right: -8rem;
  background: radial-gradient(circle, rgba(254, 1, 127, 0.9), rgba(254, 1, 127, 0));
}

.gradient-b {
  width: 28rem;
  height: 28rem;
  left: -8rem;
  top: 24rem;
  background: radial-gradient(circle, rgba(29, 5, 125, 1), rgba(29, 5, 125, 0));
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.045) 1px, transparent 1px);
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: rgba(9, 5, 29, 0.72);
  border: 1px solid var(--line);
  backdrop-filter: blur(16px);
  border-radius: 999px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.brand-mark {
  width: 3rem;
  height: 3rem;
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.brand-text strong {
  font-family: "Space Grotesk", sans-serif;
  font-size: 0.98rem;
}

.brand-text span {
  color: var(--text-muted);
  font-size: 0.84rem;
}

.site-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link,
.lang-switch {
  color: var(--text-soft);
  font-size: 0.92rem;
}

.nav-link:hover,
.lang-switch:hover,
.inline-link:hover,
.footer-links a:hover {
  color: var(--text);
}

.nav-link-cta {
  color: var(--primary);
}

.lang-switch {
  display: inline-flex;
  gap: 0.45rem;
  align-items: center;
  padding: 0.55rem 0.75rem;
  border: 1px solid var(--line);
  border-radius: 999px;
}

.lang-current {
  color: var(--text);
}

.menu-toggle {
  display: none;
  border: 0;
  background: transparent;
  padding: 0;
  width: 2.5rem;
  height: 2.5rem;
}

.menu-toggle span {
  display: block;
  width: 1.5rem;
  height: 2px;
  margin: 0.28rem auto;
  background: var(--text);
}

.intro-strip,
.hero,
.section,
.section-heading-page,
.site-footer,
.detail-hero {
  position: relative;
  z-index: 1;
}

.intro-strip {
  margin-top: 2rem;
  padding: 1rem 1.5rem;
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: 1.5rem;
  align-items: center;
}

.intro-strip p {
  margin: 0;
  color: var(--text-soft);
}

.hero {
  padding: 2rem 0 1rem;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 2rem;
  align-items: start;
}

.hero-copy {
  padding-top: 2rem;
}

.eyebrow {
  margin: 0 0 1rem;
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.84rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--primary);
}

h1,
h2,
h3 {
  margin: 0 0 1rem;
  font-family: "Space Grotesk", sans-serif;
  letter-spacing: -0.03em;
}

h1 {
  font-size: clamp(3rem, 6vw, 6rem);
  line-height: 0.95;
  max-width: 10ch;
}

h2 {
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1;
}

h3 {
  font-size: 1.4rem;
}

.hero-text,
.section-heading p,
.service-card p,
.project-summary,
.project-tagline,
.detail-panel p,
.detail-card p,
.footer-copy,
.footer-note {
  color: var(--text-soft);
  line-height: 1.7;
}

.hero-location,
.micro-note {
  color: var(--text-muted);
  margin-top: 0.85rem;
}

.hero-actions,
.project-links,
.footer-actions,
.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
}

.hero-actions {
  margin-top: 1.5rem;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 3rem;
  padding: 0 1.2rem;
  border-radius: 999px;
  border: 1px solid transparent;
  font-weight: 600;
  transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
}

.button:hover {
  transform: translateY(-1px);
}

.button-primary {
  background: linear-gradient(135deg, var(--primary), #ff3b98);
  color: #fff;
  box-shadow: 0 12px 32px rgba(254, 1, 127, 0.32);
}

.button-secondary {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.14);
}

.button-ghost {
  border-color: var(--line);
  color: var(--text-soft);
}

.proof-ribbon {
  margin-top: 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.proof-ribbon span,
.stack-list li,
.detail-chip,
.project-category {
  display: inline-flex;
  align-items: center;
  padding: 0.45rem 0.78rem;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-soft);
  font-size: 0.82rem;
}

.hero-visual {
  display: grid;
  gap: 1rem;
}

.brand-stage {
  position: relative;
  min-height: 26rem;
  border-radius: var(--radius);
  padding: 2rem;
  background:
    radial-gradient(circle at 28% 25%, rgba(254, 1, 127, 0.22), transparent 46%),
    radial-gradient(circle at 72% 76%, rgba(29, 5, 125, 0.35), transparent 40%),
    rgba(255, 255, 255, 0.05);
  border: 1px solid var(--line);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.brand-orb {
  position: absolute;
  border-radius: 999px;
  filter: blur(6px);
}

.orb-primary {
  width: 12rem;
  height: 12rem;
  top: -2rem;
  right: -1rem;
  background: rgba(254, 1, 127, 0.48);
}

.orb-secondary {
  width: 10rem;
  height: 10rem;
  bottom: -2rem;
  left: -1rem;
  background: rgba(29, 5, 125, 0.82);
}

.brand-panel {
  position: absolute;
  inset: 3rem;
  display: grid;
  place-items: center;
  border-radius: calc(var(--radius) - 8px);
  background: linear-gradient(135deg, rgba(231, 231, 231, 0.14), rgba(231, 231, 231, 0.04));
  border: 1px solid rgba(231, 231, 231, 0.16);
}

.hero-logo {
  width: min(20rem, 72%);
  filter: drop-shadow(0 30px 60px rgba(0, 0, 0, 0.28));
}

.terminal-card,
.detail-panel,
.service-card,
.process-card,
.project-card,
.detail-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.terminal-card {
  padding: 1rem 1.2rem 1.35rem;
}

.terminal-head {
  display: flex;
  gap: 0.45rem;
  margin-bottom: 1rem;
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
  gap: 0.6rem;
  font-family: "IBM Plex Mono", monospace;
  color: #ffcaeb;
  white-space: pre-wrap;
}

.hero-stats {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.stat {
  padding: 1.2rem 1.4rem;
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--line);
}

.stat strong {
  display: block;
  font-family: "Space Grotesk", sans-serif;
  font-size: 1.55rem;
  margin-bottom: 0.4rem;
}

.section {
  padding: 5.5rem 0 0;
}

.section-heading,
.section-heading-page {
  max-width: 48rem;
  margin-bottom: 2rem;
}

.service-grid,
.process-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.service-card,
.process-card,
.detail-card {
  padding: 1.4rem;
}

.service-number {
  margin: 0 0 1.25rem;
  font-family: "IBM Plex Mono", monospace;
  color: var(--text-muted);
}

.lane-block + .lane-block {
  margin-top: 2.2rem;
}

.lane-heading {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
  align-items: flex-end;
  margin-bottom: 1rem;
}

.lane-heading p:last-child {
  margin: 0;
  max-width: 34rem;
  color: var(--text-soft);
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.project-grid-wide {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.project-card {
  padding: 1.35rem;
  min-height: 100%;
}

.project-card-detailed {
  background: var(--card-strong);
}

.project-card-top {
  margin-bottom: 1rem;
}

.project-category {
  margin-bottom: 1rem;
  color: var(--primary);
  background: var(--primary-soft);
  border-color: rgba(254, 1, 127, 0.22);
}

.project-tagline {
  margin-bottom: 0;
}

.project-summary {
  margin: 0 0 1rem;
}

.stack-list,
.detail-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.detail-list {
  display: grid;
  gap: 0.8rem;
}

.detail-list li {
  position: relative;
  padding-left: 1.2rem;
  color: var(--text-soft);
}

.detail-list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.72rem;
  width: 0.42rem;
  height: 0.42rem;
  border-radius: 999px;
  background: var(--primary);
}

.project-links {
  margin-top: 1.2rem;
}

.inline-link {
  font-weight: 600;
  color: var(--text);
}

.detail-page,
.projects-index {
  padding-top: 2.5rem;
}

.detail-hero {
  padding: 3rem 0 0;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 1rem;
  align-items: stretch;
}

.detail-tagline {
  max-width: 44rem;
  color: var(--text-soft);
}

.detail-panel {
  padding: 1.4rem;
}

.detail-chip {
  margin-bottom: 0.8rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.site-footer {
  margin-top: 6rem;
  padding: 2rem 0 3rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 1rem;
  padding: 1.6rem;
  border-radius: var(--radius);
  background: linear-gradient(135deg, rgba(29, 5, 125, 0.58), rgba(19, 12, 51, 0.94));
  border: 1px solid var(--line);
}

.footer-meta {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
  padding-top: 1rem;
  color: var(--text-muted);
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

@media (max-width: 980px) {
  .hero,
  .detail-hero,
  .footer-grid,
  .detail-grid,
  .intro-strip,
  .service-grid,
  .process-grid,
  .project-grid,
  .project-grid-wide {
    grid-template-columns: 1fr;
  }

  .hero-stats {
    grid-template-columns: 1fr;
  }

  .lane-heading,
  .footer-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .site-header {
    border-radius: 28px;
    align-items: flex-start;
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
    font-size: clamp(2.6rem, 12vw, 4rem);
  }

  .brand-text span {
    display: none;
  }

  .brand-stage {
    min-height: 20rem;
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
  .lang-switch {
    transition: none;
  }
}
""".strip()


def site_js() -> str:
    return """
const header = document.querySelector(".site-header");
const toggle = document.querySelector(".menu-toggle");

if (header && toggle) {
  toggle.addEventListener("click", () => {
    const next = header.getAttribute("data-open") === "true" ? "false" : "true";
    header.setAttribute("data-open", next);
  });
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
            "All public data engineering and automation portfolio repositories by Bruno Luiz Mendes.",
            "Todos os repositorios publicos de engenharia de dados e automacao de Bruno Luiz Mendes.",
        ),
    )


def render_404() -> str:
    body = f"""<main class="detail-page">
  <section class="detail-hero">
    <div>
      <p class="eyebrow">404</p>
      <h1>Page not found</h1>
      <p class="detail-tagline">The route you asked for does not exist. Use the links below to get back to the portfolio.</p>
      <div class="hero-actions">
        <a href="/" class="button button-primary">Go home</a>
        <a href="/projects/" class="button button-secondary">View projects</a>
      </div>
    </div>
    <div class="detail-panel">
      <div class="detail-chip">Next step</div>
      <p>If you arrived here from a message or proposal, the homepage and project archive contain the current public portfolio links.</p>
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
  "name": "Bruno Luiz Mendes",
  "short_name": "Bruno",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#09051d",
  "theme_color": "#1D057D",
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
