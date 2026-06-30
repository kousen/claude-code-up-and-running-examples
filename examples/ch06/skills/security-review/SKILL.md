---
name: security-review
description: Read-only security audit of code for SQL injection, XSS, auth/authz flaws, input validation gaps, sensitive data exposure, and insecure cryptography. Surfaces findings without modifying code.
allowed-tools:
  - Read
  - Grep
  - Glob
disable-model-invocation: true
user-invocable: true
---

# Security Code Review

This skill is **explicit-invoke only** (`disable-model-invocation: true`) and **read-only** (`allowed-tools` covers reading + searching, no editing). It surfaces findings — fixing them is a separate, deliberate step.

## Categories to check

- **Injection**: SQL, NoSQL, OS command, LDAP, XPath, template
- **XSS**: reflected, stored, DOM-based; encoding context (HTML body vs. attribute vs. JS context)
- **AuthN / AuthZ**: missing checks, broken object-level authorization, privilege escalation
- **Input validation**: trust boundaries, type confusion, deserialization
- **Sensitive data exposure**: secrets in code, tokens in logs, PII in error responses, weak hashing
- **Cryptography**: hardcoded keys, ECB mode, weak algorithms (MD5/SHA-1 for security), missing IV randomness

## Output

For each finding, report:

1. **File and line** (Path:Line format so the user can jump to it)
2. **Severity** (critical / high / medium / low / informational)
3. **What's wrong**
4. **What an attack would look like**
5. **A recommended fix direction** (not the actual code change — that's a separate skill)

Group findings by severity. Don't speculate about issues you can't see in the code; if a check requires runtime context you don't have, say so.
