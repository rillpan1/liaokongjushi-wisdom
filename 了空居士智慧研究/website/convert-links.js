/**
 * convert-links.js v2 — 将 Obsidian Wiki-link 转为标准 Markdown 链接
 * 
 * 核心改进: 对无路径前缀的链接（如 [[model-对境不住]]）自动补充目录
 * 
 * 目录映射:
 *   model-*  -> /10-核心模型/model-*
 *   topic-*  -> /20-专题研究/topic-*
 *   path-*   -> /30-学习路径/path-*
 *   quote-*  -> /40-原话金句/quote-*
 *   dict-*   -> /50-概念资料/dict-*
 *   data-*   -> /50-概念资料/data-*
 *   其他     -> 保持原样
 */

const fs = require('fs');
const path = require('path');

const docsDir = path.join(__dirname, 'docs');
const excludeDirs = ['.vitepress'];

// 前缀 → 目录映射
const prefixMap = {
  'model-': '10-核心模型',
  'topic-': '20-专题研究',
  'path-':  '30-学习路径',
  'quote-': '40-原话金句',
  'dict-':  '50-概念资料',
  'data-':  '50-概念资料',
};

function getFullPath(linkPath) {
  // 如果已经是完整路径（包含 /），直接处理
  if (linkPath.includes('/')) {
    // 去掉 .md 扩展名
    let clean = linkPath.replace(/\.md$/, '');
    // 去掉前缀的 ../ 和目录引用
    clean = clean.replace(/^(?:\.\.\/)*(?:10-核心模型|20-专题研究|30-学习路径|40-原话金句|50-概念资料|03-Output|99-运维|01-Raw-Sources)\//, '');
    return clean;
  }
  
  // 无路径前缀的链接，通过前缀推断目录
  for (const [prefix, dir] of Object.entries(prefixMap)) {
    if (linkPath.startsWith(prefix)) {
      const name = linkPath.replace(/\.md$/, '');
      return `${dir}/${name}`;
    }
  }
  
  // 未知前缀，去掉 .md 扩展名
  return linkPath.replace(/\.md$/, '');
}

function getDisplayText(linkPath) {
  const clean = linkPath.replace(/\.md$/, '');
  // 如果有路径，取最后一段
  if (clean.includes('/')) {
    return clean.split('/').pop();
  }
  return clean;
}

function convertWikiLinks(content, filePath) {
  // 1. [[链接|显示文本]] -> [显示文本](/路径)
  content = content.replace(/\[\[([^|#\]]+?)\|(.+?)\]\]/g, (match, linkPath, text) => {
    const fullPath = getFullPath(linkPath);
    return `[${text}](/${fullPath})`;
  });

  // 2. [[链接]] -> [显示文本](/路径)
  content = content.replace(/\[\[([^#\]]+?)\]\]/g, (match, linkPath) => {
    const fullPath = getFullPath(linkPath);
    const text = getDisplayText(linkPath);
    return `[${text}](/${fullPath})`;
  });

  // 3. [[#锚点]] -> 本地锚点
  content = content.replace(/\[\[#(.+?)\]\]/g, (match, anchor) => {
    return `[${anchor}](#${anchor})`;
  });

  return content;
}

function processDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    
    if (entry.isDirectory()) {
      if (!excludeDirs.includes(entry.name)) {
        processDir(fullPath);
      }
    } else if (entry.name.endsWith('.md')) {
      try {
        const content = fs.readFileSync(fullPath, 'utf8');
        const converted = convertWikiLinks(content, fullPath);
        
        if (content !== converted) {
          fs.writeFileSync(fullPath, converted);
          const relPath = path.relative(docsDir, fullPath);
          const changes = countChanges(content, converted);
          console.log(`  ✓ ${relPath} (${changes} 处替换)`);
        } else {
          const relPath = path.relative(docsDir, fullPath);
          console.log(`  - ${relPath} (无变更)`);
        }
      } catch (err) {
        console.error(`  ✗ ${fullPath}: ${err.message}`);
      }
    }
  }
}

function countChanges(original, modified) {
  const origLines = original.split('\n');
  const modLines = modified.split('\n');
  let changes = 0;
  const maxLen = Math.max(origLines.length, modLines.length);
  for (let i = 0; i < maxLen; i++) {
    if (origLines[i] !== modLines[i]) changes++;
  }
  return changes;
}

console.log('开始转换 Wiki-link v2 (智能补全路径)...\n');
processDir(docsDir);
console.log('\n转换完成！');
