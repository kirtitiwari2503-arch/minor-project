from live_data import get_live_data


# Set the city for fetching live data
city = "Mumbai"

# Get live air-quality and weather data
data = get_live_data(city)

print("\nLive Data:")

# Check whether live data was fetched successfully
if data is not None:

    # Display each live data value
    for key, value in data.items():
        print(f"{key}: {value}")

else:
    # Display an error message if live data could not be fetched
    print("Could not fetch live data.")