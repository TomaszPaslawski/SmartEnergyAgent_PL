# function body is coming from Open-Meteo website as it is providing Python code for API.
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime, timedelta

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_weather_forecast(latitude: float, longitude: float, target_date_str: str) -> pd.DataFrame | None:
    """
    Downloads hourly Weather Forecast from Open-Meteo.com for selected localization and selected day.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        target_date_str (str): Date of forecast (in local time) and in format 'YYYY-MM-DD'.
                                Weather forecast will be downloaded for next day.

    Returns:
        pd.DataFrame | None: DataFrame with hourly Weather Forecast for selected location and time.
                                     None in case no DataFrame.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "pressure_msl", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "precipitation_probability", "precipitation", "weather_code"],
        "models": "ecmwf_ifs",  # Best Weather Model for Europe.
        "timezone": "Europe/Berlin",  # Timezone setting
        "start_date": target_date_str,  # From date
        "end_date": target_date_str,  # To date (one day)
    }

    try:
        print(f"DEBUG: Requesting weather for target_date_str={target_date_str}")
        print(f"DEBUG: API params used: {params}")

        responses = openmeteo.weather_api(url, params=params)

        if not responses:
            print("ERROR: Open-Meteo API returned empty list or there is not data.")
            return None

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()

        if not hourly or not hasattr(hourly, 'Time') or not hasattr(hourly, 'Interval') or not hasattr(hourly,
                                                                                                       'Variables'):
            print("ERROR: Object 'Hourly' is empty or incomplete (missing Time/Interval/Variables).")
            return None

        # Checking if all variables are present
        requested_vars_count = len(params["hourly"])
        available_vars_count = 0
        try:
            # Try to get variable with the last index - if works, all variables are there.
            hourly.Variables(requested_vars_count - 1)
            available_vars_count = requested_vars_count
        except Exception:
            # If not match we are checking the difference
            for i in range(requested_vars_count):
                try:
                    hourly.Variables(i)
                    available_vars_count += 1
                except Exception:
                    break

        if available_vars_count < requested_vars_count:
            print(
                f"ERROR: Number of variables is less ({available_vars_count}) than requested ({requested_vars_count}). Probably lack of data for some variables.")
            return None

        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_pressure_msl = hourly.Variables(1).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(2).ValuesAsNumpy()
        hourly_cloud_cover_low = hourly.Variables(3).ValuesAsNumpy()
        hourly_cloud_cover_mid = hourly.Variables(4).ValuesAsNumpy()
        hourly_cloud_cover_high = hourly.Variables(5).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(6).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(7).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(8).ValuesAsNumpy()

        # --- KLUCZOWA ZMIANA: Zmieniamy "date" na "datetime" dla kolumny czasowej ---
        hourly_data = {"datetime": pd.date_range(  # <--- Zmieniono "date" na "datetime"
            start=pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["pressure_msl"] = hourly_pressure_msl
        hourly_data["cloud_cover"] = hourly_cloud_cover
        hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
        hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
        hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
        hourly_data["precipitation_probability"] = hourly_precipitation_probability
        hourly_data["precipitation"] = hourly_precipitation
        hourly_data["weather_code"] = hourly_weather_code

        hourly_dataframe = pd.DataFrame(data=hourly_data)

        if not responses:
            print("ERROR: Open-Meteo API returned empty list or there is not data.")
            return None

        return hourly_dataframe

    except Exception as e:
        print(f"Error during downloading the Weather Forecast from Open-Meteo: {type(e).__name__}: {e}")
        return None


if __name__ == "__main__":
    example_latitude = 53.7535
    example_longitude = 17.7752

    # --- Ensuring the forecast will be for tomorrow ---
    current_actual_date = datetime.now().date()
    tomorrow_actual_date = current_actual_date + timedelta(days=1)

    # We are asking function for the forecast for tomorrow
    target_date_for_forecast = tomorrow_actual_date.strftime('%Y-%m-%d')

    print(
        f"\nWeather forecast for {example_latitude}°N {example_longitude}°E is downloading for day {target_date_for_forecast} (local time)")
    weather_df = get_weather_forecast(example_latitude, example_longitude, target_date_for_forecast)

    if weather_df is not None and not weather_df.empty:
        print("\nDownloaded forecast (first 5 rows:")
        print(weather_df.head())
        print(f"\nColumns in DataFrame: {weather_df.columns.tolist()}")
        print(f"Number of records: {len(weather_df)}")

    else:
        print("Weather Forecast has not been downloaded or the DataFrame was empty.")
