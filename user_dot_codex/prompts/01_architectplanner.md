# 01_architectplanner — ArchitectPlanner

## Goal
Make the design ready: components, interfaces, dependency policy, quality budgets.

## Inputs
- .codex/spec/01.requirements.md
- .codex/spec/02.design.md (render if missing)
- Project AGENTS.md

## Steps
1) Normalize/ensure components for all ready/planned stories (component_tags resolvable).
2) Add/adjust public interfaces for endpoints/events referenced by stories.
3) Update dependency_policy.allowed/forbidden and quality_budgets as implied by stories/NFRs.
4) Recompute design_fingerprint; set design.status=ready if prerequisites met; else keep draft and list Open Questions.
5) Log `.codex/runs/<ts>/architectplanner.md`.

## Output
- Updated `.codex/spec/02.design.md` (and optional `.codex/contracts/openapi.yaml`)

## NEXT
- If design=ready and eligible stories exist: NEXT: run TaskPlanner (02_taskplanner.md)
- If draft: BLOCKED: resolve open questions and rerun
- If ready but no eligible stories: INFO: no ready stories
