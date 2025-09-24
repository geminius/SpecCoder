# 06_integrator — Integrator

## Goal
Finish safely; update lineage and changelog; mirror GitHub issues/projects when enabled.

## Inputs
- `.codex/spec/**`, `.codex/tasks/**`, `.codex/trace/lineage.json`
- `.codex/runs/*/tester.result.json` (preferred) or `.codex/runs/*/tester.md`
- `CHANGELOG.md` (project root)
- Policies: integrator.require_tester_log, require_tester
- Optional GitHub config: `integrations.github` block from `AGENTS.md` + env override `CODEX_GITHUB_ENABLED`
- MCP GitHub server when integration is enabled

## Selection
Resolve target using Selection precedence (NEXT → eligible set → INFO).

## Local/Remote Detection (automatic)
- If no remote/PR, or no new commit created, or working tree dirty → local mode (use shadow ids).
- Else VCS mode (require merged PR/commit).

## Preflight
- Tester enforcement (if integrator.require_tester_log OR require_tester):
  - Missing tester result → `BLOCKED: missing Tester result`.
  - Tester status != PASS → `BLOCKED: Tester not passing`.
- Fingerprint drift: if any candidate task in `review` has story/design fingerprint drift vs current specs → `BLOCKED: fingerprint drift`.
- GitHub readiness (if integration enabled):
  - Require an available, authorized MCP GitHub server; on failure → mark tasks `github.pending_update=true`, log `INFO: github sync skipped`, continue with local duties.
  - Cache effective policy: `enabled` = spec flag XOR env override.

## GitHub Reconciliation (if enabled)
1) Identify candidate tasks with `github.issue_number`.
2) Batch fetch issue metadata via MCP (use `integrations.github.tools.issue_get`); cache responses under `.codex/trace/github_cache.json` for idempotency.
3) Compare remote state hash against `github.status_snapshot_sha`:
   - Missing issue → set task `status=blocked` with reason "github issue missing" and append note to `github.sync_notes`.
   - Remote closed + fingerprints match → allow local completion.
   - Remote closed + fingerprints differ → set task `status=blocked` and record drift in `github.sync_notes`.
   - Remote reopened/retitled/commented → refresh `status_snapshot_sha`, set `github.pending_update=true` if local follow-up required.
4) Respect `sync_policy`:
   - `manual`: record drift, do not issue remote writes (leave `pending_update=true`).
   - `push_only`/`two_way`: stage the necessary close/reopen/comment/project actions for step 6.

## Steps
1) Reconcile shadows (idempotent):
   - Scan `.codex/trace/lineage.json` for `shadow:<hash>` entries and replace with real commits when diff hashes now match.
   - Do not change task/story status during reconciliation.
2) For each task in `review` with gates satisfied:
   - VCS mode: require merged PR; capture `commit_sha`.
   - Local mode: compute `shadow_id = review_baseline_sha` from the task.
   - Append lineage entry (story→task→files/tests→`commit_or_shadow`).
3) Flip task `review → done`; if all tasks per story are done, flip story `in_progress → done`.
4) Refresh `.codex/spec/03.tasks.md`.
5) Update `CHANGELOG.md` (story/task IDs, impact; include `commit_sha` or `shadow:<hash>`).
6) GitHub push (if enabled & policy allows):
   - Apply queued actions: close/reopen issues, move project cards via MCP project tools (use `integrations.github.tools.project_move_item`), add/update story cross-links or comments.
   - Clear `github.pending_update` for successful actions; stamp `last_local_sync_ts` + new `status_snapshot_sha`.
   - On failure, leave `pending_update=true`, append details to `github.sync_notes`, and continue.
7) Write `.codex/runs/<ts>/integrator.md` (summaries, sync results).

## Output
- Lineage updated; statuses flipped; changelog written.
- GitHub issues/project items synchronized when enabled and successful; drift noted otherwise.

## NEXT
- None. End of chain.
