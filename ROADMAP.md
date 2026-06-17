# Roadmap

## Near term
- Add a `--json` output mode for `vemo-skills score` for CI dashboards.
- Add a generated catalog page with one card per skill and direct reference-file links.
- Add transcript-level eval fixtures for skill publishing and regen workflows.

## Mid term
- Add CI examples for GitHub Actions and self-hosted runners.
- Add optional package export: `vemo-skills bundle --format zip`.
- Add drift checks for copied `.claude/skills/**` trees in consuming projects.

## Out of scope
- Runtime enforcement inside consuming projects; that belongs to the project's governance framework.
- Project-specific values, chat identities, wiki ids, model names, or release channels.
