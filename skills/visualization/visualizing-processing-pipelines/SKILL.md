---
name: visualizing-processing-pipelines
description: >
  Generate a single self-contained HTML report that visualizes and explains a multi-step processing pipeline. Each stage gets a before/after drag-to-compare slider, a difference heatmap, inline base64 images, what/why/formula annotations, timing bars, and pass/fail metrics. Use when the user wants to visualize, explain, debug, document, or present an image / data / ML pipeline; build before/after comparison sliders; create an algorithm walkthrough or a parameter-tuning playground; or turn scattered intermediate results into one shareable file. Covers both a static exported .html and an interactive server with live parameter sliders.
license: MIT
---

# Pipeline Visualization Report

Turn a multi-step pipeline (image processing, data transforms, an ML inference
chain) into **one HTML file that explains itself** — every intermediate result
embedded inline, every step annotated with *what it does* and *why*, and a
drag-to-compare slider so the reader sees exactly what each stage changed.

Two delivery modes:

| Mode | What it is | Use when |
|---|---|---|
| **Static report** | One `.html`, all images base64-embedded, no server | sharing, code review, docs, email, archiving a result |
| **Interactive server** | Local HTTP server, parameter sliders, live re-run | tuning parameters, exploring an algorithm |

Most requests want the **static report** — start there. The interactive server
reuses the exact same encode/HTML helpers; its recipe is in
`references/design-patterns.md`.

## When to use this skill

Trigger on requests like: "visualize this pipeline", "show before/after for
each step", "explain the algorithm with images", "make a comparison slider",
"build a report of the intermediate results", "I want to tune these parameters
and see the effect", "document this matting/segmentation/processing flow".

## Quickstart — use the bundled builder, don't reinvent it

`references/scripts/viz_report.py` is the reusable, pipeline-agnostic core. It depends only
on `numpy` + `opencv-python`. Copy it next to your pipeline code (or add its
folder to `sys.path`) and drive it:

```python
from viz_report import PipelineReport

rep = PipelineReport("My Pipeline", "one-line subtitle")

rep.add_step(
    1, "Denoise", time_ms=12,
    algo_html="Median filter removes salt-and-pepper noise.",          # WHAT
    why_html="Median beats Gaussian here: it preserves edges while "    # WHY
             "killing outliers.",
    formula_html="out = median(in, k=3)",                              # MATH
    compare=(noisy_bgr, clean_bgr, "Noisy", "Denoised"),               # slider
    diff=(noisy_bgr, clean_bgr),                                       # auto heatmap
)
rep.add_timings({"denoise": 0.012, "threshold": 0.004})
rep.add_metrics({"PSNR": ("31.4 dB", True), "Verdict": ("PASS", True)})
rep.export("report.html")
```

A complete runnable demo (no external assets, synthetic image) is in
`references/examples/minimal_example.py`:

```bash
python references/examples/minimal_example.py /tmp/demo.html
```

## Builder API (the parts you need)

- `PipelineReport(title, subtitle, display_width=1024, jpeg_quality=88, lang="en")`
- `.add_step(num, title, *, time_ms, algo_html, why_html, formula_html, images, compare, diff, diff_caption)`
  - `images`: list of `(caption, array, kind)` where `kind` ∈ `"color" | "gray" | "heat" | "mask"`
  - `compare`: `(before, after, left_label, right_label[, kind])` → draggable slider
  - `diff`: a float array (rendered as heatmap), **or** `(before, after)` to auto-compute `|after-before|`
- `.add_timings({name: seconds})` → proportional bottleneck bars
- `.add_metrics({label: value | (value, ok)})` → `ok` True/False/None ⇒ green/red/neutral
- `.export(path)` → writes the single file

Standalone encode helpers (for the interactive server, or custom layouts):
`encode(img, kind=, png=)`, `diff_heat(before, after)`, `resize_for_display(img, max_w)`.

## Authoring the annotations — this is what makes it *explanatory*

A screenshot dump is not a report. For each step write three things, in
increasing optionality:

1. **`algo_html` (what)** — 1–3 sentences. What the step computes.
2. **`why_html` (why)** — the non-obvious justification: why *this* method over
   the obvious alternative, what artifact it prevents, what tradeoff it makes.
   This is the highest-value text — it is what a reader cannot reconstruct from
   the code alone.
3. **`formula_html` (how)** — the actual math/pseudocode in monospace. Use
   `<br>` for line breaks, `<code>` inline.

Prefer a **compare slider over side-by-side** images: the eye detects change far
better when the two states occupy the same pixels. Always pair a slider with a
**diff heatmap** — it answers "what *exactly* changed?" without hunting.

## Gotchas worth knowing

- **Compare / diff need same-size pairs**: the slider overlays both images in
  the same pixels and `diff_heat` subtracts arrays, so a crop/scale step that
  changes geometry breaks both — resize or crop to a common size before
  comparing. Both helpers raise a clear error if the shapes differ.
- **File size**: every image is base64-embedded, so a 10-step pipeline at 4K is
  tens of MB. `display_width` downscales before encoding (default 1024) — keep
  it. Pixel-peeping is not the point; *seeing the difference* is.
- **Masks / trimaps / line-art**: use `kind="mask"` (grayscale + lossless PNG).
  JPEG ringing puts ghost halos on hard edges and lies about what you produced.
- **Heatmaps for any float field**: difference maps, weight maps, attention,
  depth — `kind="heat"` (JET colormap) reads instantly; a dim grayscale ramp
  does not.
- **Color order**: helpers assume **BGR uint8** (cv2). Convert RGB first.

## Files in this skill

- `references/scripts/viz_report.py` — the reusable builder. **Run/import this; don't rebuild it.**
- `references/examples/minimal_example.py` — runnable synthetic demo.
- `references/design-patterns.md` — the *why* behind the design choices, plus the
  full interactive-server (parameter-slider) recipe and a rebrand/theming guide.
  Read it when building the server mode or adapting the look.
