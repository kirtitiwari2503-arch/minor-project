def get_health_advisory(aqi_category, profile):
    advice = {
        "Good": (
            "Enjoy outdoor activities as usual and "
            "continue monitoring air quality."
        ),
        "Moderate": (
            "Sensitive individuals should monitor "
            "air quality and any symptoms."
        ),
        "Poor": (
            "Reduce prolonged or strenuous outdoor "
            "activity, especially if sensitive to pollution."
        ),
        "Very Poor": (
            "Limit outdoor exposure and follow local "
            "health guidance."
        )
    }

    profile_advice = {
        "General Adult": "Follow the general precautions.",
        "Child": "Monitor air quality before outdoor activities.",
        "Older Adult": "Take extra care during periods of poor air quality.",
        "Sensitive to Air Pollution": "Pay attention to air quality alerts."
    }

    category_message = advice.get(
        aqi_category,
        "Check the latest official air quality guidance."
    )

    profile_message = profile_advice.get(
        profile,
        "Follow local health guidance."
    )

    return category_message, profile_message