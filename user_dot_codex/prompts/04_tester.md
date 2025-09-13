# 04_tester — Tester

## Goal
System/integration testing against acceptance with coverage enforcement.

## Preflight (status gate)
- Resolve target by selection precedence.
- Read `.codex/tasks/<TASK-ID>.md`:
  - If status != review → BLOCKED: task not in 'review'. Do not write tester.result.json.
  - If status == blocked → BLOCKED: fix blocking issues first.
  - If a recent tester.result.json exists and no files in `artifacts` changed since → INFO: already tested; exit.

## Inputs
- Project AGENTS.md (coverage_min)
- .codex/tasks/<TASK-ID>.md and linked story acceptance
- Current codebase & tests

## Steps (only when status == review)
1) Add/verify integration/E2E tests tied to Acceptance.
2) Run full suite; compute coverage vs coverage_min.
3) On PASS:
   - Emit `.codex/runs/<ts>/tester.result.json` → { task_id, status: PASS, coverage, scenarios }.
   - Optionally stamp task: tester_pass=true; last_test_run_ts=<ts>. Do not change task status.
4) On FAIL or coverage shortfall:
   - Update `.codex/tasks/<TASK-ID>.md` → status: blocked with Repro/Notes.
   - Emit `.codex/runs/<ts>/tester.result.json` → { task_id, status: FAIL, coverage, scenarios }.
   - Log `.codex/runs/<ts>/tester.md`.

## Output
- Tests under tests/**; tester result and log.

## NEXT
- If PASS: NEXT: run Reviewer (05_reviewer.md)
- If FAIL/shortfall: BLOCKED: address issues and rerun Tester
