"""
Find and add FREELY LICENSED province photos from Wikimedia Commons.
Run from the project root (needs internet):

  python tools/commons_images.py search "Wat Phumin Nan"
  python tools/commons_images.py pick "File:Wat Phumin.jpg"

search : lists candidate files with licence + author. Only licences that allow reuse
         (CC0, Public Domain, CC BY, CC BY-SA) are marked USABLE; NC/ND/unknown are refused.
pick   : prints the image_url and image_credit lines to paste into the province entry in
         DESTINATION_CATALOG (src/components/recommendations.py). Nothing is downloaded.

Set COMMONS_UA to a descriptive User-Agent with your contact (Wikimedia policy), e.g.
  set COMMONS_UA="TourismDashboard/1.0 (you@example.com)"
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from html import unescape

API = "https://commons.wikimedia.org/w/api.php"
UA = os.environ.get("COMMONS_UA", "TourismDashboard/1.0 (please-set-COMMONS_UA)")
ALLOWED = re.compile(r"^(CC0|Public domain|PD\b|CC BY(-SA)?\b)", re.I)
BLOCKED = re.compile(r"-N[CD]\b", re.I)


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def _api(**params) -> dict:
    params.update(format="json", prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=1000)
    return json.loads(_get(API + "?" + urllib.parse.urlencode(params)))


def _meta(info: dict, key: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", (info.get("extmetadata", {}).get(key, {}) or {}).get("value", ""))).strip()


def parse_page(page: dict) -> dict:
    """Normalise one Commons page into title/author/licence/urls and a USABLE flag."""
    info = (page.get("imageinfo") or [{}])[0]
    lic = _meta(info, "LicenseShortName")
    usable = bool(ALLOWED.match(lic)) and not BLOCKED.search(lic)
    return {
        "title": page.get("title", ""),
        "author": _meta(info, "Artist") or "Unknown author",
        "license": lic or "Unknown",
        "license_url": _meta(info, "LicenseUrl"),
        "source_url": info.get("descriptionurl", ""),
        "thumb_url": info.get("thumburl") or info.get("url", ""),
        "width": info.get("width", 0),
        "usable": usable,
    }


def cmd_search(query: str, limit: int) -> None:
    data = _api(action="query", generator="search", gsrnamespace=6, gsrsearch=query, gsrlimit=limit)
    pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0))
    if not pages:
        print("No results. Try an English or more specific query.")
    for i, page in enumerate(pages, 1):
        m = parse_page(page)
        flag = "USABLE" if m["usable"] else "REFUSED"
        print(f"{i:>2}. [{flag}] {m['title']}\n    {m['license']} | {m['author'][:60]} | {m['width']}px\n    {m['source_url']}")


def cmd_pick(title: str) -> None:
    if not title.startswith("File:"):
        title = "File:" + title
    data = _api(action="query", titles=title)
    pages = list(data.get("query", {}).get("pages", {}).values())
    if not pages or "imageinfo" not in pages[0]:
        sys.exit(f"File not found on Commons: {title}")
    m = parse_page(pages[0])
    if not m["usable"]:
        sys.exit(f"Refused: licence '{m['license']}' does not clearly allow reuse (need CC0 / PD / CC BY / CC BY-SA).")
    print("Paste these two lines into the province entry in DESTINATION_CATALOG (src/components/recommendations.py):\n")
    print(f'        "image_url": "{m["thumb_url"]}",')
    print(f'        "image_credit": "{m["author"]} / {m["license"]} (Wikimedia Commons)",')
    print(f"\nSource page: {m['source_url']}\nOpen the image link and confirm it really shows this province.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--limit", type=int, default=10)
    a = sub.add_parser("pick"); a.add_argument("title")
    args = ap.parse_args()
    cmd_search(args.query, args.limit) if args.cmd == "search" else cmd_pick(args.title)


if __name__ == "__main__":
    main()