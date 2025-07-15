-- scripts/setup_db.sql
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

-- Add an index for faster lookups by city and time
CREATE INDEX IF NOT EXISTS idx_city_local_time ON weather_data (city, local_time DESC);