#!/usr/bin/env python3
"""Executable conformance eval for VEMO_SKILLS."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "tools" / "vemo_skills_check.py"
OUT = ROOT / "eval" / "out" / "report.json"


def run(*args: str):
    proc = subprocess.run(["python3", str(CHECK), "--root", str(ROOT), *args],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def score_json():
    from importlib.machinery import SourceFileLoader

    mod = SourceFileLoader("vemo_skills_check", str(CHECK)).load_module()
    return mod.score(ROOT)


checks = []


def add(name: str, ok: bool, got: str = ""):
    checks.append({"name": name, "pass": bool(ok), "got": got})


report = score_json()
by_dim = {c["dimension"]: c for c in report["checks"]}

add("score reaches release threshold", report["score"] >= 9.5, str(report["score"]))
add("catalog parity", by_dim["catalog_sync"]["pass"], by_dim["catalog_sync"]["evidence"])
add("frontmatter layout", by_dim["frontmatter_layout"]["pass"], by_dim["frontmatter_layout"]["evidence"])
add("naming and descriptions", by_dim["naming_descriptions"]["pass"], by_dim["naming_descriptions"]["evidence"])
add("reference integrity", by_dim["reference_integrity"]["pass"], by_dim["reference_integrity"]["evidence"])
add("regen binding", by_dim["regen_binding"]["pass"], by_dim["regen_binding"]["evidence"])
add("release hygiene", by_dim["version_release"]["pass"], by_dim["version_release"]["evidence"])
add("public docs", by_dim["public_packaging_docs"]["pass"], by_dim["public_packaging_docs"]["evidence"])
add("security decoupling", by_dim["security_decoupling"]["pass"], by_dim["security_decoupling"]["evidence"])
add("attribution governance", by_dim["attribution_governance"]["pass"], by_dim["attribution_governance"]["evidence"])

CREATOR = ROOT / "tools" / "skill_creator.py"
add("skill-creator harness present", CREATOR.exists(), "tools/skill_creator.py" if CREATOR.exists() else "missing")
st = subprocess.run(["python3", str(CREATOR), "selftest"], capture_output=True, text=True)
add("skill-creator selftest passes", st.returncode == 0,
    (st.stdout.strip().splitlines() or [st.stderr.strip()])[-1])

code, out, err = run("catalog")
catalog_count = len([line for line in out.splitlines() if line.strip()])
add("CLI catalog command", code == 0 and catalog_count == report["skills"], f"code={code} count={catalog_count}")

passed = sum(1 for c in checks if c["pass"])
payload = {
    "passed": passed,
    "total": len(checks),
    "rate": round(passed / len(checks), 3),
    "score": report["score"],
    "threshold": report["threshold"],
    "checks": checks,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")

for c in checks:
    print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['name']}")
print(f"[eval] conformance {passed}/{len(checks)}; score={report['score']:.2f}/10 -> {OUT.relative_to(ROOT)}")
raise SystemExit(0 if passed == len(checks) else 1)
