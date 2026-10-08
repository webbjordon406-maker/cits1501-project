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