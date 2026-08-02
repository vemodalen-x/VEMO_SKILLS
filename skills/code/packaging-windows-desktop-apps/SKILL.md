---
name: packaging-windows-desktop-apps
description: 'Package a Windows desktop application into a reproducible, privacy-sanitized, integrity-checked portable archive or installer with locked dependencies, version metadata, licenses, manifests, clean-machine smoke tests, and release evidence. Use when building a Windows EXE, PyInstaller bundle, desktop launcher, offline AI tool, portable ZIP, installer, or GitHub release artifact. Triggers include package Windows app, build exe, PyInstaller, portable ZIP, desktop shortcut, installer, release manifest, clean-machine smoke test, and Windows release.'
---

# Packaging Windows Desktop Apps

Produce a Windows artifact that runs without the developer source tree, virtual environment, current working
directory, or private machine state. This skill owns Windows build and clean-machine behavior. Compose with
`auditing-public-releases` for source/history/privacy/license/manifest/CI/tag/remote-release authority.

## Inputs

Resolve the version source of truth, supported Windows versions and architectures, runtime/GPU requirements, packaging
tool, executable entry points, optional components/models, portable versus installer mode, signing policy, and required
public documentation.

If a support floor, architecture, installer mode, signing policy, or runtime requirement is missing, return it as an
unresolved package decision. Do not silently select a Windows version, RAM floor, architecture, or distribution mode.

## Workflow

### 1. Freeze a clean build input

Build the reviewed revision in a clean worktree or isolated checkout. Lock release dependencies by version and hash
where supported. Record interpreter/compiler, packager, OS image, architecture, and source revision.

Keep source caches, virtual environments, user databases, logs, downloads, recordings, local settings, tests, and
build leftovers outside package inputs.

### 2. Define the Windows package contract

Use one top-level directory containing only required executables/runtime files, relative-path launchers, approved
assets, licenses/notices, concise usage/privacy/security/troubleshooting docs, and a machine-readable file manifest.

Separate optional models or accelerators when licensing, size, or hardware support differs. Provide a runtime doctor
that reports actionable errors for missing GPU runtime, model, codec, port, or external tool dependencies.

### 3. Build deterministically

Create an isolated environment, install locked dependencies, and invoke PyInstaller or the chosen packager through a
versioned explicit specification. Disable development servers and source maps. Normalize archive paths and timestamps
where practical.

Embed the same product/file version and approved icon metadata in every shipped PE executable, including helper and
bridge processes. Verify hidden imports, dynamic assets, DLL search behavior, and multiprocessing entry points; a zero
packager exit alone is not acceptance.

### 4. Validate Windows-specific artifact behavior

Before generic release audit, inspect executable architecture, PE versions, optional signature state, DLL/runtime
dependencies, archive root, and launcher path resolution. Never claim signing when unsigned; document SmartScreen and
publisher limitations plainly.

### 5. Test from hostile-clean paths

Extract or install into fresh paths that include spaces, non-ASCII characters, and a non-admin user context. Verify:

- launch works from Explorer and a terminal outside the source directory;
- helper processes inherit correct relative paths and terminate cleanly;
- local services bind only to documented interfaces and ports and expose health;
- a minimal fixture completes the main flow and saves output;
- missing optional GPU/model/tool dependencies produce useful errors and promised fallbacks;
- portable removal or uninstall leaves user data only in documented locations.

Repeat on each supported architecture/Windows line or explicitly narrow support. Recompute the final archive digest
after testing.

### 6. Hand off to release audit

Run `auditing-public-releases` on exact build inputs and the final archive. That skill owns privacy and history scans,
license/manifest parity, CI permission review, tag identity, checksums, and downloaded remote re-scan. Packaging passing
does not authorize publication.

## Output Contract

Return source revision, dependency/build-environment evidence, packaging specification and log, PE metadata/signature
state, package file list and manifest, archive digest, hostile-path smoke results, supported platform matrix, runtime
doctor output, release-audit result, and known limitations.

## Boundaries

- Do not include credentials, local paths, user state, private media, or unlicensed weights.
- Do not hide runtime and signing requirements in an appendix.
- Do not tag, upload, or announce because packaging passed; publication is separately authorized.
