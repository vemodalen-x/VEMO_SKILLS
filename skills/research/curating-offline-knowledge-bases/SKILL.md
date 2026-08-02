---
name: curating-offline-knowledge-bases
description: 'Build or audit a source-traceable offline knowledge base from websites, papers, PDFs, videos, repositories, and local documents. Use when consolidating a personal or team knowledge base, clustering notes into a prerequisite topology, making material searchable without embeddings, checking whether sources were actually learned, or preserving an offline learning library. Triggers include offline knowledge base, personal knowledge base, source provenance, learning topology, prerequisite graph, no-embedding RAG, consolidate notes, and completeness audit.'
---

# Curating Offline Knowledge Bases

Build a compact learning system that preserves source traceability without confusing discovery, indexing, reading,
and mastery. Keep original-source records separate from synthesized concepts and retrieval indexes.

## Inputs

Resolve at runtime:

- source scope and snapshot date;
- destination repository and its public/private boundary;
- allowed local artifacts, copyright constraints, and retention policy;
- intended users, learning goals, and required offline surfaces;
- whether lexical search is sufficient or semantic retrieval is genuinely needed.

## Workflow

### 1. Freeze the inventory

Create a source ledger before summarizing. Give every source a stable ID and record its canonical URL or local
reference, title, source type, author/provider, publication and retrieval dates, access status, license boundary,
content hash when available, and failure reason when blocked.

Separate canonical sources from caches, generated output, dependency trees, temporary clones, and duplicates. A
directory or playlist count is evidence of discovery only, not evidence that its contents were read.

### 2. Assign an honest completeness level

Use these levels per item, not one vague percentage for the whole library:

| level | evidence | allowed claim |
|---|---|---|
| A | full text/transcript read in sections; claims, evidence, limits, application, and recall prompts exist | semantic study completed |
| B | representative primary material and structure reviewed; experiments or all entries remain incomplete | executable map established |
| C | title, path, date, type, and source link only | discoverable/indexed |
| D | only public metadata or a partial extract is accessible | blocked/partial source recorded |
| E | requested source has no reliable record yet | not ingested |

Never promote C to A because an index is searchable. Never promote B to A because a study plan exists.

### 3. Ingest with source boundaries

- Prefer primary sources and pin repository sources to a commit or release.
- For PDFs, record extraction/OCR quality and page coverage; preserve page references.
- For media, use `transcribing-long-form-media` and preserve timestamps and keyframe references.
- Keep full transcripts, temporary OCR, and downloaded media in private staging unless redistribution is licensed.
- Store original links and metadata rather than mirroring third-party bodies by default.
- Treat dynamic facts, prices, APIs, laws, and product behavior as dated snapshots that require re-verification.

### 4. Write source notes and concept notes separately

Each source note should carry machine-readable metadata plus:

1. the source's actual claims;
2. supporting evidence or examples;
3. fact vs source opinion vs curator inference vs unknown;
4. applicability, counterexamples, and time/version limits;
5. links to existing concepts;
6. one concrete experiment, decision, or practice change;
7. active-recall questions.

Create a canonical concept note only when a source adds a new decision rule, failure mode, metric, or reusable
procedure. If it is merely another example, attach it to the existing concept instead of creating a synonym card.

### 5. Build a learning topology

Organize concepts as a prerequisite DAG in addition to topical folders:

- foundation: vocabulary, data model, and invariants;
- mechanism: how the system works;
- evaluation: how correctness and failure are measured;
- production: reliability, cost, security, and operations;
- application: projects and decisions that consume the concept.

Every node should name its prerequisites, evidence notes, next nodes, minimum learning artifact, and a completion
test. Keep contradictory evidence visible; do not merge it away for a cleaner graph.

### 6. Build lightweight retrieval first

Generate a deterministic lexical index over titles, summaries, tags, aliases, headings, source IDs, and local paths.
The retrieval contract is: search the compact index, select a source or concept note, then open that note and its
evidence. Add embeddings only after measured queries show a recall gap that metadata, aliases, and full-text search
cannot solve.

For an offline interface, prefer static HTML plus a localhost-only server. Store private learning state outside the
publishable repository and provide a no-server fallback for read-only browsing.

### 7. Validate storage, traceability, and learning

Run deterministic checks for:

- required entry files and unique source/note IDs;
- manifest path, byte-size, and SHA-256 parity;
- valid UTF-8 and local-link integrity;
- orphan notes, duplicate canonical sources, and missing provenance;
- forbidden secrets, raw private state, oversized media, and model weights;
- counts by completeness level and a random source-to-summary fidelity sample;
- retrieval by author, topic, key term, counterexample, and date/version.

## Output contract

Return a source ledger, source notes, canonical concept map, prerequisite topology, generated retrieval index,
integrity manifest, and a completeness report. State separately what is stored, traceable, semantically studied,
and practiced.

## Boundaries

- Do not bypass access controls, copy paid material, or publish complete third-party transcripts by default.
- Do not claim that a directory scan, title catalog, or generated summary proves learning.
- Do not delete original source records when consolidating concepts.
- Do not expose local paths, credentials, personal state, or private documents in a public knowledge artifact.
- This skill curates and audits knowledge; it does not decide the consumer project's retention or publication gate.
