Execute the migration. For each test file in scope:

1. Replace positional `new TicketmasterEventResponse(...)` constructions
   with `TicketmasterEventResponse.builder()...build()` chains.
2. Preserve all assertions semantically.
3. Run the affected test class after each file migration. Report
   pass/fail.
4. If you decided to add a Builder to `TicketmasterAttractionResponse`,
   add it with the same pattern as the EventResponse Builder (static
   inner class, fluent setters, build()).
5. Do not migrate production code (mapper, service, controller layers).
6. Run the Ticketmaster deserialization tests as guardrails after any
   DTO builder change. They should still exercise JSON/ObjectMapper, not
   the Builder.

After all migrations, run the full backend test suite and report
results.

Note: The Phase 2 scope-confirmation prompt accidentally applied the intended migration edits before
the stream-json trace began. Start by inspecting the current working tree, keep any correct intended
changes, complete or correct anything missing, then run the same per-file and guardrail verification
specified above.
