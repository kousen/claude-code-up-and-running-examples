Read GitHub issue #167 in this repo. The Builder on
TicketmasterEventResponse already exists, the BuilderTest already
passes, and TicketmasterEventMapperTest already uses the Builder.

Audit the remaining test files under
backend/src/test/java/com/mockhub/ticketmaster/ for any direct
construction of TicketmasterEventResponse or TicketmasterAttractionResponse
via positional constructors. Specifically inspect:

- TicketmasterSyncServiceTest.java
- TicketmasterApiServiceTest.java
- TicketmasterEventMapperTest.java
- TicketmasterEventDeserializationTest.java (guardrail: migrate only if
  it directly constructs DTOs)
- TicketmasterAttractionDeserializationTest.java (guardrail: migrate only
  if it directly constructs DTOs)
- Any other test file in that subtree (do a full sweep).

Produce a report listing:
- Which files still use positional constructors and where.
- Which would benefit from a Builder migration.
- Whether TicketmasterAttractionResponse should also get a Builder, or
  whether its 3-arg shape makes a Builder unnecessary. Use this criterion:
  add the Builder if positional construction appears in more than one test
  file or if nested externalLinks setup obscures intent.
- Which deserialization tests should be run as guardrails after the change.

Do not make any code changes in this phase. Just produce the report.
