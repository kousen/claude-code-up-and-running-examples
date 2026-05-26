# Audit Report — Issue #167 Builder Migration

## Files using positional constructors

### 1. `TicketmasterEventMapperTest.java` — 10 occurrences
- Lines **117, 127, 137, 147, 157, 167, 177, 185, 195**: `new TicketmasterAttractionResponse(id, name, externalLinks)` in the `SpotifyExtraction` nested class (one per Spotify URL variant test).
- Line **491**: `new TicketmasterAttractionResponse(...)` inside `createSampleEventResponse()` helper (nested within an `Embedded` build).
- `TicketmasterEventResponse` itself is already fully on the Builder.

### 2. `TicketmasterSyncServiceTest.java` — 1 occurrence
- Line **463**: `new TicketmasterAttractionResponse(...)` inside `createSampleEvent()` helper (nested under `Embedded(...)` with venue list).
- All `TicketmasterEventResponse` construction in this file already uses `.builder()`.

### 3. `TicketmasterEventResponseBuilderTest.java` — 1 occurrence (DO NOT MIGRATE)
- Line **156**: `new TicketmasterEventResponse(...)` is **intentional** — the test `build_givenBuiltRecord_isEqualToDirectConstructor` exists specifically to assert builder output equals direct positional construction. Migrating this would defeat the test's purpose.

### 4. Files with no direct construction (no migration needed)
- `TicketmasterApiServiceTest.java` — only references `TicketmasterEventResponse` as a return type from the service; data comes from mocked HTTP JSON.
- `TicketmasterEventDeserializationTest.java` — JSON-only.
- `TicketmasterAttractionDeserializationTest.java` — JSON-only.
- `MockTicketmasterServiceTest.java` — no matches.
- `TicketmasterTicketGeneratorTest.java` — no matches.

## Should `TicketmasterAttractionResponse` get a Builder?

**Yes.** Both criteria from the guardrail are met:
1. **Multi-file usage** — positional construction appears in *two* test files (`TicketmasterEventMapperTest` and `TicketmasterSyncServiceTest`).
2. **Obscured intent in nested externalLinks setup** — the `Map.of("spotify", List.of(new ExternalLink(url, null)))` pattern repeats 10 times in `SpotifyExtraction` and reads more clearly as `.externalLinks(Map.of("spotify", List.of(...)))`. Two cases also pass `null` externalLinks (lines 177–180) — `.id().name().build()` would make that intent explicit instead of trailing-null positional.

Even though it's only 3 args today, the third arg's nesting depth is what makes positional construction noisy, not the arg count.

## Recommended migrations (in priority order)

| File | Change |
|---|---|
| `TicketmasterAttractionResponse` (production) | Add static `Builder` inner class mirroring the `TicketmasterEventResponse` pattern |
| `TicketmasterEventMapperTest` | Migrate 10 attraction constructions to `.builder()` |
| `TicketmasterSyncServiceTest` | Migrate 1 attraction construction to `.builder()` |
| `TicketmasterEventResponseBuilderTest` | Add a parallel `build_givenBuiltAttraction_isEqualToDirectConstructor` test (or extend the existing file) to lock down the new Attraction builder against its canonical constructor |

## Guardrail tests to run after the change

These exercise the JSON deserialization path (canonical record constructor) and will catch any accidental change to record component order/names/types caused by the Builder addition:

1. `TicketmasterEventDeserializationTest` — covers `TicketmasterEventResponse` JSON → record.
2. `TicketmasterAttractionDeserializationTest` — covers `TicketmasterAttractionResponse` JSON → record (the DTO getting the new Builder).
3. `TicketmasterEventResponseBuilderTest` — existing guard that builder equals positional constructor; mirror this for Attraction.

★ Insight ─────────────────────────────────────
- The Builder pattern is purely a *test-side* ergonomic — Jackson still binds to the canonical record constructor by component name, so the deserialization tests are the right guardrail to prove the production wire format hasn't shifted.
- The `BuilderTest` intentionally keeps one positional-constructor call so the canonical record shape stays asserted. Without that anchor, a Builder could silently drift from the record's component list and tests would still pass.
- `TicketmasterAttractionResponse` being only 3 args is a red herring: arg *count* matters less than *nesting depth at the call site*. The `Map.of(...)` → `List.of(...)` → `ExternalLink(...)` chain is what makes the third positional arg unreadable.
─────────────────────────────────────────────────

No code changes made — report only, as requested.
