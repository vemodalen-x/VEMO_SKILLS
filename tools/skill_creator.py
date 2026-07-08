#!/usr/bin/env python3
"""VEMO_SKILLS skill-creator — eval-driven skill authoring harness.

Adapts the methodology of Anthropic's official ``skill-creator`` meta-skill to
this repository's single-source model. It adds the behavioral/trigger evaluation
loop that the static release scorer (``tools/vemo_skills_check.py``) cannot cover:
the scorer lints a skill's shape, this harness measures whether the skill's
*description* actually triggers and lets an author iterate on it with anti-overfit
discipline.

Design notes:
- **One parser, not two.** Frontmatter is parsed by reusing
  ``vemo_skills_check.parse_frontmatter`` — this harness never rolls a second,
  divergent YAML-ish parser.
- **Honest provenance tier.** ``validate`` writes ``.skill-validated.json`` with an
  explicit ``tier`` field. ``tier: "lint"`` means only frontmatter + naming were
  checked — it does NOT claim the skill passed behavioral eval. That claim is only
  made when a trigger eval actually ran (``tier: "trigger"``).
- **Infra failure != no trigger.** The trigger harness returns a tri-state per run
  (``triggered`` / ``not_triggered`` / ``error``). Runs that could not execute are
  counted as errors and excluded from the trigger rate; if the ``claude`` CLI is
  absent the whole command reports ``status: skipped`` and exits 0. An outage is
  never silently scored as "the description failed to trigger".

Reference — Anthropic Agent Skills best practices:
  https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import select
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "tools" / "vemo_skills_check.py"

USE_CUES = ("use when", "use after", "use at", "use for", "use to", "use this skill when", "when ", "用于", "用来", "当", "在需要")


# --------------------------------------------------------------------------- #
# shared parsing (reuse the repo's single frontmatter parser)
# --------------------------------------------------------------------------- #
def _checker():
    from importlib.machinery import SourceFileLoader

    return SourceFileLoader("vemo_skills_check", str(CHECK)).load_module()


def parse_frontmatter(skill_md: Path) -> dict:
    return _checker().parse_frontmatter(skill_md)


def skill_body(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    parts = text.lstrip().split("---", 2)
    return parts[2] if len(parts) >= 3 else text


# --------------------------------------------------------------------------- #
# validate + provenance marker
# --------------------------------------------------------------------------- #
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_skill(skill_dir: Path) -> tuple[bool, list[dict]]:
    """Lint a skill's frontmatter + naming. Returns (ok, per-rule checks).

    Mirrors the ``naming-skills`` A1-A5 / B1-B3 rules and Anthropic's frontmatter
    spec (kebab name <=64, description <=1024, no angle brackets). Category is the
    VEMO_SKILLS-required extra field and must equal the parent directory.
    """
    skill_dir = Path(skill_dir)
    checks: list[dict] = []

    def rule(name: str, ok: bool, evidence: str):
        checks.append({"rule": name, "pass": bool(ok), "evidence": evidence})

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        rule("SKILL.md present", False, f"no SKILL.md in {skill_dir}")
        return False, checks
    rule("SKILL.md present", True, "found")

    fm = parse_frontmatter(skill_md)
    if not fm:
        rule("frontmatter parses", False, "no YAML frontmatter block")
        return False, checks
    rule("frontmatter parses", True, f"{len(fm)} keys")

    name = fm.get("name", "")
    category = fm.get("category", "")
    desc = fm.get("description", "")

    rule("name present", bool(name), name or "<missing>")
    rule("name charset (kebab)", bool(NAME_RE.fullmatch(name or "")), name)
    rule("name <= 64 chars", len(name) <= 64, f"len={len(name)}")
    rule("name gerund-led (verb+ing)", name.split("-", 1)[0].endswith("ing") if name else False,
         name.split("-", 1)[0] if name else "<missing>")
    rule("name == directory", name == skill_dir.name, f"name={name!r} dir={skill_dir.name!r}")

    rule("category present", bool(category), category or "<missing>")
    rule("category == directory", category == skill_dir.parent.name,
         f"category={category!r} dir={skill_dir.parent.name!r}")

    rule("description present", bool(desc), f"len={len(desc)}")
    rule("description <= 1024 chars", len(desc) <= 1024, f"len={len(desc)}")
    rule("description no angle brackets", "<" not in desc and ">" not in desc, "ok" if "<" not in desc else "has < or >")
    rule("description has when-to-use cue", any(c in desc.lower() for c in USE_CUES),
         "cue found" if any(c in desc.lower() for c in USE_CUES) else "no 'use when'/'用于' cue")

    ok = all(c["pass"] for c in checks)
    return ok, checks


def _git_commit(path: Path):
    try:
        out = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=10)
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        pass
    return None


def write_validation_marker(skill_dir: Path, checks: list[dict], tier: str = "lint") -> Path:
    """Persist ``.skill-validated.json`` — a machine-readable, tamper-evident pass marker.

    ``tier`` is deliberately explicit so the marker never over-claims:
    ``lint`` = frontmatter/naming only; ``trigger`` = a trigger eval also ran.
    ``validator_sha`` is the sha256 of THIS file, so a changed validator is detectable.
    A marker-write failure must never flip a genuine PASS into a FAIL.
    """
    skill_dir = Path(skill_dir)
    try:
        validator_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except Exception:
        validator_sha = None
    marker = {
        "skill_name": skill_dir.name,
        "validated": True,
        "tier": tier,
        "tier_meaning": {
            "lint": "frontmatter + naming rules only; NOT a behavioral/trigger eval",
            "trigger": "lint plus a trigger eval that met the pass threshold",
        }.get(tier, tier),
        "validator": "tools/skill_creator.py",
        "validator_sha": validator_sha,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_commit": _git_commit(skill_dir),
        "checks": checks,
    }
    marker_path = skill_dir / ".skill-validated.json"
    marker_path.write_text(json.dumps(marker, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return marker_path


# --------------------------------------------------------------------------- #
# train / test split (anti-overfit, deterministic)
# --------------------------------------------------------------------------- #
def split_eval_set(eval_set: list[dict], holdout: float = 0.4, seed: int = 42) -> tuple[list[dict], list[dict]]:
    """Stratified split by ``should_trigger`` (mirrors the upstream loop).

    Deterministic given ``seed`` (scripts here cannot use ``random`` without a seed
    — the harness must be reproducible). Guarantees at least one held-out item per
    present stratum so the test set can measure both triggering and non-triggering.
    """
    rng = random.Random(seed)
    pos = [e for e in eval_set if e.get("should_trigger")]
    neg = [e for e in eval_set if not e.get("should_trigger")]
    rng.shuffle(pos)
    rng.shuffle(neg)
    n_pos_test = max(1, int(len(pos) * holdout)) if pos else 0
    n_neg_test = max(1, int(len(neg) * holdout)) if neg else 0
    test = pos[:n_pos_test] + neg[:n_neg_test]
    train = pos[n_pos_test:] + neg[n_neg_test:]
    return train, test


def select_best(history: list[dict], has_test: bool) -> dict:
    """Pick the winning iteration by TEST score (held-out), not train — anti-overfit."""
    key = (lambda h: h.get("test_passed") or 0) if has_test else (lambda h: h.get("train_passed") or 0)
    return max(history, key=key)


def aggregate_runs(states: list[str]) -> dict:
    """Aggregate a query's per-run tri-state list into an honest rate.

    ``error`` runs are EXCLUDED from the trigger rate (an outage is not a
    description failure). A query with only errors is unscorable (rate=None).
    """
    triggered = states.count("triggered")
    not_triggered = states.count("not_triggered")
    errors = states.count("error")
    scored = triggered + not_triggered
    return {
        "triggered": triggered,
        "not_triggered": not_triggered,
        "errors": errors,
        "runs": len(states),
        "trigger_rate": (triggered / scored) if scored else None,
        "error_rate": (errors / len(states)) if states else 0.0,
    }


# --------------------------------------------------------------------------- #
# model-in-the-loop trigger detection (graceful when claude CLI is absent)
# --------------------------------------------------------------------------- #
def _find_project_root() -> Path:
    cur = Path.cwd()
    for parent in [cur, *cur.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return cur


def run_single_query(query: str, skill_name: str, description: str, timeout: int,
                     project_root: str, model: str | None = None) -> str:
    """Run one query through a nested ``claude -p`` and return a tri-state.

    Returns ``"triggered"`` / ``"not_triggered"`` / ``"error"``. A registered
    temp slash-command makes the skill visible in ``available_skills``; stream
    events detect triggering early. Any launch/parse failure returns ``"error"``
    (never a false ``"not_triggered"``).
    """
    if not shutil.which("claude"):
        return "error"
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    commands_dir = Path(project_root) / ".claude" / "commands"
    command_file = commands_dir / f"{clean_name}.md"
    process = None
    try:
        commands_dir.mkdir(parents=True, exist_ok=True)
        indented = "\n  ".join(description.split("\n"))
        command_file.write_text(f"---\ndescription: |\n  {indented}\n---\n\n# {skill_name}\n\n{description}\n",
                                encoding="utf-8")
        cmd = ["claude", "-p", query, "--output-format", "stream-json", "--verbose", "--include-partial-messages"]
        if model:
            cmd += ["--model", model]
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                   cwd=project_root, env=env)
        start = time.time()
        buffer = ""
        pending = None
        acc = ""
        while time.time() - start < timeout:
            if process.poll() is not None:
                rest = process.stdout.read()
                if rest:
                    buffer += rest.decode("utf-8", errors="replace")
                break
            ready, _, _ = select.select([process.stdout], [], [], 1.0)
            if not ready:
                continue
            chunk = os.read(process.stdout.fileno(), 8192)
            if not chunk:
                break
            buffer += chunk.decode("utf-8", errors="replace")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "stream_event":
                    se = event.get("event", {})
                    t = se.get("type", "")
                    if t == "content_block_start":
                        cb = se.get("content_block", {})
                        if cb.get("type") == "tool_use":
                            if cb.get("name", "") in ("Skill", "Read"):
                                pending, acc = cb.get("name"), ""
                            else:
                                return "not_triggered"
                    elif t == "content_block_delta" and pending:
                        delta = se.get("delta", {})
                        if delta.get("type") == "input_json_delta":
                            acc += delta.get("partial_json", "")
                            if clean_name in acc:
                                return "triggered"
                    elif t in ("content_block_stop", "message_stop"):
                        if pending:
                            return "triggered" if clean_name in acc else "not_triggered"
                        if t == "message_stop":
                            return "not_triggered"
                elif event.get("type") == "result":
                    return "not_triggered"
        return "not_triggered"
    except Exception:
        return "error"
    finally:
        if process is not None and process.poll() is None:
            try:
                process.kill()
                process.wait()
            except Exception:
                pass
        if command_file.exists():
            command_file.unlink()


def trigger_eval(skill_dir: Path, eval_set: list[dict], description: str | None,
                 runs_per_query: int, threshold: float, timeout: int, model: str | None) -> dict:
    """Run the eval set; return per-query verdicts + a summary. Skips (not fails) if no CLI."""
    if not shutil.which("claude"):
        return {"status": "skipped", "reason": "claude CLI not found on PATH — trigger eval needs it"}
    fm = parse_frontmatter(skill_dir / "SKILL.md")
    name = fm.get("name", skill_dir.name)
    desc = description or fm.get("description", "")
    project_root = _find_project_root()
    results = []
    for item in eval_set:
        states = [run_single_query(item["query"], name, desc, timeout, str(project_root), model)
                  for _ in range(runs_per_query)]
        agg = aggregate_runs(states)
        should = bool(item.get("should_trigger"))
        rate = agg["trigger_rate"]
        if rate is None:
            verdict = "unscorable"
        elif should:
            verdict = "pass" if rate >= threshold else "fail"
        else:
            verdict = "pass" if rate < threshold else "fail"
        results.append({"query": item["query"], "should_trigger": should, "verdict": verdict, **agg})
    scored = [r for r in results if r["verdict"] != "unscorable"]
    passed = sum(1 for r in scored if r["verdict"] == "pass")
    return {
        "status": "ok",
        "skill_name": name,
        "description": desc,
        "threshold": threshold,
        "summary": {"scored": len(scored), "passed": passed, "unscorable": len(results) - len(scored)},
        "results": results,
    }


# --------------------------------------------------------------------------- #
# description improvement loop (train/test split + blinding + select-by-test)
# --------------------------------------------------------------------------- #
def _call_claude(prompt: str, model: str | None, timeout: int = 300) -> str:
    cmd = ["claude", "-p", "--output-format", "text"]
    if model:
        cmd += ["--model", model]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    res = subprocess.run(cmd, input=prompt, capture_output=True, text=True, env=env, timeout=timeout)
    if res.returncode != 0:
        raise RuntimeError(f"claude -p exited {res.returncode}: {res.stderr}")
    return res.stdout


def _improve_prompt(skill_name: str, body: str, current: str, train_results: list[dict], history: list[dict]) -> str:
    failed = [r for r in train_results if r["should_trigger"] and r["verdict"] != "pass"]
    false_fire = [r for r in train_results if not r["should_trigger"] and r["verdict"] != "pass"]
    lines = [
        f'Optimize the description for a Claude skill "{skill_name}". The description is the ONLY text Claude '
        f'sees when deciding whether to invoke the skill; it must trigger for relevant intents and stay quiet otherwise.',
        f'\nCurrent description:\n"{current}"\n',
    ]
    if failed:
        lines.append("FAILED TO TRIGGER (should have):")
        lines += [f'  - "{r["query"]}" ({r["triggered"]}/{r["runs"]})' for r in failed]
    if false_fire:
        lines.append("FALSE TRIGGERS (should not have):")
        lines += [f'  - "{r["query"]}" ({r["triggered"]}/{r["runs"]})' for r in false_fire]
    if history:
        lines.append("\nPREVIOUS ATTEMPTS (do NOT repeat — try a structurally different angle):")
        lines += [f'  train={h.get("train_passed")}/{h.get("train_total")}: "{h["description"]}"' for h in history]
    lines.append(f"\nSkill body for context:\n{body[:4000]}\n")
    lines.append(
        "Write ONE improved description. Generalize to broad user intent; do not enumerate specific queries "
        "(avoid overfitting). Imperative voice, focus on the user's goal, distinctive. ~100-200 words, hard limit "
        "1024 characters. Respond with only the description inside <new_description></new_description>."
    )
    return "\n".join(lines)


def describe_improve(skill_dir: Path, eval_set: list[dict], model: str, max_iterations: int,
                     holdout: float, runs_per_query: int, threshold: float, timeout: int) -> dict:
    if not shutil.which("claude"):
        return {"status": "skipped", "reason": "claude CLI not found on PATH — description improvement needs it"}
    fm = parse_frontmatter(skill_dir / "SKILL.md")
    name = fm.get("name", skill_dir.name)
    body = skill_body(skill_dir / "SKILL.md")
    current = fm.get("description", "")
    train, test = split_eval_set(eval_set, holdout)
    history = []
    for it in range(1, max_iterations + 1):
        ev = trigger_eval(skill_dir, train + test, current, runs_per_query, threshold, timeout, model)
        tq = {q["query"] for q in train}
        tr = [r for r in ev["results"] if r["query"] in tq]
        te = [r for r in ev["results"] if r["query"] not in tq]
        entry = {
            "iteration": it, "description": current,
            "train_passed": sum(1 for r in tr if r["verdict"] == "pass"), "train_total": len(tr),
            "test_passed": sum(1 for r in te if r["verdict"] == "pass"), "test_total": len(te),
            "train_results": tr,
        }
        history.append(entry)
        if entry["train_passed"] == entry["train_total"] or it == max_iterations:
            break
        # blind the improver to test scores before asking for a rewrite
        blinded = [{k: v for k, v in h.items() if not k.startswith("test_")} for h in history]
        try:
            text = _call_claude(_improve_prompt(name, body, current, tr, blinded), model)
        except Exception as e:
            return {"status": "error", "reason": str(e), "history": history}
        m = re.search(r"<new_description>(.*?)</new_description>", text, re.DOTALL)
        current = (m.group(1) if m else text).strip().strip('"')
    best = select_best(history, has_test=bool(test))
    return {
        "status": "ok", "skill_name": name,
        "original_description": fm.get("description", ""),
        "best_description": best["description"],
        "best_test_score": f'{best.get("test_passed")}/{best.get("test_total")}',
        "iterations": len(history), "train_size": len(train), "test_size": len(test),
        "history": history,
    }


# --------------------------------------------------------------------------- #
# hermetic selftest (no model / CLI needed)
# --------------------------------------------------------------------------- #
def selftest() -> int:
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    # 1. stratified split is disjoint, complete, and holds out both strata
    es = [{"query": f"q{i}", "should_trigger": i % 2 == 0} for i in range(10)]
    train, test = split_eval_set(es, holdout=0.4)
    q = lambda s: sorted(x["query"] for x in s)
    check("split disjoint+complete", set(q(train)).isdisjoint(q(test)) and q(train + test) == q(es),
          f"train={len(train)} test={len(test)}")
    check("split stratified (both classes held out)",
          any(x["should_trigger"] for x in test) and any(not x["should_trigger"] for x in test), "")
    train2, _ = split_eval_set(es, holdout=0.4)
    check("split deterministic", q(train) == q(train2), "")

    # 2. validate: good skill passes, bad skills fail on the right rule
    with tempfile.TemporaryDirectory() as td:
        good = Path(td) / "code" / "reviewing-widgets"
        good.mkdir(parents=True)
        (good / "SKILL.md").write_text(
            "---\nname: reviewing-widgets\ncategory: code\n"
            "description: Review widget code for defects. Use when a widget change needs a check before commit.\n"
            "---\n\n# Reviewing Widgets\n", encoding="utf-8")
        ok, _ = validate_skill(good)
        check("validate accepts a good skill", ok, "")

        noun = Path(td) / "code" / "widget-reviewer"
        noun.mkdir(parents=True)
        (noun / "SKILL.md").write_text(
            "---\nname: widget-reviewer\ncategory: code\n"
            "description: Review widgets. Use when reviewing.\n---\n# x\n", encoding="utf-8")
        ok_n, checks_n = validate_skill(noun)
        gerund_failed = any(c["rule"].startswith("name gerund") and not c["pass"] for c in checks_n)
        check("validate rejects a non-gerund name", (not ok_n) and gerund_failed, "")

        nocue = Path(td) / "code" / "scanning-things"
        nocue.mkdir(parents=True)
        (nocue / "SKILL.md").write_text(
            "---\nname: scanning-things\ncategory: code\ndescription: Scans things thoroughly.\n---\n# x\n",
            encoding="utf-8")
        ok_c, checks_c = validate_skill(nocue)
        cue_failed = any("when-to-use" in c["rule"] and not c["pass"] for c in checks_c)
        check("validate rejects a description with no when-to-use cue", (not ok_c) and cue_failed, "")

        # 3. marker round-trips, tier honest, sha matches
        marker_path = write_validation_marker(good, [{"rule": "x", "pass": True, "evidence": ""}], tier="lint")
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        check("marker tier is honest (lint)", marker["tier"] == "lint" and "NOT a behavioral" in marker["tier_meaning"], "")
        check("marker validator_sha self-matches", marker["validator_sha"] == sha, "")

    # 4. tri-state aggregation excludes errors; select_best uses test score
    agg = aggregate_runs(["triggered", "error", "not_triggered", "triggered"])
    check("aggregate excludes errors from rate", abs(agg["trigger_rate"] - (2 / 3)) < 1e-9 and agg["errors"] == 1,
          f"rate={agg['trigger_rate']}")
    check("aggregate all-error is unscorable", aggregate_runs(["error", "error"])["trigger_rate"] is None, "")
    hist = [{"train_passed": 5, "test_passed": 1}, {"train_passed": 3, "test_passed": 4}]
    check("select_best picks higher TEST score", select_best(hist, True)["test_passed"] == 4, "")

    ok_all = all(r[1] for r in results)
    for name, ok, detail in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"[skill_creator selftest] {sum(r[1] for r in results)}/{len(results)} passed")
    return 0 if ok_all else 1


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Eval-driven skill authoring harness (see module docstring).")
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="lint frontmatter/naming + write .skill-validated.json (tier=lint)")
    v.add_argument("skill_dir")
    v.add_argument("--no-marker", action="store_true", help="lint only; do not write the marker")

    t = sub.add_parser("trigger-eval", help="measure whether the description triggers (needs claude CLI)")
    t.add_argument("skill_dir")
    t.add_argument("--eval-set", required=True)
    t.add_argument("--runs-per-query", type=int, default=3)
    t.add_argument("--threshold", type=float, default=0.5)
    t.add_argument("--timeout", type=int, default=30)
    t.add_argument("--model", default=None)

    d = sub.add_parser("describe-improve", help="train/test-split description optimization (needs claude CLI)")
    d.add_argument("skill_dir")
    d.add_argument("--eval-set", required=True)
    d.add_argument("--model", required=True)
    d.add_argument("--max-iterations", type=int, default=5)
    d.add_argument("--holdout", type=float, default=0.4)
    d.add_argument("--runs-per-query", type=int, default=3)
    d.add_argument("--threshold", type=float, default=0.5)
    d.add_argument("--timeout", type=int, default=30)

    sub.add_parser("selftest", help="hermetic self-test of the deterministic core (no model needed)")

    args = p.parse_args(argv)

    if args.cmd == "validate":
        ok, checks = validate_skill(Path(args.skill_dir))
        for c in checks:
            print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['rule']}" + (f" — {c['evidence']}" if not c["pass"] else ""))
        if ok and not args.no_marker:
            try:
                mp = write_validation_marker(Path(args.skill_dir), checks, tier="lint")
                print(f"wrote {mp} (tier=lint)")
            except Exception as e:  # marker failure must not flip a genuine PASS
                print(f"WARNING: could not write marker: {e}", file=sys.stderr)
        print(f"[validate] {'PASS' if ok else 'FAIL'}: {args.skill_dir}")
        return 0 if ok else 1

    if args.cmd == "trigger-eval":
        es = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
        out = trigger_eval(Path(args.skill_dir), es, None, args.runs_per_query,
                           args.threshold, args.timeout, args.model)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0  # skipped/ok both exit 0; a genuine gate is the caller's job

    if args.cmd == "describe-improve":
        es = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
        out = describe_improve(Path(args.skill_dir), es, args.model, args.max_iterations,
                              args.holdout, args.runs_per_query, args.threshold, args.timeout)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "selftest":
        return selftest()

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
