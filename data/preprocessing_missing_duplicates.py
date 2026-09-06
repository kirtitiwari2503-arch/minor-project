
import pandas as pd

# Load Kirti's date-processed dataset
df = pd.read_csv("data/air_quality_date_processed.csv")

print("Original Dataset Shape:")
print(df.shape)

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Handle missing values if present
if df.isnull().sum().sum() > 0:

    numerical_columns = df.select_dtypes(include="number").columns

    for col in numerical_columns:
        df[col] = df[col].fillna(df[col].median())

    categorical_columns = df.select_dtypes(include="object").columns

    for col in categorical_columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    print("\nMissing values handled.")

else:
    print("\nNo missing values found.")

# Remove duplicates if present
duplicate_count = df.duplicated().sum()

if duplicate_count > 0:
    df = df.drop_duplicates()
    print("Duplicates removed:", duplicate_count)
else:
    print("No duplicate rows found.")

# Final verification
print("\nFinal Dataset Shape:")
print(df.shape)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nDuplicates After Cleaning:")
print(df.duplicated().sum())

# Save output
df.to_csv("data/air_quality_missing_duplicate_processed.csv", index=False)

print("\nProcessing completed!")
print("Output saved as air_quality_missing_duplicate_processed.csv")