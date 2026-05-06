# 道德经释义文档生成指南

## 项目概述

本项目旨在整理了空居士修行养生网(http://www.liaokong.com)上关于《道德经》的释义内容,并生成PDF文档。

## 网站信息

- **网站名称**: 了空居士修行养生网
- **网址**: http://www.liaokong.com/daodejing/
- **作者**: 了空居士(蔡衍颛)
- **内容数量**: 23篇文章,涵盖《道德经》81章
- **内容类型**: 原文、释义、师父开示

## 文档结构

已创建的文档示例包含了以下内容:

1. **标题页**: 包含来源、作者、整理时间等信息
2. **目录**: 23篇文章的完整列表
3. **示例内容**: 前五章的详细释义内容作为示例
4. **附录**: 关于作者的介绍和联系方式

## 获取完整内容的步骤

### 方法一: 手动复制粘贴(推荐用于小量内容)

1. 访问 http://www.liaokong.com/daodejing/
2. 逐篇打开23篇文章
3. 复制每篇文章的内容
4. 粘贴到Markdown文档中
5. 保存文档

### 方法二: 使用提供的脚本(批量获取)

#### Bash脚本版本

```bash
# 1. 给脚本添加执行权限
chmod +x fetch_daodejing.sh

# 2. 执行脚本
./fetch_daodejing.sh

# 3. 脚本会自动获取所有内容并保存到:
# /Users/panrui/WorkBuddy/Claw/道德经释义_了空居士.md
```

#### Python脚本版本

```bash
# 1. 安装依赖(如果需要)
pip3 install requests beautifulsoup4

# 2. 执行脚本
python3 fetch_daodejing.py

# 3. 脚本会自动获取所有内容并保存到:
# /Users/panrui/WorkBuddy/Claw/道德经释义_了空居士.md
```

## 转换为PDF的步骤

### 方法一: 使用Pandoc(推荐)

```bash
# 1. 安装Pandoc
# macOS: brew install pandoc
# Ubuntu/Debian: sudo apt-get install pandoc

# 2. 转换为PDF
pandoc 道德经释义_了空居士.md -o 道德经释义_了空居士.pdf \
  --pdf-engine=xelatex \
  -V mainfont="SimSun" \
  -V CJKmainfont="SimSun" \
  -V geometry:margin=2.5cm \
  --toc \
  --toc-depth=2 \
  --number-sections
```

### 方法二: 使用Typora

1. 打开Typora
2. 打开Markdown文档
3. 选择"文件" → "导出" → "PDF"
4. 调整格式设置
5. 导出PDF

### 方法三: 使用VS Code

1. 安装Markdown PDF插件
2. 打开Markdown文档
3. 右键选择"Markdown PDF: Export (pdf)"
4. 保存PDF文件

### 方法四: 在线转换

访问以下在线转换网站:
- https://www.markdowntopdf.com/
- https://www.cloudconvert.com/md-to-pdf

## 文章链接列表

所有23篇文章的链接:

1. http://www.liaokong.com/jingdianjiangjie/2857.html - 道德经释义——第一章至五章
2. http://www.liaokong.com/jingdianjiangjie/2858.html - 道德经释义——第六章至十章
3. http://www.liaokong.com/jingdianjiangjie/2859.html - 道德经释义——第十一章至十五章
4. http://www.liaokong.com/jingdianjiangjie/2860.html - 道德经释义——第十六章至二十章
5. http://www.liaokong.com/jingdianjiangjie/2861.html - 道德经释义——第二十一章至二十三章
6. http://www.liaokong.com/jingdianjiangjie/2862.html - 道德经释义——第二十四章至二十六章
7. http://www.liaokong.com/jingdianjiangjie/2863.html - 道德经释义——第二十七章至三十章
8. http://www.liaokong.com/jingdianjiangjie/2864.html - 道德经释义——第三十一章至三十四章
9. http://www.liaokong.com/jingdianjiangjie/2865.html - 道德经释义——第三十五章至三十七章
10. http://www.liaokong.com/jingdianjiangjie/2866.html - 道德经释义——第三十八章至四十一章
11. http://www.liaokong.com/jingdianjiangjie/2867.html - 道德经释义——第四十二章至四十五章
12. http://www.liaokong.com/jingdianjiangjie/2868.html - 道德经释义——第四十六章至四十八章
13. http://www.liaokong.com/jingdianjiangjie/2869.html - 道德经释义——第四十九章至五十二章
14. http://www.liaokong.com/jingdianjiangjie/2870.html - 道德经释义——第五十三章至五十六章
15. http://www.liaokong.com/jingdianjiangjie/2871.html - 道德经释义——第五十七章至六十章
16. http://www.liaokong.com/jingdianjiangjie/2872.html - 道德经释义——第六十一章至六十三章
17. http://www.liaokong.com/jingdianjiangjie/2873.html - 道德经释义——第六十四章至六十七章
18. http://www.liaokong.com/jingdianjiangjie/2874.html - 道德经释义——第六十八章至七十章
19. http://www.liaokong.com/jingdianjiangjie/2875.html - 道德经释义——第七十一章至七十三章
20. http://www.liaokong.com/jingdianjiangjie/2876.html - 道德经释义——第七十四章至七十六章
21. http://www.liaokong.com/jingdianjiangjie/2877.html - 道德经释义——第七十七章至七十九章
22. http://www.liaokong.com/jingdianjiangjie/2878.html - 道德经释义——第八十章至八十一章
23. http://www.liaokong.com/jingdianjiangjie/2879.html - 道德经补充说明

## 注意事项

1. **版权声明**: 请尊重原作者的版权,整理的内容仅用于个人学习参考
2. **内容准确性**: 请以原网站为准,整理过程中可能出现格式错误
3. **技术限制**: 由于网络或网站限制,部分内容可能无法完全获取
4. **字体问题**: 转换为PDF时注意中文字体设置,避免乱码

## 故障排除

### 问题1: 脚本无法执行

**解决方案**:
```bash
# 检查脚本权限
ls -l fetch_daodejing.sh

# 添加执行权限
chmod +x fetch_daodejing.sh

# 检查Python版本
python3 --version

# 如果需要,安装依赖
pip3 install requests beautifulsoup4
```

### 问题2: 网站访问失败

**解决方案**:
- 检查网络连接
- 尝试手动访问网站确认可用性
- 检查是否需要设置代理

### 问题3: PDF转换失败

**解决方案**:
- 确保已安装LaTeX(使用Pandoc时)
- 检查中文字体是否正确安装
- 尝试使用不同的转换工具

### 问题4: 中文乱码

**解决方案**:
```bash
# Pandoc转换时指定中文字体
pandoc 道德经释义_了空居士.md -o 道德经释义_了空居士.pdf \
  --pdf-engine=xelatex \
  -V CJKmainfont="SimSun"
```

## 进阶选项

### 自定义PDF样式

创建`style.tex`文件:

```latex
\usepackage{xeCJK}
\setCJKmainfont{SimSun}
\setmainfont{Times New Roman}
\setlength{\parskip}{1em}
\setlength{\parindent}{0em}
```

然后使用:

```bash
pandoc 道德经释义_了空居士.md -o 道德经释义_了空居士.pdf \
  --pdf-engine=xelatex \
  -H style.tex
```

### 添加目录页码

```bash
pandoc 道德经释义_了空居士.md -o 道德经释义_了空居士.pdf \
  --toc \
  --toc-depth=2 \
  --number-sections
```

## 联系方式

如有问题或建议,请联系原网站:
- 网站: http://www.liaokong.com
- QQ: 519702412
- 微信: 13715860608

---

**创建日期**: 2026年3月11日
**最后更新**: 2026年3月11日
**版本**: 1.0
