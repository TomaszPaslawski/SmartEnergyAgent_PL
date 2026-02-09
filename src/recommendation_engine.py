from datetime import datetime, date, time, timedelta

# --- Configuration for recommendations (to be user-configurable eventually) ---
# STORAGE_DISCHARGE_DURATION_MINUTES = 30 # This might not be needed if we recommend STARTING at peak hour
STORAGE_CHARGE_DURATION_HOURS = 3  # Battery charge duration in hours

# Hours when PV is active (Sunny Hours) - for charging recommendations
PV_ACTIVE_HOURS_START = time(10, 0)
PV_ACTIVE_HOURS_END = time(16, 0)

# Price peak definitions (general ranges)
MORNING_PEAK_TIME_RANGE = (time(6, 0), time(9, 0))  # Morning peak hours range
EVENING_PEAK_TIME_RANGE = (time(16, 0), time(20, 0))  # Evening peak hours range

# Thresholds for "very low" / "negative" electricity prices
VERY_LOW_PRICE_THRESHOLD = 50.0  # e.g., below 50 PLN/MWh
NEGATIVE_PRICE_THRESHOLD = 0.0  # e.g., negative prices


def generate_recommendations(price_analysis_results: dict, weather_analysis_results: dict, target_date: date) -> str:
    """
    Generates precise recommendations for the user based on energy price analysis and weather forecast.

    Args:
        price_analysis_results (dict): Electricity price analysis results from price_analyzer.
        weather_analysis_results (dict): Weather analysis results from weather_analyzer.
        target_date (date): The date for which recommendations are generated.

    Returns:
        str: A formatted recommendation message for the user.
    """
    recommendation_messages = []

    # --- Extract initial data from analysis results ---
    # Price Analysis
    hourly_prices_status = price_analysis_results.get('hourly_status', [])
    highest_6h_prices = price_analysis_results.get('highest_6h_prices', [])
    lowest_3h_prices = price_analysis_results.get('lowest_3h_prices', [])

    # Weather Analysis
    recharge_favorable_weather = weather_analysis_results.get('recharge_favorable', False)
    hourly_weather_status = weather_analysis_results.get('hourly_weather_status',
                                                         [])  # Not directly used in recommendations yet, but available

    recommendation_messages.append(f"--- Recommendations for {target_date.strftime('%Y-%m-%d')} ---\n")

    # 1) Check if weather will be favorable for charging
    recommendation_messages.append(
        f"1. Weather for {target_date.strftime('%Y-%m-%d')} will be favorable for PV battery charging: {'YES' if recharge_favorable_weather else 'NO'}.")
    if recharge_favorable_weather:
        recommendation_messages.append(
            f"   ({weather_analysis_results['favorable_hours_count']} out of {weather_analysis_results['total_sunny_hours_in_range']} hours between {PV_ACTIVE_HOURS_START.strftime('%H:%M')}-{PV_ACTIVE_HOURS_END.strftime('%H:%M')} with favorable conditions).")
    else:
        recommendation_messages.append(
            f"   (Too much cloud cover/unfavorable conditions during {PV_ACTIVE_HOURS_START.strftime('%H:%M')}-{PV_ACTIVE_HOURS_END.strftime('%H:%M')} hours).")
    recommendation_messages.append("")

    # Convert hourly_prices_status for easier lookup by hour string
    prices_by_hour_str = {entry['hour']: entry['price'] for entry in hourly_prices_status}

    # 2) Identify the morning hour with the highest prices (within morning peak range)
    morning_peak_hour_info = None
    if highest_6h_prices:
        # Filter highest_6h_prices to find those within the morning peak time range
        # Convert hour string 'HH:MM' to time object for comparison
        morning_peak_candidates = [
            hp for hp in highest_6h_prices
            if time.fromisoformat(hp['hour']) >= MORNING_PEAK_TIME_RANGE[0] and time.fromisoformat(hp['hour']) <
               MORNING_PEAK_TIME_RANGE[1]
        ]
        if morning_peak_candidates:
            # Pick the one with the highest price within these candidates
            morning_peak_hour_info = max(morning_peak_candidates, key=lambda x: x['price'])

    if morning_peak_hour_info:
        recommendation_messages.append(
            f"2. The highest price during the morning peak ({MORNING_PEAK_TIME_RANGE[0].strftime('%H:%M')}-{MORNING_PEAK_TIME_RANGE[1].strftime('%H:%M')}) is forecasted at {morning_peak_hour_info['hour']} with a price of {morning_peak_hour_info['price']:.2f} PLN/MWh.")
    else:
        # Fallback: if no top 6 hours are in morning peak, find the actual highest within the whole morning peak range
        all_morning_peak_data = [
            {'hour': entry['hour'], 'price': entry['price']}
            for entry in hourly_prices_status
            if time.fromisoformat(entry['hour']) >= MORNING_PEAK_TIME_RANGE[0] and time.fromisoformat(entry['hour']) <
               MORNING_PEAK_TIME_RANGE[1]
        ]
        if all_morning_peak_data:
            morning_peak_hour_info = max(all_morning_peak_data, key=lambda x: x['price'])
            recommendation_messages.append(
                f"2. The highest price during the morning peak ({MORNING_PEAK_TIME_RANGE[0].strftime('%H:%M')}-{MORNING_PEAK_TIME_RANGE[1].strftime('%H:%M')}) is forecasted at {morning_peak_hour_info['hour']} with a price of {morning_peak_hour_info['price']:.2f} PLN/MWh.")
        else:
            recommendation_messages.append("2. No price data available for the morning peak period.")
    recommendation_messages.append("")

    # 3) Identify hours with very low/negative prices within PV Active Hours (10:00-16:00)
    low_price_opportunities = []
    for entry in hourly_prices_status:
        hour_time = time.fromisoformat(entry['hour'])
        if PV_ACTIVE_HOURS_START <= hour_time < PV_ACTIVE_HOURS_END:
            if entry['price'] < NEGATIVE_PRICE_THRESHOLD:
                low_price_opportunities.append(f"{entry['hour']} (Negative: {entry['price']:.2f} PLN/MWh)")
            elif entry['price'] < VERY_LOW_PRICE_THRESHOLD:
                low_price_opportunities.append(f"{entry['hour']} (Very Low: {entry['price']:.2f} PLN/MWh)")

    if low_price_opportunities:
        recommendation_messages.append(
            f"3. During active PV hours ({PV_ACTIVE_HOURS_START.strftime('%H:%M')}-{PV_ACTIVE_HOURS_END.strftime('%H:%M')}), hours with very low/negative prices were identified: {', '.join(low_price_opportunities)}.")
    else:
        recommendation_messages.append(
            f"3. No very low/negative price hours identified during active PV hours ({PV_ACTIVE_HOURS_START.strftime('%H:%H')}-{PV_ACTIVE_HOURS_END.strftime('%H:%M')}).")
    recommendation_messages.append("")

    # 4) Recommend charging the battery
    if recharge_favorable_weather and low_price_opportunities:
        # Determine the start hour for charging based on the first identified low-price opportunity
        first_low_price_hour_str = low_price_opportunities[0].split(' ')[0]
        recommendation_messages.append(
            f"4. Weather is favorable for PV charging. Considering the charge duration ({STORAGE_CHARGE_DURATION_HOURS}h) and low prices, it is recommended to start charging the battery at {first_low_price_hour_str}.")
        # Further logic could be added here to find the optimal charging window within low-price hours
    elif recharge_favorable_weather and not low_price_opportunities:
        recommendation_messages.append(
            f"4. Weather is favorable for PV charging. However, no very low/negative prices were identified during active PV hours. Charge the battery during the lowest general price hours or as PV becomes available.")
    else:
        recommendation_messages.append(
            "4. Weather is not favorable for PV charging. The battery will not charge efficiently. Consider alternative charging sources if needed.")
    recommendation_messages.append("")

    # 5) Indicate the hour to start discharging the battery in the morning
    if morning_peak_hour_info:
        discharge_start_hour_str = morning_peak_hour_info['hour']
        recommendation_messages.append(
            f"5. It is recommended to start discharging the battery at {discharge_start_hour_str} (start of the peak hour), if needed.")
    else:
        recommendation_messages.append(
            "5. No precise data for the morning peak. No specific recommendation for morning battery discharge.")
    recommendation_messages.append("")

    # 6) Indicate the hour with the highest prices in the evening
    evening_peak_hour_info = None
    if highest_6h_prices:
        # Filter highest_6h_prices to find those within the evening peak time range
        evening_peak_candidates = [
            hp for hp in highest_6h_prices
            if time.fromisoformat(hp['hour']) >= EVENING_PEAK_TIME_RANGE[0] and time.fromisoformat(hp['hour']) <
               EVENING_PEAK_TIME_RANGE[1]
        ]
        if evening_peak_candidates:
            # Pick the one with the highest price within these candidates
            evening_peak_hour_info = max(evening_peak_candidates, key=lambda x: x['price'])

    if evening_peak_hour_info:
        recommendation_messages.append(
            f"6. The highest price during the evening peak ({EVENING_PEAK_TIME_RANGE[0].strftime('%H:%M')}-{EVENING_PEAK_TIME_RANGE[1].strftime('%H:%M')}) is forecasted at {evening_peak_hour_info['hour']} with a price of {evening_peak_hour_info['price']:.2f} PLN/MWh.")
        if recharge_favorable_weather:  # If weather is favorable for charging, surplus can be sold
            recommendation_messages.append(
                f"   RECOMMENDATION: If you have surplus energy after PV charging, consider selling it to the grid at {evening_peak_hour_info['hour']} (hour of highest evening prices).")
    else:
        recommendation_messages.append(
            "6. No precise data for the evening peak. No specific recommendation for selling surplus.")
    recommendation_messages.append("")

    recommendation_messages.append(f"------------------------------------")
    recommendation_messages.append("\n<b>--- Hourly Price Status (PLN/MWh) ---</b>")
    for entry in price_analysis_results['hourly_status']:
        recommendation_messages.append(f"  - <b>{entry['hour']}</b>: {entry['price']:.2f} ({entry['status']})")
    recommendation_messages.append("---------------------------------------------------\n")

    recommendation_messages.append("<b>--- Hourly Weather Forecast ---</b>")
    for entry in weather_analysis_results['hourly_weather_status']:
        recommendation_messages.append(
            f"  - <b>{entry['hour']}</b>: {entry['status']} (Code: {int(entry['weather_code'])}, Clouds: {entry['cloud_cover']:.0f}%)")
    recommendation_messages.append("-------------------------------------------\n")


    return "\n".join(recommendation_messages)