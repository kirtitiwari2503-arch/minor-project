import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

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





import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# 1. LOAD CLEANED DATASET
# ============================================================

df = pd.read_csv("data/air_quality_cleaned.csv")

print("Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# 2. DATE PROCESSING
# ============================================================

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(
    ["city", "date"]
).reset_index(drop=True)


# ============================================================
# 3. CREATE NEXT-DAY AQI TARGET
# ============================================================

df["target_aqi"] = df.groupby("city")["aqi"].shift(-1)

df = df.dropna(
    subset=["target_aqi"]
).reset_index(drop=True)

print("\nDataset Shape After Creating Target:")
print(df.shape)


# ============================================================
# 4. SELECT FEATURES
# ============================================================

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


# ============================================================
# 5. CATEGORICAL AND NUMERICAL FEATURES
# ============================================================

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


# ============================================================
# 6. PREPROCESSING
# ============================================================

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


# ============================================================
# 7. TRAIN-TEST SPLIT
# ============================================================

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


# ============================================================
# 8. DEFINE THREE ML MODELS
# ============================================================

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


# ============================================================
# 9. TRAIN MODELS
# ============================================================

predictions = {}

trained_models = {}


for name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(
        X_train,
        y_train
    )

    # Save trained pipeline
    trained_models[name] = pipeline

    # Make predictions
    predictions[name] = pipeline.predict(X_test)

    print(f"\n{name} training completed.")

    print(
        "Number of predictions:",
        len(predictions[name])
    )


# ============================================================
# 10. MODEL EVALUATION
# ============================================================

print("\n")
print("=" * 60)
print("MODEL EVALUATION")
print("=" * 60)


results = []


for name, y_pred in predictions.items():

    # MAE
    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    # RMSE
    rmse = mean_squared_error(
        y_test,
        y_pred
    ) ** 0.5

    # R2
    r2 = r2_score(
        y_test,
        y_pred
    )

    results.append({

        "Model": name,

        "MAE": mae,

        "RMSE": rmse,

        "R2": r2

    })


# ============================================================
# 11. CREATE COMPARISON TABLE
# ============================================================

results_df = pd.DataFrame(results)


print("\nModel Comparison:")

print(
    results_df.round(3)
)


# Save comparison table

os.makedirs(
    "data",
    exist_ok=True
)


results_df.to_csv(
    "data/model_comparison.csv",
    index=False
)


print("\nModel comparison saved at:")

print(
    "data/model_comparison.csv"
)


# ============================================================
# 12. SELECT FINAL MODEL
# ============================================================

# Lower RMSE is better

best_model_name = results_df.loc[
    results_df["RMSE"].idxmin(),
    "Model"
]


best_model = trained_models[
    best_model_name
]


print("\n")
print("=" * 60)
print("FINAL MODEL")
print("=" * 60)


print(
    "Selected Model:",
    best_model_name
)


print(
    "Reason: Lowest RMSE among the three models."
)


# ============================================================
# 13. SAVE FINAL MODEL USING JOBLIB
# ============================================================

os.makedirs(
    "models",
    exist_ok=True
)


joblib.dump(
    best_model,
    "models/final_aqi_model.joblib"
)


print("\nFinal model saved at:")

print(
    "models/final_aqi_model.joblib"
)


# ============================================================
# 14. ACTUAL VS PREDICTED AQI GRAPH
# ============================================================

best_predictions = predictions[
    best_model_name
]


plt.figure(
    figsize=(8, 6)
)


plt.scatter(
    y_test,
    best_predictions,
    alpha=0.5
)


# Perfect prediction reference line

min_value = min(
    y_test.min(),
    best_predictions.min()
)


max_value = max(
    y_test.max(),
    best_predictions.max()
)


plt.plot(
    [min_value, max_value],
    [min_value, max_value],
    linestyle="--"
)


plt.xlabel(
    "Actual AQI"
)

plt.ylabel(
    "Predicted AQI"
)


plt.title(
    f"Actual vs Predicted AQI - {best_model_name}"
)


plt.tight_layout()


plt.savefig(
    "data/actual_vs_predicted_aqi.png",
    dpi=300
)


plt.show()


print("\nActual vs Predicted graph saved at:")

print(
    "data/actual_vs_predicted_aqi.png"
)


# ============================================================
# 15. COMPLETION MESSAGE
# ============================================================

print("\n")
print("=" * 60)
print("PART 2 ML EVALUATION COMPLETED")
print("=" * 60)