import pandas as pd

# =========================================
# 1. LOAD RAW DATASET
# =========================================

df = pd.read_csv("data/air_quality_raw.csv")

print("Original Dataset Shape:")
print(df.shape)

# =========================================
# 2. DATE PREPROCESSING
# =========================================

print("\nOriginal Data Types:")
print(df.dtypes)

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Check invalid dates
print("\nInvalid dates:", df["date"].isna().sum())

# Sort by city and date
df = df.sort_values(["city", "date"]).reset_index(drop=True)

# =========================================
# 3. MISSING VALUE CHECK & HANDLING
# =========================================

print("\nMissing Values:")
print(df.isnull().sum())

if df.isnull().sum().sum() > 0:

    numerical_columns = df.select_dtypes(include="number").columns

    for col in numerical_columns:
        df[col] = df[col].fillna(df[col].median())

    categorical_columns = df.select_dtypes(include="object").columns

    for col in categorical_columns:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].mode()[0])

    print("\nMissing values handled.")

else:
    print("\nNo missing values found.")

# =========================================
# 4. DUPLICATE CHECK & HANDLING
# =========================================

duplicate_count = df.duplicated().sum()

print("\nDuplicate Rows:", duplicate_count)

if duplicate_count > 0:
    df = df.drop_duplicates()
    print("Duplicates removed:", duplicate_count)
else:
    print("No duplicate rows found.")

# =========================================
# 5. INVALID VALUE CHECK
# =========================================

pollutants = ["pm25", "pm10", "no2", "so2", "co", "o3"]

print("\nNegative Pollutant Values:")

for col in pollutants:
    print(col, ":", (df[col] < 0).sum())

print("\nNegative AQI:", (df["aqi"] < 0).sum())

# =========================================
# 6. OUTLIER DETECTION USING IQR
# =========================================

print("\nOutlier Summary:")

for col in pollutants:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_count = (
        (df[col] < lower_bound) |
        (df[col] > upper_bound)
    ).sum()

    print(
        col,
        "-> Outliers:", outlier_count,
        "| Lower:", round(lower_bound, 2),
        "| Upper:", round(upper_bound, 2)
    )

# IMPORTANT:
# Outliers are detected but NOT automatically removed.
# Extreme pollution values may represent genuine observations.

# =========================================
# 7. FINAL VALIDATION
# =========================================

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum().sum())

print("\nDuplicate Rows After Cleaning:")
print(df.duplicated().sum())

print("\nNegative Values After Cleaning:")

for col in pollutants:
    print(col, ":", (df[col] < 0).sum())

print("\nFinal AQI Range:")
print("Minimum:", df["aqi"].min())
print("Maximum:", df["aqi"].max())

# =========================================
# 8. SAVE FINAL CLEAN DATASET
# =========================================

df.to_csv("data/air_quality_cleaned.csv", index=False)

print("\nPreprocessing completed successfully!")
print("Final dataset saved as: air_quality_cleaned.csv")