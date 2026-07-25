# Style

The writing rules for this book. Most were discovered by measuring an early
draft and finding it defective; the numbers below are real.

**Read this before writing any prose for the book.**

---

## The voice

You are a teacher explaining something to one student who is capable and
currently confused. Not a reference work, not a survey, not a lecture to a hall.

The concrete test: **does the text anticipate what the reader will get wrong?**
An early draft contained, across 35,000 words, *zero* instances of the move a
teacher makes constantly — predicting the student's wrong first guess and
addressing it. That was the single largest defect found in the whole project,
and it is invisible unless you look for it.

Do this before the hard derivations:

> Before deriving it, guess. If one direction of the bowl is a hundred times
> steeper than another, how much does that slow you down — a little, or a lot?
> Most people's instinct is that it costs a constant factor, some fixed tax for
> an awkward shape. The instinct is wrong, and wrong in an important way.

And name where people actually fail:

> One warning before we start, because nearly everyone makes the same mistake
> here on first contact.

## Chapter openings

**Do not use a template.** Measured in an early draft:

- 12 / 16 openings contained the literal words "This chapter"
- 8 / 16 began with a "Chapter N did X" callback
- 10 / 16 used the same em-dash-plus-coda rhythm

A reader feels this by chapter four without being able to name it.
`tools/audit.py` now fails the build if it recurs.

Vary the *mode*, not just the words. The sixteen current openings use: a direct
instruction, a scenario you are placed inside, a puzzle, a concrete failure, a
contrast, a decision you must make, a physical setup, a claim you should not yet
believe, a statement that sounds like metaphor and is not, a surprising number,
an apparent paradox, a warning about vocabulary, a problem statement, a question
about spending, a strange idea stated plainly, and a return to the beginning.

**After rewriting an opening, read the paragraph beneath it.** Seven of sixteen
rewritten openings collided with the text that followed — one said "calculus
problem" twice in adjacent paragraphs. Editing in isolation causes this.

## Chapter closings

Every chapter ends with **"What the chapter bought"** — a fixed heading, on
purpose. But an early draft had eight of sixteen opening that section with a
bare count: "Six reflexes", "Three results", "Two rulers, two illusions", "One
principle", "Three formulas". That is a tic. Vary the sentence.

The closing must also hand off to the next chapter with a reason, not a
label. Not "Chapter 7 covers parallelism" but "once a model is too large for one
accelerator, how is the work split, and what does that splitting cost?"

## Sentences

- **Justify the claim in the sentence that makes it.** "Momentum converts a
  κ-dependence into a √κ-dependence" is a claim; the worked example that follows
  it is the payment.
- **Prefer a computed number to an adjective.** Not "much more expensive" but
  "a nine-thousand-fold increase in parameters".
- **Em-dashes are fine but they are not a rhythm.** If three consecutive
  paragraphs end with one, you are writing a formula, not prose.
- **Avoid "it is worth noting", "the whole point is", "importantly".** If it were
  not worth noting you would have cut it.
- **Second person is correct here.** "You will bounce from wall to wall." The
  book is addressed to a reader who is working, not observing.

## The boxes

Four kinds, and they mean different things. Do not blur them.

| box | contains | rule |
|---|---|---|
| `.box.deriv` | a numbered derivation | must be reproducible on blank paper; every step shown |
| `.box.worked` | a worked example | must contain real arithmetic with a stated result |
| `.box.trap` | how this material is misread | must name a trap class from Appendix B |
| `.drill` | a short exercise | answer in `<details>`, one click away |

A derivation box that hand-waves a step is worse than no box, because the reader
is being asked to reproduce it later.

## Mathematics

Inline `\( … \)`, display `\[ … \]`. Both editions pick these up automatically.

- **Define every symbol at first use in a chapter**, even if defined earlier in
  the book. Readers arrive mid-book.
- **State what is given.** If an exponent or a bandwidth is supplied rather than
  derived, say so explicitly — the book's central promise depends on it.
- **Show the substitution.** The derivations that matter here are mostly
  substitute-then-differentiate; the value is in seeing which term cancels and
  why, so do not skip to the result.

## Numbers

Every figure in the book has been checked. `docs/NUMBERS.md` records the ones
that recur and where. **If you change a number, grep for it** — most appear in a
chapter, sometimes in a drill, and again in Appendix D.

Round consistently: three significant figures in prose, exact integers where the
answer is an integer, and always with units named.

## Readings

Each entry is a link plus **one line saying how to read it**. Never a bare
citation. Examples in use:

> read the ablations as experiments about your Derivation 3.1
> three pages, read fully
> read it only *after* your first blank-paper attempt at Derivation 13.2
> skim for what changed — work partitioning, not mathematics

## Checks before committing

```bash
make audit          # six structural checks, exits non-zero on failure
make pdf            # full build, ~100s
```

And by eye: read your new opening together with the paragraph after it, and read
your new closing together with the next chapter's opening. The seams between
adjacent pieces are where this book has historically broken.
