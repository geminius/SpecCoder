# 07_pr_creator — PR Creator (Utility)

## Goal
Commit current changes and open a ready‑for‑review PR through the GitHub integration, honoring guardrails and not breaking local-only workflows.

## Inputs
- Project/user `AGENTS.md` (PR Automation settings and title convention)
- Git repository state (remotes, default branch)
- Optional: `.codex/tasks/*.md` and latest `.codex/runs/*/builder.md` for PR title/body hints

## Selection
Utility prompt — run explicitly. For consistency: resolve targets using Selection precedence if applicable.

## Guardrails / Preflight (must pass)
0) Integration toggle and policy (no local fallback):
   - Compute effective toggle: spec flag XOR env override (`CODEX_GITHUB_ENABLED`). If disabled → `INFO: github integration disabled`.
   - Require the GitHub integration to be available and authorized; otherwise `BLOCKED: GitHub integration unavailable`.
   - Use only the configured integration tools; do not create or invoke any local scripts/clients (no `.codex/tools/**`, no `gh`, no direct HTTP). If integration is disabled/unavailable → exit with `BLOCKED` (do not attempt local fallbacks).
1) Project configuration present:
   - Ensure project `AGENTS.md` contains an `integrations.github` block; if absent, append the default block and `BLOCKED: github integration not configured`.
   - If `owner` or `repo` is empty → `BLOCKED: github repo not configured. Please fill those fields and rerun.`
2) Remote present and reachable:
   - `git remote get-url origin` must succeed; else `BLOCKED: no remote origin`.
3) Determine base branch (default):
   - `BASE=$(git rev-parse --abbrev-ref origin/HEAD | sed 's#origin/##') || BASE=main`.
4) Enforce forbidden paths policy (fail‑closed):
   - If staged or working changes touch `infra/**`, `.github/**`, `deploy/**`, `**/*.secrets*`, `**/.env*`, `**/secrets/**` → `BLOCKED: forbidden path changes`.
     - Exception (opt‑in): if `integrations.github.pr_creator.allow_repo_plumbing=true`, allow PRs that include `.github/**` or repo plumbing changes for review (PR Creator never authors those changes itself). Other sensitive paths remain blocked.
     - Example check: `git status --porcelain | awk '{print $2}' | rg -n '^(infra/|\.github/|deploy/)|(\.secrets|/secrets/|/\.env)'`.
5) Small PR sanity (advisory):
   - If changed files > 50 or total diff > ~1000 lines, print `INFO: pr_too_large` and proceed only if explicitly confirmed.
6) Tests‑first sanity (advisory):
   - Optionally run `lint`/`test` commands from AGENTS.md before creating the PR; if failing, `BLOCKED: red_tests` (project policy dependent).

## Steps
1) Derive PR title and body (rich auto-generation):
   - Changed files: collect from `git diff --cached --name-status || git diff --name-status` for a Files Changed section.
   - Task match: find `.codex/tasks/TASK-*.md` with `status in {review,in_progress}` whose `artifacts` intersect ≥60% with changed files; pick the strongest match.
   - Title:
     - If a task matched: `[<STORY-ID>][<TASK-ID>][COMP-<component>] <short summary>`.
     - Else: `chore: <short summary>` (derive from first commit message or a brief summary of changes).
   - Body assembly (prefer latest `.codex/runs/*/builder.md` if present; otherwise synthesize):
     - Summary: one-paragraph explanation of what and why.
     - Motivation: if task matched → include story “Motivation” from `.codex/spec/01.requirements.md` for that `story_id`.
     - Details: outline key changes; include any design/policy notes.
     - Scope: if task matched → include task “Scope” section.
     - Testing: include unit/integration notes; if latest `.codex/runs/*/tester.result.json` for the task is PASS, include coverage percentage and scenario names.
     - Files Changed: embed the changed files list (optionally with status A/M/D).
     - Changelog (draft): `- <story_id>/<task_id> [<component>]: <one-line summary> (to be finalized on merge)`.
   - Store the rendered body to a temp file under `.codex/runs/<ts>/pr_body.md` for traceability.
2) Branching (idempotent):
   - If using a task: `BRANCH="${builder.branch_naming:-task/<TASK-ID>}"`.
   - Else: `BRANCH="chore/auto-pr-$(date +%Y-%m-%dT%H-%M-%S)"`.
   - `git checkout -B "$BRANCH"`.
3) Commit (idempotent):
   - Stage changes (respect .gitignore): `git add -A`.
   - If nothing to commit → skip to push/PR.
   - Commit: `git commit -m "<derived title>"`.
4) Push:
   - `git push -u origin "$BRANCH"`.
5) Create PR (ready-for-review) via configured tools in `integrations.github.tools`:
   - If a PR already exists for branch: ensure it’s ready and update body (use `tools.pr_get`, `tools.pr_mark_ready`, `tools.pr_update`). If multiple open PRs reference the same task, prefer the one whose diff overlaps the highest proportion of the task’s `artifacts`; if ambiguous, print `INFO: multiple candidate PRs` and proceed with the branch‑matched PR only.
   - Else create using the GitHub integration (use `tools.pr_create` with base=head/title/body) (create as ready by default unless project policy dictates draft).
   - If reviewers configured in `reviewer.request_reviewers`, request through the integration (use `tools.pr_request_reviewers`).
6) Terminal line:
   - On success: `NEXT: PR created/updated and ready for review`.
   - On soft issues: `INFO: pr_too_large` (if large) or `INFO: PR already exists (ensured ready)`.
   - On hard issues: `BLOCKED: <reason>`.

## Notes
- Never blocks local-only workflows outside PR creation: if preflight fails (no remote or GitHub integration), stop cleanly with BLOCKED; do not modify repo.
- No local fallback: use only the configured GitHub integration tools; do not create or run any `.codex/tools/**` scripts for PRs.
- Idempotent: safe to rerun; reuses branch and PR if present, ensures ready state.
- Keep titles short; detailed notes go in the PR body file.
