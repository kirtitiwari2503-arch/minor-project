import pandas as pd

# Load raw dataset
df = pd.read_csv("data/air_quality_raw.csv")

# Check original data types
print("Original Data Types:")
print(df.dtypes)

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Check invalid dates
print("\nInvalid dates:", df["date"].isna().sum())

# Sort data by city and date
df = df.sort_values(["city", "date"]).reset_index(drop=True)

# Check updated data types
print("\nUpdated Data Types:")
print(df.dtypes)

# Display date range
print("\nDate Range:")
print("Start:", df["date"].min())
print("End:", df["date"].max())

# Save intermediate dataset
df.to_csv("data/air_quality_date_processed.csv", index=False)

print("\nDate preprocessing completed!")