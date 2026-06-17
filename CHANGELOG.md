# Changelog · VEMO_SKILLS

All notable public changes to this repository are documented here.

This project uses semantic versioning for public releases. Generic skill bodies,
catalog metadata, executable checks, and documentation are kept in the same
release so consumers can pin a complete skill home by tag.

## [1.0.0] — 2026-06-17

### Added
- Initial public release of `VEMO_SKILLS` as an independent skill-home repository.
- 23 reusable skills across `orchestration`, `governance`, `research`, `code`, and `visualization`.
- Bilingual public entry docs: `README.md` and `README_zh.md`.
- Repository-local visual assets under `assets/`: logo, lifecycle diagram, catalog map, and social-preview source.
- CLI entrypoint `bin/vemo-skills` with `status`, `catalog`, `score`, `selfcheck`, `eval`, and `bind` commands.
- Deterministic checker `tools/vemo_skills_check.py` for catalog parity, frontmatter, naming, references, binding,
  version hygiene, public docs, security decoupling, executable verification, and attribution governance.
- Executable eval suite `eval/run.py`, writing its current report to `eval/out/report.json`.
- Public project docs: `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `docs/INDEX.md`, `docs/QUICKSTART.md`, and
  `docs/CRITIQUE_LOG.md`.
- Public release task record `tasks/T-20260617-vemo-skills-release.md`.

### Changed
- Normalized the repository surface for public GitHub readers: examples are account-neutral, path-neutral, and
  consumer-oriented.
- Replaced internal baseline/report references with public selfcheck and eval evidence.
- Scrubbed private source labels, local paths, and internal framework names from the public release surface.

### Verification
- `python3 bin/vemo-skills selfcheck`
- `python3 bin/vemo-skills eval`
- Sensitive-reference scans for local paths, credentials, and internal source names.
