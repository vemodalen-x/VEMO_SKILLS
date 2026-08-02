---
name: governing-project-fleets
description: 'Operate VEMO''s private local fleet control plane to discover, register, assess, and preview-first onboard Git projects across one PC. Use when the user asks to govern all PC projects, scan local repositories, choose solo/team/regulated profiles, generate fleet readiness reports, or roll out VEMO without overwriting project-owned files.'
---

# Project Fleet Governance

Use the installed VEMO CLI as the deterministic control surface. Keep this skill procedural; do not reimplement the
registry, profile scoring, managed-file hashing, or audit chain in prose or ad hoc scripts.

## Resolve the control plane

1. Try `vemo fleet profiles` from PATH.
2. If unavailable, locate the VEMO source at runtime from the current project, configured framework path, or user input,
   then use its current Python interpreter: `python <vemo-root>/bin/vemo fleet profiles`.
3. Never hardcode an account name, organization, home directory, repository URL, or project path.
4. Treat `VEMO_HOME` as private local state. Do not commit or publish its registry, config, or audit log.

## Classify the request

- **Inventory**: discover projects and report only. No registration or target writes.
- **Assess**: read the explicit registry and produce readiness findings. Prefer JSON when another tool consumes it.
- **Adopt**: register a selected project and optionally apply VEMO-managed files. This is a user-consent action.
- **Upgrade**: preview managed-file updates. Apply only after reviewing dirty/conflict findings and the requested
  profile's impact.

Discovery never means adoption. Do not register every discovered repository unless the user explicitly selects that
scope.

## Workflow

### 1. Install the local launcher

Preview first:

```text
vemo fleet install
```

Run `vemo fleet install --apply` only when the user asked to install the PC-wide control plane. Report the launcher
directory; do not mutate PATH silently.

### 2. Discover without mutation

Run `vemo fleet discover <roots...> --max-depth <n>`. Report found paths, existing registration state, and the exact
root/depth used. Large or sensitive roots require a narrow starting path rather than a whole-disk scan.

### 3. Recommend a profile

Use `vemo fleet profiles` as the source of truth:

- `solo`: individual tools, prototypes, and local utilities.
- `team`: shared products/services requiring hooks, authoritative CI, policy docs, and judge provenance.
- `regulated`: higher-assurance evidence needs, with ownership, dependency, receipt, telemetry, and release-provenance
  controls.

Explain the missing controls before proposing a higher profile. Readiness is not certification or legal compliance.

### 4. Register only selected projects

Run `vemo fleet register <path> --profile <profile>` for projects the user selected. Registration changes only the
private local registry and audit chain; it does not modify the target project.

### 5. Assess and prioritize

Run `vemo fleet status --json`. Sort remediation by:

1. required safety/authority gaps,
2. required lifecycle/evidence gaps,
3. recommended maturity improvements,
4. manual controls that cannot be verified locally.

Use `--strict` only when the caller needs a failing exit code for scheduling or policy automation.

### 6. Onboard preview-first

Run `vemo fleet onboard <path> --profile <profile>` and present create/update/conflict counts. Apply only after the user
has reviewed the plan and the target worktree is clean:

```text
vemo fleet onboard <path> --profile <profile> --apply
```

Stop on project-owned conflicts. Do not force overwrite. After apply, run the target project's
`vemo init --preset <stack>` to install local hooks, then commit through that project's normal task lifecycle.

When the user explicitly adopts the shared skill home, add `--skills-root <runtime-resolved-skill-home>` to the dry-run
and apply commands. Verify the plan writes only `.claude/skills/<name>/` working copies and does not include local
validation markers. Omit this option when the user asked for framework governance without shared-skill adoption.

### 7. Verify governance evidence

Run `vemo fleet status --strict` and `vemo fleet audit --verify`. Separate local findings from external controls such
as branch protection, reviewer independence, identity policy, and signed build provenance; verify those through their
authoritative source platform when the user requests it.

## Report contract

Return:

- inventory scope and project count,
- selected profile per registered project,
- required gaps and concrete remediation,
- dry-run/apply status and any conflicts,
- local audit-chain result,
- external/manual controls still unverified.

## Boundaries

- Never auto-register discovery results, auto-apply onboarding, auto-enable unattended mode, or change remote branch
  settings.
- Never claim that a readiness score proves security, compliance, or absence of vulnerabilities.
- Never expose private project paths in outward communications without explicit user approval.
- Never bypass dirty-worktree, managed-file conflict, scope, acceptance, judge, or CI gates.
