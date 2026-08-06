<p align="center">
  <img src="assets/Logo.png" width="160" alt="logo">
</p>

<h1 align="center">Academic-Figure-Figma-CC-Skills</h1>

<p align="center"><b>The last mile of the academic figure toolchain.</b></p>

<p align="center">
  <a href="https://github.com/yushiran/Academic-Figure-Figma-CC-Skills/stargazers"><img src="https://img.shields.io/github/stars/yushiran/Academic-Figure-Figma-CC-Skills?style=flat-square&logo=github" alt="stars"></a>
  <a href="https://github.com/yushiran/Academic-Figure-Figma-CC-Skills/network/members"><img src="https://img.shields.io/github/forks/yushiran/Academic-Figure-Figma-CC-Skills?style=flat-square&logo=github" alt="forks"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-Skill-D97757?style=flat-square" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/Figma-MCP-F24E1E?style=flat-square&logo=figma&logoColor=white" alt="Figma MCP">
</p>

<p align="center">English · <a href="README.md">中文</a></p>

---

Upstream figure pipelines ([studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro), [PaperBanana](https://github.com/llmsresearch/paperbanana)) produce raster candidates — great for exploring layout, impossible to hand-tune. This skill lets **Claude Code drive Figma directly through the official Figma MCP server**, landing a candidate or sketch as the final **editable, paper-exact vector figure**: true print width, true vector icons, every label audited against the paper source.

## 📰 News

> - **2026-08** · v0.1 released: five-step workflow + five reference docs + login-free iconfont search script.
> - **Coming soon** · 🎬 Live demo video: Figma canvas rendering on top, Claude Code drawing on the right.

## 📦 Skill structure

```
academic-figure-figma/
├── SKILL.md          # hard rules + five-step workflow
├── references/       # detail docs, loaded on demand
└── scripts/          # executable tools
```

| File | What it covers |
| --- | --- |
| `SKILL.md` | 6 hard rules; Preflight → skeleton → content → icons → arrows → balance & self-review |
| `references/figma-mcp-setup.md` | MCP connection, OAuth on remote sessions, seat/quota traps, free Education plan (200 calls/day) |
| `references/paper-canvas-specs.md` | IEEEtran 252/516pt, elsarticle ≈390pt, AAAI 239/504pt, 6pt font floor, Tinos for Times |
| `references/figure-grammar.md` | Figure grammar: arrow evidence, no false relays, variables on edges, centred mainline, anti-AI palette |
| `references/icon-sourcing.md` | Lucide / lobe-icons / simpleicons / iconfont API vector sourcing with per-mark verification |
| `references/build-workflow.md` | Incremental build, arrows, multi-column balancing, screenshot checklist, recorded pitfalls |
| `scripts/iconfont_search.py` | iconfont.cn login-free search → injectable SVG |

## 🚀 Quick start

```bash
git clone https://github.com/yushiran/Academic-Figure-Figma-CC-Skills.git
cp -r Academic-Figure-Figma-CC-Skills/academic-figure-figma ~/.claude/skills/
claude plugin install figma@claude-plugins-official   # OAuth steps: references/figma-mcp-setup.md
```

Then ask Claude Code: **"Rebuild this framework figure in Figma at IEEE double-column width."**

## 🙏 Acknowledgements

[paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro) (figure grammar distilled from its S1/S4 prompt contracts) · [PaperBanana](https://github.com/llmsresearch/paperbanana) · [academic-figure-generator](https://github.com/LigphiDonk/academic-figure-generator) · the official Figma MCP plugin
