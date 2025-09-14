# Codex Agentic Framework — v1g4

A spec‑first, prompt‑only workflow that turns product specs into deterministic coding loops — no servers, no hidden state. Agents are stateless and run with zero parameters.

## What’s Inside
- User‑level defaults under `user_dot_codex/` (copy to `~/.codex/`):
  - `AGENTS.md` — policies, selection rules, guardrails
  - `prompts/00..06` — StoryPlanner → Integrator agent prompts
  - `prompts/07_pr_creator.md` — optional PR creation utility (GitHub CLI)
  - `schemas/` — story, design, task, and derived list templates
- A minimal `demo_repo/` showing the full loop with local‑only “shadow lineage”.

## Key Features
- Zero‑parameter selection (NEXT trail → eligible set)
- Tests‑first (Tester runs only when a task is in `review`)
- Builder records `artifact_fingerprints` and `review_baseline_sha`
- Reviewer auto‑creates retrofit tasks for orphan diffs
- Integrator works with or without GitHub (local shadow lineage supported)
- Optional PR automation (via Builder/Reviewer flags) and a PR Creator utility prompt

## Quick Start
1) Copy `user_dot_codex/` → `~/.codex/`.
2) In your project, run agents in order or jump in anywhere:
   - StoryPlanner → ArchitectPlanner → TaskPlanner → Builder → Tester → Reviewer → Integrator
3) No GitHub? Everything still works locally; Integrator records a shadow ID.
4) On GitHub? Use the optional PR flags in `AGENTS.md` or run `07_pr_creator.md` to open a ready‑for‑review PR with an auto‑generated description.

## Common Use Cases
- New feature: Plan stories/design → generate small tasks → TDD via Builder → test/review/integrate.
- Existing codebase, add specs: Backfill stories/design; TaskPlanner creates focused tasks; Reviewer catches orphan diffs.
- Hotfix: Mark story `kind: hotfix` (P0); a single focused task; integrate safely.
- Local‑only: End‑to‑end without commits/PRs; Integrator logs shadow lineage.
- GitHub PRs: Use Builder/Reviewer flags or the `07_pr_creator` utility to script draft/ready PRs.

## More Details
For the full end‑to‑end design and policies, see `spec_driven_codex_agentic_framework_end_to_end_design_v_1.md`.

---

Tip: Project‑level overrides live in your repo’s `AGENTS.md` (see `demo_repo/AGENTS.md` for examples). Forbidden paths and Builder‑editable areas are enforced by guardrails.
