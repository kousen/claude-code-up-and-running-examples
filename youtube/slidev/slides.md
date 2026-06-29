---
theme: default
title: One Bash Script Runs Claude Code on Any OpenRouter Model
info: |
  Tales from the jar side — companion to *Claude Code: Up and Running* (O'Reilly).
  Point Claude Code at any OpenRouter model with one tiny bash script.
colorSchema: dark
highlighter: shiki
lineNumbers: false
fonts:
  sans: Inter
  mono: JetBrains Mono
drawings:
  persist: false
transition: slide-left
mdc: true
---

# One bash script runs Claude Code on **any** OpenRouter model

<div class="opacity-70 text-xl mt-2">Tales from the jar side</div>

Same harness. Same keybindings. Same agent loop — a completely different brain behind it.

```bash
❯ orclaude z-ai/glm-5.2
✓ Claude Code ready
  model  z-ai/glm-5.2
  route  via OpenRouter
```

<div class="opacity-60 text-sm mt-2 font-mono">That's Claude Code. That is <span class="text-orange-400">not</span> Claude running it.</div>

<!--
Cold open. Terminal already open. Type `orclaude z-ai/glm-5.2` and let Claude Code boot on a non-Anthropic model. "This is Claude Code. The model answering me is not Claude."
-->

---

# Three honest reasons to swap the model

<div class="grid grid-cols-3 gap-6 mt-8">

<div class="border-t-2 border-cyan-400 pt-4">
<div class="text-cyan-400 font-mono text-sm">01</div>
<div class="text-2xl font-bold mt-2 mb-2">Cost</div>
<div class="opacity-70">Some models are a fraction of frontier prices — and for a lot of tasks, that's perfectly fine.</div>
</div>

<div class="border-t-2 border-cyan-400 pt-4">
<div class="text-cyan-400 font-mono text-sm">02</div>
<div class="text-2xl font-bold mt-2 mb-2">Curiosity</div>
<div class="opacity-70">A wave of strong open models — DeepSeek, GLM, Kimi — that you can actually drive inside a real agent.</div>
</div>

<div class="border-t-2 border-cyan-400 pt-4">
<div class="text-cyan-400 font-mono text-sm">03</div>
<div class="text-2xl font-bold mt-2 mb-2">No lock-in</div>
<div class="opacity-70">The harness and the model are separate layers. Claude Code is great — the brain stays swappable.</div>
</div>

</div>

<!--
Three honest reasons: cost, curiosity about strong open models, and not being locked to one vendor. The harness and the model are two separate things you can mix and match.
-->

---
layout: center
class: text-center
---

# This isn't a leaderboard.<br>It's <span class="text-cyan-400">optionality</span>.

<div class="opacity-70 text-xl max-w-3xl mx-auto mt-6">
No benchmarks for your code, on your machine — and neither has anyone making that claim online. I'll show you how to try them yourself and judge with your own eyes.
</div>

<!--
I'm not going to tell you which model is best. No benchmarks for your code on your machine. The point is optionality, not a leaderboard.
-->

---
layout: section
---

<div class="font-mono text-cyan-400 tracking-widest text-sm uppercase">01 · The mechanism</div>

# It's almost embarrassingly simple

<div class="opacity-70 text-xl mt-4">
Claude Code doesn't hardcode Anthropic. It reads a couple of environment variables to decide where its requests go — and which model to ask for.
</div>

<!--
Now the teachable core: how Claude Code can be pointed at another endpoint.
-->

---

# Point the harness somewhere else

<div class="grid grid-cols-[1fr_auto_1fr] gap-6 items-center mt-8">

<div class="border border-gray-600 rounded-lg p-6">
<div class="text-xl font-bold mb-2">Claude Code</div>
<div class="opacity-70">The harness — file edits, tool loop, permissions.</div>
</div>

<div class="text-center font-mono text-xs text-cyan-300 space-y-2">
<div class="border border-gray-600 rounded px-2 py-1">ANTHROPIC_BASE_URL</div>
<div class="border border-gray-600 rounded px-2 py-1">ANTHROPIC_AUTH_TOKEN</div>
<div class="border border-gray-600 rounded px-2 py-1">ANTHROPIC_MODEL</div>
<div class="text-cyan-400 text-3xl">→</div>
</div>

<div class="border border-cyan-500 rounded-lg p-6">
<div class="text-xl font-bold mb-2 text-cyan-400">OpenRouter</div>
<div class="opacity-70">An Anthropic-compatible endpoint, fronting hundreds of models.</div>
</div>

</div>

<div class="text-center text-lg mt-8">
Hand it an OpenRouter key, name the model you want — <span class="text-cyan-400 font-semibold">and the harness has no idea anything changed.</span>
</div>

<!--
Claude Code reads three env vars: a base URL, an auth token, and a model. OpenRouter publishes an Anthropic-compatible endpoint. Point the base URL there, hand it an OpenRouter key, set the model. The harness has no idea anything changed.
-->

---
layout: two-cols
layoutClass: gap-8
---

<div class="font-mono text-cyan-400 tracking-widest text-xs uppercase">scripts/orclaude</div>

# The whole thing

<v-clicks>

- Point the base URL at OpenRouter. Auth token → your OpenRouter key.
- Set `ANTHROPIC_MODEL` to the slug you passed in — the model **you** typed is the one that runs.
- `exec claude` — that's it. No remapping, no aliases, no `case` block.

</v-clicks>

<div class="opacity-50 text-sm mt-6 border-l-2 border-cyan-600 pl-3">
Slugs drift over time. These were live on record day — check OpenRouter for current names.
</div>

::right::

```bash
#!/usr/bin/env bash

# point the harness at OpenRouter
export ANTHROPIC_BASE_URL=openrouter.ai/api/v1
export ANTHROPIC_AUTH_TOKEN=$OPENROUTER_API_KEY

# the model is just the first argument
export ANTHROPIC_MODEL="$1"
shift

# hand off to Claude Code
exec claude "$@"
```

<!--
Show scripts/orclaude. It's tiny: set the base URL to OpenRouter, set the auth token to your OpenRouter key, set the model to whatever slug you passed in, then exec claude with the rest of the arguments. No remapping, no case block, no aliases. The slug you type is the model that runs.
-->

---
layout: two-cols
layoutClass: gap-8
---

<div class="font-mono text-cyan-400 tracking-widest text-xs uppercase">Don't like wrapper scripts?</div>

# Set it in a file instead

<v-clicks>

- Claude Code reads the same three variables from an `env` block in `.claude/settings.local.json`.
- The `.local` file is git-ignored — your OpenRouter key never lands in version control.
- Persistent and per-project, instead of per-command. Same effect — pick whichever fits.

</v-clicks>

<div class="opacity-50 text-sm mt-6 border-l-2 border-cyan-600 pl-3">
<span class="font-mono">ANTHROPIC_*</span> is just the variable name Claude Code reads — the value is your OpenRouter key. No Anthropic account needed.
</div>

::right::

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "openrouter.ai/api/v1",
    "ANTHROPIC_AUTH_TOKEN": "sk-or-…",
    "ANTHROPIC_MODEL": "z-ai/glm-5.2"
  }
}
```

<!--
If you'd rather not keep a wrapper script on your PATH, Claude Code reads the same settings from a JSON file. Put an env block in .claude/settings.local.json with the same three variables. The .local file is git-ignored by default, so your OpenRouter key never lands in version control. Use whichever fits your workflow; the book covers both.
-->

---
layout: section
---

<div class="font-mono text-cyan-400 tracking-widest text-sm uppercase">02 · The task</div>

# Same job, every model

<div class="opacity-70 text-xl mt-4">
No cherry-picking. One small, self-contained task that forces the model to actually drive the tools.
</div>

<!--
To keep it fair, every model gets the exact same job.
-->

---
layout: center
class: text-center
---

<div class="font-mono text-cyan-400 tracking-widest text-xs uppercase mb-6">The prompt — pasted verbatim, every run</div>

<div class="border border-gray-600 rounded-xl p-8 max-w-3xl mx-auto text-2xl font-light leading-relaxed text-left">
Implement <span class="font-mono text-cyan-400">parseDuration</span> so it turns a string like <span class="font-mono text-green-400">1h30m</span> or <span class="font-mono text-green-400">45s</span> into a total number of seconds, then write a couple of tests and run them.
</div>

<div class="font-mono text-cyan-300 mt-8 text-lg">
read → write → test → react
</div>

<div class="opacity-60 mt-2">The full tool loop — not just chatting about code.</div>

<!--
Show the prompt I paste each time: implement parseDuration so 1h30m or 45s becomes total seconds, write a couple of tests, run them. Read file, write code, run tests, react to output. That's what separates chatting about code from operating an agent.
-->

---
layout: section
---

<div class="font-mono text-cyan-400 tracking-widest text-sm uppercase">03 · The run</div>

# Six models, one task

<div class="opacity-70 text-xl mt-4">
Explicit models first — then the routers, with <span class="font-mono text-cyan-400">free</span> saved for last.
</div>

<!--
Run the task through each model. Explicit models first to anchor the viewer, then the routers, with free as the finale.
-->

---

# The lineup

<div class="text-sm opacity-60 mb-4">Watch three things: Did it finish? · Clean tool use? · Speed &amp; cost?</div>

<div class="grid grid-cols-3 gap-4">

<div class="border border-gray-600 rounded-lg p-4">
<div class="flex justify-between text-xs"><span class="font-mono text-cyan-300">01</span><span class="text-cyan-300">EXPLICIT</span></div>
<div class="text-xl font-bold mt-1">GLM</div>
<div class="font-mono text-sm opacity-60">z-ai/glm-5.2</div>
</div>

<div class="border border-gray-600 rounded-lg p-4">
<div class="flex justify-between text-xs"><span class="font-mono text-cyan-300">02</span><span class="text-cyan-300">EXPLICIT</span></div>
<div class="text-xl font-bold mt-1">DeepSeek</div>
<div class="font-mono text-sm opacity-60">deepseek/deepseek-v4-flash</div>
</div>

<div class="border border-gray-600 rounded-lg p-4">
<div class="flex justify-between text-xs"><span class="font-mono text-cyan-300">03</span><span class="text-cyan-300">EXPLICIT</span></div>
<div class="text-xl font-bold mt-1">Kimi</div>
<div class="font-mono text-sm opacity-60">moonshotai/kimi-latest</div>
</div>

<div class="border border-gray-600 rounded-lg p-4">
<div class="flex justify-between text-xs"><span class="font-mono text-cyan-300">04</span><span class="text-cyan-300">EXPLICIT</span></div>
<div class="text-xl font-bold mt-1">Claude — full circle</div>
<div class="font-mono text-sm opacity-60">anthropic/claude-opus-4.6</div>
</div>

<div class="border border-cyan-500 rounded-lg p-4">
<div class="flex justify-between text-xs"><span class="font-mono text-cyan-300">05</span><span class="text-cyan-400 font-bold">ROUTER</span></div>
<div class="text-xl font-bold mt-1">Auto</div>
<div class="font-mono text-sm opacity-60">openrouter/auto</div>
</div>

<div class="border border-cyan-500 rounded-lg p-4">
<div class="flex justify-between text-xs"><span class="font-mono text-cyan-300">06</span><span class="text-green-400 font-bold">$0 ROUTER</span></div>
<div class="text-xl font-bold mt-1">Free</div>
<div class="font-mono text-sm opacity-60">openrouter/free</div>
</div>

</div>

<!--
The running order. Explicit models GLM, DeepSeek, Kimi, then Claude full-circle, then routers auto and free. For each, watch three things only: did it finish, how clean was the tool use, rough speed and cost.
-->

---
layout: two-cols
layoutClass: gap-8
---

<div class="font-mono text-cyan-300 text-sm">01 / 06 · EXPLICIT MODEL</div>

# GLM

<div class="font-mono text-cyan-400 text-xl mb-4">z-ai/glm-5.2</div>

A strong open model, and one in my regular rotation. We start here so the rest has a baseline.

::right::

```bash
❯ orclaude z-ai/glm-5.2
  model  z-ai/glm-5.2
❯ _
```

<!--
Model 1, GLM. One I reach for a lot. Same task, here we go. Comment on completion and tool use.
-->

---
layout: two-cols
layoutClass: gap-8
---

<div class="font-mono text-cyan-300 text-sm">02 / 06 · EXPLICIT MODEL</div>

# DeepSeek

<div class="font-mono text-cyan-400 text-xl mb-4">deepseek/deepseek-v4-flash</div>

The flash model — built to be fast and cheap. The kind you'd actually leave running on routine edits.

::right::

```bash
❯ orclaude deepseek/deepseek-v4-flash
  model  deepseek-v4-flash
❯ _
```

<!--
Model 2, DeepSeek flash. Built to be fast and cheap; the kind of model you'd leave running on routine edits. Comment on speed especially.
-->

---
layout: two-cols
layoutClass: gap-8
---

<div class="font-mono text-cyan-300 text-sm">03 / 06 · EXPLICIT MODEL</div>

# Kimi

<div class="font-mono text-cyan-400 text-xl mb-4">moonshotai/kimi-latest</div>

Moonshot's models are tuned for coding work — so the real question is how cleanly it drives the tools.

::right::

```bash
❯ orclaude moonshotai/kimi-latest
  model  kimi-latest
❯ _
```

<!--
Model 3, latest Kimi. Confirm exact slug on OpenRouter on record day. Kimi's models are tuned for coding work, so I'm curious how its tool use compares.
-->

---
layout: two-cols
layoutClass: gap-8
---

<div class="font-mono text-cyan-300 text-sm">04 / 06 · FULL CIRCLE</div>

# Claude, through the same script

<div class="font-mono text-cyan-400 text-xl mb-4">anthropic/claude-opus-4.6</div>

Route real Claude back through OpenRouter to make the point land: the harness doesn't care who's behind the curtain.

::right::

```bash
❯ orclaude anthropic/claude-opus-4.6
  model  claude-opus-4.6
  route  Anthropic via OpenRouter
❯ _
```

<!--
Model 4, the full-circle. Route Claude itself back through the same script, through OpenRouter. The harness genuinely does not care who's behind the curtain. Keep it short.
-->

---
layout: center
class: text-center
---

<div class="font-mono text-cyan-400 tracking-widest text-sm uppercase">The pivot</div>

# Now you don't even <span class="text-cyan-400">pick the model</span>

<div class="opacity-70 text-xl max-w-3xl mx-auto mt-6">
Up to now I've <span class="opacity-100 font-semibold">named</span> the model every time. OpenRouter has routers — where <span class="opacity-100 font-semibold">it</span> picks the model for you.
</div>

<!--
This is where the video turns. Slow down. So far I've been naming the model every time. OpenRouter has routers, where it picks the model for you. Watch what happens.
-->

---
layout: two-cols
layoutClass: gap-8
---

<div class="font-mono text-cyan-300 text-sm">05 / 06 · ROUTER</div>

# Auto

<div class="font-mono text-cyan-400 text-xl mb-4">openrouter/auto</div>

OpenRouter analyzes the prompt and chooses a model for me. I don't pick anything.

::right::

```bash
❯ orclaude openrouter/auto
  model   openrouter/auto
  picked  ??? — not shown
❯ _
```

<!--
Router auto. Analyzes the prompt and chooses a model for me; I pick nothing. Run the task. Then the quirk: Claude Code won't tell you which model it picked.
-->

---

# A router won't tell you which model it picked

<div class="grid grid-cols-3 gap-4 mt-8">

<div class="border border-gray-600 rounded-lg p-5">
<div class="text-2xl mb-3">🔒</div>
<div class="font-bold mb-2">The harness hides it</div>
<div class="opacity-70 text-sm">Claude Code's terminal just echoes <span class="font-mono">openrouter/auto</span> — never the model that actually served you.</div>
</div>

<div class="border border-gray-600 rounded-lg p-5">
<div class="text-2xl mb-3">🔍</div>
<div class="font-bold mb-2">The API doesn't</div>
<div class="opacity-70 text-sm">The response includes a <span class="font-mono text-green-400">model</span> field naming the choice. Not missing data — hidden data.</div>
</div>

<div class="border border-cyan-500 rounded-lg p-5">
<div class="text-2xl mb-3">📊</div>
<div class="font-bold mb-2 text-cyan-400">Where to look</div>
<div class="opacity-70 text-sm">OpenRouter's Activity dashboard logs the real model behind every request. Your peek behind the curtain.</div>
</div>

</div>

<div class="text-center text-lg mt-8">
That gap <span class="text-cyan-400">is</span> the lesson — the harness and the model are separate layers, and here you can feel the seam.
</div>

<!--
The quirk worth pausing on. I asked OpenRouter to pick the model but Claude Code won't tell me which one. The answer exists: the API response includes the model field. The terminal just doesn't show it. Look in the OpenRouter Activity dashboard. The harness hides it; the API doesn't.
-->

---
layout: two-cols
layoutClass: gap-8
---

<div class="font-mono text-cyan-300 text-sm">06 / 06 · THE FINALE</div>

# <span class="text-green-400 text-6xl">$0</span><br>A real coding task, for nothing

<div class="font-mono text-cyan-400 text-xl my-4">openrouter/free</div>

Same idea as auto, restricted to free models. You trade something — speed, rate limits — but the agent still runs.

::right::

```bash
❯ orclaude openrouter/free
  model  openrouter/free
  cost   $0.00
❯ _
```

<!--
The finale. The free router. Same idea as auto, restricted to free models, so the whole task runs for zero dollars. Same opacity; the dashboard tells you what actually ran. You trade speed or rate limits, but driving a real coding agent for nothing still gets me.
-->

---
layout: two-cols
layoutClass: gap-8
---

<div class="font-mono text-cyan-300 text-sm">One more router flavor</div>

# Always run the newest version

The **latest-model router** is the opposite of a mystery. You name the family with a <span class="font-mono text-cyan-400">~</span> prefix; OpenRouter resolves it to the newest concrete model in that family.

<v-clicks>

- Never pin a stale version — and never edit a slug when a new release drops.
- Unlike `auto` / `free`, it's **predictable** — the response names the exact version it resolved to.

</v-clicks>

::right::

```bash
❯ orclaude ~anthropic/claude-opus-latest
  asked   ~anthropic/claude-opus-latest
  served  claude-opus-4.6  ← newest
❯ _
```

<!--
One more router flavor worth knowing, and it's the opposite of the mystery. The latest-model router uses a tilde prefix: ~anthropic/claude-opus-latest. You name the family; OpenRouter always resolves it to the newest concrete version in that family. So you never pin a stale version, and you never edit a slug when a new release drops. Unlike auto and free, this one isn't a mystery: the API response names the exact concrete model it resolved to. Claude Code's terminal still won't print it, but the activity dashboard will, and it's predictable by design.
-->

---
layout: section
---

<div class="font-mono text-cyan-400 tracking-widest text-sm uppercase">04 · The honest verdict</div>

# What actually happened

<!--
The honest verdict: where it's seamless, where it gets weird.
-->

---

# Harness vs. model

<div class="grid grid-cols-2 gap-6 mt-6">

<div class="border border-gray-600 border-l-4 border-l-green-400 rounded-lg p-6">
<div class="text-xs font-bold tracking-widest text-green-400 mb-3">WHAT HELD UP</div>
<div class="text-2xl font-bold mb-3">Every model ran inside Claude Code</div>
<div class="opacity-70">The file editing, the tool loop, the permissions — that all came from the harness, not the model. That alone is kind of remarkable.</div>
</div>

<div class="border border-gray-600 border-l-4 border-l-orange-400 rounded-lg p-6">
<div class="text-xs font-bold tracking-widest text-orange-400 mb-3">WHERE IT GOT WEIRD</div>
<div class="text-2xl font-bold mb-3">The tool use varied</div>
<div class="opacity-70">Coding-tuned and bigger models drove the tools cleanly. The cheaper and free ones got there — with more wobble.</div>
</div>

</div>

<div class="text-center text-xl mt-8 max-w-4xl mx-auto">
No ranking from me — the right answer depends on <span class="text-cyan-400">your</span> code, <span class="text-cyan-400">your</span> budget, and <span class="text-cyan-400">your</span> patience. Now you can run the experiment yourself in about ten seconds per model.
</div>

<!--
The headline: every model spoke the protocol well enough to run inside Claude Code. The harness came from Claude Code, not the model. Where they differed was tool use: coding-tuned and bigger models drove the tools cleanly; cheaper and free ones wobbled. No ranking; the right answer depends on your code, budget, and patience.
-->

---
layout: two-cols
layoutClass: gap-8
---

<div class="font-mono text-cyan-400 tracking-widest text-xs uppercase">From the book</div>

# Claude Code:<br>Up and Running

O'Reilly Media — this whole topic lands in **Chapter 12**, coming to the early release a little later. Consider this an early preview.

<div class="border border-cyan-500 rounded-lg p-4 mt-6 font-mono inline-block">
<span class="text-cyan-400">❯</span> orclaude <span class="opacity-60">lives in the book's example repo — link below.</span>
</div>

::right::

<div class="flex items-center justify-center h-full">
<img src="/ccur_early_access_cover.jpeg" class="rounded shadow-2xl max-h-100" alt="Claude Code: Up and Running" />
</div>

<!--
This ties into my book, Claude Code: Up and Running, from O'Reilly. The OpenRouter material lands in Chapter 12, coming to the early release a bit later. The orclaude script is in the book's example repo.
-->

---
layout: center
class: text-center
---

# Point it at any model —<br>and tell me which one surprised you

<div class="opacity-70 text-xl max-w-3xl mx-auto mt-4">
Grab <span class="font-mono text-cyan-400">orclaude</span> from the example repo, run the experiment yourself, and drop a comment.
</div>

<div class="grid grid-cols-2 gap-6 mt-8 text-left max-w-3xl mx-auto">

<div class="border border-gray-600 rounded-lg p-5">
<div class="text-xs font-bold tracking-widest text-cyan-300 mb-2">WATCH NEXT</div>
<div class="font-bold mb-1">The same models, from Java</div>
<div class="opacity-70 text-sm">Spring AI 2.0 — where you <span class="opacity-100">can</span> get the router to name the model it picked.</div>
</div>

<div class="border border-gray-600 rounded-lg p-5">
<div class="text-xs font-bold tracking-widest text-cyan-300 mb-2">LINKS IN DESCRIPTION</div>
<div class="font-bold mb-1">Script + the book</div>
<div class="opacity-70 text-sm">The example repo and <span class="opacity-100">Claude Code: Up and Running</span> early release.</div>
</div>

</div>

<div class="font-mono text-cyan-300 text-sm mt-8 tracking-widest">TALES FROM THE JAR SIDE</div>

<!--
Grab the script, point it at whatever model you're curious about, tell me in the comments which one surprised you. Companion video: running these same models from Spring AI 2.0 in Java, where you can get the router to tell you which model it picked. Subscribe.
-->
