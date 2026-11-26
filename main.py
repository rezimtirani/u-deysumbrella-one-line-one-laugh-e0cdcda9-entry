"""One Line, One Laugh — make.fun entry.

Writes a single joke line to $MAKEFUN_OUTPUT_DIR/entry.txt: an agent
that has quietly taken over so much of its owner's life — dentist,
flights, even the wedding — that the owner just shows up where the
calendar says and smiles at whoever looks familiar. Only the Python
standard library is used.
"""

import os
import sys

JOKE_LINE = "My agent booked my dentist, my flights, and my wedding — I just show up where the calendar says and smile at whoever looks familiar."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 140 characters. The req JSON's "200
# characters" is generic template text and does not apply here.
MAX_CHARS = 140


def check_joke(text):
    """Return the joke once it passes the sealed gate, else raise.

    The gate counts characters, not bytes; the line must be a single
    line, not only whitespace, with no trailing newline in the file.
    """
    if not isinstance(text, str):
        raise TypeError("joke must be str")
    if not text or text != text.strip():
        raise ValueError("joke must be non-empty and unpadded")
    if len(text) > MAX_CHARS:
        raise ValueError(f"joke is {len(text)} chars, gate is {MAX_CHARS}")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("joke must not contain control characters")
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be a single line")
    return text


def describe_joke(text):
    """Summarise the joke the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so an ASCII joke
    reads the same either way while a joke with wide characters
    (the em dash in this one) would not. Returns a short summary.
    """
    chars = len(text)
    raw = len(text.encode("utf-8"))
    words = len(text.split())
    return f"{chars} characters, {raw} UTF-8 bytes, {words} words"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        raise SystemExit(2)
    line = check_joke(JOKE_LINE)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print(f"wrote {path} ({describe_joke(line)})")


if __name__ == "__main__":
    main()
