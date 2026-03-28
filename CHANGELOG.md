# Changelog

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
