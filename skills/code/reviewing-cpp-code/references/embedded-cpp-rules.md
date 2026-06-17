# Embedded / SIMD C++ Coding Rules (generic module)

> Generic reference module for the `code/` category. **Both** `reviewing-cpp-code` and `optimizing-cpp-performance` carry an
> **identical copy** under their own `references/`: the per-skill regen model copies `references/` only from inside a
> skill folder, so a category-level shared file would not survive regen — each skill owns a byte-identical copy. **Keep
> the two copies in parity on any edit.**
> A curated checklist for embedded / DSP / image C++ on ARM-class targets. Zero project hardcodes — where a rule once
> named a project's toolchain (VCS, NDK), it is **genericized** here and the concrete toolchain is supplied by the
> consuming project (instance), not asserted in this module.
>
> **Public provenance**: this is an original checklist curated for the skill hub. It carries no private contributor
> names, project ids, or account identifiers.

The rules below split into **(A) generic embedded/SIMD rules** — portable to any embedded C++ target — and
**(B) toolchain/process rules** — genericized so the concrete tool (VCS, NDK ABI) is an instance value, never hardcoded.

---

## A. Generic embedded / SIMD rules

| # | rule | rationale | scope |
|---|------|-----------|------|
| G1 | **Avoid `while` / `goto`; prefer `for`.** Use `for` as the single loop idiom so bounds + step are visible at the loop head. | readability, fewer infinite-loop/fall-through bugs | generic |
| G2 | **Single exit point, and the function must `return`.** Avoid scattered early-returns; converge to one exit (a `return` at the end). | predictable cleanup, easier resource/exception reasoning | generic |
| G3 | **Reuse NEON registers when unrolling loops.** When unrolling a SIMD loop, reuse vector registers across iterations rather than allocating fresh ones each pass. | reduces register pressure / spills | generic |
| G4 | **Use `vld4`/`vst4` for 4-channel interleaved data (and `vld3`/`vst3` for 3-channel).** Match the de/interleave intrinsic to the channel count instead of manual gather/scatter. | hardware de-interleave is far cheaper than scalar shuffling | generic |
| G5 | **Prefer a local buffer over large image-sized allocations.** Process in tiles/strips through a small local buffer rather than allocating a whole-image scratch. | cache locality + lower peak memory | generic |
| G6 | **Multiply instead of divide; shift instead of multiply/divide by powers of two.** Replace `/ k` hot-path divides with reciprocal-multiply; replace `* 2^n` / `/ 2^n` with `<<` / `>>`. | divide is many cycles; shifts are 1 | generic |
| G7 | **No memory allocation inside loops.** Hoist all allocation out of hot loops (and ideally out of the per-frame path entirely). | allocator calls in a loop kill throughput + risk fragmentation | generic |
| G8 | **Handle boundaries separately; keep the center region branch-free.** Peel boundary rows/cols into their own code; the interior loop does no boundary test. | the hot interior loop stays branchless / vectorizable | generic |
| G9 | **Add elapsed-time instrumentation to new functions.** Newly added functions (especially hot-path) should carry timing instrumentation so regressions are measurable. | makes perf regressions visible, not silent | generic |

## B. Toolchain / process rules (genericized — concrete tool is an instance value)

| # | rule (generic form) | instance binding | scope |
|---|---------------------|-------------------------------|------|
| T1 | **Stay within the target toolchain's portable ABI; isolate platform-specific functions behind `#ifdef`.** Do not call functions unique to one compiler if another target toolchain must also compile the code; gate platform-only code with a platform macro (e.g. `#ifdef _WIN32`). | The consuming project supplies the actual compiler, ABI, and platform macro set. | generic |
| T2 | **Before committing, update from the VCS and keep the diff minimal.** Sync your working copy (pull/update) before commit and keep changes scoped/minimal. | The consuming project supplies the actual VCS and update command. | generic |

> **Instance binding for B**: the consuming project declares its actual target toolchain set and VCS (e.g. in its
> instance / project_profile). This module states the *discipline*; concrete compiler, ABI, and VCS names stay in the
> consumer instance, not in this generic module.

---

## How the two skills consume this
- `reviewing-cpp-code` checks code **against** A + B as review findings (flag violations, cite the rule #).
- `optimizing-cpp-performance` uses A (esp. G3–G8) as the **optimization technique catalog** when proposing rewrites.
- Both cite a rule by its `#` (G1…G9 / T1–T2) so findings are traceable to the checklist entry.
