#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取了空居士网站上道德经释义的所有内容
"""

import requests
import re
from bs4 import BeautifulSoup
import time

BASE_URL = "http://www.liaokong.com"
OUTPUT_FILE = "/Users/panrui/WorkBuddy/Claw/道德经释义_了空居士.md"

# 所有文章的链接列表
ARTICLES = [
    "/jingdianjiangjie/2857.html",
    "/jingdianjiangjie/2858.html",
    "/jingdianjiangjie/2859.html",
    "/jingdianjiangjie/2860.html",
    "/jingdianjiangjie/2861.html",
    "/jingdianjiangjie/2862.html",
    "/jingdianjiangjie/2863.html",
    "/jingdianjiangjie/2864.html",
    "/jingdianjiangjie/2865.html",
    "/jingdianjiangjie/2866.html",
    "/jingdianjiangjie/2867.html",
    "/jingdianjiangjie/2868.html",
    "/jingdianjiangjie/2869.html",
    "/jingdianjiangjie/2870.html",
    "/jingdianjiangjie/2871.html",
    "/jingdianjiangjie/2872.html",
    "/jingdianjiangjie/2873.html",
    "/jingdianjiangjie/2874.html",
    "/jingdianjiangjie/2875.html",
    "/jingdianjiangjie/2876.html",
    "/jingdianjiangjie/2877.html",
    "/jingdianjiangjie/2878.html",
    "/jingdianjiangjie/2879.html",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

def get_article_content(url):
    """获取单篇文章的内容"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取标题
        title = soup.find('h1', class_='post-title')
        if title:
            title = title.get_text().strip()
        else:
            title = "未知标题"

        # 提取正文内容
        content_div = soup.find('div', class_='entry')
        if content_div:
            # 清理HTML标签,保留文本
            content = content_div.get_text(separator='\n', strip=True)
            # 移除多余的空行
            content = re.sub(r'\n\s*\n', '\n\n', content)
        else:
            content = "无法获取内容"

        return title, content
    except Exception as e:
        return "错误", f"获取失败: {str(e)}"

def main():
    """主函数"""
    # 创建输出文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 道德经释义\n\n")
        f.write("**来源**: 了空居士修行养生网 (http://www.liaokong.com)\n")
        f.write("**作者**: 了空居士(蔡衍颛)\n")
        f.write("**整理时间**: 2026年3月11日\n\n")
        f.write("---\n\n")

    # 获取每篇文章
    total = len(ARTICLES)
    for i, article in enumerate(ARTICLES, 1):
        print(f"正在获取第 {i}/{total} 篇文章...")

        url = BASE_URL + article
        title, content = get_article_content(url)

        # 追加到文件
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(f"## {title}\n\n")
            f.write(f"{content}\n\n")
            f.write("---\n\n")

        time.sleep(1)  # 避免请求过快

    print(f"完成!所有内容已保存到: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
