#!/usr/bin/env python3
"""
Site crawler for SEO analysis — claude-seo-pro v2.1
Crawls a website via sitemap + link discovery, collecting:
- HTTP status codes + TTFB
- Meta tags (title, description, H1, canonical, robots, OG tags)
- Internal/external links with anchor text
- Images with alt text
- Word count, text/HTML ratio, HTML size
- External link status (HEAD checks)
- Image file sizes (HEAD checks)
"""

import argparse
import json
import re
import sys
import time
from collections import defaultdict
from urllib.parse import urljoin, urlparse

__version__ = "2.2.0"


def check_dependencies():
    """Check required dependencies and print versions."""
    missing = []
    try:
        import requests
        print(f"  requests: {requests.__version__}")
    except ImportError:
        missing.append("requests")
    try:
        import bs4
        print(f"  beautifulsoup4: {bs4.__version__}")
    except ImportError:
        missing.append("beautifulsoup4")
    try:
        import lxml
        print(f"  lxml: {lxml.__version__}")
    except ImportError:
        missing.append("lxml")
        print("  lxml: not installed (will use html.parser fallback)")

    if "requests" in missing or "beautifulsoup4" in missing:
        print(f"\nERROR: Missing required dependencies: {', '.join(missing)}")
        print(f"Install: pip install {' '.join(missing)}")
        sys.exit(1)

    return "lxml" not in missing


try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Install dependencies: pip install requests beautifulsoup4 lxml")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description=f"SEO Site Crawler v{__version__}")
    parser.add_argument("url", help="Starting URL to crawl")
    parser.add_argument("--max-pages", type=int, default=500, help="Max HTML pages to crawl")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between requests (seconds)")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout (seconds)")
    parser.add_argument("--output", default="/tmp/crawl_data.json", help="Output JSON file path")
    parser.add_argument("--check-external", action="store_true", help="Check external link status codes (HEAD)")
    parser.add_argument("--check-image-sizes", action="store_true", help="Check image file sizes via HEAD requests")
    parser.add_argument("--output-format", choices=["json", "summary"], default="json", help="Output format")
    parser.add_argument("--user-agent", default="claude-seo-pro/2.1 (SEO Audit Bot)", help="User agent string")
    return parser.parse_args()


def normalize_url(url, base_domain):
    """Normalize URL: remove fragment, ensure consistent format."""
    parsed = urlparse(url)
    if parsed.hostname != base_domain:
        return None
    path = parsed.path
    if not path:
        path = "/"
    url_clean = f"{parsed.scheme}://{parsed.hostname}{path}"
    if parsed.query:
        url_clean += f"?{parsed.query}"
    return url_clean


def fetch_sitemap(base_url, session, timeout):
    """Fetch and parse sitemap.xml, return list of URLs."""
    urls = set()
    sitemap_urls = [
        f"{base_url}/sitemap.xml",
        f"{base_url}/sitemap_index.xml",
        f"{base_url}/wp-sitemap.xml",
    ]
    for sitemap_url in sitemap_urls:
        try:
            resp = session.get(sitemap_url, timeout=timeout)
            if resp.status_code == 200 and "xml" in resp.headers.get("content-type", ""):
                soup = BeautifulSoup(resp.text, "lxml-xml")
                for sitemap in soup.find_all("sitemap"):
                    loc = sitemap.find("loc")
                    if loc:
                        try:
                            sub_resp = session.get(loc.text.strip(), timeout=timeout)
                            if sub_resp.status_code == 200:
                                sub_soup = BeautifulSoup(sub_resp.text, "lxml-xml")
                                for url_tag in sub_soup.find_all("url"):
                                    loc2 = url_tag.find("loc")
                                    if loc2:
                                        urls.add(loc2.text.strip())
                        except Exception:
                            pass
                for url_tag in soup.find_all("url"):
                    loc = url_tag.find("loc")
                    if loc:
                        urls.add(loc.text.strip())
        except Exception:
            pass
    return urls


def extract_page_data(url, resp, soup, base_domain):
    """Extract SEO-relevant data from a page."""
    html_content = resp.text
    html_size = len(resp.content)

    data = {
        "url": url,
        "status": resp.status_code,
        "ttfb_ms": int(resp.elapsed.total_seconds() * 1000),
        "content_type": resp.headers.get("content-type", ""),
        "html_size": html_size,
        "text_length": 0,
        "text_html_ratio": 0.0,
        "title": None,
        "description": None,
        "h1": None,
        "h1_all": [],
        "canonical": None,
        "canonical_in_body": False,
        "meta_robots": None,
        "word_count": 0,
        "og_title": None,
        "og_description": None,
        "og_image": None,
        "internal_links": [],
        "external_links": [],
        "images": [],
        "has_schema": False,
        "redirect_target": None,
    }

    if resp.history:
        data["redirect_target"] = resp.url
        data["status"] = resp.history[0].status_code

    # Title
    title_tag = soup.find("title")
    if title_tag:
        data["title"] = title_tag.get_text(strip=True)

    # Description
    desc_tag = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
    if desc_tag and desc_tag.get("content"):
        data["description"] = desc_tag["content"].strip()

    # H1 — filter out h1 inside code/pre/svg/template (v2.2 fix: false positives)
    EXCLUDE_PARENTS = {"code", "pre", "svg", "template", "script", "style"}
    h1_tags = [
        h for h in soup.find_all("h1")
        if not any(p.name in EXCLUDE_PARENTS for p in h.parents)
    ]
    data["h1_all"] = [h.get_text(strip=True) for h in h1_tags]
    if h1_tags:
        data["h1"] = h1_tags[0].get_text(strip=True)

    # Canonical — detect if placed in <body> instead of <head> (v2.2)
    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    if canonical_tag and canonical_tag.get("href"):
        data["canonical"] = canonical_tag["href"].strip()
        data["canonical_in_body"] = canonical_tag.find_parent("head") is None

    # Meta robots
    robots_tag = soup.find("meta", attrs={"name": re.compile(r"robots", re.I)})
    if robots_tag and robots_tag.get("content"):
        data["meta_robots"] = robots_tag["content"].strip()

    # OG tags (NEW v2.1)
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        data["og_title"] = og_title["content"].strip()

    og_desc = soup.find("meta", attrs={"property": "og:description"})
    if og_desc and og_desc.get("content"):
        data["og_description"] = og_desc["content"].strip()

    og_img = soup.find("meta", attrs={"property": "og:image"})
    if og_img and og_img.get("content"):
        data["og_image"] = og_img["content"].strip()

    # Word count + text/HTML ratio (v2.2: exclude script/style from denominator)
    body = soup.find("body")
    if body:
        # Remove script/style tags before extracting text
        body_copy = body.__copy__() if hasattr(body, '__copy__') else body
        for tag in body.find_all(["script", "style"]):
            tag.decompose()
        text = body.get_text(separator=" ", strip=True)
        text_length = len(text.encode("utf-8"))
        words = [w for w in text.split() if len(w) > 1]
        data["word_count"] = len(words)
        data["text_length"] = text_length
        # Use markup size excluding inline scripts/styles for fairer ratio
        markup_size = html_size
        for script in soup.find_all("script"):
            if script.string:
                markup_size -= len(script.string.encode("utf-8"))
        for style in soup.find_all("style"):
            if style.string:
                markup_size -= len(style.string.encode("utf-8"))
        if markup_size > 0:
            data["text_html_ratio"] = round(text_length / markup_size * 100, 1)

    # Links — with img alt and aria-label fallback for anchor text (v2.2 fix)
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        anchor = a_tag.get_text(strip=True)
        if not anchor:
            img = a_tag.find("img", alt=True)
            if img and img["alt"].strip():
                anchor = img["alt"].strip()
        if not anchor:
            anchor = a_tag.get("aria-label", "").strip()
        if not anchor:
            anchor = a_tag.get("title", "").strip()
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)

        if parsed.hostname == base_domain:
            data["internal_links"].append({"href": full_url, "anchor": anchor})
        elif parsed.scheme in ("http", "https"):
            data["external_links"].append({"href": full_url, "anchor": anchor})

    # Images
    for img_tag in soup.find_all("img"):
        src = img_tag.get("src", "")
        alt = img_tag.get("alt")
        if src:
            data["images"].append({
                "src": urljoin(url, src),
                "alt": alt,
                "has_alt_attr": "alt" in img_tag.attrs,
            })

    # Schema
    for script in soup.find_all("script", type="application/ld+json"):
        data["has_schema"] = True
        break

    return data


def check_external_links(pages, session, timeout):
    """Check status codes of external links via HEAD requests. Max 100 unique domains."""
    external_urls = set()
    for p in pages:
        for link in p.get("external_links", []):
            external_urls.add(link["href"])

    # Limit to 100 unique domains
    domain_urls = {}
    for url in external_urls:
        domain = urlparse(url).hostname
        if domain and domain not in domain_urls:
            domain_urls[domain] = url
        if len(domain_urls) >= 100:
            break

    results = []
    print(f"\nChecking {len(domain_urls)} external domains...")
    for i, (domain, url) in enumerate(domain_urls.items()):
        try:
            resp = session.head(url, timeout=timeout, allow_redirects=True)
            results.append({"url": url, "domain": domain, "status": resp.status_code})
        except requests.exceptions.Timeout:
            results.append({"url": url, "domain": domain, "status": "timeout"})
        except Exception as e:
            results.append({"url": url, "domain": domain, "status": f"error: {str(e)[:50]}"})

        if (i + 1) % 20 == 0:
            print(f"  Checked {i + 1}/{len(domain_urls)} external domains...")
        time.sleep(0.5)

    return results


def check_image_sizes(pages, session, timeout):
    """Check image file sizes via HEAD requests. Returns size tier distribution."""
    image_urls = set()
    for p in pages:
        for img in p.get("images", []):
            image_urls.add(img["src"])

    results = []
    print(f"\nChecking {len(image_urls)} image sizes...")
    for i, url in enumerate(image_urls):
        try:
            resp = session.head(url, timeout=timeout, allow_redirects=True)
            content_length = resp.headers.get("content-length")
            size_bytes = int(content_length) if content_length else None
            content_type = resp.headers.get("content-type", "")
            results.append({
                "url": url,
                "size_bytes": size_bytes,
                "content_type": content_type,
                "status": resp.status_code,
            })
        except Exception:
            results.append({"url": url, "size_bytes": None, "content_type": "", "status": "error"})

        if (i + 1) % 50 == 0:
            print(f"  Checked {i + 1}/{len(image_urls)} images...")
        time.sleep(0.3)

    # Categorize by size tiers
    tiers = {"optimal": 0, "acceptable": 0, "large": 0, "too_large": 0, "critical": 0, "unknown": 0}
    for img in results:
        s = img.get("size_bytes")
        if s is None:
            tiers["unknown"] += 1
        elif s < 50000:
            tiers["optimal"] += 1
        elif s < 100000:
            tiers["acceptable"] += 1
        elif s < 500000:
            tiers["large"] += 1
        elif s < 1000000:
            tiers["too_large"] += 1
        else:
            tiers["critical"] += 1

    return {"images": results, "tiers": tiers, "total": len(results)}


def crawl(args):
    """Main crawl loop."""
    parsed_start = urlparse(args.url)
    base_domain = parsed_start.hostname
    base_url = f"{parsed_start.scheme}://{base_domain}"

    session = requests.Session()
    session.headers.update({"User-Agent": args.user_agent})

    print(f"claude-seo-pro crawler v{__version__}")
    print(f"Crawling {base_url} (max {args.max_pages} pages)...")

    # Step 1: Discover URLs from sitemap
    sitemap_urls = fetch_sitemap(base_url, session, args.timeout)
    print(f"Found {len(sitemap_urls)} URLs in sitemap")

    # Step 2: BFS crawl
    to_visit = set()
    to_visit.add(base_url + "/")
    to_visit.update(sitemap_urls)

    visited = set()
    pages = []
    html_count = 0

    parser = "lxml" if check_dependencies() else "html.parser"

    while to_visit and html_count < args.max_pages:
        url = to_visit.pop()
        norm = normalize_url(url, base_domain)
        if not norm or norm in visited:
            continue
        visited.add(norm)

        try:
            resp = session.get(norm, timeout=args.timeout, allow_redirects=True)
            content_type = resp.headers.get("content-type", "")

            if "text/html" not in content_type:
                continue

            html_count += 1
            soup = BeautifulSoup(resp.text, parser)
            page_data = extract_page_data(norm, resp, soup, base_domain)
            pages.append(page_data)

            for link in page_data["internal_links"]:
                link_norm = normalize_url(link["href"], base_domain)
                if link_norm and link_norm not in visited:
                    to_visit.add(link_norm)

            if html_count % 10 == 0:
                print(f"  Crawled {html_count}/{args.max_pages} pages...")

            time.sleep(args.delay)

        except Exception as e:
            pages.append({
                "url": norm,
                "status": "fetch_error",
                "error": str(e),
            })

    print(f"\nCrawl complete: {html_count} HTML pages crawled")

    # Step 3: External link checks (v2.1)
    external_results = None
    if args.check_external:
        external_results = check_external_links(pages, session, args.timeout)

    # Step 4: Image size checks (v2.1)
    image_size_results = None
    if args.check_image_sizes:
        image_size_results = check_image_sizes(pages, session, args.timeout)

    # Step 5: Save results
    result = {
        "version": __version__,
        "domain": base_domain,
        "crawl_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pages_crawled": html_count,
        "total_urls_discovered": len(visited),
        "sitemap_urls": list(sitemap_urls),
        "pages": pages,
        "external_links": external_results,
        "image_sizes": image_size_results,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Results saved to {args.output}")
    return result


def analyze(result):
    """Analyze crawl data and print summary."""
    pages = result["pages"]
    html_pages = [p for p in pages if isinstance(p.get("status"), int) and p["status"] == 200]

    # --- Status distribution ---
    status_counts = defaultdict(int)
    for p in pages:
        status_counts[p.get("status", "unknown")] += 1

    print("\n=== HTTP Status Distribution ===")
    for status, count in sorted(status_counts.items(), key=lambda x: str(x[0])):
        print(f"  {status}: {count}")

    # --- Broken links ---
    broken = [p for p in pages if isinstance(p.get("status"), int) and p["status"] >= 400]
    print(f"\n=== Broken Pages (4xx/5xx): {len(broken)} ===")
    for p in broken[:10]:
        print(f"  {p['status']} {p['url']}")

    # --- Missing descriptions ---
    no_desc = [p for p in html_pages if not p.get("description")]
    total_html = max(len(html_pages), 1)
    print(f"\n=== Missing Description: {len(no_desc)}/{len(html_pages)} ({len(no_desc)*100//total_html}%) ===")

    # --- Duplicate titles ---
    titles = defaultdict(list)
    for p in html_pages:
        if p.get("title"):
            titles[p["title"]].append(p["url"])
    dup_titles = {t: urls for t, urls in titles.items() if len(urls) > 1}
    print(f"\n=== Duplicate Titles: {len(dup_titles)} groups ===")
    for title, urls in list(dup_titles.items())[:5]:
        print(f"  \"{title[:60]}\" — {len(urls)} pages")

    # --- Duplicate H1 ---
    h1s = defaultdict(list)
    for p in html_pages:
        if p.get("h1"):
            h1s[p["h1"]].append(p["url"])
    dup_h1 = {h: urls for h, urls in h1s.items() if len(urls) > 1}
    print(f"\n=== Duplicate H1: {len(dup_h1)} groups ===")

    # --- Empty anchors ---
    empty_anchors = 0
    for p in html_pages:
        for link in p.get("internal_links", []):
            if not link.get("anchor", "").strip():
                empty_anchors += 1
    print(f"\n=== Empty Anchor Links: {empty_anchors} ===")

    # --- Cyclic links ---
    cyclic = 0
    for p in html_pages:
        for link in p.get("internal_links", []):
            if link["href"].rstrip("/") == p["url"].rstrip("/"):
                cyclic += 1
    print(f"\n=== Cyclic Links: {cyclic} ===")

    # --- URL issues ---
    uppercase_urls = [p["url"] for p in pages if re.search(r"[A-Z]", urlparse(p["url"]).path)]
    print(f"\n=== URLs with Uppercase: {len(uppercase_urls)} ===")

    non_ascii = [p["url"] for p in pages if any(ord(c) > 127 for c in urlparse(p["url"]).path)]
    print(f"=== URLs with Non-ASCII: {len(non_ascii)} ===")

    # --- Text/HTML Ratio (NEW v2.1) ---
    low_ratio = [p for p in html_pages if p.get("text_html_ratio", 100) < 10]
    ratios = [p.get("text_html_ratio", 0) for p in html_pages if "text_html_ratio" in p]
    avg_ratio = sum(ratios) / max(len(ratios), 1)
    print(f"\n=== Text/HTML Ratio ===")
    print(f"  Average: {avg_ratio:.1f}%")
    print(f"  Pages below 10%: {len(low_ratio)}")

    # --- HTML Size (NEW v2.1) ---
    large_html = [p for p in html_pages if p.get("html_size", 0) > 200000]
    critical_html = [p for p in html_pages if p.get("html_size", 0) > 500000]
    print(f"\n=== HTML Document Size ===")
    print(f"  Pages > 200KB: {len(large_html)}")
    print(f"  Pages > 500KB: {len(critical_html)}")
    for p in sorted(large_html, key=lambda x: x.get("html_size", 0), reverse=True)[:5]:
        print(f"  {p.get('html_size', 0) // 1024}KB — {p['url']}")

    # --- Canonical validation (UPDATED v2.2) ---
    missing_canonical_all = [p for p in html_pages if not p.get("canonical")]
    missing_canonical_action = [
        p for p in missing_canonical_all
        if bool(urlparse(p["url"]).query)
        and "noindex" not in (p.get("meta_robots") or "").lower()
    ]
    canonical_in_body = [p for p in html_pages if p.get("canonical_in_body")]
    non_self_canonical = []
    for p in html_pages:
        if p.get("canonical") and p["canonical"].rstrip("/") != p["url"].rstrip("/"):
            non_self_canonical.append(p)
    print(f"\n=== Canonical Validation ===")
    print(f"  Missing canonical (total, INFO): {len(missing_canonical_all)}")
    print(f"  Missing canonical (actionable): {len(missing_canonical_action)}")
    if canonical_in_body:
        print(f"  Canonical in <body> (CRITICAL): {len(canonical_in_body)}")
        for p in canonical_in_body[:5]:
            print(f"    {p['url']}")
    print(f"  Non-self canonical: {len(non_self_canonical)}")
    for p in non_self_canonical[:5]:
        print(f"  {p['url']} → {p['canonical']}")

    # --- Orphan pages (NEW v2.1) ---
    sitemap_urls = set(result.get("sitemap_urls", []))
    inlink_targets = set()
    for p in html_pages:
        for link in p.get("internal_links", []):
            inlink_targets.add(link["href"].rstrip("/"))

    crawled_urls = {p["url"].rstrip("/") for p in html_pages}
    orphans = []
    for url in crawled_urls:
        if url not in inlink_targets:
            orphans.append(url)
    print(f"\n=== Orphan Pages (zero inlinks): {len(orphans)} ===")
    for o in orphans[:10]:
        print(f"  {o}")

    # --- Dead-end pages (NEW v2.1) ---
    dead_ends = [p for p in html_pages if len(p.get("internal_links", [])) == 0]
    print(f"\n=== Dead-End Pages (zero outlinks): {len(dead_ends)} ===")

    # --- OG tag coverage (NEW v2.1) ---
    has_all_og = [p for p in html_pages if p.get("og_title") and p.get("og_description") and p.get("og_image")]
    has_no_og = [p for p in html_pages if not p.get("og_title") and not p.get("og_description") and not p.get("og_image")]
    print(f"\n=== OG Tag Coverage ===")
    print(f"  All 3 OG tags: {len(has_all_og)}/{len(html_pages)} ({len(has_all_og)*100//total_html}%)")
    print(f"  No OG tags at all: {len(has_no_og)}/{len(html_pages)} ({len(has_no_og)*100//total_html}%)")

    # --- External link status (NEW v2.1) ---
    ext_data = result.get("external_links")
    if ext_data:
        ext_status = defaultdict(int)
        for e in ext_data:
            ext_status[e.get("status", "unknown")] += 1
        print(f"\n=== External Link Status ({len(ext_data)} domains) ===")
        for status, count in sorted(ext_status.items(), key=lambda x: str(x[0])):
            print(f"  {status}: {count}")
        broken_ext = [e for e in ext_data if isinstance(e.get("status"), int) and e["status"] >= 400 and e["status"] not in (403, 498, 499)]
        print(f"  Broken (excluding bot-blocks): {len(broken_ext)}")

    # --- Image sizes (NEW v2.1) ---
    img_data = result.get("image_sizes")
    if img_data:
        tiers = img_data["tiers"]
        print(f"\n=== Image Size Distribution ({img_data['total']} images) ===")
        print(f"  Optimal (<50KB): {tiers['optimal']}")
        print(f"  Acceptable (50-100KB): {tiers['acceptable']}")
        print(f"  Large (100-500KB): {tiers['large']}")
        print(f"  Too large (500KB-1MB): {tiers['too_large']}")
        print(f"  Critical (>1MB): {tiers['critical']}")
        print(f"  Unknown: {tiers['unknown']}")

    # --- TTFB distribution (NEW v2.1) ---
    ttfb_values = [p.get("ttfb_ms", 0) for p in html_pages if "ttfb_ms" in p]
    if ttfb_values:
        ttfb_values.sort()
        median_idx = len(ttfb_values) // 2
        median_ttfb = ttfb_values[median_idx]
        fast = len([t for t in ttfb_values if t < 500])
        medium = len([t for t in ttfb_values if 500 <= t < 1000])
        slow = len([t for t in ttfb_values if 1000 <= t < 2000])
        critical = len([t for t in ttfb_values if t >= 2000])
        print(f"\n=== TTFB Distribution (uncached) ===")
        print(f"  Median: {median_ttfb}ms")
        print(f"  <500ms: {fast}  |  500-1000ms: {medium}  |  1-2s: {slow}  |  >2s: {critical}")

    print("\n=== Analysis Complete ===")


if __name__ == "__main__":
    print(f"claude-seo-pro crawler v{__version__}")
    print("Checking dependencies...")
    has_lxml = check_dependencies()
    print()

    args = parse_args()
    result = crawl(args)
    analyze(result)
