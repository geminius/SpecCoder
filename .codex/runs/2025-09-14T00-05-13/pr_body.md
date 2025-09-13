# PR: PR automation flags and workflow hardening

Summary
- Add optional PR automation flags to AGENTS.md (builder/reviewer), default disabled.
- Builder: explicit BLOCKED terminal outputs on stop conditions; guardrails reminder.
- Reviewer: fingerprint drift gate for in_progress/review; optional changelog discipline; selection note.
- Integrator: fingerprint drift preflight; reconciliation idempotency note; selection note.
- TaskPlanner: explicit status=superseded when superseding; selection note.
- StoryPlanner/ArchitectPlanner: selection note added for consistency.

Motivation
- Align prompts and defaults fully with v1g4 spec for determinism and safety.
- Enable optional GitHub PR flows without introducing a new agent or breaking local-only paths.

Details
- AGENTS.md: add `builder.auto_open_pr`, `builder.open_pr_draft`, `builder.pr_remote`, `builder.pr_base`, `builder.branch_naming`, `reviewer.auto_mark_pr_ready`, `reviewer.request_reviewers`.
- 03_builder.md: add guardrails; emit BLOCKED: red_tests/dep_policy_violation/pr_too_large/fingerprint_drift.
- 05_reviewer.md: preflight blocks on fingerprint drift; optional changelog check; PR readiness automation notes.
- 06_integrator.md: block on fingerprint drift; clarify reconciliation idempotency.
- 02_taskplanner.md: mark superseded tasks with status and link; selection note.
- 00_storyplanner.md, 01_architectplanner.md: selection notes.

Readiness
- This PR is ready for review.
- No runtime behavior changes outside prompt/AGENTS guidance.

Testing
- Manual verification: prompts and demo_repo AGENTS updated; demo remains consistent.

Changelog
- Docs-only update to user defaults prompts and AGENTS; demo repo AGENTS updated.
