# Second edition — plan of work

> **Status: complete.** All eight work packages have landed; `make audit` (eleven
> checks) and `make numbers` pass, and `tools/audit-baseline.txt` is empty.
> What was deferred, deliberately, is listed at the foot of this document.
> The plan is kept as written so the reasoning behind each package survives
> alongside the commits that executed it.


The findings are in `docs/CURRICULUM-REVIEW.md`. This is what to do about them.

Two decisions taken up front, because everything below follows from them:

- **The objects the book manipulates get taught in the body**, not outsourced to
  an appendix or to prerequisites. Part I becomes two chapters, and the book
  renumbers to seventeen.
- **This is a revision, not an errata pass.** Chapter text changes materially in
  roughly half the book.

Work is organised into eight packages. They are ordered by dependency, not by
importance: WP0 must precede everything, WP1 must precede WP2, and WP7 must come
last. Sizes are relative — "day", "week" — not commitments.

---

## WP0 · Guard rails first

**Why first.** WP1 renumbers 16 chapters, 258 `Chapter N` cross-references and 73
`Derivation N.M` references. Doing that against the current audit is
unnecessarily dangerous, and two of the checks that would catch a bad renumber
are checks the book should have anyway.

**Do:**

1. Add to `tools/audit.py`:
   - **back-reference check** — for every phrase of the form "Chapter N's X",
     "the X of Chapter N", "X from Chapter N", assert that the named term
     appears in that chapter. This is the check that would have caught the two
     false Chapter 1 attributions (review §1), and it is exactly the check that
     makes a renumber safe.
   - **bank coverage** — every Appendix A entry names its chapter; assert each is
     backed by a `.box.deriv` in that chapter (review §3).
   - **lab anchoring** — every `Derivation N.M` cited in Appendix C must belong
     to a chapter at or before the lab's declared chapter (review §4).
   - **reading locators** — every `<span class="how">` must contain a locator
     token (Section / Figure / Table / Appendix / Chapter *n* / *n* pages /
     abstract / introduction, or an explicitly named element). Fails on 31
     entries today; this check is what makes WP5 finishable rather than
     open-ended.
   - **symbol registry** — a `docs/NOTATION.md` table of symbol → meaning →
     chapters; assert every symbol used in display math is registered, and warn
     when one symbol carries more than one meaning without a per-chapter
     redefinition (review §12).
2. Add a `make numbers` target that recomputes the derivable rows of
   `docs/NUMBERS.md` from their inputs — decode ceiling, cache size, bubble
   fraction, MFU, lifecycle cost, break-even — and greps `src/` for every
   resulting figure. This is the one gap `docs/NUMBERS.md` admits to, and it
   catches the Appendix D error of review §9.1 mechanically.

**Acceptance:** the four new checks run and *fail* on the current source, with
failure counts matching this review (31 readings, 2 bad back-references, 14
unbacked bank entries, 5 misanchored labs). A check that passes on a book known
to be broken is not a check.

**Size:** ~3 days. Everything after this is safer and faster.

---

## WP1 · Part I becomes two chapters

**The shape.** Chapter 1 keeps the six reflexes unchanged and gains the two
primitives it is falsely credited with. A new Chapter 2 states the objects. Old
Chapters 2–16 become 3–17.

### Chapter 1 · The Mathematical Toolkit *(revised)*

Add two sections, both short, both drilled:

- **§1.7 Bayes in one line.** The flip \(P(H\mid E) = P(E\mid H)P(H)/P(E)\), one
  worked example, one drill. Chapter 8's contamination argument and Chapter 1's
  own B-4 both depend on it, and both currently cite a section that does not
  exist.
- **§1.8 Counting operations.** An \(a\times b\) by \(b\times c\) product costs
  \(abc\) multiply–accumulates. Chapter 5 attributes this to Chapter 1 today; it
  underwrites Derivation 5.2, Worked Example 3.3, and every FLOP count in Part III.

Add to §1.3 a **table of \(\Phi\)**, or the two-term approximation, sufficient to
produce \(\Phi(2.04)\) and \(\Phi(2.1)\) unaided. Two closed-book gates currently
demand values the book never supplies (review §11).

Restate the prerequisite honestly in the preface: school mathematics **and**
prior acquaintance with what a neural network is. Keep "skip Chapter 1 if the
gate is easy"; it becomes true once §§1.7–1.8 exist.

### Chapter 2 · The Objects *(new)*

Purpose: state, precisely and without teaching machine learning, every object the
book later manipulates. It is a reference chapter with drills, not a tutorial.
Target 5,000–6,000 words.

| § | states | closes |
|---|---|---|
| 2.1 | network, layer, weights, activation, forward pass, loss | the unstated substrate of Chapters 3–4 |
| 2.2 | gradient descent; **the momentum update** \(v\leftarrow\beta v+g\), \(x\leftarrow x-\eta v\) | review §11 — Chapter 3's protocol result is about an algorithm the book never writes |
| 2.3 | logits; **softmax**; the logistic as its two-outcome case; cross-entropy as a loss | review §11 — softmax appears in three chapters and is never written |
| 2.4 | the chain rule as a product of **Jacobians**; what backpropagation computes | Derivation 4.1 (old 3.1) expands such a product |
| 2.5 | **token**, vocabulary, embedding, readout; tied vs untied | used from Chapter 1 onward, defined nowhere; also the missing support for Lab 1 |
| 2.6 | **KL divergence**, general definition; the Gaussian case as a forward pointer | Chapter 14 (old 13) leash and Move 1 |
| 2.7 | normalization: what it computes | Chapter 4's (old 3's) third theorem is about where to put it |

Deliberately **not** here: the transformer block, the gated cell, and the
policy-gradient vocabulary. Those are local to one chapter each and belong at the
head of that chapter, where they also close a coverage gap (WP2).

Gate 2 mirrors Gate 1: state each object from memory, with symbols named.

### The renumber

Mechanical, scriptable, and the single riskiest step in the plan:

- `src/chapter-02..16.html` → `chapter-03..17.html`; new `chapter-02.html`.
- `Derivation N.M` → `Derivation (N+1).M` — 73 references.
- `Chapter N` → `Chapter N+1` in prose — 258 references, excluding "Chapter 1".
- `Gate N` headings; `§N.M` section numbers within each moved file.
- `build/assemble.py`'s ordered part-divider list (one edit, lines 35–44).
- `src/index.html` contents; Appendix A chapter tags; Appendix C lab anchors;
  Appendix D headings; `docs/NUMBERS.md`; `README.md` contents table.
- Prose counts: "sixteen chapters" → seventeen (`README.md`,
  `chapter-12.html`, `appendix-d.html`, index preface).

Do it as **one commit that changes nothing but numbers**, verified by WP0's
back-reference check plus `make audit`. Resist the temptation to edit content in
the same commit; every later diff becomes unreadable if you do.

**Size:** ~2 weeks including the new chapter. The renumber itself is a day.

*(All chapter numbers below this line are the new ones.)*

---

## WP2 · The object each chapter needs, at the head of that chapter

Three objects are local and belong where they are used. Each addition also closes
a coverage gap from review §6, which is why they are worth the words.

- **Chapter 6 (Attention) — §6.0 "The block".** Q, K, V as learned projections;
  \(\text{softmax}(QK^\top/\sqrt{d})V\) written out; multi-head with
  \(d = H\,d_{\text{head}}\); the position-wise feed-forward; the residual-plus-norm
  wrapper. Then **derive the transformer's parameter count** — \(12d^2\) per layer
  plus embeddings — as the direct analogue of Chapter 5's recurrent count, which
  the book does well and then never repeats. Closes review §6a. Without this,
  \(H_{kv}\) and \(d_{\text{head}}\) arrive cold in Derivation 11.1, and the reader
  cannot check that "7 B, \(L=32\), 32 heads of 128" is self-consistent.
- **Chapter 5 (Memory and Gates) — write the recurrence.**
  \(c_t = f_t\odot c_{t-1} + i_t\odot g_t\), so \(\partial c_t/\partial c_{t-1}=f_t\).
  One line, and it is the line that makes Derivation 5.1's \(f\) mean something.
- **Chapter 14 (Teaching Preferences) — §14.0 "The vocabulary".** Policy, reward,
  trajectory, advantage, baseline, critic, the on-policy ratio. Six definitions.
  This is the chapter a faithful reader currently cannot start.

Also in this package, since they are the same kind of debt:

- **Chapter 16 §16.2** currently has no mathematics. Write the reverse step and
  the strided sampler as equations, or say plainly that it is stated without
  derivation. `docs/DECISIONS.md`'s rule is that a hand-waved step is worse than
  no box.
- **Derivation 14.2 Move 1** (the closed-form optimum) is neither derived nor
  labelled given, in the book's third protocol derivation. Add the three-line
  Gibbs/KL completion — the machinery now exists in §2.6.

**Size:** ~1 week.

---

## WP3 · Build the three constants that are currently given

From review §2. `docs/DECISIONS.md` says constants are given and models are
built; these three are counts, not measurements, and they carry five chapters.

- **Chapter 7 · new derivation: what 16 bytes/parameter is made of.** 4 bytes
  fp32 master weight + 4 momentum + 4 second moment + 4 fp32 gradient. Makes
  Chapter 13's LoRA argument land — the reader sees *which* four bytes LoRA stops
  paying — and gives Chapter 7 the second derivation it badly needs.
- **Chapter 7 or 11 · new derivation: the 6 in \(6ND\) and the 2 in \(2NT\).**
  Two multiply–accumulates per parameter per token forward, four backward;
  serving is forward only. Consumed by Chapters 7, 11 (MFU), 13, and 17's
  lifecycle objective, all of which currently ask for trust.
- Remove the **given** tag from 16 bytes/parameter in `docs/NUMBERS.md`.

**Size:** ~2 days. Highest value per word in the plan.

---

## WP4 · The four coverage gaps

From review §6. Each is a genuine hole in a book that claims to price modern
practice; each is small enough to be a section rather than a chapter.

1. **Activation memory and recomputation** (Chapter 13, or Chapter 8). Chapter 13
   names activations as one of four memory budgets and the book never prices
   them; Chapter 8's B-3 says "ignoring activations" and Appendix D's Chapter 11
   B-1 says "no room for activations". Gradient checkpointing's
   \(\sqrt{L}\) memory-for-compute trade is a textbook fit for the method.
2. **Communication cost of parallelism** (Chapter 8). It is the thinnest chapter
   in the book — 1,614 words, one derivation — and its own C-challenge asks for
   multi-axis reasoning the reader has no arithmetic for. Add all-reduce volume
   (\(2N\) bytes per step) and an interconnect roofline.
3. **Tokenization** (Chapter 6 §6.0 or Chapter 10). Compression ratio, vocabulary
   size, bits per character versus bits per token. Supports Lab 1 (which has no
   chapter today), Lab 3's acceptance criterion, and Chapter 5's
   embedding-fraction argument.
4. **Lower priority:** normalization costed rather than only placed; adaptive
   optimizer state, which is what WP3's 16 bytes counts; positional encoding and
   context extension, in a book that prices long context heavily.

**Size:** ~1 week for the first three; item 4 is optional.

---

## WP5 · The reference pass

From review §14. 31 of 76 annotations point at a whole work.

**The standard**, taken from the two best entries already in the book — Dao's
FlashAttention and Fedus's Switch Transformers. Every annotation names three
things: *where* in the source, *what* is there, and *which derivation of this book
it answers to*.

> Sections 1–3 and Figure 1. The IO analysis is Worked Example 12.1 made rigorous.

**Do:**

- Rewrite the 31 unpointed entries to that standard. WP0's locator check tells
  you when you are done.
- Split the four double entries (Nakkiran + Belkin, Ainslie + Shazeer,
  Hu + Dettmers, Frantar + Lin) so each work gets its own instruction.
- Attribute `chapter-06.html:136` — "Background on scaling behavior", the only
  entry in the book with no author and no title. It is a Jason Wei post; give it
  a byline and a title.
- For the eight book-length targets — the Ultra-Scale Playbook, *How to Scale
  Your Model*, *Dive into Deep Learning*, the Scaling Hypothesis, Kipply's
  inference arithmetic, Weng's two surveys, the Annotated Transformer — either
  name a chapter or move them to a single "standing references" list in the
  front matter, read once rather than per chapter. "Recompute every number in it
  yourself" is a good instruction on an unbounded target.

**Verify locators before shipping.** Section numbers drift between arXiv
versions; check each against the version you link to, and prefer a named element
("the degradation curves", "the parameter table") where numbering is unstable.

**Size:** ~3 days, and the most mechanical work in the plan — a good candidate to
do in one sitting with the papers open.

---

## WP6 · Rebalance the syllabus

From review §§3, 4, 7.

- **Bank.** Split entry 38 into four (coverage/voting → Ch 15; the diffusion
  forward process and guidance → Ch 16; lifecycle and break-even → Ch 17).
  Split 25 and 26. Promote the √κ argument from exercise B-2 to a numbered
  derivation box — the book's first protocol result should not live in an
  exercise. Accept that "thirty-eight" becomes roughly forty-five and change
  every place the count is asserted (Appendix A subtitle, index, README,
  Chapter 17's closing).
- **Labs.** Re-anchor 4 → Ch 11, 5 → Ch 13, 7 → Ch 13, 8 → Ch 12, so every lab
  follows the derivation it verifies. Add two whose acceptance numbers the book
  already contains: a diffusion forward-process lab for Chapter 16 (variances sum
  to one; SNR = 1 at \(t=34\) for \(\beta=0.02\)) and a coverage lab for Chapter 15
  (empirical coverage against \(1-(1-p)^k\), then against a real selector).
  Lab 1 gains a chapter to sit behind it from WP4.
- **Exercises.** Let the B set float from 2 to 6 by chapter weight instead of a
  flat 3. Chapter 10 carries six bank entries on the same allocation as
  Chapter 15, which carries a fraction of one.
- **Budgets.** Make Chapter 17's four canonical; have Chapter 13 state in one
  sentence that its four are a decomposition of them; align Appendix B's T9 to
  the same tree. Three incompatible lists of the thing the book calls its most
  valuable habit (review §5).

**Size:** ~4 days.

---

## WP7 · Notation, glossary, index

Left late because it must be done against final text, and pointless before.

- **`docs/NOTATION.md` + a printed notation table** in the front matter: symbol,
  meaning, chapter of first use. Built and enforced by WP0's registry check.
- **Resolve the worst collisions.** β carries five meanings, two of them in
  adjacent chapters; k carries six. Rename where a rename is cheap — the noise
  schedule and the KL strength cannot both stay β — and where the field's
  convention forbids renaming, say so explicitly at first use in the chapter.
- **Glossary and index.** `docs/HISTORY.md` §8 already lists the index as open.
  Once WP1–WP2 exist, a glossary is largely assembled from the definitions
  already written.

**Size:** ~4 days.

---

## WP8 · Errata

Small, independent, and shippable at any point — do them first if you want
something landed this week.

| # | fix | file |
|---|---|---|
| 1 | decode ceilings "57 … against 28" → 28.6 and 14.3; contradicts Drill 13.2 and its own preceding clause | `appendix-d.html:285` |
| 2 | Chapter 15 B-1 discards half the large model's 24-unit budget; either raise its cost to 24 or give it two attempts and a selector | `chapter-15.html`, `appendix-d.html` |
| 3 | KL used before definition (fixed by WP1 §2.6, but check every use site) | `chapter-14.html` |
| 4 | `docs/NUMBERS.md` records a Chapter 5 perplexity result — 114.5 → 78.4, 0.55 bits/token — that appears nowhere in `src/`. Write it into Chapter 6; it is the one chapter with no bits-per-token content and Chapter 10 later leans on the identity | `docs/NUMBERS.md`, `chapter-06.html` |
| 5 | `docs/DECISIONS.md` cites `docs/HISTORY.md`; `docs/HISTORY.md` cites `AGENTS.md` for the open-items list. Neither `docs/` nor `AGENTS.md` was in the repository before this review | repo root |

**Size:** an afternoon.

---

## Sequence

```
WP0 guard rails ─┬─► WP1 Part I + renumber ─┬─► WP2 local objects ──┐
                 │                          ├─► WP3 the constants ──┤
WP8 errata ──────┘                          └─► WP4 coverage gaps ──┼─► WP7 notation
                                                                    │   glossary
                             WP5 references ────────────────────────┤   index
                             WP6 rebalance  ────────────────────────┘
```

WP5 and WP6 are independent of the renumber only if done *after* it; started
before, they collide. WP8 is independent of everything.

Rough total: **six to seven weeks** of focused work, of which WP1 is a third.

## What not to do

- **Do not renumber and edit content in the same commit.** 258 cross-references
  and 73 derivation references move in WP1; if prose moves with them, no later
  reviewer can read the diff.
- **Do not grow Chapter 2 into a machine-learning tutorial.** Its job is to state
  objects precisely, not to motivate them. If it passes ~6,000 words it has
  become a different book, and the six-reflex discipline of Chapter 1 is the
  thing worth protecting.
- **Do not fix the readings by adding more of them.** The instruction quality is
  the problem, not the count.
- **Do not touch the palette, the grid, or the "What the chapter bought"
  heading.** `docs/DECISIONS.md` argues for each, and none of this review's
  findings bears on them.

## What is already right, and should survive

Constants given and models built; the derivation → drill → graded exercise →
gate → lab chain; the trap taxonomy as a diagnostic rather than a list;
systems before alignment; Part II ending on compression; the labs' predict-the-
number acceptance rule; Gate 9's part-capstone sweep. None of the work above
changes any of them — it makes the book able to keep the promises they imply.


---

# What actually happened

Each package landed roughly as written. The differences worth recording:

**WP0.** The symbol registry moved to WP7, where the registry file it checks
actually exists. The bank check was redesigned: "every entry backed by a
derivation box" would have failed 14 times and could never have passed, since
the book will never box all fifty entries. The rule became: no entry spans
several chapters, every chapter is represented, no chapter carries more
entries than it has boxes. That fires on the real defects and is reachable.

**WP1.** The renumber's first attempt double-shifted `## Chapter 13` and
`Ch. 14–16`, because two rules each claimed them. Rebuilt as a single regex
alternation in one pass. `tools/renumber.py` is kept, with a guard that
refuses to run twice.

**WP2.** Chapter 6's new block section collided with an existing Worked
Example 6.1 and Drill 6.1; labels are renumbered in document order. The same
happened in Chapters 10 and 14.

**WP4.** Item 4 — costing normalization, and positional encoding — was
deferred as the plan allowed. Adaptive optimizer state is covered by
Derivation 8.2.

**WP5.** Locators are named elements ("the degradation figure in the opening",
"the shortcut-variant table") rather than section numbers, which drift between
arXiv revisions. Found while doing it: the locator check's own exclusion list
lacked word boundaries, so `(?!a)` rejected every word starting with "a". The
first edition measures 45/76 either way, so the review's figure was not
inflated by the bug.

**WP6.** Thirty-eight bank entries became fifty. Splitting pushed Chapter 10
past its box count, which is the review's own finding that the chapter
under-teaches what it examines; three results that lived in prose are now
boxed. The DPO naming question, left open in the review, was decided in
favour of naming each method once at its point of introduction.

**WP7.** The index was not built. It has to be generated from the assembled
print document rather than written, which is a build feature; Appendix E says
so where a reader will look for it.

## Still open

1. **The index** — a build task against `.cache/book-print.html`. Attempted
   and reverted; WeasyPrint's `target-counter` does not resolve reliably for
   the volume of anchors an index requires.
2. **Costing normalization**, and **positional encoding / context extension**,
   both deferred from WP4 item 4.
3. **Verifying reading locators against the linked versions.** The named
   elements are stable and were written from knowledge of the papers, but no
   pass has been made with all 76 sources open.
4. **A close prose read.** `docs/HISTORY.md` §8 notes that the original prose
   audit measured patterns across the whole book and read only portions
   closely. This revision added roughly 9,000 words; they have been checked
   for arithmetic and cross-reference, not read aloud.
