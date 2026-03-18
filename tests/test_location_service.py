import pytest
import requests
from unittest.mock import patch, MagicMock
from src.location_service import geocode_city, validate_coordinates


def test_geocode_city_success():
    """Test of geocoding - success (Warszawa)."""

    # Mock response from Nominatim
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "lat": "52.2296756",
            "lon": "21.0122287",
            "display_name": "Warszawa, województwo mazowieckie, Polska"
        }
    ]

    with patch('src.location_service.requests.get', return_value=mock_response):
        result = geocode_city("Warszawa")

    assert result is not None
    lat, lon, name = result
    assert lat == pytest.approx(52.23, abs=0.01)
    assert lon == pytest.approx(21.01, abs=0.01)
    assert "Warszawa" in name


def test_geocode_city_not_found():
    """Test of geocoding - city not found."""

    # Mock empty response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []  # empty list

    with patch('src.location_service.requests.get', return_value=mock_response):
        result = geocode_city("XYZ123Nieistniejące")

    assert result is None


def test_geocode_city_http_error():
    """Test of geocoding - HTTP error."""

    with patch('src.location_service.requests.get') as mock_get:
        mock_get.side_effect = Exception("Network error")

        result = geocode_city("Warszawa")

    assert result is None


def test_validate_coordinates_valid():
    """Test - validation of coordinates."""

    assert validate_coordinates(52.23, 21.01) == True
    assert validate_coordinates(0, 0) == True
    assert validate_coordinates(90, 180) == True
    assert validate_coordinates(-90, -180) == True


def test_validate_coordinates_invalid():
    """Test - validation of incorrect coordinates."""

    assert validate_coordinates(999, 21.01) == False  # Latitude za duże
    assert validate_coordinates(52.23, 999) == False  # Longitude za duże
    assert validate_coordinates(-999, 0) == False
    assert validate_coordinates(0, -999) == False

def test_geocode_city_request_exception():
    """Test of geocoding - HTTP error (RequestException)."""

    with patch('src.location_service.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = geocode_city("Warszawa")

    assert result is None


def test_geocode_city_invalid_response_format():
    """Test of geocoding  – incorrect format from API (lack of key 'lat')."""

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "wrong_key": "123"  # lack 'lat' and 'lon'
        }
    ]

    with patch('src.location_service.requests.get', return_value=mock_response):
        result = geocode_city("Warszawa")

    assert result is None


def test_geocode_city_unexpected_error():
    """Test of geocoding – unexpected error."""

    with patch('src.location_service.requests.get') as mock_get:
        mock_get.side_effect = RuntimeError("Unexpected error")

        result = geocode_city("Warszawa")

    assert result is None