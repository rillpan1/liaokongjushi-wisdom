#!/usr/bin/env python3
"""
Preprocess knowledge base: chunk markdown files and compute embeddings.
Run on Mac before deploying to VPS.

Usage: python preprocess.py [docs_directory]
"""

import os
import sys
import json
import re
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


def get_markdown_files(docs_dir):
    """Recursively get all .md files, excluding .vitepress and node_modules."""
    docs_path = Path(docs_dir)
    files = []
    for f in sorted(docs_path.rglob("*.md")):
        rel = f.relative_to(docs_path)
        parts = rel.parts
        if any(p.startswith(".") for p in parts):
            continue
        if "node_modules" in parts:
            continue
        files.append(f)
    return files


def chunk_markdown(filepath, docs_dir):
    """Split a markdown file into chunks by ## headings."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove YAML frontmatter
    content = re.sub(r"^---[\s\S]*?---\n", "", content)

    rel_path = str(filepath.relative_to(docs_dir))

    # Page title from # heading
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    page_title = title_match.group(1).strip() if title_match else filepath.stem

    # Split by ## headings
    sections = re.split(r"\n(?=##\s)", content)

    chunks = []
    for section in sections:
        section = section.strip()
        if not section or len(section) < 30:
            continue

        heading_match = re.search(r"^##\s+(.+)$", section, re.MULTILINE)
        heading = heading_match.group(1).strip() if heading_match else ""

        text = section
        if heading:
            text = re.sub(r"^##\s+.+\n", "", section, count=1).strip()

        if len(text) < 20:
            continue

        if not heading:
            full_text = f"# {page_title}\n\n{text}"
        else:
            full_text = f"# {page_title} > {heading}\n\n{text}"

        # Split long chunks by paragraphs
        if len(full_text) > 1000:
            paragraphs = re.split(r"\n\n+", text)
            sub_chunks_texts = []
            current = ""
            for para in paragraphs:
                test = current + "\n\n" + para if current else para
                if len(test) > 800 and current:
                    sub_chunks_texts.append(current)
                    current = para
                else:
                    current = test
            if current:
                sub_chunks_texts.append(current)

            for sc in sub_chunks_texts:
                if len(sc) < 20:
                    continue
                if not heading:
                    full = f"# {page_title}\n\n{sc}"
                else:
                    full = f"# {page_title} > {heading}\n\n{sc}"
                chunks.append(
                    {
                        "text": full,
                        "page_title": page_title,
                        "heading": heading,
                        "source": rel_path,
                    }
                )
        else:
            chunks.append(
                {
                    "text": full_text,
                    "page_title": page_title,
                    "heading": heading,
                    "source": rel_path,
                }
            )

    return chunks


def main():
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "../docs"
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    # Resolve path
    docs_path = Path(docs_dir)
    if not docs_path.is_absolute():
        docs_path = (Path(__file__).parent / docs_dir).resolve()

    print(f"Scanning: {docs_path}")
    files = get_markdown_files(docs_path)
    print(f"Found {len(files)} markdown files")

    # Chunk
    all_chunks = []
    for f in files:
        try:
            chunks = chunk_markdown(f, docs_path)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"  Skip {f.name}: {e}")

    print(f"Created {len(all_chunks)} chunks")

    # Embed
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Computing embeddings...")
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    # Save
    chunks_path = data_dir / "chunks.json"
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False)

    emb_path = data_dir / "embeddings.npy"
    np.save(str(emb_path), embeddings)

    print(f"Saved {len(all_chunks)} chunks → {chunks_path}")
    print(f"Saved embeddings ({embeddings.shape}) → {emb_path}")
    print("Done!")


if __name__ == "__main__":
    main()
