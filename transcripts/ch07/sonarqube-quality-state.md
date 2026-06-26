# ch07 sonarqube quality state

Date captured: 2026-05-24

Working directory:

```text
~/Documents/AI/mockhub
```

Prompt:

```text
Use the SonarQube MCP server to inspect the current MockHub quality state.

Resolve the project key from the repository configuration rather than guessing.
Report the quality gate, a small set of maintainability/coverage/security
measures, and any security hotspots. Do not infer SonarCloud status from the
codebase alone; ask the service that owns the analysis.

Do not edit files.
```

Output:

```text
★ Insight ─────────────────────────────────────
- Quality gate evaluation is split between **overall code** measures (e.g. `coverage`, `sqale_index`) and **new code** measures (e.g. `new_coverage`, `new_security_hotspots_reviewed`). Most SonarCloud quality gates only fail on the *new code* conditions — overall metrics give the long-term health picture but don't gate merges.
- A `security_hotspots` count of 0 with `new_security_hotspots_reviewed = 100%` means there's nothing currently outstanding *and* the gate's review requirement is satisfied — distinct facts that both must hold.
- `sqale_index = 232` is minutes of estimated technical debt (~3.8 hrs) across ~30.5 KLoC — that's what produces the `A` maintainability rating (rating = 1.0).
─────────────────────────────────────────────────

## MockHub SonarCloud Status

**Project:** `kousen_mockhub` (org `kousen-it-inc`) — resolved from `sonar-project.properties`.

### Quality Gate: **PASSING** ✅
All six new-code conditions green:

| Condition | Threshold | Actual |
|---|---|---|
| New reliability rating | A | A |
| New security rating | A | A |
| New maintainability rating | A | A |
| New coverage | ≥ 80% | **86.3%** |
| New duplicated lines | ≤ 3% | **0.2%** |
| New hotspots reviewed | 100% | **100%** |

### Overall measures

| Metric | Value |
|---|---|
| Lines of code | 30,532 |
| Coverage | 85.7% |
| Bugs | 0 (Reliability A) |
| Vulnerabilities | 0 (Security A) |
| Security hotspots | 0 |
| Code smells | 39 |
| Technical debt | 232 min (~3.8 hrs, Maintainability A) |
| Duplicated lines | 0.6% |

### Security hotspots: none open
`search_security_hotspots` returned 0 results in `TO_REVIEW` — nothing awaiting triage.

Bottom line: project is fully green on SonarCloud — main work outstanding is the 39 code smells / ~4 hrs of tech debt, none of which are gating.
```
