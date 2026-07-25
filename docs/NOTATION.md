# Notation

The registry behind Appendix E. One row per symbol, listing every meaning it
carries and the chapters that use it. `make audit` checks that the chapter
lists here match where the symbol actually appears in `src/`, so this file
cannot quietly go stale.

**A symbol with more than one meaning must be redefined at first use in every
chapter that uses it** (`docs/STYLE.md`). The point of this table is not to
eliminate reuse — the field's conventions make that impossible — but to make
the collisions visible to whoever edits next.

---

## Collisions, worst first

| symbol | meanings | chapters |
|---|---|---|
| **β** | power-law exponent · momentum coefficient · bytes per stored value · KL strength on the leash · noise-schedule rate | 1, 2, 5, 11, 14, 16 |
| **k** | kernel side · compute constant in *C = kND* · number of task parts · draft length · top-*k* routing · number of samples · stride | 4, 7, 9, 12, 13, 15, 16 |
| **σ** | weight standard deviation · the logistic function · coding widths σ_p, σ_q · noise standard deviation | 1, 2, 3, 5, 6, 10, 14 |
| **α** | loss exponent · acceptance rate · noise-schedule retention ᾱ | 1, 12, 16 |
| **ε** | tolerance · clip width · predicted noise | 1, 2, 5, 14, 16 |
| **A, B** | loss coefficients · low-rank factors · advantage · option labels | 7, 13, 14, 17 |
| **d** | model width · head dimension d_head · vector dimension | 1, 6, 11 |
| **L** | the loss · number of layers | 2, 3, 7, 8, 11 |
| **E** | irreducible loss · number of experts · expectation | 7, 13 |
| **p** | probability · parameter count in the OLS risk · target distribution | 9, 10, 12, 15 |
| **γ** | discount factor · tokenizer compression ratio | 1, 2, 10 |
| **ρ** | contraction rate · probability ratio | 3, 14 |
| **κ** | condition number · additive reward constant | 3, 14 |

**β and k are the dangerous ones.** β carries five meanings, two of which — the
KL strength of Chapter 14 and the noise schedule of Chapter 16 — sit in
adjacent chapters. Both are the field's own notation and neither can be
renamed without making the book harder to read against the literature, so both
are redefined explicitly where they appear.

## Symbols with one meaning throughout

`N` parameters · `D` training tokens · `C` compute budget · `T` serving
lifetime in tokens · `s` sequence position/length · `H` number of heads ·
`V` vocabulary size · `θ` all parameters · `π` policy · `Φ` standard normal CDF ·
`Υ` the universal intelligence measure · `η` step size · `λ` curvature ·
`Δ` quantizer step · `Z` partition function.
