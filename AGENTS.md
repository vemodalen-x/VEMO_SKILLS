# VEMO_SKILLS agent guide

This repo is a shared skill home. Treat `skills/index.json` as the activation surface and each indexed skill folder
as an independently bindable package. Keep generated copies and validation markers out of git.

## Required checks
- Run `python3 bin/vemo-skills selfcheck` before declaring a release-ready change.
- Run `python3 bin/vemo-skills eval` when changing the checker, catalog rules, release docs, or any skill layout.
- Keep `skills/index.json`, `skills/*/*/SKILL.md`, `agents/openai.yaml`, and both README catalogs in parity.

## Editing rules
- Generic skill bodies carry no project ids, chat ids, local paths, or account names.
- Add or move skills through the `publishing-skills` procedure.
- The release-ready score threshold is `9.5/10`.
