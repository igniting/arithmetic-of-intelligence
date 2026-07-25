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
  7. back-refs    — "Chapter N's X" actually points at something Chapter N says
  8. bank         — Appendix A entries are one-per-chapter and not over-bundled
  9. labs         — every lab follows the derivation it verifies
 10. readings     — every reading annotation names where in the source to look

Run:  python3 tools/audit.py        (exit code 1 if anything fails)
"""
import collections
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
defined_anywhere = set()
for p in chapters:
    defined_anywhere |= set(
        re.findall(r'<span class="label">Derivation ([0-9]+\.[0-9]+)', text(p)))
for p in chapters:
    t = text(p)
    own = int(p.stem[-2:])
    defined = set(re.findall(r'<span class="label">Derivation ([0-9]+\.[0-9]+)', t))
    for c in sorted(set(re.findall(r"Derivation ([0-9]+\.[0-9]+)", t))):
        # a chapter's own derivations must be defined in it; a derivation from
        # another chapter may be cited, but must exist somewhere
        if int(c.split(".")[0]) == own:
            if c not in defined:
                bad(f"{p.name}: cites undefined Derivation {c}")
        elif c not in defined_anywhere:
            bad(f"{p.name}: cites Derivation {c}, which no chapter defines")
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

# ---------------------------------------------------------------- 7. back-refs
# A chapter that says "Chapter N's X" is making a checkable claim: that Chapter N
# contains X. Two such claims in the first edition were false (Chapter 5 credited
# Chapter 1 with the matrix-multiply cost; Chapter 8 credited it with Bayes'
# rule), and neither is visible from inside either chapter. The test picks the
# rarest content word in the referenced phrase and asks whether the target
# chapter uses it. Matching is on a four-letter prefix, which is deliberately
# permissive: this check should never cry wolf.
print("\nback-references")
before = len(problems)

STOP = set("""a an the of in on at to for from by with and or as is are was were be been
being that this these those it its their our your we you they i one two three same other
another such which what when where how why not no any all both each every some into over
under about after before during than then so if but do does did have has had book chapter
chapters part section sections above below here there now new own very more most much many
few little just also only even still yet already again once first second third result
results argument arguments idea ideas thing things way ways point points fact facts value
values number numbers quantity quantities case cases form forms use uses using used account
notion treatment discussion version story picture account statement claim claims""".split())
VERB = set("""makes make made uses use used gives give gave shows show showed tells tell told
says say said puts put turns turn turned lets let becomes become came comes come does do
did prices price priced counts count counted""".split())
KEY = 4


def flat(p):
    t = p.read_text()
    t = re.sub(r"<style.*?</style>|<script.*?</script>", " ", t, flags=re.S)
    return re.sub(r"<[^>]+>", " ", t)


bodies = {int(p.stem[-2:]): flat(p).lower() for p in chapters}
vocab = {n: {w[:KEY] for w in re.findall(r"[a-z]{2,}", t)} for n, t in bodies.items()}
docfreq = collections.Counter()
for v in vocab.values():
    docfreq.update(v)

_W = r"[A-Za-z][A-Za-z0-9-]*"
REFS = [
    (rf"Chapter (\d+)'s ((?:{_W} ){{0,2}}{_W})", 0),
    (rf"the ((?:{_W}[ -]){{0,2}}{_W}) (?:of|from) Chapter (\d+)", 1),
    (rf"Chapter (\d+) (?:introduced|prepared|drilled|computed|answered|gave us) "
     rf"(?:the |a |us )?((?:{_W} ){{0,2}}{_W})", 0),
]

for p in chapters:
    src, t = int(p.stem[-2:]), flat(p)
    for pattern, order in REFS:
        for m in re.finditer(pattern, t):
            a, b = m.group(1), m.group(2)
            target, phrase = (int(a), b) if order == 0 else (int(b), a)
            if target == src or target not in bodies:
                continue
            words = [w for w in re.findall(r"[a-z]{3,}", phrase.lower())
                     if w not in STOP and w not in VERB]
            if len(words) < 2:
                continue
            heads = [w[:KEY] for w in words]
            rarest = min(docfreq[h] for h in heads)
            keys = sorted({h for h in heads if docfreq[h] == rarest})
            if not any(k in vocab[target] for k in keys):
                bad(f"chapter {src:02d} credits Chapter {target} with "
                    f"'{phrase.strip()}' — no such wording there")
if len(problems) == before:
    ok("every 'Chapter N's X' back-reference lands on something Chapter N says")

# ---------------------------------------------------------------- 8. bank
# Appendix A is the declared syllabus, so its entries must be atomised evenly:
# one chapter each, every chapter represented, and no entry carrying more
# results than the chapter has boxes to teach them in.
print("\nderivation bank")
before = len(problems)
bank = text(SRC / "appendix-a.html")
entries = re.findall(
    r'<span class="bnum">(\d+)</span>.*?<span class="bch">\s*Ch\.?\s*([0-9–—,\s-]+)</span>',
    bank, re.S)
per_chapter = collections.Counter()
for num, tag in entries:
    named = [int(x) for x in re.findall(r"\d+", tag)]
    if len(named) > 1:
        bad(f"bank entry {num} spans Chapters {tag.strip()} — one entry per chapter")
    for c in named:
        per_chapter[c] += 1
for p in chapters:
    n = int(p.stem[-2:])
    if n <= 2:
        continue  # Part I is toolkit and vocabulary, not bank material
    if per_chapter[n] == 0:
        bad(f"chapter {n} has no entry in the derivation bank")
        continue
    boxes = text(p).count("box deriv") + text(p).count("box worked")
    if per_chapter[n] > boxes:
        bad(f"chapter {n}: {per_chapter[n]} bank entries but only {boxes} "
            f"derivation/worked boxes to teach them")
if len(problems) == before:
    ok(f"{len(entries)} bank entries, one chapter each, all chapters covered")

# ---------------------------------------------------------------- 9. labs
# A lab's acceptance criterion is a number its derivation predicts, so the lab
# must not run before that derivation — nor long after it, which is the failure
# the first edition had.
print("\nlab anchoring")
before = len(problems)
labs = re.split(r'<span class="lnum">Lab ', text(SRC / "appendix-c.html"))[1:]
for block in labs:
    n = block.split("&middot;", 1)[0].strip()
    m = re.search(r"alongside Chapter (\d+)", block)
    cited = {int(x) for x in re.findall(r"Derivation (\d+)\.\d+", block)}
    if not m or not cited:
        continue
    declared, latest = int(m.group(1)), max(cited)
    if latest != declared:
        bad(f"lab {n} runs alongside Chapter {declared} but its acceptance "
            f"criterion cites Derivation {latest}.x — anchor it to Chapter {latest}")
if len(problems) == before:
    ok("every lab is anchored to the chapter of the derivation it verifies")

# ---------------------------------------------------------------- 10. readings
# STYLE.md: a reading is a link plus one line on how to read it. "How" must
# include where — a section, a figure, a table, a page count — or the
# instruction is being applied to an entire paper.
print("\nreading locators")
before = len(problems)
LOCATOR = re.compile(
    r"Section|Figure|Table|Appendix|Chapter \d|Chapters \d"
    r"|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+) pages?\b"
    r"|abstract|introduction|training recipe"
    r"|\b(?:Episodes?|Lectures?|Parts?) \d"
    # a *named* element — "the parallelism chapter", "the memory table" — but not
    # "this chapter", which is about our book and locates nothing in theirs
    # the exclusion needs \b, or (?!a) rejects every word starting with "a"
    r"|\b(?!(?:this|the|that|each|every|its|his|her|their|an?)\b)\w+"
    r" (?:chapters?|appendix|tables?|figures?|box|sections?)\b", re.I)
vague = 0
for p in chapters:
    t = text(p)
    for how in re.findall(r'<span class="how">(.*?)</span>', t[t.find(">Readings"):], re.S):
        if not LOCATOR.search(how):
            vague += 1
            bad(f"chapter {p.stem[-2:]}: reading points at a whole work — "
                f"\"{re.sub(r'<[^>]+>', '', how)[:60]}...\"")
if len(problems) == before:
    ok("every reading names where in the source to look")

# ---------------------------------------------------------------- summary
#
# Checks 7-10 were added against a book that already fails them, and the fixes
# are weeks of writing (docs/SECOND-EDITION-PLAN.md). So the audit runs as a
# ratchet: known failures are recorded in tools/audit-baseline.txt and do not
# break the build, anything new does, and a baselined failure that has been
# fixed must be struck from the baseline. The count only goes down.
print()
BASELINE = ROOT / "tools" / "audit-baseline.txt"
known = set()
if BASELINE.exists():
    known = {ln.strip() for ln in BASELINE.read_text().splitlines()
             if ln.strip() and not ln.startswith("#")}

new = [p for p in problems if p not in known]
fixed = known - set(problems)

for p in new:
    print(f"\033[31mnew\033[0m      {p}")
for p in sorted(fixed):
    print(f"\033[33mfixed\033[0m    {p}")
    print("         ^ remove this line from tools/audit-baseline.txt")

if known:
    print(f"\n{len(problems) - len(new)} known problem(s) outstanding, "
          f"{len(new)} new, {len(fixed)} fixed but still baselined")

if new or fixed:
    sys.exit(1)
if problems:
    print("\033[32mno new problems\033[0m")
    sys.exit(0)
print("\033[32mall checks passed\033[0m")
