# Public Release Review Log

This log records the public-release review for VEMO_SKILLS v1.0.0.

## Review Scope

- Root public docs: `README.md`, `README_zh.md`, `CHANGELOG.md`, `CONTRIBUTING.md`,
  `SECURITY.md`, `ROADMAP.md`, `THIRD-PARTY-NOTICES.md`, and `CONVENTIONS.md`.
- Release tooling: `bin/vemo-skills`, `tools/vemo_skills_check.py`, and `eval/run.py`.
- Skill bodies under `skills/**/SKILL.md` and public reference modules under
  `skills/**/references/**`.
- Public release task record under `tasks/`.

## Findings Addressed

- Removed internal baseline report references from public docs and checker requirements.
- Replaced private contributor names and chat-source labels with an identity-light public ledger.
- Removed internal framework names and local source-path references from the public release surface.
- Added repository-local visuals so README images render from relative paths.
- Kept third-party attribution focused on external sources and license scope.

## Release Criteria

- `python3 bin/vemo-skills selfcheck` passes.
- `python3 bin/vemo-skills eval` passes.
- Sensitive-reference scans find no credentials, private paths, internal source names, or old source-baseline markers.
- `README.md` and `README_zh.md` include the same skill catalog tokens.

## Status

Ready for public v1.0.0 upload after the final verification commands pass.

## v1.1.0 — eval-driven skill authoring

### Gap addressed
- The static release scorer lints a skill's *shape* (naming, frontmatter, catalog parity) but never measures
  *behavior* — whether a description actually triggers, or whether the skill improves a result. A skill could score
  10/10 and still be useless. This adds the behavioral layer, mirroring the eval-driven loop of Anthropic's official
  skill-creator.

### Added
- `tools/skill_creator.py`: `validate` (+ honest-tier provenance marker), `trigger-eval` (tri-state; an
  infrastructure failure is *skipped*, not a missed trigger — the honest distinction the upstream harness omitted),
  `describe-improve` (train/test split, blinded to test scores, select-by-held-out-score), and a hermetic `selftest`.
- Skill `governance/authoring-skills-with-evals` (+ `references/eval-loop.md`).

### Design decisions
- Reuse the repo's single frontmatter parser rather than introduce a second, divergent one.
- The behavioral layer is additive: the release gate stays the static scorer; the harness is the authoring aid.
- Model-in-the-loop commands degrade gracefully without the `claude` CLI (report *skipped*, exit 0).

### Release criteria (posture unchanged)
- `python3 bin/vemo-skills selfcheck` >= 9.5 with every gated dimension green; `eval` passed==total;
  `author-selftest` green; sensitive-reference scan clean; `README.md` and `README_zh.md` catalog tokens equal.
