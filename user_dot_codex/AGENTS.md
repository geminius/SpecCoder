# AGENTS.md (user defaults) — v1g4

## Agent Registry
- StoryPlanner: 00_storyplanner.md
- ArchitecturePlanner: 01_architectureplanner.md
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

## PR Automation (optional)
# Builder can optionally open a draft PR after moving a task to review.
# Reviewer can optionally flip a draft PR to ready-for-review.
- builder.auto_open_pr: false
- builder.open_pr_draft: true
- builder.pr_remote: origin
- builder.pr_base: main
# Optional: create/use a branch per task when opening PRs (tooling dependent)
- builder.branch_naming: task/<TASK-ID>
- reviewer.auto_mark_pr_ready: false
# Optional: auto-request reviewers by handle
- reviewer.request_reviewers: []

## Local-only shadow integration (automatic; no flags)
- If no remote, or working tree dirty, or no new commit created during the run → Integrator switches to local mode.
- In local mode, `shadow_id = review_baseline_sha` (from task) is used in lineage/changelog instead of a commit SHA.
- Later, if a real commit appears with matching diff hash, Integrator may reconcile `shadow_id → commit_sha` (idempotent).

## Global Guardrails & Commands
- Never edit: infra/**, .github/**, deploy/**, **/*.secrets*, **/.env*, **/secrets/**
- Builder edits only: src/**, tests/**, scripts/**, .codex/tasks/**, .codex/tools/**
- Commands (override in project): install, lint, test, test:it, coverage_min (default 80)
- Commit/PR (when VCS is used): "[STORY-ID][TASK-ID][COMP-<component>] <summary>"

## Agent Tooling Convention
- Project-specific helper scripts and small utilities that agents may create or run must live under `.codex/tools/**` at the project root.
  - Prefer simple, composable, idempotent scripts (bash/python) with no hidden state.
  - Agents should invoke them via relative paths (e.g., `./.codex/tools/<tool>.sh`) and avoid placing tools elsewhere.
  - Any networked tool usage must respect repository/network sandbox settings and project policies.

## Folder Conventions (src, tests, scripts)
- `src/**`
  - Production/runtime code only (libraries, services, CLI entrypoints that ship with the app).
  - Organize by components from `02.design.md` (e.g., `src/api`, `src/reporting`). Keep public interfaces stable and documented.
  - No test data, prototypes, or throwaway scripts. No secrets or environment-specific credentials.
  - Keep configuration injectable (env vars, config files) and avoid global hidden state.
- `tests/**`
  - All automated tests. Mirror `src/**` structure where practical.
  - Split by type using markers/directories: unit (default), integration (`-m it` per `AGENTS.md`), and optional e2e.
  - Include fixtures under `tests/fixtures/**`. Keep tests deterministic; avoid real network/IO unless explicitly marked as integration.
  - Do not place test helpers in `src/**`; keep them under `tests/_utils/**` or similar.
- `scripts/**`
  - Developer/CI utilities (install, lint, format, local setup, codegen, data seeding, migrations wrappers).
  - Not imported by production code; safe to run locally and in CI. Prefer idempotent, parameterized scripts with `--help`.
  - If a script is intended for agent use during runs, prefer `.codex/tools/**` instead (see above).

## Spec Conventions
- Front-matter: YAML with stable keys (see schemas)
- Fingerprints required: story_fingerprint, design_fingerprint
- .codex/spec/03.tasks.md is derived; planners rebuild it (do not hand-edit)
- Status transitions: story draft→ready→planned→in_progress→done (blocked side-state); task ready→in_progress→review→done (blocked|needs_update|superseded side-states)
