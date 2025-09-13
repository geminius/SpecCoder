# Codex Agentic Framework — v1g4

This pack reflects the v1g4 design:
- Zero-parameter selection (NEXT → eligible set)
- Tester runs only on `review`
- Builder computes `artifact_fingerprints` and `review_baseline_sha`
- Reviewer auto-creates retrofit tasks for orphan code changes
- Integrator supports local-only **shadow lineage** (no GitHub required)

Copy:
- `user_dot_codex/` → `~/.codex/`
- `project_skeleton/` → your repo, then run the agents.
