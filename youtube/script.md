# Script — "One Bash Script Runs Claude Code on Any OpenRouter Model"

> Spoken script with screen cues. `[SCREEN]` = what's on screen, `[B-ROLL]` = cutaway/overlay.
> Brackets are stage directions, not read aloud. Times are targets, not gospel.
> Tone: Ken — dry, fair, technical. No hype, no model-bashing.

---

## COLD OPEN  (0:00–0:30)

[SCREEN: clean terminal, nothing else.]

This is Claude Code.

[Type: `orclaude z-ai/glm-5.2` — let the Claude Code UI boot.]

But the model answering me right now? Not Claude. That's GLM — an open model from a completely
different company. And notice I just typed its name straight from OpenRouter; nothing's hardcoded.

[Beat. Let it sit.]

Same tool, same keybindings, same agent loop — completely different brain behind it. And by the
end of this video, you'll be able to do this with almost any model on OpenRouter, using one tiny
bash wrapper — including, at the very end, running a real coding task for *zero dollars*. Let's get into it.

[Title card.]

---

## THE WHY  (0:30–1:30)

So why would you do this?

A few honest reasons. **Cost** — some of these models are a fraction of the price of frontier models,
and for a lot of tasks that's fine. **Curiosity** — there's a wave of strong open models right now,
DeepSeek, GLM, Kimi, and you might want to actually *use* one inside a real agent instead of a chat box.
And **not being locked in** — Claude Code is a genuinely great harness, and it turns out the harness and
the model are two separate things you can mix and match.

One thing I'm *not* going to do: tell you which model is best. I don't have benchmarks for your code on
your machine, and neither does anyone making that claim on the internet. What I can do is show you how to
try them yourself and judge with your own eyes. That's the whole point — optionality, not a leaderboard.

---

## THE MECHANISM  (1:30–3:30)

Here's the trick, and it's almost embarrassingly simple.

[SCREEN: open `scripts/orclaude` in the editor.]

Claude Code doesn't hardcode Anthropic. It reads a couple of environment variables — a base URL and an
auth token — to decide where to send requests. And OpenRouter publishes an endpoint that speaks the same
API dialect. So you point Claude Code at OpenRouter instead of Anthropic, hand it an OpenRouter key, tell
it which model to use... and the harness has no idea anything changed.

[SCREEN: highlight the export block.]

That's it. Base URL goes to OpenRouter. The auth token is your OpenRouter key. And these three —
opus, sonnet, haiku — those are the model names Claude Code asks for internally. We just remap all of
them to whatever model we actually want.

[SCREEN: highlight the `$1` assignments.]

And here's the whole point: the first argument is the model. Any raw OpenRouter slug — `vendor/model` —
gets copied into all of those Claude Code model tiers. Nothing's hardcoded. If OpenRouter lists it, you
can try Claude Code on it. That's the entire trick, and it's what we're leaning on for the rest of the
video.

[SCREEN: show a small `.claude/settings.local.json` snippet, or lower-third it.]

There is another way to persist the same setup: `.claude/settings.local.json`. That's great when one
project should always run through one routed backend. It is *not* what I'm using here, because this video
is all about switching models quickly. Static JSON pins a repo; this wrapper lets the model be an
argument.

[B-ROLL: openrouter.ai/models page, scrolling.]

Quick honesty note: these model slugs change over time. The ones I'm showing were live when I recorded
this — check OpenRouter for the current names before you copy mine.

---

## THE TASK  (3:30–4:00)

To keep this fair, every model gets the **exact same job**. No cherry-picking.

[SCREEN: show the prompt I'll paste each time.]

> *"In this project, implement `parseDuration` so it turns a string like `1h30m` or `45s` into a total
> number of seconds, then write a couple of tests and run them."*

Small, self-contained, and it forces the model to actually drive the tools — read the file, write code,
run the tests, react to the output. That's the part that separates "can chat about code" from "can
operate an agent." Same task, every model. Let's run it.

---

## THE RUN  (4:00–9:30)

> For each model: paste the same prompt, then narrate only three things —
> **did it finish, how clean was the tool use, and rough speed.** ~45–60s each. Let the terminal breathe.

> Order: **explicit models first** (anchor the viewer), **then the routers**, with `free` as the finale.

### 1 — `z-ai/glm-5.2`  (explicit)
[Type: `orclaude z-ai/glm-5.2`]

We start with models I name explicitly. GLM first — one I reach for a lot. Same task, here we go.

[Run task. Comment on completion + tool use.]

### 2 — `deepseek/deepseek-v4-flash`  (explicit)
[Type: `orclaude deepseek/deepseek-v4-flash`]

DeepSeek's flash model — built to be fast and cheap. This is the kind of model you'd actually leave
running on routine edits.

[Run task. Comment on speed especially.]

### 3 — latest Kimi  (explicit)  ⚠️ confirm exact slug on OpenRouter on record day
[Type: `orclaude moonshotai/kimi-<latest>`]

The latest Kimi. Kimi's models are tuned for coding work, so I'm curious how its tool use compares.

[Run task.]

### 4 — (optional full-circle) `anthropic/claude-opus-4.1`  (explicit)
[Type: `orclaude anthropic/claude-opus-4.1`]

One more explicit one, just to make the point land: I can route *Claude itself* back through the same
script, through OpenRouter. The harness genuinely does not care who's behind the curtain.

[Run task. Short.]

---

> **PIVOT** — this is where the video turns. Slow down here.

So far I've been *naming* the model every time. But OpenRouter has something different: routers, where
*it* picks the model for you. Watch what happens.

### 5 — `openrouter/auto`  (router — the mystery beat)
[Type: `orclaude openrouter/auto`]

`openrouter/auto` analyzes the prompt and chooses a model for me. I don't pick anything.

[Run task. Comment on completion + tool use.]

Now here's the quirk worth pausing on. I asked OpenRouter to pick the model — but Claude Code won't
tell me which one it picked. Up here it just says `openrouter/auto`, and that's all you get.

[SCREEN: point at the model indicator still reading the router slug.]

And the frustrating part is the answer *exists*. OpenRouter's own response includes a field naming the
model it chose — when I run this same router from Spring AI, I get the full response object and the
model name is right there. The terminal just doesn't show it. So where do you actually look?

[SCREEN: switch to OpenRouter Activity dashboard, find the request.]

Right here — OpenRouter's activity console logs the real model that served each request. That's your
peek behind the curtain. And honestly, that gap *is* the lesson of this whole video: the harness and
the model are separate layers, and here's a spot where you can feel the seam.

### 6 — `openrouter/free`  (router — the finale)
[Type: `orclaude openrouter/free`]

And the one I saved for last, because it's the most fun: the free router. Same idea as `auto`, but
restricted to free models — so this entire task runs for **zero dollars**. Same opacity, by the way;
the terminal says `openrouter/free`, and the dashboard tells you what actually ran.

[Run task. Be honest about throttling/latency if it shows. Check the dashboard to reveal the model.]

You're obviously trading something for free — usually speed, or rate limits — but the fact that you can
drive a real coding agent, on a real task, for nothing? That still gets me.

---

## THE HONEST VERDICT  (9:30–11:00)

So what actually happened.

[SCREEN: side-by-side or quick recap montage of the runs.]

The headline: **every one of these spoke the protocol well enough to run inside Claude Code.** That alone
is kind of remarkable. The harness — the file editing, the tool loop, the permissions — that all came
from Claude Code, not the model.

Where they differed was the *tool use*. [Fill in with what you actually observed — e.g. "some models
nailed the read-edit-test loop on the first try; others got confused on multi-step tool calls or needed
a nudge."] That's the real lesson here: a big chunk of what makes Claude Code feel good is the harness,
and the model underneath is swappable — but not *equally* good at being swapped in. Coding-tuned models
and the bigger ones drove the tools more cleanly. The cheaper and free ones got the job done but with
more wobble.

[Beat.]

I'm not going to hand you a ranking, because the right answer depends on your code, your budget, and
your patience. But now you can run this experiment yourself in about ten seconds per model.

---

## BOOK TIE-IN + CTA  (11:00–end)

This whole topic — running Claude Code on other models through OpenRouter — is something I'm covering in
my new book, **Claude Code: Up and Running**. It'll land in Chapter 12; that chapter's coming to the
early release a bit later, so consider this an early preview.

The `orclaude` script is in the book's example repo — link in the description. Grab it, point it at
whatever model you're curious about, and let me know in the comments which one surprised you. I did not
expect [whichever model] to do as well as it did.

And if you want to see the *other* side of this — running these same models from Java, with Spring AI
2.0, where you actually *can* get the router to tell you which model it picked — I've got a companion
video on that. Link on screen.

If you want more of this — the harness, the models, the weird corners of agentic coding — subscribe,
and I'll see you in the next one.

[End card.]

---

## Post-production notes
- Lower-third each model's slug as it runs, so viewers can copy it.
- Overlay OpenRouter's *actual* price for a couple of models from the dashboard — real numbers only.
- Keep the API key off-screen at all times (it's in an env var; don't `echo` it).
- If a model fails the task live, **keep it in** and say so — honest failure is on-brand and useful.
