#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理五篇灵文文档中的网页导航文字
"""

import re

def clean_content(content):
    """清理文档内容"""
    lines = content.split('\n')
    cleaned_lines = []
    skip_mode = False
    
    for line in lines:
        # 检查是否是需要删除的行
        skip_line = False
        
        # 整理说明
        if re.search(r'明端根据千聊直播间-了空居士与北斗七星-解读.*请以直播语音为准', line):
            skip_line = True
        
        # 微信联系方式
        if re.search(r'免费打通大小周天.*微信：\d+', line):
            skip_line = True
        
        # 分类标题单独一行
        if re.match(r'^\*\*\s*丹道\s*$', line):
            skip_line = True
        
        # 导航文字
        if re.search(r'\*<<\*没有了', line):
            skip_line = True
        
        # 上一篇/下一篇导航
        if re.search(r'蔡衍颛先生讲解.*\*>>\*', line):
            skip_line = True
        
        # 相关文章推荐标题
        if re.search(r'### \*\* 您可能还会对下面的文章感兴趣', line):
            skip_line = True
        
        if re.search(r'### \*\*随便看看', line):
            skip_line = True
        
        # 相关文章列表（单独一行）
        if re.match(r'^蔡衍颛先生讲解《五篇灵文》[^*]*$', line):
            skip_line = True
        
        if re.match(r'^蔡衍颛先生讲解重阳祖师《最上一乘妙诀》$', line):
            skip_line = True
        
        # 只有这些关键词的行
        if re.match(r'^\s*$', line) and skip_mode:
            # 如果在跳过模式中遇到空行，继续跳过
            cleaned_lines.append(line)
            skip_mode = False
            continue
        
        if not skip_line:
            cleaned_lines.append(line)
        
        skip_mode = skip_line
    
    # 合并行
    result = '\n'.join(cleaned_lines)
    
    # 清理多余的星号
    result = re.sub(r'\*{4,}', '', result)
    
    # 清理多余空行
    result = re.sub(r'\n{4,}', '\n\n\n', result)
    
    return result

def main():
    # 读取原文件
    input_file = '/Users/panrui/WorkBuddy/Claw/五篇灵文_了空居士_完整版.md'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"原始文档行数: {len(content.splitlines())}")
    print(f"原始文档字符数: {len(content)}")
    
    # 清理内容
    cleaned_content = clean_content(content)
    
    print(f"清理后文档行数: {len(cleaned_content.splitlines())}")
    print(f"清理后文档字符数: {len(cleaned_content)}")
    
    # 保存清理后的文件
    output_file = '/Users/panrui/WorkBuddy/Claw/五篇灵文_了空居士_完整版.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"\n文档已清理并保存: {output_file}")

if __name__ == '__main__':
    main()
