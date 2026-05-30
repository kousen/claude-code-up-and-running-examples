# Chapter 3 — Stateless requests demo

A tiny, standalone script that demonstrates that requests to the API are
**stateless**: the server holds no memory between calls. This is the conceptual
reason the Ch. 3 lyrics-trainer saves progress in the browser with
`localStorage` instead of expecting the server to remember it.

The demo sends two separate Anthropic API requests: the first states a name, the
second asks for it. Because each request is independent, the model can't recall
the first — proving the call is stateless.

This script is not part of any of the book's applications — it exists only to
make the point runnable.

## Setup

```bash
cd examples/ch03
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Put your API key in a `.env` file (it's git-ignored, so it won't be committed):

```bash
cp .env.example .env
# then edit .env and set your real key
```

`.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Run

```bash
python stateless_requests.py
```

Optionally override the model (defaults to `claude-opus-4-8`) by adding
`ANTHROPIC_MODEL=...` to `.env`.
