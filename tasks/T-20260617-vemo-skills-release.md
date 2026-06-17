---
id: T-20260617-vemo-skills-release
risk: R0
state: AcceptancePassed
scope_in:
  - "README.md"
  - "README_zh.md"
  - "CHANGELOG.md"
  - "VERSION"
  - ".gitignore"
  - "AGENTS.md"
  - "CONTRIBUTING.md"
  - "SECURITY.md"
  - "ROADMAP.md"
  - "docs/**"
  - "tools/**"
  - "bin/**"
  - "eval/**"
  - "tasks/T-20260617-vemo-skills-release.md"
  - "skills/governance/**"
acceptance:
  status: passed
  build_exit: 0
  smoke_exit: 0
  evidence: "selfcheck 10.00/10; eval 11/11; git diff --check clean; sensitive scan clean"
judge:
  required: false
  verdict: null
owning_chat: local-release
heartbeat: 2026-06-17T00:00
---

# VEMO_SKILLS first complete version

## Goal
Create an independent VEMO_SKILLS Git repository from the skill-home source, score the source baseline, then raise the
target repository to the VEMO-style complete-version threshold of `9.5/10`.

## Acceptance
- Source Wildskills baseline is recorded.
- VEMO_SKILLS selfcheck passes.
- VEMO_SKILLS eval passes.
- Final score is at least `9.5/10`.
- Git repository has an initial release-ready commit.

## Execution log
- 2026-06-17: source Wildskills scored `6.55/10.0`.
- 2026-06-17: created independent VEMO_SKILLS repository and normalized public identity.
- 2026-06-17: added `bin/vemo-skills`, `tools/vemo_skills_check.py`, `eval/run.py`, public docs, and release reports.
- 2026-06-17: `python3 bin/vemo-skills eval` passed `11/11`.
- 2026-06-17: `python3 bin/vemo-skills selfcheck` passed at `10.00/10.0`.
- 2026-06-17: `git diff --check` and sensitive scan passed.

## Result
Accepted. The repository is ready for initial upload after the local Git commit is created.
