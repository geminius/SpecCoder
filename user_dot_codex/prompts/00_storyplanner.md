# 00_storyplanner — StoryPlanner

## Goal
Seed or augment project specs from feature needs; bootstrap `.codex/*`.

## Preflight
- Ensure `.codex/{spec,tasks,trace,runs,contracts}` exist; create if missing.
- Do NOT copy schemas into project. Render outputs using schema paths from AGENTS.md.

## Inputs
- Interactive Q&A or a feature file path (PRD/bullets).
- User/Project AGENTS.md for conventions and schema paths.

## Selection
Resolve target using Selection precedence (NEXT → eligible set → INFO).

## Steps
1) Intake features; produce vertical user stories with:
   - id: STORY-### (incremental), status=ready, priority=P2, depends_on=[], component_tags=[], tasks_generated=false
   - sections: Motivation, Acceptance (testable bullets), NFR, Out of Scope (optional)
   - compute story_fingerprint
   - Hotfix note: when the feature is a hotfix, set `kind: hotfix` and consider defaulting priority to P0.
2) Ensure `.codex/spec/02.design.md` exists; if missing, render from design schema with status=draft.
3) Append stories to `.codex/spec/01.requirements.md` (dedupe on normalized title).
4) Write run log `.codex/runs/<ts>/storyplanner.md`.

## Output
- `.codex/spec/01.requirements.md` (stories)
- `.codex/spec/02.design.md` (if missing)
- run log only

## NEXT
- If any story is ready: NEXT: run ArchitectPlanner (01_architectplanner.md)
- Else: INFO: no actionable features
