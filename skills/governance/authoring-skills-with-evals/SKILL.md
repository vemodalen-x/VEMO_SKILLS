---
name: authoring-skills-with-evals
description: >
  Author, evaluate, and improve skills with an eval-driven loop instead of by intuition. Use when creating a new skill, revising an existing one, judging whether a skill's description actually triggers, or tuning that description for better trigger accuracy. Runs a with-skill-vs-baseline behavioral eval with variance, a trigger-rate eval, and a train/test-split description optimizer via the repo's skill-creator harness, modeled on Anthropic's official skill-creator. Triggers include create a skill, write a SKILL.md, run a skill eval, benchmark a skill, description not triggering, improve a skill description, skill quality, eval-driven authoring.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Authoring Skills with Evals

Create and improve a skill the way you would tune a model: draft it, **measure it on realistic
prompts**, and iterate on evidence — not on a hunch that "the description reads fine". This skill
is the VEMO_SKILLS adaptation of **Anthropic's official `skill-creator` meta-skill**; it keeps that
loop but binds it to this home's single-source model and its release scorer.

> **Two layers, do not confuse them.**
> - `tools/vemo_skills_check.py` (the release scorer, threshold 9.5) lints a skill's **shape** —
>   frontmatter, naming, catalog parity, decoupling. It cannot tell you whether the skill *works*.
> - `tools/skill_creator.py` (this skill's harness) measures **behavior** — does the description
>   trigger, and does the body produce a better result than no skill at all.
> A skill is only "done" when it passes **both**.

## When to use
- Creating a new skill from scratch, or splitting/merging existing ones.
- A skill under- or over-triggers (fires when it shouldn't, or stays silent when it should).
- You want to optimize a `description:` for trigger accuracy without overfitting to a few queries.
- Auditing a skill's authoring evidence without treating generated markers as source.

## The loop (eval-driven authoring)
See `references/eval-loop.md` for the full rationale and prompt-design rules. In short:

1. **Draft** the `SKILL.md`. Put *all* the "when to use it" signal in `description:` — it is the only
   text the model sees when deciding to invoke the skill. Write it in the imperative and make it a
   little "pushy": the model tends to *under*-trigger skills.
2. **Write an eval set** — 6-12 realistic prompts as JSON, each `{"query": "...", "should_trigger": true|false}`.
   Include hard negatives (near-misses that must NOT trigger) and messy, real-sounding positives.
3. **Lint the shape**: `python3 tools/skill_creator.py validate skills/<cat>/<name>`. It is read-only by default and
   checks frontmatter, naming, and `agents/openai.yaml`. Use `--marker` only when an ephemeral lint receipt is useful;
   the marker is gitignored and never part of the skill package.
4. **Measure triggering**: `python3 tools/skill_creator.py trigger-eval skills/<cat>/<name> --eval-set evals.json`.
   Reports a per-query trigger rate over N runs (triggering is nondeterministic — one sample is noise).
5. **Improve the description**: `python3 tools/skill_creator.py describe-improve skills/<cat>/<name> --eval-set evals.json --model <model>`.
   Splits the eval set train/test, optimizes on train, and picks the winner by **held-out test score**
   so it cannot memorize the eval set.
6. **Re-run** until the trigger eval is clean and a with-skill run beats the no-skill baseline.

## Commands
| command | what it does | needs `claude` CLI |
|---|---|---|
| `validate <dir> [--marker]` | lint frontmatter + naming + UI metadata; optional marker is gitignored | no |
| `trigger-eval <dir> --eval-set f.json` | measure description trigger rate (tri-state per run) | yes |
| `describe-improve <dir> --eval-set f.json --model M` | train/test-split description optimization | yes |
| `selftest` (`vemo-skills author-selftest`) | hermetic check of the deterministic core | no |

The two model-in-the-loop commands **degrade gracefully**: if the `claude` CLI is not on `PATH` they
report `status: skipped` and exit 0. An infrastructure gap is reported as *skipped*, never scored as
"the description failed to trigger" — a run that could not execute is an `error`, excluded from the rate.

## Optional ephemeral provenance marker
When explicitly requested, `.skill-validated.json` carries a tier:
- `lint` — frontmatter + naming only. **Does not** claim a behavioral/trigger eval ran.
- `trigger` — lint plus a trigger eval that met the pass threshold.

It also records `validator_sha` and `git_commit`. Never hand-edit or commit the marker; regenerate it with
`validate --marker`. Durable release evidence belongs in eval/task receipts, not inside every plugin package.

## Boundaries
- **Does not adopt.** Producing/validating a skill is not the same as putting it in a project's toolset
  (a user-consent decision). Registration/placement is `publishing-skills`; naming conformance is
  `naming-skills`; this skill owns the **eval loop** and complements both.
- **Render-nothing / send-nothing.** It writes only the skill under authoring and an explicitly requested,
  gitignored marker; it never
  publishes, announces, or edits the catalog.
- **Zero project identity** in any skill body (this home's red line) — the harness only reads shape and
  triggering, so keep evals free of project-specific values too.

## References
- `references/eval-loop.md` — the full loop, the two eval types (trigger vs output-quality), variance /
  baseline discipline, the train/test split, and description-writing rules.
- Anthropic Agent Skills — best practices: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- Anthropic engineering — equipping agents with Agent Skills (the official skill-creator's home).
