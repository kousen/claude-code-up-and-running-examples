# Ch8 MockHub #39 Order Review Implementation Prompt

```text
Implement MockHub issue #39, scoped only to the subitem "Order review step
with itemized breakdown before payment."

The Phase 1 spec is approved. The Phase 2 plan correctly identified that
this is mostly frontend checkout flow, but adjust the implementation scope
to use the routed boundary from the spec:

- Add a dedicated `/checkout/review` route for the human order-review step.
- Keep `/checkout` as the existing payment page.
- Users should reach `/checkout/review` from cart checkout actions.
- Users can go back to `/cart` from review without losing cart state.
- Users can continue from `/checkout/review` to `/checkout`.
- If a user navigates directly to `/checkout` with a non-empty cart and has
  not passed the review gate for that cart, redirect them to `/checkout/review`.
- Preserve the existing payment behavior after the user reaches `/checkout`.

Implementation constraints:

- Reuse or extend the existing `OrderReview` component. Do not create a
  duplicate review component.
- Reuse the existing cart summary behavior where appropriate. Preserve the
  10% service-fee invariant and do not introduce a third source of truth for
  fee math.
- Preserve the price-change signal when `priceAtAdd` and `currentPrice`
  differ.
- Do not change backend DTOs, `OrderService`, MCP tools, ACP endpoints, or
  checkout response shapes.
- Do not add a progress indicator, promo-code behavior, tax behavior, new
  database state, or a new global Zustand checkout store.
- Do not commit.

Testing and verification:

- Add or update focused frontend tests for the new review page/gate.
- Add or update at least one Playwright test that walks cart -> review ->
  payment using mocked API responses where appropriate.
- Run the relevant frontend tests and Playwright check for this flow. Run
  backend tests only if you touch backend code; otherwise explicitly report
  that backend code was untouched.
- Report changed files, tests run, pass/fail, and any follow-up risks.
```
