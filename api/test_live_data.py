from live_data import get_live_data


city = "Mumbai"

data = get_live_data(city)

print("\nLive Data:")

if data is not None:

    for key, value in data.items():
        print(f"{key}: {value}")

else:
    print("Could not fetch live data.")