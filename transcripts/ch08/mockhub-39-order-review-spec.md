# ch08 mockhub 39 order review spec

Date captured: 2026-05-26

Working directory:

```text
~/Documents/AI/mockhub
```

Prompt:

```text
Read GitHub issue #39 in this repo and focus only on the subitem
"Order review step with itemized breakdown before payment."

Write a one-page working spec for that subitem in the postconditions-
first Design by Contract style:

1. Postconditions: what must be true after this slice is done?
2. Preconditions: what must already be true for the work to start?
3. Invariants: what must remain true while the code changes?
4. Negative criteria: what must NOT happen?

Include the cart-to-review-to-payment routing, the itemized breakdown
fields, the back-to-cart navigation, and the agentic-checkout
invariant that this slice does not change the MCP/ACP path.
Also account for the existing OrderReview component, the existing
CartSummary/OrderService 10% service fee behavior, and the price-change
signal when priceAtAdd and currentPrice differ.

Do not start implementing. Treat the spec as a draft; revise it if
inspection reveals a better boundary.
```

Output:

```text
Spec written to `docs/specs/order-review-step.md`.

`★ Insight ─────────────────────────────────────`
- The existing `OrderReview` component is already read-only and already composes `CartSummary` — the slice is really about **routing** (inserting `/checkout/review` between `/cart` and `/checkout`), not about new presentation logic. That's why the spec's hardest invariants are about *what doesn't change*: the fee constant, the price-change signal, the agentic path.
- The single-fee-source invariant matters because both `CartSummary` (frontend display) and `OrderService` (backend authority) hardcode 10%. A review step is the natural place to add a "fees breakdown" component, which is exactly where a third copy of `0.10` would sneak in. The spec forbids it preemptively.
- The agentic invariant is almost free here because MCP/ACP never touch React routes — but stating it explicitly protects against well-meaning refactors that move fee math from `OrderService` into a "shared checkout module" the React page calls into.
`─────────────────────────────────────────────────`

**Boundary tradeoff worth your input before implementation:** the spec defaults to a new `/checkout/review` route, but a single `/checkout` page with internal step state is the cheaper alternative. The routed approach is better for the sibling "progress indicator" subitem and supports deep-linking; the stateful approach is faster to ship. I went with routed in the draft — flag if you'd rather start stateful.
```

Generated spec artifact:

```markdown
# Spec: Order Review Step (Issue #39, subitem)

**Status:** Draft — revise if implementation reveals a better boundary.
**Branch:** `feat/ch08-order-review-step`
**Scope:** Frontend only. Insert a dedicated review step between cart and payment on the `/checkout` flow. No backend, MCP, or ACP changes.

---

## 1. Postconditions (what must be true when this is done)

- Cart → review → payment → confirmation is a visible, three-segment routing path on the frontend.
- A user clicking "Proceed to Checkout" from `CartPage` lands on a **review screen** that shows the itemized breakdown and a clearly-labeled "Continue to Payment" action, not the payment form.
- The review screen renders every cart item with: event name, section / row / seat, ticket type badge, `currentPrice`, and a "+/-$X since added" indicator whenever `currentPrice !== priceAtAdd`.
- The review screen shows a totals block driven by the existing `CartSummary` rules: **subtotal, 10% service fee, total** — matching the values the backend `OrderService` will compute on `POST /api/v1/orders/checkout`.
- A "Back to Cart" affordance returns the user to `/cart` without mutating cart state (no remove, no clear, no order created).
- The payment screen (mock + Stripe tabs) renders only after the user explicitly continues from review.
- The existing `OrderReview` component is reused — not duplicated or forked.
- Component tests cover: itemized rendering, price-change indicator, totals match `CartSummary`, "Back to Cart" navigation, "Continue to Payment" navigation, empty-cart redirect.

## 2. Preconditions (what must be true before starting)

- User is authenticated (existing `ProtectedRoute` guard on `/checkout`).
- `useCart()` returns a non-empty cart; empty-cart state still routes to the existing `EmptyState` block.
- `OrderReview`, `CartSummary`, `CartItem`, `useCart`, `ROUTES` already exist and behave as documented in `CLAUDE.md`.
- Backend `OrderService` 10% service fee logic is unchanged and remains the source of truth for the total written to the order.

## 3. Invariants (what must remain true during the change)

- **Single fee constant.** Frontend keeps `SERVICE_FEE_RATE = 0.1` in exactly one place (`CartSummary`); the review step does not introduce a second copy. Backend stays at `BigDecimal("0.10")` in `OrderService`. Display ≡ what backend charges.
- **Cart is not mutated by reviewing.** No `POST /api/v1/orders/checkout`, no `clearCart`, no `removeFromCart` triggered by entering, viewing, or leaving the review screen.
- **Price-change signal is preserved.** `CartItem`'s `priceChanged` rendering (`priceAtAdd` vs `currentPrice`) continues to work in both the cart page and the review step; the review step does not hide or override it.
- **Agentic checkout path is untouched.** MCP `checkout` + `confirmOrder` tools and ACP `/acp/v1/checkout/**` endpoints continue to call `OrderService.checkout(...)` directly. The review step is a browser-only UI insertion; no agent ever transits a React route.
- **`OrderReview` stays read-only.** It does not gain remove / edit buttons. Editing the cart still requires returning to `/cart`.
- **`CartPage` "Proceed to Checkout" target may change**, but its semantics — "advance toward payment" — do not.

## 4. Negative criteria (what must NOT happen)

- Do **not** create an order or payment intent on entering the review screen. Order creation stays gated behind the explicit payment action (mock submit or "Pay with Stripe").
- Do **not** recompute totals from a third formula. Service fee math lives in `CartSummary` (frontend) and `OrderService` (backend); no inline `subtotal * 0.10` elsewhere.
- Do **not** alter `CartItemDto`, `OrderResponse`, or any backend DTO. This slice ships without a backend diff.
- Do **not** modify MCP tool signatures, `AcpController`, or `OrderService` — including no new "review" endpoint.
- Do **not** introduce a new global state store. Review-step navigation is route-based (URL is the source of truth), not Zustand.
- Do **not** suppress the price-change indicator on the review screen "to look cleaner." It is a deliberate user-protection signal before payment.
- Do **not** bypass auth or empty-cart guards on the new route.
- Do **not** add the progress indicator here — that is a sibling subitem in #39 and ships in its own slice. This spec is structured so the indicator can drop in over the same route layout.

---

## Proposed boundary (revisable)

- New route: `ROUTES.CHECKOUT_REVIEW = '/checkout/review'`.
- `CartPage` "Proceed to Checkout" → `/checkout/review`.
- `/checkout/review` renders `OrderReview` (already read-only) + a footer with "Back to Cart" (→ `/cart`) and "Continue to Payment" (→ `/checkout`).
- `/checkout` remains the payment page, but its embedded `OrderReview` panel becomes a compact summary (or stays — decide during implementation; the invariants don't require either choice).
- Empty cart on `/checkout/review` reuses the existing `EmptyState` pattern from `CheckoutPage`.

**Alternative boundary to consider during implementation:** keep one `/checkout` route and drive review-vs-payment with internal step state. Cheaper, but worse for the progress-indicator subitem and harder to deep-link. Default to the routed approach unless inspection surfaces a reason to prefer the stateful one.
```
