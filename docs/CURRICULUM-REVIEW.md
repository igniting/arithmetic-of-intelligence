# Curriculum review

A review of the syllabus itself — what is taught, in what order, with what
weight, and how it is assessed. Not a prose or copy edit. Everything below was
checked against `src/`, `tools/audit.py`, and the four docs.

Findings are ordered by how much they cost the reader, not by how easy they are
to fix. Each names the exact file and the exact claim.

---

## Verdict

The curriculum is sound and unusually well-designed for its stated purpose. The
central rule — constants given, models built — is real, not decorative: I could
not find a single exercise that rewards recalling a benchmark number. The
derivation → drill → graded exercise → gate → lab chain is coherent, the trap
taxonomy is a genuinely good diagnostic instrument, and the systems-before-alignment
ordering in Part III earns its keep (Chapter 13 reads as forced moves rather than
fashion precisely because Chapters 10–12 came first).

The defects are of one kind, and it is the kind a batch-written book gets: the
*spine* is right and the *joints* have drifted. Chapter 1 does not contain
everything later chapters say it contains; the derivation bank is atomized
unevenly across the parts; the labs point at the wrong chapters; three of the
book's most load-bearing numbers are handed over as constants when the book's own
rule says they should be built. None of this is visible from inside a chapter.
All of it is visible across chapters, which is why the audit passes.

---

## 1. Chapter 1 is missing two primitives that later chapters cite it for

The most serious finding, because it breaks the book's foundational promise
("six reflexes carry the entire book … from here they are furniture").

**Bayes' rule is never taught.** `src/chapter-08.html:78` says the contamination
flip "is nothing more than the Bayes flip of Chapter 1." Chapter 1 contains no
Bayes' rule — §1.3 is the binomial, §1.6 is bits, and the word does not appear in
the file. Appendix A entry 20 requires the flip. Chapter 1's own exercise B-4
requires it, untaught, and Gate 1 quietly excludes B-4 from the pass criteria
(it examines A1–7 and B-1 through B-3) — which reads like the gap was felt but
not named.

**The matrix-multiply cost primitive is never stated.**
`src/chapter-05.html:56` says "Both costs come from the matrix-multiply primitive
of Chapter 1 — multiplying an \(a\times b\) matrix by a \(b\times c\) matrix
costs \(abc\) multiply–accumulates". Chapter 1 never says this. Derivation 5.2,
Worked Example 3.3, and every FLOP count in Part III rest on it.

**Linear algebra generally.** The stated prerequisite is "school-level
mathematics — logarithms, elementary calculus, basic probability". Chapter 2
opens by aligning coordinates with the eigenbasis of the Hessian; Derivation 3.1
expands a product of Jacobians. Neither is school-level, and neither is in
Chapter 1's six reflexes.

*Fix:* add §1.7 "Bayes in one line" and fold the `abc` matmul count into §1.2 or
a new §1.8 on counting operations. Both are short. This also makes the preface's
"skip Chapter 1 without guilt" honest rather than dangerous — as it stands, a
reader who skips loses two things the book later assumes.

## 2. Three load-bearing numbers are "given" when the book's own rule says they should be built

`docs/DECISIONS.md` is unambiguous: constants from the literature are given
(bandwidth, scaling exponents), models are built. Three numbers currently sit on
the wrong side of that line, and they are among the most reused in the book:

| number | where | status |
|---|---|---|
| the **6** in \(C = 6ND\) | `chapter-06.html:47` | "about 6, counting the forward and backward passes" — never counted |
| the **2** in \(2NT\) | `chapter-16.html:34` | "one multiply–add per parameter, forward only" — asserted in half a clause |
| **16 bytes/parameter** of optimizer state | `chapter-07.html:61` | "on the order of 16 bytes … once everything is counted" — never counted |

None of these is an empirical measurement. Each is a *count*: 2 FLOPs per
parameter per token forward and 4 backward; 4 bytes of fp32 master weight plus 4
of momentum plus 4 of second moment plus 4 of fp32 gradient. They are exactly the
kind of arithmetic this book exists to teach, and they carry Chapters 6, 7, 10,
12, and 16. `docs/NUMBERS.md` even labels 16 bytes/param **given**, which
formalizes the error.

*Fix:* one derivation box in Chapter 7 (the 16-byte decomposition, which then
makes Chapter 12's LoRA argument land harder) and one in Chapter 6 or 10 (the
2N/6N forward-backward count, which Chapter 10's MFU formula and Chapter 16's
lifecycle objective both consume). This is the single highest-value addition
available to the book, because three chapters currently ask the reader to trust
a number where they could be shown one.

## 3. The derivation bank is atomized unevenly, and Part III's tail is under-weighted

Appendix A is declared the syllabus. Counted by chapter, its 38 entries fall:

```
Ch 2: 3   Ch 3: 6   Ch 4: 3   Ch 5: 2   Ch 6: 2   Ch 7: 2   Ch 8: 2   Ch 9: 6
Ch 10: 3  Ch 11: 3  Ch 12: 3  Ch 13: 2  Ch 14–16: 1 (shared)
```

Entry 38 bundles four unrelated results — coverage, the voting threshold, the
diffusion forward process *and* guidance, and the lifecycle cost with its
break-even — across three chapters. Meanwhile convolution arithmetic gets six
entries to itself. Entry 25 bundles typicality, the OLS excess risk, and
grokking; entry 26 is Legg's Υ plus the wireheading threshold.

Two consequences. First, "thirty-eight" is a round number obtained by bundling,
not an honest atomization (atomized consistently it is roughly 48). Second, and
worse pedagogically, the Part III sweep in Gate 16 tells a reader that Chapters
14–16 are one item's worth of reproduction when they contain at least five
distinct reproducible results.

**Related:** 14 of the 38 entries have no `.box.deriv` anywhere in the book —
they live in prose or worked examples. Most sharply, **entry 2 is a `protocol`
item with no derivation box.** The √κ speedup is the book's first
three-separate-days result, and Gate 2 has to ask for it as "the √κ argument of
B-2", an exercise. Derivation 2.1 is the stable step range; Derivation 2.2 is
symmetry breaking. The crown of Chapter 2 is not boxed.

*Fix:* promote the √κ argument to Derivation 2.2 (renumber symmetry-breaking to
2.3); split entry 38 into four entries across Chapters 14, 15, 16; split 25 and
26. Accept that the count becomes ~44 and change the subtitle.

## 4. The lab manual points at the wrong chapters

Appendix C says the labs run "roughly one per chapter from Chapter 10 onward."
Checked against the derivations each lab actually verifies:

| lab | scheduled | derivation it verifies | lives in |
|---|---|---|---|
| 1 · BPE tokenizer | Ch 10 | — | **nowhere in the book** |
| 2 · streaming softmax | Ch 11 | 11.1 | Ch 11 ✓ |
| 3 · char-level LM | Ch 12 | §9.2 identity | Ch 9 |
| 4 · KV cache | Ch 12 | 10.1 | Ch 10 |
| 5 · LoRA | Ch 13 | §12.3 (\(2rd\)) | Ch 12 |
| 6 · preference optimization | Ch 13 | 13.2 | Ch 13 ✓ |
| 7 · quantization | Ch 15 | 12.1 | Ch 12 |
| 8 · speculative decoding | Ch 16 | 11.2, 11.3 | Ch 11 |

Five of eight are scheduled one to five chapters after the derivation they test,
and Appendix C says so in its own text without noticing — Lab 7 sits at Chapter
15 while its acceptance criterion cites "Derivation 12.1's \(R^2\) sensitivity."
The book's whole lab premise is *predict the number, then run the code*; a
five-chapter gap between deriving the number and predicting it defeats that.

Two further gaps: **Lab 1 requires byte-pair encoding, which no chapter covers**
(see §6 below), and **Chapters 14, 15 and 16 have no lab of their own** — they
are given labs about quantization and speculation instead.

*Fix:* re-anchor 4→Ch 10, 5→Ch 12, 7→Ch 12, 8→Ch 11. Then add two labs whose
acceptance numbers the book already contains: a diffusion forward-process lab
for Chapter 15 (verify \(\bar\alpha\) coefficients sum to one in variance;
confirm SNR = 1 at t = 34 for β = 0.02) and a coverage-versus-k lab for Chapter
14 (measure empirical coverage against \(1-(1-p)^k\) and against a real
selector's reliability). Both are cheap and both close the elicit/create and
coverage-is-not-accuracy lessons with a measurement.

## 5. "Name your budget" is the signature habit, and the book gives three different budget lists

This matters more than it looks, because T9 is one of the two classes Appendix B
says accounts for "most professional disagreements in this field."

- `chapter-12.html:32` — four resources: weights; gradients and optimizer state;
  activations; per-token computation.
- `chapter-16.html:83` — "the four budgets": training operations; serving
  operations; memory bytes and bandwidth; human preference information.
- `appendix-b.html` T9 — seven: weights, optimizer state, activations,
  bandwidth, training operations, serving operations, human preference data.

Chapter 12 says "each technique below improves exactly one of these four";
Chapter 16 says "the book has priced four distinct scarce resources" and names a
different four; Appendix A's synthesis essay S4 uses Chapter 16's. A reader
building the habit the book most wants to leave them with is handed three
incompatible vocabularies.

*Fix:* make Chapter 16's four canonical and have Chapter 12 state explicitly
that its four are a decomposition of the third (memory and bandwidth) plus the
first two — one sentence. Align T9's list to the same tree.

## 6. Coverage gaps, ranked

**a. The transformer parameter count.** Chapter 4 derives the recurrent layer's
\(4d_h(d_{in}+d_h+1)\), assembles a full model, and extracts the
embedding-plus-readout fraction — an excellent piece of teaching. Chapter 5 never
does the analogous thing for a transformer. There is no \(12d^2\) per layer, no
head split, no accounting of where the parameters sit. The consequence surfaces
in Part III: Worked Example 10.1 hands the reader "a 7-billion-parameter model
with L = 32, 32 heads of dimension 128" and the reader has no tool in the book
with which to check that those numbers are consistent. Grouped-query attention is
priced in Chapter 10 without multi-head attention ever having been set up in
Chapter 5.

**b. Activation memory and recomputation.** Chapter 12 names activations as one
of its four memory budgets. Nothing in the book ever prices them. Chapter 7's
B-3 explicitly says "ignoring activations", and Appendix D's Chapter 10 B-1
solution ends "barely, with no room for activations, so four in practice" — the
book keeps bumping into the budget it never counts. Gradient checkpointing (the
\(\sqrt{L}\) memory-for-compute trade) is the natural derivation and is a
textbook fit for this book's method.

**c. The communication cost of parallelism.** Chapter 7 is the thinnest chapter
in the book (1,614 words, one derivation) and covers only the pipeline bubble and
division-by-\(N\). Data-parallel all-reduce volume, tensor-parallel
communication, and the interconnect's own roofline are absent — even though the
C-challenge asks the reader to reason about "multi-axis parallelism" they have no
arithmetic for, and Appendix D's answer to it has to hand-wave ("costs
communication rather than idle time"). Chapter 7 could carry two more derivations
comfortably.

**d. Tokenization.** Zero coverage, yet Lab 1 requires implementing BPE, Lab 3's
acceptance requires converting nats/char to bits/char to a predicted file size,
and Chapter 4's embedding-fraction argument turns on vocabulary size. A short
§5.0 or a Chapter 9 section on vocabulary/compression-ratio arithmetic would
close it and would sit naturally next to "cross-entropy is a file size."

**e. Lower priority:** normalization is told where to sit (Chapter 3) but never
costed or derived; adaptive optimizers appear only as a C-challenge gesture,
though their state is what the 16 bytes/param of §2 counts; positional encoding
and context extension are absent from a book that prices long context heavily.

## 7. Exercise load is uniform where the content is not

Every chapter from 2 to 16 carries exactly 4 A-drills, 3 B-problems, 1
C-challenge — with two chapters getting a fourth B. Total 134 end-of-chapter
exercises plus 41 inline drills.

The uniformity is indefensible against the chapters' own weights. Chapter 9
carries six bank entries, eight distinct topics and four worked examples, and
gets 9 exercises. Chapter 14 carries a third of one bank entry and gets 8.
Chapter 6, the declared crown jewel and a protocol derivation, gets the same 8 as
Chapter 15. Chapter 3 carries six bank entries on 8 exercises.

*Fix:* let the B set float between 2 and 6 by chapter weight. The A drills can
stay fixed — they are calibration, not load.

## 8. Sequencing notes

**Chapter 15 is the odd one out and its placement costs the arc.** It is the only
non-language chapter, has one derivation box, shares a fraction of one bank
entry, has no lab of its own, and interrupts the otherwise tight
13 → 14 → 16 progression (post-training → inference-time compute → lifecycle).
§15.2's strided sampling — "a reformulation of the reverse process makes it
deterministic and permits strides" — is asserted with no mathematics at all, and
§15.4 (latent diffusion) is pure prose. Either give it two more derivations and
its own lab, or move it after Chapter 16 as a coda. The current position is the
worst of both.

**Chapter 9 §9.7 is weighted oddly.** Legg's Υ and the wireheading threshold get
two of 38 bank entries — as much as all of Chapter 13, and more than diffusion.
The geometric-series calculation is nice and the reward-channel argument does pay
off in Chapter 13's leash, but two full bank entries for agent-theory material
with no engineering consequence in the rest of the book is generous next to a
diffusion chapter that shares a quarter of one entry.

**Well-judged and worth defending:** systems before alignment; ending Part II on
compression; Gate 9 as a Part II capstone sweep; Chapter 8 before Chapter 9
(measurement scepticism before the generalization account).

## 9. Concrete errors found

1. **`src/appendix-d.html:285` — decode ceilings doubled.** Chapter 16 B-3 says
   the 35 B option's ceiling is "roughly 57 tokens per second against 28" for
   the 70 B. The same sentence correctly states 70 GB against 140 GB at half
   precision, and 2 TB/s ÷ 70 GB = **28.6**, ÷ 140 GB = **14.3**. The figures
   quoted are those of the *8-bit and 4-bit* rows of Chapter 10's B-3 solution.
   Chapter 12's Drill 12.2(b) gives 14.3 for a 70 B model at 16 bits, so the book
   contradicts itself. Should read "roughly 29 … against 14."

2. **Chapter 14 B-1 is not a matched-compute comparison.** The problem gives a
   24-unit budget and a large model costing 12, so the large model gets two
   attempts — but the parenthetical and the solution both treat it as a *single*
   answer needing no selection, discarding half its budget. Worked Example 14.1
   is clean (budget 10, cost 10, exactly one attempt); B-1 inherits its phrasing
   without inheriting its arithmetic. Either set the large model's cost to 24 or
   let it have two attempts and a selector.

3. **Derivation 13.2 Move 1 is asserted, not derived and not labelled given.**
   "Maximizing … is a standard variational problem whose solution is …" —
   `src/chapter-13.html`. `docs/STYLE.md` requires that a derivation box show
   every step and that anything supplied rather than derived be said to be
   supplied; `docs/DECISIONS.md` calls a hand-waved step in a derivation box
   worse than no box. This is the book's third protocol derivation, the one the
   gate says is "most likely to be asked of you in a professional setting", and
   its first move is the one step not shown. The Gibbs/KL completion is three
   lines and uses machinery the reader has (Chapter 9 already carries a KL
   formula).

4. **KL divergence is used before it is defined.** Chapter 13 writes
   \(\mathrm{KL}(\pi\|\pi_{\text{ref}})\) with no definition; Chapter 9 §9.3
   gives only the Gaussian closed form. `docs/STYLE.md`: "Define every symbol at
   first use in a chapter, even if defined earlier in the book."

5. **`docs/NUMBERS.md` records a Chapter 5 result that is not in the book.**
   The row "perplexity 114.5 → 78.4 | **0.55 bits/token**" has no counterpart
   anywhere in `src/` — grep finds none of the three figures. Either the passage
   was cut and the ledger not updated, or it was planned and never written. Given
   that Chapter 5 is the one chapter with no bits-per-token content and Chapter 9
   later leans on the identity, it is worth writing rather than deleting.

6. **Broken doc references.** `docs/DECISIONS.md` cites `docs/HISTORY.md` and
   `docs/HISTORY.md` cites `AGENTS.md` for the open-items list; neither the
   `docs/` directory nor `AGENTS.md` is in the repository. The README's editing
   instructions point only at `src/`.

## 10. What the audit cannot see, and what would extend it

`tools/audit.py` passes all six checks, and its checks are good ones. Everything
in §§1–5 above is invisible to it because it validates *within* files and *from*
chapters *to* appendices, never the reverse. Three cheap additions would have
caught four of this review's findings:

- **Bank coverage.** Every Appendix A entry names its chapter; assert each is
  backed by a `.box.deriv` or an explicitly-tagged worked example in that
  chapter. Catches §3, including the unboxed protocol entry.
- **Lab anchoring.** Every "Derivation N.M" cited in Appendix C must belong to a
  chapter at or before the lab's declared chapter. Catches §4 entirely.
- **Back-reference check.** For each "of Chapter N" / "Chapter N's X" phrase,
  assert the named term appears in chapter N. Catches §1 (both Bayes and the
  matmul primitive) and would have caught the KL definition gap.

A fourth, for numbers: the review found one arithmetic contradiction across
files (§9.1). A check that re-derives the small set of formulas in
`docs/NUMBERS.md` from their inputs — decode ceiling, cache size, bubble
fraction, lifecycle cost — and compares against every occurrence of the resulting
figure in `src/` would close the one gap the docs admit to ("the audit cannot
catch an arithmetic inconsistency").

---

# Part II — Technical content

A second pass, over the technical substance rather than the syllabus: what the
book defines, what it assumes, what its notation does, and how precisely it
points at its sources. The findings here are the reason for
`docs/SECOND-EDITION-PLAN.md`.

## 11. The book manipulates objects it never states

This is the largest single finding in either pass. The book derives results
*about* things it never writes down. Every item below was confirmed by grep over
all of `src/`, not by impression.

| object | never stated | but required by |
|---|---|---|
| **softmax** | no formula anywhere in the book | Derivations 5.1, 5.2, 11.1; §5.3 temperature; Lab 2 |
| **attention** | `softmax(QK^T/√d)V` never written; Q, K, V never defined as learned projections | all of Chapter 5, Chapter 10's cache, Chapter 11's kernel |
| **multi-head attention** | absent from Chapter 5 entirely | \(H_{kv}\), \(d_{\text{head}}\) appear cold in Derivation 10.1; grouped-query attention is priced on them |
| **the momentum update** | \(v \leftarrow \beta v + g,\ x \leftarrow x - \eta v\) never written | Chapter 2's √κ result — a *protocol* derivation — and the cover figure |
| **the gated recurrence** | \(c_t = f_t\odot c_{t-1} + i_t\odot g_t\) never written | Derivation 4.1's per-step factor *is* \(f\); the identification is the chapter's crux and is left implicit |
| **KL divergence** | only the Gaussian closed form (§9.3); no general definition | Chapter 13's leash, Derivation 13.2's Move 1, Schulman reading |
| **advantage \(A\)** | "\(A\) for the advantage" — never defined | Worked Example 13.1, Drill 13.1, §13.4, four exercises |
| **policy, critic, baseline, on-policy ratio** | RL vocabulary used throughout Chapter 13 | a protocol chapter the reader cannot parse without it |
| **token, vocabulary** | never defined | used from Chapter 1 (perplexity per token) onward; \(D\) is measured in them |
| **logit** | first used in §5.3, undefined | temperature, softmax saturation, Worked Example 5.1 |
| **normalization layer** | what it computes is never stated | Chapter 3's third theorem is about *where to put it* |
| **Jacobian** | never defined | Derivation 3.1 is a product of them |
| **\(\Phi\), the normal CDF** | named in §1.3; never defined, and **no table of values anywhere** | Derivation 3.2 needs \(\Phi(2.04)=0.9793\); Appendix D needs \(\Phi(2.1)=0.9821\); **Gate 3 demands both on blank paper** |
| **the reverse diffusion step** | §15.2 contains no equation at all | the chapter's own sampling story |
| **mixed precision; what optimizer state contains; tensor parallelism** | asserted or named only | Chapter 7 §7.2, its C-challenge, and Appendix D's answer to it |

Two of these are acute rather than merely untidy. The **Φ table** makes two
closed-book gates literally impossible as written — a reader cannot produce
0.9793 from nothing. And the **RL vocabulary** gap means Chapter 13, one of the
three protocol chapters, is the one chapter a reader who has followed the book
faithfully cannot begin.

## 12. Notation collides, and there is no apparatus to resolve it

`docs/STYLE.md` requires defining every symbol at first use in a chapter, which
the chapters mostly honour locally. Nothing manages symbols *globally*, and the
book reuses them heavily:

| symbol | meanings in use |
|---|---|
| **β** | power-law exponent (§1.1, §4.5) · momentum coefficient (cover figure, README) · bytes per value (Der. 10.1) · KL strength (Ch 13) · noise schedule (Ch 15) |
| **k** | kernel side (Ch 3) · compute constant \(C=kND\) (Ch 6) · number of parts (Ch 8) · draft length (Ch 11) · top-\(k\) routing (Ch 12) · sample count (Ch 14) |
| **A, B** | loss coefficients (Ch 6) · LoRA factors (Ch 12) · advantage / batch (Ch 13, Ch 10) · option labels (Ch 9, Ch 16) |
| **b** | data exponent (Ch 6) · gate bias (Der. 4.2) · bits per weight (Ch 12) |
| **σ** | weight standard deviation (Ch 1–2) · the logistic function (Ch 4, 13) · \(\sigma_p,\sigma_q\) coding widths and noise sd (Ch 9) |
| **p** | probability (Ch 8, 14) · parameter count in the OLS risk (§9.6) · target distribution (Der. 11.2) |
| **L** | the loss (Ch 2, 6) · number of layers (Ch 3, 10) |
| **E** | irreducible loss (Ch 6) · expert count (Ch 12) · expectation |
| **α, κ, d, v, V, C, T, s** | two or three meanings each |

β and k are the dangerous ones: β carries five meanings, two of which
(KL strength, noise schedule) sit in adjacent chapters, and one of which
(momentum) belongs to the result the cover figure plots.

There is also **no notation table, no glossary, and no index** — `docs/HISTORY.md`
§8 already lists the index as open. For a book whose stated use is "when a new
paper resists you, scan this list and ask which entry prices it", the absence of
a lookup path is a functional gap, not a cosmetic one.

## 13. The stated prerequisite does not match the actual demand

The preface promises "school-level mathematics — logarithms, elementary
calculus, basic probability" and says Chapter 1 "sharpens exactly six
mathematical reflexes and nothing else". What the chapters actually require:

- the spectral theorem, implicitly — Chapter 2 aligns coordinates with the
  eigenbasis of the curvature in its first paragraph;
- matrix calculus — Derivation 3.1 expands \(\prod(I+J_\ell)\);
- the matrix-multiply cost, and Bayes' rule — both attributed to Chapter 1,
  both absent from it (Part I §1 of this review);
- KL divergence and constrained optimisation *over distributions* — Chapter 13
  Move 1;
- rejection sampling — Derivation 11.2;
- everything about neural networks, which is outsourced to a reading annotation
  ("Watch before Chapter 2 if you have never seen a neural network") rather than
  stated as a prerequisite.

The honest position is that this book has two prerequisites — school mathematics
*and* prior acquaintance with neural networks — and currently declares one.

## 14. Readings: 31 of 76 point at a whole work

Measured over every `<span class="how">` annotation in `src/chapter-*.html`,
counting an entry as *pointed* if it names a section, figure, table, chapter,
page count, abstract, or a specific named element:

```
ch01 4/4   ch02 3/4   ch03 1/5   ch04 2/5   ch05 2/5   ch06 4/5   ch07 2/5   ch08 1/4
ch09 4/6   ch10 1/4   ch11 3/5   ch12 4/5   ch13 6/6   ch14 1/4   ch15 4/5   ch16 3/4
                                                       total 45/76 = 59% pointed
```

`docs/STYLE.md` says every entry is "a link plus one line saying *how* to read
it. Never a bare citation." The annotations are never bare — the *how* is always
there — but 31 of them apply that instruction to an entire paper, blog series or
book. Chapters 3, 8, 10 and 14 are the weakest (1 pointed entry each).

Three specific problems beyond the count:

1. **One entry has no author and no title.** `chapter-06.html:136` reads
   "Background on scaling behavior", linking to a post on `jasonwei.net`. It is
   the only unattributed reading in the book.
2. **Four entries bundle two works under one annotation** — Nakkiran + Belkin
   (ch 9), Ainslie + Shazeer (ch 10), Hu + Dettmers and Frantar + Lin (ch 12) —
   so 80 works are covered by 76 annotations, and the paired ones necessarily
   get a vaguer instruction than a single work would.
3. **Several point at book-length works with no locator**: the Ultra-Scale
   Playbook, *How to Scale Your Model*, *Dive into Deep Learning*, Branwen's
   Scaling Hypothesis, Kipply's inference-arithmetic post, two of Weng's
   surveys, the Annotated Transformer. "Recompute every number in it yourself"
   is a good instruction attached to an unbounded target.

The best entries in the book show exactly what the standard should be — Dao,
FlashAttention: "Sections 1–3 and Figure 1. The IO analysis is Worked Example
11.1 made rigorous"; Fedus, Switch Transformers: "Section 2 and the
auxiliary-loss box". Both name *where*, *what*, and *against which derivation*.
45 entries meet that standard and 31 do not.

---

## If only five things are changed

1. Add Bayes and the matmul cost to Chapter 1 (§1). Cheapest fix, largest
   foundational hole.
2. Derive the 6, the 2, and the 16 bytes (§2). Turns three acts of faith into
   three pieces of arithmetic, in the book most committed to that conversion.
3. Re-anchor the labs and add the two missing ones (§4). The lab manual is a
   strong instrument currently pointed at the wrong targets.
4. Split bank entry 38 and box the √κ result (§3). Makes the syllabus honest
   about what Part III's tail requires.
5. Fix the doubled decode ceilings in Appendix D and the unmatched compute in
   Chapter 14 B-1 (§9.1, §9.2).

Items 1, 2 and 4 are each under a day. Item 3 is a re-labelling plus two new
labs. Item 5 is two paragraphs.
