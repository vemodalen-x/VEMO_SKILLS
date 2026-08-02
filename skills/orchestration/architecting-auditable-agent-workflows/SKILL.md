---
name: architecting-auditable-agent-workflows
description: 'Design reliable agent workflows that separate LLM judgment from deterministic authority, use typed tools and versioned state, preserve provenance, validate outputs independently, and require human approval for irreversible actions. Use when building an AI agent, copilot, multi-step automation, tool-calling workflow, durable job, human-in-the-loop system, or production agent architecture. Triggers include agent architecture, deterministic agent, typed tools, provenance, idempotency, workflow state, human approval, audit trail, and production agent.'
---

# Architecting Auditable Agent Workflows

Build an agent as a controlled workflow around a probabilistic model. The LLM interprets and ranks; deterministic code,
validators, state transitions, and humans retain authority where correctness or reversibility matters.

## Inputs

Resolve the user goal, domain risks, authoritative data sources, allowed tools, irreversible actions, latency/cost
budget, persistence needs, privacy boundary, and acceptance metrics. Do not choose a multi-agent topology before the
workflow and failure modes require one.

## Workflow

### 1. Create a decision-rights matrix

For every stage, assign one owner:

- **LLM:** intent normalization, semantic extraction, candidate ranking, explanation, and ambiguity detection;
- **deterministic code:** arithmetic, schemas, scheduling, permissions, policy checks, identifiers, state mutation,
  and acceptance calculations;
- **provider/source:** current external facts with timestamp, expiry, confidence, and raw evidence hash;
- **human:** high-impact approval, unresolved ambiguity, exceptions, publication, payment, deletion, and other
  irreversible decisions.

If a model is the only component that can tell whether its own result is valid, the design is incomplete.

### 2. Define typed contracts before prompts

Specify request, intermediate, tool, error, and result schemas. Include source IDs, assumptions, confidence, validation
status, and version fields. Reject malformed outputs; do not silently coerce an unconstrained paragraph into business
state.

Give each tool a narrow capability, explicit preconditions, bounded output, timeout, retry class, and permission level.
Treat tool and retrieved content as untrusted input even when it came from another internal component.

### 3. Model the workflow as explicit state transitions

Use named states such as intake, normalized, enriched, proposed, validated, awaiting-approval, applied, failed, and
cancelled. Persist transitions with input/output hashes and timestamps. Make retriable stages idempotent; assign stable
operation IDs and refuse stale writes.

For long jobs, persist checkpoints, bounded progress, cancellation, and resumable inputs. Distinguish a safe stop plus
resume from a true pause protocol.

### 4. Preserve provenance and version state

Store provider, canonical source URL/identifier, retrieved-at, valid-until, confidence, verification status, and payload
hash for dynamic facts. Append versions rather than overwriting accepted baselines. Compare structured fields to detect
meaningful drift; wording changes alone should not create business events.

Separate run state, user memory, source knowledge, and retrieval cache. Give each store an independent retention and
deletion policy; do not put every kind of context into one prompt or vector store.

### 5. Validate independently and fail visibly

Run deterministic validation after model and tool stages. Validation errors block persistence or action and return
stable error codes plus repair options. Explanatory text may describe a conflict but cannot override it.

For high-impact domains, separate the generator from the critic/validator and preserve negative evidence. Escalate to
human review when data is stale, confidence is below the frozen threshold, the action is irreversible, or model/tool
signals disagree beyond tolerance.

### 6. Design providers and degraded modes

Wrap network/model dependencies behind provider protocols. Enforce allowlists, timeouts, response-size limits, bounded
retries, concurrency caps, and TTL caches. Tests use deterministic fixtures, not live credentials. A degraded mode must
label missing/stale data; it must not synthesize a success response.

### 7. Evaluate the workflow, not only the final prose

Measure schema validity, task success, tool selection, argument correctness, policy violations, validator findings,
human overrides, retry/recovery, latency, cost, and state consistency. Keep adversarial cases for stale data,
conflicting providers, prompt injection, duplicate requests, cancellation, and resumed jobs.

Run an end-to-end fixture path that is credential-free and produces a machine-readable receipt. Mark fixture/model-
simulated evidence non-authoritative; never present it as real provider or user evidence.

## Architecture deliverables

Produce a component/responsibility table, decision-rights matrix, typed schemas, state machine, provider contract,
sequence diagram, permission/approval table, failure-code catalog, persistence model, evaluation plan, and one offline
reproduction path.

## Boundaries

- Do not make a model authoritative for time, money, permissions, compliance, or hard constraints.
- Do not add multiple agents when one coordinator plus typed tools is easier to test and operate.
- Do not swallow validator errors, fabricate provider fields, or mutate accepted versions in place.
- Do not log credentials or unnecessary sensitive payloads.
- This skill designs the workflow; project-specific acceptance thresholds and deployment gates stay in the consumer.
