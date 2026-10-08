import data

weather = data.assign_seasons(data.load_weather())


def test_total_days():
    assert len(weather) == 365


def test_birak_days():
    # Birak is December (31 days) + January (31 days)
    assert (weather["season"] == "Birak").sum() == 62


def test_bunuru_days():
    # Bunuru is February (28 days) + March (31 days)
    assert (weather["season"] == "Bunuru").sum() == 59


def test_first_date_is_read_day_first():
    # The CSV's first row is "1/10/2025", which means 1 October 2025
    assert str(weather["date"].iloc[0].date()) == "2025-10-01"