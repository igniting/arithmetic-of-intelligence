# The Arithmetic of Intelligence

**A problem course in modern machine learning, from the pathological valley to direct preference optimization.**

By Anshu Avinash.

A textbook that teaches machine learning the way physics is taught to engineers: as a small set of results you derive, drill, and then recognise everywhere. Sixteen chapters, four appendices, thirty-eight core derivations, roughly two hundred exercises with worked solutions, and eight labs whose acceptance criterion is a number your derivation predicted in advance.

Nothing in the book asks you to memorise a benchmark score, a release date, or an author list. Where a constant from the literature is needed it is *given*, the way `g = 9.8 m/s²` is given in a physics paper. What is never given is the model you must build to use it.

---

## Contents

| Part | Chapters |
|---|---|
| **I — Foundations** | 1 The Mathematical Toolkit |
| **II — The Classical Era (2012–2022)** | 2 The Geometry of Training · 3 The Architecture of Depth · 4 Memory and Gates · 5 Attention · 6 The Economics of Scale · 7 The Machinery of Scale · 8 Measurement · 9 Compression and Occam |
| **III — The Modern Era (2022– )** | 10 The Price of a Token · 11 Bytes over FLOPs · 12 Sparsity and Thrift · 13 Teaching Preferences · 14 Thinking at Inference Time · 15 Generation by Denoising · 16 The Whole Lifecycle |
| **Appendices** | A The Derivation Bank · B The Trap Taxonomy · C The Lab Manual · D Solutions |

Two editions are built from the same source: a linked **[web edition](https://igniting.github.io/arithmetic-of-intelligence/)** (`src/index.html`, math rendered in-browser by KaTeX) and a 177-page **PDF** (math pre-rendered, fonts embedded, fully self-contained). The PDF is built by CI and available as a build artifact on each push.

---

## Building

**Requirements:** Node 18+, Python 3.10+, and the system libraries WeasyPrint needs (Pango, cairo, GDK-PixBuf — on Debian/Ubuntu: `apt install libpango-1.0-0 libpangoft2-1.0-0 libcairo2 libgdk-pixbuf-2.0-0`).

```bash
make install     # npm deps + Python venv with pip dependencies
make pdf         # -> dist/The-Arithmetic-of-Intelligence.pdf
```

Other targets:

```bash
make figure      # regenerate the cover figure from its equations
make audit       # run the source consistency checks
make serve       # preview the web edition at localhost:8000
make clean       # remove build artefacts
```

### How the build works

The web edition is the canonical source. The PDF is derived from it in four steps, because the PDF renderer executes no JavaScript and has no network access:

1. **`build/coverfig.py`** → `figures/cover-figure.svg`
   Generates the cover figure by actually running the optimisers (see below).

2. **`build/prerender.js`** → `.cache/rendered/`
   Walks every `\( … \)` and `\[ … \]` expression in `src/*.html` and replaces it with static KaTeX markup — about 1,850 expressions. Strips the CDN `<script>` and `<link>` tags. Fails loudly rather than silently dropping an expression.

3. **`build/assemble.py`** → `.cache/book-print.html`
   Merges the twenty chapter and appendix files into one document with part dividers, a table of contents, and running page numbers. Inlines `build/print.css`, the KaTeX stylesheet, and all fonts as base64 data URIs, so the output is a single self-contained file.

4. **`build/topdf.py`** → `dist/`
   Renders with WeasyPrint (chosen over headless-Chrome for its `@page` support: real page geometry, running page numbers, and `target-counter` so the contents page resolves actual page numbers) and stamps PDF metadata.

---

## The cover figure

The cover is not decoration. It is a plot of the book's first derivation.

`build/coverfig.py` sets up the loss `L = ½(x² + 100y²)` — an ill-conditioned valley with condition number κ = 100 — and then *runs* two optimisers on it:

- **plain gradient descent** at 99% of its stability ceiling `η < 2/λ_max`, which ricochets between the valley walls;
- **heavy-ball momentum**, which damps that oscillation and accelerates along the floor.

After seventy steps momentum has reached the minimum while gradient descent is still a quarter of its starting distance away. That gap is the √κ speedup of Derivation 2.2, drawn rather than asserted.

One honest note: *optimally* tuned momentum (η = (2/(√λ_max+√λ_min))², β = ((√κ−1)/(√κ+1))²) overshoots so hard on its first swings that it leaves the frame. The figure uses well-tuned but less aggressive settings (β = 0.90, η = 0.008) that stay in view and still converge an order of magnitude faster. The caption says "gradient descent and momentum on an ill-conditioned valley", which is accurate.

---

## Repository layout

```
.
├── src/                    # the book — canonical source, also the web edition
│   ├── index.html          #   cover, preface, contents
│   ├── book.css            #   screen styles
│   ├── chapter-01..16.html
│   └── appendix-a..d.html
├── build/
│   ├── coverfig.py         # cover figure from its equations
│   ├── prerender.js        # LaTeX -> static KaTeX
│   ├── assemble.py         # merge + inline into one print document
│   ├── print.css           # page geometry, running heads, break rules
│   └── topdf.py            # render + metadata
├── tools/
│   └── audit.py            # source consistency checks
├── figures/
│   └── cover-figure.svg    # generated by build/coverfig.py
├── .github/workflows/
│   ├── build.yml               # CI: audit + build PDF on every push
│   └── pages.yml               # deploy web edition to GitHub Pages
├── Makefile
├── package.json            # katex, the three typefaces
└── requirements.txt        # weasyprint, pypdf
```

`.cache/` and `dist/` are intermediate/output directories and are git-ignored. The PDF is available as a CI build artifact from the Actions tab.

---

## The audit

`make audit` runs six classes of check over the source. They exist because this book was drafted in batches, and every one of them caught a real error at some point:

1. **Structure** — every chapter carries the same furniture: lead paragraph, derivation and worked-example boxes, closing section, readings, graded A/B/C exercises, a gate.
2. **Links** — every internal `href` resolves.
3. **Markup** — `<div>`, display-math delimiter, and `<details>` pairs balance in every file.
4. **Derivation references** — every "Derivation N.M" cited in a chapter is actually defined there.
5. **Solution coverage** — every B and C exercise has a matching solution in Appendix D.
6. **Prose** — chapter openings are not built from one template. This check exists because an early draft had twelve of sixteen chapters opening with the literal words "This chapter", which is invisible while writing and obvious while reading.

---

## Editing

Edit `src/*.html` directly; it is the source of truth for both editions. Each chapter is self-contained and follows one shape:

```
opener (eyebrow · title · one-line blurb)
lead paragraph
  §  prose, with:
       .box.deriv    numbered derivations
       .box.worked   worked examples with real arithmetic
       .box.trap     the ways this material is misread
       .drill        inline drills, answers in <details>
  "What the chapter bought"  — closing synthesis, hands off to the next chapter
  Exercises A (drills) / B (problems) / C (challenge)
  Gate  — what to reproduce on blank paper before continuing
  Readings — each link annotated with how to read it
```

Write math with `\( … \)` inline and `\[ … \]` display. Both editions pick it up automatically.

After editing, run `make audit && make pdf`.

---

## Licence

Split licence — see [LICENSE](LICENSE) for full text:

- **Book content** (`src/`, `figures/`): [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- **Build tooling** (`build/`, `tools/`, Makefile, CI): MIT
