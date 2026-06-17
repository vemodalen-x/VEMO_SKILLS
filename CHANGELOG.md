# Changelog · VEMO_SKILLS (shared skill home)

> Template-owned generic skill bodies. Semver, PR-merged + tagged like framework repos.
> Project-specific values never live here — they live in the business-repo instance.

## [1.0.0] — 2026-06-17

### Added
- Independent `VEMO_SKILLS` Git repository, rebuilt from the shared skill-home source as a public upload-ready
  artifact.
- VEMO-style executable surface: `bin/vemo-skills`, `tools/vemo_skills_check.py`, and `eval/run.py`.
- Release scoring threshold: `>= 9.5/10`, covering catalog parity, frontmatter, naming, references, regen binding,
  version hygiene, public docs, security decoupling, executable verification, and attribution governance.
- Public release docs: `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `docs/INDEX.md`, `docs/QUICKSTART.md`,
  `docs/CRITIQUE_LOG.md`, and the Wildskills/VEMO_SKILLS assessment reports.
- Task record `tasks/T-20260617-vemo-skills-release.md` for the first complete-version pass.

### Changed
- Public identity normalized to `VEMO_SKILLS`; repository-local examples use `.governance/VEMO_SKILLS`.
- The `publishing-skills` README-style reference now points to the concrete shared reference module path.
- `contributing-framework-changes` frontmatter now includes an explicit when-to-use cue for skill auto-invocation.

## [0.19.0] — unreleased (contrib PR)

### Added — new category `visualization/` + skill `visualizing-processing-pipelines`
- **First skill in a new `visualization/` category** (declare-and-create): renders a multi-step processing
  pipeline (image / data / ML) into one **self-contained HTML report** — per-stage before/after drag-to-compare
  slider, diff heatmap, inline base64 images, what/why/formula annotations, timing bars, pass/fail metrics.
- Ships a pipeline-agnostic **numpy+opencv builder** under `references/scripts/viz_report.py` (static `.html`
  mode + an interactive parameter-slider HTTP-server recipe in `references/design-patterns.md`) plus a runnable
  `references/examples/minimal_example.py` demo.
- Boundary: render/explain aid — the caller drives the builder, it does not run the pipeline; compare & diff
  need same-size BGR-uint8 pairs; base64-inline so large frames downscale via `display_width`. Distinct from
  `orchestration/rendering-html-eval-reports` (eval/training metrics) — this explains pipeline stages.
- Lockstep: README/README_zh Layout line, Skill-Catalog row, keyword-trigger row.

## [0.18.0] — 2026-06-12 (release train: PR #1 #2 #3 #4 #5 #6 + T044/T047)
> The Friday release train folds six merged PRs plus the T044/T047 commit (c0811b8, which bumped `VERSION` to
> 0.18.0 but missed its CHANGELOG section — backfilled below at release) into one version. New skills:
> `code/validating-on-device-inference`, `code/gating-tflite-op-envelopes` (T047), `code/bumping-library-versions`,
> `orchestration/attending-group-mentions`, `orchestration/packaging-device-sdk-releases`.

### Added — backfill for c0811b8 (T044 + T047, recorded at release)
- **T044**: optional 🏆 contribution **leaderboard on both announce skills** — `announcing-skills` gains an
  `include_leaderboard` instance gate; `announcing-framework-releases` design-reversed to carry the same optional
  leaderboard (single hub ledger, reuses `skill_hub` maps); merged-PR-only counting lines.
- **T047**: new skill **`code/gating-tflite-op-envelopes`** (generalized `envelope_gate.py` as a reference tool;
  repeatable `NAME=VERSION` envelopes; fail-closed; THIRD-PARTY tflite line).
- **CONVENTIONS §7**: PR-only / weekly Friday official release train / merged-PR-only contribution counting.

### Changed — `governance/polishing-chinese-prose`: new 文牍腔 rule R39 (P-23)
- **R39 — no self-coined concept-terms / metaphor-as-jargon in human-facing output.** Sits one level above R34
  (which bans self-coined *abbreviations*); R39 bans self-coined *concept words* and *metaphor-as-term*. Three clauses:
  (1) describe the phenomenon in plain words **before** naming it; (2) if you name it, the name is **immediately
  followed by a one-sentence definition**; (3) a metaphor borrowed from physics/math/medicine may aid understanding
  but **must not be reused as a formal term** without flagging it as a figure of speech. **Scope**: every human-facing
  output (user messages, reports, broadcasts); **agent-to-agent internal comms are exempt** (the always-on 文牍腔
  activation class). **Decoupling (A3 / `skill_spec` §9)**: the rule lives here; any **project term-mapping table**
  (banned-form → standard-form) is an **instance asset** and is **not** recorded in this repo — R39 carries only
  **de-projectified illustrative examples** (e.g. a coined "X 病" / an un-expanded "X-3" used as a concept), no project
  glossary entries.
- Lockstep: band heading `R33–R38`→`R33–R39`, frontmatter `description:`, the dual-activation-class line, the
  provenance footer, README/README_zh Skill-Catalog rows, the `publishing-deliverables` SKILL.md + `technical-report-style.md`
  cross-cites, and the `THIRD-PARTY-NOTICES.md` scope-note heading — all moved to `R33–R39`. No prior rule changed;
  R-numbers retained so existing by-number cross-cites stay valid.

### Changed — `orchestration/rendering-html-eval-reports`: training-experiment / ablation report variant (P-19)
- The skill rendered **evaluation** reports only; it now also renders a **training-experiment / ablation** report type,
  sharing the same self-containment, provenance-header, privacy, and interface-language rules. The new variant adds:
  an **experiment-ladder table** (per round: variable / hypothesis / result / verdict), **inline training curves**
  (base64, single-file), an **ablation comparison table**, **per-figure measured-vs-inferred labelling**, and a
  **consolidated limitations section**. New generic rule **R6 — measured-vs-inferred labelling**: every reported number
  is marked as **measured** or **inferred/estimated**; an unlabelled number is rendered with a visible marker rather
  than passing as measured. Skeleton markup added to `references/html-template.md` as a **parallel training-report
  skeleton** (the eval skeleton is unchanged). Fully de-projectified — zero project vocab; the report type is a
  general paper-style structure (abstract / method / setup / results / ablation / limitations).
- **Scope note for review**: the skill keeps its name `rendering-html-eval-reports` (renaming would trip the
  `naming-skills` gate + catalog-token churn — out of scope); training-report is framed as a **second report variant**
  under the same skill. The broadened scope is surfaced here for the lead's ratification rather than silently widened.
- Lockstep: rule count `R1–R5`→`R1–R6` (SKILL.md "five rules" → "six rules"), the two report-type variants documented
  in SKILL.md sections + README/README_zh Use-via-Prompt prose.

> Source: P-01 device-window (user-pointed; idea contributed by Shen Shanlan — the on-board acceptance need surfaced when
> the target device came online). Skill drafted on a PR branch; **VERSION not bumped** until the lead's release gate
> tags it. Distilled from the real on-board acceptance run, then **fully de-projectized** (skill_spec §9 / A3): no device
> model, no model file, no sha, no threshold, no gesture/task vocabulary survives — each is a caller-read parameter.
### Added
- **New skill `code/validating-on-device-inference`** — a **device-runtime acceptance** methodology checklist: push the
  converted package to the device → run → collect results + logs, then judge on two axes with **consistency outranking
  performance**. **Block 1 (consistency, runs first):** (1a) known-answer check — elementwise `max|Δ| ≤ caller tol` +
  **argmax agreement N/N** (a scrambled input plumbing shows as large Δ — this block proves the device feed is faithful);
  (1b) low-precision **budget judged in softmax/decision space, NOT raw logit** (the decision lives in probability space,
  so a "large" logit drift can still PASS); (1c) **canary headroom = margin ÷ observed device deviation**, with the
  portable caveat that **absolute margin is not cross-comparable across golden sets of different sizes — the ratio is**.
  **Block 2 (performance, only after Block 1 PASSES):** warmup rounds separated from timing rounds, latency reported as a
  **distribution (not a single shot — thermal drift)**; delegate **on/off each measured AND consistency re-verified under
  the delegate** (an accelerated wrong answer is still wrong); **power as a labelled proxy** (CPU/freq/temp, explicitly
  "not measured power"). Plus push/single-writer discipline (own `/data/local/tmp/<dir>`), log filtering + exit-code /
  crash fallback, and a **PASS/FAIL report-row block** to feed an upper-layer acceptance. **Read/measure-only** — does
  not convert, retrain, edit code, or adopt. **Reuse-not-reinvent**: recommends the upstream TFLite benchmark binary for
  the timing-round collection (a recommendation, not a vendored import — no THIRD-PARTY row). **Boundary**: static
  op-envelope gating is the **pre-device** portability check; this is the **device-runtime** correctness+speed check;
  mobile-GPU conv selection is **design-time**, this is **acceptance-time**. **Decoupled (skill_spec §9)**: device handle,
  package, tolerances, latency gate, budget, canary, and device directory are all instance-read — zero hardcoded project
  values. Idea contributed by Shen Shanlan (user-originated).

### Changed — `code/validating-on-device-inference`: weak-substitute-platform extrapolation rule (T052)
- Block 2 (latency, §2a) gains a **weak-substitute-platform extrapolation** rule for when the timing was measured on a
  platform **weaker** than the ship target — an asymmetric, conservative-proxy reading: **passes the gate → directional
  PASS** (the stronger target is at least as fast, gate holds with margin); **fails the gate → inconclusive / target
  re-test required, NOT a hard FAIL** (a weaker platform missing the gate does not prove the target misses it);
  **thin-margin caveat (hard)** — when the pass margin is thin (e.g. **< ~20%** of the gate, caller-set), the directional
  PASS is fragile (platform delta / thermal drift erases it) → **discount it and annotate "target platform must be
  measured"**. Every latency number is **tagged with the platform** it was measured on (target vs substitute) — the R6
  measured-vs-inferred posture (a substitute-platform number is *inferred* for the target). Field lesson (T052): a
  171ms/200ms-style thin pass on a weaker platform is not a clean ship signal. Lockstep: §2a checklist, the Block 4
  `latency.pXX` report row, a Common-traps entry, the frontmatter `description:`, and README/README_zh catalog rows. No
  prior rule changed; **fully de-projectized** (the < ~20% threshold + platform identities are caller-set; no project
  device/number baked in).

> Source: user-pointed (idea contributed by Shen Shanlan). Name **`attending-group-mentions`** (the lead's candidate;
> `answering-` was rejected as too Q&A-narrow — the skill also sends files and escalates). Category **orchestration**
> (operational Feishu-send sibling of `publishing-deliverables`, NOT governance-meta — it staffs a chat, it does not
> operate on the hub). Drafted on a PR branch; **VERSION not bumped** until the lead's release gate tags it. Distilled
> from real group-attendance practice, then **fully de-projectized** (skill_spec §9 / A3): no chat id, open_id, contact
> name, or model survives — each is a caller-read parameter.
### Added
- **New skill `orchestration/attending-group-mentions`** — staffs a team group chat **reactively**: when someone @s the
  bot, read the request and reply to that need. Pull new messages by **cursor** (`lark-cli im +chat-messages-list`;
  cursor file = per-instance asset), filter @bot mentions since last handled, **triage** (report / data / status /
  question / over-authority **decision**), then: **serve the serviceable** — send a file/link as the bot
  (`im +messages-send --file`, field-verified), or **answer numbers ONLY by quoting a named ledger/report with its
  caveat attached** (measured / license-limited / as-of) — **never fabricate / compute-to-satisfy**; **escalate
  decision-class** (commit a deadline / change a metric / publish externally) with "**已转负责人**" + @user, never
  auto-answered. **Reply discipline (every reply):** must **@ the asker**, which forces message-type **`post`**
  (Markdown cannot @) using the at element `{"tag":"at","user_id":"ou_xxx"}` — **NOT** the card `<at id=>` form (the two
  surfaces differ; a card `<at>` in a post stays literal); Chinese prose via **`polishing-chinese-prose`** (full
  ruleset + instance wordlist, 黑话禁出); numbers carry their caveat inline. **Cursor + trace:** advance the cursor
  **per-message, only after a mention is successfully handled** (not per-batch — a mid-run crash leaves unhandled
  mentions for the next pass, and a re-run over the same cursor must **not** re-send — idempotent on the handled id),
  and record **one `flow_log.md` line per response** (who asked / what was answered / file or link / "escalated").
  **Reactive inbound-servicing** — replies only when @'d, only to the asker; **distinct from** `announcing-skills` /
  `publishing-deliverables` (proactive outbound push); shares their send mechanism (lark-cli, `send_as`, identity
  preconditions), differs in direction + surface. **Read/Write/Bash** — invokes lark-cli (an invoked tool, not a
  vendored library → no THIRD-PARTY row); ships no helper script (pure methodology). **Decoupled (skill_spec §9)**:
  group id, bot/user identity, cursor-file path, wordlist path, open_id map, and the quotable-source list are all
  instance-read; zero hardcoded project values. Idea contributed by Shen Shanlan (user-originated).
> Source: P-? SDK-release (user-pointed; idea contributed by Shen Shanlan — surfaced packaging the first device SDK
> release). Skill drafted on a PR branch; **VERSION not bumped** until the release train tags it. Distilled from the
> real first-release packaging, then **fully de-projectized** (skill_spec §9 / A3): no library name, no release version
> digits, no model/platform/group survives — each is a caller-read parameter (the first release version is a specific
> value that lives in the instance, never here).
### Added
- **New skill `orchestration/packaging-device-sdk-releases`** — assembles a built algorithm library into a deliverable
  **mobile SDK release package**, and **composes** other skills rather than restating them. **§1 Version** — the release
  version is **assigned by `code/bumping-library-versions`** (referenced, not restated — single source for the version
  rule); packaging **consumes** the resulting string for the package name + `RELEASE_NOTES` and **verifies** the three
  surfaces agree at pack time (§5). **§2 Layout** — `include/` (minimal public headers) ·
  `libs/<abi>/` · `models/` (each **license-annotated**) · `docs/RELEASE_NOTES` (version · capability list with each
  number's 口径 · API quick-table · known limits) · `docs/USAGE.md` (init→feed→get→release how-to + minimal snippet +
  FAQ) · `examples/` (a **compilable** minimal call example; build command in its top comment) · `THIRD_PARTY` (the
  **package's** notices, distinct from this repo's `THIRD-PARTY-NOTICES.md`). **USAGE + examples are written against the
  shipped headers — inventing a non-existent API is a FAIL; the example must compile against the package** (verified in
  §5). **§3 License annotation (hard)** — a model whose training data is license-restricted MUST be
  conspicuously marked with its usage boundary, or it is a packaging FAIL. **§4 Two ship-along reports** — quality via
  **`rendering-html-eval-reports`** (cited, not re-spec'd; inherits its R6 measured-vs-inferred) and performance via
  **`validating-on-device-inference`** (latency distribution / power proxy / platform annotation), **plus the memory =
  system-delta method this skill OWNS** (algo OFF vs ON, sample system-available + process PSS, take the steady-state
  delta across rounds — distribution not single-shot; the validation skill does not cover memory); non-target-platform
  numbers are header-flagged (R6 posture applied to perf). **§5 Verification** — manifest + per-key-artifact sha +
  unpack-reverify + version-agreement recheck + **example-compiles** + a **capability↔binary consistency gate** (every
  `RELEASE_NOTES` capability claim must trace to a real path/symbol in the **shipped** library, not a stub/placeholder
  build — a claim that cannot be pointed to in the binary is a FAIL; T052 field lesson: a stubbed `.a` cannot produce
  the claimed numbers). **§6 Boundary** — **packaging ≠ releasing**: the skill ends at a verified
  package; the **outward send is a human/lead decision** (same boundary `announcing-skills` / `attending-group-mentions`
  honor). **Composition over duplication**: the SKILL.md enumerates borrowed (eval-report, on-device-validation,
  outward-send boundary) vs owned (version scheme / layout / license-annotation / memory-delta / verification).
  **Read/Write/Bash** — zip/sha/unzip are invoked tools, not vendored libraries → **no THIRD-PARTY row**; ships no helper
  script (pure methodology). **Decoupled (skill_spec §9)**: `lib_name`, version digits, platform, group, model-license
  facts, and report source data are all instance-read; zero hardcoded project values. Idea contributed by Shen Shanlan
  (user-originated).

> Source: user-pointed split (the user asked that version management be its **own** skill, not a section of the packaging
> skill). Lands on the **same PR branch** as `packaging-device-sdk-releases` (one PR, two skills). Drafted on a PR
> branch; **VERSION not bumped** until the release train tags it. Generalized from a consuming project's release
> convention, then **fully de-projectized** (skill_spec §9 / A3): no library name, no version-field constant name, no
> source-file path survives — the version-field name + file are caller parameters.
### Added
- **New skill `code/bumping-library-versions`** — owns the **library version rule**, referenced by
  `packaging-device-sdk-releases` (single source). **Shape** — four-segment `X.Y.Z.W`. **Single source → three agreeing
  surfaces**: a source string constant, the init-log line, and a `getVersion()` API — all must read the same string
  (mismatch = FAIL). **Bump policy** — W (last) = bug-fix `+1`; Z (penultimate) = feature `+1` and **reset W to 0**;
  both-in-one-release = Z `+1` and reset W to 0; **X.Y (first two) = human-set only**, never auto-bumped; earlier
  segments stay on a W/Z bump. **Precondition (hard)** — the **acceptance build+run has already passed** (a version
  asserts "this built and passed"; bumping before acceptance lies about the artifact — if not passed, **stop**). After
  bumping, **report old → new explicitly** with the reason. **Read/Edit/Bash** — edits the caller-specified version
  field; does not run/judge acceptance (it depends on acceptance having passed). **Decoupled (skill_spec §9)**: the
  version-field name, the source file, and the library name are **caller-specified** — generalized from a consuming
  project's release convention, zero project names embedded. Idea contributed by Shen Shanlan (user-pointed — split into
  its own skill).
- **Category — `code` (lead-ruled).** Placed in `code` on the **domain** axis (a library's version is a code /
  deploy-domain concern — where its users look), which takes precedence over the incumbent "all `code` skills are
  read-only" convention. It is the **first write-action skill in `code`**, surfaced as an **explicit boundary
  annotation** (SKILL.md Boundary + catalog rows): it **writes ONLY the version constant / log line, no logic** — the
  exception is declared, not silently taken.

## [0.17.0] — 2026-06-11 (T042)
> Source: T042 (user-approved; name **`rendering-html-eval-reports`** ratified by user, category **orchestration** ruled
> by team-lead — sibling of `publishing-deliverables` as a stage-output producer, no new category). Idea contributed by
> Shen Shanlan (user-originated). Independent minor per release-train discipline; stacks on 0.16.1 (T041, same release
> train — 0.16.1 is T041's uncommitted change, last repo tag is v0.16.0; commit order T041(0.16.1)→T042(0.17.0), the
> lead's version gate).
### Added
- **New skill `orchestration/rendering-html-eval-reports`** — renders **pre-computed** evaluation results into a
  **single self-contained HTML report** (CSS inlined, images base64-embedded). Sections: a **mandatory provenance
  header** (data version / model sha / runtime / date), a **per-class accuracy table** vs an instance-supplied
  acceptance threshold, a **confusion matrix including the abstain/rejection column** (abstention rate surfaced as a
  headline metric), a **sample gallery** (R2 asymmetry: **all** error cases with predicted labels + overlays, correct
  ones **sampled**), and a **latency distribution with its caller-supplied caveats**. **Render-only** — consumes
  metrics, does not run inference or compute them. **Image-input contract**: the caller supplies each image **already
  de-identified and base64-encoded** (`data:` URI); the skill (`Read, Write`) inlines it and never touches raw image
  bytes — a privacy-hardening so a raw frame cannot leak through the skill. Five generic rules (R1 provenance-mandatory
  / R2 all-errors-sampled-correct / R3 abstain-class-first-class / R4 latency-carries-caveats / R5 privacy-and-destination). Ships
  `references/html-template.md` (markup skeleton + inline CSS + per-section render rules) inside the skill folder.
  **Decoupled (`skill_spec` §9)**: class set, acceptance threshold, latency caveat text, provenance values, privacy
  policy, and the **report-interface language** (project language policy; the English strings in the template are a
  placeholder — **data keys like class ids / sha / version strings stay verbatim, never translated**; Chinese interface
  text defers to `polishing-chinese-prose`; non-ASCII interface text requires a **UTF-8 source file + `charset=utf-8`**,
  and a compiled emitter must set **UTF-8 source encoding explicitly** (e.g. MSVC `/utf-8`) or it mojibakes off-machine —
  a T037 field lesson) are all instance-read; zero hardcoded project values. **Distinct from
  `publishing-deliverables`** (Feishu wiki doc publish): this renders a local self-contained HTML artifact (not
  committed to git); the two compose but are different functions.
- `README.md` / `README_zh.md` — Skill-Catalog row, `orchestration/` layout line, a Use-via-Prompt entry, and a
  Keyword-triggers row added in lockstep (R32 bilingual pair).
- `contributors.yaml` — `rendering-html-eval-reports` contribution recorded under **Shen Shanlan** (idea attribution,
  same precedent as `polishing-chinese-prose`).

## [0.16.1] — 2026-06-11 (T041)
### Changed (docs — README_zh prose only; no rule change)
- `README_zh.md` — rewrote the first-principles block into natural spoken Chinese per `polishing-chinese-prose`
  (R33–R38, this hub's own skill — first enforcement on this repo); colloquialized the axiom Chinese names to the
  user-ratified set (A3 通用归通用，项目归项目 / A4 改不回来的事，人来拍板; A1 说做完不算，验过才算 & A2 以文档记录为准 marked
  n/a), and scrubbed narrative 账本→记录/名册. Meaning unchanged; EN untouched.

## [0.16.0] — 2026-06-11
> Source: T036 (user-approved, form ruled by user: the Chinese-prose rules are **promoted from an embedded reference
> module to a standalone skill `polishing-chinese-prose`**, category `governance`). Independent minor per release-train
> discipline; shares the user gate with 0.15.0 (T035) but tag + CHANGELOG entry stay separate. Supersedes the earlier
> embedded-module form of T036 (no separate prior entry — this is the single landed change).
### Added
- **New skill `governance/polishing-chinese-prose`** — the **canonical Chinese-prose authority**, holding **all**
  Chinese-prose rules self-contained (no cross-skill reference paths): the **翻译腔 band R14–R20** (active voice, no
  vague modifiers, sentence-splitting, unambiguous pronouns, consistent terminology, 的/地/得, consistent persona) +
  the **new 文牍腔 band R33–R38** (treating **bureaucratese**, the user's "不是人话" complaint): **R33** 动词优先于名词串
  (no noun-stacking; 余光中《中文的常态与变态》framing) · **R34** 自造缩略语禁用 + a preserve-vs-replace seed table
  (盘验→我查过了 …; proper nouns like Gate-2/pin/版本门 preserved) · **R35** ≤1 arrow-chain per paragraph · **R36** ≤1
  parenthetical per sentence · **R37** "念出来测试" as the governing check · **R38** term-preservation with human
  connective prose · plus the **EN→zh term table**. Rules derive from team **user-feedback** (contributor Shen
  Shanlan), not an external guide.
- **Two activation classes** (restated in the new skill's `SKILL.md`): R14–R20 (翻译腔) **instance-activated**
  (deliverable-language switch); R33–R38 (文牍腔) **agent-layer always-on**, applying to **any Chinese agent-dialogue
  reply** regardless of the switch — the skill is the *authority/spec*, the always-on carrier is the consuming
  project's memory. Applicability **explicitly names agent dialogue Chinese output**.
### Changed
- **Chinese-prose style now cited by name, not relative-pathed** — `publishing-deliverables` (SKILL.md Language rule +
  References), `technical-report-style.md` (Language R13 + Module), `readme-style.md` (R31 scope boundary + R32 zh-mirror
  rubric + its ownership sentence), `CONVENTIONS.md` (R32 fluency rubric + pointer), and `structuring-solution-docs`
  all point at `polishing-chinese-prose` **by name** as the authority (the by-name pattern `publishing-skills` uses for
  `naming-skills`). The README layout tree-diagram comment no longer lists `zh-prose` as a publishing-deliverables
  reference.
- **`README.md` / `README_zh.md` Skill Catalog** — added the `governance/polishing-chinese-prose` row (catalog now 16);
  `publishing-deliverables` row reworded (report style R1–R32; Chinese prose delegated by name).
- **`THIRD-PARTY-NOTICES.md`** — yikeke + 余光中 rows' "where used" repointed to the new skill location; scope note
  retitled. (余光中 = R33 framing only, idea-cited; the two reviewed GitHub guides stay out — nothing borrowed.)
- **`contributors.yaml`** — added **Shen Shanlan** (feishu) for `polishing-chinese-prose`.
### Removed
- **`publishing-deliverables/references/zh-prose.md`** — deleted; its content moved wholesale into the new standalone
  skill. No rules lost; R-numbers retained (R14–R20 / R33–R38) so existing by-number cross-cites stay valid.

## [0.15.0] — 2026-06-11
> Source: T035 (user-approved; all three recommendations adopted — single 5-column catalog + relocated trigger
> sub-table, true bilingual mirror, curated-rows + completeness check; structured-frontmatter generation deferred as a
> flagged follow-up). Stacks on released v0.14.1 (T034). Does not touch the T034 First-Principles block.
### Added
- **README `## Skill Catalog`** (replaces `## Skills (role table)`) — one **structured row per skill** with
  **category as an explicit column** (was only a path prefix — the user-reported gap: "属于什么类别没说清"), plus
  **does / when-to-use / boundary**. The **skill** column keeps the `` `<category>/<name>` `` identifier token, so the
  existing §4 multiset diff (set-A extraction) is **unchanged**. Trigger keywords stay in the **Use via Prompt →
  Keyword triggers** sub-table (relocated, not removed) to keep the catalog readable — 3 scattered surfaces → 2 by
  design. Mirrored in `README_zh.md` (R32).
- **`publishing-skills` Step 5 — a 5th machine check (catalog completeness)**: **derived-equality** (category cell ==
  `category:`, skill token's name == `name:` — equality, not just non-empty, so the category column can't drift) +
  **curated-cell non-empty** (does/when/boundary) + **trigger coverage** (each prompt-triggered skill has a keyword-row).
  Runs on both READMEs. This gates *new* skill registration on a complete catalog row — governance, not a one-off edit.
- **`CONVENTIONS.md` §3** — a **Skill-Catalog row-format clause** (home-local, like the §9 product-front-matter
  convention — not a generic entry-doc rule, so it stays in CONVENTIONS, not `skill_spec`). Defines the columns,
  derived-vs-curated rule, token-preservation, and trigger-sub-table coverage; points at the Step-5 check as enforcer.
### Changed
- Lockstep wording: every "role table / role-table row" → "Skill Catalog / catalog row" across `README.md`,
  `README_zh.md`, `CONVENTIONS.md` (§0 lifecycle, §3, §4), and `publishing-skills` (Model, Step 4, Step 5). The
  multiset check keeps the `<category>/<name>` token, so only wording changed — its logic is identical.

## [0.14.1] — 2026-06-11 (T034)
### Changed (docs — README first-principles rewrite; no rule/skill change)
- `README.md` / `README_zh.md` — replaced the Why/Features opening with a **First Principles** block answering four
  questions (防什么 / which principles it lands / system position / honest gap), per the T034 ecosystem-wide rewrite.
  As a **shared mechanism** (not a gate-bearing/ledger-owning framework), A1/A2 are marked **n/a**; A3 (decoupling) is
  the primary principle, A4 (adoption consent) via `skill_spec` §6. Principle pointers only — no rule restated.
  Bilingual R32 parity. No skill body or version-gated rule touched.

## [0.14.0] — 2026-06-11
> Source: T033 (user-approved; name ruled `announcing-framework-releases`, message template approved, instance binding
> = a sibling `framework_announce` block). Stacks on released v0.13.0 (T031).
### Added
- **`governance/announcing-framework-releases`** — a governance-meta skill that announces a **framework version
  release** to the team chat as a Lark interactive card: framework name + code, old→new version, a **change-class
  summary** (Added / Changed / ⚠️ BREAKING / Fixed) **extracted** from the released framework's CHANGELOG top entry
  (render-don't-author), a deterministic **consumer-impact verdict**, and repo / CHANGELOG links + maintainer. The
  impact rule is **framework-agnostic**: ⚠️ BREAKING marker **or semver-major bump** → breaking; recognized
  non-breaking sections only → compatible; else → neutral (the semver-major fallback handles external frameworks whose
  CHANGELOGs don't use the ⚠️ marker, e.g. Wildpanda). Carries its **own** `references/card-format.md` (a change-class
  table + impact line — **no leaderboard**, distinct from `announcing-skills`' card). **Zero hardcode** (skill_spec §9):
  group + maintainer open_id are instance-owned (`framework_announce`, group reused from `skill_hub.announce`); repo /
  CHANGELOG URL is resolved at runtime from the submodule remote (the `syncing-frameworks` pattern). Triggers
  post-tag-verify; outward-facing confirm-before-send.
### Changed
- `announcing-skills` role-table + keyword wording clarified to **skill-hub 上新** (vs the new framework-release
  announce) — a boundary note so the two `announcing-*` skills read as distinct objects, not a collision.

## [0.13.0] — 2026-06-11
> Source: T031 (user-approved; name ruled `selecting-mobile-gpu-convolutions`). Stacks on v0.12.0 (T028).
### Added
- **`code/selecting-mobile-gpu-convolutions`** — a read-only advisory skill encoding **three measured heuristics** for
  choosing standard vs depthwise-separable convolutions on a mobile GPU (OpenCL / TFLite delegate): first-frame time ∝
  OpenCL kernel count (not FLOPs), warmup gain ∝ arithmetic intensity, steady-state time ∝ FLOPs ÷ GPU utilization. The
  portable part is the **proportionality**; every concrete number carries a measurement tag
  〔实测·张帆·dn_bayer_71 (standard) vs PMRIDv10 (separable), one denoising project〕 as **evidence, not fact**. Includes
  an explicit **heuristics-not-laws** preamble, **applicability + reversal conditions** (≤12ch / kernel-fusion can flip
  it), a **design-time + on-device dual checklist** (the on-device "measure to confirm" step is the safety mechanism for
  a thin-evidence heuristic), and a **boundary vs `optimizing-cpp-performance`** (GPU architecture choice vs CPU
  hot-path opt). No `allowed-tools` (pure advisory reasoning). **Zero hardcoded identity** (skill_spec §9): the Feishu
  group / image paths / open_id are not in the body; contribution credited as label `张帆` in `contributors.yaml`.
### Changed
- `code/` category re-described from "C/C++ source skills" → "code / deploy-domain skills" (README + README_zh layout
  line) — Framework-4 deploy domain spans code-review, CPU-perf, and now GPU conv-selection (user-approved scope).
- `reviewing-cpp-code` role-table duty line gains the spec-authority clause ("when the project mounts a coding spec,
  reviews against that spec as the authority") — closes the T028 advisory note (role row lagged the v0.12.0 body change).
- `optimizing-cpp-performance` role/keyword wording clarified to **CPU** (NEON/cache/multithread) to disambiguate from
  the new GPU conv-selection skill.

## [0.12.0] — 2026-06-11
> Source: T028 (user-approved; config-key reading (i) — explicit instance path-list). Built on v0.11.0 (T027).
### Changed
- **`reviewing-cpp-code`** — **behavior change** (minor): now **spec-bound**. New **Step 0** reads an instance-declared
  spec-source path-list (`coding.review_spec_sources`) and, when present, treats the mounted coding spec text as the
  **authority** — reviews the target code clause-by-clause and cites findings by the spec's own section / rule number.
  The generic Checklist is **demoted to supplementary** (fills only what the spec is silent on: compiler-warning
  analysis, signed/unsigned, SIMD alignment, truncation/overflow) with a no-double-report rule; with **no spec mounted
  it stays the full standard** (graceful fallback). New **§5 Comment-spec conformance (report-only)** reports per-function
  comment-field + signature conformance as findings but **does not** run the comment spec's read-trigger / blocking-gate /
  status-registry workflow (that is the implementing agent's obligation — the skill stays read-only). `description` updated
  to state the spec-authority behavior (still passes `naming-skills`: gerund name unchanged, ≤1024, keywords intact).
  **Zero hardcoding** (skill_spec §9): the skill names no framework / repo path / module — spec text is never copied in,
  only read at runtime and cited; the spec source is whatever the instance's `coding.review_spec_sources` points at.

## [0.11.0] — 2026-06-11
> Source: T027 (user-approved;映射表全收推荐, BLOCKING-1 取方案 (a)). **⚠️ BREAKING — all 12 skills renamed to
> gerund (verb+ing) form** + a new naming-governance skill. Pre-1.0, so a minor bump, but this is a
> **breaking rename**: every consumer's `.claude/skills/<name>/` folder names change and any `project_profile.yaml`
> `shared_skills.provides` / path references must be updated on the pin bump.
### ⚠️ BREAKING — skill renames (12, gerund form)
- `cpp-code-review` → **`reviewing-cpp-code`**; `cpp-perf-optimize` → **`optimizing-cpp-performance`**
- `framework-contribute` → **`contributing-framework-changes`**; `framework-sync` → **`syncing-frameworks`**
- `skill-announce` → **`announcing-skills`**; `skill-publish` → **`publishing-skills`**
- `governance-visualize` → **`visualizing-governance`**; `prd-breakdown` → **`breaking-down-prds`**
- `publish-deliverable` → **`publishing-deliverables`**; `decision-review` → **`reviewing-decisions`**
- `solution-doc-structure` → **`structuring-solution-docs`**; `thinking-partner` → **`challenging-assumptions`**
- All via `git mv` (history preserved); each `SKILL.md` `name:` updated to match its new folder; all cross-skill body
  refs, README/README_zh (role table · layout · mermaid labels · Use-via-Prompt · keyword table), `CONVENTIONS.md`,
  and `THIRD-PARTY-NOTICES.md` paths updated in lockstep.
### Added
- **`skills/governance/naming-skills/`** — a read-only validator for skill `name` + `description` against the
  authoring naming rules (name ≤64 / lowercase-digits-hyphens / no edge hyphen / **gerund** / folder-match;
  description non-empty / ≤1024 / what+when / keywords). Authority the home cites for skill naming; transcribed as an
  original checklist from the Anthropic skill-authoring naming rules (Datawhale ch.6 §1.1–1.4 rendering) — attribution
  + transcription-boundary scope note added to `THIRD-PARTY-NOTICES.md`. Contributor: Dong Runze (feishu) →
  `contributors.yaml`.
- **`publishing-skills`** — new **Step 0.5 naming gate** (runs `naming-skills` before placement; hard-fail blocks
  registration) + **Step 5 fourth self-check** (whole-tree naming conformance) + Model pointer to `naming-skills` as
  the naming authority.
- **`CONVENTIONS.md` §2** — naming-conformance pointer line (rule owned by `skill_spec` §9, authority = `naming-skills`).
### Changed
- The gerund-form naming convention is now a **hard rule** in this ecosystem (was an upstream *recommendation*);
  the spec-level clause lands in Wildmeerkat `skill_spec` §9 (separate bump). `contributors.yaml` historical `item:`
  fields (`cpp-code-review` / `cpp-perf-optimize`) left **unchanged** — they are a historical ledger; the leaderboard
  ranks by contribution count, not by current skill name.

## [0.10.1] — 2026-06-10
> Source: T024 (user-approved; Gate-1 closed 2026-06-10 via team-lead, D1–D6 ruled per recommendations). Docs +
> one cross-ref hardening — no skill / category / behavior change (patch). Built on v0.10.0 (`2ff7850`).
### Added
- `README.md` + `README_zh.md` — new **"Bootstrap via LLM"** subsection under *Getting started*: a copy-paste,
  zero-config English prompt (mirrored into both READMEs; surrounding zh prose translated, fenced block stays EN — D2)
  that a standalone consumer hands to an LLM to do the install end-to-end. **Executable + verify-bearing** (D3): submodule
  attach → per-folder regen → a bind-verify step that flags any skill whose `references/` did not land. States the regen
  rules once as the single source: copy each `skills/<category>/<name>/` **folder incl. `references/`**, flatten the
  category level, `.claude/skills/` is a gitignored artifact, meta skills not special-cased. Identity-decoupled
  (placeholder `<this-repo-url>`, no org/account). Closes the gap where *Getting started* step 2 named no concrete regen
  procedure for standalone consumers (it pointed at governed-project-only `Project_Init`/team-bootstrap).
### Fixed
- `README.md` *Getting started* step 2 (was: "regen copies all of `skills/**/SKILL.md`") — **omitted `references/`**,
  contradicting the folder-incl-references rule the new section requires; rewritten to "copies each
  `skills/<category>/<name>/` **folder** — `SKILL.md` **and** any `references/` — flattening the category level", plus a
  forward-link to *Bootstrap via LLM*. Mirrored in `README_zh.md`. (D6: only this site made a file-granularity claim; the
  other regen mentions are silent at a higher abstraction and were left untouched — incl. the `:91` mermaid, to avoid an
  `R29-render` must-pass liability for no correctness gain.)
- `skills/governance/framework-contribute/SKILL.md` README-check cite — was "the framework's **R1/R29** freshness
  obligation", which named two rules **neither of which is the freshness rule** (R29 = required-sections, R1 =
  report-body summary in `technical-report-style.md`; the actual README-freshness rule is **R30**). Hardened by-name per
  the GB4-01/T023 precedent → "the framework's **R29+ entry-doc freshness obligation** in `readme-style.md`, incl. R30
  README-freshness"; **R1 dropped** (report-body, out of README scope). Clears the ledgered backlog item (compliance INFO).

## [0.10.0] — 2026-06-10
> Source: T023 skill intake (user direct order; Gate-1 closed 2026-06-10 via team-lead, D1–D11 ruled). Contributions
> from the team Feishu group: 李程 (2 C++ skills) + 张文政 (11-rule 规约 list). Built on v0.9.1 (`a6d3ef4`).
### Added — new `code/` category (declare-and-create; first domain category, owned by Framework 4 / Wildpanda — skill_spec §7)
- `skills/code/cpp-code-review/` — C/C++ coding-standard + compiler-warning review with an embedded/DSP/image lens;
  read-only analysis. Generalized from a contributed body (project-specific "YUVHDR" wording evicted; technique catalog
  kept; domain focus is instance-supplied — skill_spec §9). `allowed-tools: Read, Grep, Glob`. 来源: 李程 (Feishu).
- `skills/code/cpp-perf-optimize/` — cache / ARM NEON / multithread optimization analysis; read-only, proposes code.
  Generalized (project "YUV/HDR" + "本项目使用 pthread" platform asserts evicted; target/threading instance-supplied).
  `allowed-tools: Read, Grep, Glob`. 来源: 李程 (Feishu).
- `references/embedded-cpp-rules.md` — generic embedded/SIMD rule module, carried **byte-identical inside each `code/`
  skill's own `references/`** (regen flattens category, so a per-skill copy is what survives — kept in parity).
  张文政's 11 rules folded with a **generic (A: G1–G9) vs toolchain (B: T1–T2) split** — toolchain rules
  genericized so the concrete VCS/NDK/`_WIN32` is an instance value, not a hardcode; per-rule `来源: 张文政` tags.
### Added — `governance/skill-announce` (cross-framework governance-meta skill, beside `skill-publish`)
- `skills/governance/skill-announce/` — post-release notify step: announces newly-registered skill(s) to a team chat as
  a celebratory Lark **interactive card** (上新表 + 🏆 cumulative contribution leaderboard). Identity-decoupled: group,
  send identity, **repo URL** (D10 addendum), and the contributor/PR→open_id maps are instance-owned
  (`skill_hub.announce`); ledger is hub-owned + identity-free. Card surface chosen for real tables; `<at>` syntax is
  card-specific (distinct from a `post` — kept separate in references to avoid cross-contamination).
- `skills/governance/skill-announce/references/card-format.md` — Lark card constraints + the field-tested v6 template
  (config `wide_screen_mode`+`width_mode:fill`; `row_height` low/middle/high only; never set column `width`; `<at>` only
  in `lark_md`; `{VERSION}`/`{REPO_URL}`/`{ROWS}`/`{RANKING}` placeholders).
### Added — contribution ledger (hub-wide fact)
- `contributors.yaml` — identity-FREE cumulative contribution tally (keyed by contributor label + item + source + date),
  the source the `skill-announce` 🏆 leaderboard reads. Seeded: 李程 ×2, 张文政 ×1. The label→open_id map for @-mentions
  stays instance-side (`skill_hub.announce.contributor_open_id`), keeping the hub ledger decoupled (skill_spec §9).
### Changed
- `README.md` — new `code/` layout line; role-table rows for `code/cpp-code-review`, `code/cpp-perf-optimize`,
  `governance/skill-announce`; Use-via-Prompt section for `skill-announce`; keyword rows for all three new skills.
- `CONVENTIONS.md` §1 — category-example set extended with `code/` (a domain category owned by a domain framework,
  skill_spec §7), still declare-and-create with no hardcoded enum.
- (GB-009 — D7 residue sweep, per GB4-01 precedent) entry-doc cross-refs to the README rule family hardened from a
  numeric range to by-name: `README.md` + `README_zh.md` standalone-note and `CONVENTIONS.md` §3 now read "the **R29+
  entry-doc family** in `readme-style.md` (incl. the R32 bilingual pair)" — drift-proof against a future Rn. Full-span
  *descriptor* cells (skill "carries R1–R32"; the `publish-deliverable` role-table cell) left numeric (correct, en/zh
  synced); `CONVENTIONS.md` §6 product-framing exclusion + §7 pointer-table `readme-style.md (R29–R32)` left numeric
  (file already named; range is a span descriptor, not a consult-pointer).

## [0.9.1] — 2026-06-10
> Source: T022 GB4-01 (R-range ceiling drift, post-batch entropy audit GB-004; user-approved Gate-1 2026-06-10 via team-lead, D7 by-name hardening + GB4-N2).
### Fixed (GB4-01 — stale R31 entry-doc ceilings after R32 introduction)
- `skills/governance/skill-publish/SKILL.md` — README-authoring pointer hardened from a numeric ceiling to a
  **by-name citation** ("the R29+ entry-doc family in `readme-style.md`, incl. the bilingual pair") — drift-proof; the
  stale "R29–R31" risked an author skipping R32 (the bilingual pair).
- `README.md` role-table descriptor `R1–R31` → `R1–R32` (aligned to the authoritative ceiling + its EN/zh siblings;
  by-name form misfits a full-range table cell, so numeric here — see receipt note).
### Changed (GB4-N2 — zh-prose scope alignment)
- `skills/orchestration/publish-deliverable/references/zh-prose.md` header — scope note now states the module also
  serves the **README zh-mirror semantic-fluency advisory** (R32 rubric, T021 D7), not only deliverable bodies.
- *Untouched (frozen history):* `CHANGELOG.md` [0.6.0] "R29–R31" — correctly records the pre-R32 state.

## [0.9.0] — 2026-06-10
> Source: T021 (VEMO_SKILLS standalone-output readiness — user-approved Gate-1 2026-06-10 via team-lead; D1 MIT / D2 VEMO_SKILLS Authors / D3 home-local front matter / D4 static badges / D5 arc42 CC-BY-SA scoped / D6 NOTICES / D7 zh-prose→R32 advisory rubric). Reference: Wildpanda v1.8.0.
### Added (standalone-output readiness)
- **`LICENSE`** (new, root) — **MIT**, `Copyright (c) 2026 VEMO_SKILLS Authors`. The repo's primary license for its own original
  work; the dominant inbound borrowing is also MIT.
- **`THIRD-PARTY-NOTICES.md`** (new, root) — attribution table for 7 borrowed sources across 3 licenses (standard-readme
  / MADR / markmap / yikeke-zh-style-guide = MIT; Microsoft + Google style guidance = CC-BY-4.0; **arc42 = CC-BY-SA**),
  + an arc42 scope note (section-skeleton + own prose → **not** an arc42 derivative; no repo-license constraint) +
  a pointer to the self-scoped vendored `thinking-partner/LICENSE` (MIT, mattnowdev).
### Added (Wildpanda-grade front matter — home-local, NOT a generic R-rule)
- `README.md` gains product front matter: centered title + tagline, **static badges** (license → in-repo `LICENSE`,
  version → `VERSION`, changelog; **zero org-pathed `shields.io` URLs** — identity red line), **Why** + **Features**
  sections, and a **"reading this repo two ways"** standalone-vs-governed note. Bare cross-repo citations
  (`skill_spec` / `Project_Init` / `team_bootstrap`) gain **degrade-gracefully** qualifiers (present in a governed
  project; not required standalone). README footer gains **License** section.
- `CONVENTIONS.md` **§9** — the product-front-matter convention lives **home-local** (VEMO_SKILLS-as-standalone-output),
  deliberately **not** in `readme-style.md`: internal framework READMEs are orientation docs, not product pages, and
  must not inherit product framing. Includes a standalone summary of `skill_spec` §9 (for use outside a governed project).
### Added (R32 zh-mirror fluency rubric — D7)
- `readme-style.md` **R32 advisory leg** now **cross-cites** `zh-prose.md` **R14–R20** (+ its EN→zh term table) as the
  zh-mirror authoring rubric (mirror must read as **written Chinese**, not translationese). **Cross-cite, not a copy**
  (zh-prose stays owned in `technical-report-style`'s module space — single source). Stays **ADVISORY, not must-pass**
  (fluency isn't machine-checkable; the structural parts remain the must-pass proxy — preserves the T020 D2 split).
- `readme-style.md` **R31** narrowed by **one sanctioned carve-out**: zh-prose reaches the `README_zh.md` *mirror* (the
  exception is named in R31 — visible, not silent); the English entry doc + report bodies stay prose-excluded.
- `zh-prose.md` gains a generic **EN→zh term table** (pin / home / materialize / template-owned / bump / gate …) for
  repo-wide terminology consistency (R18).
### Changed (zh-mirror fluency rewrite)
- `README_zh.md` **rewritten** as fluent written Chinese per zh-prose R14–R20 (user-flagged: the prior mirror was
  word-for-word translationese — "完全不可读"). Heading-skeleton parity preserved (structural, tolerates rewritten
  prose); front matter mirrored; mermaid still compiles. (Wildwombat `README_zh.md` rewritten in the same pass — see
  that repo's changelog.)

## [0.8.0] — 2026-06-10
> Source: T020 (bilingual README — user-approved Gate-1 2026-06-10 via team-lead; D1 ADR addendum / D2 structural / D4 business).
> Companion: Wildmeerkat v0.14.0 (audit_spec §13.2 check 5 + gate_spec + Framework_Release wiring). Reference: Wildpanda v1.8.0.
### Added (R32 bilingual pair; GB-008 two-layer shape)
- `readme-style.md` gains **`R32`**: an entry doc ships as a language **pair** — `README.md` (English, canonical) +
  `README_zh.md` (Chinese mirror) in the same directory, each with a top-of-file **bidirectional language switcher**
  (`🇨🇳 中文 | 🇬🇧 English`, the non-current language linking to its file). `README_zh.md` is a **faithful mirror**
  (same heading skeleton + governance diagram, translated). R32 governs the **structure** only and **cites** the
  language policy ADR for canonicity (this instance: `ADR-0003` + its 2026-06-10 bilingual addendum — **English wins
  on drift**); it does not restate the policy (single-source). Identity-decoupled; Wildpanda cited as provenance.
- `readme-style.md` Machine check — **`R32`** structural check, **must-pass at release** (`audit_spec` §13.2 check 5;
  `gate_spec` wires advisory @ Gate 2 / must-pass @ release): three parts — zh-mirror **presence**, **bidirectional
  switcher** grep (both sides), **heading-skeleton parity**. Semantic translation faithfulness stays advisory/human;
  diagrams in `README_zh.md` are covered by `R29-render` (must compile too).
### Added (VEMO_SKILLS own zh mirror — R32 dogfood)
- `README_zh.md` — the rule's home repo now conforms: a faithful Chinese mirror of `README.md` (10 H1/H2 + 4 H3
  parity, same governance diagram, switcher both sides). `README.md` gains the EN-side switcher + R29→R29–R32 pointer.

## [0.7.0] — 2026-06-10
> Source: T019 (v0.13.0 governance batch — user-approved Gate-1 2026-06-10 via team-lead, D1-a split + D2).
> Companion: Wildmeerkat v0.13.0 (gate_spec §2d wiring + registry_spec §2b GB-007 + audit_spec §13.2 check 4).
### Added (GB-008 diagram-compile check)
- `readme-style.md` Machine-check gains **`R29-render`**: every ```mermaid block in an entry doc MUST compile under
  `mmdc` (a markmap source SHOULD render under `markmap`). Carries the **unquoted-edge-label** syntax note (bare
  parens/pipes in an unquoted edge label fail — quote the label; `(BIND)` was the live break) and the GB-008 provenance
  (VEMO_SKILLS README v0.6.0 shipped a non-compiling block past an 8/8 substance review). This file is the **single
  source for the check**; `gate_spec` §2d wires *when* (advisory @ Gate 2, must-pass @ release).
- Note: `readme-style.md` is a module of `technical-report-style.md` and carries no own version — this VERSION/CHANGELOG
  bump covers the change.
### Added (Getting-started bootstrap docs; in-footprint user add)
- `README.md` — new **"Getting started — first, install the meta skills"** section placed **before** Use-via-Prompt:
  documents the meta-skill first-acquisition path (attach this repo as a submodule pinned to a release tag → run the
  bootstrap regen → it materializes **every** registered skill, incl. `framework-sync` / `framework-contribute` /
  `skill-publish`, into `.claude/skills/` → only then do the prompt triggers resolve). Makes the self-reference
  explicit — the meta skills are themselves registered skills in `skills/governance/`, so acquiring the repo + regen
  **is** acquiring the maintenance toolchain (no separate installer). Points at `Wildwombat Project_Init` steps 1–2 /
  `team_bootstrap` (no duplication); identity-decoupled (no org/account/project hardcode). Closes the meta-skill
  bootstrap chicken-and-egg gap a user hit reading the live README. Plus a Use-via-Prompt back-pointer.
- `CONVENTIONS.md` §0 (bind stage) — now states the regen binds **every** registered skill **including the
  governance-meta skills themselves**; no separate installer (cross-pointer to the README Getting-started section).

### Also released here
- The T018 README diagram hotfix (`202e042` — quoted the `(BIND)` edge label so the mermaid block compiles) was on
  `main` ahead of any tag; v0.7.0 is the first tag that contains it, so the tag's tree now passes its own `R29-render`.

## [0.6.0] — 2026-06-10
### Added (T017 skill-publish governance; user-approved Gate-1 2026-06-10 via team-lead; D1-a/D2-a/D3-a/D4)
- `skills/governance/skill-publish/` — new skill: publish a skill into this home by its **declared category**
  (frontmatter `category:` is the single source; the path is derived). Existing category → place; **new category →
  create the folder** (declare-and-create, no fixed enum). Maintains the README on every add/move/rename/remove and
  self-checks via a **README ⇄ skills multiset diff** (not a count compare) + a declared-category⇄path consistency
  check. Governs **placement + registration only** — adoption (entering a project toolset) stays the user-consent red
  line (skill_spec §6). Identity-decoupled: no org/account/project hardcode (skill_spec §9).
- `CONVENTIONS.md` — home-local operating conventions consolidated **with pointers** to Framework 0 `skill_spec`
  (D1-a, consolidate-with-pointers, no duplication): category layout, declared-`category` field, README-maintenance
  obligation + multiset check, regen-byte-identical rule, identity-decoupling self-check, versioning, actor constraint.
### Changed
- `category:` frontmatter **backfilled** on all 8 pre-existing skills (zero moves — values match current dirs), so the
  declared category is now the single source of truth for every skill.
- `README.md` — Layout reconciled to `skills/<category>/<name>/` (per functional category, declare-and-create; was
  "per-framework"); added the `skill-publish` role-table row, governance-diagram node, Use-via-Prompt section, and
  中英 keyword row; pointer to `CONVENTIONS.md`. R29–R31; R30 version pointer (no hardcoded number).
- **Registration lifecycle documented** (in-footprint user add): `CONVENTIONS.md` §0 + `skill-publish` framing +
  README state the ordered chain **register → bind (+consent = adopt) → sync / contribute** — registration is the
  **precondition**; an unregistered/untagged skill is invisible to `framework-sync` and `framework-contribute`.
  Registration ≠ adoption (adoption stays the user-consent red line). README governance diagram gains a REGISTER node
  upstream of sync/contribute; Use-via-Prompt prompts re-ordered to the lifecycle.
> Companion: Wildmeerkat v0.12.0 (`skill_spec` §9 per-category vocab fix + CONVENTIONS pointer).

## [0.5.0] — 2026-06-10
### Added (T016 v0.11.0 batch; user-approved 2026-06-10 via team-lead; D1-a/D3/D4-a)
- `skills/governance/framework-sync/` — new skill (new `governance/` grouping per D1-a): checks whether any governance
  framework pinned as a **submodule** has advanced upstream, reports the diff, and bumps pins **only on a user version
  gate** (never auto). Submodule model — no template-boundary file list, no file-copy; the unit of sync is the whole
  pinned submodule at a tag. Targets resolved at runtime from `project_profile`; upstream read from the **live remote**
  (`git remote get-url`), so it is correct across org migrations (zero-hardcode, skill_spec §9). Session-start
  report-only trigger (`chat_spec` §4 step 6) + keyword. `gh` pre-check with `git ls-remote` read fallback. Reference
  shape borrowed from Wildpanda `governance-sync` (notify-don't-auto-update), mechanism rewritten for submodules.
- `skills/governance/framework-contribute/` — new skill: opens a PR carrying a local framework improvement back to that
  framework's repo via a `contrib/*` branch (no temp-clone, no file-copy — the change is already in the submodule
  clone). **Peer dual-path selected by a live permission probe** (`permissions.push`): Path A (push access) → push the
  branch to the repo's own origin + in-repo PR; Path B (no push access) → `gh repo fork` + push to the fork +
  cross-repo PR. Neither path is a default or a fallback — an external contributor PR-ing a framework they do not own
  is a first-class case. **Identity-decoupled**: owner/repo from the remote, contributor from `gh api user`, path from
  the probe — zero hardcoded account/org. Handles the **detached-HEAD-at-pinned-tag** case (branch from upstream head,
  never commit detached) and restores the pinned state after the PR. Co-Authored-By + README-check mandatory. Reference
  shape from the single-upstream `governance-contribute`, mechanism rewritten for the submodule model.
- `publish-deliverable/references/technical-report-style.md` — **Machine-checkable thresholds (GB-006)** section: a
  consolidated, deterministic presentation-conformance check (R23 paragraph length / R21 conclusion block / R25 table
  width / R27 line length + inline-tag density / R22 heading depth) with measure + report definitions. Single source
  for the threshold values; the gate step that runs it is wired in `gate_spec` §2c. Advisory/non-blocking. Thresholds
  anchored to the GB-006 evidence (T003_solution R23/R25/R27 breaches).
- **Identity decoupling** (user hard constraint, in-scope T016): framework-sync/contribute resolve owner/identity/
  permission **at runtime** (`git remote get-url` / `gh api user` / `permissions.push` probe) — zero hardcoded
  account/org. framework-contribute offers **peer dual-path** (push-access → in-repo PR / no-push → fork cross-repo
  PR), selected by a live probe; external-contributor PRs (e.g. to a framework one does not own) are a first-class
  case, not a fallback. framework-sync's report path works read-only.
- `README.md` — governed to entry-doc style R29–R31 (Purpose / Quickstart / Skills role-table / Governance diagram /
  Version pointer) + new **Use via Prompt** section: copy-paste natural-language triggers for sync and contribute/PR,
  peer-path explanation (zero-config, zero-identity), and a 中英 keyword-trigger table. (R30 / Framework_Release step 4
  README-at-release obligation.)

## [0.4.0] — 2026-06-10
### Added (T015 README governance + visualization; user full-package adoption 2026-06-10; D2-a placement)
- `skills/orchestration/publish-deliverable/references/readme-style.md` — new **entry-document** style module,
  rules **R29+**: R29 required-section checklist (Purpose / Quickstart / Role table / Governance diagram / Version;
  missing section → warning), R30 README freshness (defers to `audit_spec` §13.2; optional `ttl_days` frontmatter),
  R31 scope boundary. **Physically separate** from R1–R28 (report body): README rules and report-body rules do not
  cross-apply (different artifact + audience). Borrowed standard-readme (RichardLitt/standard-readme, MIT, 6.3k★)
  section-checklist idea, slimmed. Referenced from `publish-deliverable/SKILL.md` + the `technical-report-style.md`
  Module pointer.
- `skills/orchestration/governance-visualize/` — new skill: renders the governance system as a mermaid **flowchart**
  (frameworks/gates/agents) + **stateDiagram** (task seven-gate lifecycle) + interactive **markmap HTML** overview for
  onboarding; SVG via `mmdc` at release; Feishu whiteboard path via `publish-deliverable`. Render-don't-author
  (every node traces to a source definition); diagrams are regenerable build artifacts (ties to `audit_spec` §13
  freshness). Tooling (`mmdc`, `markmap-cli`) is installed at first use, not pinned here. Idea/tooling borrows:
  mermaid-js, markmap (markmap-js, MIT, 12.9k★).

## [0.3.0] — 2026-06-10 (released: tag v0.3.0)
### Added (presentation/scannability rules, task T014 part B; user red-line approval 2026-06-10)
- `skills/orchestration/publish-deliverable/references/technical-report-style.md` — new **Presentation /
  Scannability** section, rules **R21–R28**: R21 one-page conclusion, R22 progressive disclosure + ≤3 heading
  depth, R23 short paragraphs (≤7 lines), R24 keyword-first, R25 narrow tables (≤5 cols), R26 table-vs-list,
  R27 annotation convergence, R28 Feishu block mapping. Each carries a machine-checkable threshold; platform/
  language-agnostic except R28 (Feishu). Lands as a new section after R13/the zh-prose Module pointer (R14–R20
  physically live in the separate `zh-prose.md` module; numbering R21–R28 stays globally unique). Borrowed from
  **Microsoft Style Guide "Scannable content" (CC-BY-4.0)**; R26 from **Google dev-docs**; transcribed to checkable
  rules. R27 does not relax R4 (it governs tag *placement*, not whether to tag). SKILL.md references note updated.

## [0.2.0] — 2026-06-09 (local; pending publish gate)
### Added (research-solution skills, task #12 parts 3–4)
- `skills/research/solution-doc-structure/` — solution/design-doc **structure** ruleset (arc42 skeleton S1–S12,
  CC-BY-SA + MADR per-decision blocks D1–D6, MIT — borrowed as structure ideas, transcribed to checkable rules)
  + `references/arc42-mapping.md` checklist. Governs the `solution_document` shape (Wildtarsier §1.9).
- `skills/research/decision-review/` — reliability ruleset (self-built): per-decision **6-field floor**
  (options/evidence/trade-offs/assumptions/failure-modes/validation) as a 准出 completeness criterion + a
  **cross-model red-team** pre-publish pass (a step inside the existing Gate 2, NOT a new gate). Borrows the ideas of
  structured-MADR (machine-checkable fields) + adversarial-review (cross-model critique).
### Adopted (task #12 part 4, user consent 2026-06-09)
- `skills/research/thinking-partner/` — **adopted** discussion-style sparring skill (multi-round assumption-challenge +
  mental-model diagnosis), complements `decision-review`. Source: github.com/mattnowdev/thinking-partner (150⭐).
  **License: MIT (Copyright (c) 2026 mattnowdev)** — full notice retained in the vendored dir. Vendored **byte-exact**
  via `git clone` (subagent verbatim channels were denied; team-lead cloned the repo, so SKILL.md + both
  `references/` files are the real artifact, not a transcription). §9 decoupling: clean — zero hardcoded project values.
### Notes
- The first two skills are **self-authored generic rulesets** (governance-architect's lane); thinking-partner is an
  external **adopt**. Project values (red-team model, which decisions are "key") stay in the business instance — zero
  hardcode (skill_spec §9).

## [0.1.0] — 2026-06-09 (released: commit 1613d17 + tag v0.1.0)
### Added
- Repo skeleton: `skills/<framework>/<name>/` per-framework layout (skill_spec §7 ownership), VERSION, README.
- Homed generic skill bodies (copied + refactored to zero-hardcode from the business repo):
  - `skills/orchestration/prd-breakdown/SKILL.md` — generic PRD-decomposition mechanism.
  - `skills/orchestration/publish-deliverable/SKILL.md` — generic publish + domain-routing + notify mechanism
    (all project values read from instance at runtime).
  - `skills/orchestration/publish-deliverable/references/technical-report-style.md` — generic report rules R1–R12 + R13.
  - `skills/orchestration/publish-deliverable/references/zh-prose.md` — optional Chinese-prose module R14–R20
    (generic content; activated by the business-repo instance switch).
### Notes
- Not yet published to GitHub; business-repo submodule wiring is prepared-inactive (deferred to the publish gate).
