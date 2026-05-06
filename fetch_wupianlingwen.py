#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取了空居士五篇灵文网站所有文章并合并到一个文档
"""

import subprocess
import re
import json
from datetime import datetime

def get_page_content(url):
    """获取网页内容"""
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        print(f"获取页面失败: {url}, 错误: {e}")
        return ""

def extract_title(html):
    """提取文章标题"""
    # 查找 h1 标签
    match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if match:
        title = match.group(1)
        # 清理HTML标签和多余空格
        title = re.sub(r'<[^>]+>', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        return title
    return "未知标题"

def extract_content(html):
    """提取文章正文内容"""
    # 查找 article.post 标签内的内容
    match = re.search(r'<article[^>]*class="post"[^>]*>(.*?)</article>', html, re.DOTALL)
    
    if match:
        content = match.group(1)
    else:
        # 备用方案：查找 content div
        match = re.search(r'<div[^>]*class="content"[^>]*>(.*?)</div>', html, re.DOTALL)
        if match:
            content = match.group(1)
        else:
            return ""
    
    # 清理脚本和样式
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<iframe[^>]*>.*?</iframe>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div[^>]*class="mainad"[^>]*>.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div[^>]*class="inner"[^>]*>\s*</div>', '', content, flags=re.DOTALL)
    
    # 转换为Markdown格式
    content = html_to_markdown(content)
    
    return content

def html_to_markdown(html):
    """将HTML转换为Markdown"""
    # 移除HTML标签但保留基本格式
    markdown = html
    
    # 移除div、span等无意义标签
    markdown = re.sub(r'</?div[^>]*>', '\n', markdown)
    markdown = re.sub(r'</?span[^>]*>', '', markdown)
    markdown = re.sub(r'</?font[^>]*>', '', markdown)
    markdown = re.sub(r'</?strong>', '', markdown)
    
    # 处理标题
    markdown = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n', markdown)
    markdown = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n', markdown)
    markdown = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n', markdown)
    markdown = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n', markdown)
    
    # 处理粗体
    markdown = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', markdown)
    markdown = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', markdown)
    
    # 处理斜体
    markdown = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', markdown)
    markdown = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', markdown)
    
    # 处理引用
    markdown = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1\n', markdown, flags=re.DOTALL)
    
    # 处理列表
    markdown = re.sub(r'<ul[^>]*>', '', markdown)
    markdown = re.sub(r'</ul>', '\n', markdown)
    markdown = re.sub(r'<ol[^>]*>', '', markdown)
    markdown = re.sub(r'</ol>', '\n', markdown)
    markdown = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', markdown)
    
    # 处理段落
    markdown = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', markdown)
    
    # 处理br
    markdown = re.sub(r'<br\s*/?>', '\n', markdown)
    
    # 清理所有剩余的HTML标签
    markdown = re.sub(r'<[^>]+>', '', markdown)
    
    # 清理HTML实体
    markdown = re.sub(r'&nbsp;', ' ', markdown)
    markdown = re.sub(r'&lt;', '<', markdown)
    markdown = re.sub(r'&gt;', '>', markdown)
    markdown = re.sub(r'&amp;', '&', markdown)
    markdown = re.sub(r'&quot;', '"', markdown)
    
    # 清理行首行尾空格
    lines = [line.strip() for line in markdown.split('\n')]
    markdown = '\n'.join(lines)
    
    # 在转换后清理网页导航相关内容
    patterns_to_remove = [
        r'明端根据千聊直播间[^\n]*请以直播语音为准。',
        r'免费打通大小周天[^\n]*微信：\d+',
        r'^\*\*\s*丹道\s*$',
        r'^\*<<\*没有了',
        r'^蔡衍颛先生讲解[^*]+\*>>\*$',
        r'^### \*\* 您可能还会对下面的文章感兴趣',
        r'^### \*\*随便看看',
        r'^蔡衍颛先生讲解《五篇灵文》[^\n]*$',
        r'^蔡衍颛先生讲解重阳祖师《最上一乘妙诀》$',
    ]
    
    for pattern in patterns_to_remove:
        markdown = re.sub(pattern, '', markdown, flags=re.MULTILINE)
    
    # 清理多余空行
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    return markdown.strip()

def main():
    # 所有文章ID
    article_ids = [2850, 2851, 2852, 2853, 2854, 2855, 2856, 2857, 2858, 2859, 2860, 2861, 2862, 2863]
    
    # 收集所有文章信息
    articles = []
    
    print(f"开始获取 {len(article_ids)} 篇文章...")
    
    for article_id in article_ids:
        url = f"http://www.liaokong.com/jingdianjiangjie/{article_id}.html"
        print(f"正在获取: {url}")
        
        html = get_page_content(url)
        if not html:
            print(f"  失败: 无法获取页面")
            continue
        
        title = extract_title(html)
        content = extract_content(html)
        
        if content:
            articles.append({
                'id': article_id,
                'url': url,
                'title': title,
                'content': content
            })
            print(f"  成功: {title} (长度: {len(content)} 字符)")
        else:
            print(f"  失败: 无法提取内容")
    
    print(f"\n成功获取 {len(articles)} 篇文章")
    
    # 生成Markdown文档
    now = datetime.now().strftime('%Y年%m月%d日')
    
    markdown_content = f"""# 五篇灵文与相关经典_了空居士_完整版

**来源**: [了空居士修行养生网](http://www.liaokong.com/)
**作者**: 了空居士(蔡衍颛)
**整理时间**: {now}
**文章数量**: {len(articles)}篇

---

## 目录

"""
    
    # 生成目录
    for i, article in enumerate(articles, 1):
        markdown_content += f"{i}. [{article['title']}](#{i}-{article['title'].replace(' ', '-')})\n"
    
    markdown_content += "\n---\n\n"
    
    # 生成正文
    for i, article in enumerate(articles, 1):
        markdown_content += f"# {i}. {article['title']}\n\n"
        markdown_content += f"**原文链接**: {article['url']}\n\n"
        markdown_content += "---\n\n"
        markdown_content += article['content']
        markdown_content += "\n\n---\n\n"
    
    markdown_content += """
---

## 说明

本文档整合了了空居士(蔡衍颛)关于《五篇灵文》、重阳祖师《最上一乘妙诀》以及《道德经》释义的系列文章。

**主要内容包括**:
- 《五篇灵文》六篇详解（包括序言）
- 重阳祖师《最上一乘妙诀》
- 《道德经》部分章节释义

**内容特点**:
- 原文准确呈现
- 逐句逐字释义
- 深入浅出讲解
- 结合现代视角

如有任何问题，请访问原作者网站: http://www.liaokong.com/
"""
    
    # 保存文件
    output_file = '/Users/panrui/WorkBuddy/Claw/五篇灵文_了空居士_完整版.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n文档已生成: {output_file}")
    print(f"总行数: {len(markdown_content.splitlines())}")

if __name__ == '__main__':
    main()
