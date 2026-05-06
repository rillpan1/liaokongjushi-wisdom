#!/bin/bash

# 获取了空居士网站上道德经释义的所有内容
# 创建时间: 2026-03-11

BASE_URL="http://www.liaokong.com"
OUTPUT_FILE="/Users/panrui/WorkBuddy/Claw/道德经释义_了空居士.md"

# 清空输出文件
echo "# 道德经释义" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "**来源**: 了空居士修行养生网 (http://www.liaokong.com)" >> "$OUTPUT_FILE"
echo "**作者**: 了空居士(蔡衍颛)" >> "$OUTPUT_FILE"
echo "**整理时间**: 2026年3月11日" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 所有文章的链接列表
ARTICLES=(
"/jingdianjiangjie/2857.html"
"/jingdianjiangjie/2858.html"
"/jingdianjiangjie/2859.html"
"/jingdianjiangjie/2860.html"
"/jingdianjiangjie/2861.html"
"/jingdianjiangjie/2862.html"
"/jingdianjiangjie/2863.html"
"/jingdianjiangjie/2864.html"
"/jingdianjiangjie/2865.html"
"/jingdianjiangjie/2866.html"
"/jingdianjiangjie/2867.html"
"/jingdianjiangjie/2868.html"
"/jingdianjiangjie/2869.html"
"/jingdianjiangjie/2870.html"
"/jingdianjiangjie/2871.html"
"/jingdianjiangjie/2872.html"
"/jingdianjiangjie/2873.html"
"/jingdianjiangjie/2874.html"
"/jingdianjiangjie/2875.html"
"/jingdianjiangjie/2876.html"
"/jingdianjiangjie/2877.html"
"/jingdianjiangjie/2878.html"
"/jingdianjiangjie/2879.html"
)

# 计数器
count=0
total=${#ARTICLES[@]}

# 获取每篇文章
for article in "${ARTICLES[@]}"; do
    count=$((count + 1))
    echo "正在获取第 $count/$total 篇文章..."

    url="${BASE_URL}${article}"

    # 获取页面内容并提取正文部分
    content=$(curl -s -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" "$url" 2>/dev/null)

    # 提取标题
    title=$(echo "$content" | grep '<h1 class="post-title">' | sed 's/.*<h1 class="post-title">\(.*\)<\/h1>.*/\1/' | sed 's/<[^>]*>//g')

    # 提取正文内容 (在 <div class="entry"> 之后的部分)
    body=$(echo "$content" | sed -n '/<div class="entry">/,/<\/div>/p' | sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g' | sed 's/&lt;/</g' | sed 's/&gt;/>/g' | sed 's/&amp;/\&/g')

    # 写入文件
    echo "## $title" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "$body" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    sleep 1  # 避免请求过快
done

echo "完成!所有内容已保存到: $OUTPUT_FILE"
