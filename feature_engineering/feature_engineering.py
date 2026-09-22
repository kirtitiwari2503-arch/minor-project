import pandas as pd

# =========================================
# 1. LOAD CLEANED DATASET
# =========================================

df = pd.read_csv("data/air_quality_cleaned.csv")

print("Original Dataset Shape:")
print(df.shape)


# =========================================
# 2. CONVERT DATE COLUMN
# =========================================

df["date"] = pd.to_datetime(df["date"])

# Sort data city-wise and date-wise
df = df.sort_values(["city", "date"]).reset_index(drop=True)

print("\nDate Range:")
print(df["date"].min(), "to", df["date"].max())

print("\nCities:")
print(df["city"].unique())


# =========================================
# 3. CREATE NEXT-DAY AQI TARGET
# =========================================

df["target_aqi"] = (
    df.groupby("city")["aqi"].shift(-1)
)

print("\nSample of Next-Day AQI Target:")
print(
    df[
        ["city", "date", "aqi", "target_aqi"]
    ].head(10)
)


# =========================================
# 4. CHECK DATE CONTINUITY
# =========================================

df["next_date"] = (
    df.groupby("city")["date"].shift(-1)
)

df["date_difference"] = (
    df["next_date"] - df["date"]
).dt.days

print("\nDate Difference Between Consecutive Records:")
print(
    df["date_difference"]
    .value_counts()
    .sort_index()
)

print("\nRecords Where Next Date Is Not Exactly 1 Day:")
print(
    (df["date_difference"] != 1).sum()
)


# =========================================
# 5. CHECK TARGET MISSING VALUES
# =========================================

print("\nMissing Target Values:")
print(
    df["target_aqi"].isnull().sum()
)


# =========================================
# 6. REMOVE LAST RECORD OF EACH CITY
# =========================================

df = df.dropna(
    subset=["target_aqi"]
).reset_index(drop=True)


# =========================================
# 7. FINAL DATASET SHAPE
# =========================================

print("\nFinal Dataset Shape:")
print(df.shape)


# =========================================
# 8. FINAL DATASET PREVIEW
# =========================================

print("\nFinal Feature-Engineered Dataset:")
print(
    df[
        [
            "city",
            "date",
            "aqi",
            "pm25",
            "pm10",
            "no2",
            "so2",
            "co",
            "o3",
            "target_aqi"
        ]
    ].head(10)
)