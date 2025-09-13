---
id: TASK-001
type: task
status: done
priority: P1
story_id: STORY-001
component: api
artifacts: ['src/api/reset.py', 'tests/api/test_reset.py']
assignee: codex
story_fingerprint: "sha256:b2e05a12a67f7f7f35f6da5e6f71750a0c0f4a1c2b273c51d66706f479fc6be6"
design_fingerprint: "sha256:20ac8619173d9f92645a468e7d63e3e7c92fac501b98df3a606ff15d212465cb"
superseded_by: null
artifact_fingerprints:
  src/api/reset.py: 32a2901a07c8db1455cfefa289526ca4327907d5c449b768ed0963dd21a1425e
  tests/api/test_reset.py: cb4f9e96dd8c368b121b7aa70b7b88f4e610cfa58b0e6cc611ee3fb3317cc94a
review_baseline_sha: "db5918b1355c090188875e7999cfd68b5eddf40f36f28255d2c975518e01a380"
tester_pass: true
last_test_run_ts: "2025-09-13T08:49:42.694159Z"
---
### Scope
Create POST /v1/auth/reset handler that validates input and returns {ok: true}. Stub notify/db.

### Test Plan
- unit: request_password_reset returns ok for valid email
- integration: (future) trigger notify queue

### Rollback
git revert <commit or shadow>; no schema changes.
