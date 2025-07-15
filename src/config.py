# src/config.py
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL")
CITIES = [city.strip() for city in os.getenv("CITIES", "London").split(',')]

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "weather_db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# --- Paths ---
# You might not need these if processing in-memory, but good for larger projects
RAW_DATA_DIR = "data/raw_data"
PROCESSED_DATA_DIR = "data/processed_data"

# Create directories if they don't exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)