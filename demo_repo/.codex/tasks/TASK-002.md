---
id: TASK-002
type: task
status: ready
priority: P2
story_id: STORY-002
component: api
artifacts: ['src/api/reports_export.py', 'tests/api/test_reports_export.py']
assignee: null
story_fingerprint: "sha256:4e6875acfa96dfb5f3a6a030a1b7fb3b01b9d92737d2c24fee589fe3a3e1c5a6"
design_fingerprint: "sha256:2ff2b48a932e4e0e3b5b586426e8d72dfda7de9b3fcef706379c6ba4eaeb1892"
superseded_by: null
artifact_fingerprints: {}
review_baseline_sha: ""
tester_pass: null
last_test_run_ts: null
---
### Scope
Add GET /v1/reports/{id}/export?format=csv endpoint: validate params, enforce role permissions, stream CSV from reporting layer, set headers and filename, handle 404/413.

### Test Plan
- unit: permission check denies non-Analyst roles (403)
- unit: 404 for invalid report id
- integration: successful CSV download with correct headers and UTF-8 encoding
- integration: 413 when row count exceeds 50,000 with proper message
- observability: audit event `reports.export.requested` emitted

### Rollback
git revert <commit or shadow>; no schema changes.
