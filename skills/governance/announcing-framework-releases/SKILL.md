---
name: announcing-framework-releases
category: governance
description: Announce a governance framework's formal version release to the team chat as a Feishu (Lark) interactive card — framework name + code, old→new version, change-class summary (Added / Changed / ⚠️ BREAKING) extracted from its CHANGELOG, a one-line consumer-impact verdict (sync now? breaking?), repo + CHANGELOG links, maintainer, plus an optional 🏆 cumulative contribution leaderboard (instance-gated by include_leaderboard, computed from the same hub ledger as announcing-skills). Use after a framework release is tagged and push-verified. Identity-decoupled — group and the maintainer/contributor open_id maps are instance values; repo URL is resolved at runtime from the submodule remote.
---

# Announcing Framework Releases

After a governance framework cuts a **formal version release** (a new version tag, pushed and verified), post a
**version-update card** to the team chat: which framework, old→new version, a change-class summary pulled from its
CHANGELOG, a one-line **consumer-impact verdict**, the repo / CHANGELOG links + maintainer, and — when the instance
opts in — an **optional 🏆 cumulative contribution leaderboard**. This is a **governance-meta** skill — it operates on
the framework ecosystem, alongside `syncing-frameworks` / `announcing-skills` / `publishing-skills`.

**Boundary vs `announcing-skills`**: `announcing-skills` celebrates **skill-hub 上新** (新 skill); **this** skill
announces a **framework version update** (framework / version / change-class / consumer-impact). Different trigger,
data, and core payload. **Both** carry the **same optional 🏆 leaderboard** — a per-user ruling (2026-06-11): a
contribution shows up wherever it is announced, so the leaderboard rides **both** cards, computed from the **one** hub
ledger (`contributors.yaml`) and gated by the instance toggle. **PR-sourced contributions count only once their PR is
merged** (user ruling 2026-06-11); unmerged PRs are excluded from the ledger and the leaderboard. (This reverses the skill's original "no leaderboard"
design; see the CHANGELOG.) The leaderboard block is **identical in shape** to `announcing-skills`' — see
`references/card-format.md`.

## Triggers
- **Prompt / keyword**, run **post-release** (after the framework's release tag is cut **and push-verified**):
  "公告框架版本更新" / "announce framework release" / "发框架升级公告" / "框架版本公告".
- Inputs from the caller: **which framework** released + its **old→new version**. Not automatic — it is a step run in
  the version-gate flow after a verified release.

## Model (read first)
- **Render, don't author.** The change summary is **extracted** from the released framework's CHANGELOG top entry
  (`## [X.Y.Z]` … its `### Added/Changed/Fixed/BREAKING` sections) — the CHANGELOG is the **single source** of the
  change text. This skill classifies + links; it never rewrites the change prose.
- **Framework-agnostic (decoupling — skill_spec §9).** No framework name is hardcoded. *Which* framework released
  comes from the caller's input; its repo / CHANGELOG URL is **resolved at runtime** from the pinned submodule's
  remote (`git -C <submodule> remote get-url origin`) — the same pattern `syncing-frameworks` uses. (Note the
  divergence from `announcing-skills`, which reads an instance `repo_url` for the single hub; a framework announce
  targets many frameworks, so URL resolution is runtime, not instance.)
- **Two homes for identity.** The **group chat id** and the **maintainer→open_id map** are **org-instance facts**
  (`project_profile.yaml -> framework_announce`, with the group reused from `skill_hub.announce.group_chat_id` —
  single source, same group). Nothing identity-bearing is hardcoded in this skill.
- **Leaderboard reuses the hub's single ledger + maps (no second ledger).** The optional leaderboard is computed from
  the **same** hub `contributors.yaml` as `announcing-skills`, and resolves @-mentions via the **same** instance maps
  `skill_hub.announce.contributor_open_id` + `pr_account_map` — **not** redeclared under `framework_announce` (single
  source, the same way `framework_announce` reuses `group_chat_id`). A per-user ruling (2026-06-11): the leaderboard is
  "contributions made visible", not a taxonomy — so both cards read one ledger and may show the same ranking. Gated by
  `framework_announce.include_leaderboard`.
- **Card surface, not post.** The change-class summary is a real table, so the message is a Lark **interactive card**
  (`--msg-type interactive`). The send mechanism (lark-cli, `send_as`, idempotency) is shared with `announcing-skills`
  / `publishing-deliverables`; only the payload differs — see `references/card-format.md` (this skill's **own** card
  reference; the change-class table is this card's distinctive part, plus the **same optional leaderboard block** as
  `announcing-skills`).

## Inputs (all instance-read / runtime-resolved; zero hardcode)
- From the caller: the **released framework** (its code, e.g. the submodule id) + **old→new version**.
- From `project_profile.yaml -> framework_announce`: `send_as` (user|bot) · `maintainer_open_id` (framework code →
  open_id) · `include_leaderboard` (bool — render the 🏆 leaderboard section or skip it). **Group chat id**: read at
  runtime from `skill_hub.announce.group_chat_id` (same group, single source — not redeclared in `framework_announce`).
- **For the leaderboard** (only if `include_leaderboard`): the hub `contributors.yaml` ledger (same one
  `announcing-skills` reads) + the instance `skill_hub.announce.contributor_open_id` and `pr_account_map` maps (reused,
  **not** redeclared under `framework_announce` — single source).
- Resolved at runtime: the framework's **repo URL** and **CHANGELOG URL** via `git -C <submodule> remote get-url
  origin` (build the CHANGELOG link from the remote + the repo's CHANGELOG path).
- From the framework: its **CHANGELOG.md** top `[X.Y.Z]` entry (the released version's change text).

## Procedure
1. **Read the released framework's CHANGELOG top entry** (`## [<NEW_VER>]`): collect its `### Added` / `### Changed` /
   `### Fixed` / `### BREAKING` (or `⚠️ BREAKING`) sections. This is the authoritative change text — extract, don't rewrite.
2. **Classify the changes** into the change-class table rows (one row per present class; ⚠️ BREAKING row first if present).
3. **Derive the consumer-impact verdict** (deterministic rule — see below).
4. **Resolve repo + CHANGELOG URLs** at runtime from the submodule remote.
5. **Resolve the maintainer**: `maintainer_open_id[<framework-code>]` → `ou_xxx` for the card `<at>`. **Missing**
   (e.g. an external maintainer not in the group) → render the maintainer as **plain text**, skip the `@` (do not fail).
6. **Compute the leaderboard** *(only if `include_leaderboard` is true **and** the `contributor_open_id` map is
   non-empty — either condition unmet → skip this step and the leaderboard block in step 7; no error)*. **Read** (do
   **not** write) the hub `contributors.yaml`: per contributor, `count = len(contributions)`; sort by count desc;
   assign 🥇🥈🥉 to the top three (then `4.`, `5.`, …); collect each person's item list. Resolve each label's `<at>`
   via the reused `skill_hub.announce.contributor_open_id` (and `pr_account_map` for PR-sourced rows). This is the
   **same ledger and same maps** `announcing-skills` uses — a single source, so the two cards' leaderboards may match.
   *(Adding framework-contribution entries to the ledger is a separate ledger-maintenance step, not done by this skill.)*
7. **Build the card** per `references/card-format.md` (fill `{FRAMEWORK}`/`{CODE}`/`{OLD_VER}`/`{NEW_VER}`/`{REPO_URL}`/
   `{CHANGELOG_URL}`/`{IMPACT}`/`{CHANGE_ROWS}`/`{MAINTAINER_AT}`/`{DATE}`; **if the leaderboard is on**, also fill
   `{RANKING}` and include the `hr` + ranking-heading + Table ② block; **else omit that block**; honor the field-tested
   hard constraints).
8. **Confirm, then send** (outward-facing — sending to a group publishes). `lark-cli im +messages-send --as <send_as>
   --chat-id <group_chat_id> --msg-type interactive --content '<card-json>' --idempotency-key <framework>-<NEW_VER>`.
   `--content` does not accept `@file` — inline the JSON.
9. **Record.** Write the announcement (framework + old→new version + group) into the consuming project's `flow_log.md`.

## Consumer-impact verdict (deterministic rule — checkable, not free prose)
> Do **not** key "breaking" solely on a textual `⚠️ BREAKING` marker — **external frameworks' CHANGELOGs may not use it**
> (e.g. one that only has `### Added/Changed`). Use a **framework-agnostic** fallback signal: a **semver major bump**.
```
IF  CHANGELOG top entry contains "⚠️ BREAKING" / "### BREAKING"   OR   major-version bump (X increases, e.g. 1.x → 2.0)
    → IMPACT = "⚠️ 破坏性更新：sync 前请评估对本项目的影响，可能需要适配。"
ELIF only recognized non-breaking sections (Added / Changed / Fixed) AND not a major bump
    → IMPACT = "✅ 向后兼容：可在下一个版本门照常 sync 升级。"
ELSE (no recognized sections / unparseable)
    → IMPACT = "ℹ️ 变更类型待确认：请查阅 CHANGELOG 评估影响。"   # do not guess
```
- Semver-major is the universal signal; the textual marker is a **supplement**, not the sole trigger.

## Rules
- **Decoupling red line (skill_spec §9)**: zero hardcoded framework name / repo / identity. Group + maintainer map are
  instance-owned (`framework_announce`, group reused from `skill_hub.announce`); the leaderboard ledger + contributor
  maps are reused from the hub / `skill_hub.announce` (single source, not redeclared); repo/CHANGELOG URL resolved at
  runtime from the submodule remote. The CHANGELOG is the single source of change text.
- **Leaderboard is instance-gated, single-ledger** — render the 🏆 section only when `include_leaderboard` is true
  **and** the `contributor_open_id` map is non-empty; either unmet → omit silently (no error). It reads the **one** hub
  ledger (`contributors.yaml`) — it never writes a second one. The same block appears on `announcing-skills`' card.
- **Card, not post** — the change-class table needs the interactive surface; `<at>` syntax is card-specific
  (`references/card-format.md`), distinct from a post's `{"tag":"at"}`.
- **Announce-after-push** — run **only after the release tag is cut and push-verified**; never pre-announce.
- **Outward-facing** — sending to a group publishes; **confirm with the user before sending**.

## Never touched
- The framework's repo / tags / CHANGELOG — read-only; this skill announces a release, it does not cut one.
- The `maintainer_open_id` / `contributor_open_id` / `pr_account_map` / `group_chat_id` — instance values, read not written.
- The hub `contributors.yaml` ledger — **read-only** here (this skill ranks from it; adding framework-contribution
  entries is a separate ledger-maintenance step, not this skill's job).

## References
- `references/card-format.md` — this skill's **own** Lark interactive-card reference (the version-update card: a
  change-class table + impact line + maintainer, plus the **same optional 🏆 leaderboard block** as `announcing-skills`,
  instance-gated).
