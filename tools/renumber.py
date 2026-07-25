#!/usr/bin/env python3
"""One-shot: shift Chapters 2-16 up by one to make room for the new Chapter 2.

Run once, from the repository root, then delete. Changes numbers and nothing
else -- no prose, no markup, no content. Every replacement happens in a single
pass with a callback, so nothing cascades (2 -> 3 -> 4).

Two classes of hazard, both handled explicitly:

  * Reading annotations cite *other people's* sections and chapters. Legg's
    "Chapters 2-4" and Sutskever's "Section 3.3" must not move. Bare "Section 4"
    and "Figure 2" are never touched at all; dotted "Section N.M" inside a
    reading moves only when N is that file's own chapter number, which is what
    distinguishes our Section 9.3 from their Section 3.3.
  * Docs that describe the *first* edition -- HISTORY, the review, the plan --
    are records and are left alone. NUMBERS, DECISIONS and STYLE describe the
    book as it stands and move with it.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LO, HI = 2, 16          # chapters that shift
SENTINEL = "\x00%d\x00"

# Literals that look like our numbering and are not. Protected verbatim.
PROTECTED = [
    "Chapters 2&ndash;4 for the measure",        # Legg, Machine Super Intelligence
    "Section 3.3 is the reversal trick",         # Sutskever et al., seq2seq
]

EXTRA = ["src/index.html", "build/assemble.py", "README.md",
         "docs/NUMBERS.md", "docs/DECISIONS.md", "docs/STYLE.md"]


def shift(n):
    n = int(n)
    return n + 1 if LO <= n <= HI else n


def renumber(text, own_chapter):
    for i, lit in enumerate(PROTECTED):
        text = text.replace(lit, SENTINEL % i)

    # Readings cite external work; hold them aside for the rules that need it.
    hows = re.findall(r'<span class="how">.*?</span>', text, re.S)
    for i, h in enumerate(hows):
        text = text.replace(h, f"\x01{i}\x01", 1)

    # ONE alternation, ONE pass. Anything matched here cannot be matched again,
    # which is what stops "## Chapter 13" or "Ch. 14&ndash;16" being shifted twice
    # by two rules that both claim it.
    RANGE = r"\s*(?:through|and|&ndash;|&mdash;|-)\s*"
    COMBINED = re.compile(
        r"(?P<file>chapter-\d{2}\.html)"
        r"|(?P<chrange>Chapters \d+" + RANGE + r"\d+)"
        r"|(?P<ch>Chapter \d+)"
        r"|(?P<dotted>(?:Derivation|Worked Example|Drill|Sections?) \d+\.\d+)"
        r"|(?P<gate>Gate \d+)"
        r"|(?P<chabbrrange>Ch\. \d+\s*&ndash;\s*\d+)"
        r"|(?P<chabbr>Ch\. \d+)"
        r"|(?P<head><h2>\d+\.\d+)"
        r'|(?P<toc>min-width:2\.4em;font-weight:600">\d+</span>)')

    def bump(m):
        s = m.group(0)
        kind = m.lastgroup
        if kind == "file":
            return re.sub(r"\d+", lambda d: f"{shift(d.group()):02d}", s, count=1)
        if kind == "head":
            # the "2" in "<h2>" is not a chapter number
            return re.sub(r"(<h2>)(\d+)(\.)",
                          lambda d: f"{d.group(1)}{shift(d.group(2))}{d.group(3)}", s)
        if kind == "toc":
            # careful: this span also contains "2.4em", which is not a chapter
            return re.sub(r'(">)(\d+)(</span>)',
                          lambda d: f"{d.group(1)}{shift(d.group(2))}{d.group(3)}", s)
        if kind in ("chrange", "chabbrrange"):
            return re.sub(r"\d+", lambda d: str(shift(d.group())), s)
        # everything else: the number is the last run of digits before any dot part
        return re.sub(r"(\d+)", lambda d: str(shift(d.group(1))), s, count=1)

    text = COMBINED.sub(bump, text)

    # Put the readings back, renumbering only what is demonstrably ours.
    for i, h in enumerate(hows):
        own = own_chapter
        def bump_reading(m):
            s = m.group(0)
            kind = m.lastgroup
            if kind == "chrange":
                return re.sub(r"\d+", lambda d: str(shift(d.group())), s)
            if kind == "dotted":
                # a dotted section inside a reading is ours only when it names
                # this file's own chapter; otherwise it is the source's own
                n = int(re.search(r"(\d+)\.", s).group(1))
                if s.startswith("Section") and own is not None and n != own:
                    return s
                if s.startswith("Section") and own is None:
                    pass  # appendices: dotted sections are always ours
            return re.sub(r"(\d+)", lambda d: str(shift(d.group(1))), s, count=1)

        fixed = re.compile(
            r"(?P<chrange>Chapters \d+" + RANGE + r"\d+)"
            r"|(?P<ch>Chapter \d+)"
            r"|(?P<dotted>(?:Derivation|Worked Example|Sections?) \d+\.\d+)").sub(
            bump_reading, h)
        text = text.replace(f"\x01{i}\x01", fixed, 1)

    for i, lit in enumerate(PROTECTED):
        text = text.replace(SENTINEL % i, lit)
    return text


def main():
    # This has already been run. It is kept as the record of what WP1 did to
    # the numbering; running it again would shift the book a second time.
    if (ROOT / "src" / "chapter-17.html").exists():
        sys.exit("already renumbered: chapter-17.html exists. Refusing to run again.")

    # Rename files first, descending, so nothing is overwritten.
    for n in range(HI, LO - 1, -1):
        src = ROOT / "src" / f"chapter-{n:02d}.html"
        dst = ROOT / "src" / f"chapter-{n + 1:02d}.html"
        if dst.exists():
            sys.exit(f"refusing to overwrite {dst}")
        src.rename(dst)
        print(f"  {src.name} -> {dst.name}")

    targets = []
    for p in sorted((ROOT / "src").glob("chapter-*.html")):
        n = int(p.stem[-2:])
        # after the rename this file holds what used to be chapter n-1
        targets.append((p, 1 if n == 1 else n - 1))
    targets += [(p, None) for p in sorted((ROOT / "src").glob("appendix-*.html"))]
    targets += [(ROOT / rel, None) for rel in EXTRA]

    for path, own in targets:
        if not path.exists():
            sys.exit(f"missing {path}")
        before = path.read_text()
        after = renumber(before, own)
        if after != before:
            path.write_text(after)
            print(f"  renumbered {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
