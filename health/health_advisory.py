"""
NABHA - Rule-Based Health Risk & Personalized Preventive Advisory

This is a project-defined preventive advisory system.
It is NOT a medically validated clinical risk score and does NOT diagnose disease.
"""

PM25_HIGH = 60   # Project-defined recommendation threshold
PM10_HIGH = 100  # Project-defined recommendation threshold


def get_aqi_base_risk(aqi):
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


def get_health_modifier(health_condition):
    condition = str(health_condition).strip().lower()
    if condition == "asthma":
        return 15
    elif condition in {"heart disease", "heart disease/cardiovascular"}:
        return 15
    elif condition in {"other respiratory", "other respiratory condition"}:
        return 10
    return 0


def get_age_modifier(age):
    return 10 if age < 18 or age >= 60 else 0


def get_outdoor_modifier(outdoor_exposure):
    exposure = str(outdoor_exposure).strip().lower()
    if exposure == "high":
        return 10
    elif exposure == "moderate":
        return 5
    return 0


def get_profession_modifier(profession_exposure):
    profession = str(profession_exposure).strip().lower()
    if profession in {"mostly outdoor", "outdoor"}:
        return 10
    elif profession == "mixed":
        return 5
    return 0


def get_predicted_aqi_modifier(current_aqi, predicted_aqi):
    # >20% increase gets +10 instead of adding both +5 and +10.
    if predicted_aqi <= current_aqi:
        return 0
    if current_aqi == 0:
        return 10

    percentage_increase = ((predicted_aqi - current_aqi) / current_aqi) * 100
    if percentage_increase > 20:
        return 10
    return 5


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
    base_risk = get_aqi_base_risk(current_aqi)
    health_modifier = get_health_modifier(health_condition)
    age_modifier = get_age_modifier(age)
    outdoor_modifier = get_outdoor_modifier(outdoor_exposure)
    profession_modifier = get_profession_modifier(profession_exposure)
    predicted_modifier = get_predicted_aqi_modifier(current_aqi, predicted_aqi)

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


def get_risk_level(score):
    if score <= 24:
        return "Low"
    elif score <= 49:
        return "Moderate"
    elif score <= 74:
        return "High"
    return "Very High"


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
    recommendations = []

    condition = str(health_condition).strip().lower()
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

    if predicted_aqi > current_aqi:
        recommendations.append(
            "Predicted AQI is higher than the current AQI; plan outdoor activities accordingly."
        )

    if str(outdoor_exposure).strip().lower() in {"moderate", "high"}:
        recommendations.append(
            "Consider reducing the duration of outdoor exposure during higher pollution periods."
        )

    if str(profession_exposure).strip().lower() in {
        "mixed", "mostly outdoor", "outdoor"
    }:
        recommendations.append(
            "If outdoor work is unavoidable, take appropriate exposure-reduction precautions and monitor AQI."
        )

    if sensitive_user and current_aqi > 100:
        recommendations.append(
            "Because you are in a project-defined sensitive group, take extra precautions during high pollution."
        )

    if pm25 > PM25_HIGH:
        recommendations.append(
            f"PM2.5 is elevated (>{PM25_HIGH}). Reduce prolonged exposure to particulate pollution."
        )

    if pm10 > PM10_HIGH:
        recommendations.append(
            f"PM10 is elevated (>{PM10_HIGH}). Avoid dusty or heavily polluted outdoor areas."
        )

    if risk_level in {"High", "Very High"}:
        recommendations.append(
            "Overall project-defined risk is elevated; consider limiting unnecessary outdoor exposure."
        )

    return recommendations


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
    level = get_risk_level(score)
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

    return {
        "risk_score": score,
        "risk_level": level,
        "recommendations": recommendations,
    }


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

    for number, result in [(1, result1), (2, result2)]:
        print(f"\n--- Test Case {number} ---")
        print("Risk Score:", result["risk_score"])
        print("Risk Level:", result["risk_level"])
        print("Recommendations:")
        for item in result["recommendations"]:
            print("-", item)