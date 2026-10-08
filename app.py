# Flask application for Noongar Seasons website
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, send_file

from data import SEASONS, load_weather, assign_seasons
from analysis import season_summary, season_detail

app = Flask(__name__)
PAGES = Path(__file__).parent / "templates"

# Load and prepare the data once, when the app starts
weather = assign_seasons(load_weather())


# --- Helpers ---

def match_season(name):
    """Return the correctly capitalised season name, or None if it isn't valid.

    Accepts any capitalisation, so "makuru" and "MAKURU" both become "Makuru".
    """
    for season in SEASONS:
        if season.lower() == name.strip().lower():
            return season
    return None


def to_records(df):
    """Convert a DataFrame to a list of dicts that jsonify can handle.

    Dates become "YYYY-MM-DD" strings and NaN becomes None (null in JSON),
    because NaN is not valid JSON.
    """
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%d")
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
    # Any other unknown address also gets the friendly error page
    return send_file(PAGES / "error.html"), 404


# --- API routes ---

@app.route("/api/summary")
def api_summary():
    summary = season_summary(weather).reset_index()
    events = {s: season_detail(weather, s)["events"] for s in SEASONS}
    return jsonify(seasons=SEASONS, summary=to_records(summary), events=events)


@app.route("/api/season/<name>")
def api_season(name):
    season = match_season(name)
    if season is None:
        return jsonify(error=f"Unknown season: {name!r}", valid_seasons=SEASONS), 404

    detail = season_detail(weather, season)
    return jsonify(
        name=detail["name"],
        stats=detail["stats"],
        events=detail["events"],
        daily=to_records(detail["daily"]),
    )


if __name__ == "__main__":
    app.run(debug=True)