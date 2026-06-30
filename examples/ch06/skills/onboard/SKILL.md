---
name: onboard
description: Generate a CODEBASE.md architecture overview and a Slidev PRESENTATION.md for new team members. Use for unfamiliar projects where someone needs to come up to speed quickly.
context: fork
model: opus
user-invocable: true
---

# Codebase Onboarding Generator

This skill runs in a forked subagent so the broad discovery work doesn't pollute the parent conversation's context. The parent receives a concise summary; the full analysis lives in the generated files.

## Procedure

1. **Analyze project structure**
   - Top-level layout, build tooling, language and framework versions
   - Key entry points, primary modules, integration points
   - Notable conventions (testing, error handling, configuration, naming)

2. **Write `CODEBASE.md`**
   - Architecture overview (high-level + per-module)
   - Setup and run instructions
   - Key patterns to know — what's idiomatic in *this* repo
   - Gotchas — things that surprised you while exploring
   - Where to start reading (5-10 file pointers)

3. **Generate `PRESENTATION.md`** in Slidev format
   - 12-20 slides covering the same ground
   - Use the same conventions as `slides.md` if one exists in the repo

4. **Note** any TODOs you found that look like onboarding-relevant footguns.

Use a professional, practical tone. Skip marketing fluff — new team members need to *do work*, not be sold on the project.
