import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app
# from playwright.sync_api import sync_playwright



# Flask client
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client



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
