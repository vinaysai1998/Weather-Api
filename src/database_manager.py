# src/database_manager.py
import psycopg2
from psycopg2 import Error
import pandas as pd
from src.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        print("Database connection established successfully.")
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None

def create_table_if_not_exists():
    """
    Creates the weather_data table if it doesn't already exist.
    This function can be run once during setup or as part of the pipeline start.
    """
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS weather_data (
                id SERIAL PRIMARY KEY,
                city VARCHAR(100) NOT NULL,
                region VARCHAR(100),
                country VARCHAR(100) NOT NULL,
                latitude DECIMAL(9,6),
                longitude DECIMAL(9,6),
                local_time TIMESTAMPTZ NOT NULL,
                temp_c DECIMAL(5,2),
                temp_f DECIMAL(5,2),
                condition_text VARCHAR(255),
                humidity INTEGER,
                wind_kph DECIMAL(5,2),
                pressure_mb DECIMAL(7,2),
                last_updated TIMESTAMPTZ NOT NULL,
                ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_city_local_time ON weather_data (city, local_time DESC);
            """
            cursor.execute(create_table_query)
            conn.commit()
            print("Table 'weather_data' checked/created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def insert_weather_data(df: pd.DataFrame):
    """
    Inserts a DataFrame of processed weather data into the PostgreSQL table.
    """
    if df.empty:
        print("No data to insert.")
        return

    conn = None
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            # Prepare the INSERT statement
            # Adjust column names if your DataFrame columns differ from DB
            columns = df.columns.tolist()
            # Remove 'wind_category' if it's not in the DB schema
            if 'wind_category' in columns:
                columns.remove('wind_category')

            # Ensure the order of columns matches the SQL VALUES order
            insert_statement = f"""
            INSERT INTO weather_data ({', '.join(columns)})
            VALUES ({', '.join(['%s'] * len(columns))})
            ON CONFLICT (id) DO NOTHING; -- Prevents duplicate inserts if id exists (e.g., from re-running)
            """
            # If you don't have a unique ID that can conflict, you might remove ON CONFLICT.
            # For this project, you'll likely insert new rows each time.
            
            # Convert DataFrame rows to a list of tuples for executemany
            data_to_insert = [tuple(row[col] for col in columns) for index, row in df.iterrows()]
            
            cursor.executemany(insert_statement, data_to_insert)
            conn.commit()
            print(f"Successfully inserted {len(df)} records into weather_data.")
    except Error as e:
        print(f"Error inserting data into PostgreSQL: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def fetch_weather_data_from_db(city: str = None, limit: int = 100) -> pd.DataFrame:
    """
    Fetches weather data from the database, optionally filtered by city.
    """
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            query = "SELECT * FROM weather_data"
            params = []
            if city:
                query += " WHERE city = %s"
                params.append(city)
            query += " ORDER BY local_time DESC LIMIT %s;"
            params.append(limit)

            df = pd.read_sql_query(query, conn, params=params)
            return df
    except Error as e:
        print(f"Error fetching data from PostgreSQL: {e}")
        return pd.DataFrame() # Return empty DataFrame on error
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Test DB connection and table creation
    create_table_if_not_exists()

    # Example of inserting dummy data (for testing)
    from datetime import datetime, timedelta
    dummy_data = {
        "city": ["TestCity", "TestCity"],
        "region": ["TestRegion", "TestRegion"],
        "country": ["TestCountry", "TestCountry"],
        "latitude": [10.0, 10.1],
        "longitude": [20.0, 20.1],
        "local_time": [datetime.now(), datetime.now() - timedelta(hours=1)],
        "temp_c": [25.0, 24.5],
        "temp_f": [77.0, 76.1],
        "condition_text": ["Sunny", "Cloudy"],
        "humidity": [60, 65],
        "wind_kph": [10.0, 12.0],
        "pressure_mb": [1010.0, 1009.5],
        "last_updated": [datetime.now(), datetime.now() - timedelta(hours=1)],
        "ingestion_timestamp": [datetime.utcnow(), datetime.utcnow()]
    }
    dummy_df = pd.DataFrame(dummy_data)
    # If you remove 'id' from dummy_data, and the table has SERIAL ID, it will auto-increment.
    # If you include 'id' here, make sure it's unique if you have an ON CONFLICT (id) clause.
    
    # insert_weather_data(dummy_df) # Uncomment to test insertion
    
    # Test fetching data
    fetched_df = fetch_weather_data_from_db(city="TestCity")
    if not fetched_df.empty:
        print("\nFetched Data:")
        print(fetched_df.to_string())