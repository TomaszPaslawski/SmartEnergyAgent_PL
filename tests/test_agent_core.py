import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import pytz
from src.agent_core import run_daily_agent_logic, PSE_PUBLICATION_HOUR_CET


@patch('src.agent_core.datetime')
def test_run_daily_agent_logic_before_publication_time(mock_datetime):
    """Test security check – agent finishes before publication hour (before 14:00)."""

    # Mock datetime.now() – hour set for 13:30 CET
    poland_tz = pytz.timezone('Europe/Warsaw')
    fake_now = datetime(2026, 3, 10, 13, 30, 0, tzinfo=poland_tz)

    mock_datetime.now.return_value = fake_now
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    result = run_daily_agent_logic(53.75, 17.77)

    # Function should finish earlier (return None)
    assert result is None
    # There should not be calls to API (functions ended before)


@patch('src.agent_core.send_telegram_message')
@patch('src.agent_core.get_weather_forecast')
@patch('src.agent_core.get_electricity_prices_pse')
@patch('src.agent_core.datetime')
def test_run_daily_agent_logic_pse_api_fails(mock_datetime, mock_get_prices, mock_get_weather, mock_telegram):
    """Test PSE API fails (return None)."""

    # Mock datetime.now() – after 14:00 (we have data)
    poland_tz = pytz.timezone('Europe/Warsaw')
    fake_now = datetime(2026, 3, 10, 14, 30, 0, tzinfo=poland_tz)

    mock_datetime.now.return_value = fake_now
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    # Mock PSE API – return None (error)
    mock_get_prices.return_value = None

    result = run_daily_agent_logic(53.75, 17.77)

    # Function should end after PSE error
    assert result is None

    # Weather API should not be called (since PSE API failed)
    mock_get_weather.assert_not_called()

    # Telegram should not be called (same as above)
    mock_telegram.assert_not_called()


import pandas as pd


@patch('src.agent_core.send_telegram_message')
@patch('src.agent_core.get_weather_forecast')
@patch('src.agent_core.analyze_price_peaks')
@patch('src.agent_core.get_electricity_prices_pse')
@patch('src.agent_core.datetime')
def test_run_daily_agent_logic_weather_api_fails(mock_datetime, mock_get_prices, mock_analyze_prices, mock_get_weather,
                                                 mock_telegram):
    """Test Weather API fails (return None)."""

    # Mock datetime.now() – after 14:00
    poland_tz = pytz.timezone('Europe/Warsaw')
    fake_now = datetime(2026, 3, 10, 14, 30, 0, tzinfo=poland_tz)

    mock_datetime.now.return_value = fake_now
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    # Mock PSE API – success (return DataFrame)
    mock_prices_df = pd.DataFrame({
        'dtime': [fake_now],
        'rce_pln': [400.0]
    })
    mock_get_prices.return_value = mock_prices_df

    # Mock analyze_price_peaks – returns results
    mock_analyze_prices.return_value = {
        'highest_6h_prices': [],
        'lowest_3h_prices': [],
        'high_price_exceeded': False,
        'hourly_status': [],
        'details': []
    }

    # Mock Weather API – return None (error)
    mock_get_weather.return_value = None

    result = run_daily_agent_logic(53.75, 17.77)

    # Function should end after API Weather error
    assert result is None

    # Telegram should not be called
    mock_telegram.assert_not_called()


@patch('src.agent_core.send_telegram_message')
@patch('src.agent_core.generate_recommendations')
@patch('src.agent_core.analyze_weather_for_recharge')
@patch('src.agent_core.get_weather_forecast')
@patch('src.agent_core.analyze_price_peaks')
@patch('src.agent_core.get_electricity_prices_pse')
@patch('src.agent_core.datetime')
def test_run_daily_agent_logic_full_success(
        mock_datetime, mock_get_prices, mock_analyze_prices,
        mock_get_weather, mock_analyze_weather, mock_generate_recs, mock_telegram
):
    """Integration smoke test – complete flow works without errors."""

    # Mock datetime.now() – after 14:00
    poland_tz = pytz.timezone('Europe/Warsaw')
    fake_now = datetime(2026, 3, 10, 14, 30, 0, tzinfo=poland_tz)

    mock_datetime.now.return_value = fake_now
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    # Mock PSE API – success
    mock_prices_df = pd.DataFrame({
        'dtime': [fake_now],
        'rce_pln': [400.0]
    })
    mock_get_prices.return_value = mock_prices_df

    # Mock price analysis
    mock_analyze_prices.return_value = {
        'highest_6h_prices': [{'hour': '07:00', 'price': 600.0}],
        'lowest_3h_prices': [{'hour': '02:00', 'price': 100.0}],
        'high_price_exceeded': True,
        'hourly_status': [],
        'details': []
    }

    # Mock Weather API – success
    mock_weather_df = pd.DataFrame({
        'datetime': [fake_now],
        'weather_code': [1],
        'cloud_cover': [20.0]
    })
    mock_get_weather.return_value = mock_weather_df

    # Mock weather analysis
    mock_analyze_weather.return_value = {
        'recharge_favorable': True,
        'favorable_hours_count': 5,
        'total_sunny_hours_in_range': 6,
        'hourly_weather_status': [],
        'details': []
    }

    # Mock recommendations
    mock_generate_recs.return_value = "Test recommendation message"

    # Mock Telegram – success
    mock_telegram.return_value = True

    result = run_daily_agent_logic(53.75, 17.77)

    # Ensure all modules have been called
    mock_get_prices.assert_called_once()
    mock_analyze_prices.assert_called_once()
    mock_get_weather.assert_called_once()
    mock_analyze_weather.assert_called_once()
    mock_generate_recs.assert_called_once()
    mock_telegram.assert_called_once_with("Test recommendation message")
