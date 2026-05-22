import string

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

from weather_client import OpenWeatherClient, WeatherConfigError, WeatherLookupError


load_dotenv()


def normalize_city(raw_city):
    """Return a display-friendly city name, or an empty string for blank input."""
    return string.capwords((raw_city or "").strip())


def create_app(weather_client=None):
    app = Flask(__name__)
    app.config["WEATHER_CLIENT"] = weather_client or OpenWeatherClient.from_env()

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            city = normalize_city(request.form.get("search"))
            if not city:
                return (
                    render_template(
                        "index.html",
                        error_message="Please enter a city name.",
                    ),
                    400,
                )
            return redirect(url_for("weather", city=city))

        return render_template("index.html")

    @app.route("/<city>")
    def weather(city):
        city_name = normalize_city(city)
        if not city_name:
            return redirect(url_for("error"))

        try:
            report = app.config["WEATHER_CLIENT"].get_weather(city_name)
        except WeatherConfigError:
            return (
                render_template(
                    "error.html",
                    error_message="The weather service is not configured.",
                ),
                500,
            )
        except WeatherLookupError:
            return redirect(url_for("error"))

        return render_template("city.html", **report.to_template_context())

    @app.route("/error")
    def error():
        return render_template(
            "error.html",
            error_message="This city does not exist. Please try again.",
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
