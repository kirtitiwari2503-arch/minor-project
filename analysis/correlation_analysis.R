# ==========================================
# NABHA - Correlation & Relationship Analysis
# Team Member: Jeesha
# ==========================================

library(ggplot2)

# Load cleaned dataset
df <- read.csv("data/air_quality_cleaned.csv")

cat("Dataset loaded successfully!\n")
cat("Rows:", nrow(df), "\n")
cat("Columns:", ncol(df), "\n")

# Select AQI and pollutant variables
variables <- c("aqi", "pm25", "pm10", "no2", "so2", "co", "o3")

cor_data <- df[, variables]

# ------------------------------------------
# Correlation Matrix
# ------------------------------------------

cor_matrix <- cor(cor_data, use = "complete.obs")

cat("\n==========================================\n")
cat("CORRELATION MATRIX\n")
cat("==========================================\n")

print(round(cor_matrix, 3))

# Save correlation matrix
write.csv(
  round(cor_matrix, 3),
  "data/correlation_matrix.csv"
)

# ------------------------------------------
# Correlation of AQI with each pollutant
# ------------------------------------------

aqi_correlations <- cor_matrix["aqi", ]

cat("\n==========================================\n")
cat("CORRELATION WITH AQI\n")
cat("==========================================\n")

print(round(aqi_correlations, 3))

# ------------------------------------------
# Scatter Plot: AQI vs PM2.5
# ------------------------------------------

p1 <- ggplot(df, aes(x = pm25, y = aqi)) +
  geom_point(alpha = 0.4) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "AQI vs PM2.5",
    x = "PM2.5",
    y = "AQI"
  )

print(p1)

ggsave(
  "data/aqi_vs_pm25.png",
  plot = p1,
  width = 7,
  height = 5
)

# ------------------------------------------
# Scatter Plot: AQI vs PM10
# ------------------------------------------

p2 <- ggplot(df, aes(x = pm10, y = aqi)) +
  geom_point(alpha = 0.4) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "AQI vs PM10",
    x = "PM10",
    y = "AQI"
  )

print(p2)

ggsave(
  "data/aqi_vs_pm10.png",
  plot = p2,
  width = 7,
  height = 5
)

# ------------------------------------------
# Scatter Plot: AQI vs NO2
# ------------------------------------------

p3 <- ggplot(df, aes(x = no2, y = aqi)) +
  geom_point(alpha = 0.4) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "AQI vs NO2",
    x = "NO2",
    y = "AQI"
  )

print(p3)

ggsave(
  "data/aqi_vs_no2.png",
  plot = p3,
  width = 7,
  height = 5
)

cat("\n==========================================\n")
cat("Correlation analysis completed successfully!\n")
cat("Correlation matrix and scatter plots saved.\n")
cat("==========================================\n")