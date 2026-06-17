# readme-style · Entry-Document Style Module (R29+) — generic

> Module of `technical-report-style.md`, **physically separate** because it governs a different artifact and audience:
> **entry documents** (repo `README.md`, onboarding guides) — read by a *new* engineer orienting to the repo, not a
> reviewer of a deliverable. The R1–R28 report-body rules do **not** apply to READMEs and these R29+ rules do **not**
> apply to report bodies; keep the two families apart (this separation is the whole reason for a distinct file).
>
> Generic content (reusable by any repo); no instance values here. Apply when authoring or auditing a repo's entry doc.
> Borrowed from standard-readme (RichardLitt/standard-readme, MIT, 6.3k★) — section-checklist idea, slimmed to the
> governance-repo case. Source: https://github.com/RichardLitt/standard-readme

## Required-section checklist (R29)
An entry-doc `README.md` SHOULD contain these sections (a missing one is a **warning**, not a block — entry docs vary):
- **Purpose** — what this repo is and who it is for, in ≤3 sentences (a stranger gets oriented immediately).
- **Quickstart** — the shortest path to "first useful thing" (clone/attach/run); copy-pasteable.
- **Role table** — the agents/roles this repo defines or governs, one row each (id · duty · boundary).
- **Governance diagram** — the operation flow as a figure (mermaid/SVG, produced by the `visualizing-governance` skill);
  for the business repo, the framework wiring; for a framework repo, its own gate/state flow.
- **Version** — current `VERSION` + a pointer to `CHANGELOG.md`; keeps the README honest about what release it describes.

## Freshness (R30)
- The README MUST be refreshed at release time when the release changed what it describes (the obligation lives in
  `Framework_Release.procedure.md`; the check is `audit_spec` §13.2 `ARTIFACT_STALE`). An optional `ttl_days:`
  frontmatter field sets a maximum age independent of releases.

## Scope boundary (R31)
- These rules govern the **entry-doc skeleton** (which sections exist, that they stay current). They do **not** govern
  report-body prose, evidence tagging, or scannability — those remain R1–R28 (`technical-report-style.md`) and the
  Chinese-prose authority is the **`polishing-chinese-prose`** skill; they apply to deliverables, never to READMEs.
- **One sanctioned carve-out (R32 zh mirror):** the `polishing-chinese-prose` 翻译腔 band (R14–R20) *does* reach the **`README_zh.md` mirror**, as the
  **advisory** rubric for R32's semantic-faithfulness leg (see R32). This is the single exception — prose rules stay
  excluded from the **English** entry doc and from report bodies; only the Chinese *mirror's* fluency is governed, and
  only advisorily. The exception is named here so it is visible, not silent.

## Bilingual pair (R32)
An entry doc ships as a **language pair**, not a single file (reference convention: this repository's bilingual README pair):
- **`README.md` (English) + `README_zh.md` (Chinese), same directory.** Both files MUST exist.
- **Bidirectional language switcher** at top-of-file. The current language is bold; the other is a link to its file:
  - EN side: `<a href="README_zh.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong>`
  - zh side: `<strong>🇨🇳 中文</strong> | <a href="README.md">🇬🇧 English</a>`
- **`README_zh.md` is a faithful mirror** of `README.md`: the same section skeleton (heading parity), the same
  governance diagram, content translated. It is not an independent document.
- **Language canonicity is NOT asserted here** — it is governed by the **project's language policy** (instance-owned;
  a tiered language-policy ADR + its bilingual-README provision): **the English README is canonical; English wins on
  drift.** R32 governs only the *structure* of the pair; do not restate the policy, and do not hardcode an ADR number
  (instance value — `skill_spec` §9 decoupling).
- The flag glyphs (🇨🇳/🇬🇧) are part of this repository's bilingual README convention — keep parity.

## Machine check
- `R29`: scan the README's headings; any required section absent → **warning** (list the missing section).
- `R30`: defer to `audit_spec` §13.2 (do not re-implement the freshness rule here — single source).
- `R31`: structural — a README that embeds report-body content (long evidence tables, deliverable prose) is mis-scoped;
  flag to move that content to a deliverable.
- `R29-render` (GB-008): the **Governance diagram** must actually render. **Every** ```mermaid block in the entry doc
  MUST compile under `mmdc`; a markmap source `.md` SHOULD render under `markmap`.
  - *how to measure*: extract each ```mermaid fence to a temp file, run `mmdc -i <block>.mmd -o <tmp>.svg`; a non-zero
    exit or a `Parse error` is a **breach**. (This is the single source for the *check*; `gate_spec` §2d wires *when*
    it runs — advisory at Gate 2, must-pass at release — and `audit_spec` §13.2 check 4 runs it at release.)
  - *report on breach*: file + block index + the `mmdc` error line.
  - *common-syntax note*: bare parens/pipes in an **unquoted** edge label fail (`-->|a (b)|` → mermaid reads the `(`
    as a node shape and errors `got 'PS'`); **quote the label** `-->|"a (b)"|`. Parens/pipes inside **quoted** node
    text (`X["a | b"]`) are fine. (Provenance: VEMO_SKILLS README v0.6.0 shipped exactly this break — a `(BIND)` bare
    paren in an unquoted edge label — and it passed an 8/8 substance review because nobody rendered the figure.)
  - *posture*: advisory at Gate 2, **must-pass at release** (GB-008 / `gate_spec` §2d) — a draft is not blocked on a
    figure, but a non-compiling diagram cannot ship.
- `R32` (bilingual pair): **structural** check, **must-pass at release** (`audit_spec` §13.2 check 5; `gate_spec`
  wires *when* — advisory at Gate 2, must-pass at release). Three machine-checkable parts:
  - *presence*: `README_zh.md` exists beside every `README.md` → a missing mirror is a **breach**.
  - *switcher*: both files carry the bidirectional switcher (grep the EN side for `href="README_zh.md"` + the zh side
    for `href="README.md"`, each with its flag glyph) → a one-directional or absent switcher is a **breach**.
  - *heading parity*: the two files have the same count and sequence of `#`/`##` headings (the machine proxy for
    "mirror") → a skeleton mismatch is a **breach** (the zh file drifted from the EN structure).
  - *report on breach*: repo + which part (presence / switcher direction / heading delta).
  - *advisory (not machine)*: **semantic translation faithfulness** — whether the prose actually says the same thing,
    **and reads as written Chinese rather than translationese** — is a human/reviewer concern; the machine proxies
    structure only. The rubric for this advisory review is the **`polishing-chinese-prose`** 翻译腔 band (R14–R20:
    active-voice, sentence-splitting, consistent terminology, 的/地/得, no filler) **+ its EN→zh term table** — the
    `README_zh.md` mirror is authored to that standard. This is a **cross-cite, not a copy**: Chinese-prose style is
    owned by the standalone `polishing-chinese-prose` skill (single source); R32 only *points* to it by name as the
    zh-mirror rubric. Stays **advisory** (fluency is not machine-
    checkable — the structural parts above are the must-pass proxy). Diagrams in `README_zh.md` are covered by
    `R29-render` (every ```mermaid block in the zh mirror must compile too).
