# Lark Interactive-Card Format (announcing-framework-releases)

> Generic reference for the Feishu (Lark) **interactive card** that `announcing-framework-releases` posts. The card
> surface is used (not `post`) because the change-class summary is a **real table**. Zero project values here — the
> group, maintainer/contributor open_ids, framework name, versions, and URLs are runtime/instance inputs rendered into
> the placeholders below. The distinctive part of this card is the **change-class table + consumer-impact line**; it
> **also carries the same optional 🏆 contribution leaderboard** as `announcing-skills` (a per-user ruling 2026-06-11 —
> the leaderboard rides both cards, instance-gated by `include_leaderboard`, computed from the one hub ledger).

## Why a card, not a post
`post` cannot render real tables; this announcement needs the change-class table. So the message is sent as
`--msg-type interactive` with a card payload. The **send mechanism is shared** with `announcing-skills` /
`publishing-deliverables` (lark-cli, `send_as`, idempotency-key) — **only the payload differs**.

## ⚠️ `<at>` syntax is surface-specific — do NOT cross-contaminate
- **Card (this skill)**: mentions use `<at id=ou_xxx></at>` (and `<at id=all></at>` for @all), **only inside `lark_md`**
  text/columns. A `text` column will not render `<at>`.
- **Post (`publishing-deliverables`)**: mentions use `{"tag":"at","user_id":"ou_xxx"}`.
- Two different syntaxes for two different surfaces. Never mix them.

## Hard constraints (field-tested — violating these makes the card reject)
- Card `config` **must** include `{"wide_screen_mode": true, "width_mode": "fill"}`.
- Header `template`: `turquoise`.
- Table `row_height`: **only** `low` / `middle` / `high` — `auto` is **rejected**. Use `high`.
- Table columns: **never** set a column `width` — any px value is **rejected**. Omit it; `width_mode:"fill"` handles width.
- @-mention columns/divs **must** be `"data_type":"lark_md"` (a `text` column will not render `<at>`).

## Card structure (change-class table + optional leaderboard)
1. **Header** — turquoise banner, title `📢 治理框架版本更新公告`.
2. **Opener `div`** (`lark_md`) — `<at id=all></at>` + a notice line + **框架：{FRAMEWORK}（{CODE}）** + **版本：{OLD_VER} → {NEW_VER}**
   + `[📦 仓库]({REPO_URL})　[📋 CHANGELOG]({CHANGELOG_URL})`.
3. **Impact `div`** (`lark_md`, prominent) — `{IMPACT}` (the deterministic consumer-impact verdict).
4. **Table ① 变更分类摘要** — columns: `类别` (Added / Changed / ⚠️ BREAKING / Fixed) · `要点` (CHANGELOG-extracted, 1–3
   bullets per class). The ⚠️ BREAKING row, if present, goes **first**.
5. **`hr`** divider.
6. **Footer `div`** (`lark_md`) — `🛠️ 维护者 {MAINTAINER_AT}`（`<at id=ou_xxx></at>`, or plain text if no open_id）
   `　|　发布日期 {DATE}` + an upgrade hint: `如何升级：在你项目的版本门用 syncing-frameworks 评审并 bump pin。`
7. **`hr`** divider. *(leaderboard block — omitted when the leaderboard is off)*
8. **Ranking heading `div`** (`lark_md`) — `🏆 Skill Hub 累计贡献排行榜`. *(leaderboard block)*
9. **Table ② 排行榜** — columns: `名次` (🥇🥈🥉 / 4. / 5. …) · `贡献人` (`lark_md`, `<at id=ou_xxx></at>`) · `累计贡献` (count) · `贡献内容` (items). *(leaderboard block)*

> **Leaderboard is conditional** — elements 7–9 (the `hr` + ranking heading + Table ②) render **only** when the instance
> `framework_announce.include_leaderboard` is true **and** the `contributor_open_id` map is non-empty. When off, drop
> those three elements; the card is then header + opener + impact + Table ① + footer. The leaderboard block is the
> **same shape** as `announcing-skills`' Table ②, computed from the **same** hub `contributors.yaml` (single ledger);
> the skill body (`Procedure` step 6/7 + Rules) owns the gate.

## Placeholders (filled at runtime — never hardcode)
- `{FRAMEWORK}` / `{CODE}` — framework name + code (caller input; e.g. its submodule id).
- `{OLD_VER}` / `{NEW_VER}` — old→new version (caller input).
- `{REPO_URL}` / `{CHANGELOG_URL}` — resolved at runtime from the submodule remote (`git -C <submodule> remote get-url
  origin`), **not** hardcoded and **not** an instance value (frameworks are many; resolution is runtime).
- `{IMPACT}` — the deterministic consumer-impact verdict (see the skill's rule: ⚠️ BREAKING marker OR semver-major →
  breaking; recognized non-breaking sections only → compatible; else → neutral).
- `{CHANGE_ROWS}` — Table ① rows, one per present change class (⚠️ BREAKING first).
- `{MAINTAINER_AT}` — `<at id=ou_xxx></at>` from instance `framework_announce.maintainer_open_id[<code>]`; **plain text**
  if the maintainer has no open_id (external maintainer not in the group).
- `{DATE}` — the release date.
- `{RANKING}` — Table ② rows (leaderboard block only): contributors sorted by count desc, medals for top 3. Computed
  from the hub `contributors.yaml`; `<at>` open_ids come from instance `skill_hub.announce.contributor_open_id[label]`
  (and `pr_account_map` for PR-sourced rows) — the **same** ledger + maps `announcing-skills` uses (single source).
  Present only when the leaderboard is on.

## Template (skeleton — `{...}` are runtime fills)
```json
{
  "config": {"wide_screen_mode": true, "width_mode": "fill"},
  "header": {"template": "turquoise", "title": {"tag": "plain_text", "content": "📢 治理框架版本更新公告"}},
  "elements": [
    {"tag": "div", "text": {"tag": "lark_md", "content": "<at id=all></at> 📣 治理框架有正式版本更新，请相关项目留意 🛠️\n**框架：{FRAMEWORK}（{CODE}）**　|　**版本：{OLD_VER} → {NEW_VER}**\n[📦 仓库]({REPO_URL})　[📋 CHANGELOG]({CHANGELOG_URL})"}},
    {"tag": "div", "text": {"tag": "lark_md", "content": "{IMPACT}"}},
    {"tag": "table", "page_size": 5, "row_height": "high",
     "header_style": {"text_align": "left", "background_style": "grey", "bold": true},
     "columns": [
       {"name": "class", "display_name": "类别", "data_type": "text"},
       {"name": "points", "display_name": "要点", "data_type": "text"}
     ],
     "rows": [ "{CHANGE_ROWS}" ]},
    {"tag": "hr"},
    {"tag": "div", "text": {"tag": "lark_md", "content": "🛠️ 维护者 {MAINTAINER_AT}　|　发布日期 {DATE}\n如何升级：在你项目的版本门用 syncing-frameworks 评审并 bump pin。"}},
    {"tag": "hr"},
    {"tag": "div", "text": {"tag": "lark_md", "content": "**🏆 Skill Hub 累计贡献排行榜**"}},
    {"tag": "table", "page_size": 5, "row_height": "high",
     "header_style": {"text_align": "left", "background_style": "grey", "bold": true},
     "columns": [
       {"name": "rank", "display_name": "名次", "data_type": "text"},
       {"name": "who", "display_name": "贡献人", "data_type": "lark_md"},
       {"name": "count", "display_name": "累计贡献", "data_type": "text"},
       {"name": "items", "display_name": "贡献内容", "data_type": "text"}
     ],
     "rows": [ "{RANKING}" ]}
  ]
}
```
(This card shape mirrors the field-tested constraints derived from `announcing-skills`' live send tests. The
distinctive part is the change-class table + impact line; the **leaderboard block** — the last three elements (`hr` +
ranking heading + Table ②) — is the **same** as `announcing-skills`' and is included **only when the leaderboard is
on**; drop those three elements when off (see the "Leaderboard is conditional" note in the Card-structure section).
`page_size` paginates a table; keep it at/above the expected row count to show all rows.)
