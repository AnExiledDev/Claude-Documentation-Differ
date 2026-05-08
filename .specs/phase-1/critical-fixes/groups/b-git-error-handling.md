---
group: B
title: Fix _run_git() silent error swallowing (1.2)
files:
  - lib/differ.py
---

## Acceptance Criteria

- [x] `_run_git()` checks `returncode` and raises `subprocess.CalledProcessError` on non-zero when `check=True` (default)
- [x] `_run_git()` accepts `check` parameter (default `True`) for callers that handle empty output
- [x] All existing callers reviewed — callers where failure is expected (e.g., no commits found) use `check=False`
- [x] Error messages include the git command that failed (for debugging)
