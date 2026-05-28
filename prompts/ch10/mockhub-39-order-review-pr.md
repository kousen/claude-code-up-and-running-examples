Draft commit and PR materials for the current MockHub branch.

Context:
- Branch: feat/ch08-order-review-step
- GitHub issue: #39, "Polish checkout flow"
- Scope: only the subitem "Order review step with itemized breakdown before payment"
- Do not commit, push, open a PR, merge, deploy, or mutate external state.

Please inspect the current working tree and produce:

1. A concise conventional commit message.
2. A PR title.
3. A PR description with:
   - Summary
   - Scope boundaries
   - Tests run
   - Notes for reviewers
4. A short "not included" list for the other issue #39 bullets intentionally left for later.

Important details to preserve:
- The browser flow adds `/checkout/review` between cart and payment.
- `OrderReviewPage` reuses the existing `OrderReview` and `CartSummary` behavior.
- The 10% service-fee invariant remains in existing CartSummary math.
- The review gate is sessionStorage-based UX state, not a security control.
- The gate fingerprint includes cart id, subtotal, priceAtAdd, and currentPrice so repricing or cart edits force a fresh review.
- MCP/ACP checkout response shape and behavior are untouched.
