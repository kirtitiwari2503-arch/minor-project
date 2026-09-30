"""
NABHA - Rule-Based Health Risk & Personalized Preventive Advisory

This is a project-defined preventive advisory system.
It is NOT a medically validated clinical risk score and does NOT diagnose disease.
"""

# Set project-defined thresholds for pollutant recommendations
PM25_HIGH = 60   # Project-defined recommendation threshold
PM10_HIGH = 100  # Project-defined recommendation threshold


# Calculate the base risk from the current AQI
def get_aqi_base_risk(aqi):
    # Assign a base risk value according to the AQI range
    if aqi <= 50:
        return 10
    elif aqi <= 100:
        return 25
    elif aqi <= 200:
        return 50
    elif aqi <= 300:
        return 70
    elif aqi <= 400:
        return 85
    else:
        return 100


# Calculate the risk modifier based on health condition
def get_health_modifier(health_condition):
    # Convert the health condition to lowercase for comparison
    condition = str(health_condition).strip().lower()
    
    # Add a higher modifier for asthma
    if condition == "asthma":
        return 15
    elif condition in {"heart disease", "heart disease/cardiovascular"}:
        return 15
    elif condition in {"other respiratory", "other respiratory condition"}:
        return 10
    return 0


# Calculate the risk modifier based on age
def get_age_modifier(age):
    # Add a modifier for project-defined sensitive age groups
    return 10 if age < 18 or age >= 60 else 0


# Calculate the risk modifier based on outdoor exposure
def get_outdoor_modifier(outdoor_exposure):
    # Convert the exposure level to lowercase for comparison
    exposure = str(outdoor_exposure).strip().lower()
    
    # Assign a modifier based on outdoor exposure
    if exposure == "high":
        return 10
    elif exposure == "moderate":
        return 5
    return 0


# Calculate the risk modifier based on profession exposure
def get_profession_modifier(profession_exposure):
    # Convert the profession exposure to lowercase
    profession = str(profession_exposure).strip().lower()
    
    # Assign a modifier based on work exposure
    if profession in {"mostly outdoor", "outdoor"}:
        return 10
    elif profession == "mixed":
        return 5
    return 0


# Calculate the modifier based on the predicted AQI
def get_predicted_aqi_modifier(current_aqi, predicted_aqi):
    # >20% increase gets +10 instead of adding both +5 and +10.
    if predicted_aqi <= current_aqi:
        return 0
    if current_aqi == 0:
        return 10

    # Calculate the percentage increase in predicted AQI
    percentage_increase = ((predicted_aqi - current_aqi) / current_aqi) * 100
    
    # Assign a higher modifier when the increase is greater than 20%
    if percentage_increase > 20:
        return 10
    return 5


# Calculate the overall project-defined health risk score
def calculate_risk_score(
    current_aqi,
    predicted_aqi,
    pm25,
    pm10,
    age,
    health_condition,
    outdoor_exposure,
    profession_exposure,
):
    # Calculate individual risk components
    base_risk = get_aqi_base_risk(current_aqi)
    health_modifier = get_health_modifier(health_condition)
    age_modifier = get_age_modifier(age)
    outdoor_modifier = get_outdoor_modifier(outdoor_exposure)
    profession_modifier = get_profession_modifier(profession_exposure)
    predicted_modifier = get_predicted_aqi_modifier(current_aqi, predicted_aqi)

    # Add all risk components together
    raw_score = (
        base_risk
        + health_modifier
        + age_modifier
        + outdoor_modifier
        + profession_modifier
        + predicted_modifier
    )

    # PM2.5/PM10 are used for recommendations, not score points,
    # because no pollutant score modifiers were specified.
    return min(raw_score, 100)


# Convert the numerical score into a risk level
def get_risk_level(score):
    # Assign a risk level according to the score range
    if score <= 24:
        return "Low"
    elif score <= 49:
        return "Moderate"
    elif score <= 74:
        return "High"
    return "Very High"


# Generate preventive recommendations based on user and air-quality data
def generate_recommendations(
    current_aqi,
    predicted_aqi,
    pm25,
    pm10,
    age,
    health_condition,
    outdoor_exposure,
    profession_exposure,
    risk_level,
):
    # Create an empty list to store recommendations
    recommendations = []

    # Convert the health condition to lowercase
    condition = str(health_condition).strip().lower()
    
    # Identify users belonging to the project-defined sensitive groups
    sensitive_user = (
        age < 18
        or age >= 60
        or condition in {
            "asthma",
            "heart disease",
            "heart disease/cardiovascular",
            "other respiratory",
            "other respiratory condition",
        }
    )

    # Generate a recommendation based on the current AQI
    if current_aqi <= 50:
        recommendations.append(
            "Air quality is relatively good; normal outdoor activities can continue."
        )
    elif current_aqi <= 100:
        recommendations.append(
            "Monitor air quality and reduce prolonged outdoor exposure if discomfort occurs."
        )
    elif current_aqi <= 200:
        recommendations.append(
            "Reduce prolonged outdoor exposure, especially during strenuous activity."
        )
    elif current_aqi <= 300:
        recommendations.append(
            "Reduce outdoor exposure and avoid prolonged or strenuous outdoor activity."
        )
    else:
        recommendations.append(
            "Avoid unnecessary outdoor exposure and follow local air-quality guidance."
        )

    # Add a recommendation when the predicted AQI is higher
    if predicted_aqi > current_aqi:
        recommendations.append(
            "Predicted AQI is higher than the current AQI; plan outdoor activities accordingly."
        )

    # Add advice for moderate or high outdoor exposure
    if str(outdoor_exposure).strip().lower() in {"moderate", "high"}:
        recommendations.append(
            "Consider reducing the duration of outdoor exposure during higher pollution periods."
        )

    # Add advice for outdoor or mixed professions
    if str(profession_exposure).strip().lower() in {
        "mixed", "mostly outdoor", "outdoor"
    }:
        recommendations.append(
            "If outdoor work is unavoidable, take appropriate exposure-reduction precautions and monitor AQI."
        )

    # Add extra precautions for sensitive users during high pollution
    if sensitive_user and current_aqi > 100:
        recommendations.append(
            "Because you are in a project-defined sensitive group, take extra precautions during high pollution."
        )

    # Check whether PM2.5 is above the project-defined threshold
    if pm25 > PM25_HIGH:
        recommendations.append(
            f"PM2.5 is elevated (>{PM25_HIGH}). Reduce prolonged exposure to particulate pollution."
        )

    # Check whether PM10 is above the project-defined threshold
    if pm10 > PM10_HIGH:
        recommendations.append(
            f"PM10 is elevated (>{PM10_HIGH}). Avoid dusty or heavily polluted outdoor areas."
        )

    # Add advice for high or very high overall risk
    if risk_level in {"High", "Very High"}:
        recommendations.append(
            "Overall project-defined risk is elevated; consider limiting unnecessary outdoor exposure."
        )

    # Return the complete list of recommendations
    return recommendations


# Assess the overall health risk and generate recommendations
def assess_health_risk(
    current_aqi,
    predicted_aqi,
    pm25,
    pm10,
    age,
    health_condition,
    outdoor_exposure,
    profession_exposure,
):
    # Calculate the numerical risk score
    score = calculate_risk_score(
        current_aqi,
        predicted_aqi,
        pm25,
        pm10,
        age,
        health_condition,
        outdoor_exposure,
        profession_exposure,
    )
    
    # Convert the score into a risk level
    level = get_risk_level(score)
    
    # Generate recommendations using the calculated risk level
    recommendations = generate_recommendations(
        current_aqi,
        predicted_aqi,
        pm25,
        pm10,
        age,
        health_condition,
        outdoor_exposure,
        profession_exposure,
        level,
    )

    # Return the risk score, level and recommendations
    return {
        "risk_score": score,
        "risk_level": level,
        "recommendations": recommendations,
    }


# Run test cases when this file is executed directly
if __name__ == "__main__":
    # Test Case 1
    result1 = assess_health_risk(
        current_aqi=80,
        predicted_aqi=90,
        pm25=35,
        pm10=70,
        age=25,
        health_condition="None",
        outdoor_exposure="Low",
        profession_exposure="Mostly indoor",
    )

    # Test Case 2
    result2 = assess_health_risk(
        current_aqi=220,
        predicted_aqi=280,
        pm25=85,
        pm10=140,
        age=65,
        health_condition="Asthma",
        outdoor_exposure="High",
        profession_exposure="Mostly outdoor",
    )

    # Display the results of both test cases
    for number, result in [(1, result1), (2, result2)]:
        print(f"\n--- Test Case {number} ---")
        print("Risk Score:", result["risk_score"])
        print("Risk Level:", result["risk_level"])
        print("Recommendations:")
        for item in result["recommendations"]:
            print("-", item)