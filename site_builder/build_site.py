from __future__ import annotations

import html
import shutil
from pathlib import Path
try:
    from .content import LANES, PROJECTS, SITE
except ImportError:
    from content import LANES, PROJECTS, SITE


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
  const key = "b-tech-theme";
  let theme = "dark";
  try {
    const stored = window.localStorage.getItem(key);
    if (stored === "light" || stored === "dark") {
      theme = stored;
    }
  } catch (error) {
    theme = "dark";
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
    theme_dark = t(language, "Dark", "Dark")
    theme_light = t(language, "Light", "Light")
    theme_to_light = t(language, "Switch to light mode", "Mudar para modo claro")
    theme_to_dark = t(language, "Switch to dark mode", "Mudar para modo escuro")
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
    <button
      class="theme-switch"
      type="button"
      data-theme-toggle
      data-label-dark="{html.escape(theme_to_dark)}"
      data-label-light="{html.escape(theme_to_light)}"
      aria-label="{html.escape(theme_to_light)}"
    >
      <span class="theme-option theme-option-dark">{html.escape(theme_dark)}</span>
      <span class="theme-option theme-option-light">{html.escape(theme_light)}</span>
    </button>
    <a href="{switch_to}" class="lang-switch" hreflang="{switch_label.lower()}">
      <span class="lang-current">{current_label}</span>
      <span class="lang-next">{switch_label}</span>
    </a>
  </nav>
</header>"""


def footer_markup(language: str) -> str:
    primary_label = t(language, "Start on Upwork", "Comecar no Upwork")
    secondary_label = t(language, "Connect on LinkedIn", "Conectar no LinkedIn")
    return f"""<footer class="site-footer" id="contact">
  <div class="footer-grid">
    <div>
      <p class="eyebrow">{html.escape(SITE['name'])}</p>
      <h2>{html.escape(t(language, SITE['role_en'], SITE['role_pt']))}</h2>
      <p class="footer-copy">{html.escape(t(language, SITE['about_en'], SITE['about_pt']))}</p>
    </div>
    <div class="footer-actions">
      <a href="{SITE['upwork_url']}" class="button button-primary" target="_blank" rel="noreferrer">{html.escape(primary_label)}</a>
      <a href="{SITE['linkedin_url']}" class="button button-secondary" target="_blank" rel="noreferrer">{html.escape(secondary_label)}</a>
    </div>
  </div>
  <div class="footer-meta">
    <div class="footer-links">
      <a href="{SITE['linkedin_url']}" target="_blank" rel="noreferrer">LinkedIn</a>
      <a href="{SITE['upwork_url']}" target="_blank" rel="noreferrer">Upwork</a>
    </div>
    <p>© 2026 {html.escape(SITE['name'])}</p>
  </div>
</footer>"""


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
    <a href="{detail_href}" class="inline-link">{html.escape(t(language, 'View case', 'Ver case'))}</a>
    <a href="{repo_href}" class="inline-link" target="_blank" rel="noreferrer">GitHub</a>
  </div>
</article>"""


def hero_carousel_markup(language: str) -> str:
    slides = [
        {
            "image": "/assets/slide-lakehouse.svg",
            "alt_en": "Warehouse and dbt architecture visual",
            "alt_pt": "Visual de arquitetura de warehouse e dbt",
            "title_en": "Warehouse + dbt delivery",
            "title_pt": "Entrega de warehouse + dbt",
            "text_en": "Layered models, cost-aware design, orchestration, and clean handoff.",
            "text_pt": "Modelagem em camadas, custo controlado, orquestracao e handoff limpo.",
        },
        {
            "image": "/assets/slide-observability.svg",
            "alt_en": "Monitoring and operational observability visual",
            "alt_pt": "Visual de monitoramento e observabilidade operacional",
            "title_en": "Monitoring that operators can use",
            "title_pt": "Monitoramento que a operacao usa",
            "text_en": "Run logs, event logs, retries, dead-letter flows, and replay-safe pipelines.",
            "text_pt": "Run logs, event logs, retries, dead-letter e pipelines seguros para replay.",
        },
        {
            "image": "/assets/slide-revenue-automation.svg",
            "alt_en": "Marketing and CRM automation visual",
            "alt_pt": "Visual de automacao de marketing e CRM",
            "title_en": "Revenue and CRM automation",
            "title_pt": "Automacao de receita e CRM",
            "text_en": "Attribution, lead routing, CRM syncs, and AI-assisted workflow automation.",
            "text_pt": "Atribuicao, roteamento de leads, sync com CRM e automacao com AI.",
        },
    ]
    cards = []
    dots = []
    for index, slide in enumerate(slides):
        active = " is-active" if index == 0 else ""
        cards.append(
            f"""<article class="carousel-slide{active}" data-carousel-slide>
  <img src="{slide['image']}" alt="{html.escape(t(language, slide['alt_en'], slide['alt_pt']))}" class="carousel-image">
  <div class="carousel-caption">
    <strong>{html.escape(t(language, slide['title_en'], slide['title_pt']))}</strong>
    <span>{html.escape(t(language, slide['text_en'], slide['text_pt']))}</span>
  </div>
</article>"""
        )
        dots.append(
            f'<button class="carousel-dot{active}" type="button" aria-label="{html.escape(t(language, slide["title_en"], slide["title_pt"]))}" data-carousel-dot="{index}"></button>'
        )
    return f"""<div class="brand-stage" data-carousel>
  <div class="brand-orb orb-primary"></div>
  <div class="brand-orb orb-secondary"></div>
  <div class="brand-chip">
    <img src="/assets/brand-mark.svg" alt="{html.escape(SITE['logo_alt'])}" class="brand-chip-logo">
    <span>{html.escape(SITE['name'])}</span>
  </div>
  <div class="carousel-shell">
    {''.join(cards)}
  </div>
  <div class="carousel-controls">{''.join(dots)}</div>
</div>"""


def hero_markup(language: str) -> str:
    actions = []
    primary_label = t(language, "Start on Upwork", "Comecar no Upwork")
    secondary_label = t(language, "Connect on LinkedIn", "Conectar no LinkedIn")
    actions.append(
        f'<a href="{cta_url()}" class="button button-primary" target="_blank" rel="noreferrer">{html.escape(primary_label)}</a>'
    )
    actions.append(
        f'<a href="{SITE["linkedin_url"]}" class="button button-secondary" target="_blank" rel="noreferrer">{html.escape(secondary_label)}</a>'
    )
    proof = "".join(f"<span>{html.escape(item)}</span>" for item in SITE["proof_ribbon"])
    stats = "".join(
        f"""<div class="stat">
  <strong>{html.escape(item['value'])}</strong>
  <span>{html.escape(t(language, item['label_en'], item['label_pt']))}</span>
</div>"""
        for item in SITE["stats"]
    )
    terminal_lines = (
        (
            "$ pipeline stack",
            "python -- dbt -- warehouses -- automation",
            "$ controls",
            "logs -- monitoring -- retries -- dead-letter",
            "$ buyer value",
            "clean delivery -- lower ops risk -- faster handoff",
        )
        if language == "en"
        else (
            "$ pipeline stack",
            "python -- dbt -- warehouses -- automacao",
            "$ controles",
            "logs -- monitoramento -- retries -- dead-letter",
            "$ valor",
            "entrega limpa -- menos risco operacional -- handoff rapido",
        )
    )
    return f"""<section class="hero">
  <div class="hero-copy" data-reveal>
    <p class="eyebrow">{html.escape(t(language, SITE['role_en'], SITE['role_pt']))}</p>
    <h1>{html.escape(t(language, SITE['headline_en'], SITE['headline_pt']))}</h1>
    <p class="hero-text">{html.escape(t(language, SITE['subheadline_en'], SITE['subheadline_pt']))}</p>
    <p class="hero-location">{html.escape(t(language, SITE['location_en'], SITE['location_pt']))}</p>
    <div class="hero-actions">{''.join(actions)}</div>
    <div class="proof-ribbon">{proof}</div>
  </div>
  <div class="hero-visual" data-reveal>
    {hero_carousel_markup(language)}
    <div class="terminal-card">
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
    <p class="eyebrow">{html.escape(t(language, 'What B Tecnologia builds', 'O que a B Tecnologia entrega'))}</p>
    <h2>{html.escape(t(language, 'Systems built to stay in production', 'Sistemas feitos para ficar em producao'))}</h2>
  </div>
  <div class="service-grid">{cards}</div>
</section>"""


def project_sections_markup(language: str) -> str:
    cards = "".join(project_card(language, project, compact=True) for project in featured_projects())
    return f"""<section class="section section-projects" id="projects">
  <div class="section-heading">
    <p class="eyebrow">{html.escape(t(language, 'Selected work', 'Cases selecionados'))}</p>
    <h2>{html.escape(t(language, 'Selected Projects', 'Projetos selecionados'))}</h2>
    <p>{html.escape(t(language, 'A compact sample of systems built for data platforms, finance ops, marketing integrations, and automation workflows.', 'Uma selecao compacta de sistemas entregues para plataforma de dados, operacao financeira, integracoes de marketing e automacao.'))}</p>
  </div>
  <div class="project-grid">{cards}</div>
  <div class="section-actions">
    <a href="{route_prefix(language)}/projects/" class="button button-secondary">{html.escape(t(language, 'View all projects', 'Ver todos os projetos'))}</a>
  </div>
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
    <p class="eyebrow">{html.escape(t(language, 'How we work', 'Como trabalhamos'))}</p>
    <h2>{html.escape(t(language, 'Senior execution, clean delivery', 'Execucao senior, entrega limpa'))}</h2>
    <p>{html.escape(t(language, SITE['about_en'], SITE['about_pt']))}</p>
  </div>
  <div class="process-grid">{cards}</div>
</section>"""


def home_markup(language: str) -> str:
    return f"""<main>
  {hero_markup(language)}
  {services_markup(language)}
  {project_sections_markup(language)}
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
            "body": t(language, "Designed to look real in production, not just present well in a portfolio.", "Pensado para parecer uma entrega real de producao, nao apenas um portfolio bonito."),
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
        <a href="{repo_href}" class="button button-primary" target="_blank" rel="noreferrer">GitHub</a>
        <a href="{SITE['upwork_url']}" class="button button-secondary" target="_blank" rel="noreferrer">Upwork</a>
        <a href="{SITE['linkedin_url']}" class="button button-ghost" target="_blank" rel="noreferrer">LinkedIn</a>
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
      <h2>{html.escape(t(language, 'Related portfolio work', 'Trabalhos relacionados do portfolio'))}</h2>
    </div>
    <div class="project-grid">{related}</div>
  </section>
</main>"""


def projects_index_markup(language: str) -> str:
    cards = "".join(project_card(language, project, detailed=True) for project in PROJECTS)
    return f"""<main class="projects-index">
  <section class="section-heading section-heading-page" data-reveal>
    <p class="eyebrow">{html.escape(t(language, 'Project portfolio', 'Portfolio de projetos'))}</p>
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
  <text x="520" y="220" font-size="34" fill="#f4efff" font-family="IBM Plex Mono, monospace">Data Engineering + AI Systems</text>
  <text x="520" y="320" font-size="72" font-weight="700" fill="#ffffff" font-family="Space Grotesk, Arial, sans-serif">B Tecnologia</text>
  <text x="520" y="390" font-size="34" fill="#ded8f4" font-family="IBM Plex Sans, sans-serif">Production-ready pipelines, integrations, and automation systems.</text>
</svg>"""


def svg_slide_lakehouse() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#130c33"/>
      <stop offset="100%" stop-color="#23105a"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="760" rx="40" fill="url(#bg)"/>
  <rect x="70" y="72" width="1060" height="96" rx="24" fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.10)"/>
  <rect x="96" y="104" width="210" height="20" rx="10" fill="#FE017F"/>
  <rect x="96" y="138" width="330" height="12" rx="6" fill="rgba(255,255,255,0.22)"/>
  <rect x="70" y="220" width="320" height="430" rx="28" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.10)"/>
  <rect x="438" y="220" width="320" height="430" rx="28" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.10)"/>
  <rect x="806" y="220" width="324" height="430" rx="28" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.10)"/>
  <text x="108" y="274" fill="#FFFFFF" font-size="28" font-family="IBM Plex Sans, Arial, sans-serif">raw</text>
  <text x="476" y="274" fill="#FFFFFF" font-size="28" font-family="IBM Plex Sans, Arial, sans-serif">stage</text>
  <text x="844" y="274" fill="#FFFFFF" font-size="28" font-family="IBM Plex Sans, Arial, sans-serif">analytics</text>
  <rect x="108" y="312" width="244" height="52" rx="16" fill="#1D057D"/>
  <rect x="108" y="388" width="244" height="52" rx="16" fill="rgba(255,255,255,0.08)"/>
  <rect x="108" y="464" width="244" height="52" rx="16" fill="rgba(255,255,255,0.08)"/>
  <rect x="476" y="312" width="244" height="52" rx="16" fill="#FE017F"/>
  <rect x="476" y="388" width="244" height="52" rx="16" fill="rgba(255,255,255,0.08)"/>
  <rect x="476" y="464" width="244" height="52" rx="16" fill="rgba(255,255,255,0.08)"/>
  <rect x="844" y="312" width="248" height="168" rx="20" fill="rgba(255,255,255,0.08)"/>
  <rect x="844" y="508" width="248" height="52" rx="16" fill="rgba(255,255,255,0.08)"/>
  <circle cx="390" cy="338" r="12" fill="#FE017F"/>
  <circle cx="760" cy="338" r="12" fill="#FE017F"/>
  <path d="M364 338h52" stroke="#FE017F" stroke-width="6" stroke-linecap="round"/>
  <path d="M734 338h52" stroke="#FE017F" stroke-width="6" stroke-linecap="round"/>
</svg>"""


def svg_slide_observability() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760">
  <defs>
    <linearGradient id="bg2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#100827"/>
      <stop offset="100%" stop-color="#1D057D"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="760" rx="40" fill="url(#bg2)"/>
  <rect x="80" y="76" width="460" height="260" rx="30" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.12)"/>
  <rect x="80" y="378" width="460" height="302" rx="30" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.12)"/>
  <rect x="582" y="76" width="538" height="604" rx="30" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.12)"/>
  <text x="118" y="134" fill="#FFFFFF" font-size="28" font-family="IBM Plex Sans, Arial, sans-serif">pipeline_runs</text>
  <text x="118" y="436" fill="#FFFFFF" font-size="28" font-family="IBM Plex Sans, Arial, sans-serif">pipeline_events</text>
  <text x="620" y="134" fill="#FFFFFF" font-size="28" font-family="IBM Plex Sans, Arial, sans-serif">sla + alerting</text>
  <rect x="118" y="168" width="386" height="24" rx="12" fill="rgba(255,255,255,0.10)"/>
  <rect x="118" y="214" width="300" height="24" rx="12" fill="#73F3A1"/>
  <rect x="118" y="260" width="210" height="24" rx="12" fill="#FFD166"/>
  <rect x="118" y="506" width="386" height="20" rx="10" fill="rgba(255,255,255,0.08)"/>
  <rect x="118" y="548" width="386" height="20" rx="10" fill="rgba(255,255,255,0.08)"/>
  <rect x="118" y="590" width="240" height="20" rx="10" fill="#FE017F"/>
  <path d="M620 532c40-90 98-108 148-158 56-56 88-114 150-214" stroke="#FE017F" stroke-width="8" fill="none" stroke-linecap="round"/>
  <circle cx="620" cy="532" r="16" fill="#FE017F"/>
  <circle cx="768" cy="374" r="16" fill="#FE017F"/>
  <circle cx="918" cy="246" r="16" fill="#FE017F"/>
  <circle cx="1068" cy="160" r="16" fill="#73F3A1"/>
  <rect x="620" y="566" width="438" height="54" rx="18" fill="rgba(255,255,255,0.08)"/>
</svg>"""


def svg_slide_revenue_automation() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760">
  <defs>
    <linearGradient id="bg3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120b33"/>
      <stop offset="100%" stop-color="#20094f"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="760" rx="40" fill="url(#bg3)"/>
  <rect x="88" y="94" width="240" height="150" rx="28" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.10)"/>
  <rect x="480" y="94" width="240" height="150" rx="28" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.10)"/>
  <rect x="872" y="94" width="240" height="150" rx="28" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.10)"/>
  <text x="132" y="160" fill="#FFFFFF" font-size="30" font-family="IBM Plex Sans, Arial, sans-serif">ads</text>
  <text x="528" y="160" fill="#FFFFFF" font-size="30" font-family="IBM Plex Sans, Arial, sans-serif">forms</text>
  <text x="914" y="160" fill="#FFFFFF" font-size="30" font-family="IBM Plex Sans, Arial, sans-serif">crm</text>
  <path d="M328 170h116" stroke="#FE017F" stroke-width="8" stroke-linecap="round"/>
  <path d="M720 170h116" stroke="#FE017F" stroke-width="8" stroke-linecap="round"/>
  <circle cx="452" cy="170" r="15" fill="#FE017F"/>
  <circle cx="844" cy="170" r="15" fill="#FE017F"/>
  <rect x="88" y="320" width="1024" height="352" rx="30" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.10)"/>
  <text x="132" y="382" fill="#FFFFFF" font-size="28" font-family="IBM Plex Sans, Arial, sans-serif">routing + enrichment + sync</text>
  <rect x="132" y="426" width="168" height="110" rx="20" fill="#1D057D"/>
  <rect x="332" y="426" width="168" height="110" rx="20" fill="#FE017F"/>
  <rect x="532" y="426" width="168" height="110" rx="20" fill="rgba(255,255,255,0.10)"/>
  <rect x="732" y="426" width="168" height="110" rx="20" fill="rgba(255,255,255,0.10)"/>
  <rect x="932" y="426" width="136" height="110" rx="20" fill="#73F3A1"/>
  <rect x="132" y="574" width="936" height="26" rx="13" fill="rgba(255,255,255,0.08)"/>
</svg>"""


def site_css() -> str:
    return """
:root {
  color-scheme: dark;
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
  --theme-color: #1D057D;
  --header-surface: rgba(9, 5, 29, 0.72);
  --grid-line: rgba(255, 255, 255, 0.045);
  --gradient-a: rgba(254, 1, 127, 0.9);
  --gradient-b: rgba(29, 5, 125, 1);
  --stage-base: rgba(255, 255, 255, 0.05);
  --stage-glow-a: rgba(254, 1, 127, 0.22);
  --stage-glow-b: rgba(29, 5, 125, 0.35);
  --brand-chip-bg: rgba(9, 5, 29, 0.7);
  --brand-chip-line: rgba(255, 255, 255, 0.14);
  --carousel-shell-bg: rgba(7, 4, 24, 0.48);
  --carousel-shell-line: rgba(255, 255, 255, 0.14);
  --carousel-caption-bg: rgba(9, 5, 29, 0.72);
  --carousel-caption-line: rgba(255, 255, 255, 0.12);
  --button-secondary-bg: rgba(255, 255, 255, 0.08);
  --button-secondary-line: rgba(255, 255, 255, 0.14);
  --button-ghost-color: rgba(245, 239, 255, 0.76);
  --pill-surface: rgba(255, 255, 255, 0.04);
  --terminal-code: #ffcaeb;
  --stat-surface: rgba(255, 255, 255, 0.05);
  --footer-surface: linear-gradient(135deg, rgba(29, 5, 125, 0.58), rgba(19, 12, 51, 0.94));
  --theme-switch-bg: rgba(255, 255, 255, 0.06);
  --theme-switch-thumb: rgba(255, 255, 255, 0.14);
  --theme-switch-text: rgba(245, 239, 255, 0.64);
}

html[data-theme="light"] {
  color-scheme: light;
  --bg: #ffffff;
  --bg-elevated: #ffffff;
  --bg-soft: rgba(17, 24, 39, 0.03);
  --card: rgba(255, 255, 255, 0.94);
  --card-strong: rgba(255, 255, 255, 0.98);
  --text: #15122b;
  --text-soft: rgba(21, 18, 43, 0.78);
  --text-muted: rgba(21, 18, 43, 0.56);
  --line: rgba(21, 18, 43, 0.1);
  --shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
  --theme-color: #ffffff;
  --header-surface: rgba(255, 255, 255, 0.94);
  --grid-line: rgba(21, 18, 43, 0.05);
  --gradient-a: rgba(254, 1, 127, 0.14);
  --gradient-b: rgba(29, 5, 125, 0.08);
  --stage-base: rgba(255, 255, 255, 0.88);
  --stage-glow-a: rgba(254, 1, 127, 0.08);
  --stage-glow-b: rgba(29, 5, 125, 0.06);
  --brand-chip-bg: rgba(255, 255, 255, 0.94);
  --brand-chip-line: rgba(21, 18, 43, 0.08);
  --carousel-shell-bg: rgba(255, 255, 255, 0.94);
  --carousel-shell-line: rgba(21, 18, 43, 0.08);
  --carousel-caption-bg: rgba(255, 255, 255, 0.94);
  --carousel-caption-line: rgba(21, 18, 43, 0.1);
  --button-secondary-bg: rgba(21, 18, 43, 0.04);
  --button-secondary-line: rgba(21, 18, 43, 0.1);
  --button-ghost-color: #1d057d;
  --pill-surface: rgba(21, 18, 43, 0.04);
  --terminal-code: #8f135d;
  --stat-surface: rgba(255, 255, 255, 0.96);
  --footer-surface: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(247, 247, 250, 1));
  --theme-switch-bg: rgba(21, 18, 43, 0.04);
  --theme-switch-thumb: rgba(21, 18, 43, 0.08);
  --theme-switch-text: rgba(21, 18, 43, 0.58);
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
  background: radial-gradient(circle, var(--gradient-a), rgba(254, 1, 127, 0));
}

.gradient-b {
  width: 28rem;
  height: 28rem;
  left: -8rem;
  top: 24rem;
  background: radial-gradient(circle, var(--gradient-b), rgba(29, 5, 125, 0));
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: var(--header-surface);
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
.lang-switch,
.theme-switch {
  color: var(--text-soft);
  font-size: 0.92rem;
}

.nav-link:hover,
.lang-switch:hover,
.theme-switch:hover,
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

.theme-switch {
  position: relative;
  display: inline-grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: center;
  width: 6.8rem;
  padding: 0.24rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: var(--theme-switch-bg);
  cursor: pointer;
  overflow: hidden;
}

.theme-switch::after {
  content: "";
  position: absolute;
  top: 0.24rem;
  left: 0.24rem;
  width: calc(50% - 0.24rem);
  height: calc(100% - 0.48rem);
  border-radius: 999px;
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
  justify-content: center;
  padding: 0.32rem 0.2rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--theme-switch-text);
}

html[data-theme="dark"] .theme-option-dark,
html[data-theme="light"] .theme-option-light {
  color: var(--text);
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

.hero,
.section,
.section-heading-page,
.site-footer,
.detail-hero {
  position: relative;
  z-index: 1;
}

.hero {
  padding: 3rem 0 1rem;
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
  font-size: clamp(2.4rem, 4.8vw, 4.6rem);
  line-height: 0.98;
  max-width: 11ch;
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
.footer-copy {
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
  background: var(--button-secondary-bg);
  border-color: var(--button-secondary-line);
  color: var(--text);
}

.button-ghost {
  border-color: var(--line);
  color: var(--button-ghost-color);
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
  background: var(--pill-surface);
  color: var(--text-soft);
  font-size: 0.82rem;
}

.hero-visual {
  display: grid;
  gap: 1rem;
}

.brand-stage {
  position: relative;
  min-height: 32rem;
  border-radius: var(--radius);
  padding: 1.25rem;
  background:
    radial-gradient(circle at 28% 25%, var(--stage-glow-a), transparent 46%),
    radial-gradient(circle at 72% 76%, var(--stage-glow-b), transparent 40%),
    var(--stage-base);
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

.brand-chip {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.7rem 0.95rem;
  border-radius: 999px;
  background: var(--brand-chip-bg);
  border: 1px solid var(--brand-chip-line);
  backdrop-filter: blur(12px);
}

.brand-chip-logo {
  width: 2rem;
  height: 2rem;
}

.brand-chip span {
  font-family: "Space Grotesk", sans-serif;
  font-size: 0.95rem;
}

.carousel-shell {
  position: absolute;
  inset: 1.2rem;
  border-radius: calc(var(--radius) - 10px);
  overflow: hidden;
  border: 1px solid var(--carousel-shell-line);
  background: var(--carousel-shell-bg);
}

.carousel-slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  transform: scale(1.03);
  transition: opacity 420ms ease, transform 420ms ease;
}

.carousel-slide.is-active {
  opacity: 1;
  transform: scale(1);
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-caption {
  position: absolute;
  left: 1.25rem;
  right: 1.25rem;
  bottom: 1.25rem;
  display: grid;
  gap: 0.35rem;
  padding: 1rem 1.1rem;
  border-radius: 22px;
  background: var(--carousel-caption-bg);
  border: 1px solid var(--carousel-caption-line);
  backdrop-filter: blur(10px);
}

.carousel-caption strong {
  font-family: "Space Grotesk", sans-serif;
  font-size: 1.08rem;
}

.carousel-caption span {
  color: var(--text-soft);
  line-height: 1.55;
}

.carousel-controls {
  position: absolute;
  right: 1.4rem;
  top: 1.6rem;
  z-index: 2;
  display: inline-flex;
  gap: 0.55rem;
}

.carousel-dot {
  width: 0.8rem;
  height: 0.8rem;
  border-radius: 999px;
  border: 0;
  padding: 0;
  background: rgba(255, 255, 255, 0.24);
  cursor: pointer;
}

.carousel-dot.is-active {
  background: var(--primary);
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
  color: var(--terminal-code);
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
  background: var(--stat-surface);
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

.section-actions {
  display: flex;
  justify-content: center;
  margin-top: 1.4rem;
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

.project-card-compact .project-card-top {
  margin-bottom: 0.7rem;
}

.project-card-compact .project-summary {
  margin-bottom: 0;
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

.detail-stack-preview {
  list-style: none;
  padding: 0;
  margin: 1.2rem 0 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
}

.detail-stack-preview li {
  padding: 0.48rem 0.78rem;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: var(--pill-surface);
  color: var(--text-soft);
  font-size: 0.82rem;
}

.detail-panel {
  padding: 1.4rem;
}

.detail-chip {
  margin-bottom: 0.8rem;
}

.detail-proof-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.detail-proof-card {
  padding: 1.3rem 1.35rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--line);
  background: var(--card);
  box-shadow: var(--shadow);
}

.detail-proof-kicker {
  margin: 0 0 0.85rem;
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.detail-proof-card strong {
  display: block;
  font-family: "Space Grotesk", sans-serif;
  font-size: 1.18rem;
  line-height: 1.2;
  margin-bottom: 0.5rem;
}

.detail-proof-card span {
  color: var(--text-soft);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.detail-grid-rich {
  align-items: stretch;
}

.detail-card h2 {
  margin-bottom: 1rem;
}

.detail-card-emphasis {
  background: linear-gradient(135deg, rgba(254, 1, 127, 0.12), rgba(29, 5, 125, 0.18));
}

html[data-theme="light"] .detail-card-emphasis {
  background: linear-gradient(135deg, rgba(254, 1, 127, 0.08), rgba(29, 5, 125, 0.06));
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
  background: var(--footer-surface);
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
  .detail-proof-grid,
  .detail-grid,
  .service-grid,
  .process-grid,
  .project-grid,
  .project-grid-wide {
    grid-template-columns: 1fr;
  }

  .hero-stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
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

  .theme-switch {
    width: 100%;
    max-width: 8rem;
  }

  .site-header[data-open="true"] .site-nav {
    display: flex;
  }

  .brand-stage {
    min-height: 26rem;
  }

  .carousel-caption {
    left: 1rem;
    right: 1rem;
    bottom: 1rem;
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
  .lang-switch,
  .theme-switch,
  .theme-switch::after {
    transition: none;
  }
}
""".strip()


def site_js() -> str:
    return """
const themeKey = "b-tech-theme";
const root = document.documentElement;
const themeToggle = document.querySelector("[data-theme-toggle]");
const themeMeta = document.querySelector("#theme-color-meta");

const applyTheme = (theme) => {
  const nextTheme = theme === "light" ? "light" : "dark";
  root.setAttribute("data-theme", nextTheme);
  if (themeMeta) {
    themeMeta.setAttribute("content", nextTheme === "light" ? "#ffffff" : "#1D057D");
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
  applyTheme(root.getAttribute("data-theme") || "dark");
}

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

const carousel = document.querySelector("[data-carousel]");

if (carousel) {
  const slides = Array.from(carousel.querySelectorAll("[data-carousel-slide]"));
  const dots = Array.from(carousel.querySelectorAll("[data-carousel-dot]"));
  let activeIndex = 0;
  let timer;

  const setActive = (index) => {
    activeIndex = index;
    slides.forEach((slide, slideIndex) => {
      slide.classList.toggle("is-active", slideIndex === index);
    });
    dots.forEach((dot, dotIndex) => {
      dot.classList.toggle("is-active", dotIndex === index);
    });
  };

  const restart = () => {
    window.clearInterval(timer);
    timer = window.setInterval(() => {
      setActive((activeIndex + 1) % slides.length);
    }, 4200);
  };

  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      setActive(index);
      restart();
    });
  });

  setActive(0);
  restart();
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
        t(language, "Project Portfolio", "Portfolio de Projetos"),
        t(
            language,
            "Portfolio of data engineering, analytics, and automation systems by B Tecnologia.",
            "Portfolio de sistemas de engenharia de dados, analytics e automacao da B Tecnologia.",
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
      <p>If you arrived here from a message or proposal, the homepage and project archive contain the current B Tecnologia portfolio links.</p>
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
    write_text(DIST / "assets" / "slide-lakehouse.svg", svg_slide_lakehouse())
    write_text(DIST / "assets" / "slide-observability.svg", svg_slide_observability())
    write_text(DIST / "assets" / "slide-revenue-automation.svg", svg_slide_revenue_automation())


if __name__ == "__main__":
    build_pages()
