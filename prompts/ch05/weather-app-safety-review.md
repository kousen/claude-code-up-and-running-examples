# Chapter 5 weather-app safety / trust-boundary review prompt

The Ch5 review prompt that folds permissions into the review (ch05 ~lines
589-603). The last line is the point: not just "is the code safe?" but "what
boundary would make future agent work safer?" Produces the structured
severity/evidence/risk/recommendation findings the chapter shows. Reconcile the
two sample findings (the live-API test finding, the publish-script finding) to
whatever the real review surfaces.

```text
Review this Flask app for safety and trust-boundary issues.

Focus on:
- input validation
- secret handling
- network calls
- tests that hit external services
- commands or scripts that would be risky for an agent to run
- repository operations that should require explicit human approval

Do not edit files. Report findings with severity, evidence, and a recommended permission boundary or workflow change.
```
