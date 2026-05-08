---
group: B
title: Fix _run_git() silent error swallowing (1.2)
files:
  - lib/differ.py
---

## Acceptance Criteria

- [ ] `_run_git()` checks `returncode` and raises `subprocess.CalledProcessError` on non-zero when `check=True` (default)
- [ ] `_run_git()` accepts `check` parameter (default `True`) for callers that handle empty output
- [ ] All existing callers reviewed — callers where failure is expected (e.g., no commits found) use `check=False`
- [ ] Error messages include the git command that failed (for debugging)
