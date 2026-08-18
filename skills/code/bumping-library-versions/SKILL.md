---
name: bumping-library-versions
description: >
  Bump a device/library's four-segment version after an acceptance build+run passes, and keep the version single-sourced. The four segments X.Y.Z.W are embedded in three agreeing surfaces — a source string constant, the init log line, and a getVersion() API. Bump rules: W (last) = bug-fix +1; Z (penultimate) = feature +1 and reset W to 0; both-in-one-release = Z +1 and reset W to 0; X.Y (first two) = major/platform-line, human-set only. Precondition: the acceptance build+run has already succeeded. After bumping, report old → new explicitly. Use when releasing a library and the version must advance. Identity-decoupled — the version-string field name + file are caller parameters; no project names embedded.
allowed-tools: Read, Edit, Bash
---

# Bumping Library Versions

Advance a device/library's **four-segment version** when a release is cut, and keep that version **single-sourced** so
every surface that reports it agrees. This skill **owns the version rule**: the segment shape, the bump policy, the
acceptance precondition, and the old→new report. It is referenced by `packaging-device-sdk-releases` (which **consumes**
the resulting version string and **verifies** the surfaces agree at pack time) — the rule lives **here**, once.

> The version-string **field name** and the **file** it lives in are **caller-specified** (e.g. a named string constant
> in a named source file). This body hardcodes **no** project field name, file path, or library name — they are read
> from the caller / instance.

## When to use
- A library release is being cut and its version must advance (a bug-fix or a feature shipped).
- Trigger phrases: "升库版本号", "bump the library version", "改版本号", "发版升号", "version bump after acceptance".
- **Not automatic** — run on request as part of cutting a release, **after** the acceptance build+run has passed (§Precondition).

## Inputs (all caller-read; zero hardcode)
- `version_field` — the version-string **field/constant name** the consumer uses, and the **file(s)** it is defined in.
- The **current version** string (four segments).
- The **release kind** — bug-fix / feature / both — that drives the bump.
- The **three surfaces** the consumer exposes the version through (constant / init-log / `getVersion()`), so agreement
  can be confirmed.

## Model — version shape & single-source
- **Shape `X.Y.Z.W`** (four segments):
  - **W** — last (bug-fix counter).
  - **Z** — penultimate (feature counter).
  - **X.Y** — first two (major / platform-line).
- **Single source → three agreeing surfaces.** The version is defined **once** and surfaced in **three places that must
  agree**: (1) a **source string constant** compiled into the library, (2) the **init log line** the library prints on
  load, (3) the **`getVersion()` API** return. A release where these three disagree is a **FAIL** — they must read the
  same string. (The bump edits the single source; the other two derive from it. If they are separate literals in the
  consumer's code, update all of them and confirm agreement.)

## Bump rules (which segment moves)
- **Bug-fix only** → **W += 1**. (Earlier segments unchanged.)
- **Feature only** → **Z += 1**, and **reset W to 0**.
- **Both feature and bug-fix in one release** → **Z += 1**, and **reset W to 0** (the feature bump subsumes the W reset).
- **X.Y (major / platform-line)** → **human-set only** — never auto-bumped by this skill; the maintainer/lead decides
  when a major or platform line changes.
- **Earlier segments stay unchanged** on a W or Z bump.

## Precondition (hard)
- **The acceptance build+run has already succeeded** in the current task. Do **not** bump a version onto a library that
  has not passed its acceptance — the version number asserts "this built and passed," so bumping before acceptance lies
  about the artifact. If acceptance has not run / not passed, **stop** and say so; do not bump.

## Workflow
1. **Confirm the precondition** — acceptance build+run passed. If not → stop, report why.
2. **Locate the version** — read `version_field` in the caller-specified file(s); parse the four segments.
3. **Apply the bump** per the rules above (bug-fix → W+1; feature/both → Z+1, W=0; X.Y untouched).
4. **Write back to the single source** (and any sibling literals for the init-log / `getVersion()` surfaces if they are
   separate), so all three surfaces read the new string.
5. **Report `old → new` explicitly** — e.g. "version 3.2.1.4 → 3.2.2.0 (feature bump)". The explicit old→new line is the
   record of what changed and why.

## Rules
- **Bump only after acceptance** — the precondition is hard; an un-accepted artifact does not get a version bump.
- **Single source, three agreeing surfaces** — constant / init-log / `getVersion()` must read the same string after the bump.
- **Only the rule-permitted segments move** — W (bug-fix), Z (feature, resets W); X.Y is human-set, never auto-bumped.
- **Report old → new explicitly** — every bump states the before/after and the reason.
- **Decoupling red line (skill_spec §9)** — the version-field name, the file path, and the library name are
  **caller-specified**; this body hardcodes none. Borrowed from a consuming project's release convention, generalized
  here — the concrete field/file/library names live in the instance, not in this body.

## Never touched
- The **X.Y major / platform-line** segments — **human-set**, never auto-bumped by this skill.
- The **acceptance gate itself** — this skill **depends on** acceptance having passed; it does not run or judge acceptance.
- The caller's field name / file path — read and edited as the version source, but the *identity* of which field/file
  is the instance's to specify, not this skill's to assume.

## Boundary
- **Category note — first write-action skill in `code` (explicit exception).** It is placed in `code` on the **domain**
  axis (a library's version is a code / deploy-domain concern — that is where someone looks for it), which takes
  precedence over the incumbent convention that every other `code` skill is read-only/advisory. Unlike its siblings,
  this skill **writes** — but **only the version constant / log line** (the single version source), **nothing else**: it
  touches **no logic, no behavior, no other source**. The write is narrowly bounded to the version string surfaces; the
  exception is **declared here, not silently taken**.
- **vs `packaging-device-sdk-releases`** — that skill **assembles the release package** and, at pack time, **verifies**
  the three version surfaces agree; **this** skill **owns the version rule** (shape, bump policy, precondition) and
  **performs the bump**. Bump the version → here; package the release and verify agreement → there. The rule is stated
  **once, here**; packaging references it.
- **Provenance** — the four-segment scheme + bump policy are **borrowed from a consuming project's release convention**
  and generalized; a consumer with its own convention follows that, using this skill's shape only as the default.
