# Import necessary libraries
import json
from pathlib import Path

import pandas as pd

DATA_FILE = Path(__file__).parent / "CITS1501 Data csv.csv"
INFO_FILE = Path(__file__).parent / "seasons.json"

# Map BoM's long column names to the short names used in the app
COLUMN_MAP = {
    "Date": "date",
    "Minimum temperature (°C)": "min_temp",
    "Maximum temperature (°C)": "max_temp",
    "Rainfall (mm)": "rain",
    "Sunshine (hours)": "sun",
    "3pm relative humidity (%)": "rh_3pm",
}

# The six Nyoongar seasons, in calendar order, and the months each one covers
SEASONS = ["Birak", "Bunuru", "Djeran", "Makuru", "Djilba", "Kambarang"]
MONTH_TO_SEASON = {
    12: "Birak", 1: "Birak",
    2: "Bunuru", 3: "Bunuru",
    4: "Djeran", 5: "Djeran",
    6: "Makuru", 7: "Makuru",
    8: "Djilba", 9: "Djilba",
    10: "Kambarang", 11: "Kambarang",
}


def load_weather(path=DATA_FILE):
    """Read the BoM CSV, keep the columns we use, and parse dates."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Weather data file not found: {path}")

    # latin-1 handles the degree symbol in BoM's column names
    df = pd.read_csv(path, encoding="latin-1")
    df = df.rename(columns=COLUMN_MAP)

    missing = [col for col in COLUMN_MAP.values() if col not in df.columns]
    if missing:
        raise ValueError(f"Data file is missing expected columns: {missing}")

    # Keep only the columns the app uses
    df = df[list(COLUMN_MAP.values())]

    # Dates are in Australian day/month/year format
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    return df


def assign_seasons(df):
    """Return a copy of df with a 'season' column, in calendar order."""
    df = df.copy()
    df["season"] = pd.Categorical(
        df["date"].dt.month.map(MONTH_TO_SEASON),
        categories=SEASONS,
        ordered=True,
    )

    if df["season"].isna().any():
        raise ValueError("Some rows could not be assigned a season")
    return df


def load_season_info(path=INFO_FILE):
    """Read the season descriptions from seasons.json."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Season information file not found: {path}")

    with open(path, encoding="utf-8") as f:
        info = json.load(f)

    if set(info["seasons"]) != set(SEASONS):
        raise ValueError(f"seasons.json must describe exactly these seasons: {SEASONS}")
    return info


if __name__ == "__main__":
    weather = assign_seasons(load_weather())
    print(weather.head())
    print(weather.groupby("season", observed=True).size())