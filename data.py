#Print neccessary libraries and load data
import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).parent / "CITS1501 Data csv.csv"

daily_weather = pd.read_csv(DATA_FILE, encoding="latin-1")
daily_weather["Date"] = pd.to_datetime(daily_weather["Date"], dayfirst=True)

# Map BoM's long column names to short ones 
COLUMN_MAP = {
    "Date": "date",
    "Minimum temperature": "min_temp",
    "Maximum temperature": "max_temp",
    "Rainfall": "rain",
    "Evaporation": "evap",
    "Sunshine": "sun",
    "9am relative humidity": "rh_9am",
    "3pm relative humidity": "rh_3pm",
    "Speed of maximum wind gust": "max_gust",
}
daily_weather.rename(columns=COLUMN_MAP, inplace=True)

#Define Indigenous seasons mapping
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
daily_weather["season"] = pd.Categorical(
    daily_weather["date"].dt.month.map(MONTH_TO_SEASON),
    categories=SEASONS,
    ordered=True,
)

season_groups = daily_weather.groupby("season", observed=True, sort=True)
print(daily_weather.head())
print(season_groups.size())