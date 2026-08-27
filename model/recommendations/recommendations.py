def generate_recommendations(
    stress_level,
    anxiety_level,
    sleep_hours,
    exercise_days_per_week,
    loneliness,
    social_support,
    emotional_exhaustion
):
    """
    Generate basic personalized wellbeing recommendations.

    This is a rule-based prototype.
    It is NOT medical advice or a diagnosis.
    """

    recommendations = []

    # ------------------------------------------
    # Stress
    # ------------------------------------------

    if stress_level >= 4:

        recommendations.append(
            "Try simple stress-management activities such "
            "as deep breathing, short breaks, or relaxation exercises."
        )

    # ------------------------------------------
    # Anxiety
    # ------------------------------------------

    if anxiety_level >= 4:

        recommendations.append(
            "Consider setting aside time for calming activities "
            "and discussing persistent anxiety with a qualified professional."
        )

    # ------------------------------------------
    # Sleep
    # ------------------------------------------

    if sleep_hours < 6:

        recommendations.append(
            "Try to maintain a consistent sleep schedule and "
            "aim for adequate sleep each night."
        )

    # ------------------------------------------
    # Physical activity
    # ------------------------------------------

    if exercise_days_per_week < 2:

        recommendations.append(
            "Consider gradually adding regular physical activity "
            "such as walking, stretching, or another activity you enjoy."
        )

    # ------------------------------------------
    # Loneliness
    # ------------------------------------------

    if loneliness >= 4:

        recommendations.append(
            "Consider spending time with trusted friends, family, "
            "or supportive communities to strengthen social connections."
        )

    # ------------------------------------------
    # Social support
    # ------------------------------------------

    if social_support <= 2:

        recommendations.append(
            "If you are comfortable, consider reaching out to someone "
            "you trust for emotional or practical support."
        )

    # ------------------------------------------
    # Emotional exhaustion
    # ------------------------------------------

    if emotional_exhaustion >= 4:

        recommendations.append(
            "Make time for rest and activities that help you recover "
            "from emotional or mental fatigue."
        )

    # ------------------------------------------
    # Default recommendation
    # ------------------------------------------

    if len(recommendations) == 0:

        recommendations.append(
            "Continue maintaining healthy sleep, physical activity, "
            "social connections, and regular self-care habits."
        )

    # ------------------------------------------
    # Professional support
    # ------------------------------------------

    recommendations.append(
        "If wellbeing difficulties persist or significantly affect "
        "daily life, consider speaking with a qualified mental-health professional."
    )

    return recommendations


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    recommendations = generate_recommendations(

        stress_level=4,

        anxiety_level=3,

        sleep_hours=5,

        exercise_days_per_week=1,

        loneliness=4,

        social_support=2,

        emotional_exhaustion=4

    )

    print("\n======================================")

    print("PERSONALIZED RECOMMENDATIONS")

    print("======================================")

    for number, recommendation in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"{number}. {recommendation}"
        )

    print("======================================")