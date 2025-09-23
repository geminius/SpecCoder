# 08_githubissuecreator — GitHubIssueCreator

## Goal
Materialize `.codex/tasks` entries as GitHub issues (and update existing ones) whenever GitHub integration is enabled.

## Inputs
- `.codex/tasks/*.md`
- `.codex/spec/01.requirements.md` (for story titles)
- GitHub config block `integrations.github` from `AGENTS.md`
- Environment override `CODEX_GITHUB_ENABLED`
- GitHub CLI (`gh`) with `repo` scope

## Selection
Resolve target using Selection precedence (NEXT → eligible set → INFO).

## Preflight
- Compute effective toggle: spec flag XOR env override. If disabled → `INFO: github integration disabled`.
- Require `gh` installed/authenticated; otherwise `BLOCKED: gh not available`.
- Run `gh auth status` first (no auto-login). Missing `repo`/`project` scopes or auth failure → `BLOCKED: gh not authenticated` with guidance to run `gh auth login --scopes repo,project`. 
- Ensure project `AGENTS.md` has an `integrations.github` block; if absent, append the default block and `BLOCKED: github integration not configured`. If present but `owner` or `repo` empty → `BLOCKED: github repo not configured. Please fill those fields and rerun.`
- Optional project settings: `project_view`, `default_column`.

## Candidate Tasks
- Include tasks with status `ready|in_progress|review` where `github.issue_number` is null.
- Include tasks flagged `github.pending_update=true`.
- If none → `INFO: nothing to github_issue_creator`.

## Steps (per task)
1) Build context:
   - Load story title via `story_id` for linking.
   - Gather Scope/Test Plan excerpts for the issue body.
   - Derive labels: `story/<story_id>`, `component/<component>`, `priority/P#`, plus a status label (replace `_` with `-`, e.g., `status/in-progress`).
2) Determine action:
   - If `issue_number` is null → plan to create a new issue.
   - If `pending_update=true` and `issue_number` present → run `gh issue view --repo <owner/repo> <issue_number> --json number,url,updatedAt,state,title,body` (treat 404 as deleted).
     • 404/not found → mark for recreation.
     • Found but remote hash differs → record drift in `github.sync_notes`, leave `pending_update=true`, skip edits (Integrator handles reconcile).
     • Found and matches hash → clear `pending_update`, update timestamps.
3) Create or edit issue when required:
   - Compose body in a temp file via `mktemp` (delete after use). Sections: Summary, Story link, Scope bullets, Acceptance/Test Plan highlights, Open Questions, Local Status.
   - New issue: `gh issue create --repo <owner/repo> --title "TASK-###: <summary>" --body-file <tempfile> --label <labels> --json number,url,updatedAt`.
   - Existing issue refresh: `gh issue edit --repo <owner/repo> <issue_number> --title ... --body-file <tempfile>` then `gh issue view --json number,url,updatedAt,state,title,body` for metadata.
   - Update task fields (`issue_number`, `issue_url`, `last_remote_updated_at`).
4) Sync project (optional):
   - If `project_view` configured, call `gh project item-add` when `project_item_id` empty, then `gh project item-move` to column mapped from task status (ready→Todo, in_progress→In Progress, review→Review, done→Done).
   - Store `project_item_id` on first add.
5) Update snapshot:
   - Compute `status_snapshot_sha` (sha256 of title + body + state).
   - Set `last_local_sync_ts`, clear `pending_update` when action succeeded, append concise entry to `github.sync_notes`.
6) Persist:
   - Write task file with updated YAML.
   - Append summary to `.codex/runs/<ts>/github_issue_creator.md` (task id, issue number, action, outcome).

## Output
- Tasks updated with GitHub linkage and sync metadata.
- Run log describing created or reconciled issues.

## NEXT
- None. This agent does not auto-chain.
