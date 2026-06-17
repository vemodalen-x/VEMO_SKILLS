---
name: visualizing-governance
category: orchestration
description: Render the governance system's operation as diagrams — a mermaid flowchart of how frameworks/gates/agents run, a stateDiagram of the task seven-gate lifecycle, and an interactive markmap HTML overview for onboarding. Use when a README needs its governance diagram, when onboarding material is produced, or at release time to regenerate embedded SVGs. Owned by Framework 0 (orchestration).
---

# Governance Visualize

Turn the governance system's structural definitions (frameworks, roles, gates, task states) into **figures**:
a flowchart of how the system operates, a state diagram of the task lifecycle, and an interactive web overview.
The orchestrator owns this; this skill standardizes the rendering so every repo's governance diagram is built the
same way and stays a regenerable artifact (never hand-drawn, never stale by hand).

## When to use
- A repo README needs its **Governance diagram** section (readme-style R29) populated or refreshed.
- **Onboarding** material is produced (Wildwombat R4) — needs the flow figure + an interactive overview.
- **Release time**: regenerate the embedded SVG so the diagram tracks the current spec (ties to the
  `Framework_Release.procedure.md` README-refresh step + `audit_spec` §13 freshness check).
- Trigger phrases: "治理流程图", "governance diagram", "onboarding overview", "regen the flowchart".

## Inputs
- **source definitions** (read, never invented): the framework set + I/O contracts (`project_profile.yaml`
  `governance_frameworks`), the agent roster (`registry_spec` §2 / instance), the gate positions (`gate_spec`),
  and the task seven-gate state machine (`task_spec`). All structure comes from these — the skill renders, it does
  not author governance facts.
- **target** — which artifact to emit (flowchart / stateDiagram / markmap overview) and where it embeds (a README
  section, an onboarding doc, a Feishu node).
- **output format** — `mermaid` source (default, zero-migration), `svg` (release-embedded, via `mmdc`),
  Feishu `whiteboard` (for wiki publishing), or interactive `html` (via `markmap-cli`).

## Procedure
1. **Read the source definitions** (above). Do not hardcode framework/role/gate names — pull them from
   `project_profile.yaml` + the specs. A generic repo with no instance renders the generic skeleton only.
2. **Build the flowchart** (`mermaid flowchart`): frameworks as the base layer (Framework 0 always-on + domain
   frameworks by task type), the route → resolve → merge path (`registry_spec` §3/§4), the two gates, and where
   each roster agent acts. Keep it to one screen; deeper detail goes to the stateDiagram or appendix.
3. **Build the lifecycle** (`mermaid stateDiagram-v2`): the seven gates PlanCreated → ReviewApproved →
   ImplementationDone → AcceptancePassed → ProcedureCompleted → PostReviewUpdated → Archived, with Gate 1 (user) and
   Gate 2 (compliance) annotated on their transitions.
4. **Emit per target format**:
   - `mermaid` — write the source block into the target doc (README section / onboarding md).
   - `svg` — `mmdc -i <src.mmd> -o <out.svg>` and embed; run at release so the figure tracks the spec.
   - `whiteboard` — hand the mermaid source to `publishing-deliverables` (Feishu native whiteboard) for wiki nodes.
   - `html` — `markmap-cli <src.md> -o <overview.html>` to produce the **interactive collapsible overview** used in
     onboarding (a mindmap of the framework/role/gate hierarchy; user-requested for training).
5. **Record**: note the generated artifact(s) + their embed locations in the owning task's flow-ledger entry.

## Rules
- **Render, don't author**: every node/edge traces to a source definition (§Inputs). The skill never invents a
  framework, role, gate, or state — if the source is missing, surface it (per `registry_spec` §5 "missing → ask"),
  don't guess.
- **Regenerable, not hand-drawn**: diagrams are build artifacts. A README's governance figure is regenerated from
  source at release, not edited by hand (keeps it from drifting — `audit_spec` §13 freshness).
- **mermaid first**: default to mermaid source (zero migration, renders in GitHub/Feishu/markmap). SVG/HTML are
  derived outputs. (Borrow: mermaid-js; markmap markmap-js-12.9k★ MIT for the interactive overview — tooling, not text.)
- **Tooling is use-time**: `mmdc` (mermaid-cli) and `markmap-cli` are installed when the skill first runs a `svg`/`html`
  emit (a machine step), not pinned by this spec.
- **Decoupling (skill_spec §9)**: this body is generic; all framework/role/gate values come from the business-repo
  instance + specs at runtime. Zero hardcode.

## References
- `registry_spec` (frameworks/roles/routing), `gate_spec` (gates), `task_spec` (seven-gate states) — the source of
  truth for what the diagram depicts.
- `readme-style.md` R29 (the README "Governance diagram" section this skill populates).
- mermaid (flowchart/stateDiagram), `@mermaid-js/mermaid-cli` (`mmdc`, SVG), `markmap-cli` (interactive HTML).
