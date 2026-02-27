import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from src.weather_fetcher import get_weather_forecast
from datetime import datetime, timedelta

example_latitude = 53.7535
example_longitude = 17.7752

# --- Ensuring the forecast will be for tomorrow ---
current_actual_date = datetime.now().date()
tomorrow_actual_date = current_actual_date + timedelta(days=1)
target_date_for_forecast = tomorrow_actual_date.strftime('%Y-%m-%d')


def test_get_weather_forecast_success():
    with patch('src.weather_fetcher.openmeteo_requests.Client') as mock_client:
        # === MOCK RESPONSE ===
        mock_response = MagicMock()
        mock_response.UtcOffsetSeconds.return_value = 3600

        # === MOCK HOURLY ===
        mock_hourly = MagicMock()
        mock_hourly.Time.return_value = 1700000000
        mock_hourly.TimeEnd.return_value = 1700086400
        mock_hourly.Interval.return_value = 3600

        mock_values = np.array([20.0] * 24)

        def mock_variables(index):
            mock_var = MagicMock()
            mock_var.ValuesAsNumpy.return_value = mock_values
            return mock_var

        mock_hourly.Variables = mock_variables

        mock_response.Hourly.return_value = mock_hourly

        mock_openmeteo = MagicMock()
        mock_openmeteo.weather_api.return_value = [mock_response]
        mock_client.return_value = mock_openmeteo

        result = get_weather_forecast(example_latitude, example_longitude, target_date_for_forecast)

        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert len(result) == 24


def test_get_weather_forecast_empty_response():
    with patch('src.weather_fetcher.openmeteo') as mock_openmeteo:
        mock_openmeteo.weather_api.return_value = []

        result = get_weather_forecast(53.75, 17.77, "2026-02-04")

        assert result is None

@pytest.mark.parametrize("exception_type", [
    Exception,
    ConnectionError,
    TimeoutError,
])
def test_get_weather_forecast_handles_exceptions(exception_type):
    with patch('src.weather_fetcher.openmeteo') as mock_openmeteo:
        mock_openmeteo.weather_api.side_effect = exception_type("API error")

        result = get_weather_forecast(53.75, 17.77, "2026-02-04")

        assert result is None


def test_get_weather_forecast_hourly_is_none():
    with patch('src.weather_fetcher.openmeteo') as mock_openmeteo:
        mock_response = MagicMock()
        mock_response.Hourly.return_value = None  # Hourly zwraca None
        mock_response.Latitude.return_value = 53.75
        mock_response.Longitude.return_value = 17.77
        mock_response.Elevation.return_value = 100
        mock_response.Timezone.return_value = "Europe"
        mock_response.TimezoneAbbreviation.return_value = "/Berlin"
        mock_response.UtcOffsetSeconds.return_value = 3600

        mock_openmeteo.weather_api.return_value = [mock_response]

        result = get_weather_forecast(53.75, 17.77, "2026-02-04")

        assert result is None


def test_get_weather_forecast_missing_variables():
    with patch('src.weather_fetcher.openmeteo') as mock_openmeteo:
        mock_response = MagicMock()
        mock_response.Latitude.return_value = 53.75
        mock_response.Longitude.return_value = 17.77
        mock_response.Elevation.return_value = 100
        mock_response.Timezone.return_value = "Europe"
        mock_response.TimezoneAbbreviation.return_value = "/Berlin"
        mock_response.UtcOffsetSeconds.return_value = 3600

        mock_hourly = MagicMock()
        mock_hourly.Time.return_value = 1700000000
        mock_hourly.Interval.return_value = 3600

        # Variables(8) error → not enough variables
        def mock_variables(index):
            if index >= 5:  # only 5 variables
                raise Exception("Variable not found")
            mock_var = MagicMock()
            mock_var.ValuesAsNumpy.return_value = [20.0] * 24
            return mock_var

        mock_hourly.Variables = mock_variables
        mock_response.Hourly.return_value = mock_hourly
        mock_openmeteo.weather_api.return_value = [mock_response]

        result = get_weather_forecast(53.75, 17.77, "2026-02-04")

        assert result is None