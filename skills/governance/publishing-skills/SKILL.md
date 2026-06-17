---
name: publishing-skills
category: governance
description: Publish a skill into this shared skill home — auto-categorize by the skill's declared category (existing category → place into skills/<category>/<name>/; new category → create the folder), then maintain the README and verify regen. Use when adding, moving, or renaming a skill in VEMO_SKILLS. Placement + registration only — adoption (entering a project's toolset) stays a user-consent decision.
---

# Skill Publish

Place a skill into this shared skill home under its **declared category**, keep the README in lockstep, and verify the
working-copy regen. This skill governs **placement + registration** inside the home — it does **not** adopt a skill into
any project's toolset (that is the Skill Scout's pipeline and always needs user consent; skill_spec §6).

**Registration is the precondition for everything downstream.** The lifecycle is **register → bind (+consent = adopt)
→ sync / contribute** (see `CONVENTIONS.md` §0): a skill that is not registered here is invisible to `syncing-frameworks`
(which compares released = registered + tagged versions) and to `contributing-framework-changes` (which PRs a registered skill).
This skill performs the *register* stage; binding and sync/contribute are downstream of it.

## Model (read first)
- **Category is declared, not guessed.** Every skill carries `category:` in its `SKILL.md` frontmatter (single source
  of truth). The directory `skills/<category>/<name>/` is a **derived placement target**, not the source — if the
  frontmatter and the path ever disagree, the frontmatter wins and the skill is in the wrong folder (a check, below).
- **Naming is gated, not assumed.** A skill's `name`/`description` must pass the **`naming-skills`** validator (the
  authority for skill naming — name ≤64 / `[a-z0-9-]` / no edge hyphen / **gerund** / name==dir; description
  non-empty / ≤1024 / what+when / keywords) **before** registration. This skill references that rule, it does not
  restate it (consolidate-with-pointers); the gate runs at Step 0.5 and the whole-tree check at Step 5.
- **Categories are declare-and-create, not a fixed enum.** If `skills/<category>/` already exists → place into it. If
  it does not → **create the folder** and record the new category. The category set is whatever the filesystem holds;
  no hardcoded list (so this skill is correct for any home, not just this one — skill_spec §9 identity dimension).
  A category is a **functional grouping** (e.g. `governance/ orchestration/ research/`), not a framework repo.
- **README is part of the deliverable.** Every add / move / rename / remove updates the README (**Skill-Catalog row** +
  category-layout line + Use-via-Prompt entry + keyword-triggers row where applicable). The README ⇄ skills consistency
  is **machine-checked** by a multiset diff **plus a catalog-row completeness check** (Step 5), not a count compare — a
  count compare misses a rename or a wrong-folder placement. (Catalog-row format: `CONVENTIONS.md` §3.)
- **Identity-decoupled.** No org / account / project path is hardcoded. Targets are the local `skills/**` tree; the
  home repo is read from `git remote get-url origin` only if a remote reference is needed. Works for any consumer of
  this home (skill_spec §9). See `CONVENTIONS.md` for the full home-local convention set.
- **Regen is a build artifact.** A consuming project regenerates each skill into `.claude/skills/<name>/` (gitignored).
  Publishing a skill body obliges a **byte-identical regen check** (`diff -r`) wherever the home is consumed.

## Triggers
- **Manual / keyword**: "发布一个 skill" / "publish a skill" / "把这个 skill 归类" / "categorize this skill" /
  "add a skill to VEMO_SKILLS" / "新增 skill 到 skill 库".
- Not automatic — publishing is an authoring action, run on request.

## Pre-Check (Step 0, mandatory)
1. Confirm the working directory is a skill home (a `skills/` tree with a `README.md`, `VERSION`, `CHANGELOG.md`).
   If not → "Not a skill home (no skills/ + README/VERSION/CHANGELOG)" → **stop**.
2. Read the incoming skill's `SKILL.md` frontmatter. If `name:` or `category:` is missing → ask the author to add the
   declared category, **stop**. (Auto-categorize needs a declared value; it never guesses.)
3. If the skill already exists under a *different* category than declared → this is a **move**, not a fresh publish;
   confirm intent before relocating (and the README multiset check will flag the old row).

## Step 0.5 — Naming gate (mandatory, before placement)
Run the **`naming-skills`** validator on the incoming `SKILL.md` (it is the authority for skill naming; this skill
references it, it does not restate the rules). Registration is **blocked** unless every **hard** rule passes:
- `name` ≤ 64 chars, only `[a-z0-9-]`, no leading/trailing hyphen, **gerund (verb+ing)** form, and
  `name` == its parent directory name;
- `description` non-empty, ≤ 1024 chars, states what-it-does + when-to-use, with trigger keywords.
Any hard FAIL (incl. a non-gerund name — a hard rule in this ecosystem) → report the failing rule, ask the author to
fix the name/description, **stop**. Body/length advisories are INFO and do not block.

## Publish Flow
### Step 1 — Read the declared category
From the incoming `SKILL.md` frontmatter: `name:` and `category:`. These are the single source for placement.

### Step 2 — Resolve the target folder
Target = `skills/<category>/<name>/`.
- If `skills/<category>/` **exists** → place into it.
- If `skills/<category>/` **does not exist** → **create** the folder (declare-and-create) and note "new category
  `<category>` created" for the report and the CHANGELOG.

### Step 3 — Place the body (and references)
Write `SKILL.md` (and any `references/`) under the target. For a **move**, relocate the existing folder
(`git mv skills/<old-cat>/<name> skills/<category>/<name>`) so history is preserved — never copy-then-delete.

### Step 4 — Maintain the README (obligation)
Update `README.md`:
- **Skill Catalog** — add/update the skill's row: **category** (== `category:`) · **skill** (`` `<category>/<name>` ``
  token, == `name:`) · **does** · **when to use** · **boundary**. Curated cells non-empty; derived cells equal frontmatter.
  (Catalog-row format: `CONVENTIONS.md` §3. The `<category>/<name>` token is what the Step 5 multiset diff extracts.)
- **Layout section** — ensure the `<category>/` line lists the skill (add the category line if the category is new).
- **Use via Prompt** — add a trigger entry + a **Keyword-triggers sub-table** row **if** the skill is user-prompt-triggered.
- **R30**: never hardcode a version number in the README — point at `VERSION` + `CHANGELOG.md`.
(README entry-doc style: the R29+ entry-doc family in
`skills/orchestration/publishing-deliverables/references/readme-style.md` — incl. the bilingual pair.)

### Step 5 — Self-check (machine, before declaring done)
- **README ⇄ skills multiset diff** (not a count compare). Build set A = README **Skill-Catalog** rows' `` `<category>/<name>` ``
  skill tokens; set B = every `skills/*/*/SKILL.md` keyed by its frontmatter `name:` + `category:`. Assert **A == B** as
  multisets; report `only-in-README` (orphan row) and `only-in-tree` (unregistered skill). Validate against the
  **filesystem**, not a fixed list (categories are free-form).
- **Declared-category ⇄ placement-path**: for every `SKILL.md`, assert `category:` == the `<dir>` it sits under.
  Catches a skill in the wrong folder or a stale frontmatter value.
- **Identity grep-clean** (skill_spec §9): `grep -Ei '<org>|<account>'` on the new `SKILL.md` → 0 hits. (The home repo
  name as an example is allowed only if annotated "resolved at runtime".)
- **Naming conformance (whole tree)** — run **`naming-skills`** over every `skills/*/*/SKILL.md` and assert all
  **hard** rules green (name ≤64 / `[a-z0-9-]` / no edge hyphen / gerund / name==dir; description non-empty / ≤1024 /
  what+when / keywords). A FAIL here means a mis-named or stale skill slipped in — fix before declaring done.
- **Skill-Catalog completeness** (the row's *quality*; existence is already covered by the multiset diff above, so this
  does not re-assert it). For each `skills/*/*/SKILL.md`, in its Skill-Catalog row:
  - **derived-equality** (deterministic): the row's **category** cell **== frontmatter `category:`**, and the **skill**
    token's `<name>` **== frontmatter `name:`**. (Equality, not just non-empty — the category column is the user-facing
    "what category is this" answer; a non-empty-only check would let it drift and re-introduce the confusion this fixes.)
  - **curated non-empty**: **does** / **when to use** / **boundary** cells are all non-empty.
  - **trigger coverage**: every **prompt-triggered** skill has a row in the Use-via-Prompt **Keyword-triggers** sub-table.
  Run on both `README.md` and `README_zh.md` (R32 mirror). Any failure → fix before declaring done. (Format: `CONVENTIONS.md` §3.)

### Step 6 — Regen + verify (where the home is consumed)
In a consuming project: regenerate the skill into `.claude/skills/<name>/` and run
`diff -r skills/<category>/<name> .claude/skills/<name>` → must be clean (byte-identical; the copy is a build artifact).

### Step 7 — Version + changelog + ledger
- Bump `VERSION` (minor for a new skill / category; patch for a move or wording) and add a `CHANGELOG.md` entry
  (name the skill, its category, and any new category created). Keep **VERSION == CHANGELOG top == (at release) tag**.
- **PR-only + weekly train (ruled 2026-06-11)**: land the change via **branch → PR → merge** (no direct push to the
  default branch). The **tag + announcement** are cut by the **weekly Friday release train** — PRs merged by the Friday
  cutoff ride that train; unmerged PRs wait, and their contributions are not counted until merged.
- A publish is a workflow event — mirror it into the consuming project's `flow_log.md` when run there.

## Never touched
- A skill's **adoption** into a project toolset — that is the Skill Scout pipeline + a **user-consent red line**
  (skill_spec §6). This skill places and registers; it never decides a skill is adopted.
- Instance files / runtime ledgers, except the `flow_log.md` row recording a publish.
- The regenerated `.claude/skills/**` copies as a *source* — they are build artifacts; the home `skills/**` is edited.

## Notes
- **Who runs it**: the Skill Scout proposes a skill → the user consents → publishing places + registers it. The actor
  is a role constraint, not a separate categorization system — agents are framework-homed (registry_spec), there is no
  parallel agent-folder layout here.
- **Difference from a flat skill dump**: categorization is declared and machine-verified, so the home stays navigable
  and the README cannot silently drift from the tree.
