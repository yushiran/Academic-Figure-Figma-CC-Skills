<p align="center">
  <img src="Logo.png" width="180" alt="Academic-Figure-Figma-CC-Skills logo">
</p>

<h1 align="center">Academic-Figure-Figma-CC-Skills</h1>

<p align="center">
  <b>The last mile of the academic figure toolchain.</b><br>
  <b>学术绘图工具链的最后一公里。</b>
</p>

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

---

<a id="english"></a>

## English

Upstream tools (ChatGPT figure pipelines such as
[paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro),
[PaperBanana](https://github.com/llmsresearch/paperbanana)) generate raster *candidate*
figures — good for exploring layout, impossible to hand-tune. This skill lets
**Claude Code drive Figma directly through the official Figma MCP server** and land the
final, **editable, paper-exact vector figure**: true print dimensions (IEEE / Elsevier /
AAAI), true vector icons, fonts and terminology aligned with the paper source.

```
candidate images (raster, explore)   ──▶   this skill (Figma MCP, converge)
studio-pro C01-C04 / PaperBanana           editable vectors at print size
```

### Features

- **Correctness first** — audits every number, term, and metric label against the paper
  source before drawing; a figure-grammar contract (arrow evidence, no false relays,
  variables on edges, centred mainline) distilled from studio-pro's prompt contracts.
- **Paper-exact canvases** — IEEEtran 252/516 pt, elsarticle ≈390 pt, AAAI 239/504 pt,
  6 pt font floor, Tinos as the Times substitute inside Figma.
- **True-vector icons** — Lucide / lobe-icons / simpleicons / iconfont.cn (login-free
  search API cracked, `scripts/iconfont_search.py`), injected via `createNodeFromSvg`.
- **Quota-aware** — documents the Figma MCP seat/quota traps (View seat = 6 calls/month
  on any plan; free Education plan = Professional + Full seat = 200 calls/day).

### Quick start

```bash
git clone https://github.com/yushiran/Academic-Figure-Figma-CC-Skills.git
cp -r Academic-Figure-Figma-CC-Skills/academic-figure-figma ~/.claude/skills/
claude plugin install figma@claude-plugins-official   # then OAuth, see references/figma-mcp-setup.md
```

Then just ask Claude Code: *"Rebuild this framework figure in Figma at IEEE
double-column width."*

### Repository layout

```
academic-figure-figma/
├── SKILL.md                          # hard rules + 5-step workflow
├── references/
│   ├── figma-mcp-setup.md            # connection, OAuth on remote sessions, seats & quota
│   ├── paper-canvas-specs.md         # print widths, font floors, fonts
│   ├── figure-grammar.md             # what a good framework figure must obey
│   ├── icon-sourcing.md              # vector icon/logo sourcing & verification
│   └── build-workflow.md             # incremental build, arrows, balancing, pitfalls
└── scripts/
    └── iconfont_search.py            # iconfont.cn search → injectable SVG
```

### Roadmap

- **v0.2 — fewer round trips**: battle-tested Figma JS snippet library + local verified
  icon cache, so one `use_figma` call builds a whole stage.
- **v0.3 — spec compiler**: declarative `figure.spec.json` → local SVG preview
  (zero-quota iteration) → one-shot Figma build.
- **v0.4 — auto layout**: ELK/dagre layout for graph-shaped figures; reusable figure
  templates (pipeline, two-panel train/infer, encoder-decoder).

### Acknowledgements

[paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro)
(figure-grammar rules distilled from its S1/S4 prompt contracts) ·
[PaperBanana](https://github.com/llmsresearch/paperbanana) ·
[academic-figure-generator](https://github.com/LigphiDonk/academic-figure-generator) ·
Figma official MCP plugin.

---

<a id="中文"></a>

## 中文

上游工具（[paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro)、
[PaperBanana](https://github.com/llmsresearch/paperbanana) 等 ChatGPT 生图管线）负责生成
栅格**候选图**——适合探索构图，但无法手工微调。本技能让 **Claude Code 通过官方 Figma MCP
直接操作画布**，落成最终的**可编辑、论文精确尺寸的矢量成稿**：真实印刷宽度（IEEE / Elsevier /
AAAI）、真矢量图标、字体与术语和论文源对齐。

```
候选图（栅格, 发散探索）   ──▶   本技能（Figma MCP, 收敛定稿）
studio-pro C01-C04 等              印刷尺寸的可编辑矢量
```

### 特性

- **正确性先行** — 画前逐项核对论文中的数字、术语、指标名；内置从 studio-pro prompt 契约
  提炼的图语法规范（箭头双端证据、禁虚假中继、变量上线不占框、主线居中）。
- **论文精确画布** — IEEEtran 252/516 pt、elsarticle ≈390 pt、AAAI 239/504 pt，
  6 pt 字号底线，Figma 内用 Tinos 替代 Times。
- **真矢量图标** — Lucide / lobe-icons / simpleicons / iconfont.cn（免登录搜索 API 已打通，
  `scripts/iconfont_search.py`），经 `createNodeFromSvg` 注入。
- **额度意识** — 记录 Figma MCP 席位/额度陷阱（View 席位任何计划都是 6 次/月；
  教育版免费拿 Professional + Full 席位 = 200 次/天）。

### 快速开始

```bash
git clone https://github.com/yushiran/Academic-Figure-Figma-CC-Skills.git
cp -r Academic-Figure-Figma-CC-Skills/academic-figure-figma ~/.claude/skills/
claude plugin install figma@claude-plugins-official   # 然后完成 OAuth, 见 references/figma-mcp-setup.md
```

之后直接对 Claude Code 说：**「把这张框架图按 IEEE 双栏宽度在 Figma 里画出来」**。

### 路线图

- **v0.2 — 减少往返**：实战验证过的 Figma JS 代码片段库 + 本地已核验图标缓存，
  一次 `use_figma` 调用搭完一个阶段。
- **v0.3 — 规格编译器**：声明式 `figure.spec.json` → 本地 SVG 预览（零额度迭代）→
  一次性生成 Figma 成稿。
- **v0.4 — 自动布局**：图状结构用 ELK/dagre 自动排位；沉淀可复用图模板
  （pipeline、训练/推理双面板、encoder-decoder）。

### 致谢

[paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro)
（图语法规则提炼自其 S1/S4 prompt 契约）·
[PaperBanana](https://github.com/llmsresearch/paperbanana) ·
[academic-figure-generator](https://github.com/LigphiDonk/academic-figure-generator) ·
Figma 官方 MCP 插件。
