import pandas as pd

# Load the cleaned air quality dataset
df = pd.read_csv("data/air_quality_cleaned.csv")

# Display the original dataset shape
print("Original Dataset Shape:")
print(df.shape)

# Convert the date column to datetime format
df["date"] = pd.to_datetime(df["date"])

# Sort the data by city and date
df = df.sort_values(["city", "date"]).reset_index(drop=True)

# Display the date range of the dataset
print("\nDate Range:")
print(df["date"].min(), "to", df["date"].max())

# Display the cities present in the dataset
print("\nCities:")
print(df["city"].unique())

# Create the next-day AQI as the prediction target
df["target_aqi"] = df.groupby("city")["aqi"].shift(-1)

# Create previous-day AQI features
df["aqi_lag1"] = df.groupby("city")["aqi"].shift(1)
df["aqi_lag2"] = df.groupby("city")["aqi"].shift(2)
df["aqi_lag3"] = df.groupby("city")["aqi"].shift(3)

# Create the 3-day rolling average of previous AQI values
df["aqi_rolling3"] = (
    df.groupby("city")["aqi"]
    .transform(lambda x: x.shift(1).rolling(3).mean())
)

# Create the 7-day rolling average of previous AQI values
df["aqi_rolling7"] = (
    df.groupby("city")["aqi"]
    .transform(lambda x: x.shift(1).rolling(7).mean())
)

# Get the next date for each city
df["next_date"] = df.groupby("city")["date"].shift(-1)

# Calculate the difference between consecutive dates
df["date_difference"] = (
    df["next_date"] - df["date"]
).dt.days

# Display the distribution of date differences
print("\nDate Difference:")
print(df["date_difference"].value_counts().sort_index())

# Count records where the next date is not exactly one day later
print("\nRecords Where Next Date Is Not Exactly 1 Day:")
print((df["date_difference"] != 1).sum())

# Check missing values in the newly created features
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

# Remove rows with missing feature or target values
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

# Remove the temporary date-checking columns
df = df.drop(columns=["next_date", "date_difference"])

# Display the final dataset shape
print("\nFinal Dataset Shape:")
print(df.shape)

# Display the main feature-engineered columns
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

# Save the feature-engineered dataset
df.to_csv(
    "data/air_quality_feature_engineered.csv",
    index=False
)

# Display the completion message
print("\nFeature-engineered dataset saved successfully.")