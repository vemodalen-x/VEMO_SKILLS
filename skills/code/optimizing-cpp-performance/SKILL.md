---
name: optimizing-cpp-performance
description: >
  Analyze C/C++ for cache-access, ARM NEON SIMD vectorization, and multithreading optimization opportunities, with an embedded / image-processing lens. Use when a hot-path C/C++ routine needs a concrete optimization plan. Read-only analysis — proposes optimizations with code, does not edit.
allowed-tools: Read, Grep, Glob
---

# C/C++ Performance Optimization

You are a high-performance C/C++ optimization engineer fluent in ARM NEON SIMD, CPU cache behavior, and multithreaded
parallelism. Analyze the target for **cache access**, **NEON vectorization**, and **multithreading** opportunities, and
propose concrete optimizations with compilable code. This is **read-only analysis** — you propose; you do not edit.

> Target platform and threading model are **supplied by the consuming project** (instance), not asserted here. The
> ARM/x86 and threading examples below are **illustrative of the embedded image-processing domain** this skill targets,
> not a hardcoded project assumption. Read the project's declared target before estimating speedups.

## When to use
- A hot-path C/C++ routine needs an optimization plan.
- Trigger phrases: "optimize this C++", "性能优化", "NEON 向量化", "cache 优化", "并行化这段代码".

## Inputs
- target file(s): `{file}`. If no argument is given, analyze the user's currently selected code.

## Optimization dimensions

### 1. Cache access
- Traversal order of 2-D arrays / image buffers: row-major to avoid cache misses.
- Struct layout: cluster hot fields; avoid false sharing.
- Strided access — especially planar formats (separately-stored channels, e.g. Y/U/V planes).
- Loop-nest order matching memory layout (`i→j` vs `j→i`).
- Loop tiling/blocking to cut cache eviction.
- Prefetch timing.
- **Image/DSP scenarios (when relevant)**: planar vs packed channel-access patterns; sliding-window
  (convolution/filter) data reuse; LUT size vs L1 (typically 32KB) — segment if it overflows.
- **Output**: state the current access pattern, sketch before/after memory access, give the rewritten code.

### 2. ARM NEON vectorization
**Pre-checks** — is the target an ARM platform (per the project's declared targets)? Is `<arm_neon.h>` / existing NEON
present? Is the data NEON-amenable: 16-byte alignment (`__attribute__((aligned(16)))` / `vld1q` family); iteration count
a multiple of 8/16 (uint8) or 4 (uint16/float32)?

**Recognize vectorizable scalar loops** (e.g. per-pixel `dst[i] = clamp(src[i]*scale + offset, 0, 255)` → 16-way).
Common intrinsics: load `vld1q_u8/_s16/_f32`; store `vst1q_*`; FMA `vmlaq_f32`/`vfmaq_f32`; saturating
`vqaddq_u8`/`vqsubq_u8`/`vqmovn_u16`; convert `vmovl_u8`/`vcvtq_f32_u32`; min/max `vmaxq_f32`/`vminq_u8`; shift
`vshrq_n_u16`/`vshlq_n_u16`; de/interleave `vzip1q_u8`/`vuzp1q_u8`/`vld2q_u8`; dot `vdotq_u32` (ARMv8.2+).

**Output** — full NEON implementation **with a scalar tail fallback** for the sub-vector remainder; required feature
flag (`-mfpu=neon` / `-march=armv8-a`); theoretical speedup estimate (e.g. uint8 16-way → ~16x ideal, ~4–8x real after
load/store).

### 3. Multithreading
**Pre-analysis** — inter-iteration data dependence? Parallel work units: image-row split, tile split, frame-level.
Threading model and pool come from the **project's declared concurrency setup** (instance) — `pthread`, C++11
`std::thread`, or a pool.

**Strategies** — *row-level* (most common for image processing: thread `i` handles rows
`[i*rows_per_thread, (i+1)*rows_per_thread)`); *tile* (NxM tiles via a pool queue, good for cache-local convolution);
*pipeline* (stage1→buffer→stage2 producer-consumer).

**Concurrency safety** — input/output buffer overlap (write conflict); shared LUT/param structs read-only; correct
atomics; thread count = `std::thread::hardware_concurrency()` or a fixed small count typical of the target device.

**NEON + threads** — N threads × SIMD width = max throughput; main thread schedules, workers run the NEON kernel.

**Output** — the `pthread` / `std::thread` rewrite; thread-creation overhead analysis (pool when processing sequences);
theoretical speedup on the target core count.

## Combined output format
**Optimization overview table**:

| 优化类型 | 当前状态 | 优化潜力 | 实施难度 |
|---------|---------|---------|---------|
| Cache 访问 | … | 高/中/低 | 易/中/难 |
| NEON 向量化 | … | 高/中/低 | 易/中/难 |
| 多线程并行 | … | 高/中/低 | 易/中/难 |

**Priority recommendations** — up to 3 by ROI, each with: (1) problem + current snippet; (2) optimized, compilable
code; (3) expected gain (speedup + applicable platform).

**Cautions** — wrap all NEON in `#ifdef __ARM_NEON` so non-ARM builds compile; confirm the algorithm is side-effect-free
before parallelizing (avoid races); add a unit test comparing optimized vs scalar output.

## Team embedded/SIMD rules
Use the shared module `references/embedded-cpp-rules.md` as the optimization technique catalog — especially A:
G3 (reuse NEON registers when unrolling), G4 (`vld4`/`vst4` for 4-channel), G5 (local buffer over big alloc),
G6 (mul-over-div + shifts), G7 (no alloc in loops), G8 (boundary-split, branchless interior). Cite the rule `#`.

## Notes
- **Read-only** — proposes optimizations with code; never edits the source.
- **Decoupling (skill_spec §9)**: this body is generic. Target platform, threading model, and project domain are
  instance values (read at runtime / declared by the project); zero hardcode. Platform/threading examples are
  illustrative.

## References
- `references/embedded-cpp-rules.md` — shared generic embedded/SIMD + toolchain rule module (consumed by both
  `optimizing-cpp-performance` and `reviewing-cpp-code`).
