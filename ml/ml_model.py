import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Load feature-engineered dataset
df = pd.read_csv("data/air_quality_feature_engineered.csv")

print("Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Sort by date and city
df = df.sort_values(
    ["date", "city"]
).reset_index(drop=True)


# Define features and target
features = [
    "city",
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
    "aqi_rolling7"
]

target = "target_aqi"

X = df[features]
y = df[target]


# Create chronological train-test split
unique_dates = sorted(
    df["date"].unique()
)

split_index = int(
    len(unique_dates) * 0.8
)

split_date = unique_dates[split_index]

train_mask = df["date"] < split_date
test_mask = df["date"] >= split_date

X_train = X[train_mask]
X_test = X[test_mask]

y_train = y[train_mask]
y_test = y[test_mask]


print("\nTraining Data Shape:")
print(X_train.shape)

print("\nTesting Data Shape:")
print(X_test.shape)

print("\nTraining Date Range:")
print(df.loc[train_mask, "date"].min())
print("to")
print(df.loc[train_mask, "date"].max())

print("\nTesting Date Range:")
print(df.loc[test_mask, "date"].min())
print("to")
print(df.loc[test_mask, "date"].max())


# Define categorical and numerical features
categorical_features = [
    "city"
]

numerical_features = [
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
    "aqi_rolling7"
]


# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "city",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numbers",
            "passthrough",
            numerical_features
        )
    ]
)


# Define models
models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=100,
        random_state=42
    )
}


results = []
predictions = {}


# Calculate naive baseline
baseline_predictions = X_test["aqi_lag1"]

baseline_mae = mean_absolute_error(
    y_test,
    baseline_predictions
)

baseline_rmse = mean_squared_error(
    y_test,
    baseline_predictions
) ** 0.5

baseline_r2 = r2_score(
    y_test,
    baseline_predictions
)

print("\nNaive Baseline:")
print(f"MAE: {baseline_mae:.3f}")
print(f"RMSE: {baseline_rmse:.3f}")
print(f"R2: {baseline_r2:.3f}")


# Train and evaluate models
for model_name, model in models.items():

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    pipeline.fit(
        X_train,
        y_train
    )

    y_pred = pipeline.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    rmse = mean_squared_error(
        y_test,
        y_pred
    ) ** 0.5

    r2 = r2_score(
        y_test,
        y_pred
    )

    results.append(
        {
            "Model": model_name,
            "MAE": round(mae, 3),
            "RMSE": round(rmse, 3),
            "R2": round(r2, 3)
        }
    )

    predictions[model_name] = y_pred

    print(
        f"\n{model_name} training completed."
    )

    print(
        f"MAE: {mae:.3f}"
    )

    print(
        f"RMSE: {rmse:.3f}"
    )

    print(
        f"R2: {r2:.3f}"
    )


# Model comparison
results_df = pd.DataFrame(
    results
)

print("\nModel Comparison:")
print(results_df)


# Save model comparison
results_df.to_csv(
    "data/model_comparison.csv",
    index=False
)

print("\nModel comparison saved at:")
print(
    "data/model_comparison.csv"
)


# Select model with lowest RMSE
best_model_name = results_df.loc[
    results_df["RMSE"].idxmin(),
    "Model"
]

print("\nSelected Model:")
print(best_model_name)

print(
    "Reason: Lowest RMSE among the three models."
)


# Check whether selected model beats baseline
best_rmse = results_df.loc[
    results_df["Model"] == best_model_name,
    "RMSE"
].iloc[0]

print("\nBaseline RMSE:")
print(
    round(baseline_rmse, 3)
)

print("\nBest Model RMSE:")
print(
    round(best_rmse, 3)
)

if best_rmse < baseline_rmse:

    print(
        "\nThe ML model performs better than "
        "the naive baseline."
    )

else:

    print(
        "\nThe ML model does not improve "
        "over the naive baseline."
    )


# Train selected model again
final_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            models[best_model_name]
        )
    ]
)

final_model.fit(
    X_train,
    y_train
)


# Check feature importance
model = final_model.named_steps["model"]

preprocessor_fitted = (
    final_model.named_steps["preprocessor"]
)

feature_names = (
    preprocessor_fitted
    .get_feature_names_out()
)

importance = model.feature_importances_

feature_importance = pd.DataFrame(
    {
        "Feature": feature_names,
        "Importance": importance
    }
)

feature_importance = (
    feature_importance
    .sort_values(
        "Importance",
        ascending=False
    )
)

print("\nFeature Importance:")

print(
    feature_importance
    .head(15)
    .to_string(index=False)
)


# Save feature importance
feature_importance.to_csv(
    "data/feature_importance.csv",
    index=False
)

print("\nFeature importance saved at:")
print(
    "data/feature_importance.csv"
)


# Save final model
joblib.dump(
    final_model,
    "models/final_aqi_model.joblib"
)

print("\nFinal model saved at:")
print(
    "models/final_aqi_model.joblib"
)


# Create actual vs predicted graph
best_predictions = (
    predictions[best_model_name]
)

plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    y_test,
    best_predictions,
    alpha=0.5
)

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
    f"Actual vs Predicted AQI - "
    f"{best_model_name}"
)

plt.tight_layout()

plt.savefig(
    "data/actual_vs_predicted_aqi.png"
)

plt.close()

print(
    "\nActual vs Predicted graph saved at:"
)

print(
    "data/actual_vs_predicted_aqi.png"
)


print(
    "\nML training and evaluation completed."
)