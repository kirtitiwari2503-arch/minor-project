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

# Display the number of rows and columns
cat("Dataset Dimensions:\n")
print(dim(df))

# Display the column names
cat("\nColumn Names:\n")
print(names(df))

# =========================================
# 2. AQI SUMMARY STATISTICS
# =========================================

# Display summary statistics of AQI
cat("\nAQI Summary Statistics:\n")
print(summary(df$aqi))

# =========================================
# 3. INDIVIDUAL AQI STATISTICS
# =========================================

# Calculate the mean AQI
cat("\nMean AQI:\n")
print(mean(df$aqi))

# Calculate the median AQI
cat("\nMedian AQI:\n")
print(median(df$aqi))

# Find the minimum AQI
cat("\nMinimum AQI:\n")
print(min(df$aqi))

# Find the maximum AQI
cat("\nMaximum AQI:\n")
print(max(df$aqi))

# Calculate the standard deviation
cat("\nStandard Deviation of AQI:\n")
print(sd(df$aqi))

# Display the AQI quartiles
cat("\nAQI Quartiles:\n")
print(quantile(df$aqi))

# =========================================
# 4. AQI HISTOGRAM
# =========================================

# Create a histogram to show AQI distribution
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

# Create a boxplot to show the spread of AQI values
boxplot(
  df$aqi,
  main = "Boxplot of AQI",
  ylab = "AQI"
)

# =========================================
# 6. AQI CATEGORY ANALYSIS
# =========================================

# Display AQI category counts
cat("\nAQI Category Counts:\n")

# Count the records in each AQI category
category_counts <- table(df$aqi_category)

# Display the category counts
print(category_counts)

# =========================================
# 7. AQI CATEGORY BAR CHART
# =========================================

# Create a bar chart for AQI categories
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

# Display the first few rows of daily AQI data
cat("\nDaily AQI Trend Data:\n")

print(head(daily_aqi))

# Plot AQI trend over time
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

# Display the final AQI analysis summary
cat("\n=========================================\n")
cat("FINAL AQI ANALYSIS SUMMARY\n")
cat("=========================================\n")

# Display the mean AQI
cat("Mean AQI:", mean(df$aqi), "\n")

# Display the median AQI
cat("Median AQI:", median(df$aqi), "\n")

# Display the minimum AQI
cat("Minimum AQI:", min(df$aqi), "\n")

# Display the maximum AQI
cat("Maximum AQI:", max(df$aqi), "\n")

# Display the standard deviation
cat("Standard Deviation:", sd(df$aqi), "\n")

# Display the first quartile
cat("Q1:", quantile(df$aqi, 0.25), "\n")

# Display the third quartile
cat("Q3:", quantile(df$aqi, 0.75), "\n")