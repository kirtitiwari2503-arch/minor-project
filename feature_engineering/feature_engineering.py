import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/air_quality_cleaned.csv")

print("Original Dataset Shape:")
print(df.shape)

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Sort data city-wise and date-wise
df = df.sort_values(["city", "date"]).reset_index(drop=True)

print("\nDate Range:")
print(df["date"].min(), "to", df["date"].max())

print("\nCities:")
print(df["city"].unique())

# Create next-day AQI target
df["target_aqi"] = df.groupby("city")["aqi"].shift(-1)

# Create AQI lag features
df["aqi_lag1"] = df.groupby("city")["aqi"].shift(1)
df["aqi_lag2"] = df.groupby("city")["aqi"].shift(2)
df["aqi_lag3"] = df.groupby("city")["aqi"].shift(3)

# Create rolling AQI features
df["aqi_rolling3"] = (
    df.groupby("city")["aqi"]
    .transform(lambda x: x.shift(1).rolling(3).mean())
)

df["aqi_rolling7"] = (
    df.groupby("city")["aqi"]
    .transform(lambda x: x.shift(1).rolling(7).mean())
)

# Check date continuity
df["next_date"] = df.groupby("city")["date"].shift(-1)

df["date_difference"] = (
    df["next_date"] - df["date"]
).dt.days

print("\nDate Difference:")
print(df["date_difference"].value_counts().sort_index())

print("\nRecords Where Next Date Is Not Exactly 1 Day:")
print((df["date_difference"] != 1).sum())

# Check missing values
print("\nMissing Values:")
print(
    df[
        [
            "target_aqi",
            "aqi_lag1",
            "aqi_lag2",
            "aqi_lag3",
            "aqi_rolling3",
            "aqi_rolling7"
        ]
    ].isnull().sum()
)

# Remove rows with missing values
df = df.dropna(
    subset=[
        "target_aqi",
        "aqi_lag1",
        "aqi_lag2",
        "aqi_lag3",
        "aqi_rolling3",
        "aqi_rolling7"
    ]
).reset_index(drop=True)

# Remove temporary columns
df = df.drop(columns=["next_date", "date_difference"])

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFeature-Engineered Dataset:")
print(
    df[
        [
            "city",
            "date",
            "aqi",
            "aqi_lag1",
            "aqi_lag2",
            "aqi_lag3",
            "aqi_rolling3",
            "aqi_rolling7",
            "target_aqi"
        ]
    ].head(10)
)

# Save feature-engineered dataset
df.to_csv(
    "data/air_quality_feature_engineered.csv",
    index=False
)

print("\nFeature-engineered dataset saved successfully.")