from app import app  # import the Flask app from app.py


def test_summary_route():
    client = app.test_client()          # a fake browser that can call the app
    response = client.get("/api/summary")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["summary"]) == 6


def test_season_route():
    client = app.test_client()
    response = client.get("/api/season/Makuru")
    assert response.status_code == 200
    data = response.get_json()
    assert data["events"]["cold_nights"] == 11


def test_unknown_season_route():
    client = app.test_client()
    response = client.get("/api/season/Summer")
    assert response.status_code == 404


def test_season_page_ignores_capitals():
    client = app.test_client()
    response = client.get("/season/MAKURU")
    assert response.status_code == 200

def test_match_page_loads():
    client = app.test_client()
    response = client.get("/match")
    assert response.status_code == 200


def test_match_route():
    client = app.test_client()
    response = client.get("/api/match?max_temp=16&rain=20")
    assert response.status_code == 200
    data = response.get_json()
    assert data["season"] == "Makuru"


def test_match_route_missing_input():
    client = app.test_client()
    response = client.get("/api/match?max_temp=25")   # no rain given
    assert response.status_code == 400
    assert "error" in response.get_json()
