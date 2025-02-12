import streamlit as st
import requests
import plotly.express as px
import geocoder

# API Configuration
WEATHER_API_KEY = "d24586cb970848408bb84701252601"
WEATHER_API_URL = "https://api.weatherapi.com/v1/forecast.json"

# Streamlit UI Configuration
st.set_page_config(page_title="Weather Forecast", layout="wide")
st.title("🌤️ Weather Forecast Application")

# Sidebar for User Inputs
st.sidebar.header("🔍 Weather Search Options")
coordinates = st.sidebar.text_input("Enter Coordinates (lat, lon) or City Name", "")
forecast_days = st.sidebar.slider("📅 Select Forecast Days", 1, 7, 3)

# Function to Fetch Weather Data
def fetch_weather(coords, days):
    url = f"{WEATHER_API_URL}?key={WEATHER_API_KEY}&q={coords}&days={days}&aqi=yes&alerts=yes&hourly=1"
    response = requests.get(url)
    return response.json()

# Function to Display Weather Data
def display_weather_data(weather_data):
    location_data = weather_data["location"]
    forecast = weather_data["forecast"]["forecastday"]
    current = weather_data["current"]

    st.subheader(f"📍 Location: {location_data['name']}, {location_data['region']}, {location_data['country']}")
    st.markdown(f"**🕒 Local Time:** {location_data['localtime']}")
    st.image(f"https:{current['condition']['icon']}", width=100)
    st.markdown(f"**🌥 Condition:** {current['condition']['text']}")

    # Current Weather Overview
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**🌡 Temperature:** {current['temp_c']}°C / {current['temp_f']}°F")
        st.markdown(f"**🤒 Feels Like:** {current['feelslike_c']}°C / {current['feelslike_f']}°F")
        st.markdown(f"**💨 Wind:** {current['wind_kph']} kph, {current['wind_dir']}")
        st.markdown(f"**🌊 Pressure:** {current['pressure_mb']} mb")
    with col2:
        st.markdown(f"**💧 Humidity:** {current['humidity']}%")
        st.markdown(f"**☁️ Cloud Cover:** {current['cloud']}%")
        st.markdown(f"**👀 Visibility:** {current['vis_km']} km")
        st.markdown(f"**🔆 UV Index:** {current['uv']}")

    # Air Quality
    st.subheader("🌬 Air Quality Index")
    air_quality = current["air_quality"]
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"**CO:** {air_quality['co']} μg/m³")
        st.markdown(f"**NO2:** {air_quality['no2']} μg/m³")
        st.markdown(f"**O3:** {air_quality['o3']} μg/m³")
    with col4:
        st.markdown(f"**SO2:** {air_quality['so2']} μg/m³")
        st.markdown(f"**PM2.5:** {air_quality['pm2_5']} μg/m³")
        st.markdown(f"**PM10:** {air_quality['pm10']} μg/m³")

    # Forecast Graphs
    st.subheader("📊 Hourly Weather Trends")

    # Hourly Forecast Data
    hourly_times, hourly_temps, hourly_humidities, hourly_clouds, hourly_feelslike = [], [], [], [], []
    for day in forecast:
        for hour in day["hour"]:
            hourly_times.append(hour["time"])
            hourly_temps.append(hour["temp_c"])
            hourly_humidities.append(hour["humidity"])
            hourly_clouds.append(hour["cloud"])
            hourly_feelslike.append(hour["feelslike_c"])

    # Hourly Temperature Trend
    fig_temp = px.line(
        x=hourly_times, y=hourly_temps,
        labels={"x": "Time", "y": "Temperature (°C)"},
        title="Hourly Temperature Trend"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    # Hourly Humidity Trend
    fig_humidity = px.line(
        x=hourly_times, y=hourly_humidities,
        labels={"x": "Time", "y": "Humidity (%)"},
        title="Hourly Humidity Trend"
    )
    st.plotly_chart(fig_humidity, use_container_width=True)

    # Hourly Cloud Cover Trend
    fig_cloud = px.line(
        x=hourly_times, y=hourly_clouds,
        labels={"x": "Time", "y": "Cloud Cover (%)"},
        title="Hourly Cloud Cover Trend"
    )
    st.plotly_chart(fig_cloud, use_container_width=True)

    # Hourly Feels Like Temperature
    fig_feelslike = px.line(
        x=hourly_times, y=hourly_feelslike,
        labels={"x": "Time", "y": "Feels Like Temperature (°C)"},
        title="Hourly Feels Like Temperature"
    )
    st.plotly_chart(fig_feelslike, use_container_width=True)

# Fetch User Location Using Geocoder
if st.sidebar.button("📍 Get Location"):
    location = geocoder.ip('me')
    if location.latlng:
        coordinates = f"{location.latlng[0]},{location.latlng[1]}"
        st.sidebar.success(f"✅ Location detected: {coordinates}")

        # Automatically fetch and display weather data after detecting location
        weather_data = fetch_weather(coordinates, forecast_days)
        if weather_data:
            st.sidebar.success(f"✅ Weather data fetched for: {coordinates}")
            display_weather_data(weather_data)
        else:
            st.sidebar.error("❌ Failed to retrieve weather data. Please try again.")
    else:
        st.sidebar.warning("⚠️ Unable to detect location. Please enter coordinates manually.")

# Manual Search (if coordinates are entered manually)
if st.sidebar.button("📡 Get Weather"):
    if coordinates:
        weather_data = fetch_weather(coordinates, forecast_days)
        if weather_data:
            st.sidebar.success(f"✅ Weather data fetched for: {coordinates}")
            display_weather_data(weather_data)
        else:
            st.sidebar.error("❌ Failed to retrieve weather data. Please try again.")
    else:
        st.sidebar.error("⚠️ No location detected. Please enter coordinates or allow location access.")