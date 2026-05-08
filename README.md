# Documentation Differ

Track changes to Claude documentation and generate AI-powered changelogs.

## Overview

This tool monitors Anthropic's Claude documentation for changes, stores snapshots in Git, and uses Claude Code CLI to generate structured changelogs suitable for blog content about new and changed features.

### Supported Sources

| Source | Description | Pages | Schedule |
|--------|-------------|-------|----------|
| `claude-code` | [Claude Code CLI docs](https://code.claude.com/docs/en/) | ~54 | Every 6 hours |
| `api` | [Claude API docs](https://platform.claude.com/docs/en/) | ~539 | Every 48 hours |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Fetch all documentation sources
python3 fetch.py

# Fetch a specific source
python3 fetch.py --source claude-code
python3 fetch.py --source api

# Check for changes (diff report only)
python3 diff.py

# Generate AI-powered changelog
python3 diff.py --changelog --source claude-code
```

## Requirements

- **Python 3.11+**
- **Playwright** — headless browser for fetching documentation pages
- **Node.js 18+** — required for the Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)
- **Git** — used via subprocess for diff analysis and change tracking

## Commands

### fetch.py

Fetches documentation pages from configured sources using Playwright.

```bash
python3 fetch.py                              # Fetch all sources
python3 fetch.py --source claude-code         # Fetch Claude Code CLI docs only
python3 fetch.py --source api                 # Fetch Claude API docs only
python3 fetch.py --check                      # Dry run — show what would be fetched
python3 fetch.py --force                      # Fetch even if recently run
python3 fetch.py --rate-limit 2.0             # Seconds between requests (default: 1.0)
python3 fetch.py --cooldown-hours 2           # Min hours between fetches (default: 1)
```

### diff.py

Analyzes changes between documentation versions and optionally generates changelogs.

```bash
python3 diff.py                               # Analyze all sources (uncommitted changes)
python3 diff.py --source claude-code          # Analyze Claude Code changes only
python3 diff.py HEAD~5 HEAD                   # Compare specific commits
python3 diff.py --changelog                   # Generate AI-powered changelog
python3 diff.py --since 2026-02-01            # Changes since date
python3 diff.py --since-last-changelog        # Changes since last changelog commit
python3 diff.py --model sonnet                # Force a specific model
python3 diff.py --budget 10.00               # Override budget cap (USD)
python3 diff.py --max-search-days 60          # Extend changelog commit search window
```

## Architecture

```
Fetch → Store → Diff → Triage → Changelog → Daily Merge
```

1. **Fetch**: Playwright fetches all pages listed in each source's `llms.txt` index
2. **Store**: Pages are saved as markdown in `docs/<source>/en/`
3. **Track**: Changes are tracked via Git commits with source-specific messages
4. **Diff**: Git diff analysis produces a structured change report
5. **Triage**: Rule-based pre-classification tags changes as SIGNIFICANT, MINOR, or SKIP based on heuristics (new/removed pages, heading changes, line count thresholds)
6. **Changelog**: Claude Code CLI generates a structured changelog, informed by triage classifications. Model selection is dynamic based on estimated token count.
7. **Daily Merge**: An end-of-day workflow synthesizes partial changelogs into a single `daily.md`

### Dynamic Model Selection

Token estimation runs after diff analysis to choose the right model:

| Estimated Tokens | Model | Budget Cap |
|-----------------|-------|------------|
| < 100k | `sonnet` | $6.00 |
| 100k–180k | `sonnet` (aggressive truncation) | $6.00 |
| > 180k | `sonnet[1m]` | $24.00 |

For large diffs (>10 changes), the diff is split by category. Each category gets its own independent model selection based on its token estimate.

## Project Structure

```
documentation-differ/
├── fetch.py                  # Fetcher CLI
├── diff.py                   # Diff analysis + changelog CLI
├── sources.py                # Source configuration (dataclass registry)
├── lib/
│   ├── differ.py             # Git diff utilities (subprocess-based)
│   ├── fetcher.py            # Playwright fetching logic
│   ├── tokens.py             # Token estimation + model selection
│   ├── triage.py             # Rule-based change triage
│   └── prompts/
│       ├── claude_code.md    # Claude Code changelog prompt
│       ├── api.md            # API changelog prompt
│       └── daily_merge.md    # Daily merge synthesis prompt
├── tests/                    # pytest suite (106 tests)
├── docs/
│   ├── claude-code/          # Claude Code CLI doc snapshots
│   │   ├── metadata.json
│   │   └── en/
│   └── api/                  # Claude API doc snapshots
│       ├── metadata.json
│       └── en/
├── output/
│   ├── claude-code/
│   │   ├── index.md                          # Auto-generated TOC
│   │   └── YYYY-MM-DD/
│   │       ├── daily.md                      # AI-synthesized daily summary
│   │       ├── partial_00h_changelog.md      # 00:00 UTC run
│   │       ├── partial_06h_changelog.md      # 06:00 UTC run
│   │       └── diff.md                       # Structured diff report
│   └── api/
│       └── (same structure)
├── .github/workflows/
│   ├── differ-reusable.yml   # Reusable workflow (shared logic)
│   ├── doc-differ.yml        # Claude Code caller (every 6h)
│   ├── api-differ.yml        # API caller (every 48h)
│   └── daily-merge.yml       # Daily changelog merge (23:55 UTC)
├── requirements.txt          # Runtime dependencies
└── requirements-dev.txt      # Dev dependencies (pytest)
```

## Automation

Four GitHub Actions workflows handle monitoring and synthesis:

| Workflow | File | Schedule | Purpose |
|----------|------|----------|---------|
| Claude Code Differ | `doc-differ.yml` | Every 6 hours | Fetch + diff + changelog for Claude Code docs |
| API Differ | `api-differ.yml` | Every 48 hours | Fetch + diff + changelog for API docs |
| Reusable Differ | `differ-reusable.yml` | (called by above) | Shared workflow logic |
| Daily Merge | `daily-merge.yml` | 23:55 UTC daily | Synthesize partial changelogs into `daily.md` |

All workflows share a `differ-push` concurrency group to prevent simultaneous pushes to main.

### Setup

1. **Repository secret**: Set `CLAUDE_CODE_OAUTH_TOKEN` in your GitHub repository settings (Settings → Secrets and variables → Actions). This is an OAuth token for Claude Code CLI, used for headless changelog generation.

2. **Claude Code CLI**: The workflow installs a pinned version of `@anthropic-ai/claude-code` via npm. The `--dangerously-skip-permissions` flag is required for headless (non-interactive) mode; `--allowedTools Read,Write` restricts the actual tool surface to file operations only.

3. **Push the workflow files** and the bot will begin monitoring on schedule.

## Adding New Sources

1. Add an entry to `sources.py`:
```python
SOURCES["new-source"] = Source(
    key="new-source",
    name="New Source",
    index_url="https://example.com/llms.txt",
    url_pattern=r"https://example\.com/docs/en/[\w/-]+\.md",
    prompt_file="lib/prompts/new_source.md",
    base_url="https://example.com",
    commit_label="New Source",
)
```

2. Create a prompt file in `lib/prompts/`
3. Create a caller workflow in `.github/workflows/` (use `differ-reusable.yml`)

## Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --tb=short -q
```
