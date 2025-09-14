---
id: TASK-003
type: task
status: ready
priority: P2
story_id: STORY-002
component: reporting
artifacts: ['src/reporting/csv_export.py', 'tests/reporting/test_csv_export.py']
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
Implement CSV generation for reports: header row, UTF-8 encoding, quoting, row limit enforcement (50,000), and streaming support.

### Test Plan
- unit: CSV rows properly quoted and UTF-8 encoded
- unit: header row present and correct order
- unit: raises/export-limit condition beyond 50,000 rows
- integration: emits `reports_export_csv_total` counter and latency histogram on export

### Rollback
git revert <commit or shadow>; no schema changes.
