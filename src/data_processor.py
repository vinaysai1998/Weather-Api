# src/data_processor.py
import pandas as pd
from datetime import datetime

def parse_weather_data(raw_data: dict) -> dict | None:
    """
    Parses raw JSON weather data into a structured dictionary.
    """
    if not raw_data or "current" not in raw_data or "location" not in raw_data:
        print("Warning: Invalid or incomplete raw data received.")
        return None

    location = raw_data.get("location", {})
    current = raw_data.get("current", {})

    try:
        processed_record = {
            "city": location.get("name"),
            "region": location.get("region"),
            "country": location.get("country"),
            "latitude": location.get("lat"),
            "longitude": location.get("lon"),
            # Ensure localtime is parsed correctly for database
            "local_time": pd.to_datetime(location.get("localtime")),
            "temp_c": current.get("temp_c"),
            "temp_f": current.get("temp_f"),
            "condition_text": current.get("condition", {}).get("text"),
            "humidity": current.get("humidity"),
            "wind_kph": current.get("wind_kph"),
            "pressure_mb": current.get("pressure_mb"),
            # Ensure last_updated is parsed correctly
            "last_updated": pd.to_datetime(current.get("last_updated")),
            "ingestion_timestamp": datetime.utcnow() # When it was ingested by our pipeline
        }
        return processed_record
    except Exception as e:
        print(f"Error parsing weather data: {e} for data: {raw_data}")
        return None

def transform_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs further transformations on a DataFrame of parsed weather data.
    This is where you'd add more complex logic, e.g., calculating derived metrics.
    """
    if df.empty:
        return df

    # Example transformation: Ensure numerical types
    numeric_cols = ['latitude', 'longitude', 'temp_c', 'temp_f', 'humidity', 'wind_kph', 'pressure_mb']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce') # Coerce errors will turn non-numeric to NaN

    # Example: Calculate a simple wind speed category (could be more complex)
    df['wind_category'] = pd.cut(df['wind_kph'],
                                 bins=[0, 10, 30, 100, 999],
                                 labels=['Calm', 'Breezy', 'Windy', 'Stormy'],
                                 right=False,
                                 include_lowest=True)

    return df

if __name__ == "__main__":
    # Example usage
    sample_raw_data = {
        "location": {
            "name": "London", "region": "City of London, Greater London", "country": "UK",
            "lat": 51.52, "lon": -0.11, "tz_id": "Europe/London", "localtime_epoch": 1678886400,
            "localtime": "2023-03-15 10:00"
        },
        "current": {
            "last_updated_epoch": 1678886400, "last_updated": "2023-03-15 10:00",
            "temp_c": 10.0, "temp_f": 50.0, "is_day": 1,
            "condition": {"text": "Partly cloudy", "icon": "//[cdn.weatherapi.com/weather/64x64/day/116.png](https://cdn.weatherapi.com/weather/64x64/day/116.png)", "code": 1003},
            "wind_kph": 15.0, "pressure_mb": 1012.0, "humidity": 75
        }
    }
    
    processed_record = parse_weather_data(sample_raw_data)
    if processed_record:
        df_single = pd.DataFrame([processed_record])
        transformed_df = transform_weather_data(df_single)
        print("Transformed Data:")
        print(transformed_df.to_string())