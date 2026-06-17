#!/usr/bin/env python3
"""
Minimal end-to-end demo of viz_report.PipelineReport.

Builds a synthetic 3-step image pipeline (blur -> threshold -> edges) on a
generated image, with zero external assets, and writes one self-contained
HTML file you can open in any browser.

Run:
    python minimal_example.py            # writes /tmp/viz_demo.html
    python minimal_example.py out.html   # custom path
"""

import os
import sys
import time

import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from viz_report import PipelineReport  # noqa: E402


def make_input(h=360, w=540):
    """Synthetic scene: gradient + shapes + noise (no files needed).
    Seeded RNG => the demo output is byte-for-byte reproducible."""
    rng = np.random.default_rng(42)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    base = (xx / w * 160 + yy / h * 60).astype(np.uint8)
    img = cv2.cvtColor(base, cv2.COLOR_GRAY2BGR)
    cv2.circle(img, (w // 3, h // 2), 70, (60, 180, 230), -1)
    cv2.rectangle(img, (w * 6 // 10, h // 4), (w * 9 // 10, h * 3 // 4),
                  (200, 120, 60), -1)
    noise = rng.integers(0, 60, img.shape, dtype=np.int16)
    return np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/viz_demo.html"
    img = make_input()

    rep = PipelineReport(
        "Demo Pipeline",
        "blur → threshold → edges — synthetic example for the viz-report skill")

    timings = {}

    # Step 1: denoise
    t = time.time()
    blur = cv2.GaussianBlur(img, (7, 7), 0)
    timings["blur"] = time.time() - t
    rep.add_step(
        1, "Gaussian Denoise", time_ms=timings["blur"] * 1000,
        algo_html="Apply a <strong>7&times;7 Gaussian blur</strong> to suppress "
                  "the additive sensor noise before downstream thresholding.",
        why_html="A light blur first means the threshold step keys off real "
                 "structure instead of speckle — otherwise every noisy pixel "
                 "becomes its own tiny blob.",
        formula_html="out = GaussianBlur(in, k=7&times;7, &sigma;=auto)",
        compare=(img, blur, "Noisy input", "Denoised"),
        diff=(img, blur))

    # Step 2: threshold
    t = time.time()
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    timings["threshold"] = time.time() - t
    rep.add_step(
        2, "Otsu Threshold", time_ms=timings["threshold"] * 1000,
        algo_html="Binarise with an <strong>Otsu</strong> threshold, which picks "
                  "the cut that minimises intra-class variance automatically.",
        why_html="Otsu adapts to the image histogram, so the same code works "
                 "across exposures without a hand-tuned constant.",
        images=[("Binary mask", mask, "mask")])

    # Step 3: edges
    t = time.time()
    edges = cv2.Canny(gray, 60, 160)
    timings["edges"] = time.time() - t
    rep.add_step(
        3, "Canny Edges", time_ms=timings["edges"] * 1000,
        algo_html="Extract contours with the <strong>Canny</strong> detector.",
        images=[("Edges", edges, "mask")])

    rep.add_timings(timings)
    rep.add_metrics({
        "Foreground %": (f"{(mask > 0).mean() * 100:.1f}%", None),
        "Edge pixels": (f"{int((edges > 0).sum())}", None),
        "Verdict": ("PASS", True),
    })

    rep.export(out)


if __name__ == "__main__":
    main()
