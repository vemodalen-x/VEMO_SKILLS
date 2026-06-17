# Technical-Report Style Spec (generic)

> Style-as-rules for project deliverables (borrowed from Vale's concept; generation discipline from
> ml-paper-writing). Every published deliverable MUST satisfy these rules. Phrased as checkable rules.
> Generic / template-owned (skill_spec §9): no project value hardcoded — the language tier is read from the instance.

## Structure
- R1. Lead with a **summary/abstract** (≤5 sentences): what was done, key result, main risk.
- R2. Then sections in a fixed order where applicable: Background/Goal → Method/Options → Comparison →
  Results/Findings → Recommendation → Risks & Open Items → References.
- R3. One idea per paragraph; sections are short and scannable.

## Evidence & Citations
- R4. Every quantitative claim carries a **citation** (link) and a tag: **实测 / 文献 / 推测**.
- R5. No unsourced performance numbers. Uncertainty is stated, not hidden.
- R6. Comparisons use a **table** with fixed columns; trade-offs shown for every option.

## Visuals
- R7. Architectures/flows/pipelines → a **diagram** (Feishu whiteboard mermaid), not prose.
- R8. Structured data (specs, comparisons, metrics) → **tables**, not bullet walls.

## Wording (Vale-style prose rules)
- R9. Prefer plain, precise wording; avoid vague verbs ("appropriate", "as needed") — state thresholds.
- R10. Active voice, present tense for findings; define acronyms on first use.
- R11. No marketing/overstating; recommended option is stated plainly with reasons.

## Conclusion discipline
- R12. End with explicit **Recommendation** + **Risks/Open Items** + **Next actions** (no dangling report).

## Language (binds to the instance language policy — no hardcode)
- R13. **The deliverable body language is set by the project's language policy** (instance-owned). The skill reads
  the policy from the business-repo instance; this spec does not name a specific language. If the policy assigns
  **Chinese** to outward team deliverables, the **`polishing-chinese-prose`** skill is the Chinese-prose authority and
  its 翻译腔 band (R14–R20) applies to the body. Operational notes (language-agnostic): keep proper nouns / model names /
  metric units / URLs as-is (e.g. MobileNetV2, TSM, INT8, 200ms); evidence tags stay 实测 / 文献 / 推测.

## Module
- The Chinese-prose ruleset lives in the standalone **`polishing-chinese-prose`** skill (cited by name, not relative-
  pathed), in two bands: **R14–R20 (翻译腔)** — instance-activated, apply only when the instance language policy
  selects Chinese for outward deliverables; **R33–R39 (文牍腔)** — agent-layer always-on, applies to any Chinese
  agent-dialogue reply regardless of the deliverable-language switch.
- The **entry-document** ruleset (R29+) lives in `readme-style.md` — a **separate family** for repo READMEs / onboarding
  guides, NOT report bodies. R1–R28 (report body) and R29+ (entry doc) do **not** cross-apply; the two address different
  artifacts and audiences. Apply `readme-style.md` when authoring/auditing an entry doc, never to a deliverable.

## Presentation / Scannability (borrowed — Microsoft Style Guide "Scannable content", CC-BY-4.0; R26 from Google dev-docs)
> Platform- and language-agnostic (except R28, which is Feishu-specific). These govern *presentation/structure/scan*,
> not content (R1–R13 content rules still apply unchanged). Each carries a machine-checkable threshold.
- R21. **Lead with a one-page conclusion.** The first content block IS a conclusion block, ≤1 screen
  (≤25 lines / ≤400 CJK chars), carrying the three elements **decision / key revisions / risks** — a reader decides
  from one screen.
- R22. **Progressive disclosure + layering.** The main body keeps conclusions only; raw data / long tables /
  per-item sourcing sink under an **"Appendix"** heading and do not appear in the main line. Heading depth ≤3 levels.
- R23. **Short paragraphs.** One paragraph ≤7 lines (≈≤5 sentences); over that → split, or convert to a list.
- R24. **Keyword-first.** Each paragraph's first sentence and each bullet's opening ≤8 chars surface the item's
  conclusion word — a scan that reads only the first word still locates the point.
- R25. **Narrow tables.** Table columns ≤5 (recommend ≤4); over that → transpose (swap rows/columns) or split.
  Each cell ≤1 sentence; long content drops to a table-footnote row.
- R26. **Table vs list — pick the right container** (Google dev-docs): multi-attribute side-by-side comparison → table;
  parallel same-kind items or ordered steps → list; never use a table to hold single-column content (a pseudo-table).
- R27. **Converge annotations.** Inline confidence/source tags (实测 / 文献 / 推测 · paper / OSS / source) converge to
  a sentence-/line-end short note `〔…〕`; give the legend once at the top; the body carries no scattered inline tags.
  (Does **not** relax R4's "every quantitative claim is tagged" — R27 governs tag *placement*, not whether to tag.)
- R28. **Feishu block mapping** (the only platform-bound rule): "one-page conclusion" → Feishu **callout** block;
  decision/architecture diagrams → **whiteboard** (mermaid auto-converts); long tables prefer a Feishu **table block**
  over a markdown table. Port the *semantics*, not the markdown syntax (Feishu docx is block-structured, not Markdown).

## Machine-checkable thresholds (GB-006 — presentation conformance check)
> The presentation gate step (`gate_spec` §2c) runs these on outward deliverables before user review / publication.
> This is the **single source** for the threshold *values* — the gate spec wires *when*, this defines *what*.
> Each is a deterministic check over the markdown; a breach is **reportable, advisory** (location + rule + threshold),
> not gate-failing by default. The subset below is the machine-checkable part of R21–R28 (R24/R26/R28 stay
> judgement-based — keyword-first, container choice, and platform mapping are not reducible to a single number).

| check | rule | threshold | how to measure | report on breach |
|---|---|---|---|---|
| paragraph length | R23 | ≤ 7 lines per paragraph | consecutive non-blank, non-list, non-table, non-heading lines | line range + actual count |
| conclusion block | R21 | first content block ≤ 25 lines | lines until the first blank after the opening block | actual length |
| table width | R25 | ≤ 5 columns per table | count `|`-delimited cells in a table's header row | table location + col count |
| line length | R27/R23 | ≤ 150 chars per line (inline-tag-wall proxy) | character count per rendered line, excluding code blocks | line numbers > threshold |
| inline-tag density | R27 | ≤ 1 inline `〔…〕` tag per line (rest sink to line-end) | count `〔` per line outside the legend | lines with scattered tags |
| heading depth | R22 | ≤ 3 levels (`###` max) | max `#` run length across headings | offending heading |

- **Scope**: outward deliverables only (user review / team publication). Internal drafts are exempt.
- **Exclusions**: fenced code blocks, the legend line (R27), and appendix tables explicitly marked as raw-data dumps
  (R22 permits wide reference tables under "Appendix").
- **Posture**: advisory (mirrors `gate_spec` §2c + `audit_spec` §11). The check produces a finding list; the author
  runs a presentation pass; acceptance is not blocked by presentation alone unless an instance elevates it (§4).
- **Provenance**: thresholds anchored to the GB-006 evidence (T003_solution: R23 13-line block, R25 8-col matrix,
  R27 >150-char inline-tag walls) — the numbers are the rule limits those breaches crossed.
