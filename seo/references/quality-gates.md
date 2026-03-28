# Content Quality Gates — Minimum Thresholds (v2.1)

## Minimum Word Count by Page Type

| Page type | Minimum | Recommended | Flag as thin |
|-----------|---------|-------------|-------------|
| Homepage | 300 | 500+ | <200 |
| Product page | 150 | 300+ | <100 |
| Category page | 100 | 200+ | <50 |
| Blog article | 500 | 1000+ | <300 |
| Service page | 300 | 600+ | <200 |
| About page | 200 | 400+ | <150 |
| Contact page | 50 | 100+ | <30 |
| FAQ page | 300 | 500+ | <200 |
| Location page | 300 | 500+ | <200 |

## Uniqueness Thresholds

| Element | Threshold | Action |
|---------|-----------|--------|
| Title tag | Must be unique per page | Flag duplicates |
| Meta description | Must be unique per page | Flag duplicates |
| H1 tag | Must be unique per page | Flag duplicates |
| Body content | >80% unique per page | Flag near-duplicates |

## Description Coverage

| Coverage | Rating |
|----------|--------|
| >95% pages with description | Excellent |
| 80-95% | Good |
| 50-80% | Needs work |
| <50% | Critical |

## Title Length

| Length | Rating |
|--------|--------|
| 30-60 chars | Optimal |
| 20-30 chars | Short |
| 60-70 chars | Slightly long (may truncate) |
| >70 chars | Too long |
| <20 chars | Too short |

## Description Length

| Length | Rating |
|--------|--------|
| 120-160 chars | Optimal |
| 70-120 chars | Short (but acceptable) |
| 160-200 chars | Slightly long |
| >200 chars | Too long (will truncate) |
| <70 chars | Too short |

## HTML Document Size (NEW v2.1)

| Size | Rating |
|------|--------|
| <50 KB | Optimal |
| 50-100 KB | Normal |
| 100-200 KB | Large — review |
| 200-500 KB | Very large — optimize |
| >500 KB | Critical — will impact TTFB |

## Text/HTML Ratio (NEW v2.1)

| Ratio | Rating |
|-------|--------|
| >40% | Excellent |
| 25-40% | Good |
| 10-25% | Acceptable |
| 5-10% | Low — flag for review |
| <5% | Critical — likely boilerplate-heavy |

## Open Graph Coverage (NEW v2.1)

| Coverage | Rating |
|----------|--------|
| >90% pages with all 3 OG tags | Excellent |
| 70-90% | Good |
| 50-70% | Needs work |
| <50% | Poor — social sharing degraded |

Required OG tags: `og:title`, `og:description`, `og:image`

## External Link Health (NEW v2.1)

| Broken count (excluding bot-blocks) | Rating |
|--------------------------------------|--------|
| 0 | Excellent |
| 1-3 | Good |
| 4-10 | Needs work |
| >10 | Poor |

Note: 403/498 from marketplaces (Wildberries, MegaMarket) are bot-blocks, NOT broken links.
