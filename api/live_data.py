from openweather_api import (
    get_coordinates,
    get_air_quality,
    extract_air_quality_data,
    get_weather
)


# Get live air-quality and weather data for a city
def get_live_data(city):

    # Get the coordinates of the selected city
    coordinates = get_coordinates(city)

    # Return None if coordinates are not available
    if coordinates is None:
        return None

    # Store latitude and longitude
    lat, lon = coordinates

    # Get live air-quality data
    air_quality_response = get_air_quality(
        lat,
        lon
    )

    # Return None if air-quality data is not available
    if air_quality_response is None:
        return None

    # Extract pollutant values from the air-quality response
    air_quality = extract_air_quality_data(
        air_quality_response
    )

    # Get current weather data
    weather_response = get_weather(
        lat,
        lon
    )

    # Return None if weather data is not available
    if weather_response is None:
        return None

    # Extract the main weather information
    main_data = weather_response.get(
        "main",
        {}
    )

    # Extract the weather description
    weather_list = weather_response.get(
        "weather",
        []
    )

    # Extract wind information
    wind_data = weather_response.get(
        "wind",
        {}
    )

    # Get the weather description if available
    if weather_list:
        weather_description = weather_list[0].get(
            "description"
        )
    else:
        weather_description = None

    # Store all live air-quality and weather data
    data = {
        "city": city,
        "latitude": lat,
        "longitude": lon,

        "openweather_aqi": air_quality.get(
            "openweather_aqi"
        ),

        "pm25": air_quality.get("pm25"),
        "pm10": air_quality.get("pm10"),
        "no2": air_quality.get("no2"),
        "so2": air_quality.get("so2"),
        "co": air_quality.get("co"),
        "o3": air_quality.get("o3"),

        "temperature": main_data.get(
            "temp"
        ),

        "feels_like": main_data.get(
            "feels_like"
        ),

        "humidity": main_data.get(
            "humidity"
        ),

        "pressure": main_data.get(
            "pressure"
        ),

        "weather": weather_description,

        "wind_speed": wind_data.get(
            "speed"
        )
    }

    # Return the collected live data
    return data