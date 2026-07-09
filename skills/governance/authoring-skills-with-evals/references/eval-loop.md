# The eval-driven authoring loop

Reference for `authoring-skills-with-evals`. This is the *why* behind the harness; the SKILL.md is the
*how*. It adapts the methodology of Anthropic's official `skill-creator` to this repository.

## Why measure at all
A skill is a prompt with progressive disclosure: the model sees `name` + `description` first and only
reads the body if it decides to invoke the skill. Two failure modes follow, and neither is visible by
reading the file:
1. **Trigger failure** — the description does not fire for the intents it should (or fires for ones it
   shouldn't). This is a *retrieval* problem, independent of body quality.
2. **Output failure** — the skill fires but its guidance does not make the result better than the model
   would have done unaided.

Static linting (naming, frontmatter) catches neither. You have to *run* the skill.

## Two orthogonal eval types
- **Trigger eval** (`trigger-eval`): register the skill as a throwaway command, send each query through a
  fresh model session, and record whether the skill was invoked. Because triggering is nondeterministic,
  run each query several times and compare the *rate* against a threshold — never a single sample.
- **Output-quality eval** (author-run, human-reviewed): run the task **with the skill** and **without it
  (baseline)**, then compare. The baseline is the whole point — it isolates the skill's *marginal* value
  instead of measuring absolute quality. Report mean ± standard deviation over several runs; a single run
  hides variance.

## Anti-overfitting: train/test split
`describe-improve` splits the eval set (stratified by `should_trigger`, deterministic seed), optimizes the
description using only the **train** results, and blinds the improver to the **test** scores. The winning
description is selected by held-out **test** score. This is ordinary ML hygiene applied to prompt tuning:
without it, the optimizer memorizes the eval set and the description stops generalizing.

## Writing a good eval set
- 6-12 queries, a mix of positives and hard negatives. Save as JSON:
  `[{"query": "...", "should_trigger": true}, {"query": "...", "should_trigger": false}]`.
- Positives should be *realistic* — messy, with file paths, typos, and backstory — not textbook phrasings.
- Negatives should be *near misses* the skill could plausibly grab but shouldn't. An easy negative
  ("write a fibonacci function" for a PDF skill) tests nothing.
- A skill only triggers for tasks the model can't trivially do itself; trivial queries won't trigger no
  matter how good the description is.

## Writing the description
- Imperative voice, focused on the **user's intent**, not the implementation.
- Pack in the trigger words a user would actually say; the description competes with every other skill for
  attention, so make it distinctive.
- Generalize from failures to *categories* of intent — do not append an ever-growing list of exact
  queries (it overfits and burns the character budget). Stay well under the 1024-char limit.
- Explain the *why* in the body; avoid a wall of all-caps MUST/NEVER (a yellow flag per Anthropic's
  guidance) — a rule the model understands generalizes to cases you didn't spell out.

## Judging (when a human isn't in the loop)
- Use **deterministic checks** for exact things (did the skill trigger? did the file get written?).
- Use an **LLM-as-judge** only for output quality that depends on content, and let it **abstain** rather
  than emit a falsely precise score. Validate the judge against human labels before trusting it.
- Prefer a small panel with different lenses over one judge repeated, and treat a passing grade on a weak
  assertion as a red flag — a non-discriminating check (passes with and without the skill) proves nothing.

## Sources
- Anthropic — Skill authoring best practices: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- Anthropic — Equipping agents for the real world with Agent Skills (engineering blog; the official skill-creator).
- Anthropic — Building Effective Agents (evaluator-optimizer pattern).
