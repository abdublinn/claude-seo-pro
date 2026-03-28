# Schema.org Types — Google Support Status (2026)

## Fully Supported (rich results eligible)

| Type | Use case | Key required properties |
|------|----------|----------------------|
| **Article** | Blog posts, news | headline, image, datePublished, author |
| **BlogPosting** | Blog articles | Same as Article |
| **Product** | Product pages | name, image, offers (price, availability, priceCurrency) |
| **LocalBusiness** | Local businesses | name, address, telephone |
| **Organization** | Company info | name, url, logo, sameAs |
| **WebSite** | Site-level | name, url, potentialAction (SearchAction) |
| **BreadcrumbList** | Navigation | itemListElement[].name, item |
| **FAQPage** | FAQ sections | **RESTRICTED**: Only gov/health sites since Aug 2023 |
| **Review** | Product reviews | reviewRating, author, itemReviewed |
| **AggregateRating** | Star ratings | ratingValue, reviewCount, bestRating |
| **Event** | Events | name, startDate, location |
| **Recipe** | Cooking | name, image, recipeIngredient |
| **VideoObject** | Videos | name, description, thumbnailUrl, uploadDate |
| **SoftwareApplication** | Apps | name, operatingSystem, offers |
| **Course** | Online courses | name, description, provider |
| **JobPosting** | Job listings | title, datePosted, hiringOrganization |
| **ProfilePage** | Author profiles | mainEntity (Person) |

## Deprecated / Removed

| Type | Status | Date | Alternative |
|------|--------|------|-------------|
| **HowTo** | REMOVED from rich results | Dec 2023 | Use Article with step-by-step content |
| **FAQ** | RESTRICTED to gov/health | Aug 2023 | Only use on government or health authority sites |
| **Speakable** | REMOVED | 2024 | No alternative |

## Logo Requirements

- Minimum: 112x112px
- Recommended: 1200x1200px
- Format: PNG, JPEG, SVG (but SVG may cause issues with some validators)
- **Common bug**: Yoast SEO + SVG logo = 1x1px in schema. Fix by setting a separate PNG logo in Yoast settings.

## sameAs Best Practices

Include links to all official profiles:
- Wikipedia/Wikidata (strongest signal)
- Social: VK, Telegram, YouTube, Instagram
- Directories: Yandex.Справочник, 2GIS, Flamp
- Marketplaces: Wildberries, Ozon, Яндекс.Маркет
- Industry-specific directories
