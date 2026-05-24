# ch07 mockhub claude code connector checkout

Date captured: 2026-05-24

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples
```

Prompt:

```text
Use only the connected claude.ai MockHub MCP connector from Claude Code.

Do not use curl, browser scraping, source-code inspection, direct REST endpoints,
or local database access as a substitute for MCP tools. Do not use any real
payment method. Use only a mock-backed ONE_TIME payment credential.

Goal: perform a bounded sandbox checkout for buyer@mockhub.com and then clean up
temporary authority.

Required sequence:
1. Briefly confirm the authenticated MockHub business tools are available.
2. Find one inexpensive suitable ticket for buyer@mockhub.com.
3. Read the relevant commerce policy if the listing exposes a policy URL or
   event slug.
4. Create the narrowest useful purchase mandate for that exact event/category/
   section, with APPROVAL_REQUIRED and a max spend just above the total expected
   price.
5. Validate that mandate before changing cart state.
6. Issue a mock-backed ONE_TIME payment credential scoped to the same spend
   limit.
7. Add the ticket to cart, checkout, propose/approve the purchase, and confirm
   the order.
8. Read purchase evidence and risk summary.
9. Clear the cart and revoke the temporary mandate.
10. Show that the payment credential was consumed or revoked; if it remains
    active, revoke it.

Output concise evidence only: selected listing, mandate boundary, mock payment
credential boundary, order number/status/total, approval status, evidence
highlights, risk summary, and cleanup result. If any required tool is missing or
fails, stop and report the exact stopping point.
```

Output:

```text
Payment credential confirmed CONSUMED (no further revoke needed). Full sandbox flow complete.

`★ Insight ─────────────────────────────────────`
This flow demonstrates the agentic-commerce separation of concerns: a **mandate** governs *what an agent may do* (scope, sections, approval mode), a **payment credential** governs *what money it may move* (amount, single-use, merchant). They're separately revocable, and the evidence trail (`actorTimeline`) shows USER vs AGENT actors per step — that's what makes after-the-fact audit defensible.
`─────────────────────────────────────────────────`

## Sandbox checkout — evidence summary

| Item | Value |
|---|---|
| **Listing** | Lady A — `lady-a-tm-1525`, Upper Level, Row F, Seat 8 (listingId 98073) @ $30.62, Freeman Arts Pavilion, 2026-08-29 |
| **Mandate** | `e1db6715-...b62678` — PURCHASE, concerts/lady-a-tm-1525/Upper Level only, $40 cap, APPROVAL_REQUIRED, expires 2026-05-25 |
| **Payment credential** | `caa69c51-...21e98` — mock-backed ONE_TIME, $40 max USD, expires 2026-05-25 |
| **Order** | `MH-20260524-0003` — **CONFIRMED**, subtotal $30.62 + fee $3.06 = **$33.68** |
| **Approval** | `992255a8-...bc81` — status **COMPLETED**, finalOrderNumber MH-20260524-0003 |
| **Evidence rules** | mandate-authorization PASSED · purchase-approval PASSED · payment-credential PASSED · agent-risk PASSED |
| **Risk summary** | 3 INFO signals, 0 warning/critical, not blocked |
| **Cleanup** | Cart cleared ✔ · Mandate **REVOKED** ✔ · Payment credential **CONSUMED** (no revoke needed) ✔ |

```
