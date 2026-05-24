# ch07 mockhub claude code console auth walkthrough

Date captured: 2026-05-24

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples
```

Prompt:

```text
Use the connected Claude.ai MockHub MCP connector from Claude Code.

Do not use curl, browser scraping, source-code inspection, or REST endpoints as
a substitute for MCP tools. If the MockHub MCP tools are not available in this
Claude Code session, say exactly that and stop.

First inspect the available MockHub tool surface. Then find one suitable sandbox
ticket for buyer@mockhub.com, create the narrowest useful purchase mandate, use
mock-backed payment authority only, complete the checkout, read the evidence and
risk outputs, and clean up temporary authority when the run is over.

This capture is about Claude Code and MCP boundaries, not selling MockHub:
show the tool surface, authority boundary, mock-payment proof, order evidence,
risk state, and cleanup result.
```

Output:

```text
The MockHub MCP tools are not available in this Claude Code session.

What's exposed here is only the OAuth bootstrap pair (`mcp__claude_ai_MockHub__authenticate`, `mcp__claude_ai_MockHub__complete_authentication`). Calling `authenticate` returns the message:

> "This is a claude.ai MCP connector. Ask the user to run /mcp and select 'claude.ai MockHub' to authenticate."

The functional surface this capture requires — sandbox ticket browse/search, purchase mandate creation, mock-backed payment authority, checkout, order evidence read, risk state read, and authority cleanup — is not registered in this session and won't be until you complete the connector auth on the Claude Code side (`/mcp` → claude.ai MockHub). I won't fall back to curl, the REST API, source inspection, or scraping per your instructions.

Stopping here. Once you've authenticated via `/mcp`, re-run the prompt and the real MockHub tools should show up in the deferred-tool list.
```
