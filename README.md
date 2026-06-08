<div align="center">

# 🎨 UICheck-CLI

**轻量级 AI 生成代码视觉质量检测引擎**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/Version-v1.0.0-green.svg)](https://github.com/gitstq/UICheck-CLI/releases)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-orange.svg)]()

**42 条检测规则 · 7 大维度 · 零核心依赖 · 0-100 评分**

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

**UICheck-CLI** 是一款专为 AI 生成 UI 代码设计的轻量级视觉质量检测引擎。

#### 解决的痛点

随着 AI 编程助手的普及，越来越多的前端代码由 AI 生成。然而，这些代码往往**"能用但不好看"**——缺乏设计感、视觉质量参差不齐。具体表现为：

- 🎨 色彩搭配混乱，缺乏统一的设计语言
- 📏 间距排版随意，没有遵循设计规范
- ♿ 可访问性缺失，不符合 WCAG 标准
- 🧊 布局僵硬死板，带有明显的"AI 痕迹"
- 📱 响应式适配不完善，移动端体验差

#### 核心价值

UICheck-CLI 就像一位**自带设计审美的代码审查员**，能在你提交代码之前，快速扫描并发现这些视觉质量问题，给出可操作的改进建议和量化评分。

#### 自研差异化亮点

| 特性 | 说明 |
|------|------|
| **零依赖架构** | 仅依赖 Python 标准库，安装即用，无任何第三方包 |
| **42 条检测规则** | 覆盖色彩、排版、间距、布局、可访问性、性能、反模式 7 大维度 |
| **7 维度评分体系** | 0-100 综合评分，各维度独立评分，精准定位问题 |
| **多格式文件支持** | HTML / CSS / JSX / TSX / Vue SFC 一站式检测 |
| **三种报告格式** | 终端彩色表格 / JSON / Markdown，灵活适配不同场景 |

#### 灵感来源

本项目灵感来源于 GitHub Trending 上的优秀开源项目 **impeccable**。在受到其设计理念启发后，我们进行了**完全独立的自主研发**，从底层架构到检测规则均为原创实现，致力于为中文开发者社区提供一款好用的 UI 代码质量检测工具。

---

### ✨ 核心特性

- 🧠 **智能分析引擎** — 基于 **AST + 正则混合分析**，精准识别代码中的视觉质量问题
- 📐 **7 大检测维度** — 色彩、排版、间距、布局、可访问性、性能、反模式，全方位覆盖
- 📋 **42 条专业规则** — 每条规则均附带**问题描述、严重级别、修复建议**，开箱即用
- 🏆 **0-100 量化评分** — 综合评分 + 维度评分，用数据衡量视觉质量
- 📄 **多格式文件支持** — 原生支持 **HTML、CSS、JSX、TSX、Vue SFC** 五种主流前端格式
- 🖥️ **三种报告输出** — 终端**彩色表格**（直观）、**JSON**（可集成）、**Markdown**（可分享）
- 🚫 **零核心依赖** — 仅使用 Python 标准库，**pip install 即可运行**，不引入任何第三方包
- ⚡ **极速扫描** — 纯 Python 实现，毫秒级响应，适合本地开发实时检测
- 🎯 **灵活过滤** — 支持按规则类别、严重级别过滤，聚焦你关心的维度
- 🔧 **修复建议** — 每条检测结果均附带**可操作的代码修复建议**

---

### 🚀 快速开始

#### 环境要求

- **Python 3.8** 或更高版本
- 无需安装任何第三方依赖

#### 安装方式

**方式一：通过 pip 安装（推荐）**

```bash
pip install uicheck-cli
```

**方式二：从源码安装**

```bash
git clone https://github.com/gitstq/UICheck-CLI.git
cd UICheck-CLI
pip install .
```

#### 一键运行

```bash
# 扫描单个文件
uicheck-cli scan ./src/components/Button.tsx

# 扫描整个目录
uicheck-cli scan ./src

# 以 JSON 格式输出报告
uicheck-cli scan ./src --format json --output report.json

# 以 Markdown 格式输出报告
uicheck-cli scan ./src --format markdown --output report.md
```

> 💡 如果未通过 pip 安装，也可以直接以模块方式运行：
> ```bash
> python -m uicheck_cli scan ./src
> ```

---

### 📖 详细使用指南

#### 基础用法：scan 命令

`scan` 是最核心的命令，用于扫描文件或目录中的视觉质量问题。

```bash
# 扫描单个文件
uicheck-cli scan index.html

# 扫描目录（递归扫描所有支持的文件格式）
uicheck-cli scan ./src/components

# 启用详细模式（显示代码片段和修复建议）
uicheck-cli scan ./src --verbose

# 禁用彩色输出（适用于日志文件）
uicheck-cli scan ./src --no-color
```

#### 规则管理：list / info

查看和管理所有检测规则。

```bash
# 列出所有规则
uicheck-cli rules list

# 按类别筛选规则
uicheck-cli rules list --category color

# 以 JSON 格式输出规则列表
uicheck-cli rules list --format json

# 查看某条规则的详细信息
uicheck-cli rules info color-001
```

#### 报告格式

UICheck-CLI 支持三种报告输出格式，适配不同使用场景：

| 格式 | 标志 | 适用场景 |
|------|------|----------|
| **终端表格** | `--format terminal`（默认） | 本地开发实时查看，彩色高亮显示 |
| **JSON** | `--format json` | CI/CD 流水线集成、自动化处理 |
| **Markdown** | `--format markdown` | 生成可分享的检测报告文档 |

```bash
# 终端彩色表格（默认）
uicheck-cli scan ./src

# JSON 报告（输出到文件）
uicheck-cli scan ./src --format json --output report.json

# Markdown 报告（输出到文件）
uicheck-cli scan ./src --format markdown --output report.md
```

#### 过滤选项

支持按规则类别和严重级别进行过滤，聚焦你关心的维度。

```bash
# 仅检测色彩和排版规则
uicheck-cli scan ./src --rules color,typography

# 仅显示 ERROR 级别的问题
uicheck-cli scan ./src --severity error

# 组合使用：检测可访问性维度中 WARNING 及以上级别
uicheck-cli scan ./src --rules accessibility --severity warning
```

**可选的规则类别：** `color`、`typography`、`spacing`、`layout`、`accessibility`、`performance`、`antipattern`

**严重级别：** `error` > `warning` > `info`

#### 进阶用法

```bash
# 详细模式 + 指定格式 + 输出文件
uicheck-cli scan ./src -v -f json -o result.json

# 仅检测特定维度并输出 Markdown 报告
uicheck-cli scan ./src --rules color,spacing --format markdown --output review.md

# 无彩色输出 + 仅显示错误（适合 CI 环境）
uicheck-cli scan ./src --no-color --severity error
```

#### 典型使用场景

**场景一：日常开发自检**

```bash
# 在编写组件时快速检查
uicheck-cli scan ./src/components/LoginForm.tsx -v
```

**场景二：代码评审辅助**

```bash
# 生成 Markdown 报告，附在 PR 描述中
uicheck-cli scan ./src --format markdown --output pr-review.md
```

**场景三：CI/CD 质量门禁**

```bash
# 在 CI 流水线中仅检查 ERROR 级别问题
uicheck-cli scan ./src --severity error --format json --output ci-report.json
```

**场景四：专项维度优化**

```bash
# 专注优化可访问性
uicheck-cli scan ./src --rules accessibility -v
```

---

### 📊 检测规则一览

UICheck-CLI 内置 **42 条检测规则**，覆盖 **7 大维度**。以下为完整规则列表：

#### 🎨 色彩维度（6 条规则）

| 规则 ID | 名称 | 严重级别 | 描述 |
|---------|------|----------|------|
| color-001 | 硬编码颜色过多 | ⚠️ WARNING | 文件中存在超过 5 个独立的硬编码颜色值，建议使用 CSS 自定义属性 |
| color-002 | 低对比度颜色组合 | 🔴 ERROR | 检测到对比度过低的颜色对，可能导致可读性问题 |
| color-003 | 缺少深色模式支持 | ℹ️ INFO | 未检测到 `prefers-color-scheme: dark` 媒体查询或深色模式类选择器 |
| color-004 | 纯黑/纯白背景 | ⚠️ WARNING | 使用纯黑 (#000) 或纯白 (#fff) 作为背景色，容易造成视觉疲劳 |
| color-005 | 品牌色不一致 | ⚠️ WARNING | 检测到相似但不完全相同的颜色值，可能是品牌色使用不一致 |
| color-006 | 未使用 CSS 自定义属性 | ℹ️ INFO | 存在多个硬编码颜色但未使用 CSS 自定义属性（设计令牌） |

#### 📝 排版维度（6 条规则）

| 规则 ID | 名称 | 严重级别 | 描述 |
|---------|------|----------|------|
| typography-001 | 字号层级过多 | ⚠️ WARNING | 存在超过 6 个独立的 font-size 值，排版体系不够统一 |
| typography-002 | 缺少字体回退栈 | 🔴 ERROR | font-family 声明中只有一个字体，缺少通用字体回退 |
| typography-003 | 行高缺失或过小 | ⚠️ WARNING | 未设置 line-height 或行高值小于 1.4，影响文本可读性 |
| typography-004 | 标题层级跳跃 | ⚠️ WARNING | 标题层级不连续（如 h1 直接跳到 h3），影响可访问性 |
| typography-005 | 使用 px 而非 rem/em | ℹ️ INFO | font-size 使用 px 单位而非 rem/em，不利于无障碍访问和响应式设计 |
| typography-006 | 字重过多 | ⚠️ WARNING | 使用了超过 4 种独立的 font-weight 值，排版风格不统一 |

#### 📏 间距维度（4 条规则）

| 规则 ID | 名称 | 严重级别 | 描述 |
|---------|------|----------|------|
| spacing-001 | 非标准间距值 | ⚠️ WARNING | margin/padding 值不是 4px 的整数倍，破坏视觉一致性 |
| spacing-002 | 间距不一致 | ⚠️ WARNING | 相似的 CSS 选择器使用了不同的间距值 |
| spacing-003 | 缺少垂直韵律 | ℹ️ INFO | 垂直方向的间距值过多且不统一，建议建立一致的垂直韵律 |
| spacing-004 | 使用负外边距 | ⚠️ WARNING | 使用了负 margin 值，可能导致布局异常 |

#### 🧊 布局维度（6 条规则）

| 规则 ID | 名称 | 严重级别 | 描述 |
|---------|------|----------|------|
| layout-001 | 固定宽度缺少 max-width | 🔴 ERROR | 使用固定像素宽度但未设置 max-width，小屏幕上会溢出 |
| layout-002 | 缺少 viewport 元标签 | 🔴 ERROR | HTML 文件中缺少 viewport meta 标签，影响移动端响应式 |
| layout-003 | 绝对定位用于布局 | ⚠️ WARNING | 使用 position: absolute 进行布局，建议改用 flexbox/grid |
| layout-004 | 缺少响应式断点 | ⚠️ WARNING | CSS 文件中没有任何媒体查询，缺少响应式适配 |
| layout-005 | 未处理溢出 | ⚠️ WARNING | 固定高度容器未设置 overflow 处理，内容可能溢出 |
| layout-006 | 使用 float 布局 | ⚠️ WARNING | 使用 float 进行布局，建议改用现代的 flexbox/grid |

#### ♿ 可访问性维度（6 条规则）

| 规则 ID | 名称 | 严重级别 | 描述 |
|---------|------|----------|------|
| accessibility-001 | 图片缺少 alt 文本 | 🔴 ERROR | `<img>` 标签缺少 alt 属性，屏幕阅读器无法识别图片内容 |
| accessibility-002 | 表单元素缺少 label | 🔴 ERROR | input/textarea/select 没有关联的 label 元素 |
| accessibility-003 | 缺少语义化 HTML | ⚠️ WARNING | 过度使用 `<div>` 而缺少语义化标签（header/nav/main 等） |
| accessibility-004 | 缺少 ARIA 属性 | ⚠️ WARNING | 可交互元素（带 onclick 的 div/span）缺少 ARIA 角色和属性 |
| accessibility-005 | 文本颜色对比度不足 | 🔴 ERROR | 文本/背景颜色对比度低于 WCAG 要求的 4.5:1 |
| accessibility-006 | 缺少跳转导航链接 | ℹ️ INFO | 页面中没有 skip navigation 链接，键盘用户无法快速跳转到主内容 |

#### ⚡ 性能维度（6 条规则）

| 规则 ID | 名称 | 严重级别 | 描述 |
|---------|------|----------|------|
| performance-001 | 过多的内联样式 | ⚠️ WARNING | 内联 style 属性过多，降低可维护性和性能 |
| performance-002 | 重复的 CSS 选择器 | ⚠️ WARNING | 同一选择器出现多次，存在冗余和特异性冲突风险 |
| performance-003 | 未压缩的 CSS | ℹ️ INFO | CSS 中存在大量空白行和注释，生产环境建议压缩 |
| performance-004 | DOM 嵌套过深 | ⚠️ WARNING | DOM 嵌套层级超过 10 层，影响渲染性能和代码可读性 |
| performance-005 | 使用 !important | ⚠️ WARNING | 过多使用 !important，表明特异性管理存在问题 |
| performance-006 | 使用通配选择器 | ℹ️ INFO | 使用了通配选择器 (*)，匹配所有元素可能影响渲染性能 |

#### 🚫 反模式维度（8 条规则）

| 规则 ID | 名称 | 严重级别 | 描述 |
|---------|------|----------|------|
| antipattern-001 | 过度对称的 AI 风格 | ℹ️ INFO | 所有间距和圆角值完全一致，呈现典型的"AI 生成感" |
| antipattern-002 | 千篇一律的卡片布局 | ⚠️ WARNING | 多个卡片组件结构完全相同（图片+标题+段落），缺乏视觉变化 |
| antipattern-003 | 过多的渐变背景 | ⚠️ WARNING | 渐变背景使用过多，看起来过于花哨且带有"AI 痕迹" |
| antipattern-004 | 缺少微交互动效 | ⚠️ WARNING | 没有 CSS 过渡或动画，界面感觉生硬不灵动 |
| antipattern-005 | 按钮样式过于统一 | ℹ️ INFO | 所有按钮样式相同，缺少主/次/描边/幽灵按钮的层级区分 |
| antipattern-006 | 缺少悬停/聚焦状态 | 🔴 ERROR | 可交互元素没有定义 :hover 或 :focus 状态 |
| antipattern-007 | 用 Emoji 替代图标 | ⚠️ WARNING | 在 UI 中使用 Emoji 字符代替专业图标，显得不够专业 |
| antipattern-008 | 缺少加载/空状态 | ⚠️ WARNING | 存在动态内容区域但未定义加载状态或空状态占位 |

---

### 💡 设计思路与迭代规划

#### 设计理念

UICheck-CLI 的核心设计理念是**"让 AI 生成的代码也有设计感"**。

- **AST + 正则混合分析**：对于结构化的 HTML/CSS，使用正则表达式进行高效的模式匹配；对于复杂的嵌套结构，采用简化的 AST 解析思路，在准确性和性能之间取得平衡
- **零依赖架构**：全部基于 Python 标准库实现（`re`、`math`、`dataclasses`、`enum`、`argparse`），确保安装零摩擦，在任何 Python 环境下都能直接运行
- **规则可扩展**：每条规则都是独立的类，遵循统一的 `Rule` 基类接口，新增规则只需继承基类并实现 `check()` 方法

#### 技术选型原因

| 决策 | 原因 |
|------|------|
| 选择 Python | 生态丰富、开发效率高、前端工程师学习成本低 |
| 零外部依赖 | 降低安装门槛，避免依赖冲突，适合作为 CI 工具链的一部分 |
| CLI 工具形态 | 轻量、可集成、适合本地开发和 CI/CD 场景 |
| 正则 + 简化 AST | 在零依赖约束下，兼顾检测准确性和代码可维护性 |

#### 后续迭代计划

- 🔌 **VS Code 插件** — 在编辑器中实时显示视觉质量问题，支持一键修复
- 🔄 **CI/CD 集成** — 提供 GitHub Actions / GitLab CI 预设配置，自动化质量门禁
- 📝 **自定义规则 DSL** — 允许用户通过 YAML/JSON 文件定义自己的检测规则
- 📊 **Web Dashboard** — 可视化展示项目视觉质量趋势和历史数据
- 🌐 **多语言规则描述** — 规则描述和修复建议支持多语言输出
- 🤖 **AI 修复建议** — 结合 LLM 生成更智能、更上下文感知的修复方案

#### 社区贡献方向

我们欢迎以下方向的贡献：

- 🆕 新增检测规则（尤其是动画、动效、暗色模式等维度）
- 🌍 多语言规则描述翻译
- 📚 使用教程和最佳实践文档
- 🐛 Bug 修复和性能优化
- 💡 新功能建议和讨论

---

### 🤝 贡献指南

我们非常欢迎社区贡献！无论是提交 Bug 报告、功能建议，还是直接提交代码，都是对项目的巨大支持。

#### 提交 PR 规范

1. **Fork** 本仓库并创建你的特性分支：`git checkout -b feature/your-feature-name`
2. 确保代码通过现有测试：`python -m pytest tests/`
3. 遵循项目代码风格：使用类型注解、编写文档字符串、遵循 PEP 8
4. 新增规则需继承 `Rule` 基类，并在对应模块的 `register_all()` 方法中注册
5. 提交 PR 时请附上清晰的变更说明

#### Issue 反馈规则

提交 Issue 时，请尽量包含以下信息：

- 🐍 Python 版本
- 💻 操作系统及版本
- 📄 触发问题的文件或代码片段
- ❓ 期望行为 vs 实际行为
- 📋 完整的错误信息（如有）

---

### 📄 开源协议

本项目基于 **MIT License** 开源。

```
MIT License

Copyright (c) 2026 琦琦

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star 支持一下！**

Made with ❤️ by [UICheck Team](https://github.com/gitstq/UICheck-CLI)

</div>

---

## 繁體中文

### 🎉 專案介紹

**UICheck-CLI** 是一款專為 AI 生成 UI 程式碼設計的輕量級視覺品質偵測引擎。

#### 解決的痛點

隨著 AI 程式設計助手的普及，越來越多的前端程式碼由 AI 生成。然而，這些程式碼往往**「能用但不好看」**——缺乏設計感、視覺品質參差不齊。具體表現為：

- 🎨 色彩搭配混亂，缺乏統一的設計語言
- 📏 間距排版隨意，沒有遵循設計規範
- ♿ 無障礙性缺失，不符合 WCAG 標準
- 🧊 佈局僵硬死板，帶有明顯的「AI 痕跡」
- 📱 響應式適配不完善，行動端體驗差

#### 核心價值

UICheck-CLI 就像一位**自帶設計審美的程式碼審查員**，能在你提交程式碼之前，快速掃描並發現這些視覺品質問題，給出可操作的改進建議和量化評分。

#### 自研差異化亮點

| 特性 | 說明 |
|------|------|
| **零依賴架構** | 僅依賴 Python 標準函式庫，安裝即用，無任何第三方套件 |
| **42 條偵測規則** | 涵蓋色彩、排版、間距、佈局、無障礙、效能、反模式 7 大維度 |
| **7 維度評分體系** | 0-100 綜合評分，各維度獨立評分，精準定位問題 |
| **多格式檔案支援** | HTML / CSS / JSX / TSX / Vue SFC 一站式偵測 |
| **三種報告格式** | 終端彩色表格 / JSON / Markdown，靈活適配不同場景 |

#### 靈感來源

本專案靈感來源於 GitHub Trending 上的優秀開源專案 **impeccable**。在受到其設計理念啟發後，我們進行了**完全獨立的自研開發**，從底層架構到偵測規則均為原創實作，致力於為中文開發者社群提供一款好用的 UI 程式碼品質偵測工具。

---

### ✨ 核心特性

- 🧠 **智慧分析引擎** — 基於 **AST + 正規表達式混合分析**，精準識別程式碼中的視覺品質問題
- 📐 **7 大偵測維度** — 色彩、排版、間距、佈局、無障礙、效能、反模式，全方位涵蓋
- 📋 **42 條專業規則** — 每條規則均附帶**問題描述、嚴重級別、修復建議**，開箱即用
- 🏆 **0-100 量化評分** — 綜合評分 + 維度評分，用數據衡量視覺品質
- 📄 **多格式檔案支援** — 原生支援 **HTML、CSS、JSX、TSX、Vue SFC** 五種主流前端格式
- 🖥️ **三種報告輸出** — 終端**彩色表格**（直觀）、**JSON**（可整合）、**Markdown**（可分享）
- 🚫 **零核心依賴** — 僅使用 Python 標準函式庫，**pip install 即可執行**，不引入任何第三方套件
- ⚡ **極速掃描** — 純 Python 實作，毫秒級回應，適合本地開發即時偵測
- 🎯 **靈活篩選** — 支援按規則類別、嚴重級別篩選，聚焦你關心的維度
- 🔧 **修復建議** — 每條偵測結果均附帶**可操作的程式碼修復建議**

---

### 🚀 快速開始

#### 環境需求

- **Python 3.8** 或更高版本
- 無需安裝任何第三方依賴

#### 安裝方式

**方式一：透過 pip 安裝（推薦）**

```bash
pip install uicheck-cli
```

**方式二：從原始碼安裝**

```bash
git clone https://github.com/gitstq/UICheck-CLI.git
cd UICheck-CLI
pip install .
```

#### 一鍵執行

```bash
# 掃描單一檔案
uicheck-cli scan ./src/components/Button.tsx

# 掃描整個目錄
uicheck-cli scan ./src

# 以 JSON 格式輸出報告
uicheck-cli scan ./src --format json --output report.json

# 以 Markdown 格式輸出報告
uicheck-cli scan ./src --format markdown --output report.md
```

> 💡 如果未透過 pip 安裝，也可以直接以模組方式執行：
> ```bash
> python -m uicheck_cli scan ./src
> ```

---

### 📖 詳細使用指南

#### 基礎用法：scan 指令

`scan` 是最核心的指令，用於掃描檔案或目錄中的視覺品質問題。

```bash
# 掃描單一檔案
uicheck-cli scan index.html

# 掃描目錄（遞迴掃描所有支援的檔案格式）
uicheck-cli scan ./src/components

# 啟用詳細模式（顯示程式碼片段和修復建議）
uicheck-cli scan ./src --verbose

# 停用彩色輸出（適用於日誌檔案）
uicheck-cli scan ./src --no-color
```

#### 規則管理：list / info

查看和管理所有偵測規則。

```bash
# 列出所有規則
uicheck-cli rules list

# 按類別篩選規則
uicheck-cli rules list --category color

# 以 JSON 格式輸出規則列表
uicheck-cli rules list --format json

# 查看某條規則的詳細資訊
uicheck-cli rules info color-001
```

#### 報告格式

UICheck-CLI 支援三種報告輸出格式，適配不同使用場景：

| 格式 | 標誌 | 適用場景 |
|------|------|----------|
| **終端表格** | `--format terminal`（預設） | 本地開發即時查看，彩色高亮顯示 |
| **JSON** | `--format json` | CI/CD 流水線整合、自動化處理 |
| **Markdown** | `--format markdown` | 產生可分享的偵測報告文件 |

```bash
# 終端彩色表格（預設）
uicheck-cli scan ./src

# JSON 報告（輸出到檔案）
uicheck-cli scan ./src --format json --output report.json

# Markdown 報告（輸出到檔案）
uicheck-cli scan ./src --format markdown --output report.md
```

#### 篩選選項

支援按規則類別和嚴重級別進行篩選，聚焦你關心的維度。

```bash
# 僅偵測色彩和排版規則
uicheck-cli scan ./src --rules color,typography

# 僅顯示 ERROR 級別的問題
uicheck-cli scan ./src --severity error

# 組合使用：偵測無障礙維度中 WARNING 及以上級別
uicheck-cli scan ./src --rules accessibility --severity warning
```

**可選的規則類別：** `color`、`typography`、`spacing`、`layout`、`accessibility`、`performance`、`antipattern`

**嚴重級別：** `error` > `warning` > `info`

#### 進階用法

```bash
# 詳細模式 + 指定格式 + 輸出檔案
uicheck-cli scan ./src -v -f json -o result.json

# 僅偵測特定維度並輸出 Markdown 報告
uicheck-cli scan ./src --rules color,spacing --format markdown --output review.md

# 無彩色輸出 + 僅顯示錯誤（適合 CI 環境）
uicheck-cli scan ./src --no-color --severity error
```

#### 典型使用場景

**場景一：日常開發自檢**

```bash
# 在撰寫元件時快速檢查
uicheck-cli scan ./src/components/LoginForm.tsx -v
```

**場景二：程式碼審查輔助**

```bash
# 產生 Markdown 報告，附在 PR 描述中
uicheck-cli scan ./src --format markdown --output pr-review.md
```

**場景三：CI/CD 品質門禁**

```bash
# 在 CI 流水線中僅檢查 ERROR 級別問題
uicheck-cli scan ./src --severity error --format json --output ci-report.json
```

**場景四：專項維度優化**

```bash
# 專注優化無障礙性
uicheck-cli scan ./src --rules accessibility -v
```

---

### 📊 偵測規則一覽

UICheck-CLI 內建 **42 條偵測規則**，涵蓋 **7 大維度**。以下為完整規則列表：

#### 🎨 色彩維度（6 條規則）

| 規則 ID | 名稱 | 嚴重級別 | 描述 |
|---------|------|----------|------|
| color-001 | 硬編碼色彩過多 | ⚠️ WARNING | 檔案中存在超過 5 個獨立的硬編碼色彩值，建議使用 CSS 自訂屬性 |
| color-002 | 低對比度色彩組合 | 🔴 ERROR | 偵測到對比度過低的色彩對，可能導致可讀性問題 |
| color-003 | 缺少深色模式支援 | ℹ️ INFO | 未偵測到 `prefers-color-scheme: dark` 媒體查詢或深色模式類選擇器 |
| color-004 | 純黑/純白背景 | ⚠️ WARNING | 使用純黑 (#000) 或純白 (#fff) 作為背景色，容易造成視覺疲勞 |
| color-005 | 品牌色不一致 | ⚠️ WARNING | 偵測到相似但不完全相同的色彩值，可能是品牌色使用不一致 |
| color-006 | 未使用 CSS 自訂屬性 | ℹ️ INFO | 存在多個硬編碼色彩但未使用 CSS 自訂屬性（設計令牌） |

#### 📝 排版維度（6 條規則）

| 規則 ID | 名稱 | 嚴重級別 | 描述 |
|---------|------|----------|------|
| typography-001 | 字號層級過多 | ⚠️ WARNING | 存在超過 6 個獨立的 font-size 值，排版體系不夠統一 |
| typography-002 | 缺少字體回溯棧 | 🔴 ERROR | font-family 宣告中只有一個字體，缺少通用字體回溯 |
| typography-003 | 行高缺失或過小 | ⚠️ WARNING | 未設定 line-height 或行高值小於 1.4，影響文字可讀性 |
| typography-004 | 標題層級跳躍 | ⚠️ WARNING | 標題層級不連續（如 h1 直接跳到 h3），影響無障礙性 |
| typography-005 | 使用 px 而非 rem/em | ℹ️ INFO | font-size 使用 px 單位而非 rem/em，不利於無障礙存取和響應式設計 |
| typography-006 | 字重過多 | ⚠️ WARNING | 使用了超過 4 種獨立的 font-weight 值，排版風格不統一 |

#### 📏 間距維度（4 條規則）

| 規則 ID | 名稱 | 嚴重級別 | 描述 |
|---------|------|----------|------|
| spacing-001 | 非標準間距值 | ⚠️ WARNING | margin/padding 值不是 4px 的整數倍，破壞視覺一致性 |
| spacing-002 | 間距不一致 | ⚠️ WARNING | 相似的 CSS 選擇器使用了不同的間距值 |
| spacing-003 | 缺少垂直韻律 | ℹ️ INFO | 垂直方向的間距值過多且不統一，建議建立一致的垂直韻律 |
| spacing-004 | 使用負外邊距 | ⚠️ WARNING | 使用了負 margin 值，可能導致佈局異常 |

#### 🧊 佈局維度（6 條規則）

| 規則 ID | 名稱 | 嚴重級別 | 描述 |
|---------|------|----------|------|
| layout-001 | 固定寬度缺少 max-width | 🔴 ERROR | 使用固定像素寬度但未設定 max-width，小螢幕上會溢出 |
| layout-002 | 缺少 viewport 元標籤 | 🔴 ERROR | HTML 檔案中缺少 viewport meta 標籤，影響行動端響應式 |
| layout-003 | 絕對定位用於佈局 | ⚠️ WARNING | 使用 position: absolute 進行佈局，建議改用 flexbox/grid |
| layout-004 | 缺少響應式斷點 | ⚠️ WARNING | CSS 檔案中沒有任何媒體查詢，缺少響應式適配 |
| layout-005 | 未處理溢出 | ⚠️ WARNING | 固定高度容器未設定 overflow 處理，內容可能溢出 |
| layout-006 | 使用 float 佈局 | ⚠️ WARNING | 使用 float 進行佈局，建議改用現代的 flexbox/grid |

#### ♿ 無障礙維度（6 條規則）

| 規則 ID | 名稱 | 嚴重級別 | 描述 |
|---------|------|----------|------|
| accessibility-001 | 圖片缺少 alt 文字 | 🔴 ERROR | `<img>` 標籤缺少 alt 屬性，螢幕閱讀器無法識別圖片內容 |
| accessibility-002 | 表單元素缺少 label | 🔴 ERROR | input/textarea/select 沒有關聯的 label 元素 |
| accessibility-003 | 缺少語義化 HTML | ⚠️ WARNING | 過度使用 `<div>` 而缺少語義化標籤（header/nav/main 等） |
| accessibility-004 | 缺少 ARIA 屬性 | ⚠️ WARNING | 可互動元素（帶 onclick 的 div/span）缺少 ARIA 角色和屬性 |
| accessibility-005 | 文字色彩對比度不足 | 🔴 ERROR | 文字/背景色彩對比度低於 WCAG 要求的 4.5:1 |
| accessibility-006 | 缺少跳轉導覽連結 | ℹ️ INFO | 頁面中沒有 skip navigation 連結，鍵盤使用者無法快速跳到主內容 |

#### ⚡ 效能維度（6 條規則）

| 規則 ID | 名稱 | 嚴重級別 | 描述 |
|---------|------|----------|------|
| performance-001 | 過多的內聯樣式 | ⚠️ WARNING | 內聯 style 屬性過多，降低可維護性和效能 |
| performance-002 | 重複的 CSS 選擇器 | ⚠️ WARNING | 同一選擇器出現多次，存在冗餘和特異性衝突風險 |
| performance-003 | 未壓縮的 CSS | ℹ️ INFO | CSS 中存在大量空白行和註解，正式環境建議壓縮 |
| performance-004 | DOM 巢狀過深 | ⚠️ WARNING | DOM 巢狀層級超過 10 層，影響渲染效能和程式碼可讀性 |
| performance-005 | 使用 !important | ⚠️ WARNING | 過多使用 !important，表明特異性管理存在問題 |
| performance-006 | 使用通配選擇器 | ℹ️ INFO | 使用了通配選擇器 (*)，匹配所有元素可能影響渲染效能 |

#### 🚫 反模式維度（8 條規則）

| 規則 ID | 名稱 | 嚴重級別 | 描述 |
|---------|------|----------|------|
| antipattern-001 | 過度對稱的 AI 風格 | ℹ️ INFO | 所有間距和圓角值完全一致，呈現典型的「AI 生成感」 |
| antipattern-002 | 千篇一律的卡片佈局 | ⚠️ WARNING | 多個卡片元件結構完全相同（圖片+標題+段落），缺乏視覺變化 |
| antipattern-003 | 過多的漸層背景 | ⚠️ WARNING | 漸層背景使用過多，看起來過於花俏且帶有「AI 痕跡」 |
| antipattern-004 | 缺少微互動動效 | ⚠️ WARNING | 沒有 CSS 過渡或動畫，介面感覺生硬不靈動 |
| antipattern-005 | 按鈕樣式過於統一 | ℹ️ INFO | 所有按鈕樣式相同，缺少主/次/描邊/幽靈按鈕的層級區分 |
| antipattern-006 | 缺少懸停/聚焦狀態 | 🔴 ERROR | 可互動元素沒有定義 :hover 或 :focus 狀態 |
| antipattern-007 | 用 Emoji 替代圖示 | ⚠️ WARNING | 在 UI 中使用 Emoji 字元代替專業圖示，顯得不夠專業 |
| antipattern-008 | 缺少載入/空狀態 | ⚠️ WARNING | 存在動態內容區域但未定義載入狀態或空狀態佔位 |

---

### 💡 設計思路與迭代規劃

#### 設計理念

UICheck-CLI 的核心設計理念是**「讓 AI 生成的程式碼也有設計感」**。

- **AST + 正規表達式混合分析**：對於結構化的 HTML/CSS，使用正規表達式進行高效的模式比對；對於複雜的巢狀結構，採用簡化的 AST 解析思路，在準確性和效能之間取得平衡
- **零依賴架構**：全部基於 Python 標準函式庫實作（`re`、`math`、`dataclasses`、`enum`、`argparse`），確保安裝零摩擦，在任何 Python 環境下都能直接執行
- **規則可擴充**：每條規則都是獨立的類別，遵循統一的 `Rule` 基類介面，新增規則只需繼承基類並實作 `check()` 方法

#### 技術選型原因

| 決策 | 原因 |
|------|------|
| 選擇 Python | 生態豐富、開發效率高、前端工程師學習成本低 |
| 零外部依賴 | 降低安裝門檻，避免依賴衝突，適合作為 CI 工具鏈的一部分 |
| CLI 工具形態 | 輕量、可整合、適合本地開發和 CI/CD 場景 |
| 正規表達式 + 簡化 AST | 在零依賴約束下，兼顧偵測準確性和程式碼可維護性 |

#### 後續迭代計畫

- 🔌 **VS Code 擴充套件** — 在編輯器中即時顯示視覺品質問題，支援一鍵修復
- 🔄 **CI/CD 整合** — 提供 GitHub Actions / GitLab CI 預設配置，自動化品質門禁
- 📝 **自訂規則 DSL** — 允許使用者透過 YAML/JSON 檔案定義自己的偵測規則
- 📊 **Web Dashboard** — 視覺化呈現專案視覺品質趨勢和歷史資料
- 🌐 **多語言規則描述** — 規則描述和修復建議支援多語言輸出
- 🤖 **AI 修復建議** — 結合 LLM 產生更智慧、更上下文感知的修復方案

#### 社群貢獻方向

我們歡迎以下方向的貢獻：

- 🆕 新增偵測規則（尤其是動畫、動效、暗色模式等維度）
- 🌍 多語言規則描述翻譯
- 📚 使用教學和最佳實踐文件
- 🐛 Bug 修復和效能最佳化
- 💡 新功能建議和討論

---

### 🤝 貢獻指南

我們非常歡迎社群貢獻！無論是提交 Bug 回報、功能建議，還是直接提交程式碼，都是對專案的巨大支持。

#### 提交 PR 規範

1. **Fork** 本儲存庫並建立你的特性分支：`git checkout -b feature/your-feature-name`
2. 確保程式碼通過現有測試：`python -m pytest tests/`
3. 遵循專案程式碼風格：使用型別註解、撰寫文件字串、遵循 PEP 8
4. 新增規則需繼承 `Rule` 基類，並在對應模組的 `register_all()` 方法中註冊
5. 提交 PR 時請附上清晰的變更說明

#### Issue 回報規則

提交 Issue 時，請盡量包含以下資訊：

- 🐍 Python 版本
- 💻 作業系統及版本
- 📄 觸發問題的檔案或程式碼片段
- ❓ 期望行為 vs 實際行為
- 📋 完整的錯誤資訊（如有）

---

### 📄 開源協議

本專案基於 **MIT License** 開源。

```
MIT License

Copyright (c) 2026 琦琦

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

<div align="center">

**如果這個專案對你有幫助，請給一個 ⭐ Star 支持一下！**

Made with ❤️ by [UICheck Team](https://github.com/gitstq/UICheck-CLI)

</div>

---

## English

### 🎉 Introduction

**UICheck-CLI** is a lightweight visual quality detection engine designed specifically for AI-generated UI code.

#### The Problem It Solves

With the rise of AI coding assistants, more and more frontend code is being generated by AI. However, this code often **"works but doesn't look good"** — lacking design sense and consistent visual quality. Common issues include:

- 🎨 Chaotic color combinations with no unified design language
- 📏 Random spacing and layout that don't follow design conventions
- ♿ Missing accessibility features that fail WCAG standards
- 🧊 Rigid layouts with an obvious "AI-generated" feel
- 📱 Poor responsive design and mobile experience

#### Core Value

UICheck-CLI acts as a **code reviewer with an eye for design**, quickly scanning your code before you commit it, identifying visual quality issues, and providing actionable improvement suggestions with quantified scores.

#### Key Differentiators

| Feature | Description |
|---------|-------------|
| **Zero Dependencies** | Only relies on the Python standard library — install and run, no third-party packages |
| **42 Detection Rules** | Covering color, typography, spacing, layout, accessibility, performance, and anti-patterns across 7 dimensions |
| **7-Dimension Scoring** | 0-100 overall score with per-dimension scores for precise issue identification |
| **Multi-Format Support** | One-stop detection for HTML / CSS / JSX / TSX / Vue SFC |
| **Three Report Formats** | Terminal color table / JSON / Markdown for different use cases |

#### Inspiration

This project was inspired by the excellent open-source project **impeccable** from GitHub Trending. After being inspired by its design philosophy, we proceeded with **completely independent research and development** — from the underlying architecture to the detection rules, everything is an original implementation, dedicated to providing a practical UI code quality detection tool for the developer community.

---

### ✨ Core Features

- 🧠 **Intelligent Analysis Engine** — Powered by **AST + regex hybrid analysis** for precise identification of visual quality issues in code
- 📐 **7 Detection Dimensions** — Color, typography, spacing, layout, accessibility, performance, and anti-patterns — comprehensive coverage
- 📋 **42 Professional Rules** — Each rule includes an **issue description, severity level, and fix suggestion**, ready to use out of the box
- 🏆 **0-100 Quantified Scoring** — Overall score + dimension scores to measure visual quality with data
- 📄 **Multi-Format File Support** — Native support for **HTML, CSS, JSX, TSX, and Vue SFC** — five mainstream frontend formats
- 🖥️ **Three Report Outputs** — Terminal **color table** (intuitive), **JSON** (integrable), **Markdown** (shareable)
- 🚫 **Zero Core Dependencies** — Only uses the Python standard library, **pip install and run**, no third-party packages introduced
- ⚡ **Blazing Fast** — Pure Python implementation with millisecond response times, ideal for real-time local development checks
- 🎯 **Flexible Filtering** — Filter by rule category and severity level to focus on the dimensions you care about
- 🔧 **Fix Suggestions** — Every detection result comes with **actionable code fix suggestions**

---

### 🚀 Quick Start

#### Prerequisites

- **Python 3.8** or higher
- No third-party dependencies required

#### Installation

**Option 1: Install via pip (Recommended)**

```bash
pip install uicheck-cli
```

**Option 2: Install from source**

```bash
git clone https://github.com/gitstq/UICheck-CLI.git
cd UICheck-CLI
pip install .
```

#### Run It

```bash
# Scan a single file
uicheck-cli scan ./src/components/Button.tsx

# Scan an entire directory
uicheck-cli scan ./src

# Output report in JSON format
uicheck-cli scan ./src --format json --output report.json

# Output report in Markdown format
uicheck-cli scan ./src --format markdown --output report.md
```

> 💡 If you haven't installed via pip, you can also run it as a module directly:
> ```bash
> python -m uicheck_cli scan ./src
> ```

---

### 📖 Detailed Usage Guide

#### Basic Usage: The `scan` Command

The `scan` command is the core command for detecting visual quality issues in files or directories.

```bash
# Scan a single file
uicheck-cli scan index.html

# Scan a directory (recursively scans all supported file formats)
uicheck-cli scan ./src/components

# Enable verbose mode (shows code snippets and fix suggestions)
uicheck-cli scan ./src --verbose

# Disable colored output (for log files)
uicheck-cli scan ./src --no-color
```

#### Rule Management: `list` / `info`

View and manage all detection rules.

```bash
# List all rules
uicheck-cli rules list

# Filter rules by category
uicheck-cli rules list --category color

# Output rule list in JSON format
uicheck-cli rules list --format json

# View detailed information about a specific rule
uicheck-cli rules info color-001
```

#### Report Formats

UICheck-CLI supports three report output formats for different use cases:

| Format | Flag | Use Case |
|--------|------|----------|
| **Terminal Table** | `--format terminal` (default) | Real-time viewing during local development with color highlighting |
| **JSON** | `--format json` | CI/CD pipeline integration, automated processing |
| **Markdown** | `--format markdown` | Generating shareable detection report documents |

```bash
# Terminal color table (default)
uicheck-cli scan ./src

# JSON report (output to file)
uicheck-cli scan ./src --format json --output report.json

# Markdown report (output to file)
uicheck-cli scan ./src --format markdown --output report.md
```

#### Filter Options

Filter by rule category and severity level to focus on the dimensions you care about.

```bash
# Only check color and typography rules
uicheck-cli scan ./src --rules color,typography

# Only show ERROR-level issues
uicheck-cli scan ./src --severity error

# Combine: check accessibility dimension at WARNING level and above
uicheck-cli scan ./src --rules accessibility --severity warning
```

**Available rule categories:** `color`, `typography`, `spacing`, `layout`, `accessibility`, `performance`, `antipattern`

**Severity levels:** `error` > `warning` > `info`

#### Advanced Usage

```bash
# Verbose mode + specific format + output file
uicheck-cli scan ./src -v -f json -o result.json

# Check specific dimensions and output a Markdown report
uicheck-cli scan ./src --rules color,spacing --format markdown --output review.md

# No color + errors only (ideal for CI environments)
uicheck-cli scan ./src --no-color --severity error
```

#### Typical Use Cases

**Use Case 1: Daily Development Self-Check**

```bash
# Quick check while writing components
uicheck-cli scan ./src/components/LoginForm.tsx -v
```

**Use Case 2: Code Review Assistance**

```bash
# Generate a Markdown report to include in your PR description
uicheck-cli scan ./src --format markdown --output pr-review.md
```

**Use Case 3: CI/CD Quality Gate**

```bash
# Only check ERROR-level issues in your CI pipeline
uicheck-cli scan ./src --severity error --format json --output ci-report.json
```

**Use Case 4: Focused Dimension Optimization**

```bash
# Focus on accessibility improvements
uicheck-cli scan ./src --rules accessibility -v
```

---

### 📊 Detection Rules Reference

UICheck-CLI includes **42 detection rules** across **7 dimensions**. Here is the complete rule list:

#### 🎨 Color Dimension (6 Rules)

| Rule ID | Name | Severity | Description |
|---------|------|----------|-------------|
| color-001 | Too Many Hardcoded Colors | ⚠️ WARNING | More than 5 unique hardcoded color values detected; consider using CSS custom properties |
| color-002 | Low Contrast Color Combinations | 🔴 ERROR | Color pairs with contrast ratio below 1.5 detected, potential readability issues |
| color-003 | Missing Dark Mode Support | ℹ️ INFO | No `prefers-color-scheme: dark` media query or dark mode class selector detected |
| color-004 | Pure Black/White Background | ⚠️ WARNING | Pure black (#000) or pure white (#fff) used as background, causing eye strain |
| color-005 | Inconsistent Brand Colors | ⚠️ WARNING | Similar but non-identical color values detected, possibly inconsistent brand color usage |
| color-006 | No CSS Custom Properties for Colors | ℹ️ INFO | Multiple hardcoded colors found without CSS custom properties (design tokens) |

#### 📝 Typography Dimension (6 Rules)

| Rule ID | Name | Severity | Description |
|---------|------|----------|-------------|
| typography-001 | Too Many Font Size Levels | ⚠️ WARNING | More than 6 unique font-size values detected, inconsistent type scale |
| typography-002 | Missing Font Fallback Stack | 🔴 ERROR | font-family declared with only one font and no generic family fallback |
| typography-003 | Missing or Small Line-Height | ⚠️ WARNING | No line-height set or value below 1.4, affecting text readability |
| typography-004 | Heading Level Skipping | ⚠️ WARNING | Heading hierarchy skips levels (e.g., h1 -> h3), impacting accessibility |
| typography-005 | Using px Instead of rem/em | ℹ️ INFO | font-size uses px units instead of rem/em, less accessible and scalable |
| typography-006 | Too Many Font Weights | ⚠️ WARNING | More than 4 unique font-weight values detected, inconsistent typography |

#### 📏 Spacing Dimension (4 Rules)

| Rule ID | Name | Severity | Description |
|---------|------|----------|-------------|
| spacing-001 | Non-Standard Spacing Values | ⚠️ WARNING | margin/padding values are not multiples of 4px, breaking visual consistency |
| spacing-002 | Inconsistent Spacing | ⚠️ WARNING | Similar CSS selectors use different spacing values |
| spacing-003 | Missing Vertical Rhythm | ℹ️ INFO | Too many unique vertical margin values; consider establishing consistent vertical rhythm |
| spacing-004 | Negative Margin Usage | ⚠️ WARNING | Negative margin values detected, potentially causing layout issues |

#### 🧊 Layout Dimension (6 Rules)

| Rule ID | Name | Severity | Description |
|---------|------|----------|-------------|
| layout-001 | Fixed Width Without max-width | 🔴 ERROR | Fixed pixel width without max-width, will overflow on smaller screens |
| layout-002 | Missing Viewport Meta Tag | 🔴 ERROR | HTML file missing viewport meta tag, essential for responsive mobile design |
| layout-003 | Absolute Positioning for Layout | ⚠️ WARNING | position: absolute used for layout; consider flexbox or CSS grid instead |
| layout-004 | Missing Responsive Breakpoints | ⚠️ WARNING | No media queries found in CSS file, missing responsive design |
| layout-005 | Unhandled Overflow | ⚠️ WARNING | Fixed height container without overflow handling, content may overflow |
| layout-006 | Float-Based Layout | ⚠️ WARNING | float used for layout; consider modern flexbox or grid alternatives |

#### ♿ Accessibility Dimension (6 Rules)

| Rule ID | Name | Severity | Description |
|---------|------|----------|-------------|
| accessibility-001 | Images Missing Alt Text | 🔴 ERROR | `<img>` tags without alt attributes, essential for screen readers |
| accessibility-002 | Form Elements Missing Labels | 🔴 ERROR | input/textarea/select elements without associated label elements |
| accessibility-003 | Missing Semantic HTML | ⚠️ WARNING | Overuse of `<div>` without semantic tags (header/nav/main, etc.) |
| accessibility-004 | Missing ARIA Attributes | ⚠️ WARNING | Interactive elements (div/span with onclick) missing ARIA roles and attributes |
| accessibility-005 | Insufficient Text Color Contrast | 🔴 ERROR | Text/background color contrast ratio below WCAG requirement of 4.5:1 |
| accessibility-006 | Missing Skip Navigation Link | ℹ️ INFO | No skip navigation link found for keyboard users to jump to main content |

#### ⚡ Performance Dimension (6 Rules)

| Rule ID | Name | Severity | Description |
|---------|------|----------|-------------|
| performance-001 | Excessive Inline Styles | ⚠️ WARNING | Too many inline style attributes, reducing maintainability and performance |
| performance-002 | Duplicate CSS Selectors | ⚠️ WARNING | Same CSS selector appears multiple times, indicating redundancy |
| performance-003 | Uncompressed CSS | ℹ️ INFO | CSS with excessive whitespace and comments; consider minifying for production |
| performance-004 | Deep DOM Nesting | ⚠️ WARNING | DOM nesting exceeds 10 levels, hurting rendering performance and readability |
| performance-005 | Use of !important | ⚠️ WARNING | Excessive use of !important, indicating specificity management issues |
| performance-006 | Universal Selector Usage | ℹ️ INFO | Universal selector (*) matches every element, potentially impacting performance |

#### 🚫 Anti-Pattern Dimension (8 Rules)

| Rule ID | Name | Severity | Description |
|---------|------|----------|-------------|
| antipattern-001 | Overly Symmetric AI Style | ℹ️ INFO | All spacing and border-radius values are identical, typical "AI-generated" look |
| antipattern-002 | Cookie-Cutter Card Layout | ⚠️ WARNING | Multiple card components with identical structure (image+heading+paragraph) |
| antipattern-003 | Excessive Gradient Backgrounds | ⚠️ WARNING | Too many gradient declarations, looks generic and "AI-generated" |
| antipattern-004 | Missing Micro-Interactions | ⚠️ WARNING | No CSS transitions or animations, making the UI feel static |
| antipattern-005 | Uniform Button Styles | ℹ️ INFO | All buttons styled identically, missing primary/secondary/outline/ghost hierarchy |
| antipattern-006 | Missing Hover/Focus States | 🔴 ERROR | Interactive elements without :hover or :focus CSS states |
| antipattern-007 | Emoji as Icon Replacement | ⚠️ WARNING | Emoji characters used instead of proper SVG icons, looks unprofessional |
| antipattern-008 | Missing Loading/Empty States | ⚠️ WARNING | Dynamic content areas without loading or empty state placeholders |

---

### 💡 Design Philosophy & Roadmap

#### Design Philosophy

The core design philosophy of UICheck-CLI is **"making AI-generated code look designed."**

- **AST + Regex Hybrid Analysis**: For structured HTML/CSS, regex is used for efficient pattern matching; for complex nested structures, a simplified AST parsing approach balances accuracy and performance
- **Zero-Dependency Architecture**: Built entirely on the Python standard library (`re`, `math`, `dataclasses`, `enum`, `argparse`), ensuring zero-friction installation and the ability to run in any Python environment
- **Extensible Rule System**: Each rule is an independent class following a unified `Rule` base class interface. Adding new rules is as simple as extending the base class and implementing the `check()` method

#### Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Python | Rich ecosystem, high development efficiency, low learning curve for frontend engineers |
| Zero external dependencies | Lower installation barrier, avoid dependency conflicts, suitable for CI toolchains |
| CLI tool format | Lightweight, integrable, ideal for local development and CI/CD scenarios |
| Regex + simplified AST | Balances detection accuracy and code maintainability under zero-dependency constraints |

#### Roadmap

- 🔌 **VS Code Extension** — Real-time visual quality issue display in the editor with one-click fixes
- 🔄 **CI/CD Integration** — Pre-built GitHub Actions / GitLab CI configurations for automated quality gates
- 📝 **Custom Rule DSL** — Allow users to define their own detection rules via YAML/JSON files
- 📊 **Web Dashboard** — Visualize project visual quality trends and historical data
- 🌐 **Multi-Language Rule Descriptions** — Rule descriptions and fix suggestions in multiple languages
- 🤖 **AI-Powered Fix Suggestions** — Leverage LLMs for smarter, context-aware repair recommendations

#### Community Contribution Areas

We welcome contributions in the following areas:

- 🆕 New detection rules (especially for animations, motion, dark mode, etc.)
- 🌍 Multi-language rule description translations
- 📚 Tutorials and best practice documentation
- 🐛 Bug fixes and performance optimizations
- 💡 Feature suggestions and discussions

---

### 🤝 Contributing

We warmly welcome community contributions! Whether it's submitting bug reports, feature suggestions, or direct code commits, every contribution is greatly appreciated.

#### Pull Request Guidelines

1. **Fork** this repository and create your feature branch: `git checkout -b feature/your-feature-name`
2. Ensure code passes existing tests: `python -m pytest tests/`
3. Follow the project's code style: use type hints, write docstrings, follow PEP 8
4. New rules must extend the `Rule` base class and be registered in the corresponding module's `register_all()` method
5. Include a clear description of changes when submitting your PR

#### Issue Reporting Guidelines

When submitting an issue, please include as much of the following information as possible:

- 🐍 Python version
- 💻 Operating system and version
- 📄 The file or code snippet that triggered the issue
- ❓ Expected behavior vs. actual behavior
- 📋 Full error message (if applicable)

---

### 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 琦琦

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

<div align="center">

**If you find this project helpful, please give it a ⭐ Star!**

Made with ❤️ by [UICheck Team](https://github.com/gitstq/UICheck-CLI)

</div>
