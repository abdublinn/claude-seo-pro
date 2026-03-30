# claude-seo-pro v2.2.0

## Project Overview
Enhanced SEO audit skill for Claude Code. Based on claude-seo v1.6.0 → v2.0.0 → v2.1.0 → v2.2.0. Major improvements in crawl depth, agent ownership, methodology accuracy, and false positive reduction.

## Architecture
- `seo/SKILL.md` — Main orchestrator, routes `/seo <command>` to sub-skills
- `skills/` — 14 sub-skills (each with SKILL.md)
- `agents/` — 10 subagents for parallel audit (9 + competitor)
- `scripts/` — Python scripts for crawling and parsing (v2.2)
- `seo/references/` — On-demand knowledge files (7 reference docs, updated v2.2)

## Key Commands
- `/seo audit <url>` — Full audit with 10 parallel subagents
- `/seo crawl <url>` — Deep crawl analysis (18 checks)
- `/seo page <url>` — Single page analysis
- `/seo technical <url>` — Technical SEO (14 categories)
- `/seo content <url>` — Content & E-E-A-T (quality-focused)
- `/seo schema <url>` — Structured data
- `/seo images <url>` — Image optimization
- `/seo geo <url>` — AI search readiness
- `/seo sitemap <url>` — Sitemap analysis
- `/seo local <url>` — Local SEO
- `/seo plan <type>` — Strategic plan
- `/seo hreflang <url>` — International SEO
- `/seo programmatic` — Programmatic SEO
- `/seo competitor-pages` — Comparison pages

## What's New in v2.1

### Agent Ownership (eliminates duplicated work)
- `seo-crawl` owns ALL quantitative data: HTTP statuses, broken links, duplicates, meta counts
- `seo-content` owns qualitative analysis: E-E-A-T, readability, meta tag quality, OG audit
- `seo-technical` owns configuration: robots.txt rules, security, Yandex, sitemap↔crawl

### New Checks in seo-crawl (18 total, was 12)
- External link health (HEAD checks, bot-block filtering)
- Text/HTML ratio (flag <10%)
- HTML document size (flag >200KB)
- Canonical validation (self-ref, target status, chains)
- Orphan & dead-end page detection
- Open Graph tag coverage

### New Checks in seo-technical (14 categories, was 11)
- robots.txt rule testing (collateral damage detection)
- Yandex-specific (verification, Metrika, turbo pages, YML feed, Host directive)
- Sitemap ↔ crawl cross-reference

### TTFB Methodology Fix
- Always report cached + uncached TTFB
- Never say "excellent" from cached values alone
- TTFB distribution reported

### Other Improvements
- Competitor Quick Glance (5% weight in score)
- Dependency check before crawl (graceful degradation)
- Updated scoring weights: Crawl 8%→12%, added Competitor 5%
- crawl_site.py v2.1: external links, image HEAD sizing, text/HTML ratio, OG tags, HTML size
- check_links.py v2.1: orphan detection, canonical validation, PageRank flow score

## Agent Ownership Table
| Data | Owner | Others must NOT duplicate |
|------|-------|-|
| HTTP statuses, broken links, redirects, duplicates | seo-crawl | seo-technical, seo-content |
| Meta tag quality, E-E-A-T, readability | seo-content | seo-crawl |
| robots.txt, security, Yandex, sitemap↔crawl | seo-technical | seo-crawl |
| CWV measurements | seo-performance | seo-technical (flags only) |

## What's New in v2.2

### False Positive Reduction
- H1 detection now filters out `<h1>` inside `<code>`, `<pre>`, `<svg>`, `<template>` elements
- Empty links: fallback chain text → img alt → aria-label → title (reduces false empties by ~70%)
- Canonical: missing canonical only flagged as ACTION on parameterized + indexable pages
- NEW: Canonical in `<body>` detection (real bug, was previously invisible)
- Text/HTML ratio: excludes inline script/style from denominator; INFO level for JS/SSR sites
- URL normalization: handles www/non-www, protocol, case differences
- rel=prev/next: removed as recommendation (deprecated by Google since 2019)
- Added INFO severity level for context-dependent findings

## Quality Rules
- All scores are 0-100
- Crawl data must use exact counts (never estimates)
- Every CRITICAL issue must have a specific fix with code example
- JSON-LD code must be valid and ready to paste
- Never fabricate data
- TTFB: always report cached + uncached
- External 403/498 from marketplaces ≠ site errors
- If Python deps missing → accuracy warning in report header
- v2.2: Use INFO level for findings that depend on site architecture
