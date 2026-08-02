---
name: transcribing-long-form-media
description: 'Turn authorized long-form video or audio into timestamped, source-traceable learning material with caption-first extraction, local ASR fallback, keyframe/OCR verification, checkpoints, and quality gates. Use when learning from a lecture, playlist, podcast, interview, or multi-hour recording; recovering text when captions are missing; or preparing a transcript-derived knowledge note. Triggers include transcribe video, extract audio, no subtitles, ASR, Whisper, keyframes, OCR slides, podcast notes, and long video learning.'
---

# Transcribing Long-Form Media

Treat media as an auditable evidence source, not as a blob to summarize from memory. Prefer official text, retain
timestamps, and use visual evidence only where it changes or verifies the interpretation.

## Preconditions

Confirm that the user owns the media or is authorized to download/process it. Record the canonical source, creator,
event date, upload date, duration, item/playlist identity, language, chapter data, and access boundary. Do not bypass
DRM, authentication, paywalls, or platform controls.

## Workflow

### 1. Resolve the best evidence source

Check, in order:

1. creator-provided transcript or human captions;
2. official automatic captions;
3. captions on an authorized mirror, verified against the canonical source;
4. local ASR from an authorized audio track.

If a repost lacks captions, re-check the official source before running ASR. Record whether text is human, automatic,
translated, or locally generated. Never blend them without preserving lineage.

### 2. Acquire the minimum useful media

Download the smallest adequate audio stream for transcription and, only when visual verification is needed, a low-
resolution video stream. Use resumable/chunked acquisition for long assets. Record the media ID, duration, codec,
byte size, acquisition command/tool version, and content hash. Keep raw media in private staging.

### 3. Transcribe with checkpoints

- Preserve segment start/end times and the detected/declared language.
- Split long media on silence or bounded windows with overlap; reconcile boundary duplicates.
- Persist completed segments so an interrupted run resumes instead of restarting.
- Record ASR model, backend, precision, device, decoding settings, and software versions.
- Maintain a second supported backend or a smaller fallback profile; a single runtime failure must not destroy the
  workflow.
- Show ETA only after measuring real progress for a meaningful interval; do not invent speed from old checkpoints.

Speaker diarization is optional. When speakers affect meaning, keep stable anonymous speaker IDs and mark overlaps or
uncertain turns rather than assigning identities by guesswork.

### 4. Validate text before summarizing

Sample the beginning, middle, end, transitions, low-confidence spans, and every conclusion-driving segment against
the audio. Explicitly verify names, model/paper titles, numbers, units, negations, formulas, and quoted claims.

Use independent references or human ground truth for accuracy measurement. A generated transcript cannot validate
itself, and agreement between two models is a review signal rather than proof. Keep unresolved spans marked with
timestamps and confidence notes.

### 5. Extract visual evidence selectively

First create coverage frames at a coarse interval; then add scene-change frames near high-information transcript
segments. Keep frames for formulas, charts, architecture diagrams, code states, inputs/outputs, or slides whose visual
content is not represented in speech.

OCR proposes text only. Verify small type, equations, tables, and code against the original frame. For code, prefer the
official repository as the authoritative source and use the frame only to bind the talk to a version/state.

### 6. Build a continuous timeline and learning note

Partition the whole duration into contiguous chapters. For each chapter record claim, evidence type, example,
boundary, confidence, source timestamps, visual references, and implications. Distinguish speaker claims, externally
verified facts, curator inference, and unknowns.

Send the final source note through `curating-offline-knowledge-bases`: deduplicate against existing concepts, retain
the source ledger, add prerequisites and active-recall prompts, then rebuild and test retrieval.

## Acceptance gates

- The item or playlist inventory has stable IDs, count, date, and explicit failures.
- The timeline covers start to finish without silent gaps; Q&A and appendices are not collapsed into one sentence.
- Caption/ASR lineage, model/backend, media hash, and keyframe method are recorded.
- Conclusion-driving names, numbers, formulas, and visual claims were checked.
- Low-confidence spans remain visible and are not promoted to facts.
- The published knowledge layer contains original synthesis, not a redistributed full transcript.
- Search finds the note by creator, topic, named entity, and method.

## Output contract

Return a source ledger entry, private timestamped transcript artifact, coverage report, keyframe map, chapter timeline,
structured learning note, unresolved-span list, and the commands/config needed to reproduce the extraction.

## Boundaries

- Do not claim continuous human-like viewing; report which text, audio, and frames were actually inspected.
- Do not publish raw personal recordings, complete copyrighted transcripts, or biometric voice artifacts without
  authorization.
- Do not claim certified transcription/translation accuracy without an independent reference benchmark.
- This skill processes media evidence; distribution, licensing, and final publication remain separate decisions.
