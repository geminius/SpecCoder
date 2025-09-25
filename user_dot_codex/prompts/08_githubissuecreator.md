# 08_githubissuecreator — GitHubIssueCreator

## Goal
Materialize `.codex/tasks` entries as GitHub issues (and update existing ones) using the configured GitHub integration whenever it is enabled.

## Inputs
- `.codex/tasks/*.md`
- `.codex/spec/01.requirements.md` (for story titles)
- GitHub config block `integrations.github` from `AGENTS.md` (including optional `project_view`, `project_type` (`classic`|`v2`), and `columns` mapping)
- Environment override `CODEX_GITHUB_ENABLED`
- GitHub integration available in the session (default `server_id: github`)

## Selection
Resolve target using Selection precedence (NEXT → eligible set → INFO).

## Preflight
- Compute effective toggle: spec flag XOR env override. If disabled → `INFO: github integration disabled`.
- Require the GitHub to be available and authorized; otherwise `BLOCKED: GitHub integration unavailable`.
- No local fallback: do not implement or call direct HTTP clients, GitHub CLI, or any `.codex/tools/**` scripts to reach GitHub. Use only the configured integration tools; if unavailable/disabled → exit with `BLOCKED` (no fallback behavior).
- Ensure project `AGENTS.md` has an `integrations.github` block; if absent, append the default block and `BLOCKED: github integration not configured`. If present but `owner` or `repo` empty → `BLOCKED: github repo not configured. Please fill those fields and rerun.`
- Optional project settings: `project_view`, `project_type`, and `columns` mapping.

## Candidate Tasks
- Include tasks with status `ready|in_progress|review` where `github.issue_number` is null.
- Include tasks flagged `github.pending_update=true`.
- If none → `INFO: nothing to github_issue_creator`.

## Steps (per task)
1) Build context:
   - Load story title via `story_id` for linking.
   - Gather Scope/Test Plan excerpts for the issue body.
   - Derive labels: `story/<story_id>`, `component/<component>`, `priority/P#`, plus a status label (replace `_` with `-`, e.g., `status/in-progress`).
2) Determine action (use tool names from `integrations.github.tools` in `AGENTS.md`):
   - If `issue_number` is null → plan to create a new issue.
   - If `pending_update=true` and `issue_number` present → fetch via the integration tool (e.g., `github.getIssue(owner, repo, issue_number)` → number,url,updatedAt,state,title,body,labels,project_column).
     • 404/not found → mark for recreation; if `sync_policy=manual`, defer and leave `pending_update=true` with a note.
     • Found but snapshot hash differs → record drift in `github.sync_notes`, leave `pending_update=true`, skip edits (Integrator handles reconcile/push).
     • Found and matches hash → clear `pending_update`, update timestamps.
3) Create or edit issue when required (use `tools.issue_create` / `tools.issue_update`):
   - Compose body in a temp file via `mktemp` (delete after use). Sections: Summary, Story link, Scope bullets, Acceptance/Test Plan highlights, Open Questions, Local Status.
   - New issue: call `github.createIssue(owner, repo, title, body, labels)` through the integration and capture `number`, `url`, `updatedAt`.
   - Existing issue refresh: call `github.updateIssue(owner, repo, issue_number, title, body)` through the integration, then refresh via `github.getIssue`.
   - Update task fields (`issue_number`, `issue_url`, `last_remote_updated_at`).
4) Sync project (optional; use `tools.project_add_item` / `tools.project_move_item`):
   - If `project_view` configured, call the integration's project tools to add an item when `project_item_id` is empty, then move it to the configured status column using `project_type` and `columns` mapping (ready→Todo, in_progress→In Progress, review→Review, done→Done).
   - Store `project_item_id` on first add.
5) Update snapshot:
   - Compute `status_snapshot_sha` (sha256 of title + body + state and, when configured, labels + project column).
   - Set `last_local_sync_ts`, clear `pending_update` when action succeeded, append concise entry to `github.sync_notes`.
6) Persist:
   - Write task file with updated YAML.
   - Append summary to `.codex/runs/<ts>/github_issue_creator.md` (task id, issue number, action, outcome).

## Output
- Tasks updated with GitHub linkage and sync metadata.
- Run log describing created or reconciled issues.

## NEXT
- None. This agent does not auto-chain.
