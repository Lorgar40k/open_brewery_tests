import pytest
import requests
import allure

BASE_URL = "https://api.openbrewerydb.org/v1/breweries"

@allure.feature("Breweries API")
@allure.story("Get all breweries")
def test_get_all_breweries():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for brewery in data:
        assert "id" in brewery
        assert "name" in brewery
        assert "brewery_type" in brewery

@allure.story("Filter breweries by state")
def test_breweries_by_state():
    state = "California"
    response = requests.get(BASE_URL, params={"by_state": state})
    assert response.status_code == 200
    data = response.json()
    assert all(state.lower() in brewery.get("state", "").lower() for brewery in data)

@allure.story("Filter breweries by type and limit")
def test_breweries_by_type_and_limit():
    params = {"by_type": "micro", "per_page": 5}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert all(brewery["brewery_type"] == "micro" for brewery in data)

@allure.story("Get brewery by ID")
def test_get_brewery_by_id():
    response_all = requests.get(BASE_URL)
    brewery = response_all.json()[0]
    brewery_id = brewery["id"]

    response = requests.get(f"{BASE_URL}/{brewery_id}")
    assert response.status_code == 200
    brewery_detail = response.json()
    assert brewery_detail["id"] == brewery["id"]
    assert brewery_detail["name"] == brewery["name"]
