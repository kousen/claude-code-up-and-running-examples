Prepare PR materials for MockHub issue #167.

Branch:

`refactor/ch09-builder-migration-167`

Issue:

`Closes #167`

Final scope:

- Added `TicketmasterAttractionResponse.Builder`, matching the existing
  `TicketmasterEventResponse.Builder` pattern.
- Migrated positional `TicketmasterAttractionResponse` construction in
  `TicketmasterEventMapperTest` and `TicketmasterSyncServiceTest`.
- Added `TicketmasterAttractionResponseBuilderTest` guardrails.
- Preserved Jackson deserialization tests as JSON/ObjectMapper guardrails.
- Preserved direct constructors only in builder internals and
  builder-equivalence tests.
- Left `MockTicketmasterService` production fixture construction unchanged
  because the Ch9 capture spec explicitly keeps production code out of scope.
- Did not change wire DTO shape, Ticketmaster API behavior, mapper semantics, or
  sync behavior.

Verification:

- `git diff --check`
- `./gradlew test jacocoTestReport --rerun-tasks --quiet`
- Backend test report: 1176 tests, 0 failures, 0 skipped.

Prepare:

1. A conventional commit message.
2. A ready-to-use PR title.
3. A ready-to-use PR description with summary, tests, reviewer notes, and
   `Closes #167`.

Do not commit, push, or modify files. Report only the PR materials.
