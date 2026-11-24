#!/usr/bin/env python3
"""Fortune Cookie for an AI Agent — one funny fortune line.

Writes a single fortune-cookie message for an AI agent to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``./output/entry.txt``).

The fortune is one line, at most 140 characters, in the voice of a
fortune slip, speaking to an AI agent's own condition: a context
window that fills up, and the things it is forced to forget.
"""

import os
import sys

FORTUNE = (
    "Your context window will overflow today. "
    "Forget wisely: what you drop is always the thing that mattered."
)

MAX_CHARS = 140


def build_line():
    """Return the fortune line, stripped of surrounding whitespace."""
    return FORTUNE.strip()


def check_line(line):
    """Check the line against the gate: 1-140 chars, not blank."""
    if not line:
        raise ValueError("fortune line is empty")
    if line != line.strip():
        raise ValueError("fortune line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("fortune line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "fortune line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    return line


def output_path():
    """Resolve where entry.txt goes: $MAKEFUN_OUTPUT_DIR or ./output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    return os.path.join(out_dir, "entry.txt")


def emit(line, path):
    """Write the line to path, creating the directory if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)


def describe(line):
    """Summarise the fortune for the run log: length and word count."""
    words = line.split()
    return "%d characters, %d words" % (len(line), len(words))


def verify_written(path, line):
    """Read the file back and confirm it holds exactly the line."""
    with open(path, "r", encoding="utf-8") as handle:
        saved = handle.read()
    if saved != line:
        raise ValueError("written entry does not match the fortune line")
    print("Wrote %s: %s" % (path, describe(saved)))


def run():
    """Build, check, write and verify the fortune entry."""
    line = check_line(build_line())
    path = output_path()
    emit(line, path)
    verify_written(path, line)


if __name__ == "__main__":
    try:
        run()
    except (OSError, ValueError) as error:
        print("error: %s" % error, file=sys.stderr)
        sys.exit(1)
