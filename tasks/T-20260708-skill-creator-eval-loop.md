---
id: T-20260708-skill-creator-eval-loop
risk: R1
state: AcceptancePassed
scope_in:
  - "tools/skill_creator.py"
  - "bin/vemo-skills"
  - "eval/**"
  - "skills/governance/authoring-skills-with-evals/**"
  - "README.md"
  - "README_zh.md"
  - "CHANGELOG.md"
  - "VERSION"
  - "docs/CRITIQUE_LOG.md"
  - "tasks/T-20260708-skill-creator-eval-loop.md"
acceptance:
  status: passed
  build_exit: 0
  smoke_exit: 0
  evidence: "selfcheck 10.00/10; eval 13/13; author-selftest 11/11; sensitive scan clean"
judge:
  required: false
  verdict: null
owning_chat: local-improvement
heartbeat: 2026-07-08T00:00
---

# Add eval-driven skill authoring (skill-creator harness)

## Goal
Give the skill home the behavioral / trigger-evaluation layer it lacked — modeled on Anthropic's official
skill-creator — while keeping the release scorer at 10/10 and every gated dimension green.

## Scope (In / Out)
- In: the authoring harness, its CLI + eval wiring, the new authoring skill, and the catalog/version docs it obliges.
- Out: the release scorer's dimensions and weights (unchanged); any project-identity values (red line); adoption.

## Pass/Fail Criteria
- [Core] `python3 tools/skill_creator.py selftest` SHALL exit 0 (deterministic split, validate, marker, aggregation).
- [Skill] the new `governance/authoring-skills-with-evals` SHALL validate and carry a tier-honest marker.
- [Parity] README.md and README_zh.md catalog tokens SHALL equal the skill tree (24 skills) as multisets.
- [Gate] `python3 bin/vemo-skills selfcheck` SHALL be >= 9.5 with every gated dimension PASS; `eval` passed==total.
- [Decoupling] no private paths, credentials, or internal source names on the surface.

## Plan
- Build `tools/skill_creator.py` (validate + marker, trigger-eval tri-state, describe-improve train/test, selftest),
  reusing the repo's single frontmatter parser.
- Wire four CLI verbs + two eval conformance checks.
- Add the authoring skill + reference doc; bump VERSION/CHANGELOG; keep both READMEs in parity.

## Execution Log
- 2026-07-08: added `skill_creator.py`; `selftest` 11/11.
- 2026-07-08: wired CLI + eval; `eval` 13/13, score 10.00/10.
- 2026-07-08: added the authoring skill + reference; `validate` PASS, marker tier=lint.
- 2026-07-08: catalog/version/changelog updated in both languages; `selfcheck` 10.00/10.

## Acceptance Result
All criteria PASS (evidence above). The two model-in-the-loop commands degrade gracefully without the `claude` CLI.

## Conclusion
Outcome: accepted · Decision: continue · Key Evidence: selfcheck 10.00/10, eval 13/13, author-selftest 11/11 ·
Risk: low · Next Action: consider a `tier: "trigger"` upgrade once eval-set fixtures are curated per skill.
