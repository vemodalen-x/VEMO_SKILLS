# Security and release hygiene

VEMO_SKILLS is a skill-source repository, not a runtime sandbox. Its security boundary is about public-release hygiene
and identity decoupling.

## Defended risks
| Risk | Control |
|---|---|
| Project values leak into generic skill bodies | `vemo-skills selfcheck` scans for local paths, private org/account markers, and credential-like tokens |
| Activation or README catalog drifts from `skills/**` | three-way index/tree/catalog parity across both READMEs |
| Broken reference modules after category flattening | reference integrity + regen binding checks |
| "Release-ready" claimed without evidence | executable eval writes `eval/out/report.json`; release threshold is `9.5/10` |

## Limits
- The checker is a release hygiene tool, not proof that a downstream agent used a skill correctly.
- Consumers still own their own acceptance gates, ledgers, secrets handling, and runtime permissions.
- Report suspected leaks with the file path, matching line, and `python3 bin/vemo-skills selfcheck` output.
