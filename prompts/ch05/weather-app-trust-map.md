# Chapter 5 weather-app trust-map prompt

The read-only "draw the trust map first" review (ch05 ~lines 414-425). Run
against the built weather app. Produces the bulleted trust-map response the
chapter shows (request paths, where input enters, network calls, credentials,
tests, which actions need permission). Reconcile the chapter's bullet
identifiers to whatever the real app uses.

```text
Inspect this Flask weather app read-only. Do not edit files yet.

Report:
- request paths and handlers
- where user input enters the system
- where network calls happen
- where credentials are read
- what tests exist
- which actions you would need permission to take to improve safety
```
