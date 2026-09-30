import pandas as pd

# Load the feature-engineered dataset
df = pd.read_csv("data/air_quality_feature_engineered.csv")

# Select the numerical columns for correlation analysis
numeric_cols = [

    "pm25",

    "pm10",

    "no2",

    "so2",

    "co",

    "o3",

    "aqi",

    "aqi_lag1",

    "aqi_lag2",

    "aqi_lag3",

    "aqi_rolling3",

    "aqi_rolling7",

    "target_aqi"

]

# Calculate the correlation of each numerical feature with next-day AQI
print("\nCorrelation with next-day AQI:\n")

correlation = (

    df[numeric_cols]

    .corr()["target_aqi"]

    .sort_values(ascending=False)

)

# Display the correlation results
print(correlation)

# Display statistics for the next-day AQI target
print("\nTarget AQI statistics:")

print(df["target_aqi"].describe())

# Display statistics for the current AQI
print("\nCurrent AQI statistics:")

print(df["aqi"].describe())

# Display statistics for the previous-day AQI
print("\nLag 1 statistics:")

print(df["aqi_lag1"].describe())