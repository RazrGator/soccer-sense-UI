import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pandas as pd
from app import app
# from playwright.sync_api import sync_playwright


CSV_PATH = "data.csv"


# Flask client
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client



# Alpha tests
# Page loads tests:

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"SoccerSense" in response.data or b"Home" in response.data

def test_track_page_loads(client):
    response = client.get("/track")

    assert response.status_code == 200

    html_data = response.data.decode().lower()

    assert "enter field size" in html_data

def test_guide_page_loads(client):
    response = client.get("/guide")
    assert response.status_code == 200
    # assert b"enter field size" in response.data.decode().lower()


# def test_overview_page_loads(client):
#     response = client.get("/guide/overview")
#     assert response.status_code == 200
#     assert b"Overview" in response.data or b"Instructions and Guide" in response.data

def test_control_panel_page_loads(client):
    response = client.get("/track/control")
    assert response.status_code == 200
    assert b"Control" in response.data



# Button tests

def test_buttons_bring_to_correct_pages(client):
    response = client.get("/")
    html_data = response.data.decode()
    assert "/" in html_data
    assert "/track" in html_data
    assert "/guide" in html_data


# Check field dimensions tests



# Beta tests

def test_csv_data_is_complete():
    # Test and make sure each row has 4 comma separated values

    csv = pd.read_csv(CSV_PATH)

    for index, row in csv.iterrows():
        assert len(row) == 4

def test_csv_data_has_correct_types():
    # Test and make sure that the values on each row are the correct data type
    csv = pd.read_csv(CSV_PATH)

    assert pd.api.types.is_integer_dtype(csv["id"]) # Test and make sure id column has only integers

    for col in ["distance1", "distance2", "distance3"]:
        assert pd.api.types.is_float_dtype(csv[col]) # Test and make sure distance columns are only floats

def test_distances_are_within_realistic_range():
    # Test and make sure that the values on each row are the correct data type
    csv = pd.read_csv(CSV_PATH)


    for col in ["distance1", "distance2", "distance3"]:
        assert (csv[col] < 300).all() # Test and make sure distances are within realistic range

def test_distances_are_non_negative():
       # Test and make sure that the values on each row are non-negative
    csv = pd.read_csv(CSV_PATH)

    for col in ["distance1", "distance2", "distance3"]:
        assert (csv[col] >= 0).all() # Test and make sure distances are within realistic range
