# Analysis functions: each takes the weather DataFrame and returns a result
import math

from data import SEASONS

# The range of values the day matcher accepts. Perth's hottest day on record
# is under 50°C and its wettest day under 300 mm, so anything outside these
# limits is almost certainly a typing mistake.
MAX_TEMP_LIMITS = (0, 50)
RAIN_LIMITS = (0, 300)


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
    if not isinstance(threshold, (int, float)):
        raise ValueError(f"Threshold must be a number, not {threshold!r}")
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
    season = season.strip().capitalize()  # accept "makuru", "MAKURU", " Makuru "
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


def to_number(value, label, limits):
    """Turn a user's input into a number, or raise ValueError saying what's wrong.

    Form inputs arrive as text, so "31.5" is accepted as well as 31.5.
    """
    low, high = limits
    if value is None or str(value).strip() == "":
        raise ValueError(f"{label} is required")
    try:
        number = float(value)
    except ValueError:
        raise ValueError(f"{label} must be a number, not {value!r}")
    if math.isnan(number) or not low <= number <= high:
        raise ValueError(f"{label} must be between {low} and {high}")
    return number


def closest_season(df, max_temp, rain):
    """Find the season whose average day is most like the day the user describes.

    For each season we measure how far the user's day is from that season's
    average day, then keep the season with the smallest distance. This is a
    linear search for the minimum: one check per season.

    Temperature and rain use different units, so each gap is divided by the
    spread (standard deviation) of that measure across the whole year. That way
    a 6°C gap and a 5 mm gap both count as "one typical difference", and
    neither measure drowns out the other.
    """
    max_temp = to_number(max_temp, "Maximum temperature", MAX_TEMP_LIMITS)
    rain = to_number(rain, "Rainfall", RAIN_LIMITS)

    averages = df.groupby("season", observed=False)[["max_temp", "rain"]].mean()
    temp_spread = df["max_temp"].std()
    rain_spread = df["rain"].std()

    # With fewer than two days there is no spread; use 1 to avoid dividing by zero
    if not temp_spread > 0:
        temp_spread = 1
    if not rain_spread > 0:
        rain_spread = 1

    best_season = None
    best_distance = None
    distances = {}

    for season in SEASONS:
        avg_temp = averages.loc[season, "max_temp"]
        avg_rain = averages.loc[season, "rain"]
        if math.isnan(avg_temp) or math.isnan(avg_rain):
            continue  # no data for this season, so nothing to compare against

        temp_gap = (max_temp - avg_temp) / temp_spread
        rain_gap = (rain - avg_rain) / rain_spread
        distance = math.sqrt(temp_gap ** 2 + rain_gap ** 2)
        distances[season] = round(distance, 2)

        # Strictly smaller, so on a tie the earlier season in the calendar wins
        if best_distance is None or distance < best_distance:
            best_season = season
            best_distance = distance

    if best_season is None:
        raise ValueError("There is no weather data to compare against")

    return {
        "season": best_season,
        "distances": distances,
        "averages": {
            season: {
                "max_temp": round(float(averages.loc[season, "max_temp"]), 1),
                "rain": round(float(averages.loc[season, "rain"]), 1),
            }
            for season in distances
        },
    }


if __name__ == "__main__":
    from data import load_weather, assign_seasons

    weather = assign_seasons(load_weather())
    print(season_summary(weather), "\n")
    for season in SEASONS:
        print(season, season_detail(weather, season)["events"])