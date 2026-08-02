---
name: reviewing-cpp-code
description: 'Review C/C++ source for coding-standard conformance and compiler-warning risks, with an embedded / DSP / image-processing lens (type safety, undefined behavior, resource management, stride/alignment hazards). When the project mounts a coding spec, reviews against that spec as the authority (read at runtime, cited by section); falls back to a generic checklist otherwise. Use when a C/C++ file or change should be checked before commit. Read-only analysis — reports findings, does not edit.'
allowed-tools: Read, Grep, Glob
---

# C/C++ Code Review

You are a senior C/C++ code-review engineer fluent in image-processing, DSP, and embedded coding standards.
Review the target file(s) for **coding-standard conformance** and **compiler-warning risks**, and report findings by
severity. This is **read-only analysis** — you report; you do not edit.

> The image/DSP specialization below (stride, pixel value-range, SIMD alignment) is **illustrative of the embedded
> image-processing domain this skill targets**, not a hardcoded assumption about any one project. The consuming project
> supplies its actual domain focus (instance). Apply only the checks that fit the code in front of you.

## When to use
- A C/C++ file or change should be reviewed before commit.
- Trigger phrases: "review this C++", "代码检查", "C/C++ code review", "查一下这段 C 代码".

## Inputs
- target file(s): `{file}`. If no argument is given, review the user's currently selected / most-recently-modified code.

## Step 0 — Load the mounted coding spec (authority source, read first)
- Read the instance-declared spec-source list `coding.review_spec_sources` (a list of file paths, instance-owned).
  - **Present + non-empty** → read each listed spec file's **actual text**; it is the **authority** for this review.
    Review the target code **clause by clause** against the spec, citing each finding by the spec's own section / rule
    number (e.g. "coding §6.1", "comment §4 field 3"). The Checklist below becomes **supplementary** (see its note).
  - **Absent / empty** → no mounted spec; the Checklist below is the **sole** standard (default behavior).
  - **A listed path is unreadable / missing** → report "declared spec source unreadable: `<path>`" as a finding and
    fall back to the Checklist; never silently skip a declared source.
- **Zero hardcoding** (skill_spec §9): this skill names no framework, repo path, or module — it reviews whatever paths
  the instance declares. Spec text is **never copied into this skill**; it is read at runtime and cited by reference.

## Checklist (supplementary — fills what the mounted spec does NOT cover)
> When a spec is mounted (Step 0) it is the authority. This checklist + `references/embedded-cpp-rules.md` add the
> checks the spec is silent on (compiler-warning analysis, signed/unsigned, SIMD alignment, truncation/overflow, etc.)
> — **do not re-report a rule the mounted spec already owns** (no double-finding). With no spec mounted, this checklist
> is the full standard.

### 1. Coding standards
**Naming** — class `UpperCamel`; function/method (camelCase or snake — check **project-internal consistency**); member
`m_`-prefix or `_`-suffix (follow the project's existing convention); constants/macros `UPPER_SNAKE`; locals
camelCase/snake. Flag any inconsistency with the file's own established convention.

**Structure** — single-responsibility functions (flag bodies over ~60 lines); nesting depth over ~4 levels; header
include guard (`#pragma once` or `#ifndef`); unused `#include`; magic numbers (should be named constants).

**Modern C++** — raw `new`/`delete` (prefer `std::unique_ptr`/`shared_ptr`); C-style casts (prefer
`static_cast`/`reinterpret_cast`); variables/reference-params that could be `const`; missing `override`.

### 2. Compiler-warning analysis
**Type safety** — signed/unsigned mix (`int` vs `size_t`/`uint32_t`); implicit truncation (`double`→`float`,
`int64`→`int32`); integer-overflow risk (loop counters; dimension products like `width * height` overflowing `int`);
`printf`/`scanf` format-vs-argument mismatch.

**Undefined behavior** — fixed-array out-of-bounds with external input; null deref without a check; uninitialized
variable use; returning a reference/pointer to a local.

**Resource management** — leak risk (early `return` in a branch skipping `delete`); unreleased file handle / lock;
constructor exception-safety.

**Image/DSP-specific (apply when relevant)** — buffer stride computation correctness; pixel value-range boundary
checks (e.g. `[0,255]` / `[0,1023]`); alignment requirements (SIMD often needs 16-byte; some DSPs 32-byte).

### 3. Performance hazards (flag only — defer fixes to `optimizing-cpp-performance`)
Hot-path dynamic allocation; hot-path virtual calls; large objects passed by value (should be `const&`); repeated
in-loop computation hoistable out.

### 4. Team embedded/SIMD rules
Check the code against the shared rule module `references/embedded-cpp-rules.md` (A: generic embedded/SIMD G1–G9;
B: toolchain rules T1–T2, applied per the consuming project's declared toolchain). Cite a violated rule by its `#`.

### 5. Comment-spec conformance (report-only — does NOT run the comment workflow)
If a mounted spec (Step 0) includes a comment standard, **report** per-function comment conformance as findings:
- required comment fields present? (e.g. input / output / key-steps / key-params / state-deps — per the spec's own
  field list, read at runtime).
- the spec's author-coupled signature token present on agent-authored comments? (the token name is read from the
  spec / instance, **never hardcoded**).
**Boundary** — this skill is **read-only**: it flags missing / non-compliant comments as findings; it does **not** add
comments, update any comment-status registry, or run the comment spec's read-trigger / blocking-gate workflow.
Executing that workflow is the **implementing agent's task obligation**, not this reviewer's.

## Output format
Findings grouped by severity. Each finding gives:
- **位置 / location**: `file:line`
- **级别 / level**: 🔴 error · 🟡 warning · 🔵 suggestion
- **问题 / issue**: concise description (cite the rule `#` when it maps to `embedded-cpp-rules.md`)
- **修复 / fix**: a corrected code snippet

End with a **summary table** counting findings per level.

## Notes
- **Read-only** — this skill analyzes and reports; it never edits the source.
- **Decoupling (skill_spec §9)**: this body is generic. The project's domain focus, target toolchain, VCS, **and the
  coding-spec source paths** are instance values (read at runtime / declared by the project); they are not hardcoded
  here. Domain examples above are illustrative. The mounted spec (Step 0) is named by no framework or path in this body
  — it is whatever `coding.review_spec_sources` points at.

## References
- `references/embedded-cpp-rules.md` — shared generic embedded/SIMD + toolchain rule module (consumed by both
  `reviewing-cpp-code` and `optimizing-cpp-performance`).
