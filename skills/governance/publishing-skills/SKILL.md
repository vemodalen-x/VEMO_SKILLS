---
name: publishing-skills
description: 'Publish a skill into a shared skill home using standard name/description frontmatter, an explicit functional category, and the canonical category/name directory path; then update bilingual catalogs, validation evidence, versioning, and regeneration checks. Use when adding, moving, renaming, or removing a skill in VEMO_SKILLS or another category-based skill home. Placement and registration only; adopting the skill into a consumer remains a user-consent decision.'
---

# Publishing Skills

Register a skill in the shared home without adding repository-specific fields to its portable frontmatter. The
directory owns functional classification; `SKILL.md` remains compatible with standard Codex/Agent Skills tooling.

## Model

- **Portable frontmatter:** require `name` and `description`; allow only standard optional fields. Do not add a
  top-level `category` extension.
- **Explicit category:** obtain category from the existing path for updates, or from an explicit author/publisher
  input for a new skill. Never infer it silently from prose.
- **Canonical identity:** `skills/<category>/<name>/`, where `<name>` equals frontmatter `name` and `<category>` is the
  immediate parent directory.
- **Declare and create:** categories are functional groupings, not a fixed enum. Create a new category directory only
  when the author explicitly selected it.
- **Registration is not adoption:** publishing makes a skill available in the home. A consuming project still decides
  whether to bind and activate it.
- **README is part of the product:** English and Chinese catalog rows, layout lists, prompt examples, and trigger rows
  stay in parity with the tree.

## Preconditions

1. Confirm the target is a skill home with `skills/`, `README.md`, `VERSION`, and `CHANGELOG.md`.
2. Resolve `name` from frontmatter and validate it with `naming-skills`.
3. Resolve category:
   - existing skill: use its current `skills/<category>/` parent;
   - move: require the requested destination category;
   - new unplaced skill: require an explicit category argument or author decision.
4. Reject a top-level `category` field and migrate it to directory placement before publication.
5. Check for an existing skill with the same name in any category and classify the operation as add, update, move,
   rename, or remove.

## Publish Flow

### 1. Validate the portable skill

Run the authoring validator. Block on invalid frontmatter, non-gerund or mismatched names, missing trigger language,
unresolved references, private paths/identities, credentials, or project-specific policy embedded in the body.

### 2. Place the canonical source

Set the target to `skills/<category>/<name>/`. For a move or rename, use `git mv` so history remains visible. Copy only
the required `SKILL.md` plus directly used `scripts/`, `references/`, `assets/`, or `agents/` resources. Do not add
auxiliary per-skill README or changelog files.

### 3. Maintain the catalogs

Update both `README.md` and `README_zh.md`:

- catalog row token: `<category>/<name>`, derived from directory plus frontmatter name;
- concise does, when-to-use, and boundary cells;
- category layout list;
- prompt example and keyword-trigger row when user-triggered;
- total skill count and generated category visualization when those surfaces exist.

The path is the category source of truth. Do not duplicate category into skill frontmatter merely to generate a table.

### 4. Record release metadata

Add a changelog entry naming the skill and category. Follow the current unreleased release train; do not create a
second unreleased version block unnecessarily. Keep README version references indirect through `VERSION` and the
changelog.

### 5. Validate the whole home

Run:

```bash
python bin/vemo-skills selfcheck
python bin/vemo-skills author-selftest
python bin/vemo-skills eval
```

The checks must establish:

- every `skills/*/*/SKILL.md` has standard frontmatter;
- frontmatter name equals the skill directory;
- category is derived from the category directory;
- English and Chinese catalog token sets equal the skill-tree token set;
- references resolve and public files contain no private identity/path/secret values;
- the release score meets the repository threshold.

When model-in-loop tooling exists, run trigger evals with positive and near-negative prompts. If unavailable, preserve
the honest `lint` validation tier and report the missing behavioral evidence.

### 6. Verify consumer regeneration

In a consuming project, regenerate into its configured skill discovery directory and compare the copy byte-for-byte
with the home source. Generated copies are build artifacts and must not become an alternate source of truth.

### 7. Submit through review

Use branch -> pull request -> merge. Report validation commands and evidence in the PR. Tagging, announcement, and
consumer adoption happen through their own authorized workflows.

## Output Contract

Return the operation class, canonical skill token, changed files, catalog parity, validation tier, release metadata,
regeneration status, remaining behavioral evidence, and PR/commit state.

## Boundaries

- Do not guess a new skill's category or add a non-standard frontmatter field for local convenience.
- Do not hardcode organization, account, project path, chat ID, or consumer policy.
- Do not adopt, merge, tag, announce, or publish externally without the corresponding authority.
- Do not claim behavioral validation when only lint and repository conformance ran.
