from unittest.mock import patch, MagicMock
import pytest

from dashboard_app.app import app, get_live_data


def test_get_live_data_success():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [
        ("SENSOR-NORTH-01", 2.5, 0, "2026-06-22 10:00:00")
    ]

    mock_conn.cursor.return_value = mock_cursor

    with patch("dashboard_app.app.psycopg2.connect", return_value=mock_conn):
        result = get_live_data()

    assert len(result) == 1
    assert result[0][0] == "SENSOR-NORTH-01"

    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


def test_get_live_data_db_failure():
    with patch(
        "dashboard_app.app.psycopg2.connect",
        side_effect=Exception("Database unavailable")
    ):
        result = get_live_data()

    assert result[0][0] == "Error"
    assert "Database unavailable" in result[0][1]


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_index_route_returns_200(client):
    fake_data = [
        ("SENSOR-NORTH-01", 2.5, 0, "2026-06-22 10:00:00")
    ]

    with patch("dashboard_app.app.get_live_data", return_value=fake_data):
        response = client.get("/")

    assert response.status_code == 200
    assert b"SENSOR-NORTH-01" in response.data


def test_index_route_handles_error_record(client):
    fake_data = [
        ("Error", "Could not connect to DB", 0, "N/A")
    ]

    with patch("dashboard_app.app.get_live_data", return_value=fake_data):
        response = client.get("/")

    assert response.status_code == 200
    assert b"Error" in response.data