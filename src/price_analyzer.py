import pandas as pd
from datetime import datetime

THRESHOLD_HIGH_PRICE = 500.0  # PLN/MWh - current setup of the "high price"

def analyze_price_peaks(prices_df: pd.DataFrame) -> dict:
    """
    Analysis DataFrame with electricity prices provided in 15 minutes timeframes. Identifies hours
    with highest and lowest prices during the day and compares them with threshold.

    Args:
        prices_df (pd.DataFrame): DataFrame with electricity prices,
        should contain columns 'dtime' (datetime, in user time zone) and 'rce_pln' (float).

    Returns:
        dict: Dictionary contains information about identified peaks.
    """
    print("DEBUG: analyze_price_peaks: Prices peaks are now analysed...")

    results = {
        "highest_6h_prices": [],
        "lowest_3h_prices": [],
        "high_price_exceeded": False,
        "hourly_status": [],
        "details": []
    }

    if prices_df.empty:
        results["details"].append("No prices for analysis. Prices dataframe is empty.")
        print("DEBUG: analyze_price_peaks: prices_df is empty. Returning early.")
        return results

    # 1. Check if the column 'dtime' exist.
    print(f"DEBUG: analyze_price_peaks: Checking for 'dtime' column. Columns: {prices_df.columns.tolist()}")
    if 'dtime' not in prices_df.columns:
        results["details"].append("Column 'dtime' is missing from the prices DataFrame.")
        print("DEBUG: analyze_price_peaks: 'dtime' column missing. Returning early.")
        return results

    # 2. If 'dtime' exist check if the type is datetime
    print(f"DEBUG: analyze_price_peaks: 'dtime' column dtype: {prices_df['dtime'].dtype}")
    if not pd.api.types.is_datetime64_any_dtype(prices_df['dtime']):
        print("DEBUG: analyze_price_peaks: 'dtime' column is not datetime type. Attempting conversion.")
        try:
            prices_df['dtime'] = pd.to_datetime(prices_df['dtime'])
            print(f"DEBUG: analyze_price_peaks: 'dtime' column converted. New dtype: {prices_df['dtime'].dtype}")
        except Exception as e:
            results["details"].append(f"Failed to convert 'dtime' column to datetime: {e}.")
            print(f"DEBUG: analyze_price_peaks: Failed to convert 'dtime'. Error: {e}. Returning early.")
            return results
    print("DEBUG: analyze_price_peaks: 'dtime' column is valid. Proceeding to resampling.")

    # 1. Taking average price per hour from 15 minutes timeframes.
    # Setting 'dtime' as index, for easier grouping using hours.
    try:
        df_hourly = prices_df.set_index('dtime')
        # Resampling of data into hour intervals and counting the average price per hour.
        df_hourly_avg = df_hourly['rce_pln'].resample('h').mean().reset_index()
        df_hourly_avg.rename(columns={'dtime': 'hour', 'rce_pln': 'avg_hourly_price'}, inplace=True)
        print(f"DEBUG: analyze_price_peaks: Resampling successful. df_hourly_avg head:\n{df_hourly_avg.head()}")
    except Exception as e:
        results["details"].append(
            f"Error during resampling or column renaming: {e}. Prices df head:\n{prices_df.head()}")
        print(f"DEBUG: analyze_price_peaks: Resampling failed. Error: {e}. Returning early.")
        return results

    # Adding column with pure hour for simplifying (e.g. 00:00, 01:00)
    df_hourly_avg['time_only'] = df_hourly_avg['hour'].dt.strftime('%H:%M')

    if df_hourly_avg.empty:
        results["details"].append("Lack of hourly data after resampling.")
        print("DEBUG: analyze_price_peaks: df_hourly_avg is empty after resampling. Returning early.")
        return results

    print("DEBUG: analyze_price_peaks: Proceeding to identify peaks.")

    # 2. Identification of 6 hours with the highest prices.
    top_6_hours = df_hourly_avg.nlargest(6, 'avg_hourly_price')
    top_6_hours['time_obj'] = top_6_hours['time_only'].apply(lambda x: datetime.strptime(x, '%H:%M').time())
    top_6_hours_sorted = top_6_hours.sort_values(by='time_obj').drop(columns='time_obj')
    for index, row in top_6_hours_sorted.iterrows():
        results["highest_6h_prices"].append({
            "hour": row['time_only'],
            "price": round(row['avg_hourly_price'], 2)
        })
        if row['avg_hourly_price'] > THRESHOLD_HIGH_PRICE:
            results["high_price_exceeded"] = True
            results["details"].append(
                f"Hour {row['time_only']} has high electricity price: {row['avg_hourly_price']:.2f} PLN/MWh (it is over {THRESHOLD_HIGH_PRICE:.2f}).")

    # 3. Identification of 3 hours with the lowest prices.
    bottom_3_hours = df_hourly_avg.nsmallest(3, 'avg_hourly_price')
    bottom_3_hours['time_obj'] = bottom_3_hours['time_only'].apply(lambda x: datetime.strptime(x, '%H:%M').time())
    bottom_3_hours_sorted = bottom_3_hours.sort_values(by='time_obj').drop(columns='time_obj')
    for index, row in bottom_3_hours_sorted.iterrows():
        results["lowest_3h_prices"].append({
            "hour": row['time_only'],
            "price": round(row['avg_hourly_price'], 2)
        })
        results["details"].append(
            f"Hour {row['time_only']} has low electricity price: {row['avg_hourly_price']:.2f} PLN/MWh.")

    # 4. Hourly price status for ALL hours.
    results["details"].append("\n--- Hourly Price Status for the Day ---")
    # Sorting by hour for better visibility
    df_hourly_avg_sorted = df_hourly_avg.sort_values(by='hour').reset_index(drop=True)
    for index, row in df_hourly_avg_sorted.iterrows():
        hour_str = row['time_only']
        price = round(row['avg_hourly_price'], 2)
        status_text = ""
        if price > THRESHOLD_HIGH_PRICE:
            status_text = "ABOVE THRESHOLD"
            # high_price_exceeded for being sure also for 6 top hours
            results["high_price_exceeded"] = True
        else:
            status_text = "BELOW THRESHOLD"

        hourly_entry = {
            "hour": hour_str,
            "price": price,
            "status": status_text
        }
        results["hourly_status"].append(hourly_entry)
        results["details"].append(f"  - Price at {hour_str}: {price:.2f} PLN/MWh ({status_text}).")
    results["details"].append("--------------------------------------")

    print("DEBUG: analyze_price_peaks: Analysis complete. Returning results.")
    return results