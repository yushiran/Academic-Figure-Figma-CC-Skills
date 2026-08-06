#!/usr/bin/env python3
"""Search iconfont.cn and emit ready-to-use SVG strings. No login required.

The JSON search API answers only to this exact shape: POST with the query in the
URL query string (not the form body) plus an X-Requested-With header. GET returns
an HTML shell; POST with body-only params returns {"code":500,"have_no_query"}.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


def search(query, page_size=8):
    """Return the icon list for `query` (Chinese or English both work)."""
    params = urllib.parse.urlencode({
        "q": query, "sortType": "updated_at", "page": 1,
        "pageSize": page_size, "fromCollection": -1,
        "t": int(time.time() * 1000),
    })
    referer = ("https://www.iconfont.cn/search/index?searchType=icon&q="
               + urllib.parse.quote(query))
    request = urllib.request.Request(
        f"https://www.iconfont.cn/api/icon/search.json?{params}", data=b"",
        headers={"User-Agent": USER_AGENT,
                 "X-Requested-With": "XMLHttpRequest",
                 "Referer": referer})
    with urllib.request.urlopen(request, timeout=25) as response:
        payload = json.loads(response.read())
    return payload.get("data", {}).get("icons", [])


def to_svg(icon, colour="#000000"):
    """Assemble an injectable SVG string from one search-result entry."""
    width = icon.get("width", 1024)
    height = icon.get("height", 1024)
    body = icon.get("show_svg") or ""
    if body:
        body = re.sub(r"</?svg[^>]*>", "", body)
    else:
        paths = icon.get("path_a", [])
        if isinstance(paths, str):
            paths = [paths]
        body = "".join(f'<path d="{p}"/>' for p in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {width} {height}" fill="{colour}">{body}</svg>')


def main():
    """CLI: search <query> [page_size] and print id, name, svg size."""
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    for entry in search(sys.argv[1], limit):
        svg = to_svg(entry)
        print(f'{entry["id"]}\t{entry["name"][:34]:<34}\t{len(svg)}B')


if __name__ == "__main__":
    main()
