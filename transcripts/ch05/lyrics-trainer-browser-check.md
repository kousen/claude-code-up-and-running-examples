# ch05 lyrics trainer browser check

Date captured: 2026-05-22

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples/lyrics-trainer/ch05-navigation
```

Commands:

```bash
npm test
python3 -m http.server 8005
bash ~/.codex/skills/playwright/scripts/playwright_cli.sh open http://127.0.0.1:8005 --headed
bash ~/.codex/skills/playwright/scripts/playwright_cli.sh snapshot
bash ~/.codex/skills/playwright/scripts/playwright_cli.sh click e8
bash ~/.codex/skills/playwright/scripts/playwright_cli.sh press ArrowRight
bash ~/.codex/skills/playwright/scripts/playwright_cli.sh click e7
```

Unit-test output:

```text
Test Files  2 passed (2)
Tests       17 passed (17)
```

Browser snapshot highlights:

```text
Initial:
- heading "Sonnet 18 -- Line by Line"
- Line 1 of 14
- Shall I compare thee to a summer's day?
- buttons: Previous, Next

After clicking Next:
- Line 2 of 14
- Thou art more lovely and more temperate:

After pressing ArrowRight:
- Line 3 of 14
- Rough winds do shake the darling buds of May,

After clicking Previous:
- Line 2 of 14
- Thou art more lovely and more temperate:
```

Console note:

```text
The only browser console error was a harmless 404 for /favicon.ico from the
temporary Python static server.
```
