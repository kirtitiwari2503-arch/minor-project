import pandas as pd

from openweather_api import (
    get_coordinates,
    get_air_quality,
    extract_air_quality_data
)


# Load the feature-engineered dataset
df = pd.read_csv(
    "data/air_quality_feature_engineered.csv"
)

# Convert the date column to datetime format
df["date"] = pd.to_datetime(
    df["date"]
)

# Select historical data for Mumbai
mumbai_data = df[
    df["city"] == "Mumbai"
].copy()

# Display the latest Mumbai historical records
print("Mumbai historical data:")
print(
    mumbai_data[
        [
            "date",
            "pm25",
            "pm10",
            "no2",
            "so2",
            "co",
            "o3",
            "aqi"
        ]
    ].tail(7)
)


# Define the pollutants to check
pollutants = [
    "pm25",
    "pm10",
    "no2",
    "so2",
    "co",
    "o3"
]

# Display the historical minimum, maximum and mean values
print("\nMumbai historical ranges:")

for pollutant in pollutants:

    print(
        f"{pollutant}: "
        f"min={mumbai_data[pollutant].min():.3f}, "
        f"max={mumbai_data[pollutant].max():.3f}, "
        f"mean={mumbai_data[pollutant].mean():.3f}"
    )


# Set the city name for the API request
city = "Mumbai"

# Get the latitude and longitude of Mumbai
coordinates = get_coordinates(city)

# Stop the program if coordinates cannot be obtained
if coordinates is None:
    print("\nCould not get coordinates.")
    raise SystemExit

# Store latitude and longitude separately
lat, lon = coordinates

# Display Mumbai coordinates
print("\nMumbai coordinates:")
print("Latitude:", lat)
print("Longitude:", lon)


# Get the current air-quality data using the coordinates
air_quality_response = get_air_quality(
    lat,
    lon
)

# Stop the program if live air-quality data cannot be obtained
if air_quality_response is None:
    print("\nCould not get live air-quality data.")
    raise SystemExit


# Extract the required pollutant values from the API response
live_data = extract_air_quality_data(
    air_quality_response
)

# Display the live OpenWeather pollutant data
print("\nLive OpenWeather data:")

for key, value in live_data.items():

    print(
        f"{key}: {value}"
    )