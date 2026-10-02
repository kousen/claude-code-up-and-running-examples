Create a team of agents for the certificate-service project.

Use three teammates with disjoint ownership boundaries:

- tests-reviewer: src/test/** only; read-only. Look for coverage gaps.
- security-reviewer: src/main/** and build files; read-only. Look for
  credential handling, certificate validation, path traversal, and dependency
  CVE risks.
- docs-owner: README.md, CLAUDE.md, and docs/** only; may edit. Update setup
  notes and any drift between behavior and documentation.

Run them in parallel where possible.
Before docs-owner edits files, propose the plan and wait for my approval.

When the work is complete, synthesize. Report what changed, what each
teammate found, and any follow-up tasks that should remain for a human
decision.
