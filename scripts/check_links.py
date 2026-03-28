#!/usr/bin/env python3
"""
Link health analyzer for SEO — claude-seo-pro v2.1
Analyzes crawl data to report:
- Broken internal links with inlink counts
- Internal links to redirects
- Empty anchors and cyclic links
- Orphan pages (zero inlinks)
- Dead-end pages (zero outlinks)
- Canonical validation (missing, non-self, broken targets, chains)
- Redirect chain depth analysis
- External link status summary
- PageRank flow score
"""

import argparse
import json
import sys
from collections import defaultdict
from urllib.parse import urlparse

__version__ = "2.1.0"


def _normalize(url):
    """Normalize URL for comparison."""
    return url.rstrip("/") if url else ""


def _trace_redirect_chain(url, url_redirects, max_depth=10):
    """Trace a redirect chain and return the full path + final destination."""
    chain = [url]
    current = _normalize(url)
    for _ in range(max_depth):
        target = url_redirects.get(current)
        if not target or _normalize(target) == current:
            break
        chain.append(target)
        current = _normalize(target)
    return chain


def _trace_canonical_chain(url, url_canonicals, max_depth=5):
    """Trace canonical chain: page A canonical→B canonical→C."""
    chain = [url]
    current = _normalize(url)
    visited = {current}
    for _ in range(max_depth):
        canonical = url_canonicals.get(current)
        if not canonical:
            break
        canonical_norm = _normalize(canonical)
        if canonical_norm in visited or canonical_norm == current:
            break
        chain.append(canonical)
        visited.add(canonical_norm)
        current = canonical_norm
    return chain


def check_links(crawl_file, timeout=10):
    """Load crawl data and analyze link health."""
    with open(crawl_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    pages = data["pages"]
    html_pages = [p for p in pages if isinstance(p.get("status"), int) and p["status"] == 200]

    # Build inlink map: target_url -> list of source_urls
    inlinks = defaultdict(list)
    all_internal_targets = set()

    for page in pages:
        if not isinstance(page.get("status"), int):
            continue
        source = page["url"]
        for link in page.get("internal_links", []):
            target = _normalize(link["href"])
            inlinks[target].append({
                "source": source,
                "anchor": link.get("anchor", ""),
            })
            all_internal_targets.add(link["href"])

    # Map of URL -> status and redirects
    url_status = {}
    url_redirects = {}
    url_canonicals = {}
    for page in pages:
        norm = _normalize(page["url"])
        url_status[norm] = page.get("status", "unknown")
        if page.get("redirect_target"):
            url_redirects[norm] = page["redirect_target"]
        if page.get("canonical"):
            url_canonicals[norm] = page["canonical"]

    # === Broken targets ===
    broken = []
    for target in all_internal_targets:
        target_norm = _normalize(target)
        status = url_status.get(target_norm)
        if isinstance(status, int) and status >= 400:
            broken.append({
                "url": target,
                "status": status,
                "inlink_count": len(inlinks.get(target_norm, [])),
                "sources": [s["source"] for s in inlinks.get(target_norm, [])][:5],
            })

    # === Redirect targets ===
    redirects = []
    for target in all_internal_targets:
        target_norm = _normalize(target)
        status = url_status.get(target_norm)
        if isinstance(status, int) and 300 <= status < 400:
            chain = _trace_redirect_chain(target_norm, url_redirects)
            redirects.append({
                "url": target,
                "status": status,
                "inlink_count": len(inlinks.get(target_norm, [])),
                "chain": chain,
                "chain_length": len(chain) - 1,
                "final_destination": chain[-1],
            })

    broken.sort(key=lambda x: x["inlink_count"], reverse=True)
    redirects.sort(key=lambda x: x["inlink_count"], reverse=True)

    # Output: broken
    print(f"=== Broken Internal Links: {len(broken)} ===")
    for b in broken:
        print(f"  [{b['status']}] {b['url']} — {b['inlink_count']} inlinks")
        for src in b["sources"][:3]:
            print(f"    ← {src}")

    # Output: redirects with chain depth
    print(f"\n=== Internal Links to Redirects: {len(redirects)} ===")
    chains_gt1 = [r for r in redirects if r["chain_length"] > 1]
    print(f"  Redirect chains (>1 hop): {len(chains_gt1)}")
    for r in redirects[:20]:
        chain_str = " → ".join(r["chain"][:4])
        if len(r["chain"]) > 4:
            chain_str += " → ..."
        print(f"  [{r['status']}] {r['url']} — {r['inlink_count']} inlinks — chain({r['chain_length']}): {chain_str}")

    # === Empty anchors ===
    empty_anchor_count = 0
    pages_with_empty = defaultdict(int)
    for page in pages:
        for link in page.get("internal_links", []):
            if not link.get("anchor", "").strip():
                empty_anchor_count += 1
                pages_with_empty[page["url"]] += 1

    print(f"\n=== Empty Anchor Links: {empty_anchor_count} ===")
    top_empty = sorted(pages_with_empty.items(), key=lambda x: x[1], reverse=True)[:10]
    for url, count in top_empty:
        print(f"  {url} — {count} empty anchors")

    # === Cyclic links ===
    cyclic_count = 0
    for page in pages:
        for link in page.get("internal_links", []):
            if _normalize(link["href"]) == _normalize(page["url"]):
                cyclic_count += 1
    print(f"\n=== Cyclic Links: {cyclic_count} ===")

    # === Orphan pages (NEW v2.1) ===
    crawled_urls = {_normalize(p["url"]) for p in html_pages}
    inlink_target_set = set(inlinks.keys())
    orphans = [url for url in crawled_urls if url not in inlink_target_set]
    print(f"\n=== Orphan Pages (zero inlinks): {len(orphans)} ===")
    for o in orphans[:10]:
        print(f"  {o}")

    # === Dead-end pages (NEW v2.1) ===
    dead_ends = [p["url"] for p in html_pages if len(p.get("internal_links", [])) == 0]
    print(f"\n=== Dead-End Pages (zero outlinks): {len(dead_ends)} ===")
    for d in dead_ends[:10]:
        print(f"  {d}")

    # === Canonical validation (NEW v2.1) ===
    missing_canonical = [p["url"] for p in html_pages if not p.get("canonical")]
    self_canonical = []
    non_self_canonical = []
    broken_canonical_targets = []
    canonical_chains = []

    for p in html_pages:
        canonical = p.get("canonical")
        if not canonical:
            continue
        if _normalize(canonical) == _normalize(p["url"]):
            self_canonical.append(p["url"])
        else:
            non_self_canonical.append({"url": p["url"], "canonical": canonical})
            # Check if canonical target returns 200
            target_status = url_status.get(_normalize(canonical))
            if target_status and isinstance(target_status, int) and target_status != 200:
                broken_canonical_targets.append({
                    "url": p["url"],
                    "canonical": canonical,
                    "target_status": target_status,
                })

    # Canonical chains
    for p in html_pages:
        if p.get("canonical"):
            chain = _trace_canonical_chain(p["url"], url_canonicals)
            if len(chain) > 2:
                canonical_chains.append(chain)

    print(f"\n=== Canonical Validation ===")
    print(f"  Self-referencing (correct): {len(self_canonical)}")
    print(f"  Missing canonical: {len(missing_canonical)}")
    print(f"  Non-self canonical: {len(non_self_canonical)}")
    for ns in non_self_canonical[:5]:
        print(f"    {ns['url']} → {ns['canonical']}")
    print(f"  Broken canonical targets: {len(broken_canonical_targets)}")
    for bc in broken_canonical_targets:
        print(f"    {bc['url']} → {bc['canonical']} (status {bc['target_status']})")
    print(f"  Canonical chains: {len(canonical_chains)}")
    for chain in canonical_chains[:5]:
        print(f"    {' → '.join(chain)}")

    # === External link summary (NEW v2.1) ===
    all_external = set()
    external_domains = defaultdict(int)
    for page in pages:
        for link in page.get("external_links", []):
            all_external.add(link["href"])
            domain = urlparse(link["href"]).hostname
            if domain:
                external_domains[domain] += 1

    print(f"\n=== External Links Summary ===")
    print(f"  Total unique external URLs: {len(all_external)}")
    print(f"  Unique external domains: {len(external_domains)}")
    top_domains = sorted(external_domains.items(), key=lambda x: x[1], reverse=True)[:10]
    for domain, count in top_domains:
        print(f"    {domain}: {count} links")

    # === PageRank flow score (NEW v2.1) ===
    links_through_redirects = 0
    for page in pages:
        for link in page.get("internal_links", []):
            target_norm = _normalize(link["href"])
            status = url_status.get(target_norm)
            if isinstance(status, int) and 300 <= status < 400:
                links_through_redirects += 1

    pr_loss_pct = round(links_through_redirects * 0.15, 1)
    print(f"\n=== PageRank Flow ===")
    print(f"  Internal links through redirects: {links_through_redirects}")
    print(f"  Estimated PageRank loss: ~{pr_loss_pct}% of internal link equity")
    print(f"  Orphan pages (PageRank sinks): {len(orphans)}")
    print(f"  Dead-end pages (PageRank sinks): {len(dead_ends)}")

    print("\n=== Analysis Complete ===")

    return {
        "broken": broken,
        "redirects": redirects,
        "redirect_chains_gt1": len(chains_gt1),
        "empty_anchors": empty_anchor_count,
        "cyclic_links": cyclic_count,
        "orphans": orphans,
        "dead_ends": dead_ends,
        "missing_canonical": len(missing_canonical),
        "non_self_canonical": non_self_canonical,
        "broken_canonical_targets": broken_canonical_targets,
        "canonical_chains": canonical_chains,
        "external_domains": len(external_domains),
        "links_through_redirects": links_through_redirects,
        "pr_loss_pct": pr_loss_pct,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Link Health Analyzer v{__version__}")
    parser.add_argument("crawl_file", help="Path to crawl_data.json")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args()
    check_links(args.crawl_file, args.timeout)
