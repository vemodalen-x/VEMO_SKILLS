# Segmentation & matting metrics — formulas

Reference for `evaluating-segmentation-models`. Generic; the class set, thresholds, and trimap source
are caller inputs.

## Hard segmentation
- **IoU (per class c):** `IoU_c = TP_c / (TP_c + FP_c + FN_c)` on the argmax prediction vs ground truth.
- **mIoU:** mean of `IoU_c` over classes. Report per-class too — the mean hides a collapsed rare class.
- **Pixel accuracy:** `correct_px / total_px`. Report but distrust under class imbalance (a background-
  heavy image scores high while missing the object).
- **Boundary-F:** extract boundary pixels of pred and GT (morphological gradient), match within a pixel
  tolerance `θ` (often 0.5–2% of the image diagonal), compute precision/recall of boundary pixels →
  `F = 2PR/(P+R)`. This is the metric that tracks edge crispness.

## Image matting (soft alpha in [0,1])
Compute over the **unknown band** of the trimap (where `0 < trimap < 1`) and, separately, whole-image.
Let `α` = predicted alpha, `α*` = ground-truth alpha, `N` = pixel count in the region.
- **SAD (Sum of Absolute Differences):** `Σ |α − α*|` (often reported ÷1000).
- **MSE (Mean Squared Error):** `(1/N) Σ (α − α*)²`.
- **Grad (Gradient error):** `Σ | ∇(g*α) − ∇(g*α*) |` where `g` is a Gaussian derivative — penalizes
  over-smoothed / jagged edges.
- **Conn (Connectivity error):** penalizes fragmented alpha vs a connected GT region.
- **Binary IoU:** threshold `α` at 0.5 and compute IoU — a coarse sanity check, not a substitute.

## Reporting discipline
- Break every metric down **per class** (seg) or by **unknown-band vs whole-image** (matting).
- Pair the average with a **tail** statistic (`max_abs`, worst-K images): low mean + high tail = globally
  close, locally wrong.
- Fix the eval set, preprocessing, and thresholds up front; changing them after seeing results is
  metric-shopping. Record data version + model id with the numbers.
