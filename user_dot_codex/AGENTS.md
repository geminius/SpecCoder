# AGENTS.md (user defaults) — v1g4

## Agent Registry
- StoryPlanner: 00_storyplanner.md
- ArchitectPlanner: 01_architectplanner.md
- TaskPlanner: 02_taskplanner.md
- Builder: 03_builder.md
- Tester: 04_tester.md
- Reviewer: 05_reviewer.md
- Integrator: 06_integrator.md

## Schemas (authoritative)
- story: ~/.codex/schemas/requirements.template.md
- design: ~/.codex/schemas/design.template.md
- task: ~/.codex/schemas/task.template.md
- tasks_list_view: ~/.codex/schemas/tasks_list.template.md

## Selection precedence (zero-parameter; applies to all agents)
1) Latest `NEXT:` in `.codex/runs/*/*.md` that is still valid (not stale by fingerprint/status).
2) Deterministic eligible-set pick from `.codex/**`:
   - by `priority` (P0→P3), then numeric id ascending
   - tie-breaker: oldest `last_modified_ts`
3) If nothing eligible → print `INFO: nothing to <agent>` and exit.

## Policies (defaults; project may override)
- tests_first: true
- small_prs: true
- auto_spec_chain: false
- auto_post_build_test: false
- auto_run_next_task: true
- Tester gate: runs only when task status=review (hard rule; no flag)

## Builder Chain Settings
- builder.max_tasks_per_run: 3
- builder.chain_scope: same_story  # allowed: same_story | same_component | any
- builder.stop_on:
  - red_tests
  - dep_policy_violation
  - fingerprint_drift
  - pr_too_large
- builder.timebox_minutes: 30

## Review/Test/Trace policies
- require_tester: false
- reviewer.block_without_tester: false
- integrator.require_tester_log: false
- reviewer.block_without_changelog: false
- integrator.require_changelog_entry: false

## Local-only shadow integration (automatic; no flags)
- If no remote, or working tree dirty, or no new commit created during the run → Integrator switches to local mode.
- In local mode, `shadow_id = review_baseline_sha` (from task) is used in lineage/changelog instead of a commit SHA.
- Later, if a real commit appears with matching diff hash, Integrator may reconcile `shadow_id → commit_sha` (idempotent).

## Global Guardrails & Commands
- Never edit: infra/**, .github/**, deploy/**, **/*.secrets*, **/.env*, **/secrets/**
- Builder edits only: src/**, tests/**, scripts/**, .codex/tasks/**
- Commands (override in project): install, lint, test, test:it, coverage_min (default 80)
- Commit/PR (when VCS is used): "[STORY-ID][TASK-ID][COMP-<component>] <summary>"

## Spec Conventions
- Front-matter: YAML with stable keys (see schemas)
- Fingerprints required: story_fingerprint, design_fingerprint
- .codex/spec/03.tasks.md is derived; planners rebuild it (do not hand-edit)
- Status transitions: story draft→ready→planned→in_progress→done (blocked side-state); task ready→in_progress→review→done (blocked|needs_update|superseded side-states)
