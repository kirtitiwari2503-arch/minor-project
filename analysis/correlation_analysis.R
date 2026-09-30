# ==========================================
# NABHA - Correlation & Relationship Analysis
# Team Member: Jeesha
# ==========================================

# Load ggplot2 for creating the scatter plots
library(ggplot2)

# Load the cleaned air quality dataset from the data folder
df <- read.csv("data/air_quality_cleaned.csv")

# Display a message to confirm that the dataset was loaded
cat("Dataset loaded successfully!\n")

# Display the total number of rows in the dataset
cat("Rows:", nrow(df), "\n")

# Display the total number of columns in the dataset
cat("Columns:", ncol(df), "\n")

# Select AQI and pollutant variables for correlation analysis
variables <- c("aqi", "pm25", "pm10", "no2", "so2", "co", "o3")

# Create a new dataset containing only the selected variables
cor_data <- df[, variables]

# ------------------------------------------
# Correlation Matrix
# ------------------------------------------

# Calculate the correlation between all selected variables
# complete.obs uses only observations with complete values
cor_matrix <- cor(cor_data, use = "complete.obs")

# Display a heading for the correlation matrix
cat("\n==========================================\n")
cat("CORRELATION MATRIX\n")
cat("==========================================\n")

# Display the correlation values rounded to three decimal places
print(round(cor_matrix, 3))

# Save the correlation matrix as a CSV file
write.csv(
  round(cor_matrix, 3),
  "data/correlation_matrix.csv"
)

# ------------------------------------------
# Correlation of AQI with each pollutant
# ------------------------------------------

# Extract the correlation values between AQI and all selected variables
aqi_correlations <- cor_matrix["aqi", ]

# Display a heading for the AQI correlation results
cat("\n==========================================\n")
cat("CORRELATION WITH AQI\n")
cat("==========================================\n")

# Display the AQI correlation values rounded to three decimal places
print(round(aqi_correlations, 3))

# ------------------------------------------
# Scatter Plot: AQI vs PM2.5
# ------------------------------------------

# Create a scatter plot to show the relationship between PM2.5 and AQI
p1 <- ggplot(df, aes(x = pm25, y = aqi)) +
  
  # Add the individual observations to the plot
  geom_point(alpha = 0.4) +
  
  # Add a linear trend line to show the overall relationship
  geom_smooth(method = "lm", se = FALSE) +
  
  # Add the title and labels for the axes
  labs(
    title = "AQI vs PM2.5",
    x = "PM2.5",
    y = "AQI"
  )

# Display the PM2.5 versus AQI plot
print(p1)

# Save the plot as a PNG image
ggsave(
  "data/aqi_vs_pm25.png",
  plot = p1,
  width = 7,
  height = 5
)

# ------------------------------------------
# Scatter Plot: AQI vs PM10
# ------------------------------------------

# Create a scatter plot to show the relationship between PM10 and AQI
p2 <- ggplot(df, aes(x = pm10, y = aqi)) +
  
  # Add the individual observations to the plot
  geom_point(alpha = 0.4) +
  
  # Add a linear trend line to show the overall relationship
  geom_smooth(method = "lm", se = FALSE) +
  
  # Add the title and labels for the axes
  labs(
    title = "AQI vs PM10",
    x = "PM10",
    y = "AQI"
  )

# Display the PM10 versus AQI plot
print(p2)

# Save the plot as a PNG image
ggsave(
  "data/aqi_vs_pm10.png",
  plot = p2,
  width = 7,
  height = 5
)

# ------------------------------------------
# Scatter Plot: AQI vs NO2
# ------------------------------------------

# Create a scatter plot to show the relationship between NO2 and AQI
p3 <- ggplot(df, aes(x = no2, y = aqi)) +
  
  # Add the individual observations to the plot
  geom_point(alpha = 0.4) +
  
  # Add a linear trend line to show the overall relationship
  geom_smooth(method = "lm", se = FALSE) +
  
  # Add the title and labels for the axes
  labs(
    title = "AQI vs NO2",
    x = "NO2",
    y = "AQI"
  )

# Display the NO2 versus AQI plot
print(p3)

# Save the plot as a PNG image
ggsave(
  "data/aqi_vs_no2.png",
  plot = p3,
  width = 7,
  height = 5
)

# Display a message after completing the correlation analysis
cat("\n==========================================\n")
cat("Correlation analysis completed successfully!\n")
cat("Correlation matrix and scatter plots saved.\n")
cat("==========================================\n")
