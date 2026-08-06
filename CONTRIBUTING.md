# 贡献指南

本仓库的定位是**学术绘图工具链的最后一公里**：把候选图/草图落成论文精确尺寸的可编辑
Figma 矢量成稿。所有贡献都围绕这一目标——上游的候选图生成不在范围内。

## 核心原则

1. **没实测过的东西不进库。** `scripts/figma_lib.js` 的每个函数、`references/` 里的每条
   API 论断，都必须在真实 Figma 画布上验证过。v0.3 的教训：三个凭直觉写的 SVG 模板函数
   （elbowArrow/curveArrow/selfLoop）第一次实测线体全部被 viewBox 裁掉——直觉会错，截图不会。
2. **正确性优先于美观。** 涉及论文内容的示例（术语、数字、指标名）必须与来源一致。
3. **skill 必须自足。** 改动后 Claude 仅凭 SKILL.md + references + scripts 就能画图，
   不依赖外部文档查询。这是本 skill 的核心卖点，不能回退。

## 开发流程（TDD for skills）

**改 `figma_lib.js` / 新增组件：**
1. 写实现（SVG 模板路线优先，复用 `placeSvg`/`createNodeFromSvg`，不碰未验证 API）；
2. 在测试画布上一次调用画出全部新组件 + `screenshot()` 验收；
3. 截图里逐个核对：形状、位置、颜色、旋转后的定位；
4. 修到全绿再提交，commit message 写明测过什么、发现并修了什么。

**改 `SKILL.md` / `references/`：**
1. 改完跑一次 retrieval 测试：开一个只读这些文件的 fresh agent，让它写一个典型
   use_figma 调用并回答关键问题（画布宽度、箭头做法、禁用特性、并行协议）；
2. 它答不出来或答错的，就是文档 gap，补上再提交。

**改 `SKILL.md` 的 description：** 只写触发条件，不写工作流摘要（否则 agent 会照
description 行事而跳过正文——SDO 规则）。

## 提交前检查（与 CI 完全一致）

每次 commit 前本地必须跑过与 GitHub Actions 相同的检查。装好一次即可：

```bash
pip3 install --user pylint
cat > .git/hooks/pre-commit <<'EOF'
#!/bin/sh
py=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
if [ -n "$py" ]; then
  python3 -m pylint $py || { echo "pylint failed - fix before committing"; exit 1; }
fi
head -1 academic-figure-figma/SKILL.md | grep -q '^---$' || { echo "SKILL.md frontmatter broken"; exit 1; }
python3 -c "import json; json.load(open('academic-figure-figma/scripts/assets/icons/icons.json'))" || exit 1
exit 0
EOF
chmod +x .git/hooks/pre-commit
```

要求：pylint **10.00/10**（CI 用默认规则，行长 ≤100、必须有 docstring）；
SKILL.md frontmatter 完整；图标 manifest 是合法 JSON。

## 提交规范

- 一个改动一个 commit；message 写清**改了什么、为什么、怎么验证的**。
- 图标缓存新增条目：品牌 logo 必须截图肉眼核验后在 manifest 的 `verified_by_eye`
  里登记（simpleicons 的 qwen 是错的——CDN 会贴错标，这条规矩因此而立）。
- 数值类内容（画布宽度、字号）：凭记忆的必须标 `≈`，并保留自测命令
  （`\the\textwidth`）让用户可校验。

## 发版

```bash
git tag v0.x && git push --tags
```

`package-skill.yml` 会自动校验结构、打包 `academic-figure-figma-v0.x.zip` 并挂到
Release。
