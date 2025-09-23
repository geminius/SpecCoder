# Spec‑Driven Codex Agentic Framework — End‑to‑End Design (v1g4‑ready)

A prompt‑only, **spec‑first** framework that makes coding operate like product management. It uses **Markdown files + Codex CLI prompts**; no servers, no DSLs. All state is in the repo, so agents are **stateless** and can be run **in any session**, with **zero parameters** and **no GitHub required** (local‑only works end‑to‑end).

> **Constraints honored**
> 1) **Zero parameters at runtime** — every agent self‑selects targets deterministically.  
> 2) **Local‑only before any commits** — full Story→Design→Task→Build→Test→Review→Integrate loop works without GitHub or even a commit; Integrator records **shadow lineage**.

---

## 1) File/Folder Layout & Precedence

### User level (global)
```
~/.codex/
├── AGENTS.md                  # global defaults, selection rules, guardrails
├── prompts/                   # agent prompt contracts (00..06)
└── schemas/                   # default templates (requirements/design/task/tasks_list)
```

### Project level (per repo)
```
repo/
├── AGENTS.md                  # project overrides (commands, thresholds)
├── .codex/
│   ├── spec/
│   │   ├── 00.personas.md         # optional Persona Catalog (inline allowed if absent)
│   │   ├── 01.requirements.md     # stories (with story_fingerprint)
│   │   ├── 02.design.md           # architecture (design_fingerprint + policy)
│   │   └── 03.tasks.md            # derived list view (auto‑rebuilt)
│   ├── tasks/                     # one file per task (source of truth)
│   │   └── TASK-001.md
│   ├── trace/
│   │   └── lineage.json           # Integrator‑only: story→task→files/tests→commit_or_shadow
│   ├── runs/                      # per‑agent run logs (gitignored)
│   └── contracts/                 # optional OpenAPI/events
└── src/, tests/, ...
```
**Precedence**: project `AGENTS.md` overrides user `AGENTS.md`. Prompts always load from `~/.codex/prompts/`.

---

## 2) `AGENTS.md` (User‑level) — Canonical Controls

### 2.1 Agent registry
- StoryPlanner: `00_storyplanner.md`
- ArchitecturePlanner: `01_architectureplanner.md`
- TaskPlanner: `02_taskplanner.md`
- Builder: `03_builder.md`
- Tester: `04_tester.md`
- Reviewer: `05_reviewer.md`
- Integrator: `06_integrator.md`
- PRCreator (utility): `07_pr_creator.md`

### 2.2 Schema mapping (authoritative)
- `story`: `~/.codex/schemas/requirements.template.md`
- `design`: `~/.codex/schemas/design.template.md`
- `task`: `~/.codex/schemas/task.template.md`
- `tasks_list_view`: `~/.codex/schemas/tasks_list.template.md`

### 2.3 **Selection precedence** (zero‑parameter, for *all* agents)
1. **Latest `NEXT`** in `.codex/runs/*/*.md` that is still valid (not stale by fingerprint/status).  
2. **Eligible‑set pick** from `.codex/**`, deterministic: order by `priority` (P0→P3), then **numeric id** ascending; ties → **oldest `last_modified_ts`**.  
3. If nothing eligible → print **`INFO: nothing to <agent>`** and exit.

### 2.4 Policies (defaults; project may override)
- `tests_first: true`
- `small_prs: true`
- `auto_spec_chain: false`         # Story→Architect→Task (spec only); Builder stays human‑gated by default
- `auto_post_build_test: false`    # Builder prints NEXT: Tester; can auto‑invoke if true
- `auto_run_next_task: true`
- **Tester gate**: runs **only** when task `status=review` (hard rule; no flag).

### 2.5 Builder chain settings
- `builder.max_tasks_per_run: 3`
- `builder.chain_scope: same_story | same_component | any` (default `same_story`)
- `builder.stop_on: [red_tests, dep_policy_violation, fingerprint_drift, pr_too_large]`
- `builder.timebox_minutes: 30`

### 2.6 Review/Test/Trace policies
- `require_tester: false`  
- `reviewer.block_without_tester: false`  
- `integrator.require_tester_log: false`  
- **Changelog/trace discipline (optional hardening):**
  - `reviewer.block_without_changelog: false`
  - `integrator.require_changelog_entry: false`

### 2.7 Local‑only **shadow integration** (automatic)
- If **no remote**, or **working tree dirty**, or **no new commit created** this run → Integrator switches to **local mode**.  
- `shadow_id = review_baseline_sha` (see Task schema) is recorded in lineage/changelog in place of a commit SHA.  
- Later, if a real commit appears with matching diff hash, Integrator may **reconcile** `shadow_id → commit_sha` (idempotent).

### 2.8 Global guardrails & commands
- Never edit: `infra/**`, `.github/**`, `deploy/**`, `**/*.secrets*`, `**/.env*`, `**/secrets/**`.
- Builder edits only: `src/**`, `tests/**`, `.codex/tasks/**`.
- Commands (override in project): `install`, `lint`, `test`, `test:it`, `coverage_min` (default 80).
- Commit/PR conventions (when VCS is used): title `"[STORY‑ID][TASK‑ID][COMP‑<component>] <summary>"`.

### 2.9 Optional GitHub integration toggle
- Configure under `integrations.github` in project `AGENTS.md`: `enabled` (default `false`), `owner`, `repo`, optional `project_view` + `default_column`, and `sync_policy` (`push_only`, `two_way`, `manual`).
- Sessions may override with `CODEX_GITHUB_ENABLED=0|1` to flip the switch without editing specs.
- When disabled, GitHub-aware agents exit with `INFO` and fall back to the local-only flow.

---

## 3) Schemas (front‑matter)

### 3.0 Persona (optional catalog, `00.personas.md`)
Structure: one section per persona with the following fields.
```
## <Persona Name>
- role: <title / archetype>
- primary_goals: [...]
- pain_points: [...]
- environment: [devices, constraints, compliance]
```
If absent, stories may include inline Persona sections; StoryPlanner can propose catalog entries in `.codex/runs/<ts>/persona_proposals.md`.

### 3.1 Story (blocks inside `01.requirements.md`)
`01.requirements.md` begins with a single-paragraph **Product Vision** summary (purpose, target personas, primary goals), followed by one or more story blocks.
```yaml
id: STORY-012
type: story
status: draft|ready|planned|in_progress|done|blocked
priority: P0|P1|P2|P3
depends_on: []
component_tags: []
tasks_generated: false
story_fingerprint: "sha256:…"
kind: feature|refactor|hotfix   # aids policy/selection
```
Sections:
- User Story (required): "As a <persona>, I want to <do something> so that <meet goal>." (persona referenced by name)
- Motivation
- Acceptance (testable bullets aligned to the goal)
- NFR
- Out of Scope (optional)
- Outcome Measures (optional)

Persona definitions live in the optional catalog `00.personas.md`. If the catalog is absent, StoryPlanner accepts inline details during intake but should log proposals to backfill the catalog.

### 3.2 Design (`02.design.md`)
```yaml
status: draft|ready
design_fingerprint: "sha256:…"
quality_budgets: { api_p95_ms: 200, web_ttfb_ms: 300 }
dependency_policy: { allowed: {}, forbidden: [] }
components: [{ id: <name>, owner: TBD, public_interfaces: [] }]
```

### 3.3 Task (`.codex/tasks/TASK-###.md`)
```yaml
id: TASK-001
type: task
status: ready|in_progress|review|done|blocked|needs_update|superseded
priority: P0|P1|P2|P3
story_id: STORY-012
component: <component>
artifacts: ["src/...","tests/..."]
assignee: null
story_fingerprint: "sha256:…"
design_fingerprint: "sha256:…"
superseded_by: null
# Added for local‑only & deterministic review
artifact_fingerprints: {}         # path -> sha256(content) at time of "review"
review_baseline_sha: ""           # sha256 over sorted artifact_fingerprints
# GitHub linkage (optional; populated when integrations.github.enabled=true)
github:
  issue_number: null
  issue_url: ""
  project_item_id: ""
  last_remote_updated_at: ""
  last_local_sync_ts: ""
  status_snapshot_sha: ""        # hash of remote title/body/status
  pending_update: false
  sync_notes: []
# Tester metadata (optional)
tester_pass: null                  # true|false|null
last_test_run_ts: null
```
Sections: Scope, Test Plan, Rollback.

### 3.4 Derived list (`03.tasks.md`)
Human‑readable backlog (checkbox list), rebuilt from `.codex/tasks/*.md` — **do not hand‑edit**.

---

## 4) Status Lifecycles & Fingerprints

**Story:** `draft → ready → planned → in_progress → done` (side state: `blocked`).  
**Task:** `ready → in_progress → review → done` (side: `blocked | needs_update | superseded`).

- **Fingerprints** (story/design) are embedded in tasks. On drift:
  - `ready` → `needs_update` (TaskPlanner will supersede)
  - `in_progress|review` → `blocked` (prevents stale merges)
- **Builder** refuses tasks with fingerprint mismatch.

---

## 5) Agents (prompts) — Zero‑parameter, stateless

> Each agent obeys the **Selection precedence** (NEXT → eligible set → INFO). Every run ends with exactly one of: **`NEXT: …`**, **`BLOCKED: …`**, or **`INFO: …`** in its run log under `.codex/runs/<ts>/`. All steps are idempotent.

### 5.1 StoryPlanner (`00_storyplanner.md`)
**Role**: Seed or augment specs from feature needs using a persona‑first, outcome‑driven approach; bootstrap `.codex/*`.

- **Preflight**: create `.codex/{spec,tasks,trace,runs,contracts}` if missing; do not copy schemas into the project. If `00.personas.md` exists, load it for matching; otherwise accept inline personas.
- **Interactive modes**: New story (default), Update existing story, Merge stories, Bootstrap from scratch, Scan codebase and propose stories (non‑destructive), Cancel.
- **Flow (New/Update)**:
  1) Persona check → match against catalog by name/role/goals; if no match and catalog exists, propose an addition (do not auto‑write). If no catalog, validate inline persona and log a proposal to `.codex/runs/<ts>/persona_proposals.md`.
  2) Outcome framing → clarify the “so that …” outcome as an observable goal.
  3) Draft the User Story: "As a <persona>, I want to <capability> so that <outcome>."
  4) Acceptance criteria → 3–7 specific, testable bullets aligned to the outcome; include success, boundary, and one negative/permission case.
  5) NFR alignment → map to design budgets (latency, availability, accessibility, security).
  6) Scope shaping → explicitly mark Out of Scope to defer nice‑to‑haves.
  7) Duplicate/overlap detection → compare normalized triplet (persona, capability, outcome) and tags; if similar, propose update/merge instead of adding.
  8) Dependency/component hints → derive `depends_on` conservatively and `component_tags`.
  9) Status and metadata → set `status=ready` (or `draft` if insufficient detail), compute `story_fingerprint`, `tasks_generated=false`, default `priority=P2` (P0 for `kind=hotfix`).
- **Merge mode**: move sections from source stories to a target; mark sources `done` with a body note "superseded by <TARGET>"; recompute fingerprints.
- **Bootstrap mode**: if specs are missing/empty, scaffold `01.requirements.md` and `02.design.md`; seed draft stories from PRD; prompt for persona selection; prefer `status=draft`.
- **Scan mode**: heuristically mine code/tests/TODOs to draft candidates; write proposals to `.codex/runs/<ts>/story_backfill_proposals.md` and inline draft stories only if explicitly approved.
- **Outputs**: `01.requirements.md` updated; optional proposals under `.codex/runs/<ts>/*proposals.md`; ensure `02.design.md` exists (`status=draft` if new); run log.
- **NEXT**: `ArchitecturePlanner` if any story is `ready`; else `INFO`.

StoryPlanner also manages the Product Vision paragraph:
- On bootstrap or when explicitly selected, it inserts/edits a single-paragraph vision at the top of `01.requirements.md` below the main header.
- This section is not fingerprinted per story; it is informational and should remain concise and stable.

### 5.2 ArchitecturePlanner (`01_architectureplanner.md`)
**Role**: Make design **ready** (components, interfaces, budgets, dependency policy).

- **Preflight**: recompute `design_fingerprint`; ensure components/interfaces exist for stories (prioritize `ready|planned`; include `draft` to raise Open Questions); update budgets/policy.
- **Steps**: normalize `component_tags` → add/adjust public interfaces → update `dependency_policy`/budgets → set `status=ready` if prerequisites satisfied; else keep `draft` + Open Questions. Log.
- **Output**: updated `02.design.md`, optional `contracts/openapi.yaml`, run log.
- **NEXT**: `TaskPlanner` if `design=ready`; else `BLOCKED` with questions.

### 5.3 TaskPlanner (`02_taskplanner.md`)
**Role**: Turn eligible stories into **1–3** small tasks each; tests‑first.

- **Preflight**: require `design.status=ready`. Select stories where `tasks_generated=false` or tasks are stale by fingerprints.
- **Steps**: supersede stale `ready/needs_update` tasks → create fresh tasks with fingerprints → set story `tasks_generated=true` and `status=planned` → rebuild `03.tasks.md` → log.
- **Output**: `.codex/tasks/*.md`, updated specs, run log.
- **NEXT**: `Builder` if any task `ready`; else INFO.

### 5.4 Builder (`03_builder.md`)
**Role**: Implement the next `ready` task via TDD; minimal diffs.

- **Selection**: first `ready` task matching current fingerprints/policy.
- **Steps**:  
  1) **Claim** → set task `status=in_progress`; set `assignee`; log claim.  
  2) **Story flip** (idempotent) → if no other tasks for the same story are `in_progress|review`, set that story `status=in_progress`.  
  3) Write failing tests → run red.  
  4) Implement code in `artifacts` → lint/unit/it → green.  
  5) **Move to review** → update task `status=review`; compute and store `artifact_fingerprints` + `review_baseline_sha`; append mini‑changelog.  
  6) Prepare PR body text (even if no PR yet) in `.codex/runs/<ts>/builder.md`.  
  7) Refresh `03.tasks.md` if needed.
- **Output**: code + tests; task in `review`; builder run log.
- **NEXT**: `Tester` (auto‑invoke if `auto_post_build_test=true`).
- **Stops**: `red_tests`, `dep_policy_violation`, `fingerprint_drift`, `pr_too_large`.

### 5.5 Tester (`04_tester.md`)
**Role**: System/integration testing against acceptance.

- **Gate**: **only runs when task `status=review`**. If not, print `BLOCKED: task not in review` and exit without writing results.
- **Steps**: add/verify integration tests; run full suite; compute coverage ≥ `coverage_min`.
  - On **PASS** → emit `.codex/runs/<ts>/tester.result.json` (status PASS, coverage, scenarios); optionally stamp task `tester_pass=true`, `last_test_run_ts`. **Leave status = review**.
  - On **FAIL/coverage shortfall** → set task `status=blocked` + Repro/Notes; emit results (FAIL) + tester log.
- **Output**: tests, tester result/log.
- **NEXT**: `Reviewer` on PASS; `BLOCKED` otherwise.

### 5.6 Reviewer (`05_reviewer.md`)
**Role**: PR checklist, DoD & policy checks. Works **with or without** GitHub.

- **Preflight**:  
  - If `reviewer.block_without_tester` or `require_tester` and no PASS result → set task `blocked` with reason and stop.  
  - **Orphan diff** detection (local‑only or PR): if working changes touch `src/**` or `tests/**` not listed in any task’s `artifacts`, **auto‑create** `TASK-RETROFIT-###.md` (P1) and print `BLOCKED: orphan diff → created retrofit task`.
- **Steps**: DoD checks (IDs, docs, tests, coverage); dependency‑policy checks; basic perf/API sanity; log recommendations. If critical issues → set task `blocked` with reason.
- **Output**: reviewer log; possible task status change to `blocked`.
- **NEXT**: `Integrator` when clean; else `BLOCKED`.

### 5.7 Integrator (`06_integrator.md`)
**Role**: Merge/finish safely; update traceability & changelog. Supports local-only shadows and optional GitHub issue sync.

- **Local/Remote detection** (automatic, no flags):  
  - If no remote/PR, or no new commit was created, or tree is dirty → **local mode**. Else **VCS mode**.
- **Preflight**: enforce `integrator.require_tester_log/require_tester` if enabled; block on FAIL/missing. When GitHub integration is on, require authenticated `gh`; if CLI/auth unavailable, flag affected tasks (`github.pending_update=true`), emit `INFO: github sync skipped`, and continue with local bookkeeping.
- **GitHub reconciliation (if enabled)**:  
  1) Batch-refresh tracked issues (`gh issue view`, cache under `.codex/trace/github_cache.json`).  
  2) Compare remote state to `github.status_snapshot_sha`: missing issues → set task `status=blocked` with reason "github issue missing" and note in `github.sync_notes`; remote closures with matching fingerprints → safe to complete locally; closures with drift → set `blocked`, log drift.  
  3) Remote reopen/retitle/comment updates refresh `status_snapshot_sha` and set `github.pending_update=true` when local follow-up is required.  
  4) Respect `sync_policy`: `manual` records drift only; `push_only`/`two_way` queue close/reopen/comment/project actions for the push step.
- **Steps**:  
  1) Reconcile any `shadow:<hash>` lineage entries when real commits now exist (idempotent; no status flips).  
  2) For each task in `review` with gates satisfied:  
     • **VCS mode**: require merged PR; capture real `commit_sha`.  
     • **Local mode**: compute `shadow_id = review_baseline_sha`.  
     Append lineage entry (story→task→files/tests→`commit_or_shadow`).  
  3) Flip task `review → done`; if all story tasks are `done`, flip story `in_progress → done`.  
  4) Refresh `03.tasks.md`.  
  5) Update `CHANGELOG.md` (include `commit_sha` *or* `shadow:<hash>`).  
  6) **GitHub push (if enabled & policy allows)**: apply queued close/reopen/project moves (`gh project item-move`), add story cross-links/comments, update issue bodies as needed, then clear `github.pending_update`, stamp `last_local_sync_ts`, recompute `status_snapshot_sha`.  
  7) Write integrator run log summarizing status flips and sync results.
- On network/auth failure during step 6, leave `github.pending_update=true`, append details to `github.sync_notes`, and finish local tasks so the run remains idempotent.
- **Output**: lineage/changelog updates; statuses flipped; GitHub issues/project items synchronized when possible; drift logged otherwise.
- **NEXT**: end of chain.

### 5.8 GitHubIssueCreator (`08_githubissuecreator.md`)
**Role**: Materialize `.codex/tasks` entries as GitHub issues (and refresh metadata) when integration is enabled.

- **Selection**: tasks in `ready|in_progress|review` with missing `github.issue_number`, or with `github.pending_update=true`.
- **Preflight**: compute effective toggle (spec flag XOR env override). If disabled → `INFO`. Run `gh auth status` first (do not auto-login). Missing `repo`/`project` scopes or auth failure → `BLOCKED: gh not authenticated` with instructions to run `gh auth login --scopes repo,project`. Ensure project `AGENTS.md` has an `integrations.github` block; if missing, append the template and emit `BLOCKED: github integration not configured`. If the block exists but `owner`/`repo` are empty, emit `BLOCKED: github repo not configured` and ask the user to populate them before rerunning.
- **Steps**:  
  1) Build context: load story title, gather Scope/Test Plan excerpts, derive labels (`story/<story_id>`, `component/<component>`, `priority/P#`, plus status label with hyphenated state).  
  2) Determine action: for existing issues call `gh issue view --json number,url,updatedAt,state,title,body` (404 → recreate; hash drift → note in `github.sync_notes` and leave `pending_update=true`).  
  3) Compose body via `mktemp` (Summary, Story link, Scope, Acceptance/Test highlights, Open Questions, Local Status). Use `gh issue create` for new issues or `gh issue edit` + follow-up `gh issue view` for refresh; update `issue_number`, `issue_url`, `last_remote_updated_at`.  
  4) Project sync (optional): add missing cards with `gh project item-add`, move to status-mapped column via `gh project item-move`, store `project_item_id`.  
  5) Update snapshot/timestamps: compute `status_snapshot_sha`, set `last_local_sync_ts`, clear `pending_update` if successful, append concise `github.sync_notes` entry.  
  6) Persist task file and append a run log entry (`.codex/runs/<ts>/github_issue_creator.md`).
- **Output**: task metadata updated with GitHub linkage; run log noting created/refreshed issues.
- **NEXT**: `INFO` (agent does not auto-chain).

### 5.9 PR Creator (utility) (`07_pr_creator.md`)
**Role**: Commit current changes and open a ready‑for‑review PR via GitHub CLI. Optional; does not affect the Story→Design→Task→Build→Test→Review→Integrate chain.

- **Preflight/Guardrails**:
  - Require GitHub CLI installed and authenticated (`repo` scope). Else `BLOCKED: gh not installed/authenticated`.
  - Require a reachable remote (e.g., `origin`). Else `BLOCKED: no remote`.
  - Determine base branch from `origin/HEAD` (fallback `main`).
  - Enforce forbidden paths: if changes touch `infra/**`, `.github/**`, `deploy/**`, `**/*.secrets*`, `**/.env*`, `**/secrets/**` → `BLOCKED: forbidden path changes`.
  - Advisory checks: small PR hint if very large; optional lint/test runs may block if project policy demands.
- **Steps**:
  1) Derive title/body:
     • Title follows convention `[STORY-ID][TASK-ID][COMP-<component>] <summary>` when a single task in `review|in_progress` matches changed `artifacts`; else falls back to a concise `chore: …`.
     • Body prefers the latest `.codex/runs/<ts>/builder.md`; otherwise auto‑generates sections: Summary, Motivation (from matching story), Details, Scope (from task), Testing (includes Tester PASS/coverage if available), Files Changed, and a draft Changelog line.
     • Save to `.codex/runs/<ts>/pr_body.md`.
  2) Branch: use task‑based naming if matched (e.g., `task/<TASK-ID>`), else `chore/auto-pr-<ts>`; `git checkout -B <branch>`.
  3) Commit: `git add -A`; if changes staged, `git commit -m "<derived title>"`.
  4) Push: `git push -u origin <branch>`.
  5) PR: if branch already has a PR, ensure `ready` state; else `gh pr create --base <base> --head <branch> --title <title> --body-file <body>`.
     • If configured, request reviewers from `reviewer.request_reviewers`.
- **Output**: PR URL; `.codex/runs/<ts>/pr_body.md` written. Prints terminal line `NEXT: PR created/updated and ready for review` (or `BLOCKED/INFO` with reason).

---

## 6) Scenario Coverage (no exceptions)

| Scenario | Supported Path |
|---|---|
| **New feature** | StoryPlanner → ArchitecturePlanner → TaskPlanner → Builder → Tester → Reviewer → Integrator |
| **Modify feature via Codex/spec** | Edit story/design → fingerprints drift → TaskPlanner supersedes → Builder refuses stale → normal flow |
| **Manual spec edits** | Same as above; self‑heals via fingerprints |
| **Manual code edits (no task)** | Reviewer auto‑creates **retrofit task**; blocks until built/tested/integrated |
| **Add new source files** | Treated as orphan diff → retrofit task |
| **Hotfix** | `story.kind=hotfix`, P0, one‑task flow; ArchitecturePlanner can backfill later |
| **Parallel work** | Deterministic selection (priority,id,age) prevents ambiguity; small PRs limit risk |
| **Reruns/new sessions** | Stateless agents read specs/tasks/logs; consistent via selection precedence |
| **No GitHub / no commits** | Full loop works locally; Integrator records **shadow lineage** and flips statuses |
| **GitHub issue mirroring** | Toggle on: GitHubIssueCreator creates issues, Integrator reconciles status/boards; toggle off or offline: agents defer with `INFO` and keep work local |

---

## 7) Determinism & Idempotency Rules
- Agents must be rerunnable without side effects. Re‑emitting the same output is OK; duplicating entries is not.
- Only advance statuses forward (or set `blocked` with explicit reason). Never auto‑reopen to earlier states.
- Every run produces a log with a single terminal line: **`NEXT:`**, **`BLOCKED:`**, or **`INFO:`**.

---

## 8) Safety & Guardrails
- Enforce `dependency_policy` on every Builder/Reviewer run.
- Never touch forbidden paths; Builder edits only allowed areas.
- Respect `tests_first`, `small_prs`, and coverage thresholds.

---

## 9) Why this design
- **Spec‑first + fingerprints** keeps code aligned with intent and makes manual edits safe.  
- **Stateless agents + deterministic selection** allow running **any agent, any time** with **zero parameters**.  
- **Shadow lineage** enables complete local workflows before any commit/PR, and reconciles later when VCS state exists.
