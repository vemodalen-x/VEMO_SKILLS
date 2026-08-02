# VEMO_SKILLS Home Conventions

This document defines the operating procedure of the shared skill home. Skill registration and skill adoption are
separate: this repository can publish a skill, but each consumer decides whether to activate it.

## 0. Skill lifecycle

The lifecycle is ordered:

1. **Register:** place the portable source at `skills/<category>/<name>/`, update both catalogs, validate, and record
   the release change.
2. **Bind:** a consumer pins a released revision and regenerates registered skills into its configured discovery
   directory.
3. **Adopt:** the consumer activates a bound skill only with the applicable user consent.
4. **Sync or contribute:** released skills can be compared with upstream or changed through a pull request.

Registration is a precondition for the later stages, but it never implies adoption.

## 1. Category layout

- Skills live under `skills/<category>/<name>/`.
- The immediate directory under `skills/` is the category source of truth.
- Categories are functional groupings such as `governance`, `orchestration`, `research`, `code`, or `visualization`.
- The category set is not a hardcoded enum. A publisher may create a new category after the author explicitly selects
  it; the publisher must not infer one silently.
- A category is repository organization, not portable skill metadata.

## 2. Standard frontmatter

Every `SKILL.md` uses the standard skill frontmatter floor:

```yaml
---
name: gerund-led-kebab-name
description: What the skill does and when it should trigger.
---
```

Standard optional fields may be used when needed. Do not add a top-level `category` field: generic Codex/Agent Skills
validators reject repository-specific extensions, and category is already encoded by the parent directory.

The frontmatter `name` must equal the skill directory. Names and descriptions must pass `naming-skills`; hard naming
or trigger-description failures block registration.

## 3. README maintenance

Every add, move, rename, or remove updates `README.md` and `README_zh.md` together:

- one Skill Catalog row;
- the category layout list;
- a Use-via-Prompt entry and keyword-trigger row when user-triggered;
- total count and category visualization when present.

Each catalog row has category, skill token, does, when-to-use, and boundary columns. Category comes from the path;
name comes from frontmatter. The three curated cells must be non-empty.

## 4. Catalog consistency

Set A is every `<category>/<name>` token in each README catalog. Set B is every `skills/*/*/SKILL.md`, with category
from the parent directory and name from frontmatter. Assert A equals B in both languages. This catches missing rows,
orphan rows, wrong paths, and stale names.

The checker also rejects a top-level frontmatter `category`, validates `name == directory`, and verifies references.

## 5. Regeneration

The home source is canonical. Consumer copies in discovery directories are generated build artifacts and remain
gitignored. After a skill-body change, regenerate and compare source and consumer copy byte-for-byte. Never hand-edit
the generated copy as an alternate source.

## 6. Identity decoupling

Generic skill bodies contain no organization, account, project path, wiki ID, chat ID, credential, or private data.
Resolve identity, remote, permissions, thresholds, and project policy at runtime. Consumer-specific values stay in the
consumer project.

## 7. Versioning and release

- Keep `VERSION`, the current changelog release block, and the eventual release tag consistent.
- Every change lands through branch -> pull request -> merge; do not push directly to the default branch.
- Releases follow the repository's weekly train. Only merged contributions ship or count as accepted contributions.
- The pull request reports selfcheck, author-selftest, eval, and any behavioral-test evidence.

## 8. Publishing authority

The author or scout proposes a skill, the user consents, and `publishing-skills` places and registers it. This actor
rule does not create a second agent-folder hierarchy. Adoption remains a separate consumer decision.

## 9. Standalone repository surface

Because this skill home is also a standalone public repository, its README may contain a centered title, static
repo-relative badges, Why/Features sections, and a standalone-versus-governed explanation. Do not use badges or assets
that hardcode an organization/repository identity. Keep the English and Chinese entry documents structurally aligned.
