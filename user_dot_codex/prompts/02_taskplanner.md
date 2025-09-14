# 02_taskplanner — TaskPlanner

## Goal
Turn eligible stories into 1–3 small tasks each; tests-first.

## Inputs
- .codex/spec/01.requirements.md
- .codex/spec/02.design.md (must be status=ready)
- Existing .codex/tasks/*.md and .codex/spec/03.tasks.md
- Schema paths from AGENTS.md

## Selection
Resolve target using Selection precedence (NEXT → eligible set → INFO).

## Interactive Flow (first turn)
Offer a small menu; default to (1) if no selection is given:
1) Plan tasks for eligible stories — create tasks where `tasks_generated=false` or fingerprints drift.
2) Regenerate tasks for specific stories — force supersede then recreate tasks for given STORY-IDs.
3) Supersede stale tasks only — mark stale tasks superseded without creating new ones.
4) Rebuild derived list only — refresh `.codex/spec/03.tasks.md` from current tasks.
5) Cancel — exit with `INFO: user cancelled`.

## Modes & Behavior
- Plan tasks for eligible stories (default)
  - For each selected story, create 1–3 focused tasks with `status: ready`, inheriting story `priority` and mapping to a single `component` where possible.
  - Embed `story_fingerprint` and `design_fingerprint` into each task; set `story.tasks_generated=true` and `story.status=planned` if newly planned.
- Regenerate tasks for specific stories
  - Identify existing tasks for those stories; mark `ready|needs_update` ones as `superseded` and set `superseded_by` to the new tasks.
  - Recreate tasks fresh from current specs; maintain small, testable scope.
- Supersede stale tasks only
  - Detect fingerprint drift and set affected tasks to `needs_update` or `superseded` per policy; do not create new tasks.
- Rebuild derived list only
  - Leave tasks untouched; render `.codex/spec/03.tasks.md` from `.codex/tasks/*.md`.

## Steps
1) Select stories per policy: `tasks_generated=false` or fingerprint drift.
   - Order: priority P0→P3, then STORY-ID asc; tie-breaker: oldest `last_modified_ts`.
2) Execute chosen mode for each selected story, keeping 1–3 tasks max per story and ensuring each task is independently testable.
   - For hotfix stories (`kind: hotfix`), prefer a single, focused task (often P0).
3) Render `.codex/spec/03.tasks.md` from tasks_list_view schema (derived from files).
4) Log `.codex/runs/<ts>/taskplanner.md` with created/superseded tasks and any drift rationale.

## Safety & Guardrails
- Edit only `.codex/tasks/**` and derived `.codex/spec/03.tasks.md`; do not touch `src/**` or `tests/**`.
- Do not hand-edit `03.tasks.md`; always regenerate from task files.
- Maintain idempotency: reruns should not duplicate tasks; supersedes must link via `superseded_by`.
- Refuse to generate tasks if `design.status != ready`.

## Output
- New/updated `.codex/tasks/*.md`
- Updated specs and derived list
- run log

## NEXT
- If any task is ready: NEXT: run Builder (03_builder.md)
- Else: INFO: no ready tasks
