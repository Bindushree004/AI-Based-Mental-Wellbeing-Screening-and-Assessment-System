def generate_analysis(
    score,
    risk_level,
    stress_level,
    anxiety_level,
    sleep_hours,
    exercise_days_per_week,
    loneliness,
    social_support,
    emotional_exhaustion
):
    """
    Generate a simple wellbeing analysis.

    This is a rule-based prototype analysis.
    It is NOT a medical diagnosis.
    """

    observations = []

    # ------------------------------------------
    # Overall result
    # ------------------------------------------

    if risk_level == "Low Risk":

        observations.append(
            "Your responses indicate a relatively "
            "low screening risk at this time."
        )

    elif risk_level == "Moderate Risk":

        observations.append(
            "Your responses indicate some areas of "
            "wellbeing that may benefit from attention."
        )

    else:

        observations.append(
            "Your responses indicate several areas "
            "that may require additional attention."
        )

    # ------------------------------------------
    # Stress
    # ------------------------------------------

    if stress_level >= 4:

        observations.append(
            "Your reported stress level is relatively high."
        )

    elif stress_level <= 2:

        observations.append(
            "Your reported stress level is relatively low."
        )

    # ------------------------------------------
    # Anxiety
    # ------------------------------------------

    if anxiety_level >= 4:

        observations.append(
            "You reported relatively high anxiety."
        )

    # ------------------------------------------
    # Sleep
    # ------------------------------------------

    if sleep_hours < 6:

        observations.append(
            "Your reported sleep duration is below "
            "the commonly recommended range for adults."
        )

    elif sleep_hours >= 7:

        observations.append(
            "Your reported sleep duration appears "
            "relatively adequate."
        )

    # ------------------------------------------
    # Exercise
    # ------------------------------------------

    if exercise_days_per_week == 0:

        observations.append(
            "You reported no regular exercise during "
            "the week."
        )

    elif exercise_days_per_week >= 3:

        observations.append(
            "You reported regular physical activity."
        )

    # ------------------------------------------
    # Loneliness
    # ------------------------------------------

    if loneliness >= 4:

        observations.append(
            "Your responses indicate a higher level "
            "of loneliness."
        )

    # ------------------------------------------
    # Social support
    # ------------------------------------------

    if social_support >= 4:

        observations.append(
            "You reported having relatively good "
            "social support."
        )

    elif social_support <= 2:

        observations.append(
            "Your reported social support appears "
            "limited."
        )

    # ------------------------------------------
    # Emotional exhaustion
    # ------------------------------------------

    if emotional_exhaustion >= 4:

        observations.append(
            "You reported relatively high emotional "
            "exhaustion."
        )

    # ------------------------------------------
    # Final disclaimer
    # ------------------------------------------

    observations.append(
        "This screening result is not a medical "
        "diagnosis. If you are concerned about your "
        "wellbeing, consider speaking with a qualified "
        "mental-health professional."
    )

    return " ".join(observations)


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    analysis = generate_analysis(

        score=75,

        risk_level="Low Risk",

        stress_level=2,

        anxiety_level=2,

        sleep_hours=6.5,

        exercise_days_per_week=3,

        loneliness=2,

        social_support=4,

        emotional_exhaustion=2

    )

    print("\n======================================")

    print("WELLBEING ANALYSIS")

    print("======================================")

    print(analysis)

    print("======================================")