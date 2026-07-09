---
id: T-20260708-code-model-lifecycle-skills
risk: R1
state: AcceptancePassed
scope_in:
  - "skills/code/converting-pytorch-to-tflite/**"
  - "skills/code/loading-model-checkpoints/**"
  - "skills/code/evaluating-segmentation-models/**"
  - "skills/code/quantizing-on-device-models/**"
  - "README.md"
  - "README_zh.md"
  - "CHANGELOG.md"
  - "VERSION"
  - "tasks/T-20260708-code-model-lifecycle-skills.md"
acceptance:
  status: passed
  build_exit: 0
  smoke_exit: 0
  evidence: "selfcheck 10.00/10; eval 13/13; catalog 28; each skill validated tier=lint; sensitive scan clean"
judge:
  required: false
  verdict: null
owning_chat: local-improvement
heartbeat: 2026-07-08T00:00
---

# Add 4 on-device model-lifecycle code skills

## Goal
Fill the pre-deployment gap (export -> quantize -> evaluate) in the `code` category, grounded in the
recurring PyTorch->TFLite segmentation/matting workflow across this machine's projects, fully
decoupled from any project/identity value; keep the release scorer at 10/10.

## Acceptance
- The 4 new skills validate (tier=lint) and pass naming / frontmatter / reference rules.
- README.md and README_zh.md catalog tokens equal the tree (28) as multisets.
- selfcheck >= 9.5 with every gated dimension green; eval passed==total.
- No project/identity values on the surface (security_decoupling clean).

## Execution log
- 2026-07-08: authored converting-pytorch-to-tflite (+references/export-gotchas.md),
  loading-model-checkpoints, evaluating-segmentation-models (+references/metrics.md),
  quantizing-on-device-models — generalized from the source workflow notes, decoupled.
- 2026-07-08: catalog rows / layout / badge / keyword table updated in both languages; VERSION -> 1.2.0.
- 2026-07-08: selfcheck 10.00/10; eval 13/13; catalog lists 28.

## Result
Accepted. Grounded in the dominant on-device CV/ML workflow (seg/matting/bokeh, PyTorch->TFLite),
zero identity leakage; each skill composes with the existing deployment-side code skills.
