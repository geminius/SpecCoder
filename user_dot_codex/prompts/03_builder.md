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
Resolve target using Selection precedence (NEXT → eligible set → INFO).
Pick the first task where:
- status=ready
- fingerprints match current specs
- superseded_by=null
- dependency policy satisfied
- story.status in {planned,in_progress}
Order by priority P0→P3, then TASK-ID asc (tie-breaker: oldest last_modified_ts).

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

## PR Automation (optional)
- If `builder.auto_open_pr=true`, attempt to open a draft PR through the GitHub integration when conditions are met (use tools from `integrations.github.tools`):
  - Remote exists (`builder.pr_remote`); the GitHub integration is available; a PR for the current branch does not already exist.
  - Use title: `[STORY-ID][TASK-ID][COMP-<component>] <summary>` (per AGENTS.md conventions).
  - Use body file: `.codex/runs/<ts>/builder.md`.
  - Draft vs ready follows `builder.open_pr_draft`.
  - Use base and remote from AGENTS.md: `builder.pr_base` (default `main`) and `builder.pr_remote` (default `origin`).
  - If a PR already exists: print `INFO: PR already exists` and continue.
  - If prerequisites are not met (no commits, no remote), skip silently; do not block local workflows.

## Chaining (optional)
If auto_run_next_task=true, loop up to builder.max_tasks_per_run respecting chain_scope and stop_on rules; honor timebox.
Note: chain_scope allowed values: same_story | same_component | any.

## Output
- Code + tests only; task ends in review; run log updated.

## NEXT
- NEXT: run Tester (04_tester.md) for the last processed task (Tester may be auto-run if auto_post_build_test=true).

## Guardrails
- Edit only: `src/**`, `tests/**`, `.codex/tasks/**`, `.codex/tools/**` (and `scripts/**` if allowed by project AGENTS.md).
- May update `.codex/spec/01.requirements.md` to flip the related story status to `in_progress` (no other spec edits).

## Stop Conditions
- On any of the following, print a terminal line and stop:
  - `BLOCKED: red_tests` (tests failing after implementation attempts)
  - `BLOCKED: dep_policy_violation` (violates dependency_policy)
  - `BLOCKED: pr_too_large` (exceeds small_prs threshold/timebox)
  - `BLOCKED: fingerprint_drift` (story/design fingerprints no longer match)
