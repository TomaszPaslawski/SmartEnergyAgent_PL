import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.weather_analyzer import (
    analyze_weather_for_recharge,
    SUNNY_HOURS_START,
    SUNNY_HOURS_END,
    PV_FAVORABLE_WEATHER_CODES,
    MAX_CLOUD_COVER_FOR_PV_RECHARGE
)


def test_analyze_weather_for_recharge_favorable():
    """Weather test - favorable conditions for PV loading."""

    # Data generation: 24 hours (10-16 = sunny)
    base_time = datetime(2026, 3, 1, 0, 0, 0)

    data = []
    for hour in range(24):
        dt = base_time + timedelta(hours=hour)

        # 10:00-16:00 = favorable weather (kod 0-2, clouds <35%)
        if 10 <= hour < 16:
            weather_code = 1  # Mainly clear
            cloud_cover = 20.0
        else:
            weather_code = 3  # Overcast
            cloud_cover = 80.0

        data.append({
            "datetime": dt,
            "weather_code": weather_code,
            "cloud_cover": cloud_cover,
            "temperature_2m": 20.0
        })

    weather_df = pd.DataFrame(data)

    # Call function
    result = analyze_weather_for_recharge(weather_df)

    assert isinstance(result, dict)
    assert "recharge_favorable" in result
    assert "favorable_hours_count" in result
    assert "total_sunny_hours_in_range" in result
    assert "hourly_weather_status" in result

    # Check favorable hours
    assert result["total_sunny_hours_in_range"] == 6
    assert result["favorable_hours_count"] == 6

    assert result["recharge_favorable"] == True

    # Check if 24 hours in status
    assert len(result["hourly_weather_status"]) == 24


def test_analyze_weather_for_recharge_unfavorable():
    """TWeather test - not favorable conditions for PV loading."""

    base_time = datetime(2026, 3, 1, 0, 0, 0)

    data = []
    for hour in range(24):
        dt = base_time + timedelta(hours=hour)

        # 10:00-16:00 (2/6 = 33% < 60%)
        if 10 <= hour < 12:  # Only 2 hours favorable in charging window
            weather_code = 1
            cloud_cover = 20.0
        else:
            weather_code = 61  # Rain
            cloud_cover = 90.0

        data.append({
            "datetime": dt,
            "weather_code": weather_code,
            "cloud_cover": cloud_cover
        })

    weather_df = pd.DataFrame(data)
    result = analyze_weather_for_recharge(weather_df)

    # 6 sunny hours but, only 2 favorable
    assert result["total_sunny_hours_in_range"] == 6
    assert result["favorable_hours_count"] == 2

    # 2/6 = 33% < 60% → not favorable
    assert result["recharge_favorable"] == False


def test_analyze_weather_for_recharge_empty_dataframe():
    """Test with emoty DataFrame."""

    weather_df = pd.DataFrame()
    result = analyze_weather_for_recharge(weather_df)

    assert isinstance(result, dict)
    assert result["recharge_favorable"] == False
    assert result["favorable_hours_count"] == 0
    assert result["total_sunny_hours_in_range"] == 0
    assert any("empty" in detail.lower() for detail in result["details"])


def test_analyze_weather_for_recharge_missing_column():
    """Test missing column: 'weather_code'."""

    base_time = datetime(2026, 3, 1, 0, 0, 0)

    # DataFrame without 'weather_code'
    data = [
        {
            "datetime": base_time + timedelta(hours=h),
            "cloud_cover": 20.0
        }
        for h in range(24)
    ]

    weather_df = pd.DataFrame(data)
    result = analyze_weather_for_recharge(weather_df)

    assert isinstance(result, dict)
    assert result["recharge_favorable"] == False
    assert any("'weather_code'" in detail and "missing" in detail for detail in result["details"])


def test_analyze_weather_for_recharge_datetime_not_datetime():
    """Test column 'datetime' is not datetime type."""

    # 'datetime' as string
    data = [
        {
            "datetime": "2026-03-01 10:00:00",
            "weather_code": 1,
            "cloud_cover": 20.0
        }
        for _ in range(24)
    ]

    weather_df = pd.DataFrame(data)
    result = analyze_weather_for_recharge(weather_df)

    assert isinstance(result, dict)
    assert result["recharge_favorable"] == False
    assert any("not of datetime type" in detail for detail in result["details"])


def test_analyze_weather_for_recharge_no_sunny_hours_data():
    """Test lack of data in period 10:00-16:00."""

    base_time = datetime(2026, 3, 1, 0, 0, 0)

    # Data only for hours: 0-9 and 17-23 (missing 10-16)
    data = []
    for hour in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 18, 19, 20, 21, 22, 23]:
        data.append({
            "datetime": base_time + timedelta(hours=hour),
            "weather_code": 1,
            "cloud_cover": 20.0
        })

    weather_df = pd.DataFrame(data)
    result = analyze_weather_for_recharge(weather_df)

    assert result["total_sunny_hours_in_range"] == 0
    assert result["favorable_hours_count"] == 0
    assert result["recharge_favorable"] == False
    assert any("No weather data found for core sunny hours" in detail for detail in result["details"])


@pytest.mark.parametrize("weather_code, expected_status", [
    (0, "PV Favorable"),  # Clear sky
    (1, "PV Favorable"),  # Mainly clear
    (2, "PV Favorable"),  # Partly cloudy
    (3, "Overcast"),  # Overcast
    (51, "Rainy/Cloudy"),  # Drizzle
    (61, "Rainy/Cloudy"),  # Rain
    (71, "Snowy/Cloudy"),  # Snow
    (85, "Snowy/Cloudy"),  # Snow showers
    (45, "Foggy"),  # Fog
    (48, "Foggy"),  # Depositing rime fog
    (95, "Thunderstorm/Severe Weather"),  # Thunderstorm
    (99, "Thunderstorm/Severe Weather"),  # Thunderstorm with hail
])
def test_analyze_weather_status_codes(weather_code, expected_status):
    """Test of weather codes and statuses."""

    base_time = datetime(2026, 3, 1, 0, 0, 0)

    # 24 hours with the same code
    data = [
        {
            "datetime": base_time + timedelta(hours=h),
            "weather_code": weather_code,
            "cloud_cover": 20.0
        }
        for h in range(24)
    ]

    weather_df = pd.DataFrame(data)
    result = analyze_weather_for_recharge(weather_df)

    # Check if weather status appears in hourly_weather_status
    assert len(result["hourly_weather_status"]) == 24

    # Check if at least one hour has expected status
    statuses = [entry["status"] for entry in result["hourly_weather_status"]]
    assert expected_status in statuses


def test_analyze_weather_for_recharge_no_timezone():
    """Test when 'datetime' does not have information about timezone."""

    base_time = datetime(2026, 3, 1, 0, 0, 0)  # Bez timezone

    data = [
        {
            "datetime": base_time + timedelta(hours=h),
            "weather_code": 1,
            "cloud_cover": 20.0
        }
        for h in range(24)
    ]

    weather_df = pd.DataFrame(data)
    result = analyze_weather_for_recharge(weather_df)

    # Function should work and add warning into details
    assert isinstance(result, dict)
    assert any("no timezone" in detail.lower() or "assuming local time" in detail.lower()
               for detail in result["details"])