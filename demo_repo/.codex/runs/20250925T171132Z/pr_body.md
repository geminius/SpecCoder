Summary:
Refresh docs, prompts, and configs so the GitHub integration flows entirely through the MCP server and demo project settings.

Motivation:
Keep the sample repo and prompts aligned with the MCP-based GitHub integration so local workflows and guardrails stay consistent.

Details:
- README and end-to-end design capture GitHub MCP setup and toggles.
- Demo AGENTS/config files add GitHub tool mappings plus required dependencies.
- Updated prompts (Builder/Reviewer/Integrator/PR Creator/IssueCreator) to call MCP tools and block local fallbacks.

Testing:
- Not run (docs and prompt updates only).

Files Changed:
- M    README.md
- A    demo_repo/.codex/runs/20250923T061230Z/githubissuecreator.md
- A    demo_repo/.codex/runs/20250925T113837Z/github_issue_creator.md
- A    demo_repo/.codex/runs/20250925T150553Z/github_issue_creator.md
- A    demo_repo/.codex/runs/20250925T151051Z/github_issue_creator.md
- M    demo_repo/.codex/spec/03.tasks.md
- A    demo_repo/.codex/tasks/TASK-004.md
- A    demo_repo/.gitignore
- M    demo_repo/AGENTS.md
- A    demo_repo/requirements.txt
- M    spec_driven_codex_agentic_framework_end_to_end_design_v_1.md
- M    user_dot_codex/AGENTS.md
- M    user_dot_codex/prompts/03_builder.md
- M    user_dot_codex/prompts/04_tester.md
- M    user_dot_codex/prompts/05_reviewer.md
- M    user_dot_codex/prompts/06_integrator.md
- M    user_dot_codex/prompts/07_pr_creator.md
- A    user_dot_codex/prompts/08_githubissuecreator.md
- M    user_dot_codex/schemas/task.template.md

Changelog (draft):
- n/a: update GitHub integration prompts and docs (docs-only change).
