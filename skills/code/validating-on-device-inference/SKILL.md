---
name: validating-on-device-inference
category: code
description: Run a converted model on a real device and accept it — push the package, run, collect results + logs, then judge numerical consistency (host↔device) first and performance second. Consistency = elementwise |Δ| ≤ caller tol + argmax agreement N/N; low-precision budget judged on softmax distance + decision equivalence (NOT raw logit); canary headroom = margin ÷ observed device deviation. Performance = warmup/timing rounds separated, latency reported as a distribution (not one shot) with the platform it was measured on, delegate on/off each re-verified, power as an annotated proxy. A weaker-than-target test platform extrapolates conservatively (pass = directional PASS; fail = inconclusive not dead; a thin pass margin must be discounted and flagged "target must be measured"). Use when a model has cleared host-side gates and must be signed off on the target hardware. Methodology checklist — emits PASS/FAIL report rows; all device/model/threshold values are read from the caller, none are baked in.
allowed-tools: Read, Bash, Grep, Glob
---

# Validating On-Device Inference

Accept a converted model on the **real target device**: push the package, run it, collect results and logs,
then judge it on two axes — **numerical consistency** (does the device reproduce the host answer?) and
**performance** (latency / accelerator / power proxy). This is a **methodology checklist**: it tells you
*what to measure and how to judge*, and emits a PASS/FAIL report row per item to feed an upper-layer
acceptance. It does **not** convert models, edit code, or run the device for you.

> **Consistency outranks performance.** A model that is fast but numerically off is a reject; a model that is
> correct but slow is a tuning problem. Run the consistency block first; only spend device time on the
> performance block once consistency PASSES. Every concrete value — device id, model file, tolerance,
> latency gate, canary margin — is **read from the caller / instance**, never baked into this skill.

## When to use
- A model has cleared the host-side static and numerical gates and now needs **device sign-off** on the
  actual target hardware before it ships.
- You need to prove the device reproduces the host's answer, measure on-device latency honestly, and check
  an accelerator delegate without silently changing the numbers.
- Trigger phrases: "上板测试", "真机验收", "host↔device 一致性", "device numerical parity",
  "on-device latency p50/p90", "delegate 数值复验", "设备端签收".

## Inputs the caller supplies (this skill bakes in none)
- **Device handle** — how to reach the target (e.g. an `adb` serial); the skill assumes one reachable device.
- **Package** — the runnable artifact(s): the model file(s) (full- and reduced-precision variants), the
  golden fixture (known inputs + host reference outputs), and the executable/runner.
- **Judgement parameters** — elementwise tolerance `tol`; low-precision **budget** on softmax distance; the
  latency **gate** (and which percentiles matter); the **canary** sample id + its host margin; the decision
  rule values (any thresholds the runner needs to reproduce the host decision).
- **Own device directory** — a writable path under `/data/local/tmp/<own-dir>` reserved for this run.

## Block 0 — Push & environment (single-writer discipline)
- [ ] **Detect the device** — confirm exactly one reachable device and capture its identity (serial, SoC /
      board, OS build) into the report header. Abort if zero or ambiguous-multiple.
- [ ] **Push to your own directory only** — `push` the package to `/data/local/tmp/<own-dir>`. You are the
      **single writer** of that path; never write into another agent's device directory, never assume a
      shared scratch dir is yours. If you must clean up, clean only your own dir and **report before deleting**.
- [ ] **Verify the landing** — check pushed files exist + sizes match (a truncated push is a silent failure
      source); confirm the runner's shared-library dependencies resolve on-device (a missing `.so` aborts at
      launch, not build).
- [ ] **Mark down the exact runner invocation** so every later block re-runs the same command.

## Block 1 — Numerical consistency (highest priority — run first)

### 1a. Known-answer check (device vs host golden)
Feed the **golden fixture** (the known inputs whose host reference outputs you carry) through the device
runner and compare elementwise.
- [ ] **Elementwise** `max|Δ|` over all outputs **≤ caller `tol`** → PASS; count rows over tol (should be 0).
- [ ] **Argmax agreement N/N** — the device's decision index equals the host's on **every** fixture row.
- A scrambled feed (wrong layout / transpose) shows up here as a **large Δ**, not a subtle one — this block
  is what proves the device's input plumbing is faithful, so do not skip it even if the full-precision host
  parity was already proven.

### 1b. Low-precision budget (the easy-to-get-wrong one)
When the device runs a **reduced-precision** variant, judge it on the **decision-relevant** distance, not the
raw numbers:
- [ ] Judge on **softmax/probability distance ≤ caller budget** *and* **argmax/decision equivalence** —
      **NOT** on raw-logit Δ. Raw logits can drift past a logit-space tolerance while the decision is
      unchanged; the classification head's job is the *decision*, so the budget lives in probability space.
- [ ] Report both numbers (logit Δ for information, softmax Δ for the verdict) so the reader sees why a
      "large" logit drift can still PASS.

### 1c. Canary headroom (a comparable margin reading)
- [ ] Take the caller's **canary** sample (the golden row with the smallest top1–top2 margin) and compute
      **headroom = margin ÷ observed device deviation** (the device-side softmax deviation from host). A large
      ratio means the perturbation needed to flip the decision far exceeds the deviation actually observed.
- [ ] **Caveat — absolute margin is NOT cross-comparable** across golden sets of different sizes / makeups;
      the **ratio (margin ÷ deviation) is** the portable reading. Report the ratio, not the bare margin, when
      comparing runs.

## Block 2 — Performance (only after Block 1 PASSES)

### 2a. Latency — honest distribution, not a single shot
- [ ] **Separate warmup rounds from timing rounds** — discard the first N runs (kernel JIT / cache warm) and
      time the steady-state runs only.
- [ ] Report the **distribution** — at minimum the caller's percentiles (e.g. p50 / p90) — **not one number**.
      Thermal drift makes a single reading unrepresentative; a hot device runs slower.
- [ ] Judge each reported percentile against the caller's **latency gate** → PASS/FAIL per percentile.
- [ ] **Weak-substitute-platform extrapolation (when you measured on a platform *weaker* than the target).** If the test
      platform is **weaker** than the ship target, the measurement is a **conservative proxy**, and the two outcomes are
      asymmetric:
      - **Passes the gate on the weaker platform → directional PASS** is sound: the stronger target should be at least as
        fast, so the gate holds *with margin to spare*. Extrapolate the conclusion (not the exact number).
      - **Fails the gate on the weaker platform → do NOT call it dead.** A weaker platform missing the gate does not
        prove the target misses it; mark **inconclusive / target re-test required**, never a hard FAIL on the proxy.
      - **Thin-margin caveat (hard).** When the pass margin is **thin** (e.g. **< ~20%** of the gate — caller sets the
        threshold), the directional PASS is **fragile**: **discount it and annotate "target platform must be measured"**
        — a small platform delta or thermal drift can erase a thin margin. A comfortable margin extrapolates; a thin one
        does not stand on its own.
      - **Always annotate the platform** each latency number was measured on, and whether it is the **target** or a
        **weaker substitute** (the R6 measured-vs-inferred posture: a substitute-platform number is *inferred* for the
        target, not *measured* on it).
- [ ] *(Reuse, not reinvent)* the upstream **TFLite benchmark binary** is a reasonable off-the-shelf tool for
      the timing-round collection if the runtime is TFLite; this skill governs *how to judge*, not the stopwatch.

### 2b. Accelerator delegate — measure on/off AND re-verify numbers
- [ ] Run **delegate-on and delegate-off** and report both latencies (the speedup is the delegate's value).
- [ ] **Re-run Block 1's consistency check under the delegate** — a delegate can change the numerics; an
      accelerated path that fails parity is a reject, not a win. Never report a delegate latency without its
      paired numerical re-verification.

### 2c. Power — proxy only, labelled as such
- [ ] With no power meter, collect **proxy indicators** — CPU occupancy / clock frequency / temperature rise
      across the timing run.
- [ ] **Annotate every power line "proxy, NOT a measured-power figure."** A proxy may *not* be reported as
      power consumption. State the indicator and its limitation in the same line.

## Block 3 — Logs & exit
- [ ] **Filter device logs to your own tag** (logcat / equivalent) — don't drown the report in system noise.
- [ ] Capture the runner's **exit code**; a non-zero exit or a crash signature is a FAIL regardless of any
      partial numbers printed before it.
- [ ] **Crash fallback** — if the runner dies mid-run, report the last log lines + exit signal as the
      evidence; never paper over a crash with a half-collected pass.

## Block 4 — Report rows (feed the upper-layer acceptance)
Emit **one line per item**, each `PASS`/`FAIL` + the number behind it, under a header carrying the device
identity and the exact runner invocation. Minimum rows:
- `consistency.known-answer` — `max|Δ| = … (tol …)`, `argmax N/N`.
- `consistency.budget` — `softmax max|Δ| = … (budget …)`, `decision-equiv yes/no`.
- `consistency.canary` — `headroom = margin/deviation = …×`.
- `latency.pXX` — each percentile vs gate, **with the platform it was measured on** (target vs weaker substitute); a
  thin-margin pass on a substitute carries the **"target platform must be measured"** annotation, a sub-gate result on a
  weaker substitute is **inconclusive**, not FAIL.
- `delegate` — on/off latencies **+** the re-verified consistency line.
- `power.proxy` — the proxy indicator(s), explicitly labelled non-measured.
- `exit` — exit code / crash status.

**Overall:** any **consistency** FAIL → device-reject (do not let a good latency override it). Consistency all
PASS + latency within gate → device-accept; a latency-only FAIL is a tuning flag, not a correctness reject —
say which it is.

## Common traps (拷打出来的)
- **Truncated / permission-denied push** — verify sizes on-device; a partial file fails at run, not at push.
- **Missing `.so` at launch** — resolve the runner's shared-lib deps on-device before timing anything.
- **Single-shot latency** — thermal drift makes one reading lie; always report a distribution and note temp rise.
- **Raw-logit budget** — judging reduced precision on logit Δ rejects models that are decision-identical; judge
  in probability space + decision equivalence.
- **Delegate latency without re-verified numbers** — an accelerated wrong answer is still wrong.
- **Calling a proxy "power"** — CPU/freq/temp is a proxy; label it, don't dress it as measured power.
- **Trusting a thin-margin pass on a weaker platform** — a weaker substitute passing the gate by a thin margin is
  fragile (platform delta / thermal drift erases it); discount it and require a target-platform measurement. And never
  call a sub-gate result on a weaker platform a hard FAIL — it is inconclusive for the target.
- **Writing into a shared device dir** — own your `/data/local/tmp/<dir>`; coordinate before touching a path
  another writer owns; clean only your own and report first.

## Boundary & notes
- **vs static op-envelope gating** — that judgement (which ops / builtins / min-runtime a converted model
  needs) is a **pre-device, host-side** check on the artifact's *portability*; **this** skill is the
  **device-runtime** check on the *running* model's correctness + speed. Pre-device portability gate → the
  envelope-gating skill; device sign-off of the running artifact → here.
- **vs mobile-GPU conv selection** — that is a **design-time** heuristic for choosing a conv structure; this
  is **acceptance-time** validation of an already-built, already-converted model on hardware.
- **Read/measure only** — collects results, judges them, emits report rows. It does **not** convert, retrain,
  edit code, or adopt anything. The device run itself is performed by the caller's runner; this skill governs
  the discipline and the verdict.
- **Decoupling (skill_spec §9)** — this body carries **zero hardcoded project / device / model / threshold
  values**. The device handle, package, tolerances, gates, and canary are all confirmed by the consuming
  instance at runtime; this body assumes none of them.
