#!/usr/bin/env python3
"""Audit the book source for the kinds of inconsistency that creep in when
chapters are written or edited separately.

Checks:
  1. structural   — every chapter carries the same furniture (lead paragraph,
                    derivation and worked-example boxes, closing section,
                    readings list, graded exercise sets, a gate)
  2. links        — every internal href resolves to a file that exists
  3. markup       — div balance, display-math delimiter balance, <details> pairs
  4. references   — every "Derivation N.M" cited in a chapter is defined in it
  5. solutions    — every B and C exercise has a matching solution in Appendix D
  6. prose        — chapter openings are not built from a single template

Run:  python3 tools/audit.py        (exit code 1 if anything fails)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

chapters = sorted(SRC.glob("chapter-*.html"))
appendices = sorted(SRC.glob("appendix-*.html"))
all_html = sorted(SRC.glob("*.html"))

problems = []


def ok(msg):
    print(f"  \033[32mok\033[0m   {msg}")


def bad(msg):
    problems.append(msg)
    print(f"  \033[31mFAIL\033[0m {msg}")


def text(p):
    return p.read_text()


# ---------------------------------------------------------------- 1. structure
print("\nstructure")
for p in chapters:
    t = text(p)
    n = p.stem[-2:]
    missing = []
    if 'class="lead"' not in t:
        missing.append("lead paragraph")
    if "box deriv" not in t and "box worked" not in t:
        missing.append("derivation/worked box")
    if "chapter bought" not in t and "book bought" not in t:
        missing.append("closing section")
    if 'class="readings"' not in t:
        missing.append("readings")
    if 'class="gate"' not in t:
        missing.append("gate")
    for label in ("A &middot; Drills", "B &middot; Problems", "C &middot; Challenge"):
        if label not in t:
            missing.append(label)
    if missing:
        bad(f"chapter {n} missing: {', '.join(missing)}")
if not problems:
    ok(f"all {len(chapters)} chapters carry the full template")

# ---------------------------------------------------------------- 2. links
print("\nlinks")
before = len(problems)
for p in all_html:
    for href in sorted(set(re.findall(r'href="([a-z0-9-]+\.html)"', text(p)))):
        if not (SRC / href).exists():
            bad(f"{p.name} -> {href} does not exist")
if len(problems) == before:
    ok("all internal links resolve")

# ---------------------------------------------------------------- 3. markup
print("\nmarkup")
before = len(problems)
for p in all_html:
    t = text(p)
    if t.count("<div") != t.count("</div>"):
        bad(f"{p.name}: div imbalance ({t.count('<div')}/{t.count('</div>')})")
    if t.count(r"\[") != t.count(r"\]"):
        bad(f"{p.name}: display-math delimiter imbalance")
    if t.count("<details>") != t.count("</details>"):
        bad(f"{p.name}: <details> imbalance")
if len(problems) == before:
    ok("div, math-delimiter and <details> pairs balanced in all files")

# ------------------------------------------------------------ 4. derivation refs
print("\nderivation references")
before = len(problems)
for p in chapters:
    t = text(p)
    defined = set(re.findall(r'<span class="label">Derivation ([0-9]+\.[0-9]+)', t))
    cited = set(re.findall(r"Derivation ([0-9]+\.[0-9]+)", t))
    dangling = cited - defined
    if dangling:
        bad(f"{p.name}: cites undefined {sorted(dangling)}")
if len(problems) == before:
    ok("every cited derivation is defined in its chapter")

# ---------------------------------------------------------------- 5. solutions
print("\nsolution coverage")
before = len(problems)
sol = text(SRC / "appendix-d.html")
sections = re.split(r'<h3 class="solch">', sol)
for p in chapters:
    t = text(p)
    num = str(int(p.stem[-2:]))
    def count_items(grade):
        m = re.search(grade + r"</p>(.*?)</div>", t, re.S)
        return len(re.findall(r"<li>", m.group(1))) if m else 0
    nb, nc = count_items("B &middot; Problems"), count_items("C &middot; Challenge")
    sec = next((s for s in sections if s.startswith(f"Chapter {num} &middot;")), None)
    if sec is None:
        bad(f"Appendix D has no section for chapter {num}")
        continue
    sb = len(re.findall(r'class="q">B-', sec))
    sc = len(re.findall(r'class="q">C-', sec))
    if (sb, sc) != (nb, nc):
        bad(f"chapter {num}: exercises B{nb}/C{nc} but solutions B{sb}/C{sc}")
if len(problems) == before:
    ok("every B and C exercise has a matching solution")

# ---------------------------------------------------------------- 6. prose
print("\nprose")
leads = []
for p in chapters:
    m = re.search(r'<p class="lead">(.*?)</p>', text(p), re.S)
    leads.append(re.sub(r"<[^>]+>", "", m.group(1)) if m else "")

templated = sum(1 for l in leads if "This chapter" in l)
callbacks = sum(1 for l in leads if re.match(r"(Chapter \d|Part I)", l))
first_words = {l.split()[0] for l in leads if l}

if templated > 2:
    bad(f"{templated}/{len(leads)} chapter openings use the phrase 'This chapter'")
elif callbacks > 3:
    bad(f"{callbacks}/{len(leads)} chapter openings begin with a chapter callback")
elif len(first_words) < len(leads) * 0.7:
    bad(f"only {len(first_words)} distinct opening words across {len(leads)} chapters")
else:
    ok(f"openings varied: {len(first_words)} distinct first words, "
       f"{templated} templated, {callbacks} callbacks")

# ---------------------------------------------------------------- summary
print()
if problems:
    print(f"\033[31m{len(problems)} problem(s)\033[0m")
    sys.exit(1)
print("\033[32mall checks passed\033[0m")
