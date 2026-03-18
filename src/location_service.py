import requests
from typing import Optional, Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nominatim API (OpenStreetMap) - free, without API key
NOMINATIM_API_URL = "https://nominatim.openstreetmap.org/search"

# User-Agent required by Nominatim - must be unique!
HEADERS = {
    "User-Agent": "SmartEnergyAgent_PL/1.0 (https://github.com/TomaszPaslawski/SmartEnergyAgent_PL)"
}


def geocode_city(city_name: str, country: str = "Poland") -> Optional[Tuple[float, float, str]]:
    """
    Convert city name to coordinates (geocoding).

    Args:
        city_name (str): City name (e.g. "Warszawa", "Kraków")
        country (str): Country (default "Poland")

    Returns:
        Optional[Tuple[float, float, str]]:
            - (latitude, longitude, display_name) if found
            - None if not found or error

    Examples:
        >>> geocode_city("Warszawa")
        (52.2296756, 21.0122287, "Warszawa, województwo mazowieckie, Polska")

        >>> geocode_city("Nieistniejące Miasto")
        None
    """
    try:
        # Request parameters
        params = {
            "q": f"{city_name}, {country}",
            "format": "json",
            "limit": 1,  # Only first result
            "addressdetails": 1
        }

        logger.info(f"Geocoding: {city_name}, {country}...")

        # Ask to Nominatim
        response = requests.get(
            NOMINATIM_API_URL,
            params=params,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

        results = response.json()

        # Check if results found
        if not results or len(results) == 0:
            logger.warning(f"Coordinates not found for: {city_name}")
            return None

        # First result
        location = results[0]

        latitude = float(location['lat'])
        longitude = float(location['lon'])
        display_name = location.get('display_name', city_name)

        logger.info(f"Found: {display_name} ({latitude:.2f}°N, {longitude:.2f}°E)")

        return (latitude, longitude, display_name)

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error during geocoding: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Parse error from API: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during geocoding: {e}")
        return None


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Check if coordinates are valid.

    Args:
        latitude (float): latitude (-90 do 90)
        longitude (float): longitude (-180 do 180)

    Returns:
        bool: True if valid, false if invalid
    """
    if not (-90 <= latitude <= 90):
        logger.error(f"Incorrect latitude: {latitude} (must be from -90 to 90)")
        return False

    if not (-180 <= longitude <= 180):
        logger.error(f"Incorrect longitude: {longitude} (must be from -180 to 180)")
        return False

    return True


# Test section
if __name__ == "__main__":
    print("\n--- Test location_service.py ---")

    # Test 1: Warszawa
    print("\n1. Test: Warszawa")
    result = geocode_city("Warszawa")
    if result:
        lat, lon, name = result
        print(f"   ✅ {name}")
        print(f"   📍 {lat:.4f}°N, {lon:.4f}°E")
    else:
        print("   ❌ Nie znaleziono")

    # Test 2: Kraków
    print("\n2. Test: Kraków")
    result = geocode_city("Kraków")
    if result:
        lat, lon, name = result
        print(f"   ✅ {name}")
        print(f"   📍 {lat:.4f}°N, {lon:.4f}°E")
    else:
        print("   ❌ Nie znaleziono")

    # Test 3: Miasto nieistniejące
    print("\n3. Test: Nieistniejące Miasto")
    result = geocode_city("XYZ123Nieistniejące")
    if result:
        lat, lon, name = result
        print(f"   ✅ {name}")
    else:
        print("   ❌ Nie znaleziono (oczekiwane)")

    # Test 4: Walidacja współrzędnych
    print("\n4. Test: Walidacja współrzędnych")
    print(f"   (52.23, 21.01): {validate_coordinates(52.23, 21.01)} (oczekiwane: True)")
    print(f"   (999, 21.01): {validate_coordinates(999, 21.01)} (oczekiwane: False)")

    print("\n--- Testy zakończone ---")