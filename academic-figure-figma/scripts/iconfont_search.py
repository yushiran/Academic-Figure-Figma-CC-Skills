#!/usr/bin/env python3
"""Search iconfont.cn and emit ready-to-use SVG strings. No login required."""
import json, sys, time, urllib.request, urllib.parse, re

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

def search(q, n=8):
    qs = urllib.parse.urlencode({"q": q, "sortType": "updated_at", "page": 1,
                                 "pageSize": n, "fromCollection": -1,
                                 "t": int(time.time() * 1000)})
    req = urllib.request.Request(
        f"https://www.iconfont.cn/api/icon/search.json?{qs}", data=b"",
        headers={"User-Agent": UA, "X-Requested-With": "XMLHttpRequest",
                 "Referer": f"https://www.iconfont.cn/search/index?searchType=icon&q={urllib.parse.quote(q)}"})
    d = json.loads(urllib.request.urlopen(req, timeout=25).read())
    return d.get("data", {}).get("icons", [])

def to_svg(icon, colour="#000000"):
    w, h = icon.get("width", 1024), icon.get("height", 1024)
    body = icon.get("show_svg") or ""
    if body:                                     # full markup already provided
        body = re.sub(r'</?svg[^>]*>', '', body)
    else:                                        # build from path data
        body = "".join(f'<path d="{p}"/>' for p in
                       ([icon["path_a"]] if isinstance(icon.get("path_a"), str) else icon.get("path_a", [])))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="{colour}">{body}</svg>'

if __name__ == "__main__":
    for ic in search(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8):
        svg = to_svg(ic)
        print(f'{ic["id"]}\t{ic["name"][:34]:<34}\t{len(svg)}B')
