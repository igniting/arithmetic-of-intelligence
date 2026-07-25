#!/usr/bin/env python3
"""Generate the cover figure: figures/cover-figure.svg

The figure is a plot of the book's first derivation (Chapter 2). It shows
elliptical level sets of an ill-conditioned quadratic loss together with two
trajectories that are genuinely computed by running the updates, not drawn
by hand:

  * plain gradient descent at 99% of its stability ceiling, which ricochets
    across the narrow direction of the valley;
  * well-tuned heavy-ball momentum, which damps that oscillation and reaches
    the minimum while gradient descent is still a quarter of the way out.

Run:  python3 build/coverfig.py
"""
import math
import pathlib

# ----------------------------------------------------------------- problem
LAM_X, LAM_Y = 1.0, 100.0        # curvatures; condition number kappa = 100
X0, Y0 = 1.00, 0.34              # starting point
STEPS = 70

# --- plain gradient descent, at 99% of the ceiling eta < 2 / lambda_max
ETA_GD = 0.99 * 2.0 / LAM_Y
gd = [(X0, Y0)]
x, y = X0, Y0
for _ in range(STEPS):
    x -= ETA_GD * LAM_X * x
    y -= ETA_GD * LAM_Y * y
    gd.append((x, y))

# --- heavy-ball momentum.
# Optimal tuning for kappa=100 is eta=(2/(sqrt(lx)+sqrt(ly)))^2, beta=((sqrt(k)-1)/(sqrt(k)+1))^2,
# but that overshoots far outside the frame on its first swings. These settings are
# well-tuned rather than maximally aggressive: they stay within the starting
# excursion and still converge an order of magnitude faster than gradient descent.
ETA_MOM, BETA = 0.008, 0.90
mo = [(X0, Y0)]
x, y, vx, vy = X0, Y0, 0.0, 0.0
for _ in range(STEPS):
    vx = BETA * vx - ETA_MOM * LAM_X * x
    vy = BETA * vy - ETA_MOM * LAM_Y * y
    x += vx
    y += vy
    mo.append((x, y))

# ---------------------------------------------------------------- viewport
W, H = 1000.0, 620.0
XR, YR = 1.32, 0.46                      # data half-ranges
CX, CY = W * 0.52, H * 0.5               # the minimum sits here


def px(p):
    return CX + p[0] / XR * (W * 0.44), CY - p[1] / YR * (H * 0.42)


def path_d(pts):
    return "M " + " L ".join(f"{px(p)[0]:.2f},{px(p)[1]:.2f}" for p in pts)


INK, BLUE, BLUED, RUST = "#1C2733", "#2B5DA8", "#1E4176", "#A64B2A"

# level sets of 1/2 (x^2 + 100 y^2) = c  ->  semi-axes sqrt(2c) and sqrt(2c)/10
contours = []
for i, c in enumerate([0.0022, 0.0075, 0.018, 0.037, 0.068, 0.115, 0.185, 0.285]):
    ax = math.sqrt(2 * c) / XR * (W * 0.44)
    ay = math.sqrt(2 * c / LAM_Y) / YR * (H * 0.42)
    op = max(0.40 - 0.030 * i, 0.13)
    contours.append(
        f'<ellipse cx="{CX:.1f}" cy="{CY:.1f}" rx="{ax:.2f}" ry="{ay:.2f}" '
        f'fill="none" stroke="{BLUE}" stroke-width="1.05" opacity="{op:.2f}"/>')

gd_pts = [p for p in gd if abs(p[0]) <= XR and abs(p[1]) <= YR]
mo_pts = [p for p in mo if abs(p[0]) <= XR and abs(p[1]) <= YR]

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="100%">
  <defs>
    <pattern id="gp" width="26" height="26" patternUnits="userSpaceOnUse">
      <path d="M 26 0 L 0 0 0 26" fill="none" stroke="{BLUE}" stroke-width="0.6" opacity="0.10"/>
    </pattern>
    <pattern id="gp5" width="130" height="130" patternUnits="userSpaceOnUse">
      <path d="M 130 0 L 0 0 0 130" fill="none" stroke="{BLUE}" stroke-width="0.9" opacity="0.16"/>
    </pattern>
  </defs>

  <rect width="{W:.0f}" height="{H:.0f}" fill="url(#gp)"/>
  <rect width="{W:.0f}" height="{H:.0f}" fill="url(#gp5)"/>

  {"".join(contours)}

  <line x1="{CX - W*0.44:.1f}" y1="{CY:.1f}" x2="{CX + W*0.44:.1f}" y2="{CY:.1f}"
        stroke="{INK}" stroke-width="0.7" stroke-dasharray="5 5" opacity="0.30"/>

  <path d="{path_d(gd_pts)}" fill="none" stroke="{RUST}" stroke-width="1.7"
        stroke-linejoin="round" opacity="0.92"/>
  <path d="{path_d(mo_pts)}" fill="none" stroke="{BLUED}" stroke-width="2.6"
        stroke-linejoin="round" stroke-linecap="round"/>

  <circle cx="{px((X0,Y0))[0]:.1f}" cy="{px((X0,Y0))[1]:.1f}" r="5" fill="{INK}"/>
  <circle cx="{CX:.1f}" cy="{CY:.1f}" r="3.4" fill="none" stroke="{INK}" stroke-width="1.6"/>
  <circle cx="{CX:.1f}" cy="{CY:.1f}" r="8.5" fill="none" stroke="{INK}" stroke-width="0.7" opacity="0.45"/>
</svg>'''

root = pathlib.Path(__file__).resolve().parent.parent
out = root / "figures" / "cover-figure.svg"
out.parent.mkdir(exist_ok=True)
out.write_text(svg)

print(f"wrote {out.relative_to(root)}")
print(f"  gradient descent : eta={ETA_GD:.5f}  "
      f"y-contraction {1 - ETA_GD*LAM_Y:+.3f}  end |x| = {abs(gd[-1][0]):.3f}")
print(f"  momentum         : eta={ETA_MOM:.3f} beta={BETA:.2f}  "
      f"end |x| = {abs(mo[-1][0]):.4f}")
