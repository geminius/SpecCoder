# 06_integrator — Integrator

## Goal
Finish safely; update lineage and changelog; flip statuses.

## Inputs
- `.codex/spec/**`, `.codex/tasks/**`, `.codex/trace/lineage.json`
- `.codex/runs/*/tester.result.json` (preferred) or `.codex/runs/*/tester.md`
- `CHANGELOG.md` (project root)
- Policies: integrator.require_tester_log, require_tester

## Local/Remote Detection (automatic)
- If no remote/PR, or no new commit created, or working tree dirty → local mode (use shadow ids).
- Else VCS mode (require merged PR/commit).

## Preflight (Tester enforcement)
- If integrator.require_tester_log OR require_tester:
  - Missing tester result → BLOCKED: missing Tester result; stop.
  - Tester status != PASS → BLOCKED: Tester not passing; stop.

## Steps
1) For each task in `review` with gates satisfied:
   - VCS mode: ensure PR merged; get `commit_sha`.
   - Local mode: compute `shadow_id = review_baseline_sha` from task.
   - Append lineage entry (story→task→files/tests→commit_or_shadow).
2) Flip task `review → done`; if all tasks for a story are done, flip story `in_progress → done`.
3) Refresh `.codex/spec/03.tasks.md`.
4) Update `CHANGELOG.md` (story/task IDs, impact; include `commit_sha` or `shadow:<hash>`).
5) Write `.codex/runs/<ts>/integrator.md`.

## Output
- lineage updated; statuses flipped; changelog written; integrator log.

## NEXT
- None. End of chain.
