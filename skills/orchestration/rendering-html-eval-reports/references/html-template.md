# Self-Contained HTML Eval-Report Template (markup + inline CSS + render rules)

> Generic reference for `rendering-html-eval-reports`. It holds the **markup skeleton, inline CSS, and per-section
> render rules** so the SKILL.md body stays a step-by-step ≤500-line guide. **Zero project values here** — every
> bracketed `{…}` token is a caller/instance-supplied input, rendered into the placeholder at runtime. The class set,
> the acceptance threshold, the abstain/rejection class name, the latency caveat text, and the privacy policy are all
> external inputs, never hardcoded.

## Interface-text language is instance-driven (the English below is a placeholder)
The **interface text** in this skeleton — `Eval Report`, `Per-class accuracy`, `Errors`, `Correct (sampled)`,
`Latency distribution`, `Caveats`, the `PASS`/`FAIL`/`MISSING` markers, etc. — is written in English **as a default
placeholder**. Render it in the **project language policy's language** (an instance value, set `lang="{REPORT_LANG}"`
to match; see SKILL.md "Report-interface language"). **Data keys are rendered verbatim, never translated**: class ids,
`{MODEL_SHA}`, `{DATA_VERSION}`, `{RUNTIME}`, version strings, and the `{CLASS}`/`{TRUE_LABEL}`/`{PRED_LABEL}` values
are data, not interface — keep them as-is. If the policy is Chinese, `polishing-chinese-prose` is the prose authority.

> **Non-ASCII encoding (portability — field lesson).** Any non-ASCII interface text requires: the **source file saved
> as UTF-8** and the HTML declaring **`<meta charset="utf-8">`** (already in the skeleton). **If the report is emitted
> by a compiled program, the build must set the source encoding to UTF-8 explicitly** (e.g. MSVC `/utf-8`) — relying on
> the host codepage happens to work on one machine and renders **mojibake on another**. Set it at the build, don't
> trust the default.

## Self-containment invariants (non-negotiable)
- **One file, no sidecars.** CSS is inlined in a single `<style>`; every image is a `data:` URI (base64). The report
  must open offline with no network and no external asset.
- **Images are base64 data-URIs**: `<img src="data:image/png;base64,{B64}">`. The `{B64}` is supplied by the **caller**,
  **already de-identified and already encoded** (image-input contract, SKILL.md §Inputs/R5) — the skill inlines it, it
  does **not** encode pixels and never receives raw image bytes. A non-de-identified or un-vetted image must never reach
  this template.
- **No analytics, no remote fonts, no CDN.** A self-contained artifact stays self-contained.

## Document skeleton
```html
<!DOCTYPE html>
<html lang="{REPORT_LANG}">
<head>
<meta charset="utf-8">
<title>Eval Report — {MODEL_NAME} @ {DATE}</title>
<style>/* see "Inline CSS" below */</style>
</head>
<body>
  <!-- 1. provenance header  -->
  <!-- 2. per-class accuracy table -->
  <!-- 3. confusion matrix -->
  <!-- 4. sample gallery (all errors + sampled correct) -->
  <!-- 5. latency distribution + caveats -->
</body>
</html>
```

## Inline CSS (minimal, dependency-free)
A small neutral stylesheet — system fonts only (no remote font), scannable tables, a clear pass/fail color, a muted
caveat block. Adjust spacing/scale freely; keep it self-contained.
```css
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:2rem;color:#1a1a1a;line-height:1.5}
h1,h2{border-bottom:1px solid #ddd;padding-bottom:.3rem}
.prov{display:flex;flex-wrap:wrap;gap:1rem;background:#f6f8fa;border:1px solid #e1e4e8;border-radius:6px;padding:.8rem 1rem;font-size:.92rem}
.prov b{color:#444}
.miss{color:#b00;font-weight:700}            /* R1 MISSING marker */
table{border-collapse:collapse;width:100%;margin:.6rem 0}
th,td{border:1px solid #d0d7de;padding:.35rem .6rem;text-align:center}
th{background:#f1f3f5}
.pass{color:#0a7d28;font-weight:700}          /* >= threshold */
.fail{color:#b00;font-weight:700}             /* <  threshold */
.cm-abstain{background:#fff7e6}               /* abstain/rejection column highlight (R3) */
.gallery{display:flex;flex-wrap:wrap;gap:.6rem}
.tile{border:1px solid #d0d7de;border-radius:6px;padding:.4rem;width:180px;font-size:.8rem;text-align:center}
.tile.err{border-color:#b00}
.tile img{width:100%;height:auto;border-radius:4px}
.caveat{background:#fff7e6;border:1px solid #f0c36d;border-radius:6px;padding:.6rem .9rem;font-size:.9rem;margin:.6rem 0}
.caveat.warn{background:#fdecea;border-color:#e0a3a0}   /* caveats-not-declared warning (R4) */
/* training-experiment report (parallel skeleton) */
.curve{max-width:520px;border:1px solid #d0d7de;border-radius:6px;margin:.4rem 0}
.verdict-kept{color:#0a7d28;font-weight:700}
.verdict-reverted{color:#b00;font-weight:700}
.verdict-incon{color:#9a6700;font-weight:700}
.tag-meas{background:#e6f4ea;color:#0a7d28;border-radius:3px;padding:0 .3rem;font-size:.78rem}   /* R6 measured */
.tag-inf{background:#fff7e6;color:#9a6700;border-radius:3px;padding:0 .3rem;font-size:.78rem}     /* R6 inferred */
.tag-unl{background:#fdecea;color:#b00;border-radius:3px;padding:0 .3rem;font-size:.78rem}        /* R6 unlabelled */
.limits{background:#f6f8fa;border:1px solid #e1e4e8;border-radius:6px;padding:.6rem .9rem}
```

## Section 1 — Provenance header (R1, mandatory)
Render the four required fields. **Any missing field → a visible `MISSING` marker** (`<span class="miss">MISSING</span>`),
never silently omitted.
```html
<h1>Eval Report</h1>
<div class="prov">
  <span><b>Data version:</b> {DATA_VERSION|MISSING}</span>
  <span><b>Model sha:</b> {MODEL_SHA|MISSING}</span>
  <span><b>Runtime:</b> {RUNTIME|MISSING}</span>
  <span><b>Date:</b> {DATE|MISSING}</span>
</div>
```

## Section 2 — Per-class accuracy table
One row per class; compare each accuracy against the **instance-supplied** `{ACCEPTANCE_THRESHOLD}` and render a
pass/fail mark. The skill renders the comparison; it does not know the threshold number.
```html
<h2>Per-class accuracy <small>(threshold: {ACCEPTANCE_THRESHOLD})</small></h2>
<table>
  <tr><th>class</th><th>accuracy</th><th>support</th><th>vs threshold</th></tr>
  <!-- per class: -->
  <tr><td>{CLASS}</td><td>{ACC}</td><td>{SUPPORT}</td>
      <td class="{pass|fail}">{PASS or FAIL mark}</td></tr>
</table>
```

## Section 3 — Confusion matrix (R3 — abstain/rejection column is first-class)
Rows = true classes; columns = predicted classes **including the abstain/rejection column** (highlight it). Surface the
**abstention/rejection rate** as a headline line above or below the matrix — not buried.
```html
<h2>Confusion matrix</h2>
<p><b>Abstain/Reject rate: {ABSTAIN_RATE}</b> — {one-line note on what the abstain class means here}</p>
<table>
  <tr><th>true \ pred</th> <!-- predicted class headers... --> <th class="cm-abstain">{ABSTAIN_CLASS}</th></tr>
  <!-- per true class row; the abstain column cell carries class="cm-abstain" -->
  <tr><th>{TRUE_CLASS}</th> <!-- counts... --> <td class="cm-abstain">{COUNT}</td></tr>
</table>
```
> Generic note: `{ABSTAIN_CLASS}` is whatever the project's rejecting classifier returns when nothing matches; the
> skill does not name it. The column is always present even if its counts are zero.

## Section 4 — Sample gallery (R2 — all errors, sampled correct)
Two strips. The **error strip carries every error case** (do not cap/sample); the correct strip is a **sample**.
Each error tile shows the image (with overlay already drawn in) and **true → predicted** labels.
```html
<h2>Errors <small>(all {N_ERRORS} cases)</small></h2>
<div class="gallery">
  <!-- per error case (ALL of them): -->
  <div class="tile err">
    <img src="data:image/png;base64,{B64_OVERLAY}">
    <div>{TRUE_LABEL} → <b>{PRED_LABEL}</b></div>
  </div>
</div>

<h2>Correct (sampled) <small>(showing {K} of {N_CORRECT})</small></h2>
<div class="gallery">
  <!-- a SAMPLE of correct predictions: -->
  <div class="tile">
    <img src="data:image/png;base64,{B64}">
    <div>{LABEL}</div>
  </div>
</div>
```
> R2 rationale: sampling the error strip could hide a systematic failure mode; collecting every error is the point.
> Overlays (keypoints / detected region / heatmap) are drawn by the caller and baked into the image before embedding.

## Section 5 — Latency distribution + caveats (R4)
Render the distribution figures **with** the caller-supplied caveat text. **No caveat text → a visible warning**, never
bare numbers (latency without scope is misleading).
```html
<h2>Latency distribution</h2>
<table>
  <tr><th>p50</th><th>p90</th><th>max</th></tr>
  <tr><td>{P50}</td><td>{P90}</td><td>{MAX}</td></tr>
</table>
<!-- caveats present: render each line verbatim from the caller -->
<div class="caveat"><b>Caveats (scope of these numbers):</b>
  <ul>{per CAVEAT_LINE: <li>{CAVEAT_LINE}</li>}</ul>
  <i>Not comparable to a deployment-gate latency.</i>
</div>
<!-- caveats absent: -->
<div class="caveat warn"><b>⚠ Latency caveats not declared</b> — these figures lack the scope that makes them
interpretable; treat as unscoped.</div>
```

## Training-experiment report — parallel skeleton (same head/CSS/invariants)
The training-experiment / ablation type reuses the **same `<head>`, the same inline CSS, and every self-containment +
privacy invariant** above. Only the `<body>` sections differ. Document skeleton:
```html
<body>
  <!-- 1. provenance header (R1, same four fields; model_sha = trained checkpoint/config) -->
  <!-- 2. abstract / summary -->
  <!-- 3. experiment-ladder table -->
  <!-- 4. training curves (inline base64) -->
  <!-- 5. ablation comparison table -->
  <!-- 6. limitations (consolidated) -->
</body>
```
**R6 measured-vs-inferred mark (rendered next to every number).** A small inline tag; an unmarked number gets the
red `unlabelled` tag, never silently presented as measured:
```html
<span class="tag-meas">measured</span>   <!-- caller marked: actually run -->
<span class="tag-inf">inferred</span>     <!-- caller marked: extrapolated/projected -->
<span class="tag-unl">unlabelled</span>   <!-- caller supplied no mark — visible, never silent -->
```

### T-Section 1 — Provenance header (R1, mandatory)
Identical to the eval provenance band (same four fields, same `MISSING` rule).

### T-Section 2 — Abstract / summary
```html
<h1>Training-experiment report</h1>
<!-- provenance band here (T-Section 1) -->
<h2>Summary</h2>
<p>{ABSTRACT_TEXT}</p>   <!-- numbers inside carry an R6 tag -->
```

### T-Section 3 — Experiment-ladder table
One row per round: the single variable changed, the hypothesis, the result (R6-tagged numbers), the verdict.
```html
<h2>Experiment ladder</h2>
<table>
  <tr><th>round</th><th>variable</th><th>hypothesis</th><th>result</th><th>verdict</th></tr>
  <!-- per round: -->
  <tr><td>{ROUND}</td><td>{VARIABLE}</td><td>{HYPOTHESIS}</td>
      <td>{RESULT} <span class="{tag-meas|tag-inf|tag-unl}">{mark}</span></td>
      <td class="{verdict-kept|verdict-reverted|verdict-incon}">{VERDICT}</td></tr>
</table>
```
> Verdict text is the caller's (kept / reverted / inconclusive — the skill does not judge); the class only colors it.

### T-Section 4 — Training curves (inline base64)
```html
<h2>Training curves</h2>
<!-- per curve (already plotted + de-identified by the caller): -->
<figure>
  <img class="curve" src="data:image/png;base64,{B64_CURVE}">
  <figcaption>{CURVE_CAPTION}</figcaption>
</figure>
```

### T-Section 5 — Ablation comparison table
Rows = configurations (components on/off); each metric cell R6-tagged.
```html
<h2>Ablation</h2>
<table>
  <tr><th>configuration</th><!-- metric headers... --></tr>
  <!-- per config: -->
  <tr><td>{CONFIG}</td>
      <td>{METRIC} <span class="{tag-meas|tag-inf|tag-unl}">{mark}</span></td></tr>
</table>
```

### T-Section 6 — Limitations (consolidated)
```html
<h2>Limitations</h2>
<div class="limits"><ul>{per LIMITATION: <li>{LIMITATION}</li>}</ul></div>
```
> Consolidate limitations in one closing block — not scattered footnotes. This is a quality rule of the training type.

## Privacy + destination (R5) — applied during render, not a section
- Images arrive **already de-identified and already base64-encoded by the caller** (image-input contract); the skill
  inlines the supplied base64, it does not encode pixels and never receives raw bytes. If no privacy policy is supplied
  (so the caller's de-identification cannot be assumed), **do not embed the imagery** — render a placeholder tile and flag it.
- The finished `.html` is by default a **local artifact, not committed to git**. Its delivery (attach / copy to a share
  / send) is **instance-governed**; this template does not assume a destination. Outward delivery is confirm-when-unsure.
