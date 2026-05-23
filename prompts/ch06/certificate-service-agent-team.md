# Certificate-service agent team

```text
You are running in a disposable branch/worktree for a transcript capture.

Create an agent team for this Spring Boot certificate-service project.

Use three teammates with disjoint ownership:

- tests-reviewer: src/test/** only; read-only. Look for coverage gaps.
- security-reviewer: src/main/** and build files; read-only. Look for
  credential handling, certificate validation, path traversal, and dependency
  CVE risks.
- docs-owner: README.md, CLAUDE.md, and docs/** only; may edit docs after plan
  approval. Update setup notes and any drift between behavior and documentation.

Run them in parallel where possible. Because this is a headless transcript
capture, do not use split-pane mode; summarize the team shape in text instead.

Before docs-owner edits files, propose the docs edit plan. For this capture,
the human pre-approves that plan only if it is limited to README.md, CLAUDE.md,
and docs/** and does not touch source code, build files, secrets, or
configuration. If the docs plan exceeds that scope, stop and ask for approval
instead of editing.

When the work is complete, synthesize. Report what changed, what each teammate
found, and any follow-up tasks that should remain for a human decision.
```
