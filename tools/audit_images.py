"""
Image audit for the Travel Recommendation page.
Run from the project root:   python tools/audit_images.py
Outputs: console report (duplicates, HTTP status) + tools/image_audit.html (contact sheet:
province name next to the photo it will display) so the mapping can be checked by eye in a minute.
"""
import html
import urllib.request
from collections import defaultdict
from src.components.recommendations import DESTINATION_CATALOG


def status(url: str) -> str:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return f"{r.status} {r.headers.get('Content-Type', '')}"
    except Exception as e:  # noqa: BLE001
        return f"ERROR {e}"


def main() -> None:
    owners = defaultdict(list)
    for name, m in DESTINATION_CATALOG.items():
        owners[m["image_url"]].append(name)

    print("== Duplicate URLs (one photo cannot represent two provinces) ==")
    dup = {u: n for u, n in owners.items() if len(n) > 1}
    for u, n in dup.items():
        print(f"  {', '.join(n)}  ->  {u}")
    if not dup:
        print("  none")

    print("\n== HTTP status ==")
    cells = []
    for name, m in DESTINATION_CATALOG.items():
        st = status(m["image_url"])
        flag = "DUPLICATE" if m["image_url"] in dup else ""
        print(f"  {name:<22} {st[:40]:<40} {flag}")
        cells.append(
            f"<figure><img src='{html.escape(m['image_url'])}' loading='lazy'>"
            f"<figcaption><b>{html.escape(name)}</b> ({html.escape(m['en_name'])})<br>{html.escape(st[:30])} {flag}"
            f"<br><small>{html.escape(m['attractions'][0])}</small></figcaption></figure>"
        )
    page = (
        "<meta charset='utf-8'><title>Image audit</title><style>"
        "body{font-family:sans-serif;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;padding:14px}"
        "figure{margin:0;border:1px solid #ddd;border-radius:10px;overflow:hidden}"
        "img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block;background:#eee}"
        "figcaption{padding:8px;font-size:13px}</style>" + "".join(cells)
    )
    with open("tools/image_audit.html", "w", encoding="utf-8") as f:
        f.write(page)
    print("\nWrote tools/image_audit.html - open it and check each photo matches its province.")


if __name__ == "__main__":
    main()
