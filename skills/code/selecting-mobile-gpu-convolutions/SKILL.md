---
name: selecting-mobile-gpu-convolutions
category: code
description: Decide between standard and separable (depthwise+pointwise) convolutions for mobile-GPU (OpenCL / TFLite delegate) deployment using three measured heuristics — first-frame time tracks OpenCL kernel count (not FLOPs), warmup gain tracks arithmetic intensity, steady-state time tracks FLOPs ÷ GPU utilization. Use at model-design time to narrow conv choices and on-device to confirm. Read-only advisory — heuristics from one denoising project; verify on the target runtime. Reversal conditions (large channels / kernel fusion) apply.
---

# Selecting Mobile-GPU Convolutions

Choose between **standard** and **separable (depthwise + pointwise)** convolutions for **mobile-GPU** inference
(OpenCL / TFLite GPU delegate), using three measured heuristics about what actually drives on-device latency. This is
**read-only advisory** — it dispenses decision rules; it does not edit models or code.

> **Heuristics, not laws.** The three rules below are derived from **one** foreign denoising project, **two** models,
> **one** mobile GPU / runtime 〔实测·张帆·dn_bayer_71 (standard conv) vs PMRIDv10 (separable)〕. They are a
> **design-time heuristic to narrow choices**, NOT a guarantee for your model / GPU / runtime. **The portable part is
> the proportionality; every concrete number is evidence, not fact** — each carries its source tag. **Always confirm on
> the target device** (see Checklist). Reversal conditions (large channels / kernel fusion) can flip the conclusion —
> see *When this holds*.

## When to use
- Choosing a conv structure (standard vs depthwise-separable) for a model that will run on a mobile GPU.
- Explaining why a lower-FLOPs model is slower on-device, or why warmup helps one model but not another.
- Trigger phrases: "标准卷积还是可分离卷积", "mobile GPU conv selection", "为什么 FLOPs 更少反而更慢",
  "depthwise 在 GPU 上慢", "选卷积结构 端侧".

## The three rules (generic proportionality + tagged evidence)

### R1 — First-frame time ∝ OpenCL kernel count (NOT FLOPs)
OpenCL kernels are JIT-compiled on first execution, so first-frame cost tracks **how many kernels** compile.
A separable conv splits each layer into **DW + PW = 2 kernels** (unless the runtime fuses them), roughly doubling the
first-frame compile overhead.
- 〔实测·张帆·去噪项目〕standard conv (dn_bayer_71) ~18 kernels / **150 ms** first-frame (1,164M FLOPs) vs separable
  (PMRIDv10) ~35 kernels / **176 ms** (830M FLOPs). **Fewer FLOPs, yet slower first-frame** — kernel count, not FLOPs.

### R2 — Warmup gain ∝ arithmetic intensity
How much a model speeds up after warmup tracks whether its dominant layers are **compute-bound** (high arithmetic
intensity → caching weights + running the shader hot pays off) or **memory-bound** (low AI, e.g. depthwise → the
bottleneck is bandwidth, which warmup cannot fix).
- 〔实测·张帆·去噪项目〕standard-conv main layers AI > 17.5 → warmup **−41%**; depthwise AI ≈ 4.5 → only **−19%**.

### R3 — Steady-state time ∝ FLOPs ÷ GPU utilization (equivalent compute) — stronger predictor than FLOPs
Raw FLOPs predict steady-state latency poorly; **FLOPs ÷ GPU-utilization** ("equivalent compute") predicts it better,
because a structure that keeps the GPU busy does more useful work per FLOP.
- 〔实测·张帆·去噪项目〕dn_bayer_71 has **1.4×** the FLOPs of PMRIDv10 (1,164M vs 830M) yet runs **1.6× faster** in
  steady state (**89 ms vs 142 ms**). Equivalent compute: 1,164M / ~30% util = 3,880M vs 830M / ~10% util = 8,300M.
- **Honesty (source caveat)**: the measured 142/89 ≈ 1.60× is only **direction-consistent** with the
  equivalent-compute ratio 8,300/3,880 ≈ 2.1× — "the difference comes from PMRIDv10's full-resolution standard-conv
  layer's compensating contribution." Treat equivalent compute as a **direction indicator, not an exact multiplier**.

### Bottom line
On a mobile GPU at **small channel widths (≤12ch)**, a standard conv can execute **more efficiently** than a separable
one despite higher FLOPs (it keeps the GPU more utilized). **FLOPs is a design-time reference; arithmetic intensity is
the on-device cost predictor.**

## When this holds (applicability) — read before trusting
- **Holds**: small-channel (≤12ch) mobile-GPU (OpenCL / TFLite GPU delegate) inference, **no kernel fusion**. There,
  standard conv often out-executes separable despite more FLOPs.
- **Can REVERSE**: large channel counts; a runtime that **fuses DW+PW into one kernel** (removes R1's 2× kernel
  penalty); or memory-bandwidth-rich hardware — the separable advantage may return. **Do not apply the conclusion
  blindly.**

## Checklist
### Design-time — narrow choices with the heuristic
- [ ] Count OpenCL kernels per layer (separable = 2× unless fused) → estimate first-frame cost (R1).
- [ ] Estimate arithmetic intensity of the dominant layers → predict warmup benefit (R2).
- [ ] Compute FLOPs ÷ expected GPU utilization (equivalent compute), not raw FLOPs → rank steady-state (R3).
- [ ] Check channel width / fusion against *When this holds* — flag if in a reversal regime.

### On-device — confirm before trusting (mandatory for a thin-evidence heuristic)
- [ ] Measure **first-frame**, **post-warmup**, and **steady-state** separately on the target GPU / runtime.
- [ ] If the measured ranking contradicts the heuristic → **trust the measurement**; the heuristic only narrowed the search.

## Notes
- **Read-only advisory** — dispenses decision rules; does not edit models or code.
- **Boundary vs `optimizing-cpp-performance`**: that skill optimizes **C++ hot-path code** on the **CPU** (ARM NEON
  SIMD / cache / multithread); **this** skill chooses **model-architecture convolutions** for the **GPU** (OpenCL /
  TFLite delegate) at design / deploy time. Different compute target, different artifact — "optimize an already-chosen
  C++ hot path → `optimizing-cpp-performance`; decide standard vs separable conv → here."
- **Decoupling (skill_spec §9)**: the numbers are a foreign project's measured **evidence**, not facts about any
  consuming project; this body carries **zero hardcoded project / identity values**. The target runtime, GPU, and
  channel widths are confirmed by the consuming project at runtime — this body assumes none of them.
