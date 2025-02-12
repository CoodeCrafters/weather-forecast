import streamlit as st
import requests
import datetime
import plotly.express as px
import geocoder
from streamlit_lottie import st_lottie

# API Configuration
WEATHER_API_KEY = "d24586cb970848408bb84701252601"
WEATHER_API_URL = "https://api.weatherapi.com/v1/forecast.json"

# Streamlit UI
st.set_page_config(page_title="Weather Forecast", layout="wide")
st.title("🌤️ Weather Forecast Application")



# User Inputs
col1, col2 = st.columns([3, 1])
with col1:
    coordinates = st.text_area("Enter Coordinates (lat, lon) or City Name", "17.6850979,73.3944453")
    forecast_days = st.slider("Select Forecast Days", 1, 7, 3)

def fetch_weather(coords, days):
    url = f"{WEATHER_API_URL}?key={WEATHER_API_KEY}&q={coords}&days={days}&aqi=yes&alerts=yes&hourly=1"
    response = requests.get(url)
    return response.json()

# Fetch Location and Auto-search
if col2.button("📍 Get Location"):
    location = geocoder.ip('me')
    if location.latlng:
        coordinates = f"{location.latlng[0]},{location.latlng[1]}"
        st.success(f"Location detected: {coordinates}")
        weather_data = fetch_weather(coordinates, forecast_days)
    
        if weather_data:
            location = weather_data["location"]
            forecast = weather_data["forecast"]["forecastday"]
            
            st.subheader(f"📍 Location: {location['name']}, {location['region']}, {location['country']}")
            st.markdown(f"**Location ID:** {location['tz_id']}")
            st.markdown(f"**Local Time:** {location['localtime']}")
            
            # Weather Icon and Condition
            condition_icon = f"https:{weather_data['current']['condition']['icon']}"
            st.image(condition_icon, width=100)
            st.markdown(f"**Condition:** {weather_data['current']['condition']['text']}")
            
            # Current Weather Details
            st.subheader("🌡️ Current Weather Details")
            col3, col4 = st.columns(2)
            with col3:
                st.markdown(f"**Temperature:** {weather_data['current']['temp_c']}°C / {weather_data['current']['temp_f']}°F")
                st.markdown(f"**Feels Like:** {weather_data['current']['feelslike_c']}°C / {weather_data['current']['feelslike_f']}°F")
                st.markdown(f"**Wind:** {weather_data['current']['wind_kph']} kph / {weather_data['current']['wind_mph']} mph, {weather_data['current']['wind_dir']}")
                st.markdown(f"**Pressure:** {weather_data['current']['pressure_mb']} mb / {weather_data['current']['pressure_in']} in")
                st.markdown(f"**Precipitation:** {weather_data['current']['precip_mm']} mm / {weather_data['current']['precip_in']} in")
            with col4:
                st.markdown(f"**Humidity:** {weather_data['current']['humidity']}%")
                st.markdown(f"**Cloud Cover:** {weather_data['current']['cloud']}%")
                st.markdown(f"**Visibility:** {weather_data['current']['vis_km']} km / {weather_data['current']['vis_miles']} miles")
                st.markdown(f"**UV Index:** {weather_data['current']['uv']}")
                st.markdown(f"**Gust:** {weather_data['current']['gust_kph']} kph / {weather_data['current']['gust_mph']} mph")
            
            # Air Quality Details
            st.subheader("🌬️ Air Quality Details")
            air_quality = weather_data['current']['air_quality']
            col5, col6 = st.columns(2)
            with col5:
                st.markdown(f"**CO:** {air_quality['co']} μg/m³")
                st.markdown(f"**NO2:** {air_quality['no2']} μg/m³")
                st.markdown(f"**O3:** {air_quality['o3']} μg/m³")
            with col6:
                st.markdown(f"**SO2:** {air_quality['so2']} μg/m³")
                st.markdown(f"**PM2.5:** {air_quality['pm2_5']} μg/m³")
                st.markdown(f"**PM10:** {air_quality['pm10']} μg/m³")
            
            # Forecast with hourly details
            st.subheader("📅 Hourly Weather Forecast")
            hourly_times, hourly_temps, hourly_humidities, hourly_clouds, hourly_feelslike = [], [], [], [], []
            for day in forecast:
                for hour in day['hour']:
                    hourly_times.append(hour['time'])
                    hourly_temps.append(hour['temp_c'])
                    hourly_humidities.append(hour['humidity'])
                    hourly_clouds.append(hour['cloud'])
                    hourly_feelslike.append(hour['feelslike_c'])
            
            # Graphs
            st.subheader("📊 Weather Trends")
            fig = px.line(x=hourly_times, y=hourly_temps, labels={"x": "Time", "y": "Expected Temperature (°C)"}, title="Hourly Temperature Trend", line_shape="linear")
            st.plotly_chart(fig)
            
            fig2 = px.line(x=hourly_times, y=hourly_humidities, labels={"x": "Time", "y": "Humidity (%)"}, title="Hourly Humidity Trend")
            st.plotly_chart(fig2)
            
            fig3 = px.line(x=hourly_times, y=hourly_clouds, labels={"x": "Time", "y": "Cloud Cover (%)"}, title="Hourly Cloud Cover Trend")
            st.plotly_chart(fig3)
            
            fig4 = px.line(x=hourly_times, y=hourly_feelslike, labels={"x": "Time", "y": "Feels Like Temperature (°C)"}, title="Hourly Feels Like Temperature")
            st.plotly_chart(fig4)
        else:
            st.error("Failed to retrieve weather data. Please try again.")

# Manual Search
if st.button("🔍 Search"):
    weather_data = fetch_weather(coordinates, forecast_days)
    
    if weather_data:
        location = weather_data["location"]
        forecast = weather_data["forecast"]["forecastday"]
        
        st.subheader(f"📍 Location: {location['name']}, {location['region']}, {location['country']}")
        st.markdown(f"**Location ID:** {location['tz_id']}")
        st.markdown(f"**Local Time:** {location['localtime']}")
        
        # Weather Icon and Condition
        condition_icon = f"https:{weather_data['current']['condition']['icon']}"
        st.image(condition_icon, width=100)
        st.markdown(f"**Condition:** {weather_data['current']['condition']['text']}")
        
        # Current Weather Details
        st.subheader("🌡️ Current Weather Details")
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"**Temperature:** {weather_data['current']['temp_c']}°C / {weather_data['current']['temp_f']}°F")
            st.markdown(f"**Feels Like:** {weather_data['current']['feelslike_c']}°C / {weather_data['current']['feelslike_f']}°F")
            st.markdown(f"**Wind:** {weather_data['current']['wind_kph']} kph / {weather_data['current']['wind_mph']} mph, {weather_data['current']['wind_dir']}")
            st.markdown(f"**Pressure:** {weather_data['current']['pressure_mb']} mb / {weather_data['current']['pressure_in']} in")
            st.markdown(f"**Precipitation:** {weather_data['current']['precip_mm']} mm / {weather_data['current']['precip_in']} in")
        with col4:
            st.markdown(f"**Humidity:** {weather_data['current']['humidity']}%")
            st.markdown(f"**Cloud Cover:** {weather_data['current']['cloud']}%")
            st.markdown(f"**Visibility:** {weather_data['current']['vis_km']} km / {weather_data['current']['vis_miles']} miles")
            st.markdown(f"**UV Index:** {weather_data['current']['uv']}")
            st.markdown(f"**Gust:** {weather_data['current']['gust_kph']} kph / {weather_data['current']['gust_mph']} mph")
        
        # Air Quality Details
        st.subheader("🌬️ Air Quality Details")
        air_quality = weather_data['current']['air_quality']
        col5, col6 = st.columns(2)
        with col5:
            st.markdown(f"**CO:** {air_quality['co']} μg/m³")
            st.markdown(f"**NO2:** {air_quality['no2']} μg/m³")
            st.markdown(f"**O3:** {air_quality['o3']} μg/m³")
        with col6:
            st.markdown(f"**SO2:** {air_quality['so2']} μg/m³")
            st.markdown(f"**PM2.5:** {air_quality['pm2_5']} μg/m³")
            st.markdown(f"**PM10:** {air_quality['pm10']} μg/m³")
        
        # Forecast with hourly details
        st.subheader("📅 Hourly Weather Forecast")
        hourly_times, hourly_temps, hourly_humidities, hourly_clouds, hourly_feelslike = [], [], [], [], []
        for day in forecast:
            for hour in day['hour']:
                hourly_times.append(hour['time'])
                hourly_temps.append(hour['temp_c'])
                hourly_humidities.append(hour['humidity'])
                hourly_clouds.append(hour['cloud'])
                hourly_feelslike.append(hour['feelslike_c'])
        
        # Graphs
        st.subheader("📊 Weather Trends")
        fig = px.line(x=hourly_times, y=hourly_temps, labels={"x": "Time", "y": "Expected Temperature (°C)"}, title="Hourly Temperature Trend", line_shape="linear")
        st.plotly_chart(fig)
        
        fig2 = px.line(x=hourly_times, y=hourly_humidities, labels={"x": "Time", "y": "Humidity (%)"}, title="Hourly Humidity Trend")
        st.plotly_chart(fig2)
        
        fig3 = px.line(x=hourly_times, y=hourly_clouds, labels={"x": "Time", "y": "Cloud Cover (%)"}, title="Hourly Cloud Cover Trend")
        st.plotly_chart(fig3)
        
        fig4 = px.line(x=hourly_times, y=hourly_feelslike, labels={"x": "Time", "y": "Feels Like Temperature (°C)"}, title="Hourly Feels Like Temperature")
        st.plotly_chart(fig4)
    else:
        st.error("Failed to retrieve weather data. Please try again.")