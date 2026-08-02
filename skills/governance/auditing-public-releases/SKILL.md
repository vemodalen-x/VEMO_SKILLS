---
name: auditing-public-releases
description: 'Audit source, Git history, build inputs, archives, tags, CI permissions, licenses, and published assets before or after a public software release. Use when preparing a GitHub release, sanitizing a public repository, checking a release ZIP/wheel/installer, preventing private paths or media leaks, verifying checksums/manifests, or confirming that a tag and remote artifact match the reviewed commit. Triggers include public release audit, privacy scan, secret scan, release ZIP, manifest, checksum, tag verification, Git history scan, supply chain, and downloaded artifact re-scan.'
---

# Auditing Public Releases

Audit the exact surfaces that will become public and fail closed on privacy, integrity, provenance, licensing, and
authority gaps. A passing source test does not automatically validate the archive or remote release.

## Scope the release

Resolve at runtime:

- reviewed source revision, base/default branch, release branch, and proposed tag;
- staged/tracked/untracked files that can enter the build;
- produced archives, executables, wheels/installers, docs, checksums, and attestations;
- CI workflows and permissions that can publish;
- exact intended remote release asset list;
- project-specific allowlists for public media, generated assets, and optional models.

Use allowlists for sensitive classes rather than hoping a blocklist names every private filename.

## Workflow

### 1. Audit source and build inputs

Scan every file that the build can see, including allowed untracked inputs. Reject credentials/private keys, concrete
local user/workspace paths, environment files, browser/session state, user databases, logs, screenshots/recordings,
raw private media, model checkpoints not approved for distribution, caches, dependency trees, source maps, test
artifacts, and temporary validation output.

Split sensitive token literals inside the scanner's own fixtures so the scanner can inspect itself. Test positive and
negative cases, including generic documentation paths that should be allowed and concrete user paths that must fail.

### 2. Audit reachable Git history when required

Scan unique blobs reachable from the release commit for secrets and private path/content markers. A current-tree pass
does not prove history is clean. If a real secret ever entered history, revoke/rotate it; history rewriting alone does
not make the credential safe.

Record whether history was scanned and its exact revision scope. Do not silently skip large/binary blobs without an
explicit policy.

### 3. Verify metadata, dependencies, and licenses

Check version agreement across the source of truth, runtime/API, executable metadata, docs, archive name, and release
notes. Ensure direct and redistributed dependencies are locked, expected, and covered by license/third-party notices.
Review model/data/content licenses separately from code licenses.

Require security/privacy documentation appropriate to the product and disclose unsigned binaries, telemetry,
network use, retention, and unsupported platforms accurately.

### 4. Audit the built artifact

Enumerate archive member names before extraction and reject absolute paths, parent traversal, multiple unexpected
roots, forbidden path segments, and unapproved media/executables. Scan text payloads inside the archive for the same
privacy/secret patterns used on source.

Require a manifest listing every shipped file except the manifest itself. Recompute each size and SHA-256 and assert
exact set equality. Unpack to a fresh directory, re-run the manifest check, and execute the product's clean-path smoke
test. Record the final archive digest.

### 5. Audit CI and publication authority

Pin third-party actions/tools, use locked dependencies, separate read-only build/test from the minimum-permission
publish job, and pass only reviewed artifacts between them. Verify the proposed tag points to the reviewed commit and,
where policy requires, that the commit is the current default-branch head.

Publishing is an explicit human/lead action. This skill reports readiness; it does not create a tag, merge, upload, or
announce unless a separate authorized workflow requests that action.

### 6. Verify the remote release

After publication, query the authoritative remote. Confirm tag/commit identity, workflow success, exact asset names and
count, attestation/signature status, and advertised checksums. Download every public artifact, recompute its digest,
run the same archive/privacy scanner, and compare it with the local reviewed artifact.

## Report contract

Return a pass/fail table for source, history, metadata/version, dependencies/licenses, archive structure, manifest and
checksums, clean-unpack smoke, CI permissions, tag identity, and downloaded remote artifact. Include exact revision,
commands, exit codes, asset digest, unresolved findings, and whether publication itself was performed.

## Boundaries

- A privacy/release audit is not a vulnerability assessment or legal certification.
- Do not report a pass when a required surface was skipped, unavailable, or simulated.
- Do not weaken a scanner solely to accommodate a failing package; narrow any exception to a documented vendor path
  and add regression fixtures.
- Do not expose discovered secrets or private content in logs; report type and location with redaction.
- Do not publish, merge, tag, or announce without the applicable authority and consent.
