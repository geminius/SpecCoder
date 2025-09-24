# Codex Agentic Framework

A spec‑first, prompt‑only workflow that turns product specs into deterministic coding loops — no servers, no hidden state. Agents are stateless and run with zero parameters.

## What’s Inside
- User‑level defaults under `user_dot_codex/` (copy to `~/.codex/`):
  - `AGENTS.md` — policies, selection rules, guardrails
- `prompts/00..06` — StoryPlanner → Integrator agent prompts
- `prompts/07_pr_creator.md` — optional PR creation utility (via MCP)
  - `schemas/` — story, design, task, derived list templates, and a personas catalog template
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
   - StoryPlanner → ArchitecturePlanner → TaskPlanner → Builder → Tester → Reviewer → Integrator
3) No GitHub? Everything still works locally; Integrator records a shadow ID.
4) On GitHub? Use the optional PR flags in `AGENTS.md` or run `07_pr_creator.md` to open a ready‑for‑review PR via MCP with an auto‑generated description.

## Interactive Mode Menus
Agents run with zero parameters but now start with a small, first‑turn menu to make intent explicit. If you provide no selection, they default to the first option.

- StoryPlanner
  - New story (default)
  - Update existing story
  - Merge stories
  - Bootstrap from scratch
  - Scan codebase and propose stories (non‑destructive; writes `.codex/runs/<ts>/story_backfill_proposals.md` and/or draft stories)
  - Cancel

- ArchitecturePlanner
  - Make design ready (default)
  - Update components & interfaces
  - Update dependency policy
  - Update quality budgets
  - Generate/refresh API contracts
  - Analyze and list open questions (log‑only)
  - Cancel

- TaskPlanner
  - Plan tasks for eligible stories (default)
  - Regenerate tasks for specific stories
  - Supersede stale tasks only
  - Rebuild derived list only
  - Cancel

## Story Format (Required)
- User Story: As a <persona>, I want to <do something> so that <meet goal>.
- Acceptance: testable bullets aligned to the goal.
- Persona reference: use a named persona; define personas in the catalog.

## Persona Catalog (Optional)
- File: `.codex/spec/00.personas.md` (see `user_dot_codex/schemas/personas.template.md`).
- StoryPlanner matches stories to catalog personas by name/role/goals. If absent, it accepts inline details during intake and writes proposals to `.codex/runs/<ts>/persona_proposals.md` to backfill the catalog.

## Common Use Cases
- New feature: Plan stories/design → generate small tasks → TDD via Builder → test/review/integrate.
- Existing codebase, add specs: Backfill stories/design; TaskPlanner creates focused tasks; Reviewer catches orphan diffs.
- Hotfix: Mark story `kind: hotfix` (P0); a single focused task; integrate safely.
- Local‑only: End‑to‑end without commits/PRs; Integrator logs shadow lineage.
- GitHub PRs: Use Builder/Reviewer flags or the `07_pr_creator` utility to script draft/ready PRs via MCP.

## More Details
For the full end‑to‑end design and policies, see `spec_driven_codex_agentic_framework_end_to_end_design_v_1.md`.

---

Tip: Project‑level overrides live in your repo’s `AGENTS.md` (see `demo_repo/AGENTS.md` for examples). Forbidden paths and Builder‑editable areas are enforced by guardrails.

## MCP GitHub Setup

- Requirements:
  - A GitHub Personal Access Token with `repo` (and optionally `project`) scopes exported as `GITHUB_PERSONAL_ACCESS_TOKEN`.
  - Node.js with `npx` available (for the MCP GitHub server).

- Configure the MCP GitHub server (recommended via CLI):
  - `codex mcp add github --env GITHUB_TOKEN=$GITHUB_PERSONAL_ACCESS_TOKEN npx -y @modelcontextprotocol/server-github`
  - Verify: `codex mcp list` should show a `github` server with `npx -y @modelcontextprotocol/server-github`.

- Configure Codex (global):
  - Codex reads MCP config from `~/.codex/config.toml`. A minimal manual entry is:
    
    [mcp.servers.github]
    command = "npx"
    args = ["-y", "@modelcontextprotocol/server-github"]
    env = { GITHUB_TOKEN = "$GITHUB_PERSONAL_ACCESS_TOKEN" }

- Configure project integration:
  - In your project `AGENTS.md`, set `integrations.github.enabled: true` and `server_id: github`.
  - Optionally override tool names if your MCP server differs:
    - `integrations.github.tools.issue_get`
    - `integrations.github.tools.issue_create`
    - `integrations.github.tools.issue_update`
    - `integrations.github.tools.project_add_item`
    - `integrations.github.tools.project_move_item`
    - `integrations.github.tools.pr_get`
    - `integrations.github.tools.pr_create`
    - `integrations.github.tools.pr_update`
    - `integrations.github.tools.pr_mark_ready`
    - `integrations.github.tools.pr_request_reviewers`

- Toggle integration per run (optional): set `CODEX_GITHUB_ENABLED=1` (or `0`) in the environment.
