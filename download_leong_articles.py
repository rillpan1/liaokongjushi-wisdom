#!/usr/bin/env python3
"""
下载"了空居士智慧宝库"全部文章到本地
正确鉴权方式：ima-openapi-clientid / ima-openapi-apikey
"""

import os
import json
import time
import urllib.request
import urllib.error
import urllib.parse

# ====== 配置 ======
CLIENT_ID = open(os.path.expanduser("~/.config/ima/client_id")).read().strip()
API_KEY = open(os.path.expanduser("~/.config/ima/api_key")).read().strip()
KB_ID = "XBfJSuMQuiseQsMfiuWOC4E-tPvuTbwW1jwVpkyRmQc="
BASE_URL = "https://ima.qq.com"
OUTPUT_DIR = "/Users/panrui/WorkBuddy/Claw/了空居士智慧宝库"
# =====================


def api_call(path, body, extra_headers=None):
    """调用 IMA OpenAPI，返回解析后的 JSON dict"""
    url = BASE_URL + path
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "ima-openapi-clientid": CLIENT_ID,
        "ima-openapi-apikey": API_KEY,
        "ima-openapi-ctx": "skill_version=1.1.7",
    }
    if extra_headers:
        headers.update(extra_headers)

    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="ignore")
        print(f"  HTTP {e.code}: {body_text[:200]}")
        return None
    except Exception as e:
        print(f"  请求异常: {e}")
        return None


def get_all_items():
    """分页获取知识库全部文章列表"""
    all_items = []
    cursor = ""
    page = 0
    while True:
        page += 1
        print(f"📄 获取第 {page} 页...")
        body = {"knowledge_base_id": KB_ID, "cursor": cursor, "limit": 50}
        result = api_call("/openapi/wiki/v1/get_knowledge_list", body)
        if not result or result.get("code") != 0:
            print(f"  ❌ 获取失败: {result}")
            break

        data = result["data"]
        items = data.get("knowledge_list", [])
        all_items.extend(items)
        print(f"  本页 {len(items)} 篇，累计 {len(all_items)} 篇")

        if data.get("is_end", True):
            break
        cursor = data.get("next_cursor", "")
        if not cursor:
            break
        time.sleep(0.3)

    return all_items


def get_media_info(media_id):
    """获取媒体信息（含内容下载 URL）"""
    return api_call("/openapi/wiki/v1/get_media_info", {"media_id": media_id})


def download_url(url):
    """下载 URL 内容，返回 (bytes, 实际URL)"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read(), resp.geturl()


def decode_content(raw_bytes):
    """尝试用多种编码解码字节流"""
    for enc in ["utf-8", "gbk", "gb2312", "big5", "latin-1"]:
        try:
            return raw_bytes.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw_bytes.decode("utf-8", errors="replace")


def sanitize_filename(name):
    """清理文件名非法字符"""
    for ch in ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\n', '\r']:
        name = name.replace(ch, '_')
    return name.strip()[:200]  # 限制长度


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("📚 开始下载「了空居士智慧宝库」全部文章")
    print("=" * 60)

    # 第一步：获取全部文章列表
    items = get_all_items()
    total = len(items)
    print(f"\n✅ 共获取 {total} 篇文章列表\n")

    if total == 0:
        print("没有找到任何文章，退出。")
        return

    # 分类统计
    type_counts = {}
    for item in items:
        mt = item.get("media_type", 0)
        type_counts[mt] = type_counts.get(mt, 0) + 1
    print(f"📊 文章类型统计: {type_counts}")
    print()

    # 第二步：逐篇下载内容
    success = 0
    failed = 0
    skipped = 0
    all_articles = []  # (title, content) 用于合并

    for i, item in enumerate(items, 1):
        media_id = item.get("media_id", "")
        title = item.get("title", f"未命名_{i}")
        media_type = item.get("media_type", 0)

        print(f"[{i}/{total}] {title} (type={media_type})")

        # 只处理 markdown(type=7) 和 笔记(type=11)
        if media_type != 7 and media_type != 11:
            print(f"  ⚠️  跳过（类型 {media_type} 不支持）")
            skipped += 1
            continue

        # 调用 get_media_info
        info_result = get_media_info(media_id)
        if not info_result or info_result.get("code") != 0:
            print(f"  ❌ get_media_info 失败: {info_result}")
            failed += 1
            continue

        data = info_result.get("data", {})

        # --- media_type=7: markdown 文件 ---
        if media_type == 7:
            url_info = data.get("url_info", {})
            content_url = url_info.get("url", "")
            if not content_url:
                print(f"  ⚠️  无下载链接，跳过")
                failed += 1
                continue

            try:
                raw_bytes, _ = download_url(content_url)
                content = decode_content(raw_bytes)
            except Exception as e:
                print(f"  ❌ 下载失败: {e}")
                failed += 1
                continue

        # --- media_type=11: 笔记类型 ---
        elif media_type == 11:
            notebook_ext_info = data.get("notebook_ext_info", {})
            note_id = (notebook_ext_info.get("note_id") or
                       notebook_ext_info.get("notebook_id", ""))
            if not note_id:
                print(f"  ⚠️  笔记无 note_id，跳过")
                skipped += 1
                continue
            # 笔记内容需通过 notes API 获取，暂存引用
            content = f"[笔记类型 note_id={note_id}，需通过 notes API 获取]"
            # TODO: 调用 notes API 获取完整内容

        # 保存单文件
        safe_title = sanitize_filename(title)
        single_path = os.path.join(OUTPUT_DIR, f"{safe_title}.md")
        try:
            with open(single_path, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n{content}\n")
            print(f"  ✅ 已保存")
            success += 1
            all_articles.append((title, content))
        except Exception as e:
            print(f"  ❌ 保存失败: {e}")
            failed += 1

        time.sleep(0.3)

    # 第三步：写入合并文件
    combined_path = os.path.join(OUTPUT_DIR, "了空居士智慧宝库_全集.md")
    print(f"\n📝 写入合并文件: {os.path.basename(combined_path)}")
    try:
        with open(combined_path, "w", encoding="utf-8") as f:
            f.write("# 了空居士智慧宝库（全集）\n\n")
            f.write(f"> 共 {total} 篇文章，成功下载 {success} 篇\n\n")
            for title, content in all_articles:
                f.write(f"\n\n---\n\n## {title}\n\n{content}\n")
        print(f"  ✅ 合并文件已写入")
    except Exception as e:
        print(f"  ❌ 合并文件写入失败: {e}")

    # 完成统计
    print("\n" + "=" * 60)
    print("🎉 下载完成！")
    print(f"  成功: {success}")
    print(f"  失败: {failed}")
    print(f"  跳过: {skipped}")
    print(f"  输出目录: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
