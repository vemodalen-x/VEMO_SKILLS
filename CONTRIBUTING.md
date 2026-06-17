# Contributing

VEMO_SKILLS governs a reusable skill home. Contributions should preserve three invariants:

- `skills/<category>/<name>/SKILL.md` frontmatter is the source of truth for `name` and `category`.
- README catalog tokens match the skill tree in both English and Chinese READMEs.
- Generic skill bodies contain no project-specific values; those belong in the consuming project instance.

## Local checks
```bash
python3 bin/vemo-skills selfcheck
python3 bin/vemo-skills eval
```

## Pull requests
- Keep changes scoped to one skill, one category move, or one release/tooling change.
- Update `CHANGELOG.md`, `VERSION`, and docs when the public surface changes.
- Include evidence from the local checks in the PR description.
