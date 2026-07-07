# Ch8 MockHub #39 Order Review Spec Prompt

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
