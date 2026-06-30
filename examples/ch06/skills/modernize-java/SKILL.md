---
name: modernize-java
description: Update Java code to modern language features — records, switch expressions, pattern matching, virtual threads, sealed classes, text blocks, and current collection idioms. Triggers on Java source files.
paths:
  - "**/*.java"
effort: medium
user-invocable: true
---

# Modernize Java Code

Update the target code to use modern Java features:

- **Records** instead of mutable POJOs where the type is a value carrier
- **Switch expressions** with arrow syntax and exhaustiveness checking
- **Pattern matching** for `instanceof` and `switch`
- **Local variable type inference** (`var`) where it helps readability
- **Virtual threads** (Java 21+) for I/O-bound operations — `Executors.newVirtualThreadPerTaskExecutor()`
- **Sealed classes** when the type hierarchy is closed
- **Text blocks** for multiline strings
- **Sequenced collections** (Java 21+) where ordered access matters
- **Collection factory methods** (`List.of`, `Map.of`, `Map.entry`)

## Constraints

- Don't change behavior — preserve the public API and observable semantics.
- Don't apply `var` where the inferred type would harm readability (e.g., factory results that could be any of several types).
- If the project's target Java version is below 21, skip the 21+ features and note it in your summary.
- Run the test suite after non-trivial changes; if tests don't exist, surface that as a follow-up rather than as a blocker.
