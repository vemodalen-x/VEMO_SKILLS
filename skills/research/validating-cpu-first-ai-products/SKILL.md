---
name: validating-cpu-first-ai-products
description: 'Validate whether an AI product can deliver useful quality, latency, memory, privacy, and unit economics on CPU-first or client-first infrastructure before scaling implementation or promotion. Use when evaluating a local-first AI feature, browser/WASM/WebGPU pipeline, lightweight vision model, CPU inference product, model distillation candidate, or client-vs-server architecture. Triggers include CPU-first, local-first AI, browser inference, lightweight model, product validation, benchmark plan, Go Narrow Stop, unit economics, and technical feasibility.'
---

# Validating CPU-First AI Products

Decide whether the user problem and execution envelope can coexist. This skill owns product evidence and the
Go/Narrow/Stop decision. It composes with conversion, quantization, model-quality, and on-device inference skills for
implementation mechanics and platform sign-off.

## Required Decision Inputs

Require the target user, repeated job, candidate feature, supported device floor, privacy/offline promise, distribution
model, commercial goal, and decision owner. If these are missing, return `needs-input` with explicit assumptions to
confirm. Do not silently choose a product use case, operating-system floor, RAM target, sample size, user count, price,
or pass threshold merely to make the plan look complete.

## Workflow

### 1. Freeze the decision before testing

Write the target user, repeated job, current workaround, promised outcome, first useful output, and exclusions. Define
Go/Narrow/Stop thresholds before seeing results. Every threshold must come from an owner requirement, observed baseline,
published constraint, or documented provisional rationale. Use separate gates for demand, task quality, usability, latency,
memory, cost, license, privacy, payment, and repeat use.

Prefer a manual service or narrow prototype before broad automation. Record completed tasks, time saved, direct
acceptance, revision effort, repeat use, and payment behavior. Compliments, waitlists, and engagement are not demand
proof.

### 2. Gate dependencies and test rights

For every model, data source, font, test asset, and reference implementation, record source, version, license,
commercial/distribution terms, attribution, and documented limits. Exclude unclear dependencies from product
conclusions.

Build a licensed, failure-oriented test set across low-end and large inputs, edge cases, malformed files,
metadata/orientation, relevant scene or user diversity, and cases where the feature should abstain.

### 3. Compare product-level alternatives

Evaluate a no-AI/manual baseline, deterministic heuristic, lightweight local candidate, optimized local candidate, and
heavier quality reference. Treat browser/client, local CPU service, and optional remote fallback as distinct placements
with different privacy, delivery, support, and cost profiles.

Do not prescribe conversion or quantization inside this skill. Invoke the dedicated code skill and import its measured
evidence into the frozen gate table.

### 4. Measure the complete user path

Separate decode/normalization, load, preprocessing, inference, postprocessing, encoding, and transfer. Report cold and
warm median/tail latency, peak memory, CPU threads/time, output bytes, failures, retries, crashes/OOM, and controlled
concurrency. Name hardware, runtime, candidate version, input class, and repeat count.

Low-end target devices are gates, not optional observations. Client compute still incurs download, fallback, support,
analytics, and compatibility costs.

### 5. Measure decision and user quality

Pair domain metrics with task completion, first useful result, accept/edit/abandon rate, correction effort, abstention,
and confidence after a severe failure. Review all severe failures rather than relying on averages. For subjective
outputs, blind method identity, randomize order, permit "neither usable", and stratify by failure class.

### 6. Preserve reproducible evidence

Version each recipe with candidate/algorithm version, parameters, seed, input references, output format, and
privacy/metadata policy. Keep licensed golden inputs, expected properties, environment data, and failure fixes. Use
exact or bounded checks for deterministic paths and perceptual metrics plus approved human review where appropriate.

### 7. Calculate economics and decide

Include CPU and memory time, storage, request/CDN, egress, retries, fallback, payment fees, abuse, support, and human
review per successful output. Model realistic input sizes, free/paid mix, local/remote placement, and failure rates.

Return one decision:

- **Go:** the scoped task and execution envelope pass every frozen gate.
- **Narrow:** restrict user, scene, device, feature, format, or placement.
- **Stop/Pivot:** demand, quality, economics, privacy, or licensing cannot coexist in the target envelope.

Missing inputs produce `needs-input`; missing real-user or target-device evidence produces `not-ready`. Documentation
volume cannot raise either decision.

## Output Contract

Return the frozen gate table, dependency/license ledger, test-set matrix, alternative/placement matrix, raw benchmark
evidence, severe-failure gallery, user-study evidence, recipe/golden-case plan, unit economics, decision, and open gaps.

## Boundaries

- Do not market simulated, synthetic, or developer-device evidence as target-user proof.
- Do not invent product scope, sample sizes, user counts, prices, or acceptance thresholds.
- Do not redistribute weights or assets with unclear terms.
- Do not optimize a model before proving the user task and baseline.
- This skill produces decision evidence; it does not authorize launch, spending, or public claims.
