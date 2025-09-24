# AGENTS.md (project)

## Overrides
install: python -m pip install -r requirements.txt
lint: python -m pyflakes src
test: python -m pytest -q --disable-warnings
test:it: python -m pytest -q -m 'it'
coverage_min: 80

components: [auth, api, notify, db]

# GitHub integration (demo settings) — uses MCP
integrations:
  github:
    enabled: true
    owner: geminius
    repo: SpecCoder
    project_view: "test-project"
    default_column: "Todo"
    sync_policy: push_only
    server_id: github
    tools:
      issue_get: github.getIssue
      issue_create: github.createIssue
      issue_update: github.updateIssue
      project_add_item: github.projects.addItem
      project_move_item: github.projects.moveItem
      pr_get: github.getPullRequest
      pr_create: github.createPullRequest
      pr_update: github.updatePullRequest
      pr_mark_ready: github.markReadyForReview
      pr_request_reviewers: github.requestReviewers

# Optional PR automation (kept disabled in demo)
builder.auto_open_pr: false
builder.open_pr_draft: true
builder.pr_remote: origin
builder.pr_base: main
builder.branch_naming: task/<TASK-ID>
reviewer.auto_mark_pr_ready: false
reviewer.request_reviewers: []
