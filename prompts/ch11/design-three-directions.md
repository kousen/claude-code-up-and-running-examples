/design Three visually distinct directions for the city page of this Flask weather app. The page is templates/city.html with styles in static/css/main.css; the running app is at http://127.0.0.1:5077/Boston if you want to look at the current version. Show each direction as the Boston page at phone width (375px), one artboard per direction, all three on one canvas.

Each direction must commit to concrete, checkable choices, and list those commitments as short bullets under its artboard so a later /goal can be written from them:

- a named color palette with hex values, including the background and text colors, meeting WCAG AA contrast
- how the current conditions block and the five-day forecast are laid out
- whether weather icons appear, and if so how each gets meaningful alt text
- whether there is a Celsius/Fahrenheit toggle, and if so where it sits and whether the choice persists across reloads
- anything else the direction depends on (typography, spacing scale, a hero graphic)

Keep the data the page already shows: city name, date, current temp, condition, daily high/low, wind, and the five-day list. Do not change any Python. Publish the canvas and print its URL.
