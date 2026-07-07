Here are the PR materials.

---

## 1. Conventional commit message

```
refactor(ticketmaster): add TicketmasterAttractionResponse.Builder and migrate tests

Introduce a Builder for TicketmasterAttractionResponse matching the
existing TicketmasterEventResponse.Builder pattern, and migrate positional
constructor usage in the Ticketmaster mapper and sync service tests to the
builder API for readability.

- Add TicketmasterAttractionResponse.Builder
- Add TicketmasterAttractionResponseBuilderTest guardrails
- Migrate TicketmasterEventMapperTest and TicketmasterSyncServiceTest to builder
- Preserve Jackson deserialization tests as JSON/ObjectMapper guardrails
- Preserve direct constructor usage only in builder internals and
  builder-equivalence tests
- Leave MockTicketmasterService production fixture construction unchanged
  (out of scope per Ch9 capture spec)

No changes to wire DTO shape, Ticketmaster API behavior, mapper semantics,
or sync behavior.

Closes #167
```

---

## 2. PR title

```
refactor(ticketmaster): add TicketmasterAttractionResponse.Builder and migrate tests
```

---

## 3. PR description

```markdown
## Summary

Adds a `Builder` to `TicketmasterAttractionResponse`, mirroring the existing
`TicketmasterEventResponse.Builder` pattern, and migrates positional
constructor usage in the Ticketmaster test suite to the new builder API for
readability.

This is a test-only refactor on the call-site side: production code (the
record itself, mapper, and sync service) is unchanged in behavior. The
record gains a `Builder` inner class but its wire shape and constructor
remain intact.

## Changes

- Added `TicketmasterAttractionResponse.Builder` (matches
  `TicketmasterEventResponse.Builder` pattern).
- Migrated positional `TicketmasterAttractionResponse` construction in:
  - `TicketmasterEventMapperTest`
  - `TicketmasterSyncServiceTest`
- Added `TicketmasterAttractionResponseBuilderTest` as guardrails for the
  new builder.
- Preserved Jackson deserialization tests that drive construction through
  `ObjectMapper` — these intentionally remain as JSON-based guardrails.
- Preserved direct constructor usage only inside builder internals and
  builder-equivalence tests.

## Out of scope

- `MockTicketmasterService` production fixture construction is unchanged.
  The Ch9 capture spec explicitly keeps production code out of scope for
  this migration.
- No changes to wire DTO shape, Ticketmaster API behavior, mapper
  semantics, or sync behavior.

## Tests

- `git diff --check` — clean
- `./gradlew test jacocoTestReport --rerun-tasks --quiet`
- Backend test report: **1176 tests, 0 failures, 0 skipped**

## Reviewer notes

- The builder mirrors the existing `TicketmasterEventResponse.Builder`
  intentionally — please flag any drift from that pattern.
- Jackson-driven construction paths are deliberately left alone; the
  serialization contract is exercised through `ObjectMapper`, not the
  builder.
- The unchanged `MockTicketmasterService` call sites are intentional per
  the Ch9 capture spec; a follow-up issue can sweep production fixtures if
  desired.

Closes #167
```
