# TFLite export — colour fold, multi-stem, deploy, parity

Reference for `converting-pytorch-to-tflite`. Generic methodology; substitute your own model
names, converter tool, and colour matrix.

## Colour-fold algebra
A per-pixel linear colour transform is a 3×3 matrix `C` applied to the channel vector. A conv's first
layer computes `W * x`. Because `C` is linear and acts per-pixel on channels, it commutes with the
spatial conv: `W * (C·x) == (W·C) * x`. Pre-multiplying `W` by `C` therefore bakes the colour
conversion into the weights, and the exported model accepts the raw camera channels.

Two composable folds:
- **Channel reorder** (e.g. RGB→BGR): permute the input-channel axis of the weight,
  `W[:, [2,1,0], :, :]`. Only reorder the colour channels; leave auxiliary channels (e.g. a trimap 4th
  channel) in place.
- **Colour matrix** (e.g. RGB→YUV): contract the matrix into the input-channel axis,
  `einsum("oihw,ji->ojhw", W, M)` (index names illustrative).

**Order matters.** A packaged RGB↔YUV matrix is derived for a specific *output* channel order. If it
reconstructs BGR but your checkpoint trained on RGB, apply the RGB→BGR reorder **first**, then the
matrix — the reorder cancels the matrix's BGR assumption so `W'·yuv == W·rgb`. Always confirm with a
numeric check, not just by reading code.

Standard BT.601 RGB→YUV (full-range, inputs 0..255) for reference:
```
[[ 0.299,   0.587,   0.114  ],
 [-0.168736,-0.331264, 0.5   ],
 [ 0.5,    -0.418688,-0.081312]]
```
Know whether your pipeline expects Y,U,V or a different packing, and whether values are 0..1 or 0..255.

## Per-arch input-conv checklist
Fold **every** conv that receives the raw image:
- Single-stem CNNs: one input conv (the stem / `conv_stem` / `feature.0`).
- **Dual/multi-stem** backbones: a stem branch **and** an encoder stem (two keys) — fold both.
- Transformer-hybrid backbones: check whether a patch-embed conv also sees the raw input.
- **Fallback** when the arch is unknown: fold every 4-D weight whose `shape[1] == in_channels`.

Symptom of a missed stem or wrong order: **low mean error, high `max_abs` at edges/thin structures**.

## Deploy / reparameterize before tracing
Reparameterizable (fused-conv, structural-reparam) backbones only collapse their multi-branch training
blocks into single convs when switched to deploy mode. Set the flag on the wrapper **and** the nested
inner model, then `.eval()`, before tracing/exporting — otherwise you export the training-time graph.

## fp16 vs int8-hybrid (decision, not a specific tool's kwargs)
- **fp16 first.** Half-precision weights, float activations. Near-lossless (~1e-4 parity), smallest
  behavioural risk. Ship this unless latency/size forces more.
- **int8-hybrid** when you need speed: quantize weights to int8, keep activations float (dynamic-range)
  or use a representative dataset for full-int8. Prefer **per-channel** weights; for hybrid, asymmetric
  input quantization often helps. Enable the target NPU's op set if the converter exposes it.
- Full int8 / QAT is a bigger step — see `quantizing-on-device-models`.

## Parity gate
Run identical preprocessing through PyTorch (training colour) and TFLite (device colour) on a sample of
real images. Report `mae`, `rmse`, `max_abs`, and a task metric (`binary_iou` for masks). Treat
`mae ≈ 1e-4` as an fp16-rounding pass; investigate anything larger before shipping. Wire optional
`--max-mae` / `--min-iou` thresholds so the export is self-checking.
