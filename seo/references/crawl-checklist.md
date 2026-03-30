# Crawl Health Checklist — v2.2 Reference

## Severity Levels (NEW v2.2)

| Level | Meaning | Action |
|-------|---------|--------|
| CRITICAL | Blocks indexing or breaks UX | Fix immediately |
| HIGH | Significant SEO impact | Fix within 1-2 weeks |
| MEDIUM | Moderate impact | Fix in normal workflow |
| LOW | Minor improvement | Fix when convenient |
| INFO | Context-dependent or informational | Review, may not need action |

**v2.2 change:** Added INFO level for findings that depend on site architecture (e.g., text/HTML ratio on SSR sites, missing canonical on pages without duplicates).

## Scoring Rubric

Each metric is scored 0-100. The Crawl Health Score is the weighted average of all 13 metrics (8 original + 5 new in v2.1, updated in v2.2).

### 1. Broken Internal Links (404/410/5xx)

| Count | Score | Priority |
|-------|-------|----------|
| 0 | 100 | — |
| 1-5 | 80 | HIGH |
| 6-15 | 60 | HIGH |
| 16-30 | 40 | CRITICAL |
| 31-50 | 20 | CRITICAL |
| >50 | 0 | CRITICAL |

**Impact**: Each broken link wastes crawl budget, loses PageRank, and creates 404 errors in Search Console.
**Fix**: 301 redirect to closest matching page, or restore content.

### 2. Missing Meta Description

| Percentage | Score | Priority |
|-----------|-------|----------|
| 0% | 100 | — |
| <10% | 80 | MEDIUM |
| <25% | 60 | HIGH |
| <50% | 40 | HIGH |
| <75% | 20 | CRITICAL |
| >75% | 0 | CRITICAL |

**Impact**: Google auto-generates snippets (often poorly). Custom descriptions improve CTR by 5-10%.
**Fix**: CMS template + manual for key pages.

### 3. Duplicate Titles

| Groups | Score | Priority |
|--------|-------|----------|
| 0 | 100 | — |
| 1-3 | 80 | MEDIUM |
| 4-10 | 60 | HIGH |
| 11-20 | 40 | HIGH |
| 21-50 | 20 | CRITICAL |
| >50 | 0 | CRITICAL |

**Common causes**: CMS templates for product variations, paginated archives, default titles.
**Fix**: Unique title per page using CMS variables.

### 4. Duplicate H1

Same rubric as Duplicate Titles.
**Common causes**: Archive pages sharing template H1, blog pagination with generic "Blog" H1.

### 5. Internal Redirect Chains

| Count | Score | Priority |
|-------|-------|----------|
| 0 | 100 | — |
| 1-5 | 80 | MEDIUM |
| 6-20 | 60 | HIGH |
| 21-50 | 40 | HIGH |
| 51-100 | 20 | CRITICAL |
| >100 | 0 | CRITICAL |

**Impact**: Each redirect hop loses ~10-15% PageRank. Chains slow crawling.
**Fix**: Update internal links to point to final destination URL.

### 6. Empty Anchor Links

| Count | Score | Priority |
|-------|-------|----------|
| 0 | 100 | — |
| 1-10 | 80 | LOW |
| 11-30 | 60 | MEDIUM |
| 31-70 | 40 | MEDIUM |
| 71-150 | 20 | HIGH |
| >150 | 0 | HIGH |

**Impact**: Screen readers can't navigate. Crawlers get no anchor text signal.
**Fix**: Add `aria-label` or visible text. For icon-only links, use `aria-label="icon description"`.
**v2.2 note**: Links containing images with alt text, or links with `aria-label`/`title` attributes are no longer counted as empty. Only truly text-free links are flagged.

### 7. Cyclic Links (Self-referencing)

| Count | Score | Priority |
|-------|-------|----------|
| 0 | 100 | — |
| 1-10 | 80 | LOW |
| 11-30 | 60 | MEDIUM |
| 31-70 | 40 | MEDIUM |
| 71-150 | 20 | HIGH |
| >150 | 0 | HIGH |

**Impact**: Wastes crawl budget. Confuses link graph analysis.
**Fix**: Remove self-links or use `<span>` for current-page indicators in navigation.

### 8. Broken Pagination

| Count | Score | Priority |
|-------|-------|----------|
| 0 | 100 | — |
| 1 | 80 | HIGH |
| 2-3 | 60 | HIGH |
| 4-5 | 40 | CRITICAL |
| 6-10 | 20 | CRITICAL |
| >10 | 0 | CRITICAL |

**Impact**: Users and crawlers can't access paginated content. Internal links become 404.
**Fix**: Regenerate pagination or 301 redirect to last valid page.

### 9. External Link Health (NEW v2.1)

| Broken external count | Score | Priority |
|-----------------------|-------|----------|
| 0 | 100 | — |
| 1-3 | 80 | MEDIUM |
| 4-10 | 60 | HIGH |
| 11-20 | 40 | HIGH |
| >20 | 20 | CRITICAL |

**Important**: Do NOT count bot-blocks (403 from Wildberries, 498 from marketplace APIs) as broken. Only count real 404/410/5xx on external sites.
**Fix**: Replace broken external links with working alternatives or remove them.

### 10. Text/HTML Ratio (UPDATED v2.2)

| % pages with ratio >10% | Score | Priority |
|--------------------------|-------|----------|
| >90% | 100 | — |
| >80% | 80 | LOW |
| >60% | 60 | MEDIUM |
| >40% | 40 | HIGH |
| <40% | 20 | HIGH |

**v2.2 changes:**
- Ratio now excludes inline `<script>` and `<style>` content from HTML size denominator.
- For JS/SSR sites (React, Next.js, Nuxt), ratio 5-10% is expected — flag as INFO, not CRITICAL.
- Only flag as CRITICAL if ratio <5% AND word count <100 (truly thin content).

**Impact**: Very low text/HTML ratio signals boilerplate-heavy pages. Google may treat as thin content.
**Fix**: Reduce inline CSS/JS, remove unnecessary markup, add more textual content.

### 11. HTML Document Size (NEW v2.1)

| % pages under 200KB | Score | Priority |
|----------------------|-------|----------|
| >95% | 100 | — |
| >85% | 80 | LOW |
| >70% | 60 | MEDIUM |
| >50% | 40 | HIGH |
| <50% | 20 | CRITICAL |

**Impact**: Large HTML slows TTFB and parsing. Pages >500KB may timeout for slow connections.
**Fix**: Paginate long lists, defer non-critical content, optimize inline resources.

### 12. Canonical Validation (UPDATED v2.2)

| Issues | Score | Priority |
|--------|-------|----------|
| 0 actionable issues | 100 | — |
| 1-2 non-self | 80 | MEDIUM |
| 3-5 actionable missing | 60 | HIGH |
| Canonical in `<body>` | 20 | CRITICAL |
| Canonical target returns 404 | 0 | CRITICAL |
| Canonical chains | 40 | HIGH |

**v2.2 changes:**
- Missing canonical is only actionable if page has URL parameters AND is indexable (no noindex). Pages without params don't need canonical — reported as INFO.
- NEW: Canonical tag in `<body>` instead of `<head>` is flagged as CRITICAL — search engines may ignore it.
- Total missing canonical count is reported as INFO for transparency.

**Impact**: Wrong canonicals can de-index pages or consolidate ranking to wrong URL.
**Fix**: Fix canonical in `<body>` (move to `<head>`). Add canonical to parameterized indexable pages. Fix targets that return non-200.

### 13. OG Tag Coverage (NEW v2.1)

| % pages with all 3 OG tags | Score | Priority |
|-----------------------------|-------|----------|
| >90% | 100 | — |
| >70% | 80 | LOW |
| >50% | 60 | MEDIUM |
| >30% | 40 | HIGH |
| <30% | 20 | HIGH |

**Impact**: Pages shared on social without OG tags display poorly → lower social CTR.
**Fix**: Add og:title, og:description, og:image via CMS plugin (Yoast generates these automatically if configured).

## Additional Crawl Checks (not scored, but reported)

### URL Normalization
- **Uppercase in paths**: Flag if >50 URLs. Linux servers treat `/Page` and `/page` as different.
- **Cyrillic filenames**: Flag any. Causes long encoded URLs, breaks some tools.
- **Spaces in URLs**: Flag any. Always use hyphens.

### Feed Page Indexation
- `/feed/`, `*/feed/`, `*/comments/feed/` should be noindexed
- Should NOT appear in sitemap
- Common WordPress issue

### Orphan Pages
- Pages in sitemap with zero internal links pointing to them
- Crawlers may not discover them reliably

### Dead-End Pages
- Pages with zero outgoing internal links
- PageRank sinks — waste link equity

### PageRank Leak via Redirects
- Every internal link through a 301 loses ~10-15% PageRank
- N links through redirects × 0.15 = estimated total PageRank loss
