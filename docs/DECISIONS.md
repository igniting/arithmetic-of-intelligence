# Decisions

Design, pedagogical and technical choices, with the reasoning. Change any of
them if you have a better argument — but know what the argument was.

---

## Pedagogy

**Constants are given; models are built.**
The book supplies every empirical constant it needs and tests only the reasoning
that uses it. This came from the rejection of a fact-recall first draft
(`docs/HISTORY.md` §1). It is the single rule most worth preserving.

**The unit of progress is a derivation, not a chapter.**
Appendix A is the actual syllabus: thirty-eight results stated without their
derivations, so the reader must supply them. Chapters are delivery mechanisms.
This is why every chapter ends with a gate specifying what to reproduce on blank
paper rather than what to have read.

**Three derivations carry a "three separate days" protocol.**
Momentum's √κ speedup (Chapter 3), the compute-optimal allocation (Chapter 7),
and the preference-optimization collapse (Chapter 14). These are the results
with the highest transfer: the second and third use the same
substitute-differentiate-cancel discipline, and the book says so explicitly so
the fluency compounds. Spaced reproduction rather than rereading is the
instruction because rereading produces recognition, not recall.

**Traps are named, classified, and cross-referenced.**
Appendix B defines ten trap classes (T1–T10); chapters tag their trap boxes with
the relevant class. The reader logs every error against a class, and the
distribution that emerges after twenty entries *is* their remaining curriculum.
This turns error-logging from a chore into a diagnostic.

**Labs are accepted on a predicted number, not on working code.**
Every lab in Appendix C requires the reader to write down what the derivation
predicts *before* running anything: streaming softmax matching a library to 1e-6;
the preference-tuning loss starting at exactly ln 2; measured tokens-per-cycle
within 10% of the truncated-geometric formula. Code that runs proves nothing;
code that reproduces a number you predicted proves you understood the
derivation.

**Systems before alignment in Part III.**
Chapters 10–12 (inference economics, IO-aware attention, sparsity) precede
Chapter 14 (post-training) deliberately. Without the cost vocabulary — bytes,
bandwidth, budgets — the alignment era's design choices (why the critic gets
deleted, why low-rank adaptation mattered) read as fashion rather than forced
moves.

**Part II ends on compression, not on scale.**
Chapter 10 (minimum description length, the length prior, typicality) is placed
last in the classical part because it retroactively unifies everything before it:
overfitting, generalization, and Occam's razor become one subject measured in
one unit. Placing it earlier would waste that effect.

---

## Visual design

**Palette: blueprint blue `#2B5DA8`, ink `#1C2733`, rust `#A64B2A` on cool
off-white `#F5F7F6`.**
Chosen against a specific failure mode: warm cream (`#F4F1EA`) with a
terracotta accent (`#D97757`) is currently the default look of machine-generated
design, and on a brief like this it reads as a tell. The engineering/graph-paper
direction is also *derived from the subject* — the book is about working things
out on paper.

**Rust is reserved.** It appears only on trap boxes and exercise-grade labels.
A reader learns within two chapters that rust means "here is where this is
misread". Spending it elsewhere would destroy that signal.

**Typography: Zilla Slab (display), Source Serif 4 (body), IBM Plex Mono
(utility).** A slab-serif display face reads as technical without reading as
brutalist; the mono face carries derivation labels, eyebrows, and numbers so
that quantitative material is visually distinct from prose.

**The graph-paper grid is the signature and it is load-bearing.** It appears on
the cover, on part dividers, and inside derivation boxes — and nowhere else.
Derivation boxes are where the reader is expected to work along, so the grid
marks them.

**The cover figure is computed, not drawn.** `build/coverfig.py` runs both
optimisers and plots the real trajectories. A cover that is itself the book's
first result is a stronger statement than any illustration.

---

## Structure

**Two editions from one source.** `src/` is canonical and is the web edition;
the PDF is derived. The alternative — maintaining separate sources — guarantees
drift.

**Solutions live in Appendix D, not inline.** Inline drills have collapsible
answers because they are formative; end-of-chapter B and C exercises do not,
because looking is too easy and the value is in the attempt.

**Readings are annotated with how to read them.** Every entry says what to do
with the source: "read the ablations as experiments about your Derivation 4.1",
"read it only *after* your first blank-paper attempt". A bare bibliography
transfers nothing.

**"What the chapter bought" is a fixed heading, repeated sixteen times.**
Deliberate: it is a structural device like "Summary", and consistency helps
navigation. The *content* beneath it varies — an early draft had eight of
sixteen opening with a bare count, which was a tic and was fixed.

---

## Technical

**WeasyPrint over headless Chrome.**
Real `@page` support: page geometry, running page numbers, and `target-counter`,
which is what lets the contents page resolve actual page numbers. Chrome's print
path cannot do the last one without JavaScript post-processing.

**Math is pre-rendered server-side.**
The PDF renderer executes no JavaScript and has no network access, so the ~1,850
LaTeX expressions are converted to static KaTeX markup by `build/prerender.js`
before assembly. The web edition still uses the CDN and renders in-browser.

**Everything is inlined as base64 in the print document.**
KaTeX's stylesheet and fonts, and all three typefaces, become data URIs. The
resulting `.cache/book-print.html` is a single self-contained file that renders
offline and archives cleanly. Fonts come from npm (`@fontsource/*`) rather than
Google Fonts, because the build environment cannot reach fonts.googleapis.com.

**Print CSS is a separate file, not a Python string.**
`build/print.css` is edited like CSS. It was embedded in `assemble.py` during
drafting and extracting it was worth the ten minutes.

**The audit ships with the repo.**
`tools/audit.py` is not scaffolding left behind; it is the thing that keeps a
batch-written book coherent, and every one of its six checks caught a real error.
CI runs it before building.
