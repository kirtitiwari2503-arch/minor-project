# =========================================
# AQI ANALYSIS
# =========================================

# Load cleaned dataset
df <- read.csv("data/air_quality_cleaned.csv")

# Convert date column to Date format
df$date <- as.Date(df$date)

# =========================================
# 1. BASIC DATA INFORMATION
# =========================================

cat("Dataset Dimensions:\n")
print(dim(df))

cat("\nColumn Names:\n")
print(names(df))

# =========================================
# 2. AQI SUMMARY STATISTICS
# =========================================

cat("\nAQI Summary Statistics:\n")
print(summary(df$aqi))

# =========================================
# 3. INDIVIDUAL AQI STATISTICS
# =========================================

cat("\nMean AQI:\n")
print(mean(df$aqi))

cat("\nMedian AQI:\n")
print(median(df$aqi))

cat("\nMinimum AQI:\n")
print(min(df$aqi))

cat("\nMaximum AQI:\n")
print(max(df$aqi))

cat("\nStandard Deviation of AQI:\n")
print(sd(df$aqi))

cat("\nAQI Quartiles:\n")
print(quantile(df$aqi))

# =========================================
# 4. AQI HISTOGRAM
# =========================================

hist(
  df$aqi,
  main = "Distribution of AQI",
  xlab = "AQI",
  ylab = "Frequency",
  breaks = 20
)

# =========================================
# 5. AQI BOXPLOT
# =========================================

boxplot(
  df$aqi,
  main = "Boxplot of AQI",
  ylab = "AQI"
)

# =========================================
# 6. AQI CATEGORY ANALYSIS
# =========================================

cat("\nAQI Category Counts:\n")

category_counts <- table(df$aqi_category)

print(category_counts)

# =========================================
# 7. AQI CATEGORY BAR CHART
# =========================================

barplot(
  category_counts,
  main = "AQI Category Distribution",
  xlab = "AQI Category",
  ylab = "Frequency",
  las = 2
)

# =========================================
# 8. AQI TREND OVER TIME
# =========================================

# Calculate average AQI for each date
daily_aqi <- aggregate(
  aqi ~ date,
  data = df,
  FUN = mean
)

cat("\nDaily AQI Trend Data:\n")

print(head(daily_aqi))

# Plot AQI trend
plot(
  daily_aqi$date,
  daily_aqi$aqi,
  type = "l",
  main = "Average AQI Trend Over Time",
  xlab = "Date",
  ylab = "Average AQI"
)

# =========================================
# 9. FINAL AQI ANALYSIS FINDINGS
# =========================================

cat("\n=========================================\n")
cat("FINAL AQI ANALYSIS SUMMARY\n")
cat("=========================================\n")

cat("Mean AQI:", mean(df$aqi), "\n")

cat("Median AQI:", median(df$aqi), "\n")

cat("Minimum AQI:", min(df$aqi), "\n")

cat("Maximum AQI:", max(df$aqi), "\n")

cat("Standard Deviation:", sd(df$aqi), "\n")

cat("Q1:", quantile(df$aqi, 0.25), "\n")

cat("Q3:", quantile(df$aqi, 0.75), "\n")