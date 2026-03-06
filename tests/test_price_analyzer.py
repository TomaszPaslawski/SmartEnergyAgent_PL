import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.price_analyzer import analyze_price_peaks, THRESHOLD_HIGH_PRICE
from unittest.mock import patch, MagicMock



def test_analyze_price_peaks_success():
    """Check function with the correct data for analysis (24 hours)."""

    # Generate test set: 96 entries (24h × 4 = 96 quarters of an hour)
    base_time = datetime(2026, 3, 1, 0, 0, 0)

    data = []
    for i in range(96):
        dtime = base_time + timedelta(minutes=15 * i)

        # Simulation of different prices
        hour = dtime.hour
        if 6 <= hour < 9 or 17 <= hour < 20:
            price = 600.0  # Peak over 500)
        elif 23 <= hour or hour < 6:
            price = 200.0  # Cheap (night)
        else:
            price = 400.0  # Regular

        data.append({"dtime": dtime, "rce_pln": price})

    prices_df = pd.DataFrame(data)

    result = analyze_price_peaks(prices_df)

    # Check overall results
    assert isinstance(result, dict)
    assert "highest_6h_prices" in result
    assert "lowest_3h_prices" in result
    assert "high_price_exceeded" in result
    assert "hourly_status" in result

    # Check if 6 hours with highest prices and 3 hours with lowest prices were found
    assert len(result["highest_6h_prices"]) == 6
    assert len(result["lowest_3h_prices"]) == 3

    # Check if threshold has been passed
    assert result["high_price_exceeded"] == True

    # Check if 24 hours are in hourly_status
    assert len(result["hourly_status"]) == 24


def test_analyze_price_peaks_empty_dataframe():
    """Test with empty DataFrame."""

    prices_df = pd.DataFrame()

    result = analyze_price_peaks(prices_df)

    # Check structure
    assert isinstance(result, dict)
    assert result["highest_6h_prices"] == []
    assert result["lowest_3h_prices"] == []
    assert result["high_price_exceeded"] == False
    assert result["hourly_status"] == []

    assert len(result["details"]) > 0
    assert "empty" in result["details"][0].lower()


def test_analyze_price_peaks_missing_dtime_column():
    """Test when DataFrame does not have column 'dtime'."""

    # DataFrame without  'dtime'
    prices_df = pd.DataFrame({
        "rce_pln": [400.0, 500.0, 300.0]
    })

    result = analyze_price_peaks(prices_df)

    # Check if function does not crash
    assert isinstance(result, dict)
    assert result["highest_6h_prices"] == []
    assert result["lowest_3h_prices"] == []

    # Check error message
    assert any("'dtime'" in detail and "missing" in detail.lower() for detail in result["details"])


def test_analyze_price_peaks_dtime_as_string():
    """Test when 'dtime' is string."""

    data = []
    base_time = datetime(2026, 3, 1, 0, 0, 0)

    for i in range(96):
        dtime = base_time + timedelta(minutes=15 * i)
        data.append({
            "dtime": dtime.strftime("%Y-%m-%d %H:%M:%S"),  # String zamiast datetime
            "rce_pln": 400.0
        })

    prices_df = pd.DataFrame(data)

    result = analyze_price_peaks(prices_df)

    # Function should convert and works normally
    assert isinstance(result, dict)
    assert len(result["highest_6h_prices"]) == 6
    assert len(result["lowest_3h_prices"]) == 3
    assert len(result["hourly_status"]) == 24


def test_analyze_price_peaks_no_threshold_exceeded():
    """Test when price does not pass the threshold 500 PLN/MWh."""

    base_time = datetime(2026, 3, 1, 0, 0, 0)

    data = []
    for i in range(96):
        dtime = base_time + timedelta(minutes=15 * i)
        data.append({
            "dtime": dtime,
            "rce_pln": 300.0  # All prices below 500
        })

    prices_df = pd.DataFrame(data)

    result = analyze_price_peaks(prices_df)

    # Treshold has not been passed
    assert result["high_price_exceeded"] == False

    # All prices should have status "BELOW THRESHOLD"
    assert all(status["status"] == "BELOW THRESHOLD" for status in result["hourly_status"])


def test_analyze_price_peaks_dtime_conversion_error():
    """Test when 'dtime' conversion to DataFrame fails."""

    # DataFrame with 'dtime' NOT convertable
    prices_df = pd.DataFrame({
        "dtime": ["invalid_date", "not_a_datetime", "abc123"],
        "rce_pln": [400.0, 500.0, 300.0]
    })

    result = analyze_price_peaks(prices_df)

    # Function should not crash
    assert isinstance(result, dict)
    assert result["highest_6h_prices"] == []
    assert result["lowest_3h_prices"] == []

    # Conversion message
    assert any("Failed to convert 'dtime'" in detail for detail in result["details"])


def test_analyze_price_peaks_resampling_error():
    """Test when DataFrame structure causes resampling errors."""

    # DataFrame with 'dtime' but without column 'rce_pln'
    prices_df = pd.DataFrame({
        "dtime": [datetime(2026, 3, 1, i, 0, 0) for i in range(24)]
    })

    result = analyze_price_peaks(prices_df)

    assert isinstance(result, dict)
