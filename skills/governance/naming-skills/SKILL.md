---
name: naming-skills
category: governance
description: Validate and standardize a skill's name + description against the authoring naming rules — name ≤64 chars, lowercase letters/digits/hyphens only, no leading/trailing hyphen, name == parent folder, gerund (verb+ing) form; description ≤1024 chars, non-empty, says what-it-does + when-to-use with trigger keywords. Use when authoring, renaming, or publishing a skill, or auditing the home for naming conformance. Read-only validator — reports pass/fail per rule, does not rename.
allowed-tools: Read, Grep, Glob
---

# Naming Skills (skill-name + description validator)

Validate a skill's `name` and `description` against the **skill-authoring naming rules**, and report
pass/fail per rule. This is **read-only analysis** — you report; you do **not** rename, move, or edit the skill.
`publishing-skills` calls this as its naming gate before registration; an author or auditor can also run it standalone.

> **Rule provenance / transcription boundary.** The naming constraints below are the **skill-authoring naming rules
> from Anthropic's skill spec** (≤64 chars, hyphen charset, folder-match), surfaced via the Datawhale Chinese course
> rendering (`agent-skills-with-anthropic`, ch.6 §1.1–1.4, the cited authority). These are **factual rule points**, not
> copyrightable prose — the wording, the machine-check clauses, and every example here are **authored in this repo**.
> The **gerund (verb+ing) requirement** is stated in the source as a *recommendation*; **this ecosystem has ruled it a
> hard rule** (a local upgrade — see `skill_spec` §9 naming clause). Attribution is recorded in
> `THIRD-PARTY-NOTICES.md`; this skill carries **zero project/identity values** (skill_spec §9).

## Model (the rules — read first)

### A. `name` — hard constraints (all must pass)
1. **Length** — `name` is **≤ 64 characters**.
2. **Charset** — only **lowercase letters, digits, and hyphens** (`[a-z0-9-]`). No uppercase, no spaces,
   no underscores, no other punctuation.
3. **No edge hyphen** — must **not** start or end with a hyphen.
4. **Folder match** — `name` **must equal its parent directory name** (`skills/<category>/<name>/` →
   `basename` of the dir == frontmatter `name:`). The path is derived from `name`, not the reverse.
5. **Gerund (verb+ing) form** — `name` is a **gerund phrase naming the action the skill performs**
   (e.g. `reviewing-cpp-code`, `syncing-frameworks`), **not** a noun/agent name (`code-reviewer`,
   `thinking-partner`). *(Source = recommendation; ecosystem hard rule — see boundary note above.)*

### B. `description` — hard constraints (all must pass)
1. **Non-empty** and **≤ 1024 characters**.
2. **Says what-it-does + when-to-use** — states the skill's job **and** the trigger condition
   ("Use when …" / "用于 …").
3. **Trigger keywords** — embeds the words a user/agent would say to invoke it (so discovery matches).

### C. Optional frontmatter fields (validated only if present)
- `license` — SPDX-style string. `compatibility` — **≤ 500 characters**. `metadata` — free map.
  `allowed-tools` — comma list of tool names. Absence is **not** a failure; a present field must be well-formed.

### D. Body advisories (report as INFO, not fail)
- Body is **step-by-step** and **≤ 500 lines**. Referenced files sit at **one directory level** beside `SKILL.md`
  (e.g. `references/…`) so a regen that flattens the category level still resolves them.

## Triggers
- **Manual / keyword**: "校验 skill 命名" / "name a skill" / "rename a skill" / "check skill naming" /
  "audit naming" / "skill 命名校验" / "命名规范检查".
- Invoked by `publishing-skills` as the **pre-registration naming gate** (Step 0.5 there).
- Not automatic otherwise — run on request or as part of a publish/audit.

## Check Flow

### Step 1 — Locate the target(s)
- Single skill: read its `SKILL.md` frontmatter (`name:`, `description:`, optional fields) and note its
  parent directory name.
- Audit mode: enumerate every `skills/*/*/SKILL.md` and run each through Steps 2–4.

### Step 2 — Validate `name` (A1–A5)
For each rule emit **PASS/FAIL** with the offending value on FAIL:
- A1 length: `len(name) ≤ 64`.
- A2 charset: matches `^[a-z0-9-]+$`.
- A3 edge: matches `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$` (combines no-edge-hyphen with charset).
- A4 folder: `name == basename(dirname(SKILL.md))`.
- A5 gerund: heuristic — the **first token ends in `-ing`** (or the name is a single gerund word).
  A5 is **machine-screened, human-confirmed**: flag a non-`-ing`-leading name as **FAIL (confirm)**; a
  reviewer confirms genuine gerunds the heuristic misses. Never auto-pass a noun/agent name.

### Step 3 — Validate `description` (B1–B3)
- B1: non-empty and `len ≤ 1024`.
- B2: contains a what-it-does clause **and** a when-to-use clause (look for "Use when" / "用于" / "Use this skill
  when" or an equivalent trigger sentence). Missing the when-to-use clause → FAIL.
- B3: trigger keywords present (the verbs/nouns a caller would say). Thin/keyword-less description → FAIL.

### Step 4 — Validate optional fields (C) + body advisories (D)
- Any present optional field well-formed (C); `compatibility ≤ 500`.
- Body length + reference-depth advisories (D) → INFO rows (do not fail registration on these).

### Step 5 — Report
Emit a per-rule table (rule · PASS/FAIL/INFO · evidence). Overall verdict:
- **any A or B FAIL → NOT CONFORMANT** (blocks `publishing-skills` registration).
- A/B all PASS, only D INFO → **CONFORMANT** (INFO advisories listed for the author).

## Examples
- **PASS** — `reviewing-cpp-code` (gerund, 18 chars, charset clean, matches folder), `naming-skills`
  (gerund + object, 13 chars), `syncing-frameworks`.
- **FAIL A5 (not gerund)** — `cpp-code-review`, `thinking-partner`, `code-reviewer` (noun/agent forms).
- **FAIL A2/A3** — `My-Skill` (uppercase), `-foo` (leading hyphen), `bar_baz` (underscore), `name with space`.
- **FAIL B2** — a description that says what it does but never states **when** to use it (no trigger clause).

## Never touched
- A skill's **adoption** into a project toolset — a user-consent red line (skill_spec §6). This validator reports
  conformance; it never adopts, registers, renames, or edits.
- The skill body content beyond the naming/description/optional-field checks above — it does not lint prose.

## Notes
- **Read-only**: reports pass/fail; the rename itself is done by the author / `publishing-skills` (`git mv`), not here.
- **Single source of the rules**: this skill is the authority the home cites for skill naming; `skill_spec` §9 and
  `CONVENTIONS.md` point at it rather than restating the rule (consolidate-with-pointers).
