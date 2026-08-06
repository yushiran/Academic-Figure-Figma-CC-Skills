# Academic-Figure-Figma-CC-Skills

用 **Claude Code + Figma MCP** 把论文框架图画成**可编辑的矢量成稿**的技能包。

## 定位：学术绘图工具链的最后一公里

```
候选图生成（发散）                     可编辑定稿（收敛）
┌────────────────────────────┐        ┌────────────────────────────┐
│ paper-framework-figure-     │  参考  │  本仓库                     │
│ studio-pro (ChatGPT 生图)   │ ─────▶ │  academic-figure-figma      │
│ PaperBanana 等              │  图像  │  (Claude Code + Figma MCP)  │
└────────────────────────────┘        └────────────────────────────┘
     产出: C01-C04 栅格候选图              产出: 论文精确尺寸的 Figma
     (不可编辑, 仅供人工复刻)              矢量文件, 图标为真矢量, 可手调
```

上游工具（[paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro)、
[PaperBanana](https://github.com/llmsresearch/paperbanana)、
[academic-figure-generator](https://github.com/LigphiDonk/academic-figure-generator)）解决"画什么、怎么构图"，
产出的是栅格参考图。本技能解决"落成可编辑成稿"：Claude Code 通过 Figma MCP 直接在画布上
搭骨架、填内容、注入矢量图标、拉箭头、截图自查，作者最后在 Figma 里手工微调并导出 PDF。

## 技能内容

```
academic-figure-figma/
├── SKILL.md                        # 主技能: 硬规则 + 五步工作流
├── references/
│   ├── figma-mcp-setup.md          # Figma MCP 连接、OAuth(远程会话)、席位与额度、教育版
│   ├── icon-sourcing.md            # 图标/logo 矢量获取: Lucide/lobe-icons/simpleicons/iconfont API
│   ├── paper-canvas-specs.md       # 论文画布规格: IEEE/Elsevier/AAAI 宽度、字号底线、Tinos 字体
│   ├── figure-grammar.md           # 框架图图语法契约: 箭头证据/变量上线/操作链/主线居中/反AI配色
│   └── build-workflow.md           # 增量构建细节: 辅助函数、箭头、配平、截图自查、踩坑记录
└── scripts/
    └── iconfont_search.py          # iconfont.cn 免登录搜索 → 可注入 SVG
```

核心经验（全部来自实战）：

- **正确性先行**：画图前先 grep 论文核对每个数字/术语/指标名；候选图里的错误照抄进图 = 秒拒风险。
- **额度陷阱**：Figma MCP 额度由**席位类型**决定而非计划档位（View 席位无论什么计划都是 6 次/月）；
  学生走教育版免费拿 Professional + Full 席位 = 200 次/天；改席位后必须重新 OAuth。
- **图标真矢量**：`figma.createNodeFromSvg` 注入，Lucide 管概念图标、lobe-icons 管 AI 品牌 logo、
  iconfont 搜索 API 已破解免登录；每个 logo 放进画布必须截图肉眼核对（simpleicons 的 qwen 是错的）。
- **按最终尺寸设计**：画布直接建在论文印刷宽度（IEEEtran 跨栏 516pt 等），字号所见即所得；
  大图缩小 = 字号崩坏。

## 安装

```bash
git clone https://github.com/yushiran/Academic-Figure-Figma-CC-Skills.git
cp -r Academic-Figure-Figma-CC-Skills/academic-figure-figma ~/.claude/skills/
```

然后在 Claude Code 里安装 Figma 插件并完成 OAuth（详见 `references/figma-mcp-setup.md`）：

```bash
claude plugin install figma@claude-plugins-official
```

对 Claude 说「帮我把这张框架图在 Figma 里画出来」即可触发。

## 致谢

- [paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro) —
  S0-S5 候选图生成流程与"审计前移"的思想。本技能两处直接承接它：Step-0 正确性审计承接其
  候选图产物（C01-C04），`references/figure-grammar.md` 从它的 S1/S4 prompt 契约中提炼了
  paper-neutral 的图语法规则（箭头双端证据、禁虚假中继、变量上线不占框、操作链完整、
  重复实体压缩、主线居中、反 AI 配色禁令、issue-ledger 错误词表）。
- [PaperBanana](https://github.com/llmsresearch/paperbanana)、
  [academic-figure-generator](https://github.com/LigphiDonk/academic-figure-generator) — 生图管线参考。
- Figma 官方 MCP 插件（figma-use 等 skills）。
