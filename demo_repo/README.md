# Demo Project — v1g4 zero-parameter, local-only

This repo shows a **complete flow** without GitHub or commits. You can start any agent in a fresh session and it will select the next step deterministically:

- `.codex/runs/*` contains the NEXT trail from StoryPlanner → Integrator.
- `.codex/spec/*` holds the final specs; `.codex/tasks/TASK-001.md` includes fingerprints and `status: done`.
- `.codex/trace/lineage.json` records a **shadow** reference (no commit) using `review_baseline_sha`.
- `CHANGELOG.md` includes a human-readable entry with the shadow id.
- `src/` and `tests/` contain the tiny demo implementation.

Selection invariants (no parameters):
1) Latest NEXT in `.codex/runs/*` if still valid
2) Else first eligible by priority (P0→P3), then id asc, then oldest mtime
3) Else print INFO and exit

## Interactive Menus
Agents now open with a small first-turn menu (zero parameters). Defaults to the first option.

- StoryPlanner: New story, Update, Merge, Bootstrap, Scan/propose, Cancel
- ArchitecturePlanner: Make ready, Update components/interfaces, Update policy, Update budgets, Contracts, Analyze questions, Cancel
- TaskPlanner: Plan eligible, Regenerate specific, Supersede only, Rebuild list, Cancel
