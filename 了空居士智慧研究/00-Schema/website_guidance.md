# 了空居士智慧知识库 · 建站指导手册

> 基于当前知识库（64个Wiki文件、400KB纯文本、200+模型原子）的网站建设方案。
> 技术选型、架构设计、实施路线图。

---

## 一、知识库数据画像

### 内容规模

| 层级 | 文件数 | 大小 | 内容类型 |
|------|-------|------|---------|
| 10-核心模型 | 8 | 60KB | 7大模型，200+模型原子 |
| 20-专题研究 | 14 | 108KB | 13个深度分析专题 |
| 30-学习路径 | 4 | 32KB | 3条学习路线 |
| 40-原话金句 | 7 | 44KB | ~120条金句 |
| 50-概念资料 | 28 | 124KB | 25术语+索引+矛盾记录 |
| 03-Output | 3 | — | 摘要、学习指南、专题报告 |
| **合计** | **64** | **~400KB** | **纯文本Markdown** |

### 内容特征
- **全Markdown格式** — 天然适合静态网站生成器
- **双向链接丰富** — 200+ Obsidian Wiki-link 内部引用
- **五层递进结构** — 天然的网站导航骨架
- **纯中文内容** — 搜索需要中文分词能力
- **规模不大** — 纯静态托管即可，无需后端

---

## 二、网站信息架构（IA）

### 导航结构

```
首页（全景概览 + 快速入口）
│
├─ 核心模型（10-）
│  ├─ 天人合一
│  ├─ 对境不住
│  ├─ 对法不执
│  ├─ 自然务实
│  ├─ 圆融中和
│  ├─ 历境炼心
│  └─ 性命双修
│
├─ 专题研究（20-）
│  ├─ 问题分析（焦虑/情绪/人际关系/选择/疾病/财富/忍辱/生死）
│  ├─ 实践指导（入门实修/工作修行/修行进阶）
│  └─ 体系构建（家庭教育体系）
│
├─ 学习路径（30-）
│  ├─ 新手入门（7天计划）
│  ├─ 认知路径（系统学习）
│  └─ 问题路径（火线入口）
│
├─ 原话金句（40-）
│  ├─ 按经典索引（金刚经/道德经/心经/中论丹道）
│  ├─ 按模型索引（7大模型金句）
│  └─ 答疑精选
│
├─ 概念词典（50-）
│  ├─ 佛学概念（10个）
│  ├─ 丹道概念（9个）
│  └─ 心法概念（6个）
│
└─ 关于（项目说明 + 方法论 + 更新日志）
```

### 关键页面类型

| 页面类型 | 说明 | 示例 |
|---------|------|------|
| 首页 | 知识库全景 + 快速入口 | index.md |
| 模型页 | 核心模型 + 原子 + 实践指引 | model-对境不住.md |
| 专题页 | 深度分析 + 组合模型 | topic-焦虑.md |
| 路径页 | 学习路线图 | path-认知路径.md |
| 金句页 | 原话摘录 | quote-金刚经.md |
| 概念页 | 术语定义 | dict-清净心.md |

### 功能需求清单

**必备功能**：
- [ ] 五层导航栏 + 面包屑
- [ ] 全站中文全文搜索
- [ ] 内部链接正常跳转（Wiki-link 解析）
- [ ] Markdown 渲染（代码块/表格/引用/列表）
- [ ] 响应式（手机/平板/桌面）
- [ ] 深色模式

**加分功能**：
- [ ] 知识图谱可视化（模型关系网络图）
- [ ] 双向链接面板（每个页面底部显示"被谁引用"）
- [ ] 阅读进度保存（localStorage）
- [ ] PDF导出
- [ ] RSS订阅（更新通知）

---

## 三、技术方案推荐

根据你的知识库规模和需求，按"上手难度"分三级推荐：

### 方案A：VitePress（推荐 · 最佳平衡）

> 适合：愿意简单配置，希望站点美观专业

**核心优势**：
- Vite 构建极快（400KB内容几乎秒开）
- 内置中文搜索（基于 minisearch，无需额外服务）
- 自动侧边栏 + 面包屑导航
- 默认支持暗色模式
- Vue 生态，自定义灵活
- 部署到 GitHub Pages / Netlify / Vercel 免费

**需要做的工作**：
1. 将 Obsidian Wiki-link `[[...]]` 转换为标准 Markdown 链接
2. 写一个配置文件 `config.js`（定义导航栏结构）
3. 写一个转换脚本批量处理链接格式
4. 部署到免费托管平台

**迁移脚本预览**：
```bash
# Wiki-link 转 Markdown 链接
find . -name "*.md" -exec sed -i '' \
  's/\[\[\([^|]*\)|\([^]]*\)\]\]/[\2](\/\1)/g; s/\[\[\([^]]*\)\]\]/[\1](\/\1)/g' {} +
```

### 方案B：Next.js + ContentLayer（最灵活）

> 适合：想要完全自定义体验，愿意做开发

**核心优势**：
- 完全控制 UI/UX
- 可实现知识图谱（D3.js / vis.js）
- 可实现双向链接面板
- 可集成 LLM 问答功能（搜索结合AI回答）
- 可导出 PDF

**需要做的工作**：
1. 初始化 Next.js 项目
2. 配置 contentlayer 读取 Markdown
3. 设计页面模板（5种页面类型）
4. 实现搜索（pagefind / algolia）
5. 部署到 Vercel（免费）

### 方案C：Docusaurus（零折腾 · 文档站风格）

> 适合：快速上线，功能齐全

**核心优势**：
- Facebook 出品，生态成熟
- 内置搜索（Algolia 免费版支持中文）
- 内置版本管理
- 文档风格书写体验最佳
- 多语言友好

---

## 四、推荐实施路线图

根据你的情况，我推荐 **方案A：VitePress** — 上手最简单，效果最好，部署免费。

### 第1步：环境准备（~30分钟）

```bash
# 在工作目录下创建项目
cd /Users/panrui/WorkBuddy/Claw/了空居士智慧研究
mkdir website
cd website

# 初始化 VitePress
npm init -y
npm install -D vitepress

# 初始化
npx vitepress init
```

### 第2步：配置导航结构（~1小时）

编辑 `docs/.vitepress/config.ts`，定义五层导航：

```typescript
export default {
  title: '了空居士智慧',
  description: '系统性结构化智慧体系',
  themeConfig: {
    nav: [
      { text: '核心模型', link: '/10-核心模型/' },
      { text: '专题研究', link: '/20-专题研究/' },
      { text: '学习路径', link: '/30-学习路径/' },
      { text: '原话金句', link: '/40-原话金句/' },
      { text: '概念词典', link: '/50-概念资料/' },
    ],
    sidebar: { /* 各层级的子导航 */ }
  }
}
```

### 第3步：内容迁移（~1小时）

将 `02-Wiki/` 的文件复制到 `website/docs/`，同时：
1. 重命名：去掉 `topic-` `model-` `quote-` `dict-` `path-` 前缀（可选），或保持原样作为文件命名
2. **处理 Wiki-link**：写一个 Node.js 批量替换脚本

### 第4步：Wiki-link 转换脚本

核心问题是 Obsidian 的 `[[链接|显示名]]` 需要转为 `[显示名](链接)`。给你的转换脚本：

```javascript
// convert-links.js
const fs = require('fs');
const path = require('path');

const wikiDir = 'website/docs';

function convertWikiLinks(content, filePath) {
  // [[显示名|目标路径]] → [显示名](/目标路径)
  content = content.replace(/\[\[([^|#]+?)\|(.+?)\]\]/g, (m, path, text) => {
    return `[${text}](/${path.replace('.md', '')})`;
  });
  // [[目标路径]] → [目标路径](/目标路径)
  content = content.replace(/\[\[([^#]+?)\]\]/g, (m, path) => {
    const text = path.split('/').pop().replace('.md', '');
    return `[${text}](/${path.replace('.md', '')})`;
  });
  // [[#锚点]] → 本地锚点
  content = content.replace(/\[\[#(.+?)\]\]/g, (m, anchor) => {
    return `[${anchor}](#${anchor})`;
  });
  return content;
}

// 遍历所有 md 文件处理
function processDir(dir) {
  fs.readdirSync(dir, { withFileTypes: true }).forEach(entry => {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) processDir(fullPath);
    else if (entry.name.endsWith('.md')) {
      const content = fs.readFileSync(fullPath, 'utf8');
      const converted = convertWikiLinks(content, fullPath);
      if (content !== converted) fs.writeFileSync(fullPath, converted);
    }
  });
}

processDir(wikiDir);
console.log('Wiki-link 转换完成！');
```

### 第5步：搜索配置

VitePress 内置的搜索（基于 minisearch）支持中文，只需在配置中开启：

```typescript
search: {
  provider: 'local',
  options: {
    locales: {
      root: {
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索知识库' }
        }
      }
    }
  }
}
```

### 第6步：部署（~10分钟）

**推荐：Vercel（免费，国内访问也较快）**

```bash
# 1. 登录 Vercel
npm i -g vercel
vercel

# 2. 或连接 GitHub 自动部署
# 将 website/ 推送到 GitHub 仓库
# 在 Vercel 导入该仓库即可
```

**备选：GitHub Pages**

```bash
# 在 vitepress config 中设置 base 路径
export default { base: '/liaokongjushi-wisdom/' }

# 部署
npm run docs:build
npx gh-pages -d docs/.vitepress/dist
```

---

## 五、可选的增强功能

> 如果基础站点搭建完毕后，你还想进一步升级：

### 1. 知识图谱（Knowledge Graph）

用 D3.js 或 vis.js 创建一个交互式网络图。节点是每个页面，连线是内部链接关系。用户点击一个节点就跳转到该页面。

数据来源：从 `grep -roh "\[\["` 结果中提取所有内部链接关系，生成 JSON 供前端加载。

### 2. 学习路径导览

在首页添加"下一步"指引。比如用户在阅读"对境不住"时，底部推荐"下一节：对法不执"或"相关专题：如何处理焦虑"。

### 3. AI问答集成

在网站右下角添加一个"问 AI"按钮，用户提问题时，LLM 基于知识库内容回答。可以使用 Vercel AI SDK + OpenAI API 实现，费用极低（你的知识库很小，每次回答消耗约 100 tokens）。

### 4. 随机金句小部件

首页顶部或侧边显示一句随机金句。每次刷新或每天更新一句。

---

## 六、时间估算

| 阶段 | 工作内容 | 预估时间 |
|------|---------|---------|
| 环境搭建 | 初始化 VitePress + 安装依赖 | 30分钟 |
| 内容迁移 | 复制文件 + 链接转换 | 1小时 |
| 配置导航 | 编写 config.ts + 侧边栏 | 1小时 |
| 样式调优 | 主题色 / 字体 / Logo | 1小时 |
| 测试 | 本地预览 + 检查所有链接 | 30分钟 |
| 部署 | Vercel / GitHub Pages | 10分钟 |
| **总计** | | **~4小时** |

---

## 七、几个关键决策点

**1. 要不要包含原始文章（01-Raw-Sources）？**
- 可选，11MB 的额外内容
- 建议：网站初期只包含 02-Wiki（400KB），原始文章留作后台参考
- 如果放, 可以使用"资料库"部分单独呈现

**2. 域名怎么处理？**
- 建议：先用 Vercel 免费域名 `*.vercel.app`
- 以后有需要再自定义域名，成本约 70元/年（.com / .cn）

**3. 会不会和 Obsidian 冲突？**
- 不会。Obsidian 知识库作为"编辑源头"，网站是"发布版本"
- 编辑流程：Obsidian 更新 → 运行转换脚本 → 提交 GitHub → 自动部署
- 两个系统独立但数据同步

---

> 写于 2026-05-06，基于知识库当前状态。
> 如果你选择方案A（VitePress），我可以立即开始搭建。
