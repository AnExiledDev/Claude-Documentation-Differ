# Documentation Differ

Track changes to Claude Code documentation for discovering undocumented features.

## Overview

This tool monitors [Claude Code documentation](https://code.claude.com/docs/en/) for changes, storing snapshots in a Git repository and generating AI-powered changelogs suitable for blog content about new/changed features.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Fetch all documentation
python3 fetch.py

# Check for changes since last fetch
python3 diff.py

# Generate AI-powered changelog
python3 diff.py --changelog
```

## Commands

### fetch.py

Fetches all documentation pages from the Claude Code docs.

```bash
python3 fetch.py                # Fetch latest docs
python3 fetch.py --check        # Dry run - show what would be fetched
python3 fetch.py --changelog    # Fetch and generate changelog if changed
python3 fetch.py --force        # Fetch even if recently run
```

### diff.py

Analyzes changes between documentation versions.

```bash
python3 diff.py                 # Analyze changes since last commit
python3 diff.py HEAD~5 HEAD     # Compare specific commits
python3 diff.py --changelog     # Generate AI-powered changelog
python3 diff.py --since 2026-02-01  # Changes since date
```

## Project Structure

```
documentation-differ/
├── fetch.py              # Main fetcher CLI
├── diff.py               # Diff analysis CLI
├── lib/
│   ├── fetcher.py        # Playwright fetching logic
│   ├── differ.py         # Git diff utilities
│   └── changelog_prompt.md  # AI changelog prompt
├── docs/                 # Git repo with documentation snapshots
│   └── en/               # English documentation
│       ├── overview.md
│       ├── hooks.md
│       └── ...
└── output/               # Generated changelogs
    └── YYYY-MM-DD_changelog.md
```

## How It Works

1. **Fetch**: Playwright fetches all pages listed in [llms.txt](https://code.claude.com/docs/llms.txt)
2. **Store**: Pages are saved as markdown in `docs/en/`
3. **Track**: The `docs/` folder is a Git repo, automatically committing changes
4. **Analyze**: `diff.py` uses Git to find what changed
5. **Changelog**: Claude Code CLI generates blog-ready changelogs

## Automation

The included GitHub Actions workflow runs every 6 hours:
- Fetches latest documentation
- Commits any changes to the docs repo
- Generates a changelog if changes detected

To enable:
1. Set `ANTHROPIC_API_KEY` secret in your GitHub repository
2. Push the `.github/workflows/doc-differ.yml` file

## Requirements

- Python 3.11+
- Playwright (for fetching)
- GitPython (for diff analysis)
- Claude Code CLI (for changelog generation)
