---
name: structuring-solution-docs
category: research
description: Structure rules for a technical solution / design document (the research-solution framework's solution_document deliverable). Style-as-rules for document STRUCTURE — arc42 skeleton + MADR per-decision blocks — turned into checkable rules. Use when the research-solution agent authors the solution/design doc after the survey + recommendation. Owned by Framework 1 (research). Generic; project values live in the instance.
---

# Solution-Doc Structure (arc42 + MADR, as checkable rules)

Governs the **structure** of a technical solution / design document — the `solution_document` in the
research-solution framework's `requires_outputs` (Wildtarsier §1.9). Complements `technical-report-style`
(which governs report prose) and `polishing-chinese-prose` (Chinese prose); this one governs the design-doc skeleton and
the per-decision block shape. Generic content (skill_spec §9): project specifics live in the instance.

## When to use
- The research-solution agent, after the survey + recommendation, authors the solution/design doc for the chosen route.
- Trigger phrases: "写方案", "solution doc", "design doc", "技术方案文档".

## Borrowed sources (provenance)
- **arc42** (https://github.com/arc42/arc42-template, **CC-BY-SA**) — the section skeleton (S1–S12 below).
- **MADR** (https://github.com/adr/madr, **MIT**) — the per-architecture-decision block shape (D1–D6 below).
- Borrowed as *structure ideas*, transcribed into checkable rules; see the research skill_catalog borrow-note.

## A. Document skeleton (arc42-derived) — required sections
The solution doc MUST cover these (omit a section only with an explicit "N/A — reason"):
- S1. **Introduction & Goals** — what the solution achieves; the top quality goals (from the PRD/NFRs).
- S2. **Constraints** — technical/platform/regulatory constraints (the project's hardware/budget/legal limits).
- S3. **Context & Scope** — system boundary, external interfaces, what's in/out of scope.
- S4. **Solution Strategy** — the chosen route in one view; why it meets the goals (links to the survey recommendation).
- S5. **Building Blocks** — decomposition into components, each with a responsibility.
- S6. **Runtime / Flow** — key scenarios as flows (a diagram per `technical-report-style` R7 — Feishu whiteboard mermaid).
- S7. **Deployment view** — how it maps onto the target platform (runtime/hardware + integration point).
- S8. **Architecture Decisions** — the key decisions, each as a **MADR block (§B)**.
- S9. **Quality Requirements** — measurable quality scenarios (ties to the project's NFRs/targets).
- S10. **Risks & Technical Debt** — known risks + mitigations + open items.
- S11. **Interfaces / API** — the integration contract / event API for downstream build (project-specific shape).
- S12. **References** — sources, cited per `technical-report-style` R4 (实测/文献/推测 tags).

## B. Per-architecture-decision block (MADR-derived) — required fields
Every key design decision in S8 MUST carry (this is also the reviewing-decisions floor, see `reviewing-decisions` skill):
- D1. **Context & problem** — what forces the decision.
- D2. **Decision drivers** — the criteria (quality goals, constraints) that matter.
- D3. **Considered options** — ≥2 candidates, each with **pros + cons** (no one-sided option).
- D4. **Decision** — the chosen option, stated plainly.
- D5. **Rationale** — why it wins against the drivers, evidence-backed (cited).
- D6. **Consequences** — trade-offs accepted, follow-ups, what it forecloses.

## Rules
- Structure is constrained, not free-form: every solution doc satisfies §A (skeleton) + §B (each decision block).
- Diagrams/flows via whiteboard, tables for comparisons (defer to `technical-report-style` R6–R8).
- Language follows the project language policy (instance; ADR-style tiering) — same as other deliverables.
- **Decoupling (skill_spec §9)**: this body is generic. Project specifics — the actual components, the chip,
  the NFR thresholds — are instance/deliverable content, not hardcoded here.

## References
- `references/arc42-mapping.md` — the arc42 → S1–S12 mapping + what each section answers (checklist form).
