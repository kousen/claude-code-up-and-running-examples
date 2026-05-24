# ch07 mockhub claude code connector tool surface

Date captured: 2026-05-24

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples
```

Prompt:

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

Keep the output concise and suitable for quoting in Chapter 7.
```

Output:

```text
Acknowledged — those additional connectors loaded but aren't needed for the MockHub capture. Here is the chapter-ready summary.

---

## MockHub MCP Connector — Read-Only Capture

**Availability:** Yes — the authenticated `claude.ai MockHub` MCP connector is live in this Claude Code session. All tool names are namespaced `mcp__claude_ai_MockHub__*` and require `ToolSearch` to load schemas before invocation.

### Tool Surface (grouped by purpose)

**Discovery (read-only)**
- `getFeaturedEvents`, `searchEvents`, `findTickets` (recommended discovery entry point)
- `getEventDetail`, `getEventListings`, `getListingDetail`, `getFeaturedEvents`
- `compareTickets`, `getPriceHistory`, `getPricePrediction`, `getCalendarEntry`

**Cart & checkout (state-mutating — NOT exercised here)**
- `addToCart`, `removeFromCart`, `clearCart`, `refreshCart`, `getCart`, `checkout`, `confirmOrder`
- `getOrder`, `listOrders`

**Mandates & payment credentials (state-mutating — NOT exercised here)**
- `createMandate`, `validateMandate`, `revokeMandate`, `listMandates`, `getBestMandate`
- `issuePaymentCredential`, `revokePaymentCredential`, `listPaymentCredentials`

**Approvals & risk (state-mutating / sensitive — NOT exercised here)**
- `proposePurchase`, `approvePurchase`, `denyPurchase`, `listPurchaseApprovals`
- `getAgentRiskSummary`, `getAgentPurchaseEvidence`

**Policy**
- `getCommercePolicy`

**MCP resources:** None visible from this connector — only tools are exposed (no `ListMcpResourcesTool` entries appeared for the MockHub server).

### Read-Only Proof Calls

`getFeaturedEvents()` returned a curated catalog including Hamilton at DPAC (Durham), Harry Styles at Wembley, the 2026 World Cup match catalog, Kenny Chesney at the Sphere, JAY-Z at Yankee Stadium, and Tim McGraw's tour — confirming the live data surface.

`findTickets(userEmail="buyer@mockhub.com", maxResults=3)` returned the three cheapest listings keyed to that buyer profile:

| Event | Venue | Section / Row / Seat | Price |
|---|---|---|---|
| Lady A | Freeman Arts Pavilion, Selbyville | Upper Level / F / 8 | $30.62 |
| The Spinners | Hollywood Casino Gulf Coast, Bay St Louis | Upper Level / B / 6 | $30.63 |
| Robert Glasper Experiment | 9:30 Club, Washington | Balcony / B / 11 | $30.65 |

Each listing includes `commercePolicyUrl` — the hook later steps would feed to `getCommercePolicy` before any cart mutation.

### Why This Complements the Protocol-Level Capture

The protocol-level checkout capture (separate artifact) exercises the *full* AP2 mandate → payment credential → checkout flow at the wire level, showing how an agent negotiates a purchase end-to-end. This connector capture instead documents what's reachable from inside Claude Code *as a tool surface* — proving (a) the MCP connector is correctly authenticated and discoverable, (b) the read-only discovery half of MockHub is usable without any mandates or credentials, and (c) the boundary between read-only inspection and state-mutating commerce is cleanly delineated in the tool taxonomy. Together they give Chapter 7 both perspectives: the inert tool catalog a developer sees in Claude Code, and the live protocol exchange that happens when those tools fire.
```
