# 02_taskplanner — TaskPlanner

## Goal
Turn eligible stories into 1–3 small tasks each; tests-first.

## Inputs
- .codex/spec/01.requirements.md
- .codex/spec/02.design.md (must be status=ready)
- Existing .codex/tasks/*.md and .codex/spec/03.tasks.md
- Schema paths from AGENTS.md

## Steps
1) Select stories with tasks_generated=false or with stale tasks by fingerprint.
2) For the selected story:
   - Supersede stale `ready/needs_update` tasks (link superseded_by).
   - Render `.codex/tasks/TASK-###.md` from task schema; set status=ready; inherit priority; set story/design fingerprints.
   - Set story.tasks_generated=true and, if newly planned, story.status=planned.
3) Render `.codex/spec/03.tasks.md` from tasks_list_view schema (derived from files).
4) Log `.codex/runs/<ts>/taskplanner.md`.

## Output
- New/updated `.codex/tasks/*.md`
- Updated specs and derived list
- run log

## NEXT
- If any task is ready: NEXT: run Builder (03_builder.md)
- Else: INFO: no ready tasks
