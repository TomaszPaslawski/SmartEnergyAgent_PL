import pandas as pd
from datetime import datetime, timedelta
import requests
import pytest
from unittest.mock import patch, MagicMock
import json
from src.data_fetcher import get_electricity_prices_pse, PSE_API_BASE_URL

# --- Mcok with JSON with 96 entries ---
# Generated for 2026-02-04
MOCK_PSE_RESPONSE_JSON = {
    "value": []
}

base_delivery_datetime = datetime(2026, 2, 4, 0, 0, 0)  # Delivery day midnight
base_publication_datetime = datetime(2026, 2, 3, 13, 55, 15)  # Publication time

for i in range(96):
    delivery_time = base_delivery_datetime + timedelta(minutes=15 * i)
    dummy_price = 400 + (i % 20 * 10) + (i % 5 * 2)

    hour_of_delivery = delivery_time.hour
    if 6 <= hour_of_delivery < 9 or 16 <= hour_of_delivery < 20:
        dummy_price += 200
    elif 23 <= hour_of_delivery or hour_of_delivery < 5:
        dummy_price -= 50

    if i == 0:  # Special case for 00:00:00, which has period 23:45-24:00 of previous day
        actual_dtime_str = "2026-02-04 00:00:00"
        period_str = "23:45 - 24:00"
        business_date_str = "2026-02-03"
    else:
        actual_dtime_str = (base_delivery_datetime + timedelta(minutes=15 * i)).strftime("%Y-%m-%d %H:%M:%S")
        period_start_time = (base_delivery_datetime + timedelta(minutes=15 * (i - 1))).strftime("%H:%M")
        period_end_time = (base_delivery_datetime + timedelta(minutes=15 * i)).strftime("%H:%M")
        period_str = f"{period_start_time} - {period_end_time}"
        business_date_str = "2026-02-04"

    MOCK_PSE_RESPONSE_JSON["value"].append({
        "dtime": actual_dtime_str,
        "period": period_str,
        "rce_pln": round(dummy_price, 2),
        "dtime_utc": (delivery_time - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "period_utc": "dummy_period_utc",
        "business_date": business_date_str,
        "publication_ts": (base_publication_datetime + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S.%f"),
        "publication_ts_utc": (base_publication_datetime - timedelta(hours=1) + timedelta(minutes=i)).strftime(
            "%Y-%m-%d %H:%M:%S.%f")
    })


# --- Tests ---
def test_get_electricity_prices_pse_success():
    """
    Test if get_electricity_prices_pse returns a DataFrame on successful API call.
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_PSE_RESPONSE_JSON
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        test_delivery_date = "2026-02-04"
        result_df = get_electricity_prices_pse(test_delivery_date)

        assert isinstance(result_df, pd.DataFrame)
        assert not result_df.empty
        assert len(result_df) == 96

        assert result_df['dtime'].dt.date.iloc[0] == datetime.strptime(test_delivery_date, "%Y-%m-%d").date()
        assert result_df['dtime'].dt.date.iloc[-1] == datetime.strptime(test_delivery_date, "%Y-%m-%d").date()

        expected_url = PSE_API_BASE_URL

        publication_date = (datetime.strptime(test_delivery_date, "%Y-%m-%d").date() - timedelta(days=1))
        expected_filter_start = publication_date.isoformat() + "T00:00:00"
        expected_filter_end = (publication_date + timedelta(days=1)).isoformat() + "T00:00:00"
        expected_filter = f"dtime ge '{expected_filter_start}' and dtime lt '{expected_filter_end}'"

        mock_get.assert_called_once_with(
            expected_url,
            params={'$filter': expected_filter}
        )

def test_get_electricity_prices_pse_api_error_http():
    """
    Test if get_electricity_prices_pse returns None on HTTP API error (e.g., 404, 500).
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = mock_response

        test_date = "2026-02-04"
        result_df = get_electricity_prices_pse(test_date)

        assert result_df is None
        mock_get.assert_called_once()


def test_get_electricity_prices_pse_json_decode_error():
    """
    Test if get_electricity_prices_pse returns None on JSON decoding error.
    This happens if API returns non-JSON content but with a 2xx status.
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = json.decoder.JSONDecodeError("Expecting value", "doc",
                                                                      0)  # <--- Simulate JSON error

        mock_get.return_value = mock_response

        test_date = "2026-02-04"
        result_df = get_electricity_prices_pse(test_date)

        assert result_df is None
        mock_get.assert_called_once()


def test_get_electricity_prices_pse_empty_value_key():
    """
    Test if get_electricity_prices_pse returns an empty DataFrame when 'value' key is present but empty.
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"value": []}
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        test_date = "2026-02-04"
        result_df = get_electricity_prices_pse(test_date)

        assert isinstance(result_df, pd.DataFrame)
        assert result_df.empty
        mock_get.assert_called_once()


@pytest.mark.parametrize("exception_type", [

requests.exceptions.RequestException,
ValueError,
Exception,
])

def test_get_electricity_prices_pse_handles_exceptions(exception_type):
    with patch('requests.get') as mock_get:
        mock_get.side_effect = exception_type("Test error message")

        result = get_electricity_prices_pse("2026-02-04")

        assert result is None


def test_get_electricity_prices_pse_missing_value_key():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"error": "no data", "status": "empty"}
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        result_df = get_electricity_prices_pse("2026-02-04")

        assert isinstance(result_df, pd.DataFrame)
        assert not result_df.empty
        assert len(result_df) == 1