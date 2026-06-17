---
name: contributing-framework-changes
category: governance
description: Contribute a local improvement to a governance framework back to that framework's repo via a pull request. Use when a local framework or skill-home change should be proposed upstream. Works for any contributor — write-access holders push a branch to the repo directly; contributors without write access fork and open a cross-repo PR. The path is chosen at runtime by probing the actual permission; no identity, org, or account is hardcoded.
---

# Framework Contribute

Open a pull request that carries a local framework improvement back to that framework's repo. Each governance
framework is pinned as a **git submodule** — a real clone with its own remote — so the change already lives in a
working tree that can branch and PR directly. **There is no temp-clone and no file-copy** (that machinery only exists
in the single-upstream template-copy model).

This skill is **identity-decoupled**: it works for *any* contributor against *any* framework repo. The maintainer of
a repo and an outside contributor to it are **equal first-class cases** — the skill probes the actual permission at
runtime and takes the matching path. Nothing about who owns which repo is written into this file.

## Model (read first)
- The change is already in the submodule's working tree (the user edited the framework in place). Contribution =
  branch + commit + push + PR — on whichever remote the contributor can push to.
- **Everything identity-bearing is resolved at runtime, never hardcoded** (skill_spec §9, identity dimension):
  - target repo + upstream → `git -C <path> remote get-url origin` (parse `<owner>/<repo>` from it).
  - the contributor's identity → `gh api user --jq .login` (whoever is logged in).
  - **write access → probed live**: `gh api repos/<owner>/<repo> --jq .permissions.push` (true/false decides the path).
  No org, account, or repo name is baked in. The skill is correct across org migrations and for external contributors
  without edits.

## Prerequisites — GitHub CLI (`gh`)
- **Verify**: `gh auth status`.
- **Install**: Windows `winget install GitHub.cli` · Linux `sudo apt install gh` / `brew install gh` · macOS `brew install gh`.
- **Post-install**: `gh auth login`.

### Pre-Check (Step 0, mandatory)
1. Detect `gh`. Not found → show the install command for the detected OS, ask, **stop**.
2. `gh auth status`. Not authenticated → `gh auth login`, ask, **stop**.
3. Identify the target submodule (user names the framework, or infer from the dirty submodule). Resolve its path,
   parse `<owner>/<repo>` from `git remote get-url origin`, read the logged-in user (`gh api user`).
4. **Probe permission** (this selects the path, not configuration):
   `gh api repos/<owner>/<repo> --jq .permissions.push`.
   - `true` → **Path A · direct branch** (push a contrib branch to the repo, in-repo PR).
   - `false` → **Path B · fork** (fork, push to the fork, cross-repo PR).
   Both paths produce the same artifact — a PR against the framework's default branch. They are peers; neither is a
   downgrade.

## Trigger (manual only)
User invokes when they want a local framework change upstreamed.
- **Keywords**: "贡献框架" / "contribute framework" / "推框架改动" / "framework PR" / "回贡献上游".

## Shared steps (both paths)
### Step 1 — Identify the change
- In the target submodule: `git -C <path> status` + `git -C <path> diff` against `origin/<default-branch>`.
- If the submodule is at a **detached HEAD on the pinned tag** (the normal pinned state), the working-tree edits sit on
  top of that tag. **Establish a proper branch base before committing** — never commit on a detached HEAD:
  - `git -C <path> fetch origin`
  - `git -C <path> checkout -b contrib/<task-id>-<short-summary> origin/<default-branch>` (base on upstream head, then
    re-apply the edits) — or branch from current HEAD and rebase onto `origin/<default-branch>` if the exact tree must
    be preserved.
- If there are no changes vs upstream → "No framework changes to contribute" → **end**.

### Step 2 — Present & confirm
- Show the diff summary (files + hunks) and the resolved target (`<owner>/<repo>:<default-branch>`) and which path the
  permission probe selected. Ask the user to confirm scope.

### Step 3 — CHANGELOG + VERSION (framework release discipline)
- Draft a `## [Unreleased]` CHANGELOG entry (or suggest the next semver per the framework's
  `Framework_Release.procedure` — patch/minor/major). Show for edit. The maintainer may finalize the version at merge.

### Step 4 — Commit (both paths)
- On the `contrib/<task-id>-<short-summary>` branch. Commit with the contributor's own identity
  (`git config user.name` / `user.email`):
  ```
  <short summary>

  Contributed from <project_id>. Based on <pinned-tag/commit>.

  Co-Authored-By: <name> <email>
  ```

### README check (mandatory, before opening the PR)
- If the change affects a capability the framework's `README.md` describes (new rule, skill, workflow, trigger),
  update both `README.md` + `README_zh.md` in the same contrib branch (the framework's R29+ entry-doc freshness
  obligation in `readme-style.md`, incl. R30 README-freshness).

## Path A · contributor with push access
A5. **Push the branch to the repo's own origin**: `git -C <path> push origin contrib/<task-id>-<short-summary>`.
A6. **Open the PR in-repo**: `gh pr create --repo <owner>/<repo> --base <default-branch>
    --head contrib/<task-id>-<short-summary>`.
A7. **Restore the pinned state**: after the PR is open, return the submodule to its pinned tag so the consuming
    project's gitlink stays consistent — `git -C <path> checkout <pinned-tag>` (the branch remains on origin for the
    PR). Do not advance the consuming gitlink to the contrib branch (the pin only moves later via `syncing-frameworks` on
    the consumer's version gate, after merge + release).

## Path B · contributor without push access (fork)
B5. **Fork**: `gh repo fork <owner>/<repo> --clone=false`; detect the fork owner (`gh api user --jq .login`).
B6. **Add the fork as a remote and push**: `git -C <path> remote add fork <fork-url>` (temporary), then
    `git -C <path> push fork contrib/<task-id>-<short-summary>`.
B7. **Open the cross-repo PR**: `gh pr create --repo <owner>/<repo> --base <default-branch>
    --head <fork-owner>:contrib/<task-id>-<short-summary>`.
B8. **Cleanup**: remove the temporary `fork` remote (`git -C <path> remote remove fork`) and restore the pinned state
    as in A7.

## Step 7 (both paths) — Output
- Print the PR URL. Note: "Maintainer reviews + merges on GitHub; a consumer's pin moves later via `syncing-frameworks` on
  its own version gate." Mirror the event into the consuming project's `flow_log.md`.

## PR body (both paths)
```
## Source
- Project: <project_id>
- Based on: <pinned-tag/commit>

## Changes
<file list with one-line summaries>

## Changelog Entry
<drafted changelog text>

## Contributor
<name> (<email>)
```

## Important notes
- Always a **PR**, never a direct merge; the PR targets the framework's own default branch.
- Only the **framework's own** files are contributed — instance files and consuming-project runtime ledgers are never
  pushed upstream.
- Contributor `Co-Authored-By` is mandatory.
- **No identity is hardcoded**: owner/repo come from the remote, the contributor from `gh api user`, the path from a
  live permission probe. The maintainer path (A) and the external-contributor path (B) are **equal first-class cases**.
- **Difference from the single-upstream reference** (Wildpanda governance-contribute): no temp-clone, no file-copy —
  the change is already in the submodule clone; we branch + PR it in place. The fork path is preserved as a peer for
  contributors without write access, not as a fallback.
