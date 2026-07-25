# Numbers

Every figure the book highlights, what it is, and where it appears. Many recur
across a chapter, its drills, and Appendix D. **If you change one, grep for it
and change all of them** — the audit cannot catch an arithmetic inconsistency.

Figures marked <span>**given**</span> are supplied to the reader as data, in
keeping with the book's central rule (`docs/DECISIONS.md`). Everything else is
derived in the text.

`make numbers` now recomputes the figures that follow from the reference
hardware and the lifecycle model, and checks the source against them. It does
not cover the whole table; rows outside its scope are still yours to grep.

Two rows are under revision — see `docs/SECOND-EDITION-PLAN.md`:

- **16 bytes/parameter** is marked *given* below and should not be. It is a
  count (4 fp32 master weight + 4 momentum + 4 second moment + 4 fp32 gradient),
  not a measurement, and WP3 derives it. The label changes when the derivation
  lands, not before.
- The **Chapter 6 perplexity row** records a result that appears nowhere in
  `src/`. It is kept here as a commitment to write it, not as a record of the
  text as it stands. Flagged below.

---

## Reference hardware (Part III)

Introduced once in Chapter 11 and treated as established in 12, 13 and 17.

| quantity | value | note |
|---|---|---|
| half-precision compute | **312 TFLOP/s** | given |
| memory bandwidth | **2 TB/s** | given |
| fast on-chip memory | **20 MB** | given |
| bytes per half-precision value | **2** | given |
| ridge point | **156** ops/byte | derived: 312e12 / 2e12 |

---

## Chapter 3 — The Geometry of Training

| result | value |
|---|---|
| stable step size | η < 2/λ_max |
| GD steps, κ = 100, error ÷ 10³ | **345** |
| momentum steps, same target | **34** |
| ratio | **10** = √κ |
| fan-in 4096 with σ = 0.01 → output variance | 0.41 |

## Chapter 4 — The Architecture of Depth

| result | value |
|---|---|
| 227×227 → 11×11 s4 conv → 3×3 s2 pool | 55 → **27** |
| that conv's parameters | **34,944** (biases included) |
| bottleneck vs plain 3×3 pair, c = 4 | **≈ 17 : 1** |
| 54-block ResNet, paths of length 20–34 | **≈ 96%** (z = ±2.04) |
| 5×5 → two 3×3 at C = 256, weights saved | **458,752** |
| dilations 1,2,4,…,2ⁿ⁻¹ receptive field | 2ⁿ⁺¹ − 1 |
| RF ≥ 500 needs n = | **8** (gives 511) |
| single-kernel : dilated-stack weights | **≈ 3,600 : 1** |

## Chapter 5 — Memory and Gates

| result | value |
|---|---|
| horizon at f = 0.95, ε = 0.01 | **90 steps** |
| forget-gate bias for f = 0.95 | **2.94** = ln 19 |
| recurrent-path dropout, keep 0.9, 100 steps | **2.7 × 10⁻⁵** |
| example model total parameters | **66 M** |
| — of which embedding + readout | **≈ 45%** |
| WER law: −40% per decade → halving costs | **≈ 23×** data (273k hours) |

## Chapter 6 — Attention

| result | value |
|---|---|
| Var(q·k) at d = 512 → sd | **22.6** = 16√2 |
| attention/feed-forward crossover | **n = 4d** |
| reversed lag at position j | 2j − 1 |
| mean reversed lag | **exactly n** (unchanged) |
| perplexity 114.5 → 78.4 | **0.55 bits/token** — ⚠ not yet in the text |

## Chapter 7 — The Economics of Scale

| result | value |
|---|---|
| optimum condition | aAN⁻ᵃ = bBD⁻ᵇ |
| scaling | N ∝ C^(b/(a+b)), D ∝ C^(a/(a+b)) |
| halving a term ∝ N^−0.076 costs | **≈ 9,100×** parameters |
| 175 B / 300 B tokens re-budgeted at ratio 20 | **51 B** parameters, ≈ 1.02 T tokens |
| D ∝ N^0.74, params ×1000 → data × | **166** |

Exponents 0.076, 0.095, 0.74 are **given**.

## Chapter 8 — The Machinery of Scale

| result | value |
|---|---|
| bubble fraction | (P−1)/(M+P−1) |
| P = 8, M = 1 | **87.5%** idle |
| P = 8, bubble ≤ 5% requires | **M ≥ 133** |
| 50 B params × 16 B/param | **800 GB**, → **12.5 GB** across 64 |

16 bytes/parameter of optimizer state is **given**.

## Chapter 9 — Measurement

| result | value |
|---|---|
| exact-match accuracy | p^k |
| 50% frontier | p = 2^(−1/k) |
| k = 8 table | 0.50→0.004, 0.70→0.058, 0.80→0.168, 0.90→**0.430**, 0.95→0.663 |
| p: 0.67 → 0.90 at k = 8 | **4% → 43%** |
| largest k with p = 0.98 ≥ 50% | **34** |
| observed 0.70, clean 0.60 → contamination | **c = 0.25** |
| P(contaminated | correct) | **0.357** |

## Chapter 10 — Compression and Occam

| result | value |
|---|---|
| MDL table (12 bits/param) | A 516, **B 430** ← selected, C 720 |
| two-hypothesis totals | H₁ 40, H₂ 47 → H₁ wins by **7 bits** |
| Kraft, lengths 1,2,3,3 | sums to **1** |
| 23 B tokens at 1.6 bits | **4.6 GB** |
| posterior, programs 8/12/20 bits | P(next = 1) = **0.941** |
| log₂C(10000,5000) | **≈ 9,993 bits** |
| OLS risk ratio, p = 90 vs 50, n = 100 | **9.8** |
| grokking compression | **20×** (10,000 → 500 bits) |
| Legg's Υ for V=(.5,.9,.3), K=(1,2,3) | **0.51** |
| wireheading threshold, γ = 0.95 | r > **0.053** = 1/19 |
| Gaussian coding, σp=1 σq=0.1 μ=0.5 | 1.93 nats = **2.79 bits** |

OLS excess risk σ²p/(n−p−1) is **given**.

## Chapter 11 — The Price of a Token

| result | value |
|---|---|
| KV cache | 2·L·H_kv·d_head·s·B·bytes |
| 7 B, L=32, H=32, d=128, s=4096, fp16 | **0.5 MB/token**, **2.15 GB** total |
| same with H_kv = 8 | **0.54 GB** |
| batch-1 decode intensity | ≈ **1** op/byte (vs ridge 156) |
| decode ceiling, 14 GB weights | **143 tokens/s** |
| MFU at 4200 tok/s on 7 B | **56%** |

## Chapter 12 — Bytes over FLOPs

| result | value |
|---|---|
| streaming softmax, blocks {2,1} then {3,0} | **1.553** both ways |
| n = 4096 fp16 score matrix | **33.6 MB** (> 20 MB SRAM) |
| score : unavoidable traffic | n/(2d) = **16 : 1** |
| tokens per cycle | (1 − α^(k+1))/(1 − α) |
| α=0.8, k=4, c=0.1 | 3.36 per 1.4 → **2.4×** |
| α=0.5, same | **1.38×** |

## Chapter 13 — Sparsity and Thrift

| result | value |
|---|---|
| 32 layers, 8 experts × 150 M, top-2 | total **40 B**, active **11.2 B** |
| aux loss, f=(.7,.3) P=(.6,.4) | **1.08** (minimum 1) |
| capacity 1.25 × 1024/8 = 160; 200 routed | **40 dropped** |
| quantization MSE | Δ²/12, Δ = 2R/2^b |
| LoRA at d=4096, r=16 | 131,072 = **0.78%** |
| 7 B optimizer state, full → LoRA | 112 GB → **1.1 GB** |

## Chapter 14 — Teaching Preferences

| result | value |
|---|---|
| BT loss, r_w=1.2 r_l=0.7 | **0.474 nats** (shift-invariant) |
| PPO ε=0.2, ρ=1.3 A=+2 | 2.4, **gradient dead** |
| PPO ε=0.2, ρ=0.7 A=−1 | −0.8, **gradient dead** |
| DPO β=0.2, ratios 1.0 / −0.5 | margin 0.3, loss **0.554**, weight 0.426 |
| DPO loss at initialization | **ln 2 = 0.693** ← Lab 6 acceptance |
| GRPO group (1,1,1,0,0) | **+0.82** / **−1.22** |
| 7 B policy vs policy+critic | 140 GB vs **280 GB** |

## Chapter 15 — Thinking at Inference Time

| result | value |
|---|---|
| coverage | 1 − (1−p)^k |
| cost-1 p=0.2 ×10 vs cost-10 p=0.6 | **0.893** vs 0.60 |
| same with selector v = 0.7 | **0.625** |
| 5 chains at p = 0.6 | **0.683** |
| 5 chains at p = 0.4 | **0.317** (worse than one) |

## Chapter 16 — Generation by Denoising

| result | value |
|---|---|
| forward process | N(√ᾱ x₀, (1−ᾱ)I) |
| β = 0.02, SNR = 1 at | **t = 34** |
| ᾱ at t = 100 | 0.133 |
| CFG ε_u=0.20, ε_c=0.30, w=7.5 | **0.95** (extrapolation) |

## Chapter 17 — The Whole Lifecycle

| result | value |
|---|---|
| lifetime cost | 6ND + 2NT |
| A(70 B, 1.4 T) at T = 10¹³ | **1.99 × 10²⁴** |
| B(35 B, 4.2 T) at T = 10¹³ | **1.58 × 10²⁴** ← wins |
| C(20 B, 12 T) at T = 10¹³ | **1.84 × 10²⁴** (interior optimum) |
| break-even lifetime A vs B | **4.2 × 10¹²** tokens |

---

## Cover figure

Generated by `build/coverfig.py`; regenerate with `make figure`.

| quantity | value |
|---|---|
| loss | L = ½(x² + 100y²), κ = 100 |
| start | (1.00, 0.34) |
| GD step size | 0.99 × 2/λ_max = **0.0198** |
| GD y-contraction | **−0.980** (persistent zigzag) |
| momentum | β = **0.90**, η = **0.008** |
| after 70 steps | GD \|x\| = **0.247**, momentum \|x\| = **0.0006** |

Momentum is well-tuned rather than optimally tuned: the optimal setting for
κ = 100 overshoots outside the frame on its first swings. See the comment in
`build/coverfig.py`.
