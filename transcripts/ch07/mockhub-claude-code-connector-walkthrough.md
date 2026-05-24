# ch07 mockhub claude code connector walkthrough

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
The MockHub MCP server is connected, but only the OAuth bootstrap tools are currently exposed — `mcp__claude_ai_MockHub__authenticate` and `mcp__claude_ai_MockHub__complete_authentication`. The actual business tools (tickets, mandates, payment, checkout, evidence, risk) will only appear after OAuth completes.

Per your instruction not to substitute curl/REST for MCP, I won't try to call the MockHub API any other way. Two options:

1. **Start the OAuth flow now** — I'll call `authenticate`, you open the URL in your browser, paste the redirected `localhost` URL back, and the real tool surface unlocks. Then I can do the capture as specified.
2. **Stop here** — if "MCP tools not available" means *unauthenticated*, then the literal answer is: the MockHub business tools are not available in this session, so I stop.

Reading your prompt strictly ("Use the connected MockHub MCP connector"), I think option 1 is what you want — the connector *is* connected, it just needs the OAuth handshake. Want me to kick off `authenticate`?

★ Insight ─────────────────────────────────────
- MCP servers can expose a two-stage tool surface: a tiny bootstrap (auth) surface pre-login, and the real domain tools post-login. Claude Code only sees what the server advertises right now, so "the tools aren't there" and "the tools are gated" look identical from the agent side until you complete the handshake.
- The OAuth callback trick here (`http://localhost:<port>/callback?...`) is a common pattern for desktop/CLI MCP clients — the localhost page failing to load is expected; only the URL in the address bar matters, because the `code` + `state` query params are the actual handshake payload.
- Your "no curl, no REST substitutes" rule is exactly the boundary the capture is meant to show: the agent's authority comes from the MCP tool surface, not from being clever about HTTP. If the tool isn't there, the agent shouldn't route around it.
─────────────────────────────────────────────────
```
