I have a complete picture. Here are the commit and PR materials.

---

## 1. Commit message (Conventional Commits)

```
feat(checkout): add order review step between cart and payment (#39)

Inserts a dedicated /checkout/review page so buyers see an itemized
breakdown (line items, subtotal, 10% service fee, total) before any
payment method is exposed. /checkout is gated by a sessionStorage
fingerprint of the reviewed cart (id + subtotal + per-item priceAtAdd
and currentPrice) so a fresh cart or any reprice forces a re-review.
The gate is UX scaffolding, not a security control - server-side cart,
pricing, and order validation are unchanged. MCP/ACP checkout shape is
also unchanged.
```

## 2. PR title

```
feat(checkout): order review step before payment (#39)
```

## 3. PR description

```markdown
## Summary

Adds an Order Review step between the cart and the payment page so
buyers confirm an itemized breakdown before any payment UI is shown.

- New route `/checkout/review` rendered by `OrderReviewPage`, which
  reuses the existing `OrderReview` component and `CartSummary`'s
  fee math (the 10% service-fee invariant is unchanged).
- "Proceed to Checkout" buttons in `CartDrawer` and `CartSummary`
  now point at `/checkout/review` instead of `/checkout`.
- `CheckoutPage` gates entry: a non-empty cart that has not been
  reviewed redirects to `/checkout/review`. Carts already in a
  payment flow (Stripe ready or mock processing) are not redirected
  even if the cart clears mid-flow.
- New `checkout-review-gate` module stores a fingerprint of the
  reviewed cart in `sessionStorage`. The fingerprint includes cart
  id, subtotal, and each item's `priceAtAdd` + `currentPrice`, so
  adding/removing items or any price drift invalidates the gate
  and forces a fresh review.
- Gate is cleared automatically once the cart becomes empty
  post-purchase, so the next cart cycle starts at review again.

## Scope boundaries

Implements only the "Order review step with itemized breakdown
before payment" subitem of #39. No backend changes. No changes to
MCP `checkout`/`confirmOrder` tools or ACP `/acp/v1/checkout`
endpoints - request/response shapes and behavior are identical.
The review gate is sessionStorage-based UX, not a security control;
server-side cart ownership, listing availability, pricing, and
order validation continue to be the authoritative checks.

## Tests run

- `frontend` Vitest unit tests:
  - `frontend/src/lib/checkout-review-gate.test.ts` (new) - 8 cases
    covering mark/clear/detect plus fingerprint invalidation on
    subtotal change, item reprice, `priceAtAdd` change, and item
    add.
  - `frontend/src/pages/OrderReviewPage.test.tsx` (new) - empty
    state, itemized totals (subtotal/10% fee/total), price-change
    signal, Back to Cart link, Continue marks gate + navigates to
    `/checkout`.
  - `frontend/src/pages/CheckoutPage.test.tsx` (extended) - gate
    redirect when not reviewed, gate-cleared-after-empty-cart, and
    payment view stays mounted if the cart clears mid mock-payment.
- `frontend` Playwright E2E (`cart-checkout.spec.ts`):
  - cart -> review -> payment happy path including Back to Cart
    round-trip and 10% fee assertion.
  - direct nav to `/checkout` with a non-empty unreviewed cart
    redirects to `/checkout/review`.

## Notes for reviewers

- The gate is intentionally fingerprint-based rather than a single
  boolean: any cart mutation (add/remove/reprice) between review
  and payment forces a re-review. Verify that the fingerprint
  inputs match what you'd want to invalidate on.
- `CheckoutPage` skips the redirect when `stripeReady ||
  isMockProcessing` is true. Without this, the cart-cleared-by-
  server-after-payment moment would bounce the buyer back to
  review mid-flow. The new test
  `keeps the payment view visible if the cart clears while mock
  payment is processing` pins this behavior.
- `sessionStorage` access is wrapped in try/catch; in private mode
  the gate fails closed (always redirects to review), which is the
  desired UX.
- README's frontend test count bumped from 427 to 465 (38 new
  cases across the new files and CheckoutPage extensions).
- ARCHITECTURE.md route table and `docs/demo-scenarios.md`
  concurrent-buyers script updated to mention the review step.
- No new dependencies, no Flyway migrations, no changes to
  SecurityConfig or SPA exclusions (the new route is under the
  existing authenticated `/checkout` prefix).
```

## 4. "Not included" (other #39 bullets left for later)

The PR intentionally leaves the remaining "Polish checkout flow" subitems for follow-up branches:

- Saved/auto-filled payment methods or address book improvements.
- Promo / discount code entry on the review or payment step.
- Inline cart edits (qty/remove) on the review page itself - currently you go back to `/cart` to edit.
- Express checkout / one-click purchase (skip-review opt-in for trusted carts).
- Backend confirmation-page or email refresh to match the new pre-payment review wording.
- Mobile-specific UX polish beyond the existing responsive stacking.
- Server-enforced review acknowledgment (the gate today is sessionStorage UX only; if #39 later wants a hard server-side requirement, that's a separate change with a new `checkoutSession` field).

---

`★ Insight ─────────────────────────────────────`
- The fingerprint design is a small but meaningful choice: a boolean "reviewed" flag would let a price drift between review and payment slip past unnoticed. Including `priceAtAdd` *and* `currentPrice` (not just subtotal) means even a same-subtotal swap of items invalidates the gate.
- The `inPaymentFlow` escape hatch in `CheckoutPage` is the kind of subtle interaction worth a regression test - server clears the cart on successful payment, and without that guard the user would briefly see a "back to review" redirect before the confirmation route takes over.
- Calling out the gate as "UX, not a security control" in both the commit body and PR description is the kind of thing reviewers (and future readers of `git log`) appreciate - it preempts the "can't you bypass this with devtools?" comment.
`─────────────────────────────────────────────────`
