Now step back and review the whole repository state. What did we miss?

Look for integration risks, stale docs, missing tests, accidental scope creep,
and anything that would surprise a reviewer.

Context:

- Branch: `refactor/ch09-builder-migration-167`
- Issue: MockHub #167, Builder migration sweep.
- Intended scope:
  - Add `TicketmasterAttractionResponse.Builder` because positional construction
    appears in more than one test file and nested `externalLinks` obscures intent.
  - Migrate direct positional construction in `TicketmasterEventMapperTest` and
    `TicketmasterSyncServiceTest`.
  - Keep Jackson deserialization tests as guardrails; do not replace JSON
    deserialization coverage with builder tests.
  - Preserve direct constructor calls only in builder-equivalence tests.
  - Do not change wire DTO shape, Ticketmaster API behavior, mapper semantics,
    or sync behavior.

Review only. Do not modify files. Report findings, risks, and recommended
follow-up actions.
