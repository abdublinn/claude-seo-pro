#!/usr/bin/env python3
"""
Page fetcher for SEO analysis — returns page HTML with status code and headers.
"""

import argparse
import json
import sys

try:
    import requests
except ImportError:
    print("ERROR: pip install requests")
    sys.exit(1)


def fetch(url, timeout=10, user_agent="claude-seo-pro/2.0"):
    """Fetch a URL and return status, headers, and HTML."""
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": user_agent}, allow_redirects=True)
        result = {
            "url": url,
            "final_url": resp.url,
            "status": resp.status_code,
            "ttfb_ms": int(resp.elapsed.total_seconds() * 1000),
            "headers": dict(resp.headers),
            "redirects": [{"url": r.url, "status": r.status_code} for r in resp.history],
            "html": resp.text[:500000],  # Cap at 500KB
        }
        return result
    except Exception as e:
        return {"url": url, "error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    result = fetch(args.url, args.timeout)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Status: {result.get('status', 'error')}")
        print(f"TTFB: {result.get('ttfb_ms', 'N/A')}ms")
        if result.get("redirects"):
            print(f"Redirects: {' → '.join(r['url'] for r in result['redirects'])}")
        if result.get("error"):
            print(f"Error: {result['error']}")
