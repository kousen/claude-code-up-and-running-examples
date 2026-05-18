# mockhub

The "skyscraper" project — a larger application used to demonstrate
skills, sub-agents, MCP servers, and full prompt-to-PR workflows.

The MockHub application itself lives at
<https://github.com/kousen/mockhub> — a Spring Boot + Spring AI backend
with React components on the front end, built with Gradle. This folder
holds **the artifacts the book builds *around* it**: skills, sub-agent
definitions, MCP configurations, headless scripts, and captured workflows.

To work through Ch. 6–9, clone MockHub separately and point Claude Code
at it; the artifacts here are designed to be dropped into or referenced
from that working tree.

## Chapter phases

| Folder | Chapter | Artifacts |
| --- | --- | --- |
| `ch06-skills/` | Ch. 6 — Skills, Sub-agents, Agent Teams | PR-readiness skill, sub-agent definitions |
| `ch07-mcp/` | Ch. 7 — MCP and External Integrations | MockHub as an MCP server |
| `ch08-prompt-to-pr/` | Ch. 8 — From Prompt to Pull Request | Issue → plan → PR workflow, headless scripts |
| `ch09-review-testing/` | Ch. 9 — Review, Testing, Debugging | Review prompts, recovery patterns |
