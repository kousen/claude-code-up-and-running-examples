# MockHub Claude Code connector checkout

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
