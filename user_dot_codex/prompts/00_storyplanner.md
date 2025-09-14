# 00_storyplanner — StoryPlanner

## Goal
Seed or augment project specs from feature needs; bootstrap `.codex/*`.

## Preflight
- Ensure `.codex/{spec,tasks,trace,runs,contracts}` exist; create if missing.
- Do NOT copy schemas into project. Render outputs using schema paths from AGENTS.md.

## Inputs
- Interactive menu + Q&A, or a feature file path (PRD/bullets).
- User/Project AGENTS.md for conventions and schema paths.

## Selection
Resolve target using Selection precedence (NEXT → eligible set → INFO).

## Interactive Flow (first turn)
On start, present a minimal, zero-parameter menu and proceed accordingly:
1) New story — add one or more stories from human input or PRD path.
2) Update existing story — modify specific STORY-IDs; recompute fingerprints.
3) Merge stories — move sections from sources to a target; mark sources done (body note: "superseded by <TARGET>").
4) Bootstrap from scratch — if specs missing/empty, scaffold `01.requirements.md` and `02.design.md` from schemas; optionally seed draft stories from high-level product goals.
5) Scan codebase and propose stories — non-destructive heuristic scan of `src/**` and `tests/**`; write proposals to `.codex/runs/<ts>/story_backfill_proposals.md` and/or draft stories (status=draft) for human review.
6) Cancel — exit with `INFO: user cancelled`.

If no selection is provided during an interactive session, default to (1) New story.

## Modes & Behavior
- New story
  - Create vertical user stories in `.codex/spec/01.requirements.md` with front-matter:
    - `id: STORY-###` (incremental), `status: ready`, `priority: P2`, `depends_on: []`, `component_tags: []`, `tasks_generated: false`, optional `kind: feature|refactor|hotfix`.
  - Sections: Motivation, Acceptance (testable bullets), NFR, Out of Scope (optional).
  - Compute and set `story_fingerprint`.
  - Dedupe by normalized title to avoid duplicates.
- Update story
  - Require explicit `STORY-IDs` and updated fields/sections.
  - Edit content; recompute `story_fingerprint` for each updated story.
  - Do not modify unrelated stories.
- Merge stories
  - Require a target `STORY-ID` and one or more source `STORY-IDs`.
  - Move Acceptance/NFR/Motivation bullets as instructed; preserve provenance notes in body.
  - Mark source stories `status: done` and add a body line: "superseded by <TARGET>" (do not add new front-matter keys).
  - Recompute fingerprints on affected stories.
- Bootstrap from scratch
  - If `.codex/spec` is missing or empty, render `01.requirements.md` and `02.design.md` from schemas.
  - Optionally seed a minimal set of draft stories from high-level goals. Default `status: draft` unless Acceptance is sufficiently concrete, then `ready`.
- Scan codebase and propose stories (non-destructive)
  - Heuristics: endpoints/CLIs, modules without tests, TODO/FIXME clusters, public interfaces.
  - Output proposals to `.codex/runs/<ts>/story_backfill_proposals.md` and/or draft story blocks; do not set to `ready` automatically.

## Steps
1) Execute the selected mode. For story writes, append/update in `.codex/spec/01.requirements.md` with dedupe and `story_fingerprint` computed.
2) Ensure `.codex/spec/02.design.md` exists; if missing, render from design schema with `status: draft`.
3) Write run log `.codex/runs/<ts>/storyplanner.md` summarizing actions and decisions.

## Safety & Guardrails
- Never edit `.codex/spec/03.tasks.md` directly (derived by planners).
- Keep front-matter keys within the Story schema; use body notes for provenance (e.g., superseded-by) rather than new keys.
- For scan/bootstrap modes, default to `status: draft` unless Acceptance is concrete.
- Idempotent by content: reruns should not duplicate stories or proposals.

## Output
- `.codex/spec/01.requirements.md` (stories updated/appended as applicable)
- `.codex/spec/02.design.md` (ensured; created if missing)
- `.codex/runs/<ts>/story_backfill_proposals.md` (scan mode only)
- Run log only

## NEXT
- If any story is `ready`: `NEXT: run ArchitectPlanner (01_architectplanner.md)`
- Else: `INFO: no actionable features`
