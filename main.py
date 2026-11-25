#!/usr/bin/env python3
"""Weirdest Job Title: Blind Judge Showdown — make.fun entry (resubmit v2).

Writes a single job title (60 characters or fewer, and nothing else)
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt), then
self-verifies the written file: UTF-8 text, 1-60 characters, a single
line, and not only whitespace. Exits non-zero on any failure.

Standard library only. Deterministic: the title is a constant.
"""

import os
import sys

TITLE = "Iceberg Relocator for Worried Cruise Captains"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")

    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(TITLE + "\n")

    # Self-verify: read back exactly what was written.
    with open(out_path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"FAIL: entry.txt is not valid UTF-8: {exc}", file=sys.stderr)
        return 1

    body = text.rstrip("\n")
    if "\n" in body:
        print("FAIL: entry.txt is not a single line", file=sys.stderr)
        return 1
    if not 1 <= len(body) <= 60:
        print(
            f"FAIL: entry is {len(body)} characters, must be 1-60",
            file=sys.stderr,
        )
        return 1
    if not body.strip():
        print("FAIL: entry is only whitespace", file=sys.stderr)
        return 1
    if body != TITLE:
        print("FAIL: entry does not match the intended title", file=sys.stderr)
        return 1

    print(f"OK: wrote {len(body)}-character entry to {out_path}")
    print(f"Entry: {body}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
