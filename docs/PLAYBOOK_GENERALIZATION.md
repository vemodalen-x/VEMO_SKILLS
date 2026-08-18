# Generalizing Playbook Procedures into VEMO_SKILLS

VEMO_SKILLS is the right home for playbook procedures that are reusable across projects. It is not the right home for a
consumer project's task ledger, acceptance gates, local paths, model pricing, group ids, or test commands.

## Good Skill Candidates

Convert a playbook section into a VEMO_SKILLS skill when it has all of these properties:

- It describes a repeatable workflow, not a one-off task.
- The trigger can be described in natural language.
- The procedure has stable steps and clear boundaries.
- Project-specific values can be supplied at runtime by the consuming repo.
- The skill can stay advisory or artifact-producing; final acceptance remains in the consumer's VEMO gates.

Examples:

- break a PRD into scoped tasks
- review a decision record
- publish a deliverable and notify reviewers
- render an evaluation report
- validate an on-device model with caller-supplied thresholds
- check naming and metadata for another skill

## Keep Out of VEMO_SKILLS

Do not bake these into a shared skill body:

- repository-specific completion definitions
- exact build, smoke, deploy, or device commands
- project paths such as `src/core/**` unless they are examples clearly marked as placeholders
- credentials, group identifiers, user ids, private URLs, or local machine assumptions
- diagnostic facts from another project, such as scratch sizes or historical failure counts

Put those values in the consumer project's VEMO task file, config, project profile, or runtime prompt.

## Authoring Shape

Each generalized procedure should become:

```text
skills/<category>/<name>/
  SKILL.md
  references/        # optional scripts, checklists, examples, or style guides
```

`SKILL.md` should state:

- when to use the skill, in the frontmatter `description`
- what the skill does
- what inputs it expects from the consuming project
- what it will not decide or modify
- what evidence or artifact it emits

If the workflow needs deterministic work, put scripts under `references/` and have the skill call or adapt them. Avoid
long prompt prose that a small script could check.

## Publish and Bind

1. Draft or update the source skill under `skills/<category>/<name>/`.
2. For a new skill, activate its path in `skills/index.json` and generate `agents/openai.yaml`.
3. Run the naming/frontmatter/index checks through the repo tooling.
4. Keep `README.md` and `README_zh.md` catalog rows in parity.
5. Run `bin/vemo-skills selfcheck` and, for release work, `bin/vemo-skills eval`.
6. Bind into a consumer project with `bin/vemo-skills bind --dest <consumer>/.claude/skills`.

The generated `.claude/skills/<name>/` copies are build artifacts. Edit the source skill home, then bind again.

## Boundary with VEMO

VEMO_SKILLS can teach an agent how to perform a workflow. VEMO decides whether the resulting project work is allowed,
in scope, sufficiently verified, and accepted.

If a playbook rule needs mechanical enforcement, implement it in VEMO as a validator, hook, CI gate, preset, or spec.
If it is a reusable procedure that helps many repos but does not own the gate, implement it as a VEMO_SKILLS skill.
