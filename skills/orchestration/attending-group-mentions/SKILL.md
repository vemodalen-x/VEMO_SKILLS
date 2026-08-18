---
name: attending-group-mentions
description: >
  Staff a team group chat — when someone @-mentions the bot, read what they asked and reply to that need. Pull new messages by cursor (per-instance cursor file), filter for @bot mentions since last handled, triage the request (report / data / status / question / over-authority decision), serve what is serviceable (send a file or link as the bot, answer numbers ONLY by quoting the named ledger/report — never fabricate), reply to the asker with a post @-tag, in instance-policy Chinese (via polishing-chinese-prose). Decision-class requests escalate ("已转负责人" + @user), never auto-answered. Use to run group-chat attendance / answer @bot mentions on demand. Identity-decoupled — group id, bot/user identity, cursor + wordlist paths, open_id map are instance values.
allowed-tools: Read, Write, Bash
---

# Attending Group Mentions

Run **attendance on a team group chat**: whenever someone **@-mentions the bot**, read the request and reply to *that*
need. This is a **reactive, inbound-servicing** operation — it answers what people ask, in contrast to
`announcing-skills` / `publishing-deliverables`, which **proactively push** an outbound message. It operates on a group
chat, not on the skill hub, so it lives in `orchestration`, not `governance`.

> **What it is / is not.** It is a *responder*: pull new @mentions, triage, serve the serviceable, escalate the rest,
> leave a trace. It is **not** a free-roaming agent — it answers only when @'d, never volunteers messages, never sends
> a commitment. Every group id, identity, cursor path, wordlist path, and open_id is **read from the consuming
> project's instance** at runtime; this body hardcodes **none** of them.

## When to use
- A bot is a member of a team group chat and should **respond on demand** when colleagues @ it (ask for a report, a data
  file, a status, a number, or a question).
- Trigger phrases: "群里有人 @ 机器人", "值守群消息", "回复群里的 @", "attend the group chat",
  "answer @bot mentions", "群值守".
- **Not automatic / not a daemon** — run as a pass when prompted (or on the instance's schedule). One invocation
  processes the mentions accumulated since the cursor.

## Inputs (all instance-read; zero hardcode)
From the consuming project's instance (`project_profile.yaml`, e.g. a `group_attend` block):
- `group_chat_id` — the chat to attend.
- `send_as` (user | bot) + the send identity — who the reply is posted as.
- `cursor_file` — path to the **per-instance cursor** (last-handled message position / id). Instance asset, not in this body.
- `wordlist_path` — the instance term/jargon wordlist that `polishing-chinese-prose` enforces (黑话禁出).
- `user_open_id` (and any label→open_id map) — for the escalation @ and for resolving the asker.
- The **truth sources** it may quote: the named ledger / report artifacts (an instance list of what is quotable).

## Procedure

### Step 1 — Scan for new mentions (cursor-bounded)
- Read the **cursor** from `cursor_file` (last-handled message id / position). On a fresh chat, start from the
  instance-defined floor, not from the beginning of time.
- Pull messages with `lark-cli im +chat-messages-list --chat-id <group_chat_id>` (page forward from the cursor).
- Filter to **new @bot mentions** only: a message whose mention list contains the bot, with id/position **after** the
  cursor. Ignore the bot's own messages and already-handled ids.

### Step 2 — Triage each mention (oldest first)
Classify the request:
- **Report** — wants a deliverable/report → locate the artifact, send it (Step 3a).
- **Data** — wants a data file → send the file as the bot (Step 3a).
- **Status** — wants progress/state → answer from the ledger truth (Step 3b).
- **Question** — a factual ask → answer from a quotable truth source (Step 3b).
- **Over-authority decision** — wants a **commitment** (a deadline / a metric change / an external publish) → **do not
  answer it**; escalate (Step 4).

### Step 3 — Serve the serviceable
**3a. Send a file or link.**
- File: `lark-cli im +messages-send --as <send_as> --chat-id <group_chat_id> --file <path>` — the bot-identity
  `--file` send is the field-verified path. Link: post the URL in the reply body.
- Confirm the artifact exists and is the right one before sending; never send a placeholder.

**3b. Answer numbers — quote, never fabricate.**
- A numeric / factual answer is **quoted from a named ledger or report** (the instance's quotable truth source), with
  its **caveat attached** (measured value / license limitation / "as of <date>"). If the truth source does not carry
  the number, say so and escalate or defer — **never compute-to-satisfy** a request or invent a figure to look helpful.
- This is the integrity core: the value's *provenance* travels with it; a number without a source is not sent.

### Step 4 — Escalate over-authority requests
- For a **decision-class** request, **do not commit**. Reply "**已转负责人**" (handed to the owner) and **@ the user**
  (the instance's `user_open_id`) to transfer it. The skill never promises a date, changes a metric, or publishes
  externally on its own — those are human-owned decisions (an adoption gives standing authority to *answer* the
  serviceable classes, **not** to *decide*).

### Step 5 — Reply discipline (every reply)
- **Reply TO the asker** — the message **must @ the person who asked**. Because the reply carries an @, the message
  type is **`post`** (Markdown cannot @): the at element is `{"tag":"at","user_id":"ou_xxx"}` (resolve the asker's
  open_id). **This is the post form, NOT the card `<at id=ou_xxx></at>` form** — the two surfaces use different at
  syntaxes; a card `<at>` dropped into a post stays literal text. Send:
  `lark-cli im +messages-send --as <send_as> --chat-id <group_chat_id> --msg-type post --content '<post-json>'`.
- **Chinese style** — the reply prose goes through **`polishing-chinese-prose`** (full ruleset, 翻译腔 + 文牍腔) using
  the instance `wordlist_path`; **no jargon / 黑话 leaks** into a colleague-facing reply.
- **Numbers carry their caveat** (Step 3b) — measured / license-limited / as-of, inline with the figure.

### Step 6 — Advance cursor + leave a trace (per-message)
- **Advance the cursor only AFTER the mention is successfully handled, one message at a time** — never per-batch. A
  mid-run crash must leave unhandled mentions unprocessed (picked up next pass), not skipped; **re-running over the
  same cursor must not re-send** (idempotent on the handled id). This is the resumable, per-item-checkpoint discipline.
- **Record one ledger line per response** in the consuming project's `flow_log.md`: **who asked / what was answered /
  the file or link sent** (and "escalated" for decision-class). The trace is the durable record of the attendance pass.

## Rules
- **Reply to the asker, always** — a reply that doesn't @ the asker is incomplete; the @ forces `post` (not card, not
  plain markdown).
- **No fabrication** — numbers are quoted from a named source with caveat; absent a source, say so, don't invent.
- **Escalate decisions, never commit** — deadline / metric / external-publish requests go to the user, not auto-answered.
- **Outward-facing** — a group reply is outward; the serviceable classes are pre-authorized by adoption, but if a
  request is ambiguous between serviceable and decision-class, **escalate rather than guess**.
- **Decoupling red line (skill_spec §9)** — group id, identities, cursor path, wordlist path, open_id maps, and the
  quotable-source list are **instance-owned**; this body hardcodes none. The two real-chat ids / names are instance data.

## Never touched
- A **decision** (a commitment, a metric, an external publish) — escalated to the human, never made here (decision
  ownership is a human red line).
- The instance values (`group_chat_id` / `cursor_file` / `user_open_id` / `wordlist_path`) — read, never written by
  this skill (the cursor file *content* is advanced as state, but its path + identity facts are instance-owned).
- Skill **adoption** into a toolset (skill_spec §6 user-consent red line) — unrelated; this skill staffs a chat, it
  does not adopt anything.

## Boundary
- **vs `announcing-skills` / `publishing-deliverables`** — those are **proactive outbound** pushes (announce a release /
  publish a deliverable) on a schedule/trigger the *sender* owns. This is **reactive inbound servicing** — it speaks
  only in reply to an @mention, and to the asker. Shared send mechanism (lark-cli, `send_as`, identity preconditions);
  different direction and surface (`post` reply with an at-tag, not an interactive card).
- **Chinese-prose authority** is `polishing-chinese-prose` (cited by name); this skill does not restate prose rules.

## References
- Reuses the **send mechanism** documented for `announcing-skills` (lark-cli `im +messages-send`, `send_as`, identity
  preconditions). The **at-tag form differs by surface**: this skill replies with **post** `{"tag":"at"}`; the
  announce skills build a **card** `<at id=>` — see `announcing-skills/references/card-format.md` for that distinction.
