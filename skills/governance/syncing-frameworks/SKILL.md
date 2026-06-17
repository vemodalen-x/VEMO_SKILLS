---
name: syncing-frameworks
category: governance
description: Check whether any governance framework pinned as a submodule has advanced upstream (new release/commit), report the diff, and apply pin bumps only on a user version gate. Use at session start (continuity check) or when the user asks to check for framework updates. Submodule model — NOT file-copy.
---

# Framework Sync

Check the upstream of every governance framework this project pins as a **git submodule**, report which have
advanced, and (on user approval) bump the pins. This is the **submodule-model** counterpart of a single-upstream
template-copy sync: there is no file list and no file-copy — each framework is a real clone with its own remote, so a
"sync" is `git fetch` + tag/commit comparison + a version-gated pin bump.

## Model (read first)
- **Targets are resolved at runtime from the instance**, never hardcoded. Read `project_profile.yaml`:
  `governance_frameworks[].submodule`, `shared_skills[].submodule`, `starter[].submodule` — every pinned submodule
  is a sync target.
- **Upstream is read from the live remote**, never from the `source:` field: `git -C <submodule> remote get-url origin`.
  (The `source:` pin may carry a stale org; the remote is ground truth. **No org/account is hardcoded** — the skill
  follows whatever remote each submodule actually points at, so it is correct across org migrations without edits.
  Zero-hardcode, identity dimension — skill_spec §9.)
- **Read-only contributors are fully supported.** The report path (fetch + tag/commit compare) needs **no write
  access** — anyone who can read the repo can run a sync report (`git fetch` on a public/readable remote, or
  `git ls-remote` with no auth). Write access matters only for the apply step, which is the consumer's own version
  gate, not an upstream permission.
- **Never auto-update.** A pin bump moves a project onto new governance rules — that is the **consumer's version
  gate**. This skill *reports*; it applies only on explicit confirmation. (Same posture as the single-upstream
  governance-sync reference: notify, don't auto-update.)

## Prerequisites — GitHub CLI (`gh`)
- **Verify**: `gh auth status`.
- **Install**: Windows `winget install GitHub.cli` · Linux `sudo apt install gh` / `brew install gh` · macOS `brew install gh`.
- **Post-install**: `gh auth login`.
- `gh` is used for ahead/behind queries against remotes the local clone may not have fetched; if absent, the skill can
  still fall back to `git ls-remote` (no auth needed for public read), but `gh` is preferred for changelog fetch.

### Pre-Check (Step 0, mandatory)
1. Detect `gh` on PATH. Not found → show the install command for the detected OS, ask the user to install, **stop**.
2. `gh auth status`. Not authenticated → show `gh auth login`, ask, **stop**. (Read-only ops can proceed via
   `git ls-remote`; only the changelog-fetch convenience needs auth.)
3. Read `project_profile.yaml`. If no submodule-pinned frameworks exist → "No submodule-pinned frameworks to sync" → **end**.

## Triggers
- **Automatic**: session-start continuity check (`chat_spec` §4 step 6), if framework submodules are configured —
  **report only**, no auto-update. The machine reminder (SessionStart hook/cron) is wired locally by the instance's
  project-init procedure (two-layer pattern).
- **Manual / keyword**: "检查框架更新" / "check framework updates" / "同步框架" / "sync frameworks" / "框架版本".

## Sync Flow
### Step 1 — Enumerate targets
Build the target list from `project_profile.yaml` (all three submodule-bearing sections). For each, record: repo id,
local submodule path, pinned `source:` (id + ref), and the **live remote** (`git -C <path> remote get-url origin`).

### Step 2 — Read local pinned state
For each target: the pinned ref (the `@vX.Y.Z` in `source:`) and the actual checked-out commit
(`git -C <path> rev-parse HEAD`) and its tag (`git -C <path> describe --tags --exact-match 2>/dev/null`).

### Step 3 — Read upstream state
For each target, against its live remote:
- `git -C <path> fetch --tags origin` (or `git ls-remote --tags <remote>` if fetch is undesirable).
- Latest release tag: highest semver tag on the default branch.
- Latest commit on the default branch: `git -C <path> rev-parse origin/<default-branch>`.

### Step 4 — Compare & classify
Per target: `up-to-date` (pinned tag == latest upstream tag) / `behind` (newer tag or commits exist upstream) /
`ahead` (local commits not upstream — e.g. an un-contributed local change; suggest `contributing-framework-changes`) /
`detached/dirty` (local edits or detached HEAD — report, do not bump).

### Step 5 — Report (do not apply)
Present a table — **no changes made yet**:
```
repo          pinned      upstream-latest   status     behind-by
framework-a   v0.11.0     v0.11.0           up-to-date  —
framework-b   v0.2.0      v0.3.0            behind      1 tag / 4 commits
...
```
For `behind` targets, fetch and summarize the upstream CHANGELOG entries between pinned and latest (via `gh api` or the
fetched CHANGELOG.md). End with: "Bump pins for the behind frameworks? This is a version gate. (Y/N)".

### Step 6 — Apply (only on explicit user confirmation — version gate)
For each confirmed target:
- `git -C <path> fetch origin` then check out the chosen release tag (`git -C <path> checkout vX.Y.Z`).
- Stage the submodule gitlink in the business repo (the gitlink now points at the new tag commit).
- Update `project_profile.yaml` `source:` ref to the new `@vX.Y.Z` (keep the org/account as-is — the org is part of
  the canonical remote, not something this skill rewrites).
- Keep **gitlink == tag == `source:` pin** consistent (the three-way consistency rule).

### Step 7 — Commit
Commit message: `chore(governance): bump <repo> pin -> vX.Y.Z (syncing-frameworks)`. If the user declines the commit,
leave the gitlink + profile change staged. Mirror the transition into `flow_log.md` (a pin bump is a workflow event).

## Never touched
- Instance files (`instance/*`), runtime ledgers (`flow_log.md` / `chat_index.md` / `task/**`) — except the flow_log
  row recording an applied bump.
- The `source:` **org/account** — the canonical remote owns that; this skill follows the live remote, it does not
  rewrite org migrations.
- Any submodule in `detached/dirty` state — reported, never silently bumped.

## Notes
- **Difference from the single-upstream reference**: no `governance_template_boundary` file list, no per-file diff, no
  file-copy — the unit of sync is the **whole pinned submodule at a tag**, not individual template-owned files.
- Reads the live remote, so it is correct across org migrations (e.g. a project whose frameworks are split across two
  organizations) without edits.
