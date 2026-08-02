---
name: quantizing-on-device-models
description: 'Quantize a model for on-device (mobile / NPU) deployment and verify it still meets quality — choose fp16 vs int8 (dynamic-range PTQ, full-int8 PTQ with a representative dataset, or QAT), pick per-channel weights and input symmetry, decide which layers stay float, and gate on an accuracy-vs-latency budget. Use when a fp16 model is too slow or large on device, when planning an INT8 conversion, when choosing a calibration set, or when a quantized model''s accuracy regresses. Verifies parity in decision space (argmax / IoU), not raw logits. Triggers: quantize model, int8 / PTQ / QAT, representative dataset, calibration set, per-channel quantization, accuracy drop after quant, fp16 vs int8, shrink model for mobile.'
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Quantizing On-Device Models

Make a model small/fast enough for a phone or NPU **without** silently losing accuracy. Quantization is
a ladder — climb only as far as the latency/size budget forces, and re-verify quality at each rung.

## When to use
- An fp16 model misses the latency or size budget on the target device.
- Planning INT8 conversion and unsure PTG vs QAT / which calibration set.
- A quantized model regressed and you need to localize the loss.

## The ladder (climb only as needed)
1. **fp16** — half-precision weights, float compute. Near-lossless (~1e-4 parity), smallest risk. The
   default; ship it unless the budget forces more. (Export details: `converting-pytorch-to-tflite`.)
2. **int8 dynamic-range (weights-only) PTQ** — int8 weights, float activations quantized on the fly. No
   calibration data needed; good speed/accuracy balance; a solid first int8 step.
3. **full-int8 PTQ** — weights **and** activations int8, needs a **representative dataset** to calibrate
   activation ranges. Fastest on int8-only NPUs; most accuracy risk.
4. **QAT (quantization-aware training)** — simulate quantization during fine-tuning. Highest cost, best
   int8 accuracy; reach for it only when full-int8 PTQ loses too much.

## Decisions that matter
- **Per-channel weights** almost always beat per-tensor (per-channel weight scales, per-tensor
  activation) — prefer it when the converter/NPU supports it.
- **Asymmetric input quantization** often helps for image inputs (0..255 is one-sided).
- **Keep sensitive layers in float** — the first/last layer, attention softmax, and normalization are
  common accuracy sinks; a mixed-precision graph (most int8, a few float) can recover most of the loss.
- **NPU op coverage** — confirm the target runtime supports the quantized ops (tie in
  `gating-tflite-op-envelopes`); an unsupported op falls back to CPU and erases the speedup.

## Calibration set (for full-int8)
Use real inputs that **cover the deployment distribution** (lighting, subjects, edge cases) — not a
handful of clean images. A few hundred representative samples usually suffice; an unrepresentative set
clips activation ranges and tanks accuracy on the tail.

## Verify after every rung
- Judge parity in **decision space** — thresholded mask / argmax / IoU / task metric — **not raw
  logits or raw alpha**. Reduced precision moves logits harmlessly; it must not move the decision.
- Re-run `evaluating-segmentation-models` (per-class + boundary/unknown band) and record the
  **accuracy-vs-latency** point. Hand the on-device latency + numerical sign-off to
  `validating-on-device-inference`.
- Gate: state the max acceptable accuracy drop **and** the latency target up front; a rung passes only
  if it clears both.

## Boundaries
- Planning + verification discipline: you drive the actual quantizing converter/trainer; this does not
  vendor one. Layer choices, calibration data, and budgets are caller inputs — keep zero project values
  in any eval you run.
