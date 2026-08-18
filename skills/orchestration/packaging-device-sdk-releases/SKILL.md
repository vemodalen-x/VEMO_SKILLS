---
name: packaging-device-sdk-releases
description: >
  Assemble an algorithm library into a deliverable on-device (mobile) SDK release package — the release version is assigned by `bumping-library-versions` (referenced, not restated), plus a standard package layout (minimal public headers / per-ABI libs / models each license-annotated / RELEASE_NOTES / USAGE doc / a compilable examples/ source / THIRD_PARTY), and two ship-along reports (quality + performance) that REUSE the eval-report and on-device-validation skills rather than re-spec them. Owns the package-specific parts: the memory = system-delta measurement method, license-boundary annotation, and a manifest + sha + unpack-reverify check (incl. verifying the version surfaces agree). Packaging is NOT releasing — shipping the package outward is a human/lead decision. Use when an algorithm lib must become a versioned, auditable phone SDK package. Identity-decoupled — lib name, version, platform, group are caller parameters.
allowed-tools: Read, Write, Bash
---

# Packaging Device SDK Releases

Assemble a built algorithm library into a **deliverable on-device (mobile) SDK release package**: a versioned, auditable
bundle a downstream team can integrate. This is an **artifact-producer** skill — it *assembles and verifies* the
package, in the same family as `publishing-deliverables` and `rendering-html-eval-reports` (which also produce/ship a
deliverable). It **composes** other skills rather than restating them: the two ship-along reports reuse
`rendering-html-eval-reports` (quality) and `validating-on-device-inference` (performance); this skill owns only the
**packaging-specific** parts.

> **Packaging is not releasing.** This skill produces and verifies the package. **Shipping it outward** — posting to a
> group, sending to a customer, publishing externally — is a **human / lead decision**, the same outward-facing boundary
> `announcing-skills` and `attending-group-mentions` honor. Produce, verify, hand off; do not ship on your own.
>
> Every concrete value — library name, version digits, target platform, destination group — is **read from the caller /
> instance**, never baked into this body.

## When to use
- A built algorithm library (its `.so`/`.a` per ABI + model files) must become a **versioned phone SDK package** with
  the headers, models, notes, and reports a downstream integrator needs.
- Trigger phrases: "打 SDK 发布包", "端侧 SDK 打包", "出手机 SDK 发布", "package the device SDK",
  "assemble an SDK release", "SDK 版本号 + 发布包".
- **Not automatic** — run when a release is cut. One pass assembles + verifies one package; the outward send is separate.

## Inputs (all instance-read; zero hardcode)
- `lib_name` + the built artifacts (per-ABI libraries, model files) + the **public headers** to expose.
- `version` (four segments, see §1) and the **version convention** the consumer already uses (this skill defaults to
  the scheme in §1 only if the consumer has none).
- `target_platform(s)` — the platform(s) the package is built/measured for (drives the platform-annotation discipline).
- Per-model **license facts** — training-data license + any usage boundary to annotate.
- The **quality + performance source data** (eval metrics; device latency/memory/power measurements) — produced by the
  composed skills, not computed here.

## §1 — Version (assigned by `bumping-library-versions` — referenced, not restated)
- The release version is **assigned / bumped by `code/bumping-library-versions`** — that skill owns the rule: the
  four-segment `X.Y.Z.W` shape, the bump policy (W=bug-fix, Z=feature-resets-W, X.Y human-set), the **single source →
  three agreeing surfaces** invariant (source constant / init-log / `getVersion()`), and the acceptance precondition.
  **This skill does not restate those rules** (single source) — it **consumes** the resulting version string for the
  package directory name + `RELEASE_NOTES`, and **verifies** the three surfaces agree at pack time (§5).

## §2 — Package layout
Assemble a standard tree (names are conventional; adapt to the consumer's integrator expectations):
```
<lib_name>-<version>/
  include/                 # MINIMAL public headers — only the integrator-facing API, not internal headers
  libs/<abi>/              # per-ABI built libraries (arm64-v8a, armeabi-v7a, … as built)
  models/                  # each model file + its license annotation (see §3)
  docs/
    RELEASE_NOTES.md       # version · capability list (numbers carry their 口径) · API quick-table · known limits
    USAGE.md               # how to use: init → feed frame → get result → release + a minimal snippet + FAQ
    quality_report.*       # §4a (via rendering-html-eval-reports)
    performance_report.*   # §4b (via validating-on-device-inference + the memory method below)
  examples/                # a MINIMAL compilable call example (source file; build command in its top comment)
  THIRD_PARTY.*            # third-party components bundled IN THE PACKAGE + their licenses
```
- **`include/` is minimal** — expose only the integrator-facing API; internal headers stay out of the package.
- **`RELEASE_NOTES`** states: the **version**, a **capability list with each number's 口径** (measured/inferred, eval
  condition), an **API quick-table**, and **known limitations / boundaries**.
- **`docs/USAGE.md`** — the integrator-facing how-to: the **call sequence** (initialize → feed a frame → get the result
  → release), a **minimal code snippet** of that sequence, and a **FAQ / common pitfalls** section. Written against the
  **actual shipped headers** (§include/), not an idealized API.
- **`examples/`** — at least one **minimal, compilable call example source file** demonstrating the same
  init→feed→get→release flow end-to-end. Its **top comment carries the build/compile command** (so an integrator can
  build it as-is). **Hard rule — write it against the real headers; do NOT invent interfaces:** every type, function,
  and field used must exist in the shipped `include/` headers (verify against them). A fabricated or aspirational API in
  the example is a packaging **FAIL** — the example must compile against the package it ships in.
- **`THIRD_PARTY`** here is the **package's** notices file (components shipped inside the zip) — distinct from this
  governance repo's own `THIRD-PARTY-NOTICES.md`.

## §3 — Model license annotation (hard rule)
- **Every model file carries its license annotation.** A model whose **training data is license-restricted MUST be
  conspicuously marked** with its **usage boundary** (where it may / may not be used, any redistribution limit) — in
  `models/` next to the file and surfaced in `RELEASE_NOTES`. A restricted model shipped without its boundary flagged
  is a packaging FAIL. (Ties to the data-license / privacy redlines the consuming project owns.)

## §4 — Two ship-along reports (compose, don't re-spec)

### 4a. Quality report — via `rendering-html-eval-reports`
- Per-capability **accuracy + eval 口径 (条件) + the abstain/reject column**, rendered by `rendering-html-eval-reports`
  (cited by name — do **not** re-spec accuracy tables here). Inherits that skill's **R6 measured-vs-inferred labelling**:
  every shipped number is marked measured or inferred. Include the **license boundary** of any capability backed by a
  restricted model.

### 4b. Performance report — via `validating-on-device-inference` + the memory method
- **Latency distribution, power proxy, platform-annotation** — reuse `validating-on-device-inference` (it owns
  warmup-separated latency distributions, the labelled power proxy, and the on-device measurement discipline). Cite it;
  do not restate.
- **Memory — the system-delta method (this skill OWNS this; the validation skill does not cover memory):**
  measure memory as a **before/after system delta, not a single absolute reading**:
  1. With the **algorithm OFF (idle baseline)**, sample **system available memory** and the **process PSS**.
  2. With the **algorithm ON**, sample the same two.
  3. Take the **steady-state difference across multiple rounds** (discard warmup rounds; report the stabilized delta,
     not a single shot — same distribution-not-single-shot discipline as latency).
  Report the **delta** (Δ system-available, Δ PSS) as the algorithm's memory cost, with the round count.
- **Platform-annotation discipline (hard):** every performance number is **header-flagged with the platform it was
  measured on**; a number from a **non-target platform MUST be conspicuously annotated** as such (it is an *inferred*
  proxy for the target, not a measured target number — the R6 measured-vs-inferred posture applied to perf).

## §5 — Release verification (before hand-off)
- **Manifest** — list the zip contents (every file, its path).
- **sha list** — a checksum line for each **key artifact** (libraries, model files, the zip itself).
- **Unpack-reverify** — unzip into a clean location and confirm the tree matches the manifest and the sha's match (a
  truncated/garbled zip is caught here, not by the integrator).
- **Version agreement** — re-confirm the three version surfaces (constant / log / `getVersion()`) read the same string
  (the invariant defined by `bumping-library-versions`; packaging **verifies** it at pack time, does not define it).
- **Example compiles** — build the `examples/` source against the shipped `include/` headers using the command in its
  top comment; it **must compile** (this is what proves the example uses only real, shipped interfaces — §2).
- **Capability ↔ binary consistency gate** — **every capability `RELEASE_NOTES` claims must be traceable to the
  *actual* path / exported symbol in the *shipped* library** — not to a stub, a placeholder build, or a config that the
  shipped `.a`/`.so` does not actually contain. Confirm against the binary (e.g. exported symbols / the linked code
  path), **not** the filename or the claim text. A claimed capability that cannot be pointed to in the shipped binary is
  a packaging **FAIL** (field lesson: a stubbed/placeholder `.a` cannot produce the numbers `RELEASE_NOTES` claims — the
  package then lies about what it does). This guards the claim→binary seam that the sha + compile checks do not cover.

## §6 — Release-action boundary (produce, don't ship)
- This skill ends at a **verified package + its manifest/sha**. **Sending it outward** (to a group, a customer,
  an external host) is a **human/lead decision** — packaging ≠ releasing. Hand the verified package up; the outward
  send is `announcing-skills` / `publishing-deliverables` / a human, not this skill.

## Rules
- **Version: single source, three agreeing surfaces** — constant / init-log / `getVersion()` must match; mismatch = FAIL
  (rule owned by `bumping-library-versions`; packaging verifies agreement at pack time).
- **Models carry license boundaries** — a restricted-data model without its usage boundary flagged is a FAIL.
- **Example uses real interfaces only** — `USAGE.md` + `examples/` are written against the shipped headers; an invented
  / non-existent API is a FAIL (the example must compile against the package — §2 / §5).
- **Claimed capability ↔ shipped binary** — every `RELEASE_NOTES` capability claim must be traceable to a real path /
  symbol in the **shipped** library (a stub / placeholder build that cannot produce the claimed numbers is a FAIL — §5).
- **Numbers carry 口径** — measured-vs-inferred + eval condition + platform, per the composed skills' R6 / platform rules.
- **Verify before hand-off** — manifest + sha + unpack-reverify; never hand off an unverified zip.
- **Packaging ≠ releasing** — produce + verify here; the outward send is a human/lead decision.
- **Decoupling red line (skill_spec §9)** — `lib_name`, version digits, platform, group, model-license facts, and the
  report source data are **instance-owned**; this body hardcodes none. The first release version is a specific value —
  it lives in the instance, not here.

## Never touched
- The **outward send** of the package (group post / external publish) — a human/lead decision, escalated, never auto-done.
- The instance values (`lib_name` / version / platform / destination) — read, never invented by this skill.
- The **quality/performance numbers themselves** — produced by the composed skills (eval run / on-device measurement),
  not computed here; this skill assembles and annotates them.

## Boundary
- **vs `rendering-html-eval-reports`** — that **renders** the quality (and training) report; this skill **consumes** that
  report as a package member and adds the packaging around it. Quality numbers → render there, package them here.
- **vs `validating-on-device-inference`** — that **measures + judges** on-device latency/consistency/power; this skill
  **reuses** those measurements for the performance report and **adds the memory system-delta method** (which that skill
  does not cover) + the packaging. Device sign-off → there; ship-along perf report + memory → here.
- **vs `bumping-library-versions`** — that **owns the version rule and performs the bump** (shape / policy / single-
  source-three-surfaces / acceptance precondition); this skill **consumes** the resulting version string and **verifies**
  the three surfaces agree at pack time. Bump → there; consume + verify-at-pack → here.
- **vs `publishing-deliverables` / `announcing-skills`** — those **send** a deliverable/announcement outward; this skill
  **produces** the package and stops at the outward boundary (§6).
- **Chinese-prose** of any human-facing notes defers to `polishing-chinese-prose` (cited by name).

## References
- Composes `code/bumping-library-versions` (the version rule — shape / bump policy / single-source-three-surfaces /
  acceptance precondition; §1 references it, does not restate it), `orchestration/rendering-html-eval-reports` (quality +
  training reports, R6 measured-vs-inferred), `code/validating-on-device-inference` (latency distribution / power proxy /
  platform annotation), and the outward-send boundary of `orchestration/publishing-deliverables` /
  `governance/announcing-skills`. The package's own `THIRD_PARTY` notices are a **package member**, not this repo's
  `THIRD-PARTY-NOTICES.md`; zip/sha/unzip are invoked tools, not vendored libraries.
