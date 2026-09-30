import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the OpenWeather API key from the environment
API_KEY = os.getenv("OPENWEATHER_API_KEY")


# Get latitude and longitude for a city
def get_coordinates(city):
    # OpenWeather geocoding API URL
    url = "https://api.openweathermap.org/geo/1.0/direct"

    # Parameters required for the geocoding request
    params = {
        "q": f"{city},IN",
        "limit": 1,
        "appid": API_KEY
    }

    # Send the request to the geocoding API
    response = requests.get(url, params=params)

    # Check whether the API request was successful
    if response.status_code != 200:
        print("Geocoding API error:", response.status_code)
        print(response.text)
        return None

    # Convert the API response to JSON
    data = response.json()

    # Check whether the city was found
    if not data:
        print("City not found.")
        return None

    # Return the latitude and longitude
    return data[0]["lat"], data[0]["lon"]


# Get current air-quality data using latitude and longitude
def get_air_quality(lat, lon):
    # OpenWeather air pollution API URL
    url = "https://api.openweathermap.org/data/2.5/air_pollution"

    # Parameters required for the air-quality request
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }

    # Send the request to the air-quality API
    response = requests.get(url, params=params)

    # Check whether the API request was successful
    if response.status_code != 200:
        print("Air Pollution API error:", response.status_code)
        print(response.text)
        return None

    # Return the API response as JSON
    return response.json()


# Extract AQI and pollutant values from the API response
def extract_air_quality_data(data):
    # Get the first air-quality record
    air_data = data["list"][0]

    # Return the required AQI and pollutant values
    return {
        "openweather_aqi": air_data["main"]["aqi"],
        "co": air_data["components"]["co"],
        "no2": air_data["components"]["no2"],
        "o3": air_data["components"]["o3"],
        "so2": air_data["components"]["so2"],
        "pm25": air_data["components"]["pm2_5"],
        "pm10": air_data["components"]["pm10"]
    }


# Get current weather data using latitude and longitude
def get_weather(lat, lon):
    # OpenWeather weather API URL
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Parameters required for the weather request
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    # Send the request to the weather API
    response = requests.get(url, params=params)

    # Check whether the API request was successful
    if response.status_code != 200:
        print("Weather API error:", response.status_code)
        print(response.text)
        return None

    # Return the API response as JSON
    return response.json()


# Extract useful weather values from the API response
def extract_weather_data(data):
    # Return the required weather information
    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }


# Set the city for testing the API
city = "Mumbai"

# Get the coordinates of the selected city
coordinates = get_coordinates(city)

# Continue only if coordinates are available
if coordinates:
    # Store latitude and longitude
    lat, lon = coordinates

    # Display city and coordinates
    print("City:", city)
    print("Latitude:", lat)
    print("Longitude:", lon)

    # Get current air-quality data
    air_quality = get_air_quality(lat, lon)

    # Continue if air-quality data is available
    if air_quality:
        # Extract pollutant values from the API response
        pollution_data = extract_air_quality_data(air_quality)

        print("\nCurrent Air Quality Data:")

        # Display each pollutant value
        for key, value in pollution_data.items():
            print(f"{key}: {value}")

    # Get current weather data
    weather_data = get_weather(lat, lon)

    # Continue if weather data is available
    if weather_data:
        # Extract useful weather information
        current_weather = extract_weather_data(weather_data)

        print("\nCurrent Weather Data:")

        # Display each weather value
        for key, value in current_weather.items():
            print(f"{key}: {value}")