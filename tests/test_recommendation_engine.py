import pytest
from datetime import date, time
from src.recommendation_engine import generate_recommendations


def test_generate_recommendations_full_success():
    """Test of generating recomendations - full scenario."""

    # Data from price_analyzer
    price_analysis_results = {
        "highest_6h_prices": [
            {"hour": "07:00", "price": 600.0},  # Morning peak
            {"hour": "08:00", "price": 550.0},
            {"hour": "17:00", "price": 650.0},  # Evening peak
            {"hour": "18:00", "price": 620.0},
            {"hour": "19:00", "price": 580.0},
            {"hour": "20:00", "price": 500.0},
        ],
        "lowest_3h_prices": [
            {"hour": "02:00", "price": 100.0},
            {"hour": "03:00", "price": 120.0},
            {"hour": "04:00", "price": 130.0},
        ],
        "high_price_exceeded": True,
        "hourly_status": [
            {"hour": f"{h:02d}:00", "price": 300.0 + h * 10, "status": "BELOW THRESHOLD"}
            for h in range(24)
        ]
    }

    # Data from weather_analyzer
    weather_analysis_results = {
        "recharge_favorable": True,
        "favorable_hours_count": 5,
        "total_sunny_hours_in_range": 6,
        "hourly_weather_status": [
            {"hour": f"{h:02d}:00", "weather_code": 1, "cloud_cover": 20.0, "status": "PV Favorable"}
            for h in range(24)
        ],
        "details": []
    }

    target_date = date(2026, 3, 10)

    # Call function
    result = generate_recommendations(price_analysis_results, weather_analysis_results, target_date)

    # Assert result
    assert isinstance(result, str)
    assert len(result) > 0

    # Check key elements
    assert "2026-03-10" in result
    assert "YES" in result  # Supporting weather
    assert "07:00" in result  # Morning peak
    assert "17:00" in result  # Evening peak


def test_generate_recommendations_unfavorable_weather():
    """Test not supporting for PV."""

    price_analysis_results = {
        "highest_6h_prices": [
            {"hour": "07:00", "price": 600.0},
            {"hour": "17:00", "price": 650.0},
        ],
        "lowest_3h_prices": [
            {"hour": "02:00", "price": 100.0},
        ],
        "high_price_exceeded": True,
        "hourly_status": [
            {"hour": f"{h:02d}:00", "price": 300.0, "status": "BELOW THRESHOLD"}
            for h in range(24)
        ]
    }

    weather_analysis_results = {
        "recharge_favorable": False,
        "favorable_hours_count": 1,
        "total_sunny_hours_in_range": 6,
        "hourly_weather_status": [
            {"hour": f"{h:02d}:00", "weather_code": 61, "cloud_cover": 90.0, "status": "Rainy/Cloudy"}
            for h in range(24)
        ],
        "details": []
    }

    target_date = date(2026, 3, 10)

    result = generate_recommendations(price_analysis_results, weather_analysis_results, target_date)

    assert isinstance(result, str)
    assert "NO" in result  # Weather not supporting
    assert "not favorable" in result.lower() or "will not charge" in result.lower()


def test_generate_recommendations_low_prices():
    """Test when prices are low/below zero in PV hours (10-16)."""

    hourly_status = []
    for h in range(24):
        if 10 <= h < 14:
            price = 30.0  # Very low price < 50
        elif h == 14:
            price = -10.0  # Price below zero!
        else:
            price = 300.0

        hourly_status.append({
            "hour": f"{h:02d}:00",
            "price": price,
            "status": "BELOW THRESHOLD"
        })

    price_analysis_results = {
        "highest_6h_prices": [
            {"hour": "07:00", "price": 600.0},
            {"hour": "17:00", "price": 650.0},
        ],
        "lowest_3h_prices": [
            {"hour": "14:00", "price": -10.0},
            {"hour": "10:00", "price": 30.0},
            {"hour": "11:00", "price": 30.0},
        ],
        "high_price_exceeded": True,
        "hourly_status": hourly_status
    }

    weather_analysis_results = {
        "recharge_favorable": True,
        "favorable_hours_count": 5,
        "total_sunny_hours_in_range": 6,
        "hourly_weather_status": [
            {"hour": f"{h:02d}:00", "weather_code": 1, "cloud_cover": 20.0, "status": "PV Favorable"}
            for h in range(24)
        ],
        "details": []
    }

    target_date = date(2026, 3, 10)

    result = generate_recommendations(price_analysis_results, weather_analysis_results, target_date)

    assert isinstance(result, str)
    assert "Negative" in result or "Very Low" in result  # Low prices detected


def test_generate_recommendations_no_morning_peak():
    """Test lack of data during morning peak (6-9)."""

    # Prices without hours 6-9
    hourly_status = [
        {"hour": f"{h:02d}:00", "price": 300.0, "status": "BELOW THRESHOLD"}
        for h in range(24) if h < 6 or h >= 9
    ]

    price_analysis_results = {
        "highest_6h_prices": [
            {"hour": "17:00", "price": 650.0},  # Only evening peak
            {"hour": "18:00", "price": 620.0},
        ],
        "lowest_3h_prices": [
            {"hour": "02:00", "price": 100.0},
        ],
        "high_price_exceeded": True,
        "hourly_status": hourly_status
    }

    weather_analysis_results = {
        "recharge_favorable": True,
        "favorable_hours_count": 5,
        "total_sunny_hours_in_range": 6,
        "hourly_weather_status": [
            {"hour": f"{h:02d}:00", "weather_code": 1, "cloud_cover": 20.0, "status": "PV Favorable"}
            for h in range(24)
        ],
        "details": []
    }

    target_date = date(2026, 3, 10)

    result = generate_recommendations(price_analysis_results, weather_analysis_results, target_date)

    assert isinstance(result, str)
    assert "No price data available for the morning peak" in result or "No precise data" in result


def test_generate_recommendations_no_evening_peak():
    """Test lack of data during evening peak (16-20)."""

    price_analysis_results = {
        "highest_6h_prices": [
            {"hour": "07:00", "price": 600.0},  # Only morning peak
            {"hour": "08:00", "price": 550.0},
        ],
        "lowest_3h_prices": [
            {"hour": "02:00", "price": 100.0},
        ],
        "high_price_exceeded": True,
        "hourly_status": [
            {"hour": f"{h:02d}:00", "price": 300.0, "status": "BELOW THRESHOLD"}
            for h in range(24)
        ]
    }

    weather_analysis_results = {
        "recharge_favorable": True,
        "favorable_hours_count": 5,
        "total_sunny_hours_in_range": 6,
        "hourly_weather_status": [
            {"hour": f"{h:02d}:00", "weather_code": 1, "cloud_cover": 20.0, "status": "PV Favorable"}
            for h in range(24)
        ],
        "details": []
    }

    target_date = date(2026, 3, 10)

    result = generate_recommendations(price_analysis_results, weather_analysis_results, target_date)

    assert isinstance(result, str)
    assert "No precise data for the evening peak" in result


def test_generate_recommendations_empty_data():
    """Test with empty/minimal entry data."""

    price_analysis_results = {
        "highest_6h_prices": [],
        "lowest_3h_prices": [],
        "high_price_exceeded": False,
        "hourly_status": []
    }

    weather_analysis_results = {
        "recharge_favorable": False,
        "favorable_hours_count": 0,
        "total_sunny_hours_in_range": 0,
        "hourly_weather_status": [],
        "details": []
    }

    target_date = date(2026, 3, 10)

    result = generate_recommendations(price_analysis_results, weather_analysis_results, target_date)

    # Function should not crash
    assert isinstance(result, str)
    assert "2026-03-10" in result


def test_generate_recommendations_morning_peak_fallback():
    """Test when morning peak is not in top 6 however, included in hourly_status."""

    # highest_6h_prices have ONLY evening hours
    price_analysis_results = {
        "highest_6h_prices": [
            {"hour": "17:00", "price": 650.0},
            {"hour": "18:00", "price": 620.0},
            {"hour": "19:00", "price": 600.0},
            {"hour": "20:00", "price": 580.0},
            {"hour": "21:00", "price": 550.0},
            {"hour": "22:00", "price": 520.0},
        ],
        "lowest_3h_prices": [
            {"hour": "02:00", "price": 100.0},
        ],
        "high_price_exceeded": True,
        "hourly_status": [
            {"hour": f"{h:02d}:00", "price": 300.0 + h * 5, "status": "BELOW THRESHOLD"}
            for h in range(24)
        ]
    }

    weather_analysis_results = {
        "recharge_favorable": True,
        "favorable_hours_count": 5,
        "total_sunny_hours_in_range": 6,
        "hourly_weather_status": [
            {"hour": f"{h:02d}:00", "weather_code": 1, "cloud_cover": 20.0, "status": "PV Favorable"}
            for h in range(24)
        ],
        "details": []
    }

    target_date = date(2026, 3, 10)

    result = generate_recommendations(price_analysis_results, weather_analysis_results, target_date)

    assert isinstance(result, str)
    # Should found morning peak in hourly_status (fallback)
    # Hour 08:00 has price 300 + 8*5 = 340 (highest in frame 6-9)
    assert "08:00" in result or "morning peak" in result.lower()