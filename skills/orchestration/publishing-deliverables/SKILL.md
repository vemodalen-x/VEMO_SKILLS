---
name: publishing-deliverables
description: 'Publish a project deliverable (proposal / research report / experiment report / design doc) to the project''s Feishu (Lark) wiki as a clean technical-report-styled document — tables and flowcharts for structured info. Use when a stage produces a deliverable that should be filed to the team Feishu wiki. Owned by Framework 0 (orchestration); style is constrained by ml-paper-writing + the local style spec.'
---

# Publish Deliverable to Feishu

Turn a project deliverable into a technical-report-styled Feishu doc under the team wiki node.
Style is constrained by the `ml-paper-writing` skill (structure, argument, citation discipline) plus the
local style spec `references/technical-report-style.md` (borrowed from Vale's "style-as-rules" idea).

## When to use
- A stage (research / data / training / algo / deploy) produced a deliverable (方案 / 调研结果 / 实验报告 / 设计) to file to the team wiki.
- Trigger phrases: "发飞书", "publish to Feishu", "归档到 wiki".

## Inputs
- deliverable `type` (proposal | research | experiment | design), `title`, and `content` (path or text).
- deliverable **domain** (declared by the owning task; one of the instance `paths` keys).
- target Feishu wiki node: **domain-routed** — `project_profile.yaml -> deliverables.paths[domain]`
  (instance value). If the domain has no mapped path, fall back to `deliverables.feishu_wiki_root`
  (= `deliverables.routing.fallback`) **and flag it** (per task_spec §2 "Domain-routed publishing").
  Path partition ≠ framework partition. Domain names are whatever the instance `paths` defines.
- reviewer notification config: `project_profile.yaml -> deliverables.notify` (instance value) —
  `send_as` (user|bot), `group_chat_id`, `roles` (role → reviewer open_ids), `domain_reviewers` (domain → roles to @).
  **Everything is read from instance; hardcode no id / chat / name in this skill (decoupling red line, skill_spec §9).**

## Procedure
1. **Apply style (generation)**: follow the `ml-paper-writing` discipline to shape the deliverable into a
   technical report (clear structure, evidence-backed claims, verified citations); then check it against
   `references/technical-report-style.md`.
2. **Build doc content (XML)**: title + a summary callout; use **tables** for comparisons/specs and
   **`<whiteboard type="mermaid">`** for flows/architectures (per lark-doc rules). Cite sources; tag every
   data claim as 实测 / 文献 / 推测.
3. **Publish via lark-doc**: first read `../lark-shared/SKILL.md` + the lark-doc references, then
   resolve the target node = `paths[domain]` (root fallback + flag if unmapped), then
   `lark-cli docs +create --api-version v2 --parent-token <paths[domain]> --content "<xml>"`; fill sections via
   `block_replace` if a skeleton was created first.
4. **Record**: write the doc URL into the owning task's flow-ledger entry and the deliverable's domain folder.
5. **Notify reviewers (lark-im)**: after a successful publish, read `deliverables.notify` from the instance.
   - **Resolve recipients**: `roles = notify.domain_reviewers[domain]`; for each role gather its open_ids from
     `notify.roles[role]`. **Drop roles whose list is empty** (unassigned → skip, leave blank — never error).
     A role whose value is the literal `@all` → use the group "@所有人" mention.
   - **Compose** a message in the instance's outward-deliverable language as a **post**: title + 简介 + 路径（域名）
     + 链接 + an `评审：` line.
     ⚠️ **@ mentions only work in `post` format, NOT `--markdown`** (markdown wraps everything in one `md` tag and
     `<at…>` stays literal text). Build a post payload `{"<lang>":{"title":…,"content":[[…lines…]]}}` where the
     评审 line uses **`{"tag":"at","user_id":"ou_xxx"}`** per resolved reviewer (use `"user_id":"all"` for @all),
     interleaved with `{"tag":"text","text":"  "}` spacers; links use `{"tag":"a","text":url,"href":url}`.
   - **Send** to `notify.group_chat_id` using identity `notify.send_as`:
     `lark-cli im +messages-send --as <send_as> --chat-id <group_chat_id> --msg-type post --content '<post-json>' --idempotency-key <deliverable-id>`.
     Note: `--content` does **not** accept `@file` — inline the JSON (e.g. shell `--content "$(cat tmp.json)"`).
   - **Identity preconditions** (surface, don't fail silently): `send_as: user` needs scope `im:message.send_as_user`
     (if missing, emit the auth link and pause the notify, keep the publish); `send_as: bot` needs the app bot to be a
     group member (else "Bot can NOT be out of the chat").
   - **Record** the notification (group + @'d reviewers) in the task flow-ledger.

## Rules
- **Language**: deliverable body language follows the **project language policy** (instance-owned). See
  `references/technical-report-style.md` R13, which reads the policy from the instance; if the policy assigns
  Chinese to outward deliverables, the **`polishing-chinese-prose`** skill is the Chinese-prose authority (its
  翻译腔 band R14–R20 applies to the body). The skill hardcodes no language — it reads the instance switch.
- Style is constrained, not free-form: every published deliverable follows the style spec.
- Diagrams via native Feishu whiteboard (mermaid); structured data via tables — not walls of text.
- The wiki path is **domain-routed** and instance-owned (`project_profile.yaml -> deliverables.paths[domain]`);
  never hardcode a node token elsewhere. Unmapped domain → root fallback + flag.
- Publishing is outward-facing — confirm with the user before creating/overwriting when unsure.
- **Notify after publish**: every successful publish notifies the deliverable domain's reviewers in the team group
  (summary + link + @). Recipients/group/identity are instance-owned (`deliverables.notify`); unassigned role → skip.
  The notification is outward-facing too — same confirm-when-unsure rule.
- **Decoupling (skill_spec §9)**: this body is generic; all project values (wiki paths, notify config, language
  policy/activation) are read from the business-repo instance at runtime. Zero hardcode.

## References
- `references/technical-report-style.md` — generic report style rules: R1–R13 content (Vale concept) +
  R21–R28 presentation/scannability (Microsoft Style Guide "Scannable content" CC-BY-4.0; R26 Google dev-docs).
- Chinese-prose style is **not** a reference of this skill — it lives in the standalone **`polishing-chinese-prose`**
  skill (cited by name as the authority): 翻译腔 band R14–R20 (instance-activated) + 文牍腔 band R33–R39 (agent-layer
  always-on). Do not relative-path into another skill; refer to it by name.
- `references/readme-style.md` — **entry-document** style module R29+ (repo README / onboarding; standard-readme
  section-checklist, MIT). Physically separate from R1–R28: README rules and report-body rules do not cross-apply.
