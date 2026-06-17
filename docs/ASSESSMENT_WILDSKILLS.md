# Wildskills baseline assessment

Date: 2026-06-17  
Method: `python3 tools/vemo_skills_check.py --root <source-skill-home> score`

## Score
`6.55/10.0`

## Strengths
- Skill catalog parity is clean: 23 skill rows match the `skills/*/*/SKILL.md` tree.
- Frontmatter layout is consistent: each skill declares `name`, `category`, and `description`.
- The source already documents the regen model and generic/instance decoupling.

## Gaps against the VEMO-style release bar
- No VEMO-style CLI, selfcheck, executable eval, or score report.
- No standalone public-release docs set: security, roadmap, contribution guide, docs index, quickstart, critique log.
- No task record and no `.gitignore` for generated `.claude/skills/**` copies.
- One local reference citation is path-dangling from the checker viewpoint.
- Public identity cleanup is incomplete for upload-ready packaging.

## Verdict
Good skill-home content, not yet a complete VEMO-style release artifact. The target repo must add executable evidence,
public packaging, and a release threshold before upload.
