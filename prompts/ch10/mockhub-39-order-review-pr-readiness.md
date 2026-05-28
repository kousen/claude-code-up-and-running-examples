Run a PR-readiness check on the current branch for issue #39
(order review subitem). Follow these steps and produce a structured
report at the end. Do not merge, push, or deploy.

1. Inspect the branch and the issue. Confirm the change is in scope.
2. Run backend tests, frontend tests, lint, and build. Capture failures.
3. Use the SonarQube/SonarCloud MCP server to fetch the current quality
   gate state for this branch (if available) or for main as a baseline.
4. Ask reviewer sub-agents for risks if they have been installed for
   this run (mockhub-test-reviewer, mockhub-security-reviewer,
   mockhub-docs-reviewer). Each runs read-only. If those sub-agents are
   not available in the MockHub working tree, state that clearly and run
   equivalent read-only reviewer prompts by lens instead.
5. Produce a structured readiness report with these fields:
   - branch, head SHA, issue, summary of change
   - test results (counts, names of failing tests if any)
   - SonarCloud state
   - reviewer findings by lens, severity, and uncertainty
   - readiness verdict (ready / not ready) with reasoning
   - explicit "remaining for human" list
6. Stop. Do not merge, push, deploy, or revoke any external state.
