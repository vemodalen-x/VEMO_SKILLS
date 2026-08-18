# T-20260818 · Plugin contract adaptation

## Goal

Align all registered VEMO_SKILLS packages with the current skill contract and VEMO's declarative
everything-is-a-plugin architecture without adding an executable plugin runtime.

## Scope

- Standardize source frontmatter and strict YAML parsing for all 30 skills.
- Add `skills/index.json` as the explicit activation surface.
- Add generated, validated `agents/openai.yaml` UI metadata to every package.
- Make checker, catalog, bind, authoring harness, eval, conventions, and bilingual docs consume the new contract.
- Remove tracked generated validation markers; keep optional markers ephemeral.
- Exclude marketplace installation, runtime code loading, tags, and direct default-branch pushes.

## Acceptance

- Official `quick_validate.py`: 30/30 skill packages pass.
- `python3 bin/vemo-skills selfcheck`: at least 9.5/10.
- `python3 bin/vemo-skills eval`: all checks pass, including real index-driven temporary binding.
- `python3 bin/vemo-skills author-selftest`: all deterministic authoring checks pass.
- Index, filesystem tree, README/README_zh catalogs, and OpenAI metadata remain in exact package-count parity.
- Change lands on a feature branch under the repository's PR-only policy.

## Design

`SKILL.md` owns model-visible identity, triggers, and procedure. `agents/openai.yaml` owns product UI metadata.
`skills/index.json` owns activation and path-derived classification. The binder copies only activated package
folders, preserving optional resources byte-for-byte. Registration still does not imply adoption; consumers retain
the consent decision.

## Evidence

- Baseline internal selfcheck passed 10/10 while the current official validator rejected legacy `category` metadata.
- Official `quick_validate.py`: 30/30 packages passed.
- `python3 bin/vemo-skills selfcheck`: 10.00/10.0.
- `python3 bin/vemo-skills eval`: 16/16, including duplicate-key, duplicate-catalog-row, flattened-name,
  inert-tree, fail-closed bind, and real temporary binding coverage.
- `python3 bin/vemo-skills author-selftest`: 11/11.
- Package parity: 30 indexed `SKILL.md` files, 30 `agents/openai.yaml` files, 30 catalog entries, and zero
  source validation markers.
- Code review found and resolved two ambiguity paths: partial binding from an invalid index and silent overwrite
  from duplicate flattened package names. The change is prepared on `feat/plugin-contract-adaptation` under the
  repository's PR-only policy.
