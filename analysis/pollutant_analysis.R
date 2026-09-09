# ==========================================
# =========================================
library(ggplot2)
library(dplyr)

# ------------------------------------------
# 1. Load cleaned dataset
# ------------------------------------------

df <- read.csv("data/air_quality_cleaned.csv")

cat("Dataset loaded successfully!\n")
cat("Rows:", nrow(df), "\n")
cat("Columns:", ncol(df), "\n")


# ------------------------------------------
# 2. Select pollutants
# ------------------------------------------

pollutants <- c("pm25", "pm10", "no2", "so2", "co", "o3")


# ------------------------------------------
# 3. Basic Statistics
# ------------------------------------------

cat("\n==========================================\n")
cat("POLLUTANT STATISTICS\n")
cat("==========================================\n")

for (col in pollutants) {

  cat("\n------------------------------------------\n")
  cat("Pollutant:", toupper(col), "\n")

  cat("Mean:", mean(df[[col]], na.rm = TRUE), "\n")
  cat("Median:", median(df[[col]], na.rm = TRUE), "\n")
  cat("Minimum:", min(df[[col]], na.rm = TRUE), "\n")
  cat("Maximum:", max(df[[col]], na.rm = TRUE), "\n")
  cat("Standard Deviation:", sd(df[[col]], na.rm = TRUE), "\n")
}


# ------------------------------------------
# 4. Histograms
# ------------------------------------------

for (col in pollutants) {

  p <- ggplot(df, aes(x = .data[[col]])) +
    geom_histogram(bins = 30) +
    labs(
      title = paste("Distribution of", toupper(col)),
      x = toupper(col),
      y = "Frequency"
    ) +
    theme_minimal()

  print(p)
}


# ------------------------------------------
# 5. Boxplots
# ------------------------------------------

for (col in pollutants) {

  p <- ggplot(df, aes(y = .data[[col]])) +
    geom_boxplot() +
    labs(
      title = paste("Boxplot of", toupper(col)),
      y = toupper(col)
    ) +
    theme_minimal()

  print(p)
}


# ------------------------------------------
# 6. City-wise pollutant mean
# ------------------------------------------

city_summary <- df %>%
  group_by(city) %>%
  summarise(
    PM25 = mean(pm25, na.rm = TRUE),
    PM10 = mean(pm10, na.rm = TRUE),
    NO2 = mean(no2, na.rm = TRUE),
    SO2 = mean(so2, na.rm = TRUE),
    CO = mean(co, na.rm = TRUE),
    O3 = mean(o3, na.rm = TRUE)
  )

cat("\n==========================================\n")
cat("CITY-WISE POLLUTANT MEAN\n")
cat("==========================================\n")

print(city_summary)


# ------------------------------------------
# 7. PM2.5 comparison between cities
# ------------------------------------------

ggplot(df, aes(x = city, y = pm25)) +
  geom_boxplot() +
  labs(
    title = "PM2.5 Levels Across Cities",
    x = "City",
    y = "PM2.5"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1)
  )


# ------------------------------------------
# 8. PM10 comparison between cities
# ------------------------------------------

ggplot(df, aes(x = city, y = pm10)) +
  geom_boxplot() +
  labs(
    title = "PM10 Levels Across Cities",
    x = "City",
    y = "PM10"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1)
  )


# ------------------------------------------
# 9. Save city-wise summary
# ------------------------------------------

write.csv(
  city_summary,
  "data/city_wise_pollutant_summary.csv",
  row.names = FALSE
)

cat("\n==========================================\n")
cat("Pollutant analysis completed successfully!\n")
cat("City-wise summary saved.\n")
cat("==========================================\n")