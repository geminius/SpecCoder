# 07_pr_creator — PR Creator (Utility)

## Goal
Commit current changes and open a ready‑for‑review PR via GitHub CLI, honoring guardrails and not breaking local‑only workflows.

## Inputs
- Project/user `AGENTS.md` (PR Automation settings and title convention)
- Git repository state (remotes, default branch)
- Optional: `.codex/tasks/*.md` and latest `.codex/runs/*/builder.md` for PR title/body hints

## Selection
Utility prompt — run explicitly. For consistency: resolve targets using Selection precedence if applicable.

## Guardrails / Preflight (must pass)
1) GitHub CLI present and authenticated:
   - `command -v gh >/dev/null 2>&1` else `BLOCKED: gh not installed`.
   - `gh auth status` must succeed; token must include `repo` scope; else `BLOCKED: gh not authenticated`.
2) Remote present and reachable:
   - `git remote get-url origin` must succeed; else `BLOCKED: no remote origin`.
3) Determine base branch (default):
   - `BASE=$(git rev-parse --abbrev-ref origin/HEAD | sed 's#origin/##') || BASE=main`.
4) Enforce forbidden paths policy (fail‑closed):
   - If staged or working changes touch `infra/**`, `.github/**`, `deploy/**`, `**/*.secrets*`, `**/.env*`, `**/secrets/**` → `BLOCKED: forbidden path changes`.
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
5) Create PR (ready‑for‑review):
   - If PR already exists for branch: update body if needed and ensure it’s ready: `gh pr view "$BRANCH" || true; gh pr ready "$BRANCH" || true`.
   - Else create: `gh pr create --base "$BASE" --head "$BRANCH" --title "<derived title>" --body-file <body.md>` (omit `--draft` so it’s ready).
   - If reviewers configured in `reviewer.request_reviewers`, then: `gh pr edit "$BRANCH" --add-reviewer <comma-separated>`.
6) Terminal line:
   - On success: `NEXT: PR created/updated and ready for review`.
   - On soft issues: `INFO: pr_too_large` (if large) or `INFO: PR already exists (ensured ready)`.
   - On hard issues: `BLOCKED: <reason>`.

## Notes
- Never blocks local‑only workflows outside PR creation: if preflight fails (no remote or gh), stop cleanly with BLOCKED; do not modify repo.
- Idempotent: safe to rerun; reuses branch and PR if present, ensures ready state.
- Keep titles short; detailed notes go in the PR body file.
