#Import necessary libraries and functions
import pandas as pd
import matplotlib.pyplot as plt
from data import SEASONS, MONTH_TO_SEASON
 
#Seasonal Summary
def season_summary(df):
    summary = df.groupby("season", observed=False).agg(
        days=("date", "count"),
        mean_min_temp=("min_temp", "mean"),
        mean_max_temp=("max_temp", "mean"),
        total_rain=("rain", "sum"),
        mean_sun=("sun", "mean"),
        mean_rh_3pm=("rh_3pm", "mean"),
    )
    # Make sure all six seasons appear, in calendar order
    return summary.reindex(SEASONS).round(1)

def count_extreme_days(df, column, threshold, above=True):
    # Count extreme days per season based on the given threshold and direction (above or below)
    if column not in df.columns:
        raise ValueError(f"Unknown column: {column}")
 
    if above:
        matches = df[df[column] >= threshold]
    else:
        matches = df[df[column] <= threshold]
 
    # Missing values (NaN) never satisfy >= or <=, so they are not counted
    counts = matches.groupby("season", observed=False).size()
    return counts.reindex(SEASONS, fill_value=0)
 
 
def season_detail(df, season):
    # Accept any capitalisation, e.g. "makuru" or "MAKURU"
    matched = [s for s in SEASONS if s.lower() == str(season).strip().lower()]
    if not matched:
        raise ValueError(f"Unknown season: {season!r}. Expected one of {SEASONS}")
    season = matched[0]
    days = df[df["season"] == season].sort_values("date")
 
    events = {
        "hot_days": int(count_extreme_days(df, "max_temp", 35)[season]),
        "extreme_heat_days": int(count_extreme_days(df, "max_temp", 40)[season]),
        "cold_nights": int(count_extreme_days(df, "min_temp", 5, above=False)[season]),
        "rain_days": int(count_extreme_days(df, "rain", 1)[season]),
        "heavy_rain_days": int(count_extreme_days(df, "rain", 10)[season]),
    }
 
    return {
        "name": season,
        "stats": season_summary(df).loc[season].to_dict(),
        "events": events,
        "daily": days[["date", "min_temp", "max_temp", "rain"]],
    }


def plot_season_events(df):
    event_names = {
        "hot_days": "Hot days (>=35 C)",
        "extreme_heat_days": "Extreme heat (>=40 C)",
        "cold_nights": "Cold nights (<=5 C)",
        "rain_days": "Rain days (>=1 mm)",
        "heavy_rain_days": "Heavy rain (>=10 mm)",
    }
    event_counts = {
        season: season_detail(df, season)["events"]
        for season in SEASONS
    }
    colors = ["#e76f51", "#b23a48", "#457b9d", "#2a9d8f", "#e9c46a"]
    bar_width = 0.15
    season_positions = list(range(len(SEASONS)))

    fig, ax = plt.subplots(figsize=(11, 6))
    for event_index, (event_key, event_label) in enumerate(event_names.items()):
        offset = (event_index - (len(event_names) - 1) / 2) * bar_width
        positions = [position + offset for position in season_positions]
        values = [event_counts[season][event_key] for season in SEASONS]
        ax.bar(positions, values, width=bar_width, label=event_label,
               color=colors[event_index])

    ax.set_title("Weather Events by Noongar Season")
    ax.set_xlabel("Season")
    ax.set_ylabel("Count of days")
    ax.set_xticks(season_positions, SEASONS)
    ax.set_ylim(bottom=0)
    ax.legend(title="Event", frameon=False)
    ax.grid(axis="y", linestyle=":", alpha=0.45)
    ax.set_axisbelow(True)
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    from data import load_weather, assign_seasons
 
    weather = assign_seasons(load_weather())
    print(season_summary(weather), "\n")
    print("Makuru = ", (season_detail(weather, "makuru")["events"], "\n"))
    print("Bunuru = ", (season_detail(weather, "bunuru")["events"], "\n"))
    print("Birak = ", (season_detail(weather, "birak")["events"], "\n"))
    print("Djeran = ", (season_detail(weather, "djeran")["events"], "\n"))
    print("Djilba = ", (season_detail(weather, "djilba")["events"], "\n"))
    print("Kambarang = ", (season_detail(weather, "kambarang")["events"], "\n"))
    plot_season_events(weather)
