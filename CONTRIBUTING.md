# Contributing

VEMO_SKILLS governs a reusable skill home. Contributions should preserve three invariants:

- `SKILL.md` frontmatter owns model-visible identity/triggering; `skills/index.json` owns activation and path-derived category.
- Activation index, skill tree, and both README catalogs contain the same skill identities.
- Every registered package carries valid `agents/openai.yaml` UI metadata.
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
