# Quickstart

## 1. Inspect the skill catalog
```bash
python3 bin/vemo-skills catalog
```

## 2. Run the release self-check
```bash
python3 bin/vemo-skills selfcheck
```

The checker scores the repository against the release threshold, currently `9.5/10`.

## 3. Run executable eval
```bash
python3 bin/vemo-skills eval
```

This writes `eval/out/report.json` and proves that the catalog, frontmatter, reference, docs, release, and security
checks all fire.

## 4. Regenerate working copies for a consuming project
```bash
python3 bin/vemo-skills bind --dest .claude/skills
```

The destination is a build artifact. Do not edit generated copies by hand; edit `skills/<category>/<name>/` here and
regenerate.
