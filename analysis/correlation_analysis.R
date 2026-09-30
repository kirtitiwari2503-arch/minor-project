# ==========================================
# NABHA - Correlation & Relationship Analysis
# Team Member: Jeesha
# ==========================================

# Load ggplot2 package
library(ggplot2)

# Load the cleaned dataset
df <- read.csv("data/air_quality_cleaned.csv")

# Display dataset information
cat("Dataset loaded successfully!\n")
cat("Rows:", nrow(df), "\n")
cat("Columns:", ncol(df), "\n")

# Select AQI and pollutant variables
variables <- c("aqi", "pm25", "pm10", "no2", "so2", "co", "o3")

# Create data for correlation analysis
cor_data <- df[, variables]

# ------------------------------------------
# Correlation Matrix
# ------------------------------------------

# Calculate the correlation matrix
cor_matrix <- cor(cor_data, use = "complete.obs")

# Display the correlation matrix
cat("\n==========================================\n")
cat("CORRELATION MATRIX\n")
cat("==========================================\n")

# Print correlation values up to three decimal places
print(round(cor_matrix, 3))

# Save the correlation matrix
write.csv(
  round(cor_matrix, 3),
  "data/correlation_matrix.csv"
)

# ------------------------------------------
# Correlation of AQI with each pollutant
# ------------------------------------------

# Get the correlation values related to AQI
aqi_correlations <- cor_matrix["aqi", ]

# Display AQI correlation values
cat("\n==========================================\n")
cat("CORRELATION WITH AQI\n")
cat("==========================================\n")

# Print the correlation values
print(round(aqi_correlations, 3))

# ------------------------------------------
# Scatter Plot: AQI vs PM2.5
# ------------------------------------------

# Create a scatter plot for AQI and PM2.5
p1 <- ggplot(df, aes(x = pm25, y = aqi)) +
  
  # Add data points
  geom_point(alpha = 0.4) +
  
  # Add a linear trend line
  geom_smooth(method = "lm", se = FALSE) +
  
  # Add plot title and axis labels
  labs(
    title = "AQI vs PM2.5",
    x = "PM2.5",
    y = "AQI"
  )

# Display the plot
print(p1)

# Save the plot
ggsave(
  "data/aqi_vs_pm25.png",
  plot = p1,
  width = 7,
  height = 5
)

# ------------------------------------------
# Scatter Plot: AQI vs PM10
# ------------------------------------------

# Create a scatter plot for AQI and PM10
p2 <- ggplot(df, aes(x = pm10, y = aqi)) +
  
  # Add data points
  geom_point(alpha = 0.4) +
  
  # Add a linear trend line
  geom_smooth(method = "lm", se = FALSE) +
  
  # Add plot title and axis labels
  labs(
    title = "AQI vs PM10",
    x = "PM10",
    y = "AQI"
  )

# Display the plot
print(p2)

# Save the plot
ggsave(
  "data/aqi_vs_pm10.png",
  plot = p2,
  width = 7,
  height = 5
)

# ------------------------------------------
# Scatter Plot: AQI vs NO2
# ------------------------------------------

# Create a scatter plot for AQI and NO2
p3 <- ggplot(df, aes(x = no2, y = aqi)) +
  
  # Add data points
  geom_point(alpha = 0.4) +
  
  # Add a linear trend line
  geom_smooth(method = "lm", se = FALSE) +
  
  # Add plot title and axis labels
  labs(
    title = "AQI vs NO2",
    x = "NO2",
    y = "AQI"
  )

# Display the plot
print(p3)

# Save the plot
ggsave(
  "data/aqi_vs_no2.png",
  plot = p3,
  width = 7,
  height = 5
)

# Display completion message
cat("\n==========================================\n")
cat("Correlation analysis completed successfully!\n")
cat("Correlation matrix and scatter plots saved.\n")
cat("==========================================\n")