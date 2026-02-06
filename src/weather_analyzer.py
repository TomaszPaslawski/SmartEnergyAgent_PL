import pandas as pd
from datetime import time

# --- Configuration ---
SUNNY_HOURS_START = time(10, 0)  # 'Sunny' hours start
SUNNY_HOURS_END = time(16, 0)  # 'Sunny' hours end

FAVORABLE_WEATHER_CODES = [0, 1, 2,
                           3]  # Clear sky, Mainly clear, partly cloudy, and overcast (for PV, overcast is not favorable)
# Precising FAVORABLE_WEATHER_CODES for PV: only codes 0, 1, 2 (clear, mainly clear, partly cloudy)
PV_FAVORABLE_WEATHER_CODES = [0, 1, 2]  # Clear sky, Mainly clear, partly cloudy

MAX_CLOUD_COVER_FOR_PV_RECHARGE = 35.0  # Percent - max cloud percentage favorable for the PV

MIN_FAVORABLE_HOURS_PERCENTAGE = 0.60  # Percent - minimum number of favorable hours in sunny day period


def analyze_weather_for_recharge(weather_df: pd.DataFrame) -> dict:
    """
    Analyzes the weather forecast for potential energy storage recharge,
    using the weather code (weather_code) and overall cloud cover (cloud_cover) for "sunny" hours.
    It also returns hourly weather status for the entire day.

    Args:
        weather_df (pd.DataFrame): A DataFrame with a weather forecast
                                should contain a 'datetime' column (datetime, local time zone)
                                and a 'weather_code' column (int/float), and a 'cloud_cover' column (float).

    Returns:
        dict: A dictionary containing the analysis results
            (whether the weather is favorable for charging) and hourly weather status.

    """
    print("Analyzing weather for recharge potential...")

    results = {
        "recharge_favorable": False,
        "favorable_hours_count": 0,
        "total_sunny_hours_in_range": 0,
        "hourly_weather_status": [],  # New list for weather status per hour
        "details": []
    }

    if weather_df.empty:
        results["details"].append("No weather data for analysis. DataFrame is empty.")
        return results

    # Columns validation
    required_cols = ['datetime', 'weather_code', 'cloud_cover']
    for col in required_cols:
        if col not in weather_df.columns:
            results["details"].append(f"Column '{col}' is missing from the weather DataFrame.")
            return results
    if not pd.api.types.is_datetime64_any_dtype(weather_df['datetime']):
        results["details"].append("Column 'datetime' is not of datetime type.")
        return results
    if weather_df['datetime'].dt.tz is None:
        results["details"].append("WARNING: 'datetime' column in weather_df has no timezone info. Assuming local time.")

    # 'Sunny' hours filtration
    sunny_hours_df = weather_df[
        (weather_df['datetime'].dt.time >= SUNNY_HOURS_START) &
        (weather_df['datetime'].dt.time < SUNNY_HOURS_END)
        ].copy()

    if sunny_hours_df.empty:
        results["details"].append(
            f"No weather data found for core sunny hours ({SUNNY_HOURS_START}-{SUNNY_HOURS_END}).")
        results["details"].append("Recharge potential cannot be assessed due to lack of data in key hours.")
        return results

    results["total_sunny_hours_in_range"] = len(sunny_hours_df)

    # Validation of each hour under the 'sunny' period
    favorable_hours_count = 0
    favorable_hours_details = []

    for index, row in sunny_hours_df.iterrows():
        hour_str = row['datetime'].strftime('%H:%M')
        weather_code = row['weather_code']
        cloud_cover = row['cloud_cover']

        if weather_code in PV_FAVORABLE_WEATHER_CODES and cloud_cover <= MAX_CLOUD_COVER_FOR_PV_RECHARGE:
            favorable_hours_count += 1
            favorable_hours_details.append(
                f"  - Hour {hour_str}: Favorable (Code: {int(weather_code)}, Clouds: {cloud_cover:.0f}%)")
        else:
            favorable_hours_details.append(
                f"  - Hour {hour_str}: Not Favorable (Code: {int(weather_code)}, Clouds: {cloud_cover:.0f}%)")

    results["favorable_hours_count"] = favorable_hours_count

    # Validation of day potential for charging
    if results["total_sunny_hours_in_range"] > 0:
        favorable_hours_percentage = results["favorable_hours_count"] / results["total_sunny_hours_in_range"]
        results["details"].append(
            f"Zidentyfikowano {results['favorable_hours_count']} z {results['total_sunny_hours_in_range']} godzin ({favorable_hours_percentage:.0%}) z pogodą sprzyjającą ładowaniu PV w zakresie {SUNNY_HOURS_START}-{SUNNY_HOURS_END}.")
        results["details"].extend(favorable_hours_details)

        if favorable_hours_percentage >= MIN_FAVORABLE_HOURS_PERCENTAGE:
            results["recharge_favorable"] = True
            results["details"].append(
                f"Ogólna pogoda sprzyja ładowaniu! {favorable_hours_percentage:.0%} godzin ma korzystne warunki (wymagane {MIN_FAVORABLE_HOURS_PERCENTAGE:.0%}).")
        else:
            results["details"].append(
                f"Ogólna pogoda NIE sprzyja ładowaniu. Tylko {favorable_hours_percentage:.0%} godzin ma korzystne warunki (wymagane {MIN_FAVORABLE_HOURS_PERCENTAGE:.0%}).")
    else:
        results["details"].append("Brak godzin do oceny potencjału ładowania w zdefiniowanym zakresie.")

    # --- Weather status for whole day ---
    results["details"].append("\n--- Hourly Weather Status for the Day ---")
    # Checking chronological sorting of data
    weather_df_sorted = weather_df.sort_values(by='datetime').reset_index(drop=True)

    for index, row in weather_df_sorted.iterrows():
        hour_str = row['datetime'].strftime('%H:%M')
        weather_code = row['weather_code']
        cloud_cover = row['cloud_cover']

        status_text = "Nieokreślono"
        if weather_code in PV_FAVORABLE_WEATHER_CODES and cloud_cover <= MAX_CLOUD_COVER_FOR_PV_RECHARGE:
            status_text = "PV Favorable"
        elif weather_code in [0, 1, 2]:
            status_text = "Partially Favorable (some clouds)"
        elif weather_code in [3]:
            status_text = "Overcast"
        elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            status_text = "Rainy/Cloudy"
        elif weather_code in [71, 73, 75, 85, 86]:
            status_text = "Snowy/Cloudy"
        elif weather_code in [45, 48]:
            status_text = "Foggy"
        elif weather_code in [95, 96, 99]:
            status_text = "Thunderstorm/Severe Weather"

        hourly_entry = {
            "hour": hour_str,
            "weather_code": int(weather_code),
            "cloud_cover": round(cloud_cover, 0),
            "status": status_text
        }
        results["hourly_weather_status"].append(hourly_entry)
        results["details"].append(
            f"  - Weather at {hour_str}: {status_text} (Code: {int(weather_code)}, Clouds: {cloud_cover:.0f}%).")
    results["details"].append("--------------------------------------")

    return results
