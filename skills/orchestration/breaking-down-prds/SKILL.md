---
name: breaking-down-prds
category: orchestration
description: Decompose a PRD / requirements document into a structured, governable breakdown — functional & non-functional requirements, acceptance criteria, work-breakdown by stage/agent, requirement→stage traceability, and a coverage check. Use at project kickoff or a major new feature, when the orchestrator must turn a PRD into actionable, traceable work before research/build begins. Owned by Framework 0 (orchestration).
---

# PRD Breakdown

Turn a PRD into a structured breakdown that anchors all downstream work and is traceable to the project's
governance frameworks. The orchestrator (Framework 0) owns this activity; this skill standardizes it.
Borrows decomposition discipline from spec-kit (PRD-as-source → spec → tasks), BMAD-METHOD
(analyst/PM decomposition), and OpenSpec (current-state vs proposals separation).

## When to use
- Project kickoff or a major new feature: a PRD / requirements doc exists and must be decomposed before
  substantive research or build.
- Trigger phrases: "拆解 PRD", "PRD breakdown", "decompose requirements".

## Inputs
- The PRD / requirements document (path or content).
- The project's attached frameworks from `project_profile.yaml` (for traceability).

## Procedure
1. **Read the PRD as the source of truth** (spec-kit). Extract intent, scope, hard constraints.
2. **Functional Requirements (FR)** — enumerate what the system must do (features, user scenarios, triggers);
   give each a stable id `FR1, FR2, ...`; cite PRD sections.
3. **Non-Functional Requirements (NFR)** — metrics & constraints (accuracy/latency/power/robustness/privacy/
   platform/compatibility); id `NFR1, ...`; cite PRD sections.
4. **Acceptance criteria** — from the PRD's acceptance section; map each to the owning stage.
5. **Work breakdown → owning stage/agent** (BMAD analyst/PM pattern) — which stage owns which scope and which
   FR/NFR it serves.
6. **Requirement → stage traceability matrix** — each requirement → owning stage(s) → verification evidence;
   sync into the orchestration instance traceability table.
7. **Coverage check** (OpenSpec current-vs-proposed) — confirm the first/next task is in the PRD direction;
   explicitly log requirements **deferred** to later stages so nothing is lost.
8. **Open items** — facts to confirm with the user; mark `pending`, never assume.

## Output
- A PRD-breakdown deliverable containing: FR table, NFR table, acceptance→stage, work-breakdown→stage,
  coverage check, open items. Stable ids enable traceability.
- Filed as a **single authoritative file** under the project deliverables convention:
  `deliverables/<task-id>_prd_breakdown.md`. One file only — no parallel language copies.
- **Language** follows the **project language policy** (instance-owned): a PRD breakdown is a published outward
  deliverable, so its language is whatever the instance's language policy assigns to outward deliverables.
  The skill reads this from the instance; it hardcodes no language.

## Rules
- Requirements must be traceable to the project's governance frameworks (orchestration instance matrix).
- Ask-don't-assume for missing facts (chip/model/targets) → `pending`.
- This skill **produces the breakdown only**; it does not perform the research/build.
- Adoption/build of this skill is governed by Framework 0 `skill_spec`; recorded in the orchestration catalog.
- **Decoupling (skill_spec §9)**: this body is generic — project values (deliverable naming, language policy,
  framework set) are read from the business-repo instance at runtime; nothing project-specific is hardcoded here.
