# Changelog

## [2.2.0] - 2026-03-30

### Fixed (False Positive Reduction)
- **H1 counting** — `<h1>` inside `<code>`, `<pre>`, `<svg>`, `<template>`, `<script>`, `<style>` are now excluded from H1 analysis. Eliminates false "multiple H1" reports on pages with code examples.
- **Empty anchor detection** — Added fallback chain: text → img alt → aria-label → title attribute. Links with images (alt text) or accessibility attributes are no longer falsely flagged as empty.
- **Canonical missing** — No longer flags missing canonical as an error on all pages. Only flags as ACTION on parameterized (`?page=`, `?sort=`) AND indexable (no noindex) pages. Other missing canonicals reported as INFO.
- **Text/HTML ratio** — Excludes inline `<script>` and `<style>` content from HTML size denominator. JS/SSR sites (React, Next.js, Nuxt) will see fairer ratios. Ratio 5-10% on SSR sites is now INFO, not CRITICAL.
- **URL normalization** — `_normalize()` now handles www/non-www, http/https protocol differences, and URL case. Prevents false duplicate detection.
- **rel=prev/next** — Removed as a recommendation in seo-technical. Google deprecated rel=prev/next in March 2019; recommending it was outdated advice.

### Added
- **INFO severity level** — New level for context-dependent findings that may not require action (architecture-specific ratios, optional canonical on simple pages)
- **Canonical in `<body>` detection** — Detects when `<link rel="canonical">` is placed in `<body>` instead of `<head>` — a real bug that causes search engines to ignore the tag. Flagged as CRITICAL.
- **`canonical_in_body` field** in crawl data — boolean flag per page

### Changed
- crawl_site.py v2.1→v2.2: H1 filtering, anchor text fallbacks, canonical position detection, text/HTML ratio calculation
- check_links.py v2.1→v2.2: improved URL normalization, conditional canonical logic, canonical_in_body reporting
- crawl-checklist.md v2.1→v2.2: updated scoring for canonical, text/HTML ratio, empty anchors
- quality-gates.md v2.1→v2.2: context-aware text/HTML ratio thresholds
- seo-crawl SKILL.md: updated sections 2.5 (H1), 2.9 (empty anchors), 2.14 (text/HTML), 2.16 (canonical)
- seo-technical SKILL.md: pagination section updated — no longer recommends rel=prev/next

## [2.1.0] - 2026-03-28

### Added
- **Agent ownership boundaries** — clear separation eliminates duplicate work between agents
- **6 new crawl checks** (18 total): external link health, text/HTML ratio, HTML document size, canonical validation, orphan/dead-end pages, OG tag coverage
- **3 new technical categories** (14 total): robots.txt rule testing, Yandex-specific checks, sitemap↔crawl cross-reference
- **Competitor Quick Glance** — 10th subagent, 5% scoring weight
- **Dependency check** — graceful degradation if Python deps unavailable
- **crawl_site.py v2.1** — external link HEAD checks, image size HEAD checks, text/HTML ratio, OG tag extraction, HTML size tracking, TTFB distribution
- **check_links.py v2.1** — orphan detection, dead-end detection, canonical validation, redirect chain depth, PageRank flow score

### Changed
- Scoring weights: Crawl 8%→12%, Technical 17%→15%, Content 20%→18%, On-Page 20%→18%, GEO 10%→7%, added Competitor 5%
- seo-content no longer produces meta tag counts (moved to seo-crawl)
- seo-technical reduced redirect/pagination scope (details in seo-crawl)
- TTFB methodology: always reports cached + uncached, never claims "excellent" from cached alone
- Crawl health scoring rubric expanded from 8 to 13 metrics
- quality-gates.md updated with HTML size, text/HTML ratio, OG coverage, external link thresholds

### Fixed
- TTFB measurement was reporting only cached values, making scores appear 2-5x better than reality
- No mechanism to distinguish marketplace bot-blocks (403/498) from real broken external links
- Duplicate findings between seo-crawl and seo-technical for redirects/pagination

## [2.0.0] - 2026-03-21

### Added
- **seo-crawl module** — new 9th subagent for deep crawl analysis
- Broken link detection with inlink counts
- Redirect chain analysis
- Duplicate title/description/H1 detection
- Missing meta description audit with %
- Broken pagination validation
- Empty anchor link detection
- Cyclic link detection
- Feed page indexation check
- URL normalization audit (uppercase, cyrillic, encoding)
- PageRank flow analysis (orphans, dead-ends, leaks)
- Python crawler script: crawl_site.py
- Link health analyzer: check_links.py
- crawl-checklist.md reference
- seo-local skill and agent
- local-seo-signals.md and local-schema-types.md references

### Changed
- seo-technical enhanced with redirect/pagination validation
- seo-content enhanced with mass description coverage
- seo-images enhanced with file size tiers and filename audit
- Scoring: added Crawl Health 8% (from Technical and Content)

## [1.6.0] - 2026-03-15

Initial release based on claude-seo v1.6.0.
