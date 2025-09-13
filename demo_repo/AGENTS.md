# AGENTS.md (project)

## Overrides
install: python -m pip install -r requirements.txt
lint: python -m pyflakes src
test: python -m pytest -q --disable-warnings
test:it: python -m pytest -q -m 'it'
coverage_min: 80

components: [auth, api, notify, db]

# Optional PR automation (kept disabled in demo)
builder.auto_open_pr: false
builder.open_pr_draft: true
builder.pr_remote: origin
builder.pr_base: main
builder.branch_naming: task/<TASK-ID>
reviewer.auto_mark_pr_ready: false
reviewer.request_reviewers: []
