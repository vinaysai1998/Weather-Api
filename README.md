# Data-Driven Insights Dashboard: Global Weather Analysis

## Project Overview
This project builds an automated data pipeline to collect real-time weather data from the WeatherAPI.com, process it, store it in a PostgreSQL database, and visualize key insights through a Streamlit dashboard. It demonstrates skills in data ingestion, ETL (Extract, Transform, Load), database management, and data visualization.

## Features
- Fetches current weather data for multiple predefined cities.
- Parses and transforms raw JSON data into a structured format.
- Stores processed weather data in a PostgreSQL database.
- Provides a user-friendly web dashboard to explore weather trends and statistics.

## Technologies Used
- **Python 3.9+**: Core programming language.
- **`requests`**: For making HTTP requests to the WeatherAPI.
- **`psycopg2`**: PostgreSQL adapter for Python.
- **`pandas`**: For efficient data manipulation and analysis.
- **`streamlit`**: For creating interactive web dashboards.
- **PostgreSQL**: Relational database for storing weather data.
- **Docker & Docker Compose** (Optional but Recommended): For easy setup of the PostgreSQL database.

## Project Structure