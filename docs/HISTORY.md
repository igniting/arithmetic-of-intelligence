# How this book came to exist

Written for whoever picks this up next. The route mattered: several of the
book's defining choices are reactions to something that was tried and rejected,
and without that history they look arbitrary.

---

## 1. It started as an exam, and the first one was wrong

The origin was a book about the roughly thirty papers on Ilya Sutskever's
reading list — the ones he gave John Carmack as a foundation in machine
learning. The first request was a JEE-style multiple-choice paper on its
contents. (JEE is the Indian engineering entrance examination; its Advanced
paper is known for problems that require building a model rather than recalling
a fact.)

The first attempt — 68 questions, 268 marks — was **rejected outright**, and
correctly. It was fact-recall: which year a paper appeared, which number sat in
which table, who wrote what. The feedback was that it "should not be fact recall
based, it should be genuinely inspired for problem solving."

That rejection produced the rule the entire book is now built on: **constants
are given, models are built.** Everything downstream — the derivation bank, the
"given" data sheets, the refusal to test on benchmark numbers — descends from
that one correction.

## 2. A self-critique that found real problems

The rebuilt problem paper (47 questions, derivation-based) was then reviewed
against the source material, and the review found genuine faults worth
remembering because the same faults recur whenever this material is written:

- **Formula-sheet leakage.** The paper handed the student the receptive-field
  formulas and then asked questions that were substitutions into them. A physics
  paper gives you Coulomb's law, not the field of a dipole.
- **Coverage skew.** One seam — dilated convolution arithmetic — was mined five
  times while whole chapters had no problems at all. Optimisation geometry,
  LSTM gradient dynamics, the √d scaling, emergence, and test-time compute were
  entirely absent.
- **A soft bottom third.** Roughly a third of the questions were single-formula
  plug-ins; one was literally a single multiplication scored equally with a
  Lagrangian derivation.

Version 2 (56 questions, 200 marks) fixed all three. Its structure survives in
the book as the exercise sets and the trap taxonomy.

## 3. An honest answer that forced the book to double in size

Asked whether the curriculum would actually make anyone better at modern machine
learning, the answer given was: *partially*, with three specific gaps. It covered
2012–2022 only — no post-training, no inference economics, no mixture-of-experts,
no diffusion. It had **zero code**. And an exam format trains reproduction rather
than problem-finding.

Naming those gaps honestly is what produced Part III (Chapters 10–16) and the
lab manual in Appendix C. The alternative — claiming the classical material was
sufficient — would have left a book that was half a book.

## 4. From curriculum to textbook

Three curriculum documents (classical, modern, and a merged version with about
fifty-five hyperlinked readings) were then rewritten as an actual textbook:
narrative prose, numbered derivations, worked examples, inline drills with
collapsible answers, graded exercises, and per-chapter reading lists that say
*how* to read each source rather than merely listing it.

Chapters were written in batches. **That is the origin of most defects found
later** — see §6.

## 5. Design decisions taken early

Recorded in full in `docs/DECISIONS.md`. The short version: an engineering
graph-paper aesthetic — blueprint blue, ink, rust reserved for traps, on cool
off-white — deliberately chosen to avoid the cream-and-terracotta palette that
currently reads as a machine-generated design tell.

## 6. Two audits that found real errors

**A consistency audit** (now `tools/audit.py`) caught six genuine seams from
batch-writing, including two outright contradictions: Chapter 5 claimed
"Part II now closes; Chapter 6 opens Part III" when Chapter 6 is in Part II and
Part II runs to Chapter 9; and Chapter 12 called the preference-optimization
collapse "the second of the book's three protocol derivations" while Chapter 6
claimed second and Chapter 13 claimed third. It also found Chapter 1 missing its
readings and closing section, Chapter 8 with no worked example, Chapter 7 with
no trap box, and drafting residue in Chapter 10 ("but note that per-token figure
is often quoted per layer-head product, so let us be careful" — thinking aloud,
not textbook prose).

**A prose audit** followed, prompted by the observation that the writing looked
machine-generated with visible seams. Measurement confirmed it:

| symptom | before | after |
|---|---|---|
| chapter openings containing "This chapter" | 12 / 16 | 0 / 16 |
| openings beginning with a "Chapter N did X" callback | 8 / 16 | 0 / 16 |
| distinct first words across the sixteen openings | — | 14 / 16 |
| summaries opening with a bare count ("Three results…") | 8 / 16 | 0 / 16 |
| passages anticipating a reader's wrong first guess | **0** | 16 |

That last row was the real finding. Across 35,000 words there was not one
instance of the move a teacher makes constantly — *you will probably guess X;
here is why the arithmetic says otherwise*. Nine such passages were written into
the key derivations, plus further edits naming where students actually go wrong.

Rewriting the openings then created a second-order problem worth remembering:
seven new openings **collided with the paragraphs beneath them** (Chapter 6 said
"calculus problem" twice in adjacent paragraphs). Editing any opening in
isolation risks this; check what follows.

## 7. Title, cover, PDF

The book was called *Derivations First* until late. That title described the
method, not the subject. It became **The Arithmetic of Intelligence** — a claim
about what the field reduces to, which is the book's actual thesis. Alternatives
considered and still viable: *Back of the Envelope*, *Thirty-Eight Machines*,
*Calculations in Costume*.

The cover carried an imprint line and a statistics block; both were cut in
favour of a figure. That figure is not decoration — it is a plot of the book's
first derivation, generated by `build/coverfig.py` actually running gradient
descent and momentum on an ill-conditioned valley. After seventy steps momentum
has reached the minimum while gradient descent is still a quarter of the way
out: the √κ result, drawn rather than asserted.

## 8. What is still unfinished

Listed in `docs/SECOND-EDITION-PLAN.md` under **Still open**. Briefly: no
index, costing normalization and positional encoding, a Chapter 6 perplexity
row, verifying reading locators against linked versions, and a close prose read
of the ~9,000 words added in the revision.
