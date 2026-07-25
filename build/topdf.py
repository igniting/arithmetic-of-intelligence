#!/usr/bin/env python3
"""Render the assembled HTML to a PDF and stamp its metadata.

Reads   .cache/book-print.html
Writes  dist/The-Arithmetic-of-Intelligence.pdf

Run:  python3 build/topdf.py
"""
import logging
import pathlib
import time

from weasyprint import HTML
from pypdf import PdfReader, PdfWriter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / ".cache" / "book-print.html"
DIST = ROOT / "dist"
OUT = DIST / "The-Arithmetic-of-Intelligence.pdf"

TITLE = "The Arithmetic of Intelligence"
AUTHOR = "Anshu Avinash"
SUBJECT = ("A problem course in modern machine learning, from the pathological "
           "valley to direct preference optimization")

# WeasyPrint is chatty about CSS it does not implement; none of it is fatal here.
logging.getLogger("weasyprint").setLevel(logging.ERROR)


def main():
    if not SRC.exists():
        raise SystemExit("no .cache/book-print.html — run `python3 build/assemble.py` first")

    DIST.mkdir(exist_ok=True)

    t0 = time.time()
    HTML(filename=str(SRC)).write_pdf(str(OUT))
    elapsed = time.time() - t0

    # Stamp document metadata.
    reader = PdfReader(str(OUT))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({
        "/Title": TITLE,
        "/Author": AUTHOR,
        "/Subject": SUBJECT,
        "/Keywords": ("machine learning, derivations, scaling laws, inference, "
                      "post-training, diffusion"),
        "/Creator": TITLE,
    })
    with open(OUT, "wb") as fh:
        writer.write(fh)

    pages = len(PdfReader(str(OUT)).pages)
    size = OUT.stat().st_size / 1024 / 1024
    print(f"pdf: {OUT.relative_to(ROOT)}")
    print(f"  {pages} pages, {size:.1f} MB, rendered in {elapsed:.0f}s")


if __name__ == "__main__":
    main()
