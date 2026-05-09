# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a structured knowledge base (Obsidian vault) for systematically studying the teachings of 了空居士 — a Zen/Buddhist teacher. The knowledge base applies a "model atom" methodology (inspired by Karpathy's LLM Wiki and Munger's mental models) to distill ~125 original articles into reusable wisdom principles.

The project also contains a VitePress website (`website/`) that publishes the structured knowledge as a static documentation site.

## Architecture: four-layer structure

```
00-Schema/        → Maintenance specs, workflows, lint rules (the "constitution")
01-Raw-Sources/   → ~125 original articles (immutable, read-only)
02-Wiki/          → Structured knowledge (LLM-maintained, 5-level navigation)
03-Output/        → Consumer-facing deliverables (guides, summaries, reports)
```

### Wiki five-level navigation (02-Wiki/)

| Dir | Layer | Content |
|-----|-------|---------|
| `10-核心模型/` | Models | 7 core mental models, each with "model atoms" |
| `20-专题研究/` | Topics | Deep-dive analysis combining multiple models |
| `30-学习路径/` | Paths | Learning roadmaps (cognitive path, problem path, beginner) |
| `40-原话金句/` | Quotes | Curated original quotes organized by classic text |
| `50-概念资料/` | Glossary | Terminology dictionary + source index + contradiction log |
| `99-运维/` | Ops | Cross-reference tables, quick links |

### Naming conventions

Files use prefixes to indicate their layer:
- `model-*.md` → core model pages
- `topic-*.md` → topic analysis pages
- `path-*.md`  → learning path pages
- `quote-*.md` → quote collections
- `dict-*.md`  → glossary entries
- `data-*.md`  → index/data files

Cross-references use Obsidian `[[wikilink]]` syntax within the vault.

## Key workflows (defined in 00-Schema/)

When asked to process new articles or maintain the knowledge base, follow these workflows:

1. **Ingest** (`ingest_workflow.md`): Read new articles → classify → create/update Wiki pages → add cross-references → update index.md and log.md
2. **Extract** (`extract_workflow.md`): Scan articles for "model atoms" (actionable principle statements) → cluster into core models → update model pages and quote pages
3. **Lint** (`lint_checklist.md`): Check for orphan pages, contradictions, stale content, missing cross-references, index consistency. Run after every 5-10 articles ingested.

## Website commands

The VitePress site lives in `website/`. Wiki content is copied to `website/docs/`.

```bash
# Install dependencies (first time)
cd website && npm install

# Convert Obsidian [[wikilinks]] to standard Markdown links for VitePress
cd website && node convert-links.js

# Start dev server
cd website && npx vitepress dev docs

# Build for production
cd website && npx vitepress build docs

# Preview production build
cd website && npx vitepress preview docs
```

### Wiki-link conversion

The `convert-links.js` script auto-maps prefix-only wikilinks to their correct directories:
- `[[model-xxx]]` → `[xxx](/10-核心模型/model-xxx)`
- `[[topic-xxx]]` → `[xxx](/20-专题研究/topic-xxx)`
- `[[dict-xxx]]`  → `[xxx](/50-概念资料/dict-xxx)`
- etc.

Always run `node convert-links.js` after copying or modifying wiki content in `website/docs/` before building.

## VitePress configuration

Config is at `website/docs/.vitepress/config.mts`. Key settings:
- Title: "了空居士智慧", language: zh-CN
- `cleanUrls: true`, `ignoreDeadLinks: true`
- Local search provider with Chinese UI translations
- Five-section navbar + sidebar matching the wiki layers

## Important notes

- `01-Raw-Sources/` is read-only — never modify original articles
- Wiki pages use `[[wikilink]]` syntax internally; the website version uses standard `[text](url)` after conversion
- Every wiki page should have: creation date, source attribution, related page links
- The `02-Wiki/log.md` tracks all maintenance activity in `## [YYYY-MM-DD] type | description` format
- Contradictions between sources are recorded in `02-Wiki/50-概念资料/data-矛盾记录.md`
