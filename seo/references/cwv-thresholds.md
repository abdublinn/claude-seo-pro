# Core Web Vitals Thresholds — 2026 Reference

## Primary Metrics (ranking signals)

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤2.5s | 2.5s–4.0s | >4.0s |
| **INP** (Interaction to Next Paint) | ≤200ms | 200ms–500ms | >500ms |
| **CLS** (Cumulative Layout Shift) | ≤0.1 | 0.1–0.25 | >0.25 |

## Secondary Metrics (diagnostic)

| Metric | Good | Acceptable | Poor |
|--------|------|-----------|------|
| **TTFB** (Time to First Byte) | ≤800ms | 800ms–1800ms | >1800ms |
| **FCP** (First Contentful Paint) | ≤1.8s | 1.8s–3.0s | >3.0s |
| **TBT** (Total Blocking Time) | ≤200ms | 200ms–600ms | >600ms |

## LCP Subparts

| Subpart | Budget |
|---------|--------|
| TTFB | ~40% of LCP |
| Resource load delay | ~10% |
| Resource load time | ~40% |
| Element render delay | ~10% |

## INP Breakdown

| Phase | Budget |
|-------|--------|
| Input delay | <100ms |
| Processing time | <100ms |
| Presentation delay | <100ms |

## v2.0 Note: Cached vs Uncached

TTFB varies dramatically between cached and uncached visits:
- **Cached** (WP Rocket, Cloudflare, CDN): 50-200ms typical
- **Uncached** (first visit, crawler, cache miss): 500-3000ms for dynamic CMS

Always report which scenario is being measured. SiteAnalyzer/Screaming Frog crawl without cache.
