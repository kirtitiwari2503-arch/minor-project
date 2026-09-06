import pandas as pd

# Load Tejal's processed dataset
df = pd.read_csv("data/air_quality_missing_duplicate_processed.csv")

print("Dataset Shape:")
print(df.shape)

# Columns containing pollutant values
pollutants = ["pm25", "pm10", "no2", "so2", "co", "o3"]

# Check negative values
print("\nNegative Pollutant Values:")

for col in pollutants:
    print(col, ":", (df[col] < 0).sum())

# Check negative AQI
print("\nNegative AQI:")
print((df["aqi"] < 0).sum())




# -----------------------------------------
# OUTLIER DETECTION USING IQR
# -----------------------------------------

print("\nOutlier Summary:")

for col in pollutants:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = (
        (df[col] < lower_bound) |
        (df[col] > upper_bound)
    ).sum()

    print(
        col,
        "-> Outliers:", outliers,
        "| Lower:", lower_bound,
        "| Upper:", upper_bound
    )


# -----------------------------------------
# FINAL VERIFICATION
# -----------------------------------------

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nNegative Values After Cleaning:")

for col in pollutants:
    print(col, ":", (df[col] < 0).sum())

print("\nFinal AQI Range:")
print("Minimum:", df["aqi"].min())
print("Maximum:", df["aqi"].max())


# -----------------------------------------
# SAVE FINAL DATASET
# -----------------------------------------

df.to_csv("data/air_quality_cleaned.csv", index=False)

print("\nProcessing completed!")
print("Final dataset saved as air_quality_cleaned.csv")
