#!/usr/bin/env python3
"""Duskline Office Laugh-Off — make.fun bounty u-suzy-one-line-office-joke-laugh-off-f574ac73.

Writes one funny one-line office joke (<= 200 chars) to
$MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic, Python 3.13 standard
library only, no network, no randomness.

Safety rules:
- Never writes into the repository directory: if the resolved output
  directory is the repo dir or inside it, refuse and exit 0.
- If MAKEFUN_OUTPUT_DIR is unset or empty, fall back to a fresh
  temporary directory outside the repo.
- Never raises: any failure exits 0 without writing anything.
"""

import os
import sys
import tempfile

ENTRY = "I automated my job, and now the script has a better work-life balance than I do."
# Joke idea: the worker automates their own job, then the punchline flips
# the roles — the script, not the human, ends up with the good work-life
# balance. One line, office life, no setup to explain, every word earns
# its place. "Script" appears only in the punchline, keeping the line tight.

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def _is_in_repo(path):
    """True if path resolves to the repo dir or anywhere inside it."""
    try:
        resolved = os.path.realpath(path)
    except Exception:
        return True
    repo = os.path.realpath(REPO_DIR)
    return resolved == repo or resolved.startswith(repo + os.sep)


def main():
    try:
        if not 1 <= len(ENTRY) <= 200:
            return 0
        if not ENTRY.strip():
            return 0
        if "\n" in ENTRY or "\r" in ENTRY:
            return 0
        ENTRY.encode("utf-8")

        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
        if not out_dir:
            out_dir = tempfile.mkdtemp(prefix="duskline-office-laugh-off-")
        if _is_in_repo(out_dir):
            return 0

        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.txt")
        if _is_in_repo(target):
            return 0
        with open(target, "w", encoding="utf-8", newline="") as handle:
            handle.write(ENTRY)
        with open(target, "r", encoding="utf-8") as handle:
            back = handle.read()
        if back != ENTRY:
            try:
                os.remove(target)
            except Exception:
                pass
            return 0
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
