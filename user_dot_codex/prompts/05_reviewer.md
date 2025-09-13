# 05_reviewer — Reviewer

## Goal
PR checklist, DoD & policy checks; works with or without GitHub.

## Inputs
- Diff/PR (if available) or working tree changes
- Project AGENTS.md (DoD, dependency policy)
- .codex/spec/**, .codex/tasks/**
- `.codex/runs/*/tester.result.json` (preferred) or `.codex/runs/*/tester.md`

## Preflight
- If reviewer.block_without_tester OR require_tester:
  - Missing PASS tester result → set task status=blocked (reason: missing tester evidence); print BLOCKED and stop.
- Orphan diff detection (local or PR):
  - If changes touch src/**, tests/**, or scripts/** not listed in any task's `artifacts`:
    - Auto-create `.codex/tasks/TASK-RETROFIT-###.md` (priority=P1) capturing those paths; status=ready.
    - Print BLOCKED: orphan diff → created retrofit task; stop.

## Steps
1) DoD checks: IDs present, docs updated, tests present, coverage ≥ coverage_min.
2) Policy checks: dependency edges; basic perf/API sanity when feasible.
3) If critical issues → set task status=blocked with reason and stop.
4) Write `.codex/runs/<ts>/reviewer.md` (checklist + recommendations).

## Output
- Reviewer log; task may be set to blocked.

## NEXT
- If clean: NEXT: run Integrator (06_integrator.md)
- If blocked: stop after writing reason
