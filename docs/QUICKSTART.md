# VEMO_SKILLS Quickstart

VEMO_SKILLS is a source-of-truth skill hub. Consumers pin the hub, regenerate
working skill copies, and use those skills through natural-language triggers.

## 1. Get the Hub

Use either a submodule or a normal clone.

```bash
git submodule add <repo-url> .governance/VEMO_SKILLS
git -C .governance/VEMO_SKILLS checkout v1.0.0
```

For a standalone clone:

```bash
git clone <repo-url> VEMO_SKILLS
cd VEMO_SKILLS
```

## 2. Inspect the Catalog

```bash
python3 bin/vemo-skills catalog
```
On Windows, use `python bin/vemo-skills ...` if `python3` is not installed.

Each line is a stable `<category>/<skill>` token activated by `skills/index.json` and backed by
`skills/<category>/<skill>/SKILL.md`.

## 3. Bind Skills into a Consumer Project

From the hub root:

```bash
python3 bin/vemo-skills bind --dest ../consumer-project/.claude/skills
```

The bind command copies each index-activated skill folder, including `agents/openai.yaml` and any `references/`,
and flattens the category level:

```text
skills/<category>/<name>/ -> .claude/skills/<name>/
```

Treat `.claude/skills/` as generated output. Edit the source skill in this hub,
then bind again.

## 4. Verify the Hub

```bash
python3 bin/vemo-skills selfcheck
python3 bin/vemo-skills eval
```

The public release threshold is `9.5/10`. The eval command writes
`eval/out/report.json`.

## 5. Publish a Skill Change

Use the normal GitHub flow:

1. Edit or add the package under `skills/<category>/<name>/`; activate new packages in `skills/index.json`.
2. Generate and validate `agents/openai.yaml` for new packages.
3. Keep `README.md` and `README_zh.md` catalog rows in parity.
4. Update `CHANGELOG.md`.
5. Run `python3 bin/vemo-skills selfcheck` and `python3 bin/vemo-skills eval`.
6. Open a pull request.
