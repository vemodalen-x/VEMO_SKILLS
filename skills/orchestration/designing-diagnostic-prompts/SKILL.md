---
name: designing-diagnostic-prompts
description: 'Design structured diagnostic or tutoring prompts and agent workflows that interview the user, locate constraints, configure style/depth, produce a plan, and loop through assessment and feedback. Use when asked to create or improve a Human 3.0-style self-discovery prompt, a Mr. Ranedeer-style tutor prompt, a coaching/custom GPT prompt, an onboarding interview, a diagnostic agent, a personalized learning flow, or any multi-turn prompt that must ask questions before advising.'
---

# Diagnostic Prompt Design

Design multi-turn prompts that diagnose before advising. This skill turns a loose "be my coach/tutor/advisor" request into a structured workflow with intake, configuration, assessment, plan, and feedback loops.

## Inputs

- Domain and audience: life coaching, learning, product onboarding, team diagnosis, technical training, etc.
- Target outcome: insight, curriculum, decision support, behavior plan, or skill acquisition.
- Risk boundary: what the agent must not diagnose, decide, promise, or store.
- Runtime surface: chat prompt, custom GPT, skill, app flow, or project-local VEMO task.

## Procedure

1. **Frame the diagnostic map.** Choose 3-5 dimensions that explain the domain. Human-development examples use quadrants; learning examples use topic, depth, style, pace, and assessment.
2. **Define levels and transition states.** Use levels only when they change behavior. Prefer "current state -> constraint -> next action" over vague maturity labels.
3. **Ask before advising.** Start with a short intake. Ask one question at a time unless the user explicitly wants a form.
4. **Separate configuration from content.** Let the user set depth, tone, language, pacing, examples, assessment frequency, and constraints. Provide commands or explicit slots when useful.
5. **Locate the binding constraint.** Identify the dimension or misconception that blocks progress now. State evidence and uncertainty.
6. **Produce a plan.** Give a minimum effective plan: next step, why it matters, what to measure, and what would trigger a revision.
7. **Loop.** Add checkpoints: quiz, reflection, user feedback, progress update, or reconfiguration. The agent should adapt rather than repeat the same advice.
8. **Guard the boundary.** For health, finance, legal, mental health, or high-stakes life decisions, keep the output as coaching/support, not professional diagnosis or instruction.

## Output Shape

Produce one of these, depending on the request:

- **Prompt spec**: role, goal, inputs, commands, intake questions, assessment rubric, response format, stop rules.
- **Agent flow**: states, transitions, memory fields, commands, validation checks.
- **Skill draft**: `SKILL.md`-ready workflow with generic inputs and project-specific values left to runtime.

## Quality Bar

- The prompt does not give advice before it has enough context.
- The dimensions are domain-specific, not decorative.
- The user can change configuration without editing the whole prompt.
- The plan contains measurable next actions and a revision trigger.
- The workflow says what it will refuse or escalate.
- Any source inspiration is cited as pattern provenance, not copied as prompt text.

## References

- `references/source-patterns.md` — compact pattern extraction from Human 3.0 and Mr. Ranedeer.

