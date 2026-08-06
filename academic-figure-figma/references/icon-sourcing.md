# Sourcing icons and logos as true vectors

Priority order, by icon type:

| Need | Source | How | Notes |
|---|---|---|---|
| Concept icon (mic, map pin, waveform, file, list...) | **Lucide** | `https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/<name>.svg` | Uniform 2px stroke — a whole figure stays visually consistent. First choice for papers. |
| AI model / vendor logo | **lobe-icons** | `https://raw.githubusercontent.com/lobehub/lobe-icons/master/packages/static-svg/icons/<name>.svg` | Qwen, OpenAI, Gemini, Claude, HuggingFace, Whisper... Correct marks. |
| General brand | **simpleicons** | `https://cdn.simpleicons.org/<name>` | 3000+ brands but MUST verify by eye — its "qwen" entry is a different mark entirely. |
| Chinese-context concept icon | **iconfont.cn** | search API, see below | Largest pool; mixed authorship = mixed style, prefer one author's set per figure. |
| Whole icon set the user already curated | iconfont project JS bundle | `https://at.alicdn.com/t/font_XXXX.js` — parse `<symbol>` entries | User creates the project in the browser and pastes the URL. |

## iconfont search API (no login required)

The web search works without login; the JSON API needs exactly this shape —
POST with the query in the **URL query string** (not the body) plus an
`X-Requested-With` header. GET returns an HTML shell; POST with form-body params
returns `have_no_query`.

```
POST https://www.iconfont.cn/api/icon/search.json?q=<query>&sortType=updated_at&page=1&pageSize=8&fromCollection=-1&t=<ms>
Headers: User-Agent: <browser UA>, X-Requested-With: XMLHttpRequest,
         Referer: https://www.iconfont.cn/search/index?searchType=icon&q=<query>
```

Response `data.icons[]` carries `path_a` (the SVG path data directly — no file download
needed), `width`/`height` (usually 1024), `show_svg`. Chinese and English queries both
work. `scripts/iconfont_search.py` wraps this: search + assemble ready-to-inject SVG.

## Cleaning fetched SVG

- Strip standalone `width=`/`height=` attributes so viewBox controls scaling — but the
  regex must not eat `stroke-width`: use `(?<![\w-])(width|height)="[^"]*"`.
  (A naive `\s*(width|height)=` regex once truncated `stroke-width` to `stroke-` and
  broke every Lucide icon.)
- Replace `fill="currentColor"` / `stroke="currentColor"` with the target hex before
  injection; Figma does not resolve currentColor.
- Remove `style="..."` blocks; keep `stroke-linecap`/`stroke-linejoin`.

## Injecting into Figma

```js
const node = figma.createNodeFromSvg(svgString);  // true vector paths
node.name = "icon/waveform";
parent.appendChild(node);
node.rescale(targetPt / node.width);              // rescale, never resize (keeps stroke ratio)
node.x = ...; node.y = ...;
```

Result is editable VECTOR nodes — recolourable, scalable without loss.

## Verification is mandatory

After placing any brand logo, screenshot it (`await node.screenshot({scale: 4})`) and
confirm it is the real mark. Never trust the CDN filename. Real failure: simpleicons'
`qwen` renders a hexagon-star that is not Alibaba's Qwen logo; lobe-icons' `qwen.svg`
is the correct interlocked mark.

## Usage etiquette for papers

Identifying a model/tool with its logo in an academic figure is standard fair use.
Do not distort the mark's shape or recolour a brand logo (resizing is fine).
Concept icons (Lucide MIT, Material Apache-2.0) are unrestricted; iconfont icons keep
their per-author licences — check before redistribution beyond the paper.
