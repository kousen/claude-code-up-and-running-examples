# Outline — "One Bash Script Runs Claude Code on Any OpenRouter Model"

**Target length:** 10–12 min long-form.
**Spine:** one identical coding task, run through the *same* Claude Code harness, swapping only the model behind it.
**Promise to the viewer:** by the end they can `orclaude <any-model>` and judge the models for themselves.

---

## The mechanism (the one thing that makes this possible)

Claude Code reads `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN`. OpenRouter exposes an
Anthropic-compatible endpoint. So you point Claude Code at OpenRouter, hand it an OpenRouter
API key, and name the model — the harness never knows the difference. `scripts/orclaude`
is a tiny bash wrapper that sets those variables, points the tier env vars at its first argument,
and `exec`s `claude --model <slug> "$@"`.

Show `scripts/orclaude` on screen. The load-bearing line is the last one: the slug goes straight
through as `--model`, which outranks any model pinned in `settings.json` (the tier env vars alone
get silently ignored when settings pin a concrete model ID — that's a real bug we hit). Same
mechanism `ollama launch claude` uses. The tier vars stay as backup for sub-agents.

Proof beat: `scripts/orclaude-smoke <slug>` runs one headless prompt and checks the `modelUsage`
key — which model the request was *billed* against. Don't ask the model its name; it answers from
under Claude Code's system prompt and claims to be Claude Code.

Mention the project-local alternative briefly: `.claude/settings.local.json` can persist the same
`env` values when one repository should always use one routed backend (template ships as
`scripts/settings.local.json.example`). It is not the demo path, because this video needs to swap
models every run.

---

## Model lineup for the demo

Two **routers** (OpenRouter picks the model) + a spread of **specific models**. Keep the task identical.

**Demo order: explicit models first, then routers.** Concrete-then-abstract — name the models the
viewer can anchor on, *then* reveal that you don't have to pick one at all. `openrouter/free` goes
**last** as the "$0, and very different" kicker.

| Order | Slug | Kind | Why it's in the video |
|------:|------|------|----------------------|
| 1 | `z-ai/glm-5.2` | explicit | In Ken's regular rotation. Also the cold open. |
| 2 | `deepseek/deepseek-v4-flash` | explicit | Fast, cheap, coding-capable |
| 3 | `moonshotai/kimi-…` (latest) | explicit | Coding-tuned. ⚠️ use the **latest** Kimi — confirm exact slug on OpenRouter on record day |
| 4 | `anthropic/claude-opus-4.1` | explicit (optional) | Full-circle: route *real Claude* through the same script |
| 5 | `openrouter/auto` | **router** | OpenRouter picks the model. Triggers the routed-model-mystery beat. |
| 6 | `openrouter/free` | **router** | Free models only, $0. The finale. Confirmed working 2026-06-26 (Spring AI 2.0). |

> **Demo with raw slugs, not aliases.** The script treats its first argument as the OpenRouter model
> string. Typing `orclaude z-ai/glm-5.2` tells the durable story: the model choice lives on the
> command line, not inside the wrapper.

**Router reality (confirmed in OpenRouter docs — accurate on camera):** there are exactly **two** built-in
router *slugs*:
- `openrouter/auto` — analyzes the prompt and selects a (paid) model (powered by NotDiamond).
- `openrouter/free` — filters free models to those with the capabilities your request needs (vision,
  tool-calling, structured output), then **randomly** picks one from that pool.

Both **return the chosen model's name in the API response** — Claude Code's terminal just doesn't display
it (that's the mystery beat). The other items in the docs sidebar — `:free` model-variant suffix, Latest
Model Resolution, Body Builder, Model Fallbacks — are routing **strategies/parameters**, not `openrouter/*`
slugs, so Claude Code can't exercise them the same way. Two demoable routers, not a long menu — pitch it that way.

**Optional full-circle (#5):** routing real Claude back through the same script proves the mechanism is
genuinely model-agnostic — the harness doesn't care who's behind the curtain. Place it as the last
*explicit* model, right before the pivot to routers.

> ✅ **All seven slugs confirmed working 2026-06-26** in a Spring AI 2.0 app — including `openrouter/free`.
> Still re-check on record day: OpenRouter slugs drift, and the script's own comments (lines 22, 30) say
> "re-check before publishing." A throwaway run of each before you hit record is cheap insurance.

---

## The router-opacity beat (don't bury this — it's good content)

Real limitation, discovered live: when you run a **router** (`openrouter/auto`, `openrouter/free`),
Claude Code in the terminal just echoes back the router slug — it **never tells you which actual
model served the request.** And here's the kicker: OpenRouter's docs confirm the response *includes a
`model` field* naming the chosen model. So the data is right there in the API reply — Spring AI surfaces
it via the full `ClientResponse` metadata; Claude Code's terminal just doesn't display it. Not missing
data, hidden data.

Turn the limitation into a payoff on camera:
- **Workaround:** open OpenRouter's **Activity / usage dashboard** after the run — each request is logged
  with the real model that served it. That's how you reveal what `auto` / `free` actually picked.
- **Honest framing:** "The harness hides it; the API doesn't. Here's where to look." This is exactly the
  harness-vs-model distinction the whole video is about — a perfect concrete example of it.

---

## Structure

1. **Cold open (0:00–0:30)** — terminal already open. Type `orclaude xiaomi/mimo-v2.5` and let the
   Claude Code UI boot with a non-Anthropic model. "That's Claude Code. That is *not* Claude running it.
   By the end of this video you'll be able to do that with almost any model on the planet."

2. **The why (0:30–1:30)** — one honest sentence on each: cost, trying frontier open models, not being
   locked to one vendor, learning what the harness vs. the model each contribute. *No* "X beats Claude"
   claims — this video is about optionality, not a leaderboard.

3. **The mechanism (1:30–3:30)** — show `scripts/orclaude`. Walk the env vars, then land on the
   `--model` flag as the line that guarantees the slug wins (tier env vars alone lose to a pinned
   settings model). Run `orclaude-smoke` as the proof beat — includes the "DeepSeek said it was
   Claude Code" story. Mention `.claude/settings.local.json` as the static per-project version, then
   explain why the video uses the script for fast model switching. This is the teachable core.

4. **The task (3:30–4:00)** — define ONE small, judgeable task and show it once. Keep it identical for
   every model so the comparison is fair. (Suggested task in `script.md`.)

5. **The run (4:00–9:30)** — run the task through each model in the order above: **explicit models first**
   (GLM → DeepSeek → Kimi → optional Claude full-circle), **then the pivot** ("now you don't even
   pick a model") into the **routers** (`auto`, then `free` as the finale). For each: ~45–60s. Call out
   three things only — did it complete the task, how did the tool-use feel (clean vs. confused), rough
   speed/cost. The routed-model-mystery beat lives in the `auto` run. Don't over-narrate; let the terminal carry it.

6. **The honest verdict (9:30–11:00)** — where it's seamless, where it gets weird. Be specific:
   some models drive Claude Code's tool calls cleanly, others fumble multi-step tool use or subagents.
   This honesty *is* the value — "here's the catch" is better content than pretending it's flawless.

7. **Book tie-in + CTA (11:00–end)** — this connects to *Claude Code: Up and Running* (Chapter 12,
   coming to the early release later). Soft: "the script's in the book's example repo, link below."

---

## Honesty guardrails (from CLAUDE.md)

- Describe features; **do not** rank models or claim one "beats" another without benchmarks.
- No invented cost/speed multipliers on screen. If you show a price, show OpenRouter's actual number.
- Flag anything you haven't verified live. "I think this is cheaper" → just show the dashboard instead.

## Assets / prep checklist

- [ ] `OPENROUTER_API_KEY` exported in the recording shell (don't show the key on camera).
- [ ] `scripts/orclaude` on PATH or aliased.
- [ ] `scripts/orclaude-smoke <slug>` run once against the recording shell — a settings.json model
      pin or stray `ANTHROPIC_API_KEY` in the profile will silently sabotage the demo otherwise.
- [ ] Every slug above verified live on openrouter.ai/models.
- [ ] One clean sample project + the chosen task staged and reset between runs.
- [ ] OpenRouter Activity dashboard open in a tab (to reveal what the routers picked).
- [ ] Decide: commit `youtube/` to the repo, or keep it local? (folder is git-ignorable either way)

---

## Companion video idea (separate upload)

**"Run Any OpenRouter Model from Spring AI 2.0"** — the same model lineup, but from Java instead of
the CLI. Natural pair to this video, and it's where you can show the thing CC *can't* do: pull the full
`ClientResponse`, read the metadata, and print the actual model a router chose. Cross-link the two videos
(end screen + description). Same book, likely same chapter neighborhood. Worth its own title-scoring pass.
