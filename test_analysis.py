import data
import analysis

weather = data.assign_seasons(data.load_weather())


def test_makuru_total_rain():
    summary = analysis.season_summary(weather)
    assert summary.loc["Makuru", "total_rain"] == 178.4


def test_birak_mean_max_temp():
    summary = analysis.season_summary(weather)
    assert summary.loc["Birak", "mean_max_temp"] == 31.2


def test_makuru_cold_nights():
    detail = analysis.season_detail(weather, "Makuru")
    assert detail["events"]["cold_nights"] == 11


def test_bunuru_hot_days():
    detail = analysis.season_detail(weather, "Bunuru")
    assert detail["events"]["hot_days"] == 14
    
# --- Edge cases ---

def test_summary_with_no_data():
    empty = weather.iloc[0:0]
    summary = analysis.season_summary(empty)
    assert list(summary["days"]) == [0, 0, 0, 0, 0, 0]


def test_season_detail_is_case_insensitive():
    detail = analysis.season_detail(weather, "makuru")
    assert detail["name"] == "Makuru"


def test_threshold_must_be_a_number():
    try:
        analysis.count_extreme_days(weather, "max_temp", "35")
        assert False, "expected a ValueError"
    except ValueError:
        pass

# --- Day matcher (closest_season) ---

def test_hot_dry_day_matches_birak():
    result = analysis.closest_season(weather, 38, 0)
    assert result["season"] == "Birak"


def test_cold_wet_day_matches_makuru():
    result = analysis.closest_season(weather, 16, 20)
    assert result["season"] == "Makuru"


def test_matcher_compares_all_six_seasons():
    result = analysis.closest_season(weather, 24, 2)
    assert len(result["distances"]) == 6


def test_matcher_accepts_numbers_as_text():
    # Form inputs arrive as text, so "38" must work the same as 38
    result = analysis.closest_season(weather, "38", "0")
    assert result["season"] == "Birak"


def test_matcher_accepts_limits():
    # Boundary: 50°C and 0 mm are the edges of the allowed range, so they are accepted
    result = analysis.closest_season(weather, 50, 0)
    assert result["season"] in data.SEASONS


def test_matcher_rejects_blank_input():
    try:
        analysis.closest_season(weather, "", "0")
        assert False, "expected a ValueError"
    except ValueError:
        pass


def test_matcher_rejects_negative_rain():
    try:
        analysis.closest_season(weather, 25, -1)
        assert False, "expected a ValueError"
    except ValueError:
        pass


def test_matcher_rejects_impossible_temperature():
    try:
        analysis.closest_season(weather, 60, 0)
        assert False, "expected a ValueError"
    except ValueError:
        pass


def test_matcher_rejects_text():
    try:
        analysis.closest_season(weather, "hot", 0)
        assert False, "expected a ValueError"
    except ValueError:
        pass


def test_matcher_with_no_data():
    empty = weather.iloc[0:0]
    try:
        analysis.closest_season(empty, 25, 0)
        assert False, "expected a ValueError"
    except ValueError:
        pass 