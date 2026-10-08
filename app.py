"""Flask app for the Nyoongar seasonal weather explorer."""
from pathlib import Path

from flask import Flask, jsonify, send_file

from data import SEASONS, load_weather, assign_seasons, load_season_info
from analysis import season_summary, season_detail

app = Flask(__name__)
PAGES = Path(__file__).parent / "templates"

# Load the weather data and season descriptions once, when the app starts
weather = assign_seasons(load_weather())
season_info = load_season_info()


# --- Helpers ---

def match_season(name):
    """Return the correctly capitalised season name, or None if it isn't valid."""
    for season in SEASONS:
        if season.lower() == name.lower():
            return season
    return None


def to_records(df):
    """Convert a DataFrame into a list of dictionaries that jsonify can send.

    Dates become "YYYY-MM-DD" text, and missing values (NaN) become None,
    because NaN is not allowed in JSON.
    """
    df = df.copy()
    if "date" in df.columns:
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df = df.astype(object).where(df.notna(), None)
    return df.to_dict(orient="records")


# --- Page routes ---

@app.route("/")
def home():
    return send_file(PAGES / "index.html")


@app.route("/season/<name>")
def season_page(name):
    if match_season(name) is None:
        return send_file(PAGES / "error.html"), 404
    return send_file(PAGES / "season.html")


@app.errorhandler(404)
def page_not_found(error):
    return send_file(PAGES / "error.html"), 404


# --- API routes (send data to the pages as JSON) ---

@app.route("/api/summary")
def api_summary():
    summary = season_summary(weather).reset_index()
    events = {season: season_detail(weather, season)["events"] for season in SEASONS}
    return jsonify(
        overview=season_info["overview"],
        note=season_info["note"],
        seasons=SEASONS,
        info=season_info["seasons"],
        summary=to_records(summary),
        events=events,
    )


@app.route("/api/season/<name>")
def api_season(name):
    season = match_season(name)
    if season is None:
        return jsonify(error=f"Unknown season: {name}"), 404

    detail = season_detail(weather, season)
    return jsonify(
        name=season,
        info=season_info["seasons"][season],
        stats=detail["stats"],
        events=detail["events"],
    )


@app.route("/api/daily")
def api_daily():
    daily = weather[["date", "min_temp", "max_temp", "rain", "season"]].copy()
    daily["season"] = daily["season"].astype(str)
    return jsonify(daily=to_records(daily))


if __name__ == "__main__":
    app.run(debug=True)