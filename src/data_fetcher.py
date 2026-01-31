import requests
from datetime import datetime, timedelta
import os
import pandas as pd

PSE_API_BASE_URL = os.getenv("PSE_API_BASE_URL", "https://api.raporty.pse.pl/api/rce-pln")

def get_electricity_prices_pse(date_str: str) -> pd.DataFrame | None:
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        end_date = target_date + timedelta(days=1)

        date_from_formatted = target_date.isoformat(timespec='seconds')
        date_to_formatted = end_date.isoformat(timespec='seconds')

        filter_param = (
            f"dtime ge '{date_from_formatted}' and dtime lt '{date_to_formatted}'"
        )

        params = {
            "$filter": filter_param,
        }

        print(f"Calling API PSE with filter: {filter_param}")
        req = requests.Request('GET', PSE_API_BASE_URL, params=params).prepare()
        print(f"Generated URL for API request: {req.url}")

        response = requests.get(PSE_API_BASE_URL, params=params)
        response.raise_for_status()

        data_json = response.json()

        print("\n--- Raw JSON from API PSE: ---")
        print(data_json)
        print("------------------------------------------")

        if 'value' in data_json:
            df = pd.DataFrame(data_json['value'])
            if 'dtime' in df.columns:
                df['dtime'] = pd.to_datetime(df['dtime'])
            return df
        else:
            print("Warning: JSON does not contain key 'value'. Raw dataframe was created.")
            return pd.DataFrame([data_json])
    except requests.exceptions.RequestException as e:
        print(f"Error during loading data from PSE API: {e}")
        print(f"API response (if available): {e.response.text if e.response else 'N/A'}")
        return None
    except ValueError as e:
        print(f"Error in transforming data or format: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error has occurred: {e}")
        return None


if __name__ == "__main__":
    # --- Sample use ---
    test_date_str = "2025-05-15"  # Testing date

    print(f"Downloading data for date: {test_date_str}")

    prices_df = get_electricity_prices_pse(test_date_str)

    if prices_df is not None and not prices_df.empty:
        print(f"\nFirst 5 rows for {test_date_str}):")
        print(prices_df.head())
        print(f"\nColumns w DataFrame: {prices_df.columns.tolist()}")
        print(f"Number of records: {len(prices_df)}")
    else:
        print("Data download was not successful or DataFrame was empty.")