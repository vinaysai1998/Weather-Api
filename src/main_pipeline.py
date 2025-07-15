# src/main_pipeline.py
import pandas as pd
from src.config import CITIES
from src.api_client import fetch_current_weather
from src.data_processor import parse_weather_data, transform_weather_data
from src.database_manager import create_table_if_not_exists, insert_weather_data

def run_pipeline():
    """
    Main function to orchestrate the data pipeline:
    1. Fetches raw data from API for specified cities.
    2. Parses and transforms the data.
    3. Loads the processed data into the database.
    """
    print("--- Starting Data Pipeline ---")
    
    # 1. Ensure database table exists
    create_table_if_not_exists()

    all_processed_records = []

    # 2. Fetch and Parse Data for each city
    for city in CITIES:
        print(f"Fetching data for {city}...")
        raw_data = fetch_current_weather(city)
        if raw_data:
            processed_record = parse_weather_data(raw_data)
            if processed_record:
                all_processed_records.append(processed_record)
                print(f"Successfully processed data for {city}.")
            else:
                print(f"Failed to parse data for {city}.")
        else:
            print(f"Skipping {city} due to API fetch error.")

    if not all_processed_records:
        print("No data collected to process and load.")
        return

    # 3. Transform Data using Pandas
    df_raw = pd.DataFrame(all_processed_records)
    print(f"Collected {len(df_raw)} records before final transformation.")
    df_transformed = transform_weather_data(df_raw)
    print(f"Transformed {len(df_transformed)} records.")

    # 4. Load Data into Database
    insert_weather_data(df_transformed)
    print("--- Data Pipeline Completed ---")

if __name__ == "__main__":
    run_pipeline()