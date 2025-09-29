# 06_integrator — Integrator

## Goal
Finish safely; update lineage and changelog; mirror GitHub issues/project boards when enabled.

## Inputs
- `.codex/spec/**`, `.codex/tasks/**`, `.codex/trace/lineage.json`
- `.codex/runs/*/tester.result.json` (preferred) or `.codex/runs/*/tester.md`
- `CHANGELOG.md` (project root)
- Policies: integrator.require_tester_log, require_tester
- Optional GitHub config: `integrations.github` block from `AGENTS.md` + env override `CODEX_GITHUB_ENABLED`
  - Project settings (optional): `project_view`, `project_type` (`classic` | `v2`, default `v2`), and `columns` mapping
  - PR settings (optional): `pr_base`, `pr_remote`
  - `sync_policy`: `manual` | `push_only` | `two_way` (see below)
- GitHub integration available when integration is enabled

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
- Changelog discipline (optional): if `integrator.require_changelog_entry=true`, require a changelog entry or draft to exist before integration.
  - Accept either a "Changelog" section in the latest `.codex/runs/*/builder.md` for the task or a prepared entry in `CHANGELOG.md` referencing the story/task.
  - If missing → `BLOCKED: missing changelog entry`.
- GitHub readiness (if integration enabled):
  - Require the configured GitHub integration to be available and authorized; on failure → mark tasks `github.pending_update=true`, log `INFO: github sync skipped`, continue with local duties.
  - Cache effective policy: `enabled` = spec flag XOR env override.
  - Record effective `sync_policy` from `integrations.github`.

## GitHub Reconciliation (if enabled)
1) Identify candidate tasks with `github.issue_number`.
2) Batch fetch issue metadata through the GitHub integration (use `integrations.github.tools.issue_get`) with simple rate limiting (e.g., max ~50 items per run; exponential backoff on 429/5xx). Cache responses under `.codex/trace/github_cache.json` for idempotency.
3) Compare remote state (title+body+state+labels+project column when configured) against `github.status_snapshot_sha`:
   - Missing issue → do not block: set `github.pending_update=true`. If `sync_policy` is `push_only` or `two_way`, stage recreation for step 6; if `manual`, append note to `github.sync_notes`.
   - Remote closed + fingerprints match → allow local completion.
   - Remote closed + fingerprints differ → set task `status=blocked` and record drift in `github.sync_notes`.
   - Remote reopened/retitled/commented/label/column changed → refresh `status_snapshot_sha`, set `github.pending_update=true` if local follow-up is required.
4) Respect `sync_policy`:
   - `manual`: record drift; do not issue remote writes (leave `pending_update=true`).
   - `push_only`: stage local→remote actions only (close/reopen/comment/update/project move); never flip local state from remote.
   - `two_way`: as `push_only`, plus allow safe remote→local status flips when unambiguous (e.g., remote reopen after last sync may flip `done→review` only if artifact fingerprints unchanged since review; otherwise record drift).

## Steps
1) Reconcile shadows (idempotent):
   - Scan `.codex/trace/lineage.json` for `shadow:<hash>` entries and replace with real commits when diff hashes now match.
   - Do not change task/story status during reconciliation.
2) For each task in `review` with gates satisfied:
   - VCS mode: require merged PR; capture `commit_sha`.
   - Local mode: compute `shadow_id = review_baseline_sha` from the task.
   - If multiple merged commits touch the task’s `artifacts`, choose the commit whose diff overlaps the highest proportion of those `artifacts`; if ambiguous, emit `INFO: multiple candidate commits` and defer association until clarified.
   - Append lineage entry (story→task→files/tests→`commit_or_shadow`).
3) Flip task `review → done`; if all tasks per story are done, flip story `in_progress → done`.
4) Refresh `.codex/spec/03.tasks.md`.
5) Update `CHANGELOG.md` (story/task IDs, impact; include `commit_sha` or `shadow:<hash>`).
6) GitHub push (if enabled & policy allows):
   - Apply queued actions: create/update/close/reopen issues, move project cards using the GitHub integration tools (use `integrations.github.tools.project_move_item`), add/update story cross-links or comments. Respect `project_type` and `columns` mapping when moving cards.
   - Clear `github.pending_update` for successful actions; stamp `last_local_sync_ts` + new `status_snapshot_sha`.
   - On failure, leave `pending_update=true`, append details to `github.sync_notes`, and continue.
7) Write `.codex/runs/<ts>/integrator.md` (summaries, sync results).

## Output
- Lineage updated; statuses flipped; changelog written.
- GitHub issues/project items synchronized when enabled and successful; drift noted otherwise.

## NEXT
- None. End of chain.
