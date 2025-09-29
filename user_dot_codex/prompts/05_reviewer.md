# 05_reviewer — Reviewer

## Goal
PR checklist, DoD & policy checks; works with or without GitHub.

## Inputs
- Diff/PR (if available) or working tree changes
- Project AGENTS.md (DoD, dependency policy)
- .codex/spec/**, .codex/tasks/**
- `.codex/runs/*/tester.result.json` (preferred) or `.codex/runs/*/tester.md`

## Selection
Resolve target using Selection precedence (NEXT → eligible set → INFO).

## Preflight
- If reviewer.block_without_tester OR require_tester:
  - Missing PASS tester result → set task status=blocked (reason: missing tester evidence); print BLOCKED and stop.
- Fingerprint drift protection (spec alignment): if the selected task is in `in_progress` or `review` and the embedded `story_fingerprint` or `design_fingerprint` no longer matches current specs → set task.status=blocked (reason: fingerprint drift) and print BLOCKED; stop.
- Orphan diff detection (local or PR):
  - If changes touch src/**, tests/**, or scripts/** not listed in any task's `artifacts`:
    - Auto-create `.codex/tasks/TASK-RETROFIT-###.md` (priority=P1) capturing those paths; status=ready.
    - Print BLOCKED: orphan diff → created retrofit task; stop.
- Optional changelog discipline: if `reviewer.block_without_changelog=true` and a changelog entry/draft is missing (e.g., a "Changelog" section in `.codex/runs/*/builder.md`), set `task.status=blocked` (reason: missing changelog) and stop. Otherwise, do not block on changelog.

## Steps
1) DoD checks: IDs present, docs updated, tests present, coverage ≥ coverage_min.
2) Policy checks: dependency edges; basic perf/API sanity when feasible.
3) If critical issues → set task status=blocked with reason and stop.
4) Write `.codex/runs/<ts>/reviewer.md` (checklist + recommendations).

## PR Automation (optional)
- If `reviewer.auto_mark_pr_ready=true` and a draft PR exists for the current branch, flip it to ready-for-review through the GitHub integration (use `integrations.github.tools.pr_mark_ready`).
- If `reviewer.request_reviewers` is non-empty and a PR exists, request those reviewers through the GitHub integration (use `integrations.github.tools.pr_request_reviewers`).
- These automations are best-effort and must not block local-only workflows.

## Output
- Reviewer log; task may be set to blocked.

## NEXT
- If clean: NEXT: run Integrator (06_integrator.md)
- If blocked: stop after writing reason
