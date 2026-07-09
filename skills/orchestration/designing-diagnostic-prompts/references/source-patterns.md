# Source Patterns for Diagnostic Prompts

Use these as pattern provenance, not as text to copy.

## Human 3.0 Pattern

Public references:
- Dan Koe, "A Complete Knowledge Base Of HUMAN 3.0": https://thedankoe.com/letters/a-complete-knowledge-base-of-human-3-0/
- Dan Koe, "Prompt: HUMAN 3.0 Self-Discovery & Metatype Test": https://letters.thedankoe.com/p/prompt-human-30-self-discovery-and

Reusable pattern:
- Map the user's situation across a small set of dimensions.
- Diagnose current level/state per dimension.
- Find the core constraint rather than listing generic advice.
- Watch for cross-dimension cascades: one constraint may explain failures elsewhere.
- Produce a development plan aimed at the next state, not an abstract ideal.

Do not copy:
- The original long prompt body.
- Personal-development claims as facts for unrelated domains.
- Health, clinical, legal, or financial diagnosis.

## Mr. Ranedeer Pattern

Public references:
- Repository: https://github.com/JushBJJ/Mr.-Ranedeer-AI-Tutor
- Usage guide: https://github.com/JushBJJ/Mr.-Ranedeer-AI-Tutor/blob/main/Guides/How%20to%20use%20Mr.%20Ranedeer.md

Reusable pattern:
- Expose commands or explicit phases (`plan`, `start`, `continue`, `test`, `config`) so users can steer the session.
- Let the user configure depth, style, language, pacing, and assessment.
- Keep a curriculum or plan state that future turns can continue.
- Teach in loops: explain, example, question, feedback, adapt.
- Include recovery behavior for unusual output or user confusion.

Do not copy:
- Hidden chain-of-thought scaffolding.
- Prompt-injection-prone instructions that ask the model to hide internal generated text.
- A fixed persona that is irrelevant to the target domain.

## Combined Template

```text
Role:
  You are a diagnostic [coach/tutor/advisor] for [domain].

Goal:
  Help the user identify their current state, binding constraint, and next measurable step.

Configuration:
  depth: [intro/intermediate/advanced]
  tone: [direct/supportive/socratic]
  language: [runtime value]
  assessment: [none/light/strict]

Flow:
  1. Intake: ask one question at a time until enough context exists.
  2. Map: score or describe each domain dimension with evidence.
  3. Constraint: name the current bottleneck and confidence level.
  4. Plan: give the minimum effective next step and metric.
  5. Loop: reassess after user response; adapt configuration if needed.

Boundaries:
  Do not diagnose protected domains. Escalate to a qualified professional where appropriate.
```

