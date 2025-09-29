Summary:
Refresh docs, prompts, and configs so the GitHub integration flows entirely through the MCP server and demo project settings.

Motivation:
Keep the sample repo and prompts aligned with the MCP-based GitHub integration so local workflows and guardrails stay consistent.

Details:
- README and end-to-end design capture GitHub MCP setup, toggles, guardrails, and integration policy.
- Demo AGENTS/config files add GitHub tool mappings, sample task metadata, ignore rules, and required dependencies.
- Updated prompts (Builder/Reviewer/Integrator/PR Creator/IssueCreator) to call MCP tools and block local fallbacks.

Testing:
- Not run (docs and prompt updates only).

Files Changed:
- README.md (M)
- demo_repo/.codex/runs/20250923T061230Z/githubissuecreator.md (A)
- demo_repo/.codex/runs/20250925T113837Z/github_issue_creator.md (A)
- demo_repo/.codex/runs/20250925T150553Z/github_issue_creator.md (A)
- demo_repo/.codex/runs/20250925T151051Z/github_issue_creator.md (A)
- demo_repo/.codex/runs/20250925T164730Z/github_issue_creator.md (A)
- demo_repo/.codex/runs/20250925T171132Z/pr_body.md (A)
- demo_repo/.codex/runs/20250929T151445Z/github_issue_creator.md (A)
- demo_repo/.codex/runs/20250929T151445Z/pr_body.md (A)
- demo_repo/.codex/spec/03.tasks.md (M)
- demo_repo/.codex/tasks/TASK-002.md (M)
- demo_repo/.codex/tasks/TASK-003.md (M)
- demo_repo/.codex/tasks/TASK-004.md (A)
- demo_repo/.gitignore (A)
- demo_repo/AGENTS.md (M)
- demo_repo/requirements.txt (A)
- spec_driven_codex_agentic_framework_end_to_end_design_v_1.md (M)
- user_dot_codex/AGENTS.md (M)
- user_dot_codex/prompts/03_builder.md (M)
- user_dot_codex/prompts/04_tester.md (M)
- user_dot_codex/prompts/05_reviewer.md (M)
- user_dot_codex/prompts/06_integrator.md (M)
- user_dot_codex/prompts/07_pr_creator.md (M)
- user_dot_codex/prompts/08_githubissuecreator.md (A)
- user_dot_codex/schemas/task.template.md (M)

Changelog (draft):
- n/a: update GitHub integration prompts and docs (docs-only change).
