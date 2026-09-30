import pandas as pd

from openweather_api import (
    get_coordinates,
    get_air_quality,
    extract_air_quality_data
)


# Load feature-engineered dataset
df = pd.read_csv(
    "data/air_quality_feature_engineered.csv"
)

df["date"] = pd.to_datetime(
    df["date"]
)

# Select Mumbai historical data
mumbai_data = df[
    df["city"] == "Mumbai"
].copy()

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


# Historical ranges
pollutants = [
    "pm25",
    "pm10",
    "no2",
    "so2",
    "co",
    "o3"
]

print("\nMumbai historical ranges:")

for pollutant in pollutants:

    print(
        f"{pollutant}: "
        f"min={mumbai_data[pollutant].min():.3f}, "
        f"max={mumbai_data[pollutant].max():.3f}, "
        f"mean={mumbai_data[pollutant].mean():.3f}"
    )


# Get Mumbai coordinates
city = "Mumbai"

coordinates = get_coordinates(city)

if coordinates is None:
    print("\nCould not get coordinates.")
    raise SystemExit

lat, lon = coordinates

print("\nMumbai coordinates:")
print("Latitude:", lat)
print("Longitude:", lon)


# Get live air-quality data
air_quality_response = get_air_quality(
    lat,
    lon
)

if air_quality_response is None:
    print("\nCould not get live air-quality data.")
    raise SystemExit


# Extract pollutant data
live_data = extract_air_quality_data(
    air_quality_response
)

print("\nLive OpenWeather data:")

for key, value in live_data.items():

    print(
        f"{key}: {value}"
    )