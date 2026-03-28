#!/usr/bin/env python3
"""
HTML parser for SEO analysis — extracts meta tags, headings, links, images, schema.
"""

import argparse
import json
import re
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: pip install beautifulsoup4 lxml")
    sys.exit(1)


def parse_html(html, url=""):
    """Parse HTML and extract SEO-relevant data."""
    soup = BeautifulSoup(html, "lxml")

    # Title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else None

    # Description
    desc_tag = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else None

    # H1
    h1_tags = soup.find_all("h1")
    h1_list = [h.get_text(strip=True) for h in h1_tags]

    # All headings
    headings = {}
    for level in range(1, 7):
        tags = soup.find_all(f"h{level}")
        headings[f"h{level}"] = [t.get_text(strip=True) for t in tags]

    # Canonical
    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    canonical = canonical_tag["href"].strip() if canonical_tag and canonical_tag.get("href") else None

    # Meta robots
    robots_tag = soup.find("meta", attrs={"name": re.compile(r"robots", re.I)})
    meta_robots = robots_tag["content"].strip() if robots_tag and robots_tag.get("content") else None

    # OG tags
    og_tags = {}
    for meta in soup.find_all("meta", attrs={"property": re.compile(r"^og:")}):
        og_tags[meta["property"]] = meta.get("content", "")

    # Schema (JSON-LD)
    schemas = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            schemas.append(json.loads(script.string))
        except (json.JSONDecodeError, TypeError):
            schemas.append({"error": "invalid JSON-LD"})

    # Word count
    body = soup.find("body")
    word_count = 0
    if body:
        text = body.get_text(separator=" ", strip=True)
        words = [w for w in text.split() if len(w) > 1]
        word_count = len(words)

    # Links
    internal_links = []
    external_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        anchor = a.get_text(strip=True)
        link_data = {"href": href, "anchor": anchor}
        if href.startswith(("http://", "https://")) and url:
            from urllib.parse import urlparse
            if urlparse(href).hostname == urlparse(url).hostname:
                internal_links.append(link_data)
            else:
                external_links.append(link_data)
        elif href.startswith("/"):
            internal_links.append(link_data)
        elif not href.startswith(("#", "mailto:", "tel:", "javascript:")):
            external_links.append(link_data)

    # Images
    images = []
    for img in soup.find_all("img"):
        images.append({
            "src": img.get("src", ""),
            "alt": img.get("alt"),
            "has_alt_attr": "alt" in img.attrs,
            "width": img.get("width"),
            "height": img.get("height"),
            "loading": img.get("loading"),
            "srcset": bool(img.get("srcset")),
            "fetchpriority": img.get("fetchpriority"),
            "decoding": img.get("decoding"),
        })

    result = {
        "title": title,
        "title_length": len(title) if title else 0,
        "description": description,
        "description_length": len(description) if description else 0,
        "h1": h1_list,
        "headings": headings,
        "canonical": canonical,
        "meta_robots": meta_robots,
        "og_tags": og_tags,
        "schemas": schemas,
        "word_count": word_count,
        "internal_links_count": len(internal_links),
        "external_links_count": len(external_links),
        "images_count": len(images),
        "images_without_alt": sum(1 for img in images if not img["has_alt_attr"]),
        "images_empty_alt": sum(1 for img in images if img["has_alt_attr"] and img["alt"] == ""),
        "images_with_lazy": sum(1 for img in images if img["loading"] == "lazy"),
        "images_with_srcset": sum(1 for img in images if img["srcset"]),
        "images_with_dimensions": sum(1 for img in images if img["width"] and img["height"]),
    }

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="HTML file to parse (or - for stdin)")
    parser.add_argument("--url", default="", help="Base URL for link classification")
    args = parser.parse_args()

    if args.file == "-":
        html = sys.stdin.read()
    else:
        with open(args.file, "r", encoding="utf-8") as f:
            html = f.read()

    result = parse_html(html, args.url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
