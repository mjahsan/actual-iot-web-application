from unittest.mock import patch, MagicMock
import pytest

from data_simulator.simulator import init_db, simulate_data


def test_init_db_success():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch("simulator.psycopg2.connect", return_value=mock_conn):
        init_db()

    mock_cursor.execute.assert_called_once()

    executed_sql = mock_cursor.execute.call_args[0][0]

    assert "CREATE TABLE IF NOT EXISTS sensor_data" in executed_sql

    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


def test_init_db_retries_then_succeeds():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "simulator.psycopg2.connect",
        side_effect=[
            Exception("DB unavailable"),
            mock_conn
        ]
    ) as mock_connect:

        with patch("simulator.time.sleep"):
            init_db()

    assert mock_connect.call_count == 2


def test_simulate_data_single_iteration():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "simulator.psycopg2.connect",
        return_value=mock_conn
    ):

        with patch(
            "simulator.random.choice",
            return_value="SENSOR-NORTH-01"
        ):

            with patch(
                "simulator.random.uniform",
                return_value=2.5
            ):

                with patch(
                    "simulator.time.sleep",
                    side_effect=KeyboardInterrupt
                ):

                    with pytest.raises(KeyboardInterrupt):
                        simulate_data()

    mock_cursor.execute.assert_called()

    sql = mock_cursor.execute.call_args[0][0]

    assert "INSERT INTO sensor_data" in sql

    mock_conn.commit.assert_called()