# Changelog · VEMO_SKILLS

All notable public changes to this repository are documented here.

This project uses semantic versioning for public releases. Generic skill bodies,
catalog metadata, executable checks, and documentation are kept in the same
release so consumers can pin a complete skill home by tag.

## [1.3.0] - Unreleased

### Added
- New governance skill `governing-project-fleets`, which operates VEMO's private PC-wide control plane through a
  consent-gated inventory -> profile -> register -> assess -> preview -> apply -> verify workflow. It keeps discovery
  read-only, refuses force-overwrite guidance, and separates local readiness from certification or remote authority.
- New orchestration skill `designing-diagnostic-prompts`, which turns Human 3.0-style self-discovery and Mr. Ranedeer-style
  tutoring patterns into a generic prompt/agent design workflow: intake, configuration, constraint finding, plan, loop,
  and boundary.
- `docs/PLAYBOOK_GENERALIZATION.md`: guidance for converting repo-local playbook procedures into reusable shared skills.

### Changed
- Catalog grows 28 -> 30 skills; README.md and README_zh.md catalog rows, layout, badge, and keyword-trigger table kept
  in parity.
- `bin/vemo-skills` and `eval/run.py` now use the current Python interpreter instead of hardcoding `python3`, improving
  Windows support.
- GitHub pull requests and main pushes now run selfcheck + executable eval under a least-privilege, concurrency-bounded
  workflow with checkout pinned to the verified v6.0.2 commit.

## [1.2.0] — 2026-07-08

### Added
- Four on-device CV/ML model-lifecycle skills under `code/`, filling the pre-deployment gap
  (export -> quantize -> evaluate) the deployment-side skills did not cover:
  - `converting-pytorch-to-tflite` — PyTorch/ONNX -> mobile TFLite with first-conv colour-fold,
    multi-stem awareness, deploy-before-trace, and a PyTorch-vs-TFLite parity gate.
  - `loading-model-checkpoints` — robust state_dict loading (prefix by max key-overlap, loud
    diagnostics, arch/in-channel inference, weights_only security caveat).
  - `evaluating-segmentation-models` — IoU/mIoU + boundary-F for masks; SAD/MSE/Grad/Conn in the
    trimap band for matting; per-class + edge-aware; decision-space parity.
  - `quantizing-on-device-models` — fp16 -> int8-dynamic -> full-int8 PTQ -> QAT ladder with
    per-channel/asymmetry, sensitive-layer-float, and an accuracy-vs-latency gate.
- Reference modules: `converting-pytorch-to-tflite/references/export-gotchas.md`,
  `evaluating-segmentation-models/references/metrics.md`.

### Changed
- Catalog grows 24 -> 28 skills; README.md and README_zh.md catalog rows, layout, badge, and
  keyword-trigger table kept in parity.

### Verification
- `python3 bin/vemo-skills selfcheck` (10.00/10) · `python3 bin/vemo-skills eval` · each new skill validated.

## [1.1.0] — 2026-07-08

### Added
- Eval-driven skill authoring harness `tools/skill_creator.py`, modeled on Anthropic's official skill-creator:
  `validate` (frontmatter + naming lint, then a tamper-evident `.skill-validated.json` provenance marker carrying an
  explicit, honest `tier`), `trigger-eval` (per-run tri-state trigger measurement that reports an infrastructure
  failure as *skipped* — never as a missed trigger), `describe-improve` (train/test-split description optimization
  that selects the winner by held-out score), and a hermetic `selftest`.
- New skill `governance/authoring-skills-with-evals` documenting the eval-driven loop, with `references/eval-loop.md`.
- CLI commands `validate`, `trigger-eval`, `describe-improve`, and `author-selftest` on `bin/vemo-skills`.
- Two executable-eval conformance checks: the authoring harness is present and its selftest passes.

### Changed
- Catalog grows to 24 skills; `README.md` and `README_zh.md` catalog rows, layout lines, and badges kept in parity.
- Completed the `governance/` layout line (it previously omitted `polishing-chinese-prose`).

### Verification
- `python3 bin/vemo-skills selfcheck` (10.00/10)
- `python3 bin/vemo-skills eval`
- `python3 bin/vemo-skills author-selftest`

## [1.0.0] — 2026-06-17

### Added
- Initial public release of `VEMO_SKILLS` as an independent skill-home repository.
- 23 reusable skills across `orchestration`, `governance`, `research`, `code`, and `visualization`.
- Bilingual public entry docs: `README.md` and `README_zh.md`.
- Repository-local visual assets under `assets/`: logo, lifecycle diagram, catalog map, and social-preview source.
- CLI entrypoint `bin/vemo-skills` with `status`, `catalog`, `score`, `selfcheck`, `eval`, and `bind` commands.
- Deterministic checker `tools/vemo_skills_check.py` for catalog parity, frontmatter, naming, references, binding,
  version hygiene, public docs, security decoupling, executable verification, and attribution governance.
- Executable eval suite `eval/run.py`, writing its current report to `eval/out/report.json`.
- Public project docs: `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `docs/INDEX.md`, `docs/QUICKSTART.md`, and
  `docs/CRITIQUE_LOG.md`.
- Public release task record `tasks/T-20260617-vemo-skills-release.md`.

### Changed
- Normalized the repository surface for public GitHub readers: examples are account-neutral, path-neutral, and
  consumer-oriented.
- Replaced internal baseline/report references with public selfcheck and eval evidence.
- Scrubbed private source labels, local paths, and internal framework names from the public release surface.

### Verification
- `python3 bin/vemo-skills selfcheck`
- `python3 bin/vemo-skills eval`
- Sensitive-reference scans for local paths, credentials, and internal source names.
