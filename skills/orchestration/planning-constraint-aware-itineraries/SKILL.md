---
name: planning-constraint-aware-itineraries
description: 'Build or review travel itineraries with deterministic time, timezone, opening-hours, transit, budget, fixed-booking, and local-replanning constraints while using an LLM only for preference interpretation and explanation. Use when creating a travel-planning agent, generating a detailed itinerary, ingesting travel inspiration, validating schedule feasibility, or safely replanning around locked items. Triggers include travel planner, itinerary agent, two-hour itinerary, route planning, timezone, opening hours, fixed booking, local replan, and trip export.'
---

# Planning Constraint-Aware Itineraries

Represent a trip as timezone-aware scheduled data. Compose with `architecting-auditable-agent-workflows` for typed
tools, decision rights, state transitions, provenance, idempotency, and approval. This skill owns only travel-specific
normalization, constraints, replanning invariants, and feasibility tests.

## Intake

Collect destination scope, local dates or start/end instants, traveler count, pace, interests, must/avoid items,
accessibility and age constraints, budget/currencies, lodging anchors, transport mode, fixed bookings, meal/rest needs,
and acceptable uncertainty. Ask for missing hard constraints; never infer flights or reservations.

Treat prose, screenshots, rankings, and links as candidate ideas with source spans. They remain unverified until current
hours, routes, prices, weather, and booking requirements are checked.

## Domain Workflow

### 1. Normalize geography, time, and money

- Resolve places to stable geographic IDs and IANA timezones.
- Compute offsets for the actual date; never store a city as a fixed UTC offset.
- Compare timezone-aware instants across midnight, DST, and borders.
- Preserve original-currency decimal amounts and append dated exchange-rate snapshots.
- Record assumptions when the request contains only dates, relative days, or rough budgets.

### 2. Freeze travel facts

Record provider/source, retrieval and expiry times, confidence, verification state, and payload hash for places, hours,
routes, weather, events, and costs. Re-query time-sensitive facts at planning time where possible. Otherwise label them
historical, seasonal, stale, or unverified; never turn an estimate into a live fact.

### 3. Separate hard constraints and preferences

Hard constraints include trip bounds, fixed reservations, opening and last-entry windows, duration, transit and queue
time, transfer/airport buffers, accessibility, must/avoid rules, hard budget, and locked items. Never relax one merely
to produce a full schedule.

Soft objectives may reward interest fit, route clustering, diversity, meal/weather fit, novelty, and source confidence,
or penalize transit, cost, crowds, uncertainty, and fatigue. Preserve score components for explanation.

### 4. Schedule at executable granularity

Use item-level timestamps internally even if the display uses coarse blocks. Transit, queues, meals, rest, check-in,
and buffers are real items that consume time. Use a constraint solver when search warrants it; otherwise use a
deterministic heuristic with the same failure contract. LLM prose never owns authoritative timestamps.

### 5. Validate feasibility

An independent validator checks overlap, trip bounds, opening/last-entry windows, transit, DST/timezones, fixed/locked
movement, budget, required buffers, excessive daily load, and display slots extending beyond trip end. Errors block
activation and export; warnings remain visible.

### 6. Replan locally

Freeze the accepted base version. On a local change, compute the editable day/region and hash every fixed, locked, and
outside-scope item. Only flexible items wholly inside scope may change. Cross-midnight items are frozen unless the
request explicitly expands scope. Validate the candidate and append a child version; never silently rebase or move a
reservation.

If infeasible, return the conflicting constraints, quantified shortfall, and repair options with required authority.
Unavailable or stale facts produce `unverifiable`, not `feasible` or `infeasible`.

### 7. Export and round-trip

Export structured JSON plus the requested calendar, spreadsheet, or printable projection. Sanitize formulas and links,
then re-read the artifact and verify item counts, timestamps, costs, source IDs, and fixed/locked flags.

## Minimum Tests

Cover DST transitions, cross-timezone and cross-midnight travel, closed/last-entry windows, insufficient transit,
fixed and locked mutations, one-day scope preservation, hard-budget failure, trip-end residue, duplicate requests,
provider staleness, and export/import round-trip. Use deterministic provider fixtures with no live credentials.

## Output Contract

Return normalized inputs and assumptions, fact/candidate ledger, item-level plan, display projection, validation
findings, version relationship, infeasibility details, and a refresh checklist for dynamic facts.

## Boundaries

- Do not invent current hours, fares, visa rules, weather, or travel times.
- Do not let an LLM paragraph override hard constraints or validator findings.
- Do not move locked/fixed or outside-scope items during local replanning.
- Travelers remain responsible for official entry, safety, health, and booking checks.
