# Documentation Differ

Track changes to Claude documentation for discovering undocumented features.

## Overview

This tool monitors Claude documentation from multiple sources for changes, storing snapshots in a Git repository and generating AI-powered changelogs suitable for blog content about new/changed features.

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

# Check for changes since last fetch
python3 diff.py

# Generate AI-powered changelog
python3 diff.py --changelog
```

## Commands

### fetch.py

Fetches documentation pages from configured sources.

```bash
python3 fetch.py                          # Fetch all sources
python3 fetch.py --source claude-code     # Fetch Claude Code CLI docs only
python3 fetch.py --source api             # Fetch Claude API docs only
python3 fetch.py --check                  # Dry run - show what would be fetched
python3 fetch.py --force                  # Fetch even if recently run
```

### diff.py

Analyzes changes between documentation versions.

```bash
python3 diff.py                           # Analyze changes since last commit (all sources)
python3 diff.py --source claude-code      # Analyze Claude Code changes only
python3 diff.py --source api              # Analyze API changes only
python3 diff.py HEAD~5 HEAD               # Compare specific commits
python3 diff.py --changelog               # Generate AI-powered changelog
python3 diff.py --since 2026-02-01        # Changes since date
```

## Project Structure

```
documentation-differ/
├── fetch.py              # Main fetcher CLI
├── diff.py               # Diff analysis CLI
├── sources.py            # Source configuration
├── lib/
│   ├── fetcher.py        # Playwright fetching logic
│   ├── differ.py         # Git diff utilities
│   └── prompts/
│       ├── claude_code.md  # CLI-focused changelog prompt
│       └── api.md          # API-focused changelog prompt
├── docs/
│   ├── claude-code/      # Claude Code CLI documentation
│   │   ├── metadata.json
│   │   └── en/
│   │       ├── overview.md
│   │       ├── hooks.md
│   │       └── ...
│   └── api/              # Claude API documentation
│       ├── metadata.json
│       └── en/
│           ├── messages/
│           │   └── create.md
│           └── ...
├── output/
│   ├── claude-code/      # Claude Code changelogs
│   │   └── YYYY-MM-DD_changelog.md
│   └── api/              # API changelogs
│       └── YYYY-MM-DD_changelog.md
└── .github/workflows/
    ├── doc-differ.yml    # Claude Code workflow (every 6 hours)
    └── api-differ.yml    # Claude API workflow (every 48 hours)
```

## How It Works

1. **Fetch**: Playwright fetches all pages listed in each source's `llms.txt`
2. **Store**: Pages are saved as markdown in `docs/<source>/en/`
3. **Track**: Changes are tracked via Git commits
4. **Analyze**: `diff.py` uses Git to find what changed per source
5. **Changelog**: Claude Code CLI generates blog-ready changelogs with source-specific prompts

## Automation

Two GitHub Actions workflows monitor documentation:

| Workflow | File | Schedule | Source |
|----------|------|----------|--------|
| Claude Code | `doc-differ.yml` | Every 6 hours | `claude-code` |
| Claude API | `api-differ.yml` | Every 48 hours | `api` |

To enable:
1. Set `CLAUDE_CODE_OAUTH_TOKEN` secret in your GitHub repository
2. Push the workflow files

## Adding New Sources

To add a new documentation source:

1. Add entry to `sources.py`:
```python
SOURCES["new-source"] = Source(
    key="new-source",
    name="New Source",
    index_url="https://example.com/llms.txt",
    url_pattern=r"https://example\.com/docs/en/[\w/-]+\.md",
    prompt_file="lib/prompts/new_source.md",
    base_url="https://example.com",
)
```

2. Create prompt file in `lib/prompts/`
3. Create workflow file in `.github/workflows/`

## Requirements

- Python 3.11+
- Playwright (for fetching)
- GitPython (for diff analysis)
- Claude Code CLI (for changelog generation)
