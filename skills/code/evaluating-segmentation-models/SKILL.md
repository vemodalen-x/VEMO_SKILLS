---
name: evaluating-segmentation-models
description: 'Evaluate a segmentation or image-matting model with the right metrics instead of eyeballing outputs. Use when accepting a trained seg/matting model, comparing two checkpoints, or judging whether a converted or quantized model still meets quality — computing IoU/mIoU and boundary-F for masks, and SAD/MSE/Grad/Conn in the trimap unknown band for matting, reported per-class and at edges. Distinguishes globally-similar-but-edge-wrong outputs (low mean error but high max_abs at thin structures). Triggers: evaluate segmentation, matting metrics, IoU / boundary F, SAD MSE Grad Conn, per-class accuracy, compare checkpoints, is this mask good, alpha matte quality.'
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Evaluating Segmentation Models

Judge a mask/alpha model on **metrics that reflect perceived quality**, not a single average that hides
edge failures. Covers hard segmentation and soft matting, and the parity check that a converted or
quantized model still passes.

## When to use
- Sign-off on a trained segmentation / matting checkpoint.
- A/B two checkpoints, or before-vs-after a conversion/quantization step.
- Deciding whether a model is "good enough" to export or ship.

## Metrics (pick by task — see `references/metrics.md` for formulas)
- **Hard segmentation:** per-class **IoU** + **mIoU**; pixel accuracy (report but don't rely on it under
  class imbalance); **boundary-F** (F-score of boundary pixels within a tolerance) — the metric that
  actually tracks edge quality.
- **Image matting (soft alpha):** the four standard metrics **SAD, MSE, Grad, Conn**, computed in the
  **trimap unknown band** (the contested region) as well as whole-image; plus **binary IoU** of the
  thresholded alpha for a coarse sanity check.

## How to evaluate
1. **Per-class / per-region, not one number.** A single mIoU hides a collapsed rare class; a whole-image
   SAD hides bad hair/edges. Always break down by class and by the boundary/unknown band.
2. **Edge-vs-global diagnostic.** If mean error is low but **`max_abs` is near 1.0 at sparse
   edge/thin-structure pixels**, the model is globally close but locally wrong — a classic colour-order
   or missed-stem symptom (see `converting-pytorch-to-tflite`), not a real pass.
3. **Parity of the metric across host↔device.** When evaluating a converted/quantized model, judge
   consistency in **decision space** (thresholded mask / argmax / IoU), not raw logits or raw alpha —
   reduced precision moves logits harmlessly but must not move the decision. (Hand device sign-off to
   `validating-on-device-inference`.)
4. **Sample selection for the report.** Collect **all** failure cases; sample the correct ones. Feed the
   numbers + galleries to `rendering-html-eval-reports` — this skill decides *what* to measure, that one
   *renders* it.

## Acceptance
- State an explicit threshold per metric (e.g. mIoU ≥ X, boundary-F ≥ Y, matting SAD ≤ Z in the unknown
  band) **before** looking at results; a metric without a pre-set bar is a description, not a gate.
- A pass needs the per-class/boundary breakdown to clear the bar — not just the average.

## Boundaries
- Read/measure only: emits PASS/FAIL rows + numbers; it does not train or tune.
- Class set, thresholds, trimap source, and dataset are caller inputs — keep zero project values in any
  eval you run. Rendering → `rendering-html-eval-reports`; on-device sign-off → `validating-on-device-inference`.
