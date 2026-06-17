---
name: rendering-html-eval-reports
category: orchestration
description: Render pre-computed results into a single self-contained HTML report (CSS inlined, images base64-embedded, mandatory provenance header) in one of two report types — an EVALUATION report (per-class accuracy vs a threshold, a confusion matrix including the abstain/rejection class, a latency distribution, an error-case gallery with overlays) or a TRAINING-EXPERIMENT / ablation report (experiment-ladder table, inline training curves, ablation table, measured-vs-inferred labelling, limitations). Use when an eval run or a training-experiment sweep has produced results that should become a shareable local HTML artifact. Render-only — it consumes results, it does NOT run inference, train, or compute them; the eval type collects ALL error cases (samples only the correct predictions); it embeds only de-identified images per the instance privacy policy; the HTML is a local artifact, not committed to git. Distinct from publishing-deliverables (which publishes a doc to the Feishu/Lark wiki).
allowed-tools: Read, Write
---

# Render an Eval Report as Self-Contained HTML

Turn the **results** of an evaluation run into **one self-contained HTML file** — provenance header, per-class
accuracy table, confusion matrix, sample gallery, and latency distribution, with every image base64-embedded so the
report is a single portable artifact (no sidecar files, opens offline).

> **Render-only — this skill does not run the eval.** It consumes **already-computed** results (per-class metrics,
> confusion counts, latency samples, error-case records). It does **not** load a model, run inference, or compute any
> metric. Conflating *render* with *execute* would hardcode the skill to one project's runner and break decoupling
> (`skill_spec` §9). The portable thing is the **report structure**; the numbers come from the caller. The same
> applies to the training-experiment type below: it renders a **training sweep's already-recorded results**, it does
> not train.

## Two report types (same skill, same invariants)
This skill renders **two report types**, both sharing the **provenance header, self-containment, privacy, and
interface-language** rules below — they differ only in their body sections:
1. **Evaluation report** — the original type: per-class accuracy vs a threshold, confusion matrix (with the
   abstain/rejection column), sample gallery, latency distribution. Sections in **§Report sections (evaluation)**.
2. **Training-experiment / ablation report** — a paper-style write-up of a training sweep: an experiment-ladder table
   (per round: variable / hypothesis / result / verdict), inline training curves, an ablation comparison table,
   per-figure **measured-vs-inferred** labelling, and a consolidated limitations section. Sections in
   **§Report sections (training-experiment)**. The structure mirrors a paper skeleton (abstract / method / setup /
   results / ablation / limitations) — kept **generic**, no project vocabulary.

The caller declares which type to render. The shared rules (R1, R5, R6) apply to **both**; R2–R4 are
evaluation-type rules.

## When to use
- An eval run (any model, any dataset) **or** a training-experiment sweep (any number of rounds / ablations) produced
  results that should become a **shareable local HTML report** — to read offline, attach to a review, or hand to a
  teammate as a single file.
- Trigger phrases (eval): "出 HTML 评测报告" · "render the eval report" · "评测结果生成网页报告" · "self-contained eval HTML".
- Trigger phrases (training-experiment): "出训练实验报告" · "render the training-experiment report" · "训练实验/消融生成网页报告" · "ablation report HTML".
- **Not** for publishing to a wiki — that is `publishing-deliverables` (see Boundary).

## Inputs (the caller computes these; the skill renders them)
The skill consumes a results bundle. None of these values are hardcoded — all are caller/instance-supplied. The
**evaluation** inputs are below; the **training-experiment** inputs follow in their own subsection.

### Evaluation-report inputs
- **provenance** (mandatory): `data_version`, `model_sha`, `runtime`, `date`. Missing any one → the report is
  **incomplete** (Rule R1); render a visible `MISSING` marker rather than omitting the field silently.
- **per-class metrics**: for each class, its accuracy (and support count), plus the **acceptance threshold** to compare
  against (the threshold is an **instance value** — the skill renders the pass/fail mark, it does not know the number).
- **confusion counts**: an N×M matrix; the prediction axis **includes the abstain/rejection class** as a column (the
  class a rejecting/abstaining classifier returns when nothing matches). Its rate is a **headline metric** (Rule R3).
- **latency samples**: a distribution (e.g. p50/p90/max) **plus caveat text** — the caller declares the caveats that
  make the numbers non-comparable to a deployment gate (Rule R4). The skill renders the caveat block; the **text is the
  caller's** (e.g. host-CPU-not-target / includes-preprocessing / full-not-lite-variant).
- **error-case records** (one per misclassified sample): the image **as a base64 string (or a directly-inlinable
  `data:` URI)** of the **already-de-identified, overlay-drawn** picture, plus true label, **predicted label**, and the
  overlay kind (keypoints / detected region / heatmap — whatever the model emits, already baked into the image). **All**
  error cases are passed in (Rule R2). The caller supplies base64; the skill does not encode bytes (see Inputs note).
- **correct-prediction samples**: a **subset** for the gallery's "got-it-right" strip, each likewise as a base64
  string / `data:` URI of an already-de-identified image (sampling is fine here — Rule R2).
- **privacy policy** (instance value): the policy under which the caller **already de-identified** the images before
  encoding them (Rule R5). The skill never receives raw image bytes — only de-identified base64.

### Training-experiment-report inputs
For the training-experiment / ablation type, the caller supplies (again, all caller/instance-supplied, nothing
hardcoded):
- **provenance** (mandatory, same R1 four fields): `data_version`, `model_sha`, `runtime`, `date` — the training run's
  traceability root. `model_sha` here identifies the **trained checkpoint / config** the report describes.
- **abstract / summary text**: a short caller-written summary of what the sweep set out to test and found.
- **experiment-ladder rounds**: an ordered list; each round carries **variable** (the single thing changed), **hypothesis**
  (what was expected), **result** (what happened, with numbers), and **verdict** (kept / reverted / inconclusive — the
  caller's words, the skill does not judge). One-variable-per-round is a **caller discipline**, not enforced here.
- **training-curve figures**: each a base64 string / `data:` URI of an **already-rendered** curve image (loss/accuracy
  vs step/epoch — whatever the caller plotted), plus a caption. The skill inlines them; it does **not** plot.
- **ablation rows**: a comparison table — each row a configuration (which components on/off) and its metric(s); the
  caller supplies the cells, the skill renders the table.
- **measured-vs-inferred marks** (Rule R6): for **every** number in the ladder / ablation / summary, the caller marks it
  **measured** (actually run) or **inferred/estimated** (extrapolated, projected, or carried from elsewhere). An
  unmarked number is rendered with a visible "unlabelled" marker, never silently presented as measured.
- **limitations**: a caller-written list of the sweep's limitations / threats-to-validity, rendered as a consolidated
  closing section (not scattered footnotes).
- **privacy policy** (instance value): same as above — any embedded figure is **already de-identified** by the caller
  before encoding; the skill never receives raw image bytes.

> **Image-input contract (who encodes):** the skill's tools are `Read, Write` — it **does not encode pixels**. The
> caller (or an upstream tool) **de-identifies then base64-encodes** each image and passes the **base64 string / `data:`
> URI**; the skill only inlines it into the HTML. This is also a **privacy hardening**: the skill never touches raw
> image bytes, so a raw frame cannot leak through it.

## Output
- One file: `<out>.html` — fully self-contained (CSS inlined, images base64 data-URIs). No external assets.
- **Destination is instance-governed**: by default the HTML is a **local artifact, not committed to git** (Rule R5);
  how it is delivered (attached, copied to a share, etc.) is read from the instance, not assumed here.

## Report-interface language (instance-driven)
The report's **interface text** — section headings, table column labels, the caveat preamble, the pass/fail and MISSING
markers — is rendered in the **project language policy's language** (an **instance value**, read at runtime; e.g. the
consuming project's `project_profile` language switch — the same policy `publishing-deliverables` reads). The skill
hardcodes **no** interface language; the English strings in `references/html-template.md` are a **default placeholder**,
to be substituted with the instance language. **Data keys stay verbatim** — class ids, `model_sha`, version strings,
runtime names, and provenance values are **never translated** (they are data, not interface). If the policy assigns
Chinese, the **`polishing-chinese-prose`** skill is the authority for the Chinese interface text.

## Report sections (evaluation) — the generic skeleton; `references/html-template.md` holds the markup
Build the HTML from `references/html-template.md` (skeleton + inline CSS + per-section render rules). Evaluation-report
sections, in order:
1. **Provenance header** (mandatory, Rule R1) — `data_version` · `model_sha` · `runtime` · `date`, rendered as a header
   band. This is the report's traceability root; a report without it cannot be trusted to a specific model/data state.
2. **Per-class accuracy table** — one row per class: class · accuracy · support · **vs acceptance threshold** (pass/fail
   mark). The threshold value is supplied by the instance; the skill only renders the comparison.
3. **Confusion matrix** — rows = true classes, columns = predicted classes **including the abstain/rejection column**.
   Surface the **abstention/rejection rate** prominently (Rule R3) — it is often the headline finding, not a footnote.
4. **Sample gallery** — two strips: **all error cases** (Rule R2; each tile shows the image with overlay, **true →
   predicted** labels) and a **sampled** set of correct predictions. The asymmetry is a quality rule, not an option.
5. **Latency distribution** — the distribution figures + a **caveat block** rendered verbatim from the caller's caveat
   text (Rule R4). Never present latency without the caveats that scope it.

## Report sections (training-experiment) — the generic skeleton; `references/html-template.md` holds the markup
The training-experiment / ablation type uses the **parallel skeleton** in `references/html-template.md`. Sections, in
order (paper-style, kept generic):
1. **Provenance header** (mandatory, Rule R1) — same four fields as the eval type; here `model_sha` identifies the
   **trained checkpoint / config** the report describes.
2. **Abstract / summary** — the caller's short statement of what the sweep tested and found. Numbers here carry their
   measured-vs-inferred mark (Rule R6).
3. **Experiment-ladder table** — one row per round: **variable** (the single thing changed) · **hypothesis** · **result**
   (with numbers, each R6-marked) · **verdict** (kept / reverted / inconclusive — the caller's word; the skill does not
   judge). The skill renders the table; one-variable-per-round is a caller discipline.
4. **Training curves** — inline base64 figures (already plotted by the caller) with captions. The skill inlines, it does
   not plot. De-identified per the instance policy like any embedded image (Rule R5).
5. **Ablation comparison table** — rows = configurations (components on/off), columns = metric(s); each metric cell is
   R6-marked. The skill renders the comparison; it does not compute deltas the caller did not supply.
6. **Limitations** — a **consolidated** closing section from the caller's limitations / threats-to-validity list (not
   scattered footnotes). Surfacing limits in one place is a quality rule of this report type.

> Both types share the **provenance header (R1)**, **self-containment**, **privacy (R5)**, and **interface-language**
> rules. **R6 (measured-vs-inferred)** applies to **both** but is the spine of the training type, where projected /
> extrapolated numbers are common and must never read as measured.

## Rules (the skill's generic discipline)
- **R1 — Provenance is mandatory.** The four fields (`data_version`, `model_sha`, `runtime`, `date`) are required. A
  report missing any is incomplete; render an explicit `MISSING` marker so the gap is visible, never silently dropped.
- **R2 — Error-gallery asymmetry (all errors, sampled correct).** **Every** error case is included (with predicted
  label + overlay); correct predictions are only **sampled**. Sampling errors would let a systematic failure hide —
  collecting them all is the point. Do not cap or sample the error strip.
- **R3 — The abstain/rejection class is first-class.** The confusion matrix carries the abstain/rejection column, and
  its rate is surfaced as a headline metric. (Generic: a rejecting classifier returns this class when nothing matches;
  the project names it — the skill does not.)
- **R4 — Latency always carries its caveats.** Latency figures are rendered only alongside the caller-supplied caveat
  text that scopes them (what hardware, what was/wasn't timed, which variant) and their non-comparability to any
  deployment gate. No caveat text supplied → render a visible "caveats not declared" warning rather than bare numbers.
- **R5 — Privacy + artifact destination.** The skill embeds **only de-identified images**, and it receives them
  **already de-identified and already base64-encoded by the caller** (image-input contract above) — the skill does not
  encode pixels and never touches raw image bytes (`Read, Write` only), so a raw frame cannot leak through it. The
  **instance privacy policy** governs how the caller de-identifies; if no policy is supplied, the skill **refuses to
  embed** the imagery and flags it rather than inlining unvetted base64. The HTML is by default a **local artifact, not
  committed to git**; the delivery method is instance-governed. Outward delivery is confirm-when-unsure.
- **R6 — Measured vs inferred labelling (both types; the training type's spine).** Every reported number carries a
  caller-supplied mark: **measured** (actually run) or **inferred/estimated** (extrapolated, projected, or carried from
  another setting). An **unmarked** number is rendered with a visible "unlabelled" marker, never silently presented as
  measured. In a training-experiment report, projected / extrapolated figures are common — letting one read as measured
  would misrepresent the result, so the mark is mandatory on ladder, ablation, and summary numbers alike.

## Boundary
- **vs `publishing-deliverables`** (the adjacent orchestration skill): that skill **publishes a deliverable to the
  Feishu/Lark wiki** — a networked doc (XML + native whiteboard mermaid via lark-cli, a persistent wiki node, reviewer
  @-notify). **This skill renders a local self-contained HTML artifact** (base64 images, not in git, privacy-gated).
  Rendering an artifact and publishing to a wiki are **two different functions**. They *compose*: the findings in this
  HTML report can feed a Feishu summary deliverable that `publishing-deliverables` then publishes — but "render the
  HTML report" and "publish to the wiki" are distinct steps. Want the eval results filed to the team wiki → use
  `publishing-deliverables`; want a local self-contained HTML report → use this skill.
- **vs `structuring-solution-docs`**: that governs the **structure of a solution/design document** (arc42 + MADR prose);
  this produces an **eval-results artifact** (tables / matrix / gallery / numbers), not argumentative prose.

## Decoupling (skill_spec §9)
This body is generic — **zero hardcoded project values**. The class set (including the abstain/rejection class name),
the acceptance threshold, the latency caveat text, the provenance values, the privacy policy, and the
**report-interface language** (see above) are **all read from the caller / the consuming project's instance at
runtime**. The skill keeps the structure, the rules, and the slots; the project fills the values. Data keys (class ids,
sha, version/runtime strings) are rendered verbatim — never translated.

## Notes
- Render-only; consumes pre-computed results; does not run inference (restated because it is the spine).
- Self-contained = the single deliverable: CSS inlined, images as base64 data-URIs, opens with no network or sidecar.
- `references/html-template.md` is the single source for the markup/CSS skeleton and the per-section render rules; this
  body states the *what* and the *rules*, the reference holds the *how*.
