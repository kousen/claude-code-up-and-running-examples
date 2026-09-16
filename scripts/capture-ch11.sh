#!/usr/bin/env bash
# Capture one ch11 run: scripts/capture-ch11.sh <prompt-name> <app-dir>
# Example: scripts/capture-ch11.sh goal-naive weather-app/ch11-goal-loop-naive
# Reads prompts/ch11/<prompt-name>.md, runs it headless in auto mode, and
# writes transcripts/ch11/<prompt-name>-stream.jsonl (+ -stderr.log).
set -euo pipefail
name="$1"; dir="$2"
root="$(cd "$(dirname "$0")/.." && pwd)"
prompt="$root/prompts/ch11/$name.md"
out="$root/transcripts/ch11/$name-stream.jsonl"
export OWM_API_KEY="${OWM_API_KEY:-${OPENWEATHERMAP_API_KEY:-}}"
cd "$root/$dir"
echo "running $name in $dir -> $out"
claude -p "$(cat "$prompt")" --permission-mode auto \
  --output-format stream-json --verbose > "$out" 2> "${out%-stream.jsonl}-stderr.log"
echo "exit $? ; $(wc -l < "$out") lines"
