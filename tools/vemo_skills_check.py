#!/usr/bin/env python3
"""VEMO_SKILLS repository checker.

Stdlib-only checks for a skill-home repository:
- skill frontmatter and category placement
- README / README_zh catalog parity
- reference file integrity
- public-release hygiene
- VEMO-style executable verification surface

The score is intentionally transparent: every dimension reports points,
maximum points, status, and evidence.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path


WEIGHTS = {
    "catalog_sync": 1.2,
    "frontmatter_layout": 1.1,
    "naming_descriptions": 1.0,
    "reference_integrity": 0.8,
    "regen_binding": 0.8,
    "version_release": 0.8,
    "public_packaging_docs": 1.0,
    "security_decoupling": 0.9,
    "executable_verification": 1.3,
    "attribution_governance": 1.1,
}

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
]

PRIVATE_PATTERNS = [
    re.compile("/" + "home" + r"/[A-Za-z0-9_.-]+"),
    re.compile("/" + "media" + r"/[A-Za-z0-9_.-]+"),
    re.compile("Claude" + "Test"),
    re.compile("junxian" + "wusg", re.I),
    re.compile("BST" + "-AII"),
]


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def text_files(root: Path):
    skip_dirs = {".git", ".idea", "__pycache__", ".pytest_cache"}
    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.is_file():
            if path.suffix.lower() in {
                ".md", ".txt", ".yaml", ".yml", ".json", ".py", ".sh", ".html",
                ".svg", ".css", ".js", ".toml", ".gitignore",
            } or path.name in {"VERSION", "LICENSE"}:
                yield path


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = read(path).lstrip()
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    lines = parts[1].splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#") or ":" not in raw:
            i += 1
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if value in (">", "|"):
            block = []
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt and not nxt.startswith((" ", "\t")) and ":" in nxt:
                    break
                if nxt.strip() and not nxt.lstrip().startswith("#"):
                    block.append(nxt.strip())
                i += 1
            data[key] = " ".join(block)
            continue
        data[key] = value
        i += 1
    return data


def skills(root: Path):
    base = root / "skills"
    if not base.is_dir():
        return []
    rows = []
    for skill_md in sorted(base.glob("*/*/SKILL.md")):
        rel = skill_md.relative_to(root)
        parts = rel.parts
        fm = parse_frontmatter(skill_md)
        rows.append({
            "path": skill_md,
            "rel": str(rel),
            "category_dir": parts[1],
            "name_dir": parts[2],
            "name": fm.get("name", ""),
            "category": fm.get("category", ""),
            "description": fm.get("description", ""),
        })
    return rows


def catalog_tokens(text: str) -> set[str]:
    return set(re.findall(r"`([a-z][a-z0-9-]*/[a-z0-9][a-z0-9-]*)`", text))


def skill_tokens(rows) -> set[str]:
    return {f"{r['category']}/{r['name']}" for r in rows if r["category"] and r["name"]}


def points(name: str, ok: bool, evidence: str, partial: float | None = None):
    maxp = WEIGHTS[name]
    score = maxp if ok else (partial if partial is not None else 0.0)
    return {
        "dimension": name,
        "points": round(score, 2),
        "max": maxp,
        "pass": bool(ok),
        "evidence": evidence,
    }


def check_catalog(root: Path, rows):
    expected = skill_tokens(rows)
    missing = []
    extra = []
    bad_files = []
    for doc in ("README.md", "README_zh.md"):
        got = catalog_tokens(read(root / doc))
        only_in_tree = sorted(expected - got)
        only_in_readme = sorted(got - expected)
        if only_in_tree or only_in_readme:
            bad_files.append(doc)
            missing.extend(f"{doc}:{x}" for x in only_in_tree)
            extra.extend(f"{doc}:{x}" for x in only_in_readme)
    ok = not missing and not extra and bool(expected)
    evidence = f"{len(expected)} skills; catalog parity clean" if ok else (
        f"missing={missing[:8]} extra={extra[:8]}"
    )
    return points("catalog_sync", ok, evidence, partial=0.6 if expected else 0.0)


def check_frontmatter(rows):
    issues = []
    for r in rows:
        for key in ("name", "category", "description"):
            if not r[key]:
                issues.append(f"{r['rel']}: missing {key}")
        if r["name"] and r["name"] != r["name_dir"]:
            issues.append(f"{r['rel']}: name != directory")
        if r["category"] and r["category"] != r["category_dir"]:
            issues.append(f"{r['rel']}: category != directory")
    ok = bool(rows) and not issues
    return points("frontmatter_layout", ok, f"{len(rows)} SKILL.md files checked" if ok else "; ".join(issues[:8]))


def check_naming(rows):
    issues = []
    for r in rows:
        name = r["name"]
        desc = r["description"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name or ""):
            issues.append(f"{r['rel']}: invalid name charset")
        if len(name) > 64:
            issues.append(f"{r['rel']}: name >64 chars")
        if not (name.split("-", 1)[0].endswith("ing")):
            issues.append(f"{r['rel']}: name is not gerund-led")
        if not desc:
            issues.append(f"{r['rel']}: empty description")
        if len(desc) > 1400:
            issues.append(f"{r['rel']}: description too long for auto-invocation")
        use_cues = ("use when", "use after", "use at", "use for", "use to", "when ")
        if not any(cue in desc.lower() for cue in use_cues):
            issues.append(f"{r['rel']}: description lacks when-to-use cue")
    ok = bool(rows) and not issues
    partial = WEIGHTS["naming_descriptions"] * max(0, (len(rows) - len(issues)) / max(1, len(rows)))
    return points("naming_descriptions", ok, "all hard naming rules pass" if ok else "; ".join(issues[:8]), partial)


def check_references(root: Path, rows):
    issues = []
    ref_re = re.compile(r"`(references/[^`]+)`|(?<![A-Za-z0-9_/.-])(references/[A-Za-z0-9_./-]+)")
    for r in rows:
        skill_dir = r["path"].parent
        for match in ref_re.findall(read(r["path"])):
            ref = match[0] or match[1]
            ref = ref.rstrip(".,);:")
            if "…" in ref or ref.endswith("/"):
                continue
            if not (skill_dir / ref).exists():
                issues.append(f"{r['rel']}: dangling {ref}")
        ref_dir = skill_dir / "references"
        if ref_dir.exists() and not any(ref_dir.rglob("*")):
            issues.append(f"{r['rel']}: empty references dir")
    ok = not issues
    partial = WEIGHTS["reference_integrity"] if ok else (0.6 if len(issues) <= 2 else 0.0)
    return points("reference_integrity", ok, "reference paths resolve" if ok else "; ".join(issues[:8]), partial)


def check_regen(root: Path):
    has_docs = "Copy each" in read(root / "README.md") and ".claude/skills" in read(root / "README.md")
    has_cli = (root / "bin" / "vemo-skills").exists()
    has_tool = (root / "tools" / "vemo_skills_check.py").exists()
    sample = None
    rows = skills(root)
    if rows:
        sample_dir = rows[0]["path"].parent
        tmp = Path(tempfile.mkdtemp(prefix="vemo_skills_bind_"))
        try:
            dest = tmp / rows[0]["name"]
            shutil.copytree(sample_dir, dest)
            sample = all((dest / p.name).exists() for p in sample_dir.iterdir())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    ok = has_docs and has_cli and has_tool and bool(sample)
    partial = 0.5 if has_docs else 0.0
    if has_cli:
        partial += 0.2
    if sample:
        partial += 0.1
    return points("regen_binding", ok, f"docs={has_docs} cli={has_cli} sample_copy={bool(sample)}", min(partial, WEIGHTS["regen_binding"]))


def check_version(root: Path):
    version = read(root / "VERSION").strip()
    changelog = read(root / "CHANGELOG.md")
    semver = bool(re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?", version))
    top_has_version = bool(version and re.search(rf"^## \[{re.escape(version)}\]", changelog, re.M))
    has_gitignore = (root / ".gitignore").exists()
    has_task = any((root / "tasks").glob("T-*.md")) if (root / "tasks").is_dir() else False
    ok = semver and top_has_version and has_gitignore and has_task
    partial = sum([semver, top_has_version, has_gitignore, has_task]) / 4 * WEIGHTS["version_release"]
    return points("version_release", ok, f"version={version} changelog={top_has_version} gitignore={has_gitignore} task={has_task}", partial)


def check_public_docs(root: Path):
    needed = [
        "README.md", "README_zh.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md",
        "ROADMAP.md", "docs/INDEX.md", "docs/QUICKSTART.md", "docs/CRITIQUE_LOG.md",
        "docs/ASSESSMENT_WILDSKILLS.md", "docs/ASSESSMENT_VEMO_SKILLS.md",
    ]
    missing = [p for p in needed if not (root / p).exists()]
    ok = not missing
    partial = (len(needed) - len(missing)) / len(needed) * WEIGHTS["public_packaging_docs"]
    return points("public_packaging_docs", ok, "public docs complete" if ok else "missing " + ", ".join(missing), partial)


def check_security(root: Path):
    issues = []
    for path in text_files(root):
        if path.name.endswith(".json") and "eval/out" in str(path):
            continue
        text = read(path)
        rel = str(path.relative_to(root))
        for pat in PRIVATE_PATTERNS:
            if pat.search(text):
                issues.append(f"{rel}: private identity/path pattern {pat.pattern}")
                break
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                issues.append(f"{rel}: credential-like token")
                break
    ok = not issues
    partial = 0.5 if len(issues) <= 3 else 0.0
    return points("security_decoupling", ok, "no private paths/org identities/secrets" if ok else "; ".join(issues[:8]), partial)


def check_executable(root: Path):
    cli = root / "bin" / "vemo-skills"
    tool = root / "tools" / "vemo_skills_check.py"
    ev = root / "eval" / "run.py"
    report = root / "eval" / "out" / "report.json"
    parts = [cli.exists(), tool.exists(), ev.exists()]
    report_ok = False
    if report.exists():
        try:
            data = json.loads(read(report))
            report_ok = data.get("passed") == data.get("total") and data.get("total", 0) >= 8
        except ValueError:
            report_ok = False
    parts.append(report_ok)
    ok = all(parts)
    partial = sum(parts) / len(parts) * WEIGHTS["executable_verification"]
    return points("executable_verification", ok, f"cli={parts[0]} checker={parts[1]} eval={parts[2]} report={parts[3]}", partial)


def check_attribution(root: Path):
    needed = [
        "THIRD-PARTY-NOTICES.md", "contributors.yaml", "CONVENTIONS.md",
        "skills/governance/publishing-skills/SKILL.md",
        "skills/governance/naming-skills/SKILL.md",
    ]
    missing = [p for p in needed if not (root / p).exists()]
    critique = (root / "docs" / "CRITIQUE_LOG.md").exists()
    ok = not missing and critique
    partial = ((len(needed) - len(missing)) + int(critique)) / (len(needed) + 1) * WEIGHTS["attribution_governance"]
    return points("attribution_governance", ok, "attribution and governance docs present" if ok else "missing " + ", ".join(missing), partial)


def score(root: Path):
    root = root.resolve()
    rows = skills(root)
    checks = [
        check_catalog(root, rows),
        check_frontmatter(rows),
        check_naming(rows),
        check_references(root, rows),
        check_regen(root),
        check_version(root),
        check_public_docs(root),
        check_security(root),
        check_executable(root),
        check_attribution(root),
    ]
    total = round(sum(c["points"] for c in checks), 2)
    max_total = round(sum(WEIGHTS.values()), 2)
    return {
        "root": str(root),
        "score": total,
        "max": max_total,
        "threshold": 9.5,
        "pass": total >= 9.5 and all(c["pass"] for c in checks if c["dimension"] != "public_packaging_docs"),
        "skills": len(rows),
        "checks": checks,
    }


def print_human(report):
    print(f"VEMO_SKILLS score: {report['score']:.2f}/{report['max']:.1f} (threshold {report['threshold']})")
    print(f"root: {report['root']}")
    for c in report["checks"]:
        status = "PASS" if c["pass"] else "GAP"
        print(f"  [{status}] {c['dimension']}: {c['points']}/{c['max']} - {c['evidence']}")


def cmd_bind(root: Path, dest: Path, dry_run: bool):
    rows = skills(root)
    if not rows:
        print("no skills found", file=sys.stderr)
        return 2
    for r in rows:
        target = dest / r["name"]
        print(f"{r['rel']} -> {target}")
        if dry_run:
            continue
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(r["path"].parent, target)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="repository root to check")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("score")
    sub.add_parser("selfcheck")
    sub.add_parser("catalog")
    bind = sub.add_parser("bind")
    bind.add_argument("--dest", default=".claude/skills")
    bind.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root)

    if args.cmd == "score":
        print_human(score(root))
        return 0
    if args.cmd == "selfcheck":
        report = score(root)
        print_human(report)
        return 0 if report["pass"] else 1
    if args.cmd == "catalog":
        for token in sorted(skill_tokens(skills(root))):
            print(token)
        return 0
    if args.cmd == "bind":
        return cmd_bind(root, root / args.dest, args.dry_run)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
