# Third-Party Notices

VEMO_SKILLS is licensed under the MIT License (see [`LICENSE`](LICENSE)). It incorporates ideas,
checklists, and tooling from the third-party sources listed below. Each source is used in the **scope**
noted; its own license governs that borrowed material. This file discharges the attribution obligations
of the permissive and Creative-Commons sources in one auditable place.

| source | license | where used | scope of use |
|---|---|---|---|
| [standard-readme](https://github.com/RichardLitt/standard-readme) (RichardLitt) | MIT | `skills/orchestration/publishing-deliverables/references/readme-style.md` | entry-doc section-checklist idea, slimmed to the governance-repo case |
| [MADR](https://github.com/adr/madr) (adr/madr) | MIT | `skills/research/structuring-solution-docs` | per-architecture-decision block shape (D1–D6) |
| [markmap](https://github.com/markmap/markmap) (markmap-js) | MIT | `skills/orchestration/visualizing-governance` | interactive-overview rendering tooling (not text) |
| [tflite](https://pypi.org/project/tflite/) (TFLite flatbuffer schema, Python bindings) | Apache-2.0 | `skills/code/gating-tflite-op-envelopes/references/envelope_gate.py` | invoked library (not vendored) — the generated `tflite.Model` schema classes parse the flatbuffer for op codes + `min_runtime_version`; same convention as the markmap row |
| [zh-style-guide](https://github.com/yikeke/zh-style-guide) (yikeke) | MIT | `skills/governance/polishing-chinese-prose` | Chinese-prose checks (R14–R20 翻译腔), Vale-style |
| 余光中《中文的常态与变态》 (essay) | (idea cited as fact; not reproduced) | `skills/governance/polishing-chinese-prose` (R33 文牍腔) | one theoretical framing only — the R33–R39 rules themselves are original project-authored checklist text, not reproduced from the essay |
| Microsoft Style Guide — "Scannable content" | CC-BY-4.0 | `skills/orchestration/publishing-deliverables/references/technical-report-style.md` (R21–R28) | scannability thresholds |
| Google developer documentation style guidance | (dev-docs guidance) | `technical-report-style.md` (R26) | table-vs-list container rule |
| [arc42](https://github.com/arc42/arc42-template) (arc42-template) | **CC-BY-SA** | `skills/research/structuring-solution-docs/references/arc42-mapping.md` | section skeleton (S1–S12) transcribed as a checklist |
| Anthropic skill-authoring naming rules, via [datawhalechina/agent-skills-with-anthropic](https://github.com/datawhalechina/agent-skills-with-anthropic) (ch.6 §1.1–1.4, Chinese rendering of the Anthropic course) | (rules cited as facts; source repo declares no LICENSE) | `skills/governance/naming-skills` | the naming rule points (name ≤64 / charset / no edge hyphen / folder-match; description floor; gerund recommendation) — transcribed as an original validator checklist |

## arc42 (CC-BY-SA) — scope note

The arc42 borrowing in `arc42-mapping.md` uses arc42's **section names** (S1–S12 — a system/idea skeleton)
plus **original column text authored here** ("answers" + "pass check"). It is **not** a reproduction of
arc42's expressive prose, so the share-alike provision does not extend to VEMO_SKILLS' own work. The
attribution above (and the in-file header in `arc42-mapping.md`) satisfies the CC-BY-SA attribution
courtesy. VEMO_SKILLS' primary license (MIT) is unaffected.

## polishing-chinese-prose bureaucratese band (R33–R39) — scope note

The 文牍腔 band (R33–R39) in the `polishing-chinese-prose` skill is **original text authored here** as a practical
plain-language checklist. 余光中's essay《中文的常态与变态》is cited for **one theoretical framing only**; the concrete
rules, replacement examples, and read-aloud test are **not** from the essay. Two further Chinese-style guides were
reviewed for this band —
[richardchien/chinese-writing-style-guide](https://github.com/richardchien/chinese-writing-style-guide) (no LICENSE)
and [RightCapitalHQ/chinese-style-guide](https://github.com/RightCapitalHQ/chinese-style-guide) (MIT) — but they
cover mostly spacing/punctuation/terminology, **not bureaucratese**; **no expression from either was used**, so neither
is listed above (nothing borrowed = no attribution row, by design — we don't credit thin/unused sources). VEMO_SKILLS'
primary license (MIT) is unaffected.

## Skill-naming rules (source declares no LICENSE) — scope note

The `naming-skills` skill encodes the **skill-authoring naming constraints** (name ≤64 chars / lowercase
letters-digits-hyphens / no leading-trailing hyphen / folder-name match; description floor; gerund form). These
constraints originate in **Anthropic's published skill spec** and are **factual rule points, not copyrightable
expression**. The Datawhale course repo cited above is a **Chinese rendering** of that material and declares no
LICENSE; it is cited as the authoritative rendering, not reproduced. Every clause, machine-check, and example in
`naming-skills/SKILL.md` is **original text authored here**, so no copyrightable prose is copied. The **gerund
requirement** is a *recommendation* in the source that **this ecosystem upgraded to a hard rule** (see `skill_spec`
§9). VEMO_SKILLS' primary license (MIT) is unaffected.

## Vendored third-party skill

The `challenging-assumptions` skill is vendored with its own upstream license, kept self-scoped in its own
subdirectory: [`skills/research/challenging-assumptions/LICENSE`](skills/research/challenging-assumptions/LICENSE)
(MIT, Copyright (c) 2026 mattnowdev). The repository LICENSE does not absorb it; this notice points to it.
