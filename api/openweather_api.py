import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_coordinates(city):
    url = "https://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": f"{city},IN",
        "limit": 1,
        "appid": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Geocoding API error:", response.status_code)
        print(response.text)
        return None

    data = response.json()

    if not data:
        print("City not found.")
        return None

    return data[0]["lat"], data[0]["lon"]


def get_air_quality(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/air_pollution"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Air Pollution API error:", response.status_code)
        print(response.text)
        return None

    return response.json()


def extract_air_quality_data(data):
    air_data = data["list"][0]

    return {
        "openweather_aqi": air_data["main"]["aqi"],
        "co": air_data["components"]["co"],
        "no2": air_data["components"]["no2"],
        "o3": air_data["components"]["o3"],
        "so2": air_data["components"]["so2"],
        "pm25": air_data["components"]["pm2_5"],
        "pm10": air_data["components"]["pm10"]
    }


def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Weather API error:", response.status_code)
        print(response.text)
        return None

    return response.json()


def extract_weather_data(data):
    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }


city = "Mumbai"

coordinates = get_coordinates(city)

if coordinates:
    lat, lon = coordinates

    print("City:", city)
    print("Latitude:", lat)
    print("Longitude:", lon)

    air_quality = get_air_quality(lat, lon)

    if air_quality:
        pollution_data = extract_air_quality_data(air_quality)

        print("\nCurrent Air Quality Data:")

        for key, value in pollution_data.items():
            print(f"{key}: {value}")

    weather_data = get_weather(lat, lon)

    if weather_data:
        current_weather = extract_weather_data(weather_data)

        print("\nCurrent Weather Data:")

        for key, value in current_weather.items():
            print(f"{key}: {value}")