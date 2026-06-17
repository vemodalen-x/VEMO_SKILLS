# arc42 → S1–S12 mapping (checklist)

> Borrowed from arc42 (https://github.com/arc42/arc42-template, CC-BY-SA), transcribed as a checklist.
> Each section: what it answers + a pass check. Generic (skill_spec §9) — project values are deliverable content.

| § | arc42 section | answers | pass check |
|---|---|---|---|
| S1 | Introduction & Goals | what + top quality goals | goals trace to PRD/NFRs; ≤5 measurable goals |
| S2 | Constraints | what limits the design | platform/regulatory/budget constraints listed |
| S3 | Context & Scope | boundary + external interfaces | a context diagram; in/out of scope explicit |
| S4 | Solution Strategy | the chosen approach in one view | ties to the survey recommendation; why goals met |
| S5 | Building Blocks | component decomposition | each block has a responsibility; no orphan block |
| S6 | Runtime / Flow | key scenarios | ≥1 flow diagram (whiteboard mermaid) |
| S7 | Deployment | mapping to target platform | chip/runtime mapping; integration point named |
| S8 | Architecture Decisions | the key decisions | each is a MADR block (D1–D6) — reviewing-decisions floor |
| S9 | Quality Requirements | measurable quality scenarios | ties to NFRs; thresholds stated, not vague |
| S10 | Risks & Technical Debt | risks + mitigations + open items | each risk has a mitigation or an owner |
| S11 | Interfaces / API | downstream integration contract | the integration/event API shape for build (project-specific) |
| S12 | References | sources | cited per technical-report-style R4 (实测/文献/推测) |

> A section may be "N/A — <reason>" but never silently omitted.
