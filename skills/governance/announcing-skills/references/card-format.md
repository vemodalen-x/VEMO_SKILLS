# Lark Interactive-Card Format (announcing-skills)

> Generic reference for building the Feishu (Lark) **interactive card** that `announcing-skills` posts. The card surface
> is used (not `post`) because the announcement needs **real tables**. Zero project values here — the group, repo URL,
> contributor open_ids, and version are runtime/instance inputs rendered into the placeholders below.

## Why a card, not a post
`post` cannot render real tables; this announcement requires tabular layout (上新表 + 排行榜). So the message is sent as
`--msg-type interactive` with a card payload. The **send mechanism is shared** with `publishing-deliverables` (lark-cli,
`send_as`, idempotency-key) — **only the payload differs**.

## ⚠️ `<at>` syntax is surface-specific — do NOT cross-contaminate
- **Card (this skill)**: mentions use `<at id=ou_xxx></at>` (and `<at id=all></at>` for @all), **only inside `lark_md`**
  text/columns. A `lark_md` `div` or a column with `"data_type":"lark_md"` renders them; plain `text` columns do not.
- **Post (`publishing-deliverables`)**: mentions use the element form `{"tag":"at","user_id":"ou_xxx"}` (`"all"` for @all).
- These are **two different syntaxes for two different surfaces.** Never mix them — a card `<at>` in a post stays
  literal text, and a post `{"tag":"at"}` is invalid in a card.

## Hard constraints (field-tested — violating these makes the card reject)
- Card `config` **must** include `{"wide_screen_mode": true, "width_mode": "fill"}`.
- Header `template`: `turquoise` (celebratory banner).
- Table `row_height`: **only** `low` / `middle` / `high` — `auto` is **rejected**. Use `high`.
- Table columns: **never** set a column `width` — any px value is **rejected**. Omit it; `width_mode:"fill"` handles width.
- @-mention columns/divs **must** be `"data_type":"lark_md"` (a `text` column will not render `<at>`).
- Celebratory emoji throughout (🎉🎊🏆🥇🥈🥉👏💪🎈) — required.

## Card structure (up to two tables in one card)
1. **Header** — turquoise banner, title e.g. `🎉🎊 Skill Hub 上新公告`.
2. **Opener `div`** (`lark_md`) — `<at id=all></at>` + a celebratory line + the hub version + the **repo link**
   `[📦 Skill Hub 仓库]({REPO_URL})`.
3. **Table ① 上新表** — columns: `Skill` · `分类` (category) · `简介` (summary) · `贡献人` (`lark_md`, `🏅 <at id=ou_xxx></at>（来源）`).
4. **`hr`** divider. *(part of the leaderboard block — omitted when the leaderboard is off)*
5. **Ranking heading `div`** (`lark_md`) — `🏆 Skill Hub 累计贡献排行榜`. *(leaderboard block)*
6. **Table ② 排行榜** — columns: `名次` (🥇🥈🥉 / 4. / 5. …) · `贡献人` (`lark_md`, `<at id=ou_xxx></at>`) · `累计贡献` (count) · `贡献内容` (items). *(leaderboard block)*
7. **Closing `div`** (`lark_md`) — 感谢 line, e.g. `👏 感谢贡献，让 Skill Hub 越来越强 💪🎈`.

> **Leaderboard is conditional** — elements 4–6 (the `hr` + ranking heading + Table ②) render **only** when the instance
> `skill_hub.announce.include_leaderboard` is true **and** the `contributor_open_id` map is non-empty. When off, drop those three elements;
> the card is then header + opener + Table ① + closing div. The skill body (`Procedure` step 3/4 + Rules) owns the gate.

## Placeholders (filled at runtime — never hardcode)
- `{VERSION}` — the released hub version (input).
- `{REPO_URL}` — the hub git repo URL, read from instance `skill_hub.announce.repo_url` (D10 addendum; decoupling: NOT
  hardcoded in this template).
- `{ROWS}` — Table ① rows: one per newly-added skill (skill / category / summary / `🏅 <at id=…>（source）`).
- `{RANKING}` — Table ② rows: contributors sorted by count desc, medals for top 3.
- `ou_xxx` open_ids come from instance `skill_hub.announce.contributor_open_id[label]` (resolved per contributor label
  from `contributors.yaml`).

## Template (skeleton — `{...}` are runtime fills)
```json
{
  "config": {"wide_screen_mode": true, "width_mode": "fill"},
  "header": {"template": "turquoise", "title": {"tag": "plain_text", "content": "🎉🎊 Skill Hub 上新公告"}},
  "elements": [
    {"tag": "div", "text": {"tag": "lark_md", "content": "<at id=all></at> 📣 Skill Hub 又添新货，欢迎试用！✨\n**🏷️ Skill Hub 版本：{VERSION}**　|　[📦 Skill Hub 仓库]({REPO_URL})"}},
    {"tag": "table", "page_size": 5, "row_height": "high",
     "header_style": {"text_align": "left", "background_style": "grey", "bold": true},
     "columns": [
       {"name": "skill", "display_name": "Skill", "data_type": "text"},
       {"name": "category", "display_name": "分类", "data_type": "text"},
       {"name": "summary", "display_name": "简介", "data_type": "text"},
       {"name": "contributor", "display_name": "贡献人", "data_type": "lark_md"}
     ],
     "rows": [ "{ROWS}" ]},
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
     "rows": [ "{RANKING}" ]},
    {"tag": "div", "text": {"tag": "lark_md", "content": "👏 感谢贡献，让 Skill Hub 越来越强 💪🎈"}}
  ]
}
```
(This is a field-tested card shape — the constraints above were derived from live send tests. `page_size` paginates a
table; keep it at/above the expected row count to show all rows.)
