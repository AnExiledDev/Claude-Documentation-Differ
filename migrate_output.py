#!/usr/bin/env python3
"""One-time migration: move flat output files into date subdirectories.

Moves files like:
  output/claude-code/2026-02-05_changelog.md → output/claude-code/2026-02-05/changelog.md
  output/api/2026-02-15_agents-and-tools_changelog.md → output/api/2026-02-15/agents-and-tools_changelog.md

Uses `git mv` so git tracks the renames.
"""

import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_(.+)$")


def migrate_source(source_dir: Path) -> int:
    """Migrate flat files in a source output directory into date subdirs.

    Returns number of files moved.
    """
    if not source_dir.exists():
        return 0

    moved = 0
    for filepath in sorted(source_dir.iterdir()):
        if not filepath.is_file():
            continue

        match = DATE_PREFIX_RE.match(filepath.name)
        if not match:
            continue

        date_str = match.group(1)
        rest = match.group(2)

        date_dir = source_dir / date_str
        date_dir.mkdir(exist_ok=True)

        new_path = date_dir / rest
        if new_path.exists():
            print(f"  SKIP (exists): {filepath.name} → {date_str}/{rest}")
            continue

        result = subprocess.run(
            ["git", "mv", str(filepath), str(new_path)],
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  ERROR: git mv {filepath.name}: {result.stderr.strip()}")
        else:
            print(f"  {filepath.name} → {date_str}/{rest}")
            moved += 1

    return moved


def main() -> None:
    total = 0
    for source_key in ("claude-code", "api"):
        source_dir = OUTPUT_DIR / source_key
        print(f"\nMigrating {source_key}/")
        count = migrate_source(source_dir)
        print(f"  Moved {count} files")
        total += count

    print(f"\nTotal: {total} files migrated")
    if total == 0:
        print("Nothing to do.")
        sys.exit(0)


if __name__ == "__main__":
    main()
