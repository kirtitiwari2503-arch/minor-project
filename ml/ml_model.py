import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


# Load cleaned dataset
df = pd.read_csv("data/air_quality_cleaned.csv")

print("Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Sort data by city and date
df = df.sort_values(["city", "date"]).reset_index(drop=True)


# Create next-day AQI target
df["target_aqi"] = df.groupby("city")["aqi"].shift(-1)

# Remove rows where next-day AQI is not available
df = df.dropna(subset=["target_aqi"]).reset_index(drop=True)

print("\nDataset Shape After Creating Target:")
print(df.shape)


# Select input features
features = [
    "city",
    "pm25",
    "pm10",
    "no2",
    "so2",
    "co",
    "o3",
    "aqi"
]

X = df[features]
y = df["target_aqi"]


# Identify categorical and numerical features
categorical_features = ["city"]

numerical_features = [
    "pm25",
    "pm10",
    "no2",
    "so2",
    "co",
    "o3",
    "aqi"
]


# Encode city and keep numerical features unchanged
preprocessor = ColumnTransformer(
    transformers=[
        (
            "city",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numbers",
            "passthrough",
            numerical_features
        )
    ]
)


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Data Shape:")
print(X_train.shape)

print("\nTesting Data Shape:")
print(X_test.shape)


# Define models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=100,
        random_state=42
    )
}


# Train models and generate predictions
predictions = {}

for name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions[name] = pipeline.predict(X_test)

    print(f"\n{name} training completed.")
    print("Number of predictions:", len(predictions[name]))


print("\nPart 1 ML Training Completed.")