---
name: converting-pytorch-to-tflite
category: code
description: Convert a trained PyTorch (or ONNX) model into a numerically faithful mobile TFLite — fp16 or int8-hybrid — and fold the camera colour transform into the first conv so the on-device model consumes the raw camera format (YUV/BGR) directly. Use when exporting a checkpoint to TFLite for on-device deployment, when a converted model's output drifts from the PyTorch reference, or when the runtime colour space differs from the training colour space. Covers reparameterize/deploy-before-trace, multi-stem colour folding, and a PyTorch-vs-TFLite parity gate. Triggers: export to tflite, pytorch/onnx to tflite, convert model for mobile, tflite output mismatch, YUV/BGR colour fold, fp16 vs int8 export.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Converting PyTorch to TFLite

Export a trained checkpoint to a mobile TFLite whose output is **numerically identical** to the
PyTorch reference (within fp16 rounding), and whose input is the **raw camera colour format** so no
per-frame colour conversion is needed on-device. This is a **methodology + gotcha** skill; you drive
the repo's converter (e.g. a TinyNN / onnx2tf / ai-edge-torch based exporter), it does not ship one.

## When to use
- Exporting a PyTorch/ONNX checkpoint to `.tflite` for phone/NPU deployment.
- A converted model looks "close on average" but wrong at edges/thin structures.
- The device delivers YUV or BGR but the model was trained in a different colour space.

## The pipeline
1. **Load the checkpoint robustly** (see `loading-model-checkpoints`): unwrap nesting, match the
   prefix by key-overlap, confirm `missing=0 unexpected=0`, read input channels from the first conv.
2. **Set deploy / reparameterize mode BEFORE tracing** (gotcha 3).
3. **Fold the colour transform into the first conv weight(s)** (gotcha 1 & 2) if the device colour
   space differs from training — so the exported graph eats raw camera data.
4. **Convert** to TFLite: start with **fp16** (safest, ~1e-4 parity); move to **int8-hybrid** only
   when latency requires it (see `quantizing-on-device-models`).
5. **Parity-gate** the result against PyTorch on real images before trusting it (see below).

## Gotcha 1 — fold colour conversion into the first conv (don't convert at runtime)
A linear colour transform `C` (3×3) **commutes** with a convolution: `W·(C·x) == (W·C)·x`. So instead
of converting the camera frame to the training colour space every frame, **pre-multiply the first
conv's weights by `C`** and the exported model consumes the raw format directly.

- **Know your matrix's channel-order convention.** An RGB↔YUV matrix is often derived for a specific
  output order (e.g. it reconstructs BGR, not RGB). If your checkpoint was trained in the *other*
  order, apply the channel-reorder **first**, then the colour matrix, so the two cancel correctly.
- For a multi-channel model (e.g. RGB+trimap), fold only the colour channels; leave auxiliary
  channels untouched.
- Verify the fold **algebraically and numerically** — a correct fold gives parity ≈ 1e-4 (fp16).

## Gotcha 2 — multi-stem architectures have MORE THAN ONE input conv
Some backbones feed the raw input into two places (a stem branch **and** an encoder stem). If you fold
the colour transform into only one, the other still expects the original colour space. The tell-tale
symptom: **low mean error but high `max_abs` at edges** (globally similar, locally wrong). Fold **every**
input conv. Identify them by a known per-arch map; fallback: fold every 4-D weight whose
`shape[1] == in_channels`.

## Gotcha 3 — set deploy mode before tracing (reparameterizable models)
Fused-conv / reparameterizable backbones collapse branches only when switched to deploy mode. Wrappers
often nest the real net under an attribute, so set the flag on **both** the wrapper and the inner model
before you trace/export, or the exported graph is the un-fused training graph.

```python
if hasattr(model, "deploy"): model.deploy = True
inner = getattr(model, "model", None)
if inner is not None and hasattr(inner, "deploy"): inner.deploy = True
model.eval()
```

## Parity gate (always run after export)
Run the **same** preprocessing through PyTorch (training colour) and TFLite (device colour) on a sample
of real images; report `mae / rmse / max_abs` and a task metric (e.g. `binary_iou` for masks). Gate:
- `mae ≈ 1e-4` → pass (fp16 rounding).
- larger `mae`, or `max_abs` near 1.0 at sparse pixels → **investigate** (usually a colour-order or
  missed-stem bug), do not ship.

See `references/export-gotchas.md` for the colour-fold algebra, a per-arch input-conv checklist, and
fp16-vs-int8 converter-flag notes.

## Boundaries
- Methodology + parity discipline only: you drive the actual converter tool; this does not vendor one.
- The **static** runtime-envelope check is `gating-tflite-op-envelopes`; the **on-device** numerical +
  latency sign-off is `validating-on-device-inference`; **quantization** decisions are
  `quantizing-on-device-models`. This skill owns the **export + numerical-parity** step between them.
- All model names/paths/colour matrices are caller inputs — keep zero project values in any eval you run.
