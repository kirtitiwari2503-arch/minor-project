from openweather_api import (
    get_coordinates,
    get_air_quality,
    extract_air_quality_data,
    get_weather
)


def get_live_data(city):

    coordinates = get_coordinates(city)

    if coordinates is None:
        return None

    lat, lon = coordinates

    air_quality_response = get_air_quality(
        lat,
        lon
    )

    if air_quality_response is None:
        return None

    air_quality = extract_air_quality_data(
        air_quality_response
    )

    weather_response = get_weather(
        lat,
        lon
    )

    if weather_response is None:
        return None

    # Extract weather data from raw OpenWeather response
    main_data = weather_response.get(
        "main",
        {}
    )

    weather_list = weather_response.get(
        "weather",
        []
    )

    wind_data = weather_response.get(
        "wind",
        {}
    )

    if weather_list:
        weather_description = weather_list[0].get(
            "description"
        )
    else:
        weather_description = None

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

    return data