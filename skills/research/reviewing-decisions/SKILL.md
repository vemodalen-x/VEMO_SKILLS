---
name: reviewing-decisions
description: 'Reliability ruleset for technical design decisions — a lightweight design-review discipline. Each key decision must carry 6 fields (options/evidence/trade-offs/assumptions/failure-modes/validation); a cross-model red-team pass critiques the doc before publish. Use when the research-solution agent finalizes the solution_document. Owned by Framework 1 (research). Generic; reviewer models/decisions are instance values.'
---

# Decision Review (reliability discipline)

Makes design decisions **reliable, not just stated**. Two parts: a per-decision **6-field floor** (checkable),
and a **cross-model red-team** critique before publish. Self-built, borrowing the *ideas* of structured-MADR
(machine-checkable decision fields) and adversarial-review (cross-model critique) — see the research catalog borrow-note.
Pairs with `structuring-solution-docs` (its S8/MADR blocks ARE these decisions). Generic (skill_spec §9).

## When to use
- The research-solution agent finalizes the `solution_document` (Wildtarsier §1.9); apply before 准出 (Gate 2).

## A. Per-decision 6-field floor (准出 completeness — missing any = not done)
Every key design decision MUST carry all six. The 准出 check (Gate 2, compliance) verifies presence — this is a
**completeness criterion of the `solution_document` output**, NOT a new gate (the loop stays the existing two gates):
1. **Options compared** — ≥2 candidates with pros + cons each (no single-option "decision").
2. **Evidence with provenance** — each claim sourced + tagged 实测 / 文献 / 推测 (defer to technical-report-style R4).
3. **Trade-offs** — what the chosen option costs, stated plainly (no one-sided upside).
4. **Assumptions** — what must hold for the decision to be valid (so they can be checked later).
5. **Failure modes** — how it can go wrong + the mitigation or detection.
6. **Validation** — how the decision will be verified (experiment / metric / PoC) — ties to the feasibility region.

## B. Cross-model red-team (pre-publish adversarial pass)
- Before the solution_document is published, a **different agent / model** reviews it adversarially: actively look
  for weak evidence, unstated assumptions, missing failure modes, one-sided trade-offs, and over-claims.
- Findings are recorded; material ones are resolved (or explicitly accepted with reason) before publish.
- This is a **step inside the existing 准出**, not a third blocking gate — it runs out-of-band like the governance
  behavior-audit, and its output is advisory input to the compliance Gate-2 decision, not a separate gate.

## Rules
- A decision missing any of the 6 fields (§A) → the `solution_document` is **incomplete** → 准出 (Gate 2) fails.
- The red-team pass (§B) must have run before publish; its findings + resolutions are recorded in the task ledger.
- **Decoupling (skill_spec §9)**: generic. **Which model(s) red-team** and **which decisions are "key"** are
  instance/project values — e.g. `project_profile.yaml` may name the red-team reviewer model; not hardcoded here.
