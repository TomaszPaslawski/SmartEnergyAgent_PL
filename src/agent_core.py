from datetime import datetime, timedelta, time
from src.data_fetcher import get_electricity_prices_pse
from src.weather_fetcher import get_weather_forecast
from src.price_analyzer import analyze_price_peaks
from src.weather_analyzer import analyze_weather_for_recharge
from src.recommendation_engine import generate_recommendations
from src.notification_manager import send_telegram_message

# --- Constant for the PSE publications ---
# Publication hour for  RCE-PLN (next day prices), timezone: CET/CEST
# PSE publishes report between 13:00 and 14:00. Set for 14:00 to ensure data will be there.
PSE_PUBLICATION_HOUR_CET = 14
PSE_PUBLICATION_MINUTE_CET = 0

def run_daily_agent_logic(target_date: datetime.date, latitude: float, longitude: float):
    """
    Main logic of the Agent. It runs everyday for tomorrow.
    Args:
        target_date (datetime.date): Data for which we want to run the agent.
        latitude (float): Latitude for Weather Forecast.
        longitude (float): Longitude for Weather Forecast.
    """
    current_time = datetime.now()
    print(f"[{current_time}] Agent is going to be run for: {target_date}")

    # --- SECURITY CHECK: Verification of the publication hour for RCE-PLN ---
    # PSE publishes RCE-PLN for next day between 13:00 and 14:00 CET/CEST.
    # If target_date is TOMORROW, and actual hour is before publication hour
    # then, data for target_date may not be available yet.

    # Re-counting target_date (tomorrow) for 'today' for PSE
    # If target_date is TOMORROW then, data for tomorrow is published today.
    # If target_date is today then, data for today was published yesterday.

    # Data, which prices will be published (that is target_date)
    # They are published 'today' (current_time.date()) for 'tomorrow' (target_date)
    # If Agent runs today to take data for tomorrow, we must check, if the publications hour has already passed.

    # Checking, if data we are asking for is tomorrow.
    # If yes, we are checking if the publication hour has already passed.
    if target_date == (current_time.date() + timedelta(days=1)):
        publication_threshold = current_time.replace(hour=PSE_PUBLICATION_HOUR_CET,
                                                     minute=PSE_PUBLICATION_MINUTE_CET,
                                                     second=0, microsecond=0)

        if current_time < publication_threshold:
            print(f"Warning: Prices RCE-PLN for {target_date} (tomorrow) have not been published yet.")
            print(f"Mainly they are published after {PSE_PUBLICATION_HOUR_CET}:00 CET/CEST.")
            print("Data download will be skipped. Agent ends job.")
            return # Agent ends job if the data is not yet available.
    # --- SECURITY CHECK END ---


    # 1. Energy prices download
    prices_df = get_electricity_prices_pse(target_date.strftime('%Y-%m-%d'))
    if prices_df is None or prices_df.empty:
        print("Error: Data download was not successful or DataFrame is empty.")
        return

    print("\nDownloaded prices (first 5 rows:")
    print(prices_df.head())
    print(f"Number of prices records: {len(prices_df)}")

    price_analysis_results = analyze_price_peaks(prices_df)
    print("\n--- Price Analysis Results ---")
    print(f"Highest 6h prices: {price_analysis_results['highest_6h_prices']}")
    print(f"Lowest 3h prices: {price_analysis_results['lowest_3h_prices']}")
    print(f"High price exceeded: {price_analysis_results['high_price_exceeded']}")
    print("Details:")
    for detail in price_analysis_results['details']:
        print(f"  - {detail}")
    print("----------------------------")

    # price_analysis_results = analyze_price_peaks(prices_df)
    # print(f"\nResults of prices analysis: {price_analysis_results}")

    # 2. Weather Forecast download
    weather_df = get_weather_forecast(latitude, longitude, target_date.strftime('%Y-%m-%d'))
    if weather_df is None or weather_df.empty:
        print("Error: Weather Forecast download was not successful or DataFrame is empty.")
        return

    print("\nDownloaded Weather Forecast (first 5 rows:")
    print(weather_df.head())
    print(f"Number of weather records: {len(weather_df)}")

    weather_analysis_results = analyze_weather_for_recharge(weather_df)
    print("\n--- Weather Analysis Results ---")
    print(f"Recharge favorable: {weather_analysis_results['recharge_favorable']}")
    print(
        f"Favorable hours count (10-16): {weather_analysis_results['favorable_hours_count']} out of {weather_analysis_results['total_sunny_hours_in_range']}")
    print("Details:")
    for detail in weather_analysis_results['details']:
        print(f"{detail}")
    print("------------------------------")

    # 3. Generating Recommendations
    # This calls the function from recommendation_engine.py
    final_recommendation = generate_recommendations(price_analysis_results, weather_analysis_results, target_date)
    print("\n--- Agent's Recommendation ---")
    print(final_recommendation)
    print("----------------------------")

    print("\n--- Sending Telegram Notification ---")
    success = send_telegram_message(final_recommendation)  # <--- WYWOŁANIE BOTA
    if success:
        print("Telegram message sent successfully!")
    else:
        print("Failed to send Telegram message. Check logs.")
    print("-----------------------------------")

    # --- Further logic will be added here ---

    print(f"[{datetime.now()}] Agent job done for date: {target_date}")


if __name__ == "__main__":
    # --- Test parameters ---
    DEFAULT_LATITUDE = 53.7535
    DEFAULT_LONGITUDE = 17.7752

    # Weather Forecast for tomorrow

    # Turn on after 14.00 testing
    # tomorrow_date = datetime.now().date() + timedelta(days=1)

    # Turn on before 14.00 testing
    tomorrow_date = datetime.now().date()

    run_daily_agent_logic(tomorrow_date, DEFAULT_LATITUDE, DEFAULT_LONGITUDE)