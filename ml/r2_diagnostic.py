import pandas as pd

df = pd.read_csv("data/air_quality_feature_engineered.csv")

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

print("\nCorrelation with next-day AQI:\n")

correlation = (
    df[numeric_cols]
    .corr()["target_aqi"]
    .sort_values(ascending=False)
)

print(correlation)

print("\nTarget AQI statistics:")
print(df["target_aqi"].describe())

print("\nCurrent AQI statistics:")
print(df["aqi"].describe())

print("\nLag 1 statistics:")
print(df["aqi_lag1"].describe())