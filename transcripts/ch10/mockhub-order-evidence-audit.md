# ch09 mockhub order evidence audit

Date captured: 2026-05-24

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples
```

Prompt:

```text
Use only the authenticated claude.ai MockHub MCP connector from Claude Code.

This is a read-only evidence-audit capture for Chapter 11. Do not use curl,
browser scraping, source-code inspection, direct REST endpoints, or local
database access. Do not create mandates, issue payment credentials, add or
remove cart items, clear the cart, propose or approve purchases, checkout,
confirm orders, revoke mandates, revoke credentials, or otherwise mutate
MockHub state.

Audit order MH-20260524-0004 for buyer@mockhub.com.

Use only read-only MockHub MCP tools. Retrieve the purchase evidence, risk
summary, order status if useful, and payment credential status if available
through read-only tools.

Explain what each artifact proves and what it does not prove. Keep the output
concise and suitable for later Chapter 11 drafting.

If a required read-only tool is missing or if any requested information would
require a mutation, stop and report the exact boundary.
```

Output:

```text
# Audit: MH-20260524-0004 — buyer@mockhub.com

**Order summary.** CONFIRMED, $30.63 + $3.06 fee = **$33.69**, paid via mock `paymentIntentId` `mock_pi_7ad997cc…`. One ticket: The Spinners, Hollywood Casino Gulf Coast, Upper Level Row B Seat 6, event 2026-08-16. Agent `agent-sandbox-checkout-001`, mandate `927fb7fd…`.

## Read-only artifacts gathered

| Artifact | Tool | Key fields |
|---|---|---|
| Purchase evidence bundle | `getAgentPurchaseEvidence` | mandate, approval, scoped credential, checkout, fulfillment, risk signals, eval outcomes, actor timeline |
| Order record | `getOrder` | status=CONFIRMED, totals, items, agent + mandate IDs |
| Agent risk summary | `getAgentRiskSummary` | 3 signals, all INFO; blocked=false |
| Payment credentials list | `listPaymentCredentials` | credential `285e12b1…` CONSUMED by this order |

## What each artifact proves — and what it does not

**1. Mandate (`927fb7fd…`, scope=PURCHASE, max $40/txn, allowed=concerts/the-spinners-tm-1561/Upper Level, approvalMode=APPROVAL_REQUIRED).**
- Proves: user pre-authorized the agent within a bounded budget and narrow scope; the $33.69 order fits inside `maxSpendPerTransaction` and the category/event/section allowlist; status now REVOKED at 18:11:00, after the order, with $6.31 of $40 remaining.
- Does not prove: that the revocation was intentional vs. cleanup; that scope was tight enough policy-wise (only that it matched).

**2. Purchase approval (`e2d43321…`, status=COMPLETED).**
- Proves: human-in-the-loop step happened — agent proposed at 18:10:24, user approved at 18:10:29 (5s later), completed at 18:10:37 against this exact order. Snapshot of proposed total matches the final total.
- Does not prove: which UI/channel the user used to approve, or that the human actually read the proposal — only that an approval event was recorded for `buyer@mockhub.com`.

**3. Scoped payment credential (`285e12b1…`, ONE_TIME, max $40, merchant=MOCKHUB).**
- Proves: a single-use, agent-scoped, merchant-restricted credential was issued *before* checkout (18:10:03), CONSUMED at 18:10:36 by this order, and cannot be reused (`consumedByOrderNumber=MH-20260524-0004`). `listPaymentCredentials` independently confirms CONSUMED status — no orphan or duplicate credentials for this agent.
- Does not prove: that real funds moved; `backingPaymentMethod=mock` and `paymentMethod=mock` — this is sandbox settlement, not a real PSP authorization.

**4. Checkout record (`acpStatus=COMPLETED`, `agentInitiated=true`).**
- Proves: checkout was flagged as agent-initiated and completed end-to-end with a payment intent reference.
- Does not prove: idempotency protection on this specific call (`idempotencyKey=null`).

**5. Risk signals + agent risk summary.**
- Proves: only 3 INFO signals for this agent in the window (CART_HOLD, CHECKOUT, CONFIRM); highest severity INFO; not blocked; no warning/critical reasons. The `agent-risk` eval rule PASSED for this order's window.
- Does not prove: absence of risk outside the summary window (`since=2026-05-23T18:32:56Z`) or signals on other agents owned by the same user.

**6. Eval outcomes (all 4 PASSED: mandate-authorization, purchase-approval, payment-credential, agent-risk).**
- Proves: MockHub's own deterministic checks validated each control gate against persisted artifacts.
- Does not prove: completeness of the rule set — these are the rules MockHub runs, not a guarantee that no policy gap exists.

**7. Fulfillment block.**
- Proves: ticket PDF is downloadable at `/api/v1/orders/MH-20260524-0004/tickets/283030/download`; ticket not yet scanned; signing key reference recorded.
- Does not prove: email/SMS were actually delivered — both dispatches are `NOT_PERSISTED` by design; only the attempt timestamp is captured.

**8. Actor timeline (10 steps, USER vs. AGENT actors interleaved correctly).**
- Proves: causal ordering — user created mandate → user issued credential → agent added to cart → agent created order → agent proposed → **user approved** → agent consumed credential → agent confirmed → approval completed. No agent-only path bypassed the user gates.
- Does not prove: clock integrity (all timestamps are server-recorded; no external attestation).

## Boundary check

All requested data was retrievable via read-only MCP tools. No mutating tools were invoked, and no required artifact was missing.
```
