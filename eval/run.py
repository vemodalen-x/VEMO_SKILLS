#!/usr/bin/env python3
"""Executable conformance eval for VEMO_SKILLS."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "tools" / "vemo_skills_check.py"
OUT = ROOT / "eval" / "out" / "report.json"
PY = sys.executable or "python3"


def run(*args: str):
    proc = subprocess.run([PY, str(CHECK), "--root", str(ROOT), *args],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def score_json():
    from importlib.machinery import SourceFileLoader

    mod = SourceFileLoader("vemo_skills_check", str(CHECK)).load_module()
    return mod.score(ROOT)


def checker_module():
    from importlib.machinery import SourceFileLoader

    return SourceFileLoader("vemo_skills_check_eval", str(CHECK)).load_module()


checks = []


def add(name: str, ok: bool, got: str = ""):
    checks.append({"name": name, "pass": bool(ok), "got": got})


report = score_json()
by_dim = {c["dimension"]: c for c in report["checks"]}

add("score reaches release threshold", report["score"] >= 9.5, str(report["score"]))
add("activation index parity", by_dim["activation_index"]["pass"], by_dim["activation_index"]["evidence"])
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
st = subprocess.run([PY, str(CREATOR), "selftest"], capture_output=True, text=True)
add("skill-creator selftest passes", st.returncode == 0,
    (st.stdout.strip().splitlines() or [st.stderr.strip()])[-1])

code, out, err = run("catalog")
catalog_count = len([line for line in out.splitlines() if line.strip()])
add("CLI catalog command", code == 0 and catalog_count == report["skills"], f"code={code} count={catalog_count}")

with tempfile.TemporaryDirectory(prefix="vemo_skills_eval_index_") as temporary:
    fixture = Path(temporary)
    skill_file = fixture / "skills" / "code" / "reviewing-widgets" / "SKILL.md"
    skill_file.parent.mkdir(parents=True)
    skill_file.write_text("---\nname: reviewing-widgets\ndescription: Use when reviewing widgets.\n---\n", encoding="utf-8")
    index_file = fixture / "skills" / "index.json"
    index_file.write_text(
        '{"schema_version":1,"skills":["../outside/SKILL.md"],"skills":[]}', encoding="utf-8"
    )
    references, duplicate_issues = checker_module().activation_index(fixture)
    index_file.write_text('{"schema_version":1,"skills":[]}', encoding="utf-8")
    drift_references, drift_issues = checker_module().activation_index(fixture)
    blocked_destination = fixture / "bound"
    blocked_bind = checker_module().cmd_bind(fixture, blocked_destination, False)
    index_file.write_text(
        '{"schema_version":1,"skills":["code/reviewing-widgets/SKILL.md"]}', encoding="utf-8"
    )
    duplicate_row = "| code | `code/reviewing-widgets` | does | when | boundary |\n"
    for readme in ("README.md", "README_zh.md"):
        (fixture / readme).write_text(duplicate_row * 2, encoding="utf-8")
    duplicate_catalog = checker_module().check_catalog(fixture, checker_module().skills(fixture))
    second_skill = fixture / "skills" / "research" / "reviewing-widgets" / "SKILL.md"
    second_skill.parent.mkdir(parents=True)
    second_skill.write_text(
        "---\nname: reviewing-widgets\ndescription: Use when reviewing widgets.\n---\n", encoding="utf-8"
    )
    index_file.write_text(
        '{"schema_version":1,"skills":["code/reviewing-widgets/SKILL.md",'
        '"research/reviewing-widgets/SKILL.md"]}', encoding="utf-8"
    )
    _, flattened_name_issues = checker_module().activation_index(fixture)
    add(
        "registration rejects ambiguity and blocks invalid binding",
        not references and not drift_references
        and any("valid JSON" in issue for issue in duplicate_issues)
        and any("unregistered tree skills" in issue for issue in drift_issues)
        and blocked_bind == 2 and not blocked_destination.exists()
        and not duplicate_catalog["pass"]
        and any("duplicate flattened bind name" in issue for issue in flattened_name_issues),
        "; ".join(duplicate_issues + drift_issues + flattened_name_issues)
        + f"; duplicate_catalog_pass={duplicate_catalog['pass']}",
    )

with tempfile.TemporaryDirectory(prefix="vemo_skills_eval_bind_") as temporary:
    destination = Path(temporary) / "skills"
    bound = subprocess.run(
        [PY, str(CHECK), "--root", str(ROOT), "bind", "--dest", str(destination)],
        capture_output=True, text=True,
    )
    bound_count = len([path for path in destination.iterdir() if path.is_dir()]) if destination.exists() else 0
    metadata_count = len(list(destination.glob("*/agents/openai.yaml"))) if destination.exists() else 0
    add(
        "index-driven bind materializes metadata",
        bound.returncode == 0 and bound_count == report["skills"] and metadata_count == report["skills"],
        f"code={bound.returncode} skills={bound_count} metadata={metadata_count}",
    )

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
