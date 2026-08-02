---
name: loading-model-checkpoints
description: 'Load a PyTorch checkpoint into a model robustly when the state_dict nesting, key prefixes (model./module.), architecture, or input-channel count are uncertain. Use when a checkpoint silently loads onto random weights, load_state_dict reports missing/unexpected keys, a checkpoint comes from a different trainer (Lightning / DataParallel / raw torch), or you must infer the architecture and input channels before building the model. Picks the prefix variant by maximum key-overlap, prints missing/unexpected diagnostics, and flags the weights_only security caveat. Triggers: load a checkpoint, state_dict mismatch, missing/unexpected keys, strip module. prefix, wrong weights loaded, ckpt onto random weights.'
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Loading Model Checkpoints

Load weights so a mismatch is **loud, not silent**. Naive `load_state_dict` on a checkpoint from a
different trainer leaves the model on random weights (silent `missing_keys`) and every downstream
export/eval is garbage. This skill is a robust load recipe.

## When to use
- A checkpoint may be the raw `state_dict` or wrapped (`state_dict` / `model` / `module` / trainer keys).
- Keys carry a `model.` or `module.` prefix that may or may not match your built model.
- You must infer the architecture / input-channel count from the checkpoint before instantiating.
- Outputs look random or degraded and you suspect a load mismatch.

## Step 1 — unwrap the nested state_dict
Walk common wrapper keys until you reach the real tensors, then loop-strip `model.` / `module.`
prefixes until stable:
```python
state = checkpoint
for key in ("state_dict", "model_params", "model"):
    cand = state.get(key) if isinstance(state, dict) else None
    if isinstance(cand, dict):
        state = cand
```

## Step 2 — pick the prefix variant by MAX key-overlap (the trick)
Do **not** assume which prefix to strip. Build several candidate remappings and keep whichever overlaps
the built model's keys the most:
```python
model_keys = set(model.state_dict().keys())
candidates = {
    "as-is":        raw,
    "strip-model":  {k[6:] if k.startswith("model.")  else k: v for k, v in raw.items()},
    "strip-module": {k[7:] if k.startswith("module.") else k: v for k, v in raw.items()},
    "add-model":    {("model." + k): v for k, v in raw.items()},
}
tag, state = max(candidates.items(), key=lambda kv: len(set(kv[1]) & model_keys))
```

## Step 3 — load non-strict and PRINT diagnostics
```python
result = model.load_state_dict(state, strict=False)
missing = [k for k in result.missing_keys if "num_batches_tracked" not in k]
print(f"prefix={tag} missing={len(missing)} unexpected={len(result.unexpected_keys)}")
```
`num_batches_tracked` mismatches are benign — filter them so a clean load reads `missing=0 unexpected=0`.
**Non-trivial missing/unexpected → the arch or prefix is wrong. Fix before trusting any output.**

## Step 4 — infer architecture & input channels
- **Architecture:** prefer a `model_name` stored in the checkpoint; else infer from the filename; else
  a sane default. Never guess silently — log what you picked.
- **Input channels:** read `shape[1]` of the first 4-D conv weight (e.g. 3 / 4 / 6). A >3-channel model
  usually expects an auxiliary input (trimap, prior mask) and may need an upstream stage to produce it.
- **Tolerant constructor:** different codebases name the kwarg differently (`in_channels` vs `inchannel`).
  Try a small cascade and accept the first that constructs:
```python
for kwargs in (dict(num_classes=1, in_channels=in_ch), dict(num_classes=1, inchannel=in_ch),
               dict(num_classes=1), dict()):
    try: model = cls(**kwargs); break
    except TypeError: continue
```

## Security caveat — `weights_only`
`torch.load(..., weights_only=True)` loads pure tensors and is the safe default. `weights_only=False`
can **execute arbitrary code** during unpickling — use it only for checkpoints you fully trust (e.g. to
read stored non-tensor metadata like `model_name`), never for third-party/untrusted files.

## Boundaries
- Read/instantiate only: reports the load verdict; it does not train, fine-tune, or rewrite checkpoints.
- Architecture registry, kwarg names, and file layout are caller inputs — keep zero project values in any
  diagnostic you run. Downstream: `converting-pytorch-to-tflite`, `evaluating-segmentation-models`.
