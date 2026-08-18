# VEMO_SKILLS · Home Conventions

> **Operating procedure** of this shared skill home. This doc states the *home-local procedure*; the *rules* it
> implements live in the consumer's governing skill specification. **Consolidate-with-pointers,
> not duplication** — where a rule is owned by `skill_spec`, this doc points at it rather than restating it.
> Adoption (a skill entering a project's toolset) is **out of scope** here and stays a user-consent decision
> (skill_spec §6).

## 0. Skill lifecycle — registration is the precondition
A skill becomes usable in stages, **in order**. Registration is the **gate stage**: nothing downstream can see a skill
that is not registered.

1. **Register (into the home)** — what `publishing-skills` does: place a standard skill package at
   `skills/<category>/<name>/` → add its normalized `.../SKILL.md` path to `skills/index.json` → add the README
   Skill-Catalog row + Use-via-Prompt entry (multiset-checked) → CHANGELOG entry + version bump. **Index activation
   is the act of registration.** A tree-only skill is inert and fails selfcheck.
2. **Bind (into a consuming project)** — a registered skill reaches a project by: pinning the VEMO_SKILLS submodule
   (commit/tag) → `team_bootstrap` regenerates it into `.claude/skills/<name>/` (byte-identical, §5) → the project's
   `project_profile.yaml` `shared_skills.provides` reflects it. **Registration ≠ adoption**: entering a team's *active
   toolset* is a **user-consent decision** (skill_spec §6) — binding makes a registered skill *available*, consent
   makes it *adopted*. The regen materializes **every** registered skill, **including the governance-meta skills
   themselves** (`skills/governance/` — `syncing-frameworks`, `contributing-framework-changes`, `publishing-skills`): there is **no
   separate installer** for the maintenance toolchain — acquiring this repo + regen binds the meta skills like any
   other (see the README **Getting started** section for the first-acquisition commands).
3. **Then sync / contribute** — only after a skill is registered (and, for sync, **released = registered + tagged**):
   - `syncing-frameworks` compares the pinned **released** version against the upstream latest — an unregistered/untagged
     skill is invisible to it.
   - `contributing-framework-changes` opens a PR against a **registered** skill in its repo — there is nothing to PR for a skill
     that was never registered.

So the chain is **register → bind (+consent = adopt) → sync / contribute**. The rest of this doc details stage 1's
conventions (the home's own responsibility); stages 2–3 are pointers to `team_bootstrap`, `syncing-frameworks`, and
`contributing-framework-changes`.

## 1. Category layout (path-derived and create-on-publish)
- Skills live under `skills/<category>/<name>/`. A **category** is a functional grouping (`governance/`,
  `orchestration/`, `research/`, `code/`), **not** a framework repo — `governance/` is owned by no single framework,
  while a domain category like `code/` groups skills owned by a domain framework (skill_spec §7). (Rule: skill_spec §9.)
- The category set is **path-derived, not a fixed enum**: publishing selects a functional category with the author,
  places the package under `skills/<category>/`, and creates that folder when needed. The normalized activation-index
  path is the machine declaration; category never enters model-visible frontmatter.
- **Mechanism**: the `publishing-skills` skill (`skills/governance/publishing-skills/`) performs placement + registration.

## 2. Standard skill package + explicit activation index
- Every source `SKILL.md` follows the current validator contract. Its required model-visible frontmatter is `name:` +
  `description:`; supported compatibility fields may remain, but repository placement metadata such as `category:`
  is forbidden.
- `skills/index.json` is the sole activation surface. It contains bounded, unique, repository-local
  `<category>/<name>/SKILL.md` references. Checker, catalog, and bind consume this index; they do not infer activation
  from arbitrary folders.
- `agents/openai.yaml` carries quoted UI metadata. Every default prompt names `$<skill-name>`; product-specific
  metadata stays outside `SKILL.md`, preserving progressive disclosure.
- **Naming conformance**: `name:` and `description:` must pass the skill-naming rules — `name` ≤64 chars, lowercase
  letters/digits/hyphens only, no leading/trailing hyphen, **gerund (verb+ing)** form, and `name` == its parent folder;
  `description` non-empty / ≤1024 chars / what-it-does + when-to-use + trigger keywords. The **rule is owned by
  `skill_spec` §9** (naming clause); the **authority + machine-check is the `naming-skills` skill**
  (`skills/governance/naming-skills/`), which `publishing-skills` runs as its pre-registration gate. This doc points at
  those rather than restating them (consolidate-with-pointers).

## 3. README maintenance obligation (+ Skill-Catalog row format)
- Every skill **add / move / rename / remove** updates `README.md`: **Skill-Catalog row** + category-layout line +
  Use-via-Prompt entry + keyword-triggers (trigger sub-table) row (for prompt-triggered skills). README entry-doc style:
  the **R29+ entry-doc family** (`skills/orchestration/publishing-deliverables/references/readme-style.md`, incl. the
  R32 bilingual pair). R30: never hardcode a version number — point at `VERSION` + `CHANGELOG.md`.
- **Skill-Catalog row format (home-local — like the §9 product-front-matter convention, NOT a generic entry-doc rule).**
  The README **Skill Catalog** carries one structured row per registered skill, with these columns:
  - **category** — must **equal** the skill's activation-index path category (checked for equality).
  - **skill** — the `` `<category>/<name>` `` identifier token; `<name>` must **equal** the frontmatter `name:` (derived,
    checked for equality). This token is what the §4 multiset diff extracts as set A — **it must be preserved**.
  - **does** / **when to use** / **boundary** — curated one-line cells; each must be **non-empty** (no machine truth to
    compare against, so completeness, not equality).
  Trigger keywords are **not** a catalog column — they live in the **Use via Prompt → Keyword triggers** sub-table; each
  prompt-triggered skill must have a row there (coverage). The catalog absorbs the old "role table"; the keyword table is
  relocated under Use-via-Prompt as the trigger sub-table (not removed). Bilingual mirror (R32). The machine check that
  enforces this is `publishing-skills` Step 5 (catalog-column completeness + derived-equality + trigger coverage).

## 4. README ⇄ skills consistency check (machine, multiset — not count)
- Set A = README **Skill-Catalog** rows' `` `<category>/<name>` `` tokens. Set B = activated references from
  `skills/index.json`. Assert **A == B as multisets**, then independently assert index references == filesystem
  `skills/*/*/SKILL.md`. This catches orphan rows, inert tree packages, dangling references, renames, and duplicates.
- **Name ⇄ placement-path**: frontmatter `name:` must equal the indexed `<name>` directory; category is derived from
  the indexed `<category>` segment.

## 5. Regen byte-identical (build-artifact rule)
- A consuming project regenerates each skill into `.claude/skills/<name>/` (the Claude Code discovery root) — a
  **gitignored build artifact**, single source = this home (skill_spec §9). After any skill-body change, verify
  `diff -r skills/<category>/<name> .claude/skills/<name>` is clean. Never hand-edit the regenerated copies.

## 6. Identity decoupling (red line)
- Skill bodies carry **zero hardcoded project/identity values** — no org, account, project path, wiki id, chat id, or
  language switch. Identity, upstream, and permission are resolved at runtime (`git remote get-url origin` /
  `gh api user` / a live `permissions.push` probe). (Rule: skill_spec §9 identity dimension.) The home repo name is
  allowed as an *example* only if annotated "resolved at runtime".
- **Self-check**: `grep -Ei '<org>|<account>'` on a published `SKILL.md` → 0 hits.

## 7. Versioning + release
- This home is versioned + pinned like a framework repo (own `VERSION` / `CHANGELOG.md`; PR-merged + tagged via
  `Framework_Release.procedure`). Tri-consistency: **VERSION == CHANGELOG top == (at release) git tag**. A consuming
  project pins a commit/tag and bumps it on a **user version gate** (`syncing-frameworks`).
- **PR-only (ruled 2026-06-11)**: every change to this repo lands via **branch → PR → merge** — direct pushes to the
  default branch are prohibited, for maintainers too.
- **Weekly official release train**: the official release (tag + announcement card) is cut **once a week (Friday)**.
  PRs merged by the Friday cutoff ride that week's train; unmerged PRs wait for the next one.
- **Merged-PR-only contribution counting**: a PR-sourced contribution enters the contributor ledger / leaderboard only
  after its PR is **merged (accepted)**. Open or rejected PRs are not counted and do not ship in the release.

## 8. Who runs publishing (actor constraint)
- The **Skill Scout** proposes a skill → the **user consents** → `publishing-skills` places + registers it. This is a role
  constraint on the actor, **not** a separate agent-categorization system: agents are framework-homed (registry_spec),
  there is no parallel agent-folder layout in this home. Adoption stays the user-consent red line (skill_spec §6).

## 9. Product front matter (home-local — VEMO_SKILLS-as-standalone-output)
- Because VEMO_SKILLS is published as an **independent repo** (not only a submodule), its `README.md` carries a
  **product-style front matter** block above the governed sections: a centered title + one-line tagline, **static
  badges**, and **Why / Features** sections, plus a **"reading this repo two ways"** standalone-vs-governed note.
- **This is a home-local convention, NOT a generic entry-doc rule.** It deliberately does **not** live in
  `readme-style.md` (R29–R32): framework READMEs are orientation docs, not product
  pages, and must not inherit a product-framing obligation. The convention is scoped to this home only.
- **Identity red line on badges (skill_spec §9 / §6 above):** badges MUST be **static or repo-relative** — a license
  badge linking to the in-repo [`LICENSE`](LICENSE), a version badge pointing at [`VERSION`](VERSION), a changelog
  badge. **No `shields.io` org-pathed badges** (e.g. `…/github/v/release/<org>/<repo>`) — those hardcode the team org
  and breach decoupling. A logo, if added, uses a repo-relative asset path, never an external/org-hosted URL.
- The bilingual pair (R32) applies: the zh mirror reproduces the front matter (HTML title + tagline + static badges)
  and stays heading-skeleton-parallel; its prose follows the zh-mirror fluency rubric (the `polishing-chinese-prose`
  翻译腔 band R14–R20, the R32 advisory leg — see §3).

> **Standalone summary of skill_spec §9 (generic/instance decoupling)** — for readers using this repo *outside* a
> governed project (where `skill_spec` itself is not present): skill bodies carry zero hardcoded project/identity
> values; generic mechanism + rules live here; all project-specific values live in the consumer's instance and are
> read at runtime. (Full rule: `skill_spec` §9, present in a governed project. This is a summary pointer, not a
> restatement that forks the rule.)

---
> Pointers: rules → `skill_spec` (§6 adoption pipeline + consent, §7 grouping, §9 decoupling). Style → `readme-style.md`
> (R29–R32, incl. the R32 bilingual pair + its `polishing-chinese-prose` advisory rubric). Sync/contribute of frameworks →
> `syncing-frameworks` / `contributing-framework-changes`.
