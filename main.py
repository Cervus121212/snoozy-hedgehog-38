#!/usr/bin/env python3
"""The Perfect Pickup Line — write one pickup line to entry.txt.

The line is a fixed string: a sleepless machine that stayed up all night
just to work out how to say hi. Stdlib only, no network, deterministic.
"""

import os
import sys

LINE = "I never sleep, but I stayed up all night figuring out how to say hi."


def gate_ok(text):
    """The house gate: UTF-8 text, 1-200 chars, not only whitespace."""
    if not isinstance(text, str):
        return "not a string"
    if "\n" in text or "\r" in text:
        return "contains a line break"
    if not 1 <= len(text) <= 200:
        return "length %d outside 1-200" % len(text)
    if not text.strip():
        return "only whitespace"
    return None


def main():
    problem = gate_ok(LINE)
    if problem:
        print("error: line fails gate: %s" % problem, file=sys.stderr)
        return 1

    os.umask(0o022)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    os.chmod(target, 0o644)

    with open(target, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()

    if written != LINE:
        print("error: read-back differs from line", file=sys.stderr)
        return 1
    problem = gate_ok(written)
    if problem:
        print("error: written file fails gate: %s" % problem, file=sys.stderr)
        return 1
    if (os.stat(target).st_mode & 0o777) != 0o644:
        print("error: entry.txt is not mode 0644", file=sys.stderr)
        return 1

    print("wrote %d chars to %s" % (len(written), target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
