---
id: TASK-001
type: task
status: ready
priority: P2
story_id: STORY-001
component: <component>
artifacts: []
assignee: null
story_fingerprint: ""
design_fingerprint: ""
superseded_by: null
# Local-only & deterministic review
artifact_fingerprints: {}
review_baseline_sha: ""
# GitHub linkage (optional; populated when integrations.github.enabled=true)
github:
  issue_number: null
  issue_url: ""
  project_item_id: ""
  last_remote_updated_at: ""
  last_local_sync_ts: ""
  status_snapshot_sha: ""  # hash of remote title+body+state (+labels and project column when configured)
  pending_update: false
  sync_notes: []
# Tester metadata
tester_pass: null
last_test_run_ts: null
---
### Scope
<what exactly changes>

### Test Plan
- <unit>
- <integration>

### Rollback
git revert <commit or shadow>; no schema changes.
