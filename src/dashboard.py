# src/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from src.database_manager import fetch_weather_data_from_db
from src.config import CITIES # To populate city dropdown

st.set_page_config(layout="wide", page_title="Global Weather Insights")

st.title("🌎 Global Weather Insights Dashboard")
st.markdown("---")

# Sidebar for filters
st.sidebar.header("Filter Data")

# City selection
selected_city = st.sidebar.selectbox("Select City", ["All Cities"] + CITIES)

# Limit records
record_limit = st.sidebar.slider("Number of Recent Records", 10, 500, 100)

# Fetch data based on filters
@st.cache_data(ttl=600) # Cache data for 10 minutes to avoid re-fetching on every interaction
def get_data_from_db(city: str | None, limit: int) -> pd.DataFrame:
    if city == "All Cities":
        return fetch_weather_data_from_db(limit=limit)
    else:
        return fetch_weather_data_from_db(city=city, limit=limit)

df = get_data_from_db(selected_city, record_limit)

if df.empty:
    st.warning("No data available. Please run the data pipeline (`python src/main_pipeline.py`) to fetch data.")
else:
    # Ensure correct data types for plotting
    df['local_time'] = pd.to_datetime(df['local_time'])
    df['last_updated'] = pd.to_datetime(df['last_updated'])

    # Display raw data (optional, good for debugging)
    # st.subheader("Raw Data Preview")
    # st.dataframe(df.head())

    st.markdown(f"**Showing {len(df)} records for {selected_city}**")

    # --- Key Metrics ---
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    if not df.empty:
        avg_temp_c = df['temp_c'].mean()
        avg_humidity = df['humidity'].mean()
        max_wind_kph = df['wind_kph'].max()
        most_common_condition = df['condition_text'].mode()[0] if not df['condition_text'].empty else "N/A"

        col1.metric("Average Temperature (°C)", f"{avg_temp_c:.1f}")
        col2.metric("Average Humidity (%)", f"{avg_humidity:.1f}")
        col3.metric("Max Wind Speed (kph)", f"{max_wind_kph:.1f}")
        col4.metric("Most Common Condition", most_common_condition)

    st.markdown("---")

    # --- Visualizations ---
    st.subheader("Temperature Trends Over Time")
    if not df.empty:
        fig_temp = px.line(df, x='local_time', y='temp_c', color='city',
                           title='Temperature Over Time (°C)',
                           labels={'local_time': 'Time', 'temp_c': 'Temperature (°C)'})
        st.plotly_chart(fig_temp, use_container_width=True)
    else:
        st.info("No data to show temperature trends.")

    st.subheader("Humidity Distribution")
    if not df.empty:
        fig_humidity = px.histogram(df, x='humidity', nbins=20, color='city',
                                    title='Humidity Distribution',
                                    labels={'humidity': 'Humidity (%)'})
        st.plotly_chart(fig_humidity, use_container_width=True)
    else:
        st.info("No data to show humidity distribution.")

    st.subheader("Wind Speed vs. Temperature")
    if not df.empty:
        fig_scatter = px.scatter(df, x='temp_c', y='wind_kph', color='city',
                                 size='humidity', hover_data=['condition_text', 'local_time'],
                                 title='Wind Speed vs. Temperature',
                                 labels={'temp_c': 'Temperature (°C)', 'wind_kph': 'Wind Speed (kph)'})
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("No data to show wind speed vs. temperature.")

    st.subheader("Weather Conditions Breakdown")
    if not df.empty:
        condition_counts = df['condition_text'].value_counts().reset_index()
        condition_counts.columns = ['Condition', 'Count']
        fig_pie = px.pie(condition_counts, values='Count', names='Condition',
                         title='Distribution of Weather Conditions')
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No data to show weather conditions breakdown.")

st.markdown("---")
st.caption("Data powered by WeatherAPI.com")