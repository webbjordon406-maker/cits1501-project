# Import necessary libraries
import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).parent / "CITS1501 Data csv.csv"

# Map BoM's long column names to short ones for columns used in analysis and visualisation
COLUMN_MAP = {
    "Date": "date",
    "Minimum temperature (°C)": "min_temp",
    "Maximum temperature (°C)": "max_temp",
    "Rainfall (mm)": "rain",
    "Evaporation (mm)": "evap",
    "Sunshine (hours)": "sun",
    "9am relative humidity (%)": "rh_9am",
    "3pm relative humidity (%)": "rh_3pm",
    "Speed of maximum wind gust (km/h)": "max_gust",
}

# Define Indigenous seasons mapping
SEASONS = ["Birak", "Bunuru", "Djeran", "Makuru", "Djilba", "Kambarang"]
MONTH_TO_SEASON = {
    12: "Birak",
    1: "Birak",
    2: "Bunuru",
    3: "Bunuru",
    4: "Djeran",
    5: "Djeran",
    6: "Makuru",
    7: "Makuru",
    8: "Djilba",
    9: "Djilba",
    10: "Kambarang",
    11: "Kambarang",
}


def load_weather(path=DATA_FILE):
    """Read the BoM CSV, rename columns, parse dates. Return a DataFrame."""
    path = Path(path)

    # 1. Check the file exists
    if not path.exists():
        raise FileNotFoundError(f"Weather data file not found: {path}")

    # 2. Read the CSV (latin-1 handles the degree symbol in BoM headers)
    df = pd.read_csv(path, encoding="latin-1")

    # 3. Rename the columns we use to short names
    df = df.rename(columns=COLUMN_MAP)

    # 4. Check every expected column is present after renaming
    missing = [col for col in COLUMN_MAP.values() if col not in df.columns]
    if missing:
        raise ValueError(f"Data file is missing expected columns: {missing}")

    # 5. Parse dates (Australian day/month/year format)
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    # 6. Return the cleaned DataFrame
    return df


def assign_seasons(df):
    """Return a copy of df with an ordered 'season' column."""
    # 1. Work on a copy so the original DataFrame is unchanged
    df = df.copy()

    # 2. Map each day's month to its Noongar season
    df["season"] = pd.Categorical(
        df["date"].dt.month.map(MONTH_TO_SEASON),
        categories=SEASONS,
        ordered=True,
    )

    # 3. Every row should have a season; stop if any are missing
    if df["season"].isna().any():
        raise ValueError("Some rows could not be assigned a season")

    # 4. Return the DataFrame with the new column
    return df


if __name__ == "__main__":
    weather = assign_seasons(load_weather())
    print(weather.head())
    print(weather.groupby("season", observed=True).size())