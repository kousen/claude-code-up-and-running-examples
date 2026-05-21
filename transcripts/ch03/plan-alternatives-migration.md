# ch03 plan alternatives migration

Date captured: 2026-05-21

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples
```

Prompt:

```text
The plan you produced for the database migration uses ALTER TABLE ... USING. What other approaches exist, and when would each one be right?
```

Output:

```text
I checked the `ch03-local-persistence` app and it actually persists through `localStorage`, not SQL — so the `ALTER TABLE ... USING` plan you're referring to isn't one that's saved in this repo. It must be from earlier in our conversation (now summarized out of my view) or a separate context. I'll answer the question on its own terms, since it's a good one regardless of which schema it targeted.

`ALTER TABLE ... ALTER COLUMN ... TYPE ... USING` is the PostgreSQL idiom for **changing a column's type in place**, with the `USING` clause supplying the expression that converts each existing value. Here's the landscape of alternatives and the decision logic behind each.

`★ Insight ─────────────────────────────────────`
- The real axis these approaches sort along isn't "correctness" — they all produce the same end schema — it's **how long the table is locked and whether the change is reversible mid-flight**.
- `ALTER TABLE ... TYPE` takes an `ACCESS EXCLUSIVE` lock and rewrites the whole table; that's fine at small scale and catastrophic on a hot multi-million-row table.
- Production-grade migrations trade one fast risky statement for several slow safe ones (the "expand/contract" pattern).
`─────────────────────────────────────────────────`

## The approaches

**1. In-place `ALTER TABLE ... TYPE ... USING` (what the plan used)**
```sql
ALTER TABLE songs
  ALTER COLUMN play_count TYPE bigint USING play_count::bigint;
```
- **What happens:** Postgres takes an `ACCESS EXCLUSIVE` lock (blocks reads *and* writes) and, for most type changes, rewrites the entire table and its indexes.
- **Right when:** the table is small, you're in a maintenance window, or it's a fresh/dev database. Also genuinely cheap for a narrow set of "binary-compatible" changes (e.g. `varchar(50)` → `varchar(100)`, or `varchar` → `text`) where no rewrite occurs.
- **Wrong when:** the table is large and live. The exclusive lock + full rewrite can mean minutes of downtime.

**2. Expand / contract with a new column (the safe production default)**
1. `ADD COLUMN play_count_new bigint` (instant — nullable, no default with a volatile expression).
2. Backfill in batches: `UPDATE ... WHERE id BETWEEN ... ` in chunks so you never hold a long transaction.
3. Dual-write from the app (write both old and new) during rollout.
4. Swap reads to the new column, then drop the old one in a later migration.
- **Right when:** zero-downtime is required on a large, actively-written table. It's reversible at every step.
- **Cost:** multi-step, spans multiple deploys, requires app coordination.

**3. New table + copy + rename**
```sql
CREATE TABLE songs_new (... corrected schema ...);
INSERT INTO songs_new SELECT ... FROM songs;
-- catch up changes, then:
ALTER TABLE songs RENAME TO songs_old;
ALTER TABLE songs_new RENAME TO songs;
```
- **Right when:** you're changing *many* things at once (several column types, constraints, ordering), or the in-place rewrite would lock too long. Tools like `pg_repack` and `gh-ost`/`pt-online-schema-change` (MySQL world) automate exactly this shadow-table dance.
- **Cost:** most complex; you must capture writes during the copy (triggers or logical replication).

**4. Generated / computed column or a view**
- Add a `GENERATED ALWAYS AS (...) STORED` column, or expose the converted value through a view, and never touch the original.
- **Right when:** you don't actually need to *change* the stored type — you need a differently-typed *representation* (e.g. a `text` timestamp surfaced as `timestamptz`). Avoids a rewrite entirely.
- **Wrong when:** the old column's type is itself the problem (wrong storage, bad constraints).

**5. Application-level / ORM migration with batched backfill**
- Same as #2 but expressed in your migration framework (Flyway, Liquibase, Alembic, Rails). The framework adds version tracking and rollback scripts.
- **Right when:** you already have a migration tool in the project and want the change recorded, ordered, and repeatable across environments.

## Quick decision guide

| Situation | Pick |
|---|---|
| Small table / dev / maintenance window | **In-place `ALTER ... USING`** |
| Binary-compatible widening (`varchar`→`text`) | **In-place** (no rewrite anyway) |
| Large, live, write-heavy table, zero downtime | **Expand/contract (#2)** |
| Many simultaneous schema changes on a big table | **Shadow table (#3)** or `pg_repack` |
| Only need a converted *view* of the data | **Generated column / view (#4)** |
| Want it versioned & rollback-able | **Migration tool (#5)** wrapping the above |

So the in-place `ALTER TABLE ... USING` in the plan is the right call **if** that table is small or the migration runs during downtime. The moment it's a large, continuously-written table, you'd want to switch to the expand/contract pattern.

If you point me at the actual schema/plan this referred to, I can tell you specifically which bucket it falls into and rewrite it accordingly.
```
