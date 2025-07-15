# src/api_client.py
import requests
import json
from datetime import datetime
from src.config import WEATHER_API_KEY, WEATHER_API_BASE_URL

def fetch_current_weather(city: str) -> dict | None:
    """
    Fetches current weather data for a given city from WeatherAPI.com.
    """
    endpoint = f"{WEATHER_API_BASE_URL}/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error for {city}: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error for {city}: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error for {city}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred for {city}: {e}")
    return None

if __name__ == "__main__":
    # Example usage (for testing this module independently)
    test_city = "New York"
    data = fetch_current_weather(test_city)
    if data:
        print(f"Successfully fetched data for {test_city}:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Failed to fetch data for {test_city}.")