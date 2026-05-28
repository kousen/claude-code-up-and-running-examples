Based on the audit, here are the decisions:

- Migrate these test files:
  - `backend/src/test/java/com/mockhub/ticketmaster/TicketmasterEventMapperTest.java`
  - `backend/src/test/java/com/mockhub/ticketmaster/TicketmasterSyncServiceTest.java`
- Add Builder to `TicketmasterAttractionResponse`: yes.
  - Reason: positional construction appears in more than one test file, and the nested `externalLinks`
    setup obscures intent in the Spotify extraction tests. This satisfies the criterion from the
    capture spec.
- Add characterization coverage for the new attraction Builder, matching the existing
  `TicketmasterEventResponseBuilderTest` parity pattern.
- Treat `TicketmasterEventDeserializationTest.java` and
  `TicketmasterAttractionDeserializationTest.java` as JSON/Jackson guardrails only. Run them after
  the migration, but do not rewrite them into Builder tests.
- Out of scope:
  - Do not migrate production code other than adding the static inner Builder to
    `TicketmasterAttractionResponse`.
  - Do not change the JSON wire format, record components, mapper behavior, sync behavior, or
    Ticketmaster API client behavior.
  - Do not migrate the intentional direct `new TicketmasterEventResponse(...)` call in
    `TicketmasterEventResponseBuilderTest.java`.

Confirm you understand the scope. Do not make code changes in this phase.
