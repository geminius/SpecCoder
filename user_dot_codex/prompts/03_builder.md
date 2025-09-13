# 03_builder — Builder

## Goal
Implement a ready task via TDD; minimal diffs; policy-compliant.

## Inputs
- .codex/tasks/*.md
- .codex/spec/02.design.md (dependency policy)
- .codex/spec/01.requirements.md (for story status flip)
- Project AGENTS.md commands
- Policies: auto_run_next_task, auto_post_build_test; Builder Chain Settings

## Selection
Pick the first task where:
- status=ready
- fingerprints match current specs
- superseded_by=null
- dependency policy satisfied
- story.status in {planned,in_progress,done}
Order by priority P0→P3, then TASK-ID asc.

## Steps (per task)
1) Claim → update `.codex/tasks/<TASK-ID>.md` → status: in_progress; set `assignee` if available; log claim.
2) Story flip (idempotent) → if no other tasks for story are in {in_progress, review}, set that story’s status=in_progress in `.codex/spec/01.requirements.md`.
3) TDD → write failing tests; run (expect red).
4) Implement minimal code in `artifacts`; run lint + unit + it until green.
5) Move to review → update task to status=review; compute and write:
   - `artifact_fingerprints` (path → sha256(content))
   - `review_baseline_sha` (sha256 over sorted `artifact_fingerprints`)
   - append mini changelog
6) Prepare PR body text (even if no PR) in `.codex/runs/<ts>/builder.md`.
7) Refresh `.codex/spec/03.tasks.md` if needed.

## Chaining (optional)
If auto_run_next_task=true, loop up to builder.max_tasks_per_run respecting chain_scope and stop_on rules; honor timebox.

## Output
- Code + tests only; task ends in review; run log updated.

## NEXT
- NEXT: run Tester (04_tester.md) for the last processed task (Tester may be auto-run if auto_post_build_test=true).

## Stop Conditions
- red_tests; dep_policy_violation; pr_too_large; fingerprint_drift
