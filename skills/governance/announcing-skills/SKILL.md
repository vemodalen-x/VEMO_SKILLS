---
name: announcing-skills
description: 'Announce newly-registered skill(s) to a team chat as a celebratory Feishu (Lark) interactive card — a 上新表 (version / category / summary / @contributor) plus an optional 🏆 cumulative contribution leaderboard read from the hub''s contribution ledger (instance-gated by include_leaderboard). Use after a skill-hub release adds skills. Identity-decoupled — group, repo URL, and open_id map are instance values.'
---

# Skill Announce

After a skill-hub release adds one or more skills, post a **celebratory announcement card** to a team chat: a table of
what's new (hub version · category · summary · @'d contributor) and a **cumulative contribution leaderboard** (🏆 ranked
by how many contributions each person has made to the hub). This is a **governance-meta** skill — it operates on the
skill hub itself, alongside `publishing-skills` / `syncing-frameworks` / `contributing-framework-changes`.

## Triggers
- **Prompt / keyword**, run **post-release** (after `publishing-skills` registered the skills and the hub released):
  "公告一下新 skill" / "announce the new skills" / "发上新公告" / "skill 上新通知".
- Inputs: the **new-skill set** (this release's added skills) + the **released hub version**. Not automatic — it is a
  step you run after a release, mirroring how `publishing-deliverables` notifies after a publish.

## Model (read first)
- **Two facts, two homes (decoupling — skill_spec §9):**
  - The **contribution ledger** is a **hub fact**: `contributors.yaml` in the hub repo root — identity-FREE, keyed by a
    contributor **label**, listing each contribution (item + source + date). The leaderboard is computed from it. **PR-sourced
contributions count only once their PR is merged** (user ruling 2026-06-11) — open or rejected PRs are excluded
from the ledger and the leaderboard.
  - The **label→open_id map**, the **group chat id**, the **send identity**, and the **repo URL** are **org-instance
    facts**: read from the consuming project's instance `skill_hub.announce` at runtime. **Nothing identity-bearing is
    hardcoded in this skill.**
- **Card surface, not post.** Real tables need a Lark **interactive card** (`--msg-type interactive`). The send
  mechanism (lark-cli, `send_as`, idempotency) is shared with `publishing-deliverables`; only the payload differs. Card
  `<at id=ou_xxx></at>` syntax is **different** from post's `{"tag":"at"}` — see `references/card-format.md`, do not mix.

## Inputs (all instance-read; zero hardcode)
From the consuming project's `project_profile.yaml -> skill_hub.announce`:
- `send_as` (user|bot) · `group_chat_id` · `hub` (which home) · `repo_url` (hub git link, D10) ·
  `include_leaderboard` (bool — render the 🏆 leaderboard section or skip it) ·
  `contributor_open_id` (label → open_id) · `pr_account_map` (PR login → open_id, for PR-sourced contributions).
From the hub: `contributors.yaml` (the ledger). From the caller: the new-skill set + released version.

## Procedure
1. **Update the ledger.** For each newly-added skill/contribution, append an entry to the hub `contributors.yaml`
   (`label`, `item`, `source` = `feishu|pr`, `date`). Keyed by contributor **label** (identity-free).
2. **Resolve contributor identity.**
   - Source = **Feishu**: the contributor's open_id is the message sender (arrives at invocation); map its label via
     `contributor_open_id` for any other render needs.
   - Source = **repo PR**: map the PR account → open_id via `pr_account_map`.
   - For each label, look up `contributor_open_id[label]` → `ou_xxx` for the card `<at>`.
3. **Compute the leaderboard** *(only if `include_leaderboard` is true **and** the `contributor_open_id` map is non-empty
   — either condition unmet → skip this step and the Table ② / ranking-heading block in step 4; no error)*. Aggregate
   `contributors.yaml`: per contributor, `count = len(contributions)`; sort by count desc; assign 🥇🥈🥉 to the top three
   (then `4.`, `5.`, …). Collect each person's item list.
4. **Build the card** per `references/card-format.md`: turquoise header; opener `div` with `<at id=all></at>` +
   `**Skill Hub 版本：<version>**` + `[📦 Skill Hub 仓库](<repo_url>)`; Table ① 上新表 (Skill/分类/简介/贡献人
   `🏅 <at id=ou_xxx></at>（来源）`); **if the leaderboard is on** (`include_leaderboard` true + non-empty `contributor_open_id` map):
   `hr`; ranking heading; Table ② 排行榜 (名次/贡献人 `<at>`/累计贡献/贡献内容); **else omit that whole block**;
   closing 感谢 `div`. Fill `{VERSION}` / `{REPO_URL}` / `{ROWS}` / `{RANKING}` from the resolved inputs. Honor the hard
   constraints (config `wide_screen_mode`+`width_mode:fill`; `row_height` high; no column `width`; @ only in `lark_md`).
5. **Send.** `lark-cli im +messages-send --as <send_as> --chat-id <group_chat_id> --msg-type interactive
   --content '<card-json>' --idempotency-key <release-version>`. `--content` does not accept `@file` — inline the JSON.
6. **Identity preconditions** (surface, don't fail silently): `send_as: user` needs `im:message.send_as_user` (missing →
   emit the auth link, pause the send, keep the ledger update); `send_as: bot` needs the bot to be a group member.
7. **Record.** Write the announcement (group + version + @'d contributors) into the consuming project's `flow_log.md`
   when run there.

## Rules
- **Decoupling red line (skill_spec §9)**: this body is generic. Group, identity, repo URL, and the open_id maps are
  instance-owned (`skill_hub.announce`); the ledger is hub-owned and **identity-free**. Zero hardcode.
- **Leaderboard is instance-gated** — render the 🏆 section only when `include_leaderboard` is true **and** the
  `contributor_open_id` map is non-empty; either condition unmet → omit the section silently (no error). Whether to
  celebrate contributions is an instance choice, not a hub default.
- **Card, not post** — tables require the interactive surface; `<at>` syntax is card-specific (`references/card-format.md`).
- **Outward-facing** — sending to a group is outward; confirm with the user when unsure before sending.
- **Post-release step** — run after the skills are registered (`publishing-skills`) and released; it announces a real release.

## Never touched
- Skill **adoption** into a project toolset (user-consent red line, skill_spec §6) — this only announces what landed.
- The `contributor_open_id` / `pr_account_map` / `group_chat_id` — those are instance values, read not written.

## References
- `references/card-format.md` — Lark interactive-card constraints + the v6 template (placeholders, the card-vs-post
  `<at>` distinction, the field-tested hard constraints).
