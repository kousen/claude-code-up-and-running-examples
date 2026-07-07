# ch08 mockhub 39 order review plan

Date captured: 2026-05-26

Working directory:

```text
~/Documents/AI/mockhub
```

Prompt:

```text
Use the working spec from the previous capture for MockHub issue #39,
subitem "Order review step with itemized breakdown before payment."

Plan the smallest useful first increment for the review-step subitem.
Identify the blast radius: which frontend files, which backend files,
which tests need to change. Name any cross-cutting concerns (routing,
state, validation, evidence).

Do not implement yet and do not make file changes in this phase. Produce
a concise plan that can be approved before implementation.
```

Output:

```text
★ Insight ─────────────────────────────────────
- The current `CheckoutPage` already renders an `OrderReview` panel and a `Payment Method` panel side-by-side. The subitem from #39 reframes this as a *sequenced step*, not new functionality — the user explicitly confirms the review before payment becomes interactable.
- Backend already exposes everything we need: `Cart.subtotal` plus per-item `currentPrice`, and `OrderService` computes a 10% service fee that matches the frontend's `SERVICE_FEE_RATE` constant. No DTO change required for the minimum increment.
- The Stripe flow's existing `stripeReady`/`isMockProcessing` guards (CheckoutPage.tsx:125) are the precedent for "once payment has started, the cart is gone so we can't go back" — the new step state has to respect that same constraint.
─────────────────────────────────────────────────

## Plan: Order review step with itemized breakdown (first increment)

### Goal
Promote the existing inline review panel into an explicit **Step 1: Review → Step 2: Payment** flow inside `CheckoutPage`, with a clearer itemized breakdown. No new routes, no backend changes. This is the smallest standalone slice of #39's review-step subitem; the sibling "progress indicator" subitem can layer on top later.

### Blast radius

**Frontend (modified)**
- `frontend/src/pages/CheckoutPage.tsx` — introduce a `step: 'review' | 'payment'` local state. On 'review', show only the `OrderReview` panel + a "Continue to Payment" CTA. On 'payment', show the Payment Method panel with a "Back to Review" link (disabled once `stripeReady || isMockProcessing`).
- `frontend/src/components/checkout/OrderReview.tsx` — enrich the breakdown: per-item line (event + section/row/seat + price), subtotal, service fee (10%), total. Today it delegates entirely to `CartItem` + `CartSummary`; we likely want a dedicated itemized layout instead of re-using cart components, so the review reads like an invoice rather than a cart.
- `frontend/src/components/cart/CartSummary.tsx` — leave untouched (still used by `CartPage` + drawer). Avoid coupling review breakdown to the cart summary.
- (Optional, deferred) `frontend/src/lib/constants.ts` — extract `SERVICE_FEE_RATE` so backend/frontend are documented in one place. Not required for this increment.

**Frontend (new)**
- `frontend/src/components/checkout/OrderReview.test.tsx` — new component test for the itemized breakdown (subtotal/fee/total rendering, line items, edge cases like price-changed badge).

**Frontend (tests modified)**
- `frontend/src/pages/CheckoutPage.test.tsx` — the existing "renders order review with cart items" assertion still holds, but we add tests for:
  - Step 1 shows review only, payment tabs hidden/inactive.
  - Clicking "Continue to Payment" reveals payment tabs.
  - "Back to Review" works pre-payment.
  - "Back to Review" is hidden once `stripeReady` / `isMockProcessing`.

**Backend**
- No changes. `Cart` DTO already carries everything; `OrderService` already computes the 10% fee server-side; no new endpoints.

**E2E**
- `frontend/e2e/` — defer to a later increment. Existing checkout E2E (if any) will need its selector updated once we introduce the step gate; can be folded in when the progress indicator subitem lands.

### Cross-cutting concerns
- **Routing**: keep `/checkout` as a single route; step is local component state. URL-driven step (`?step=review|payment`) would survive refreshes but adds query-param coupling and is unnecessary for the first increment. Flagging it as a follow-up if users complain about losing state on refresh.
- **State / Stripe interaction**: once `stripeReady || isMockProcessing` is true, the cart has been cleared server-side; the step must lock to 'payment' and the "Back to Review" affordance must hide. Reuse the existing flag — don't introduce parallel state.
- **Validation**: server-side checkout already re-validates listings at mutate time. No new client validation. `CartItem`'s existing `priceChanged` badge already surfaces drift between add-time and review-time prices and should remain visible on the review step.
- **Evidence**: agent purchase evidence (per `AgentPurchaseApproval`) is for the agentic/MCP path, not the web UI. No evidence wiring touches this slice.
- **Accessibility**: "Continue to Payment" / "Back to Review" need accessible names; if/when the progress indicator lands, `aria-current="step"` on the active step is the standard pattern.
- **Service fee parity**: client uses `SERVICE_FEE_RATE = 0.10`, backend uses `OrderService.SERVICE_FEE_RATE = 0.10`. The new itemized breakdown will display the fee — we should keep both literals in lockstep. Worth a short comment on the frontend constant referencing `OrderService.java:50` (one of the few cases where the cross-file pointer is justified).

### Out of scope for this increment
- Progress indicator (`cart → review → payment → confirmation`) — separate #39 subitem.
- Mock payment form polish (card-number formatting, expiry, CVC) — separate subitem.
- Confirmation page CTAs — separate subitem.
- Backend itemization endpoint (e.g., returning `serviceFee` on the cart DTO) — not needed yet; revisit if frontend/backend fee constants drift.

### Suggested learning-mode contribution point
Once approved, the place where your judgment most shapes the feature is the **step-state guard logic** in `CheckoutPage.tsx`: the rule for *when* the user is allowed to go back to review (pre-mutation only) and *what* happens to the payment-method tab selection if they do. A ~6-line `canReturnToReview` predicate + the back-button handler is a natural 5–10 line slot to hand off, since it's the trade-off between "let users freely toggle" and "don't let them desync from server state once the order has been created."

Ready for your review — should I proceed to implementation, or would you like to adjust scope (e.g., bundle in the progress indicator, or push the itemized rendering further)?

```
