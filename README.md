# claude-seo-pro v2.1.0

Professional SEO audit & optimization plugin for [Claude Code](https://claude.ai/claude-code). 15 skills, 10 parallel subagents, deep crawl with 18 checks, and AI search readiness analysis.

## Features

### Full Site Audit (`/seo audit <url>`)
Runs 10 specialized subagents in parallel and produces a unified SEO Health Score (0-100):

| Agent | What it checks |
|-------|---------------|
| **seo-crawl** | 18 checks: broken links (internal + external), redirect chains, duplicate meta tags, missing descriptions, pagination, empty anchors, cyclic links, text/HTML ratio, HTML size, canonical validation, orphan pages, OG tags, feed indexation, URL normalization |
| **seo-technical** | 14 categories: crawlability, indexability, security, mobile, CWV, JS rendering, IndexNow, Yandex-specific, robots.txt rule testing, sitemap↔crawl cross-reference |
| **seo-content** | E-E-A-T assessment, readability, thin content detection, AI citation readiness, content freshness, OG tag audit |
| **seo-schema** | JSON-LD detection, validation, generation with ready-to-paste code |
| **seo-sitemap** | Structure analysis, quality gates, missing pages |
| **seo-performance** | LCP, INP, CLS, TTFB (cached + uncached methodology) |
| **seo-geo** | AI crawler access, llms.txt, passage citability, brand mentions |
| **seo-visual** | Screenshots, mobile rendering, above-the-fold analysis |
| **seo-local** | GBP signals, NAP consistency, local schema, citations (RU: Yandex.Справочnik, 2GIS) |
| **seo-competitor** | Top 3 competitor comparison, key metric gaps |

### Scoring Weights

| Category | Weight |
|----------|--------|
| Technical SEO | 15% |
| Crawl Health | 12% |
| Content Quality | 18% |
| On-Page SEO | 18% |
| Schema | 10% |
| Performance (CWV) | 10% |
| AI Search (GEO) | 7% |
| Images | 5% |
| Competitor Delta | 5% |

### Agent Ownership (no duplicate work)

| Data | Owner | Others defer |
|------|-------|-------------|
| HTTP statuses, broken links, redirects, duplicates | seo-crawl | seo-technical, seo-content |
| Meta tag quality, E-E-A-T, readability | seo-content | seo-crawl |
| robots.txt, security, Yandex, sitemap↔crawl | seo-technical | seo-crawl |
| CWV measurements | seo-performance | seo-technical (flags only) |

## Installation

### Option 1: Plugin install (recommended)
```bash
/plugin install https://github.com/AgriciDaniel/claude-seo-pro
```

### Option 2: Local development
```bash
git clone https://github.com/AgriciDaniel/claude-seo-pro.git
claude --plugin-dir ./claude-seo-pro
```

### Option 3: Manual install
```bash
git clone https://github.com/AgriciDaniel/claude-seo-pro.git
cd claude-seo-pro

# Linux/macOS
bash install.sh

# Windows
powershell -ExecutionPolicy Bypass -File install.ps1
```

### Python dependencies (optional, for deep crawl)
```bash
pip install -r requirements.txt
```
Without Python deps, the crawler falls back to WebFetch (slower, approximate counts).

## All Commands

```bash
/seo audit <url>              # Full audit with 10 parallel subagents
/seo crawl <url>              # Deep crawl analysis (18 checks)
/seo technical <url>          # Technical SEO (14 categories)
/seo content <url>            # Content quality & E-E-A-T
/seo schema <url>             # Structured data (JSON-LD)
/seo images <url>             # Image optimization
/seo geo <url>                # AI search readiness (GEO)
/seo page <url>               # Single page deep analysis
/seo sitemap <url>            # Sitemap analysis
/seo local <url>              # Local SEO
/seo plan <type>              # Strategic SEO plan (6 industry templates)
/seo hreflang <url>           # International SEO
/seo programmatic             # Programmatic SEO at scale
/seo competitor-pages         # Comparison & alternatives pages
```

Industry plan templates: `ecommerce`, `saas`, `local-service`, `publisher`, `agency`, `generic`

## Project Structure

```
claude-seo-pro/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── seo/
│   ├── SKILL.md                 # Main orchestrator (routes /seo commands)
│   └── references/              # On-demand knowledge files
│       ├── crawl-checklist.md   # Crawl health scoring rubric (13 metrics)
│       ├── cwv-thresholds.md    # Core Web Vitals 2026 thresholds
│       ├── eeat-framework.md    # E-E-A-T evaluation criteria
│       ├── quality-gates.md     # Content quality minimums
│       ├── schema-types.md      # Schema.org type reference
│       ├── local-seo-signals.md # Local ranking factors
│       └── local-schema-types.md # LocalBusiness subtypes
├── skills/                      # 15 sub-skills
│   ├── seo-audit/SKILL.md
│   ├── seo-crawl/SKILL.md
│   ├── seo-technical/SKILL.md
│   ├── seo-content/SKILL.md
│   ├── seo-schema/SKILL.md
│   ├── seo-sitemap/SKILL.md
│   ├── seo-images/SKILL.md
│   ├── seo-geo/SKILL.md
│   ├── seo-page/SKILL.md
│   ├── seo-local/SKILL.md
│   ├── seo-plan/SKILL.md + assets/
│   ├── seo-hreflang/SKILL.md
│   ├── seo-programmatic/SKILL.md
│   └── seo-competitor-pages/SKILL.md
├── agents/                      # 9 specialized subagents
│   ├── seo-crawl.md
│   ├── seo-technical.md
│   ├── seo-content.md
│   ├── seo-schema.md
│   ├── seo-sitemap.md
│   ├── seo-performance.md
│   ├── seo-geo.md
│   ├── seo-visual.md
│   └── seo-local.md
├── scripts/                     # Python crawl & analysis tools
│   ├── crawl_site.py            # Site crawler (v2.1)
│   ├── check_links.py           # Link health analyzer (v2.1)
│   ├── fetch_page.py            # Page fetcher
│   └── parse_html.py            # HTML parser
├── schema/
│   └── templates.json           # JSON-LD templates
├── requirements.txt             # Python dependencies
├── install.sh                   # Linux/macOS installer
├── install.ps1                  # Windows installer
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## What's New in v2.1 (vs v2.0)

### Agent ownership boundaries
Clear separation: seo-crawl owns all quantitative data, seo-content owns quality analysis, seo-technical owns configuration checks. No more duplicated findings.

### 6 new crawl checks (12 -> 18)
- External link health (HEAD checks with bot-block filtering)
- Text/HTML ratio (flags pages <10%)
- HTML document size (flags >200KB)
- Canonical validation (self-ref, target status, chains)
- Orphan & dead-end page detection
- Open Graph tag coverage

### 3 new technical categories (11 -> 14)
- robots.txt rule testing (collateral damage detection)
- Yandex-specific (verification, Metrika, turbo pages, YML feed)
- Sitemap ↔ crawl cross-reference

### TTFB methodology fix
Always reports cached + uncached TTFB. Never claims "excellent" from cached values alone.

### Other
- Competitor Quick Glance (5% scoring weight)
- Dependency check with graceful degradation
- Updated Python scripts (crawl_site.py v2.1, check_links.py v2.1)

## Origin

Based on [claude-seo v1.6.0](https://github.com/AgriciDaniel/claude-seo). Enhanced after real-world comparison of Claude SEO audit output vs professional crawler data (SiteAnalyzer/Moxelle), which revealed 24 gaps in crawl-level analysis.

## License

MIT
