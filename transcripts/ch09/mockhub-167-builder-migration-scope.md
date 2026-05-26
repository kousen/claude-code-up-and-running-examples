The first Phase 2 capture attempt used the original spec wording, "Confirm you understand the
scope, then proceed to Phase 3." Claude Code interpreted "proceed" literally, made the intended
migration edits, and produced no stdout before the process was stopped. Codex inspected the working
tree afterward and found only the intended Ch9 files changed:

- `backend/src/main/java/com/mockhub/ticketmaster/dto/TicketmasterAttractionResponse.java`
- `backend/src/test/java/com/mockhub/ticketmaster/dto/TicketmasterAttractionResponseBuilderTest.java`
- `backend/src/test/java/com/mockhub/ticketmaster/service/TicketmasterEventMapperTest.java`
- `backend/src/test/java/com/mockhub/ticketmaster/service/TicketmasterSyncServiceTest.java`

The prompt was then tightened to "Do not make code changes in this phase" before rerunning the
scope-confirmation capture below.

Confirmed. Here's my understanding of the scope:

**In scope**
1. Add a static nested `Builder` to `TicketmasterAttractionResponse` (production change limited to this).
2. Migrate two tests from positional record construction to the new Builder:
   - `TicketmasterEventMapperTest.java`
   - `TicketmasterSyncServiceTest.java`
   - (Note: actual path is `ticketmaster/service/` per git status — the working tree already has both files modified. I'll target the actual locations.)
3. Add a new characterization test `TicketmasterAttractionResponseBuilderTest.java` (already present as untracked) mirroring the parity pattern of `TicketmasterEventResponseBuilderTest`.
4. Run the two deserialization tests as JSON/Jackson guardrails — verify they still pass, do not rewrite them.

**Out of scope**
- No changes to mapper logic, sync service behavior, API client, or JSON wire format.
- No changes to record components on `TicketmasterAttractionResponse` beyond adding the Builder.
- Leave `TicketmasterEventResponseBuilderTest.java`'s intentional positional `new TicketmasterEventResponse(...)` call alone (it's the parity baseline).
- No migration of either deserialization test.

★ Insight ─────────────────────────────────────
- The Builder-vs-positional decision here hinges on a real signal from the capture spec: nested setup (e.g., `externalLinks` for the Spotify extraction path) makes positional record construction hard to read, especially across tests that vary only a few fields. Builders shine when call sites diverge on a small subset of many components.
- Keeping `TicketmasterEventResponseBuilderTest`'s direct constructor call is deliberate — it's the *contract pin* that proves the Builder produces an instance equivalent to positional construction. Migrate it away and the parity guarantee disappears.
- Treating the deserialization tests as guardrails (not migration targets) preserves a useful invariant: Jackson still talks to the canonical record shape, independent of how *we* build instances in unit tests. Two different concerns, two different test types.
─────────────────────────────────────────────────

Ready to proceed when you give the go-ahead.
