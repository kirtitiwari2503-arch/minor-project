import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Load the feature-engineered dataset
df = pd.read_csv("data/air_quality_feature_engineered.csv")

# Display the dataset shape
print("Dataset Shape:")
print(df.shape)

# Display all dataset columns
print("\nColumns:")
print(df.columns.tolist())


# Convert the date column to datetime format
df["date"] = pd.to_datetime(df["date"])

# Sort the data by date and city
df = df.sort_values(
    ["date", "city"]
).reset_index(drop=True)


# Define input features and prediction target
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

# Separate the features and target
X = df[features]
y = df[target]


# Get the unique dates for chronological splitting
unique_dates = sorted(
    df["date"].unique()
)

# Use 80% of the dates for training
split_index = int(
    len(unique_dates) * 0.8
)

# Get the date where the train-test split starts
split_date = unique_dates[split_index]

# Create masks for training and testing data
train_mask = df["date"] < split_date
test_mask = df["date"] >= split_date

# Create the training and testing feature sets
X_train = X[train_mask]
X_test = X[test_mask]

# Create the training and testing target sets
y_train = y[train_mask]
y_test = y[test_mask]


# Display the training and testing dataset sizes
print("\nTraining Data Shape:")
print(X_train.shape)

print("\nTesting Data Shape:")
print(X_test.shape)

# Display the training date range
print("\nTraining Date Range:")
print(df.loc[train_mask, "date"].min())
print("to")
print(df.loc[train_mask, "date"].max())

# Display the testing date range
print("\nTesting Date Range:")
print(df.loc[test_mask, "date"].min())
print("to")
print(df.loc[test_mask, "date"].max())


# Define the categorical features
categorical_features = [
    "city"
]

# Define the numerical features
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


# Create preprocessing steps for categorical and numerical features
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


# Define the regression models
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


# Store model evaluation results
results = []

# Store predictions from each model
predictions = {}


# Use previous-day AQI as the naive baseline
baseline_predictions = X_test["aqi_lag1"]

# Calculate baseline MAE
baseline_mae = mean_absolute_error(
    y_test,
    baseline_predictions
)

# Calculate baseline RMSE
baseline_rmse = mean_squared_error(
    y_test,
    baseline_predictions
) ** 0.5

# Calculate baseline R2 score
baseline_r2 = r2_score(
    y_test,
    baseline_predictions
)

# Display baseline performance
print("\nNaive Baseline:")
print(f"MAE: {baseline_mae:.3f}")
print(f"RMSE: {baseline_rmse:.3f}")
print(f"R2: {baseline_r2:.3f}")


# Train and evaluate each regression model
for model_name, model in models.items():

    # Create a pipeline with preprocessing and the model
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

    # Train the model using the training data
    pipeline.fit(
        X_train,
        y_train
    )

    # Generate predictions for the test data
    y_pred = pipeline.predict(
        X_test
    )

    # Calculate Mean Absolute Error
    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    # Calculate Root Mean Square Error
    rmse = mean_squared_error(
        y_test,
        y_pred
    ) ** 0.5

    # Calculate R2 score
    r2 = r2_score(
        y_test,
        y_pred
    )

    # Store the model evaluation results
    results.append(
        {
            "Model": model_name,
            "MAE": round(mae, 3),
            "RMSE": round(rmse, 3),
            "R2": round(r2, 3)
        }
    )

    # Store the predictions for later use
    predictions[model_name] = y_pred

    # Display the model training status
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


# Create a DataFrame for model comparison
results_df = pd.DataFrame(
    results
)

# Display the model comparison results
print("\nModel Comparison:")
print(results_df)


# Save the model comparison results
results_df.to_csv(
    "data/model_comparison.csv",
    index=False
)

print("\nModel comparison saved at:")
print(
    "data/model_comparison.csv"
)


# Select the model with the lowest RMSE
best_model_name = results_df.loc[
    results_df["RMSE"].idxmin(),
    "Model"
]

# Display the selected model
print("\nSelected Model:")
print(best_model_name)

print(
    "Reason: Lowest RMSE among the three models."
)


# Get the RMSE of the selected model
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

# Compare the selected model with the naive baseline
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


# Train the selected model again for final use
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

# Fit the final model on the training data
final_model.fit(
    X_train,
    y_train
)


# Get the trained model from the pipeline
model = final_model.named_steps["model"]

# Get the fitted preprocessing step
preprocessor_fitted = (
    final_model.named_steps["preprocessor"]
)

# Get the names of the processed features
feature_names = (
    preprocessor_fitted
    .get_feature_names_out()
)

# Get the importance of each feature
importance = model.feature_importances_

# Create a DataFrame containing feature importance
feature_importance = pd.DataFrame(
    {
        "Feature": feature_names,
        "Importance": importance
    }
)

# Sort features from highest to lowest importance
feature_importance = (
    feature_importance
    .sort_values(
        "Importance",
        ascending=False
    )
)

# Display the top feature importance values
print("\nFeature Importance:")

print(
    feature_importance
    .head(15)
    .to_string(index=False)
)


# Save feature importance results
feature_importance.to_csv(
    "data/feature_importance.csv",
    index=False
)

print("\nFeature importance saved at:")
print(
    "data/feature_importance.csv"
)


# Save the trained final model
joblib.dump(
    final_model,
    "models/final_aqi_model.joblib"
)

print("\nFinal model saved at:")
print(
    "models/final_aqi_model.joblib"
)


# Get predictions from the selected model
best_predictions = (
    predictions[best_model_name]
)

# Create the actual versus predicted AQI plot
plt.figure(
    figsize=(8, 6)
)

# Plot actual AQI against predicted AQI
plt.scatter(
    y_test,
    best_predictions,
    alpha=0.5
)

# Find the minimum AQI value for the reference line
min_value = min(
    y_test.min(),
    best_predictions.min()
)

# Find the maximum AQI value for the reference line
max_value = max(
    y_test.max(),
    best_predictions.max()
)

# Add the ideal prediction reference line
plt.plot(
    [min_value, max_value],
    [min_value, max_value],
    linestyle="--"
)

# Set the x-axis label
plt.xlabel(
    "Actual AQI"
)

# Set the y-axis label
plt.ylabel(
    "Predicted AQI"
)

# Set the plot title
plt.title(
    f"Actual vs Predicted AQI - "
    f"{best_model_name}"
)

# Adjust the plot layout
plt.tight_layout()

# Save the actual versus predicted graph
plt.savefig(
    "data/actual_vs_predicted_aqi.png"
)

# Close the plot
plt.close()

print(
    "\nActual vs Predicted graph saved at:"
)

print(
    "data/actual_vs_predicted_aqi.png"
)


# Display the completion message
print(
    "\nML training and evaluation completed."
)