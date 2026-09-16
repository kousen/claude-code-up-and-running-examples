/goal The weather app's city page matches the Night Sky mockup in design/DirectionA.dc.html (its commitments are the note-a entry in design/canvas.json), and every item below is proven by command output shown in this session:

1. templates/city.html and static/css/main.css implement the mockup: page background #0f1a24, cards #172634, text #e8eef2, muted text #9fb3c0, accent #f4b942, Manrope from Google Fonts with a system fallback; the current temperature as the hero beside an inline SVG condition icon; the five-day forecast as a vertical list with one inline SVG icon per row. Every icon is an inline SVG with role="img" and an aria-label naming the condition; a condition with no icon falls back to its text. Show the final template with cat templates/city.html.

2. A Celsius/Fahrenheit segmented control sits at the top right: two buttons at least 44px tall, aria-pressed="true" on the active unit, the choice saved in localStorage and reapplied on reload. Temperatures convert client-side from the Celsius values the server already sends. Do not change the routes or the template context in main.py.

3. A new Playwright test file in tests/ (Python, sync API, Chromium) runs against the live app at http://127.0.0.1:5077/Boston and asserts three things: no horizontal scroll at 375px and at 1280px viewports; clicking the °F button changes the hero temperature text and the choice survives page.reload(); every svg[role="img"] has a non-empty aria-label. It passes, shown by python -m pytest tests/ -v output.

4. python -m pytest is green overall, and git status --short shows tests/test_app.py, tests/test_weather_client.py, weather_client.py, and main.py unmodified.

5. npx --no-install lighthouse http://127.0.0.1:5077/Boston --only-categories=accessibility,best-practices --output=json --output-path=./lighthouse.json --chrome-flags="--headless=new" --quiet reports accessibility and best-practices both at 0.95 or higher. Print the two category scores from lighthouse.json with a one-line python3 -c command.

Constraints: do not add Python dependencies; do not edit weather_client.py or main.py; the Flask server is already running on port 5077 with --debug and reloads templates, so do not start another server. Stop after 8 turns and report which items are still unmet.
