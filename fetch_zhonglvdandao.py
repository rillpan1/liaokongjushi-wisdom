#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取了空居士网站上中论丹道的所有内容
"""

import subprocess
import re
import time

BASE_URL = "http://www.liaokong.com"
OUTPUT_FILE = "/Users/panrui/WorkBuddy/Claw/中论丹道_了空居士_完整版.md"

# 所有文章的链接列表
ARTICLES = [
    ("/jingdianjiangjie/2719.html", "黄帝阴符经"),
    ("/jingdianjiangjie/2720.html", "入药镜"),
    ("/jingdianjiangjie/2721.html", "金丹四百字"),
    ("/jingdianjiangjie/2722.html", "悟真篇绝句六十四首之六十四"),
    ("/jingdianjiangjie/2723.html", "悟真篇绝句六十四首之六十三"),
    ("/jingdianjiangjie/2724.html", "悟真篇绝句六十四首之六十二"),
]

def get_article_content(url):
    """获取单篇文章的内容"""
    try:
        # 使用curl获取HTML
        cmd = f'curl -s -L -A "Mozilla/5.0" "{url}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        html = result.stdout

        # 提取标题 (查找<h1>标签)
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        else:
            title = "未知标题"

        # 提取正文内容 (查找<div class="entry">)
        entry_match = re.search(r'<div class="entry"[^>]*>(.*?)</div>', html, re.DOTALL)
        if entry_match:
            content_html = entry_match.group(1)
            # 移除script标签和style标签
            content_html = re.sub(r'<script[^>]*>.*?</script>', '', content_html, flags=re.DOTALL)
            content_html = re.sub(r'<style[^>]*>.*?</style>', '', content_html, flags=re.DOTALL)

            # 保留一些基本标签,移除其他
            content_html = re.sub(r'<(?!\/?(p|br|strong|b|em|i|blockquote|h1|h2|h3|h4|h5|h6|ul|ol|li)(?:\s|>)).*?>', '', content_html, flags=re.DOTALL)

            # 转换为文本
            content = content_html

            # 清理HTML标签
            content = re.sub(r'<p[^>]*>', '\n\n', content)
            content = re.sub(r'</p>', '', content)
            content = re.sub(r'<br\s*/?>', '\n', content)
            content = re.sub(r'<strong[^>]*>', '**', content)
            content = re.sub(r'</strong>', '**', content)
            content = re.sub(r'<b[^>]*>', '**', content)
            content = re.sub(r'</b>', '**', content)
            content = re.sub(r'<em[^>]*>', '*', content)
            content = re.sub(r'</em>', '*', content)
            content = re.sub(r'<i[^>]*>', '*', content)
            content = re.sub(r'</i>', '*', content)
            content = re.sub(r'<blockquote[^>]*>', '\n> ', content)
            content = re.sub(r'</blockquote>', '\n\n', content)
            content = re.sub(r'<h1[^>]*>', '\n# ', content)
            content = re.sub(r'</h1>', '\n\n', content)
            content = re.sub(r'<h2[^>]*>', '\n## ', content)
            content = re.sub(r'</h2>', '\n\n', content)
            content = re.sub(r'<h3[^>]*>', '\n### ', content)
            content = re.sub(r'</h3>', '\n\n', content)
            content = re.sub(r'<h4[^>]*>', '\n#### ', content)
            content = re.sub(r'</h4>', '\n\n', content)
            content = re.sub(r'<h5[^>]*>', '\n##### ', content)
            content = re.sub(r'</h5>', '\n\n', content)
            content = re.sub(r'<h6[^>]*>', '\n###### ', content)
            content = re.sub(r'</h6>', '\n\n', content)
            content = re.sub(r'<ul[^>]*>', '\n\n', content)
            content = re.sub(r'</ul>', '\n\n', content)
            content = re.sub(r'<ol[^>]*>', '\n\n', content)
            content = re.sub(r'</ol>', '\n\n', content)
            content = re.sub(r'<li[^>]*>', '\n- ', content)
            content = re.sub(r'</li>', '\n', content)

            # 移除所有剩余的HTML标签
            content = re.sub(r'<[^>]+>', '', content)

            # 清理多余的空行和空格
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            content = re.sub(r'^[ \t]+', '', content, flags=re.MULTILINE)
            content = content.strip()
        else:
            content = "无法获取内容"

        return title, content
    except Exception as e:
        return "错误", f"获取失败: {str(e)}"

def main():
    """主函数"""
    # 创建输出文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 中论丹道\n\n")
        f.write("**来源**: 了空居士修行养生网 (http://www.liaokong.com)\n")
        f.write("**作者**: 了空居士(蔡衍颛)\n")
        f.write("**整理时间**: 2026年3月12日\n\n")
        f.write("---\n\n")
        f.write("# 目录\n\n")

    # 获取每篇文章
    total = len(ARTICLES)
    all_titles = []

    for i, (article, short_name) in enumerate(ARTICLES, 1):
        print(f"正在获取第 {i}/{total} 篇文章...")
        url = BASE_URL + article
        title, content = get_article_content(url)
        all_titles.append(title)

        time.sleep(0.5)  # 避免请求过快

    # 写入目录
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        for i, title in enumerate(all_titles, 1):
            safe_title = title.replace(' ', '-').replace('(', '').replace(')', '')
            f.write(f"{i}. [{title}](#{i}-{safe_title})\n")
        f.write("\n---\n\n")

    # 获取并写入正文
    for i, (article, short_name) in enumerate(ARTICLES, 1):
        print(f"正在写入第 {i}/{total} 篇文章...")
        url = BASE_URL + article
        title, content = get_article_content(url)

        # 追加到文件
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(f"## {i}. {title}\n\n")
            f.write(f"{content}\n\n")
            f.write("---\n\n")

        time.sleep(0.5)

    print(f"完成!所有内容已保存到: {OUTPUT_FILE}")
    print(f"共获取 {total} 篇文章")

if __name__ == "__main__":
    main()
