# VEMO_SKILLS agent guide

This repo is a shared skill home. Treat `skills/**/SKILL.md` as the product surface and keep generated copies out of
git.

## Required checks
- Run `python3 bin/vemo-skills selfcheck` before declaring a release-ready change.
- Run `python3 bin/vemo-skills eval` when changing the checker, catalog rules, release docs, or any skill layout.
- Keep `README.md` and `README_zh.md` catalog rows in parity with `skills/*/*/SKILL.md`.

## Editing rules
- Generic skill bodies carry no project ids, chat ids, local paths, or account names.
- Add or move skills through the `publishing-skills` procedure.
- The release-ready score threshold is `9.5/10`.
