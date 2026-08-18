---
name: gating-tflite-op-envelopes
description: >
  Statically gate a TFLite model against one or more target runtime envelopes — parse the flatbuffer (no runtime load) for custom ops + declared min_runtime_version, and emit PASS / REJECT with the offending operators and version per envelope. Use when screening a candidate .tflite or .task bundle for a runtime before adopting it (e.g. a host runtime and a device runtime), or recording a model card's runtime-compatibility verdict.
allowed-tools: Read, Bash, Glob
---

# Gating TFLite Op Envelopes

Decide, **statically**, whether a candidate TFLite model can run under a given **runtime envelope** — without
loading it in any TFLite runtime. An *envelope* is a target runtime version `V`: the model **PASSES** that envelope
iff it uses **no custom ops** AND its declared `min_runtime_version` is **≤ V**. Ask for one or more envelopes (e.g. a
host runtime and a device runtime); the model's verdict is the **AND** over all of them. This is a **selection /
adoption gate**: a candidate that fails an envelope cannot run on that runtime, so it is rejected for it.

## Model (read first)
- **Static parse, not interpreter probe — this is the load-bearing choice.** A custom op is *exactly* what can stop an
  interpreter from loading (unresolved-custom-op at allocate). So an interpreter-based detector can choke on the very
  case the gate exists to catch. Instead parse the **TFLite flatbuffer directly**: the `OperatorCode` table yields any
  custom ops; `Model.metadata["min_runtime_version"]` yields the declared min runtime. This works whether or not a
  kernel is registered, and needs **no TensorFlow runtime installed** (`pip install tflite flatbuffers`).
- **Two failure axes, one rule.** A model fails an envelope on (a) **any custom op** — the hard blocker, since a
  default builtin resolver has no kernel for it — or (b) **`min_runtime_version` > the envelope's target version**. A
  **missing or unparseable** `min_runtime_version` **cannot certify PASS** — the gate **fails closed** (never stamp a
  PASS it can't prove).
- **Envelopes are caller values, not baked in.** The version(s) you gate against (e.g. a host runtime's version, a
  device runtime's version) are **inputs** — the same code path runs once per envelope. No version is hardcoded in the
  tool; the only constant is the rule (`no custom op AND min_runtime_version ≤ target`).
- **Bundles are AND'd.** A `.task` (MediaPipe Tasks bundle) is a ZIP of inner `.tflite`(s) + metadata. The tool unzips
  and parses each inner model; the candidate's verdict is the **AND over inner models** (one custom op anywhere → the
  whole bundle fails that envelope).
- **Refuse to stamp a suspect parse.** A parse that finds **zero operator codes** is suspect (wrong table / corrupt
  read) — the tool **refuses to emit a verdict** for it (exit 2), to avoid a false PASS. Treat exit 2 as "re-check the
  input", not as PASS or FAIL.

## Triggers
- **Manual / keyword**: "过一下运行时包络" / "gate this model against a runtime" / "check tflite custom ops" /
  "runtime envelope gate" / "screen a .tflite / .task for adoption" / "静态算子包络核对".
- Run when **selecting/adopting a model** for a runtime, or when **recording a model card's runtime-compatibility
  verdict**. Not automatic — it is a screening step you invoke on a candidate.

## Usage
The gate ships as `references/envelope_gate.py` (regen-local, beside this `SKILL.md`). Run:
```
python references/envelope_gate.py <model.tflite | bundle.task> \
    --envelope <name>=<version> [--envelope <name>=<version> ...] [--json]
```
- `--envelope NAME=VERSION` is **repeatable**: pass one per runtime you must satisfy. `NAME` is a label for the report
  (e.g. `host`, `device`); `VERSION` is that runtime's version (e.g. `2.1.0`). All versions are **caller-supplied**.
- `--json` emits a machine-readable record (per-inner-model ops + per-envelope verdict + `parse_suspect`) suitable for
  a model-card `runtime_envelope_gate` block; omit it for a human-readable dump.
- **Exit codes**: `0` = PASS (all envelopes) · `1` = REJECTED-envelope (≥1 envelope failed) · `2` = parse-suspect
  (zero operator codes — no verdict stamped; re-check the input).

## Procedure
1. **Identify the envelopes** the candidate must satisfy (each = a runtime + its version). These come from the consuming
   project, not this skill — e.g. a host runtime version and a device runtime version.
2. **Run the gate** with one `--envelope NAME=VERSION` per runtime (`--json` if feeding a model card).
3. **Read the verdict**: PASS only if every envelope passes for every inner model. On REJECT, the report names the
   offending operator(s) and/or the version mismatch per envelope — that is the rejection evidence.
4. **On exit 2 (parse-suspect)**: do **not** treat as PASS or FAIL — the flatbuffer parse found zero operator codes;
   re-verify the input file (right path, not truncated/corrupt) and re-run.
5. **Record** the verdict where adoption decisions live (e.g. a model card / baseline record), citing the operators +
   versions, so the gate result is auditable.

## Rules
- **Static-parse, fail-closed** — never load the model in a runtime to gate it (the gate must survive the
  custom-op-won't-load case); never certify PASS on an unknown `min_runtime_version`; never stamp a verdict on a
  zero-operator-code parse.
- **Caller-supplied envelopes** — the target version(s) are inputs; do not hardcode a runtime version in the tool or
  the skill (the `2.1.0` / `2.10.0` in examples are illustrative caller values, not defaults).
- **Selection gate, not a converter** — this reads a model and judges it; it never edits, converts, or re-exports the
  model. Read-only on the candidate.

## Never touched
- The model's **adoption** decision itself — a user-consent matter (skill_spec §6). This gate produces the PASS/REJECT
  evidence; whether to adopt a passing model is decided elsewhere.
- The candidate `.tflite` / `.task` — read-only; the gate parses it, it does not modify or re-export it.

## References
- `references/envelope_gate.py` — the static flatbuffer op-dump gate (no-TensorFlow; `pip install tflite flatbuffers`).
  Parameterized by `--envelope NAME=VERSION` (repeatable); handles `.tflite` and `.task` bundles; fails closed on
  unknown version and refuses a zero-op parse (exit 2).
