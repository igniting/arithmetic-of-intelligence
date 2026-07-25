#!/usr/bin/env python3
"""Assemble the pre-rendered chapters into a single print-ready HTML document.

Reads   .cache/rendered/*.html   (output of build/prerender.js)
        build/print.css
        figures/cover-figure.svg
        node_modules/katex/dist/          (stylesheet + fonts)
        node_modules/@fontsource/...      (the three book typefaces)

Writes  .cache/book-print.html            — fully self-contained, no network

Everything external is inlined as base64 data URIs, so the resulting file can be
rendered offline and archived as a single artefact.

Run:  python3 build/assemble.py
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / ".cache" / "rendered"
NM = ROOT / "node_modules"
OUT = ROOT / ".cache" / "book-print.html"

TITLE = "The Arithmetic of Intelligence"
SUBTITLE = ("A problem course in modern machine learning, from the pathological "
            "valley to direct preference optimization.")
AUTHOR = "Anshu Avinash"
FIG_CAPTION = ("Gradient descent and momentum on an ill-conditioned valley "
               "&mdash; Chapter 3")

# (file, part divider to emit before it or None)
ORDER = [
    ("chapter-01.html", "Part I &middot; Foundations"),
    ("chapter-02.html", None),
    ("chapter-03.html", "Part II &middot; The Classical Era"),
    ("chapter-04.html", None), ("chapter-05.html", None),
    ("chapter-06.html", None), ("chapter-07.html", None),
    ("chapter-08.html", None), ("chapter-09.html", None),
    ("chapter-10.html", None),
    ("chapter-11.html", "Part III &middot; The Modern Era"),
    ("chapter-12.html", None), ("chapter-13.html", None),
    ("chapter-14.html", None), ("chapter-15.html", None),
    ("chapter-16.html", None), ("chapter-17.html", None),
    ("appendix-a.html", "Appendices"),
    ("appendix-b.html", None), ("appendix-c.html", None),
    ("appendix-d.html", None),
]

# The typeface files to embed: (css family name, package, filename pattern, variants)
FONTS = [
    ("Zilla Slab", "zilla-slab", "zilla-slab-latin-{w}-{s}.woff2",
     [("400", "normal"), ("500", "normal"), ("600", "normal"), ("700", "normal")]),
    ("Source Serif 4", "source-serif-4", "source-serif-4-latin-{w}-{s}.woff2",
     [("400", "normal"), ("600", "normal"), ("400", "italic"), ("600", "italic")]),
    ("IBM Plex Mono", "ibm-plex-mono", "ibm-plex-mono-latin-{w}-{s}.woff2",
     [("400", "normal"), ("500", "normal"), ("600", "normal")]),
]


def font_css():
    """Inline the book's typefaces as base64 woff2 @font-face rules."""
    faces = []
    for family, pkg, pattern, variants in FONTS:
        for weight, style in variants:
            fp = NM / "@fontsource" / pkg / "files" / pattern.format(w=weight, s=style)
            if not fp.exists():
                print(f"  ! missing font {fp.name}")
                continue
            b64 = base64.b64encode(fp.read_bytes()).decode()
            faces.append(
                f"@font-face{{font-family:'{family}';font-style:{style};"
                f"font-weight:{weight};font-display:swap;"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "\n".join(faces)


def katex_css():
    """KaTeX stylesheet with its fonts inlined; woff/ttf fallbacks dropped."""
    css = (NM / "katex" / "dist" / "katex.min.css").read_text()

    def embed(m):
        fp = NM / "katex" / "dist" / "fonts" / m.group(1)
        if not fp.exists():
            return m.group(0)
        b64 = base64.b64encode(fp.read_bytes()).decode()
        return f"url(data:font/woff2;base64,{b64})"

    css = re.sub(r"url\(fonts/([^)]+\.woff2)\)", embed, css)
    css = re.sub(r",\s*url\(fonts/[^)]+\.woff\)\s*format\(['\"]woff['\"]\)", "", css)
    css = re.sub(r",\s*url\(fonts/[^)]+\.ttf\)\s*format\(['\"]truetype['\"]\)", "", css)
    return css


def extract(fname):
    """Pull opener metadata and body content out of one chapter file."""
    html = (SRC / fname).read_text()

    def grab(pattern, default=""):
        m = re.search(pattern, html, re.S)
        return m.group(1).strip() if m else default

    body = grab(r"</header>(.*?)<footer>")
    body = re.sub(r"<footer>.*?</footer>", "", body, flags=re.S)
    return {
        "eyebrow": grab(r'<span class="eyebrow">(.*?)</span>'),
        "title": grab(r'<h1 class="ch">(.*?)</h1>', fname),
        "blurb": grab(r'<p class="ch-blurb">(.*?)</p>'),
        "body": body,
    }


def main():
    if not SRC.exists():
        raise SystemExit("no .cache/rendered — run `node build/prerender.js` first")

    # front matter comes from the web index page
    idx = (SRC / "index.html").read_text()
    m = re.search(r"<h2>Preface</h2>(.*?)<h2>Contents</h2>", idx, re.S)
    preface = m.group(1) if m else ""

    svg = (ROOT / "figures" / "cover-figure.svg").read_text()
    svg = svg.replace(' width="100%"', ' class="coverfig"')

    parts, toc = [], []
    for fname, part_label in ORDER:
        ch = extract(fname)
        num = ch["eyebrow"].split("&middot;")[-1].strip()
        label = num.replace("Chapter ", "").replace("Appendix ", "")
        kind = "Appendix" if "Appendix" in num else "Chapter"
        anchor = fname.replace(".html", "")

        if part_label:
            if "&middot;" in part_label:
                head, tail = part_label.split("&middot;", 1)
                eyebrow, heading = head.strip(), tail.strip()
            else:
                eyebrow, heading = "", part_label.strip()
            parts.append(
                f'<div class="part-page"><div class="part-inner">'
                f'<span class="part-eyebrow">{eyebrow}</span>'
                f'<h1 class="part-title">{heading}</h1></div></div>')
            toc.append(f'<li class="toc-part">{part_label}</li>')

        toc.append(
            f'<li class="toc-row"><span class="toc-num">{label}</span>'
            f'<span class="toc-title">{ch["title"]}</span>'
            f'<span class="toc-dots"></span>'
            f'<span class="toc-pg"><a href="#{anchor}"></a></span></li>')

        runhead = re.sub("<[^>]+>", "", ch["title"])
        parts.append(
            f'<section class="chapter" id="{anchor}">'
            f'<header class="ch-open">'
            f'<span class="ch-eyebrow">{ch["eyebrow"]}</span>'
            f'<h1 class="ch-title">{ch["title"]}</h1>'
            f'<p class="ch-blurb">{ch["blurb"]}</p></header>'
            f'<div class="ch-body" data-runhead="{kind} {label} &middot; {runhead}">'
            f'{ch["body"]}</div></section>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{TITLE}</title>
<style>{font_css()}</style>
<style>{katex_css()}</style>
<style>{(ROOT / 'build' / 'print.css').read_text()}</style>
</head>
<body>

<div class="cover-page">
  <div class="cover-fig">{svg}</div>
  <div class="cover-cap">{FIG_CAPTION}</div>
  <hr class="cover-rule">
  <h1 class="cover-title">The Arithmetic<br>of Intelligence</h1>
  <p class="cover-sub">{SUBTITLE}</p>
  <div class="cover-author">{AUTHOR}</div>
</div>

<div class="front">
<h2>Preface</h2>
{preface}
</div>

<div class="toc">
<h2>Contents</h2>
<ul>
{chr(10).join(toc)}
</ul>
</div>

{chr(10).join(parts)}

</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    print(f"assemble: {OUT.relative_to(ROOT)}  ({len(html) / 1024 / 1024:.1f} MB)")
    print(f"  {len(ORDER)} chapters/appendices, "
          f"{sum(1 for _, p in ORDER if p)} part dividers")


if __name__ == "__main__":
    main()
