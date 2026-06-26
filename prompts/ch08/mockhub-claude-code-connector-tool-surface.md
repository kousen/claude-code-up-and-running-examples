# MockHub Claude Code connector tool surface

```text
Use the connected claude.ai MockHub MCP connector from Claude Code.

Do not use curl, browser scraping, source-code inspection, direct REST endpoints,
or local database access as a substitute for MCP tools. Do not create mandates,
issue payment credentials, add anything to a cart, approve purchases, checkout,
or mutate MockHub state in any way.

Confirm whether the authenticated MockHub business tools are available in this
Claude Code session. If they are not available, say exactly that and stop.

If they are available, report:
- the visible MockHub tool surface grouped by purpose
- whether MCP resources are visible
- a small read-only proof call that uses MockHub MCP tools, such as featured
  events or ticket search for buyer@mockhub.com
- why this read-only connector capture complements the separate protocol-level
  checkout capture

Keep the output concise and suitable for quoting in Chapter 9.
```
