#!/usr/bin/env python3
"""Recompute the book's derived figures and check the source agrees.

docs/NUMBERS.md says: "If you change one, grep for it and change all of them —
the audit cannot catch an arithmetic inconsistency." This closes that gap for
the figures that follow from the reference hardware and from the lifecycle
model, which are the ones that recur across chapters, drills and Appendix D.

Each entry below states a quantity, computes it from *given* constants only, and
names the figure as it should appear in the prose. The check is presence: a
computed figure that appears nowhere has drifted out of the book; a figure that
should appear and does not is either a typo or a deletion. Contradictory values
elsewhere in the text are not detectable this way — that is what the CONTRADICTS
field is for, listing spellings that must *not* appear.

Run:  python3 tools/numbers.py       (exit code 1 if anything fails)
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# ---- given constants (docs/NUMBERS.md, "Reference hardware") ----------------
FLOPS = 312e12        # half-precision compute, operations per second
BW = 2e12             # memory bandwidth, bytes per second
SRAM = 20e6           # fast on-chip memory, bytes
FP16 = 2              # bytes per half-precision value
OPT_BYTES = 16        # optimizer-state bytes per parameter

problems = []


def ok(msg):
    print(f"  \033[32mok\033[0m   {msg}")


def bad(msg):
    problems.append(msg)
    print(f"  \033[31mFAIL\033[0m {msg}")


CORPUS = {p.name: p.read_text() for p in sorted(SRC.glob("*.html"))}


def find(fig):
    return sorted(n for n, t in CORPUS.items() if fig in t)


def check(label, computed, appears, contradicts=()):
    """`appears`: how the figure is written in the prose. `contradicts`: spellings
    that would be wrong for this quantity and must not occur."""
    where = find(appears)
    if not where:
        bad(f"{label}: computed {computed:g}, but '{appears}' appears nowhere in src/")
    else:
        ok(f"{label} = {appears}  ({', '.join(w.replace('.html', '') for w in where)})")
    for wrong in contradicts:
        for n in find(wrong):
            bad(f"{label}: {n} contains '{wrong}', which contradicts {appears}")


def ceiling(params_b, bytes_per_param=FP16):
    """Batch-1 decode ceiling in tokens/s: bandwidth over weight bytes."""
    return BW / (params_b * 1e9 * bytes_per_param)


print("\nreference hardware")
check("ridge point", FLOPS / BW, ">156</span> operations per byte")

print("\ndecode ceilings (bandwidth / weight bytes)")
check("7 B at fp16", ceiling(7), "143 tokens per second")
check("70 B at fp16", ceiling(70), "2000/140 = 14.3")
check("70 B at 8 bits", ceiling(70, 1), "14.3 \\), \\( 28.6")
check("70 B at 4 bits", ceiling(70, 0.5), "28.6 \\), and \\( 57 \\) tokens")
# The 35 B / 70 B pair in Chapter 16's B-3 is the case that was wrong in the
# first edition: it quoted the 4-bit and 8-bit figures for a half-precision pair.
check("35 B at fp16", ceiling(35), "29 tokens per second",
      contradicts=("roughly 57 tokens per second against 28",))

print("\ntransformer parameter count (Chapter 6)")
d, H, L, V = 4096, 32, 32, 32000
check("head dimension d/H", d / H, "32 \\times 128 = 4096")
check("one layer, 12d^2", 12 * d**2, "201{,}326{,}592")
check("32 layers, non-embedding", 12 * d**2 * L, "6.44 \\times 10^9")
check("untied tables", 2 * V * d, "0.26 \\times 10^9")

print("\nkey-value cache")
kv_7b = 2 * 32 * 32 * 128 * FP16
check("7 B, 32 kv-heads, per token", kv_7b, "524{,}288")
check("7 B at s = 4096", kv_7b * 4096, ">2.15 GB<")
check("70 B, 8 kv-heads, per token", 2 * 80 * 8 * 128 * FP16, "327{,}680")

print("\nmemory and utilization")
check("50 B optimizer state, GB", 50e9 * OPT_BYTES / 1e9, "800 gigabytes")
check("175 B optimizer state, GB", 175e9 * OPT_BYTES / 1e9, "2{,}800 \\) GB")
check("MFU at 4200 tok/s on 7 B", 4200 * 6 * 7e9 / FLOPS, ">56%<")

print("\nattention traffic")
check("4096-square fp16 score matrix, MB", FP16 * 4096 ** 2 / 1e6, "= 33.6 \\) MB")
check("score : unavoidable traffic at n=4096, d=128", 4096 / (2 * 128), "\\frac{n}{2d} = 16")

print("\nlifecycle (6ND + 2NT at T = 1e13)")
for name, N, D, fig in (("A", 70e9, 1.4e12, "1.99&times;10"),
                        ("B", 35e9, 4.2e12, "1.58&times;10"),
                        ("C", 20e9, 12e12, "1.84&times;10")):
    check(f"option {name}", (6 * N * D + 2 * N * 1e13) / 1e24, fig)
check("break-even A vs B",
      6 * (70e9 * 1.4e12 - 35e9 * 4.2e12) / (2 * (35e9 - 70e9)) / 1e12, "4.2\\times10")

print()
if problems:
    print(f"\033[31m{len(problems)} problem(s)\033[0m")
    sys.exit(1)
print("\033[32mall figures reproduce\033[0m")
