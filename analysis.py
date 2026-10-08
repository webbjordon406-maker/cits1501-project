# Analysis functions: each takes the weather DataFrame and returns a result
from data import SEASONS


def season_summary(df):
    """Return one row per season with its average and total weather."""
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
    """Count the days in each season where a column is above (or below) a threshold."""
    if column not in df.columns:
        raise ValueError(f"Unknown column: {column}")

    if above:
        matches = df[df[column] >= threshold]
    else:
        matches = df[df[column] <= threshold]

    # Missing values never pass >= or <=, so they are not counted.
    # fill_value=0 keeps seasons with no matching days in the result.
    counts = matches.groupby("season", observed=False).size()
    return counts.reindex(SEASONS, fill_value=0)


def season_detail(df, season):
    """Return the statistics and weather event counts for one season."""
    if season not in SEASONS:
        raise ValueError(f"Unknown season: {season!r}. Expected one of {SEASONS}")

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
    }


if __name__ == "__main__":
    from data import load_weather, assign_seasons

    weather = assign_seasons(load_weather())
    print(season_summary(weather), "\n")
    for season in SEASONS:
        print(season, season_detail(weather, season)["events"])