def calculate_wellbeing_score(
    stress_level,
    anxiety_level,
    mood_difficulty,
    loneliness,
    concentration_difficulty,
    feeling_overwhelmed,
    sleep_problems_due_to_worry,
    emotional_exhaustion,
    social_support,
    social_isolation
):
    """
    Calculate an explainable wellbeing score from 0 to 100.

    This is a prototype screening score.
    It is NOT a medical diagnosis.
    """

    # ------------------------------------------
    # Negative wellbeing factors
    # ------------------------------------------

    negative_score = (
        stress_level
        + anxiety_level
        + mood_difficulty
        + loneliness
        + concentration_difficulty
        + feeling_overwhelmed
        + sleep_problems_due_to_worry
        + emotional_exhaustion
        + social_isolation
    )

    # ------------------------------------------
    # Positive factor
    # ------------------------------------------

    positive_score = social_support

    # ------------------------------------------
    # Combined risk score
    # ------------------------------------------

    risk_score = negative_score - positive_score

    # Minimum possible risk score:
    # 9 negative factors × 1 - 5 support = 4
    #
    # Maximum possible risk score:
    # 9 negative factors × 5 - 1 support = 44

    minimum_risk = 4
    maximum_risk = 44

    # Convert risk score into 0-100 wellbeing score.
    #
    # Low risk = higher wellbeing score
    # High risk = lower wellbeing score

    wellbeing_score = 100 - (
        (risk_score - minimum_risk)
        / (maximum_risk - minimum_risk)
        * 100
    )

    # Keep score between 0 and 100

    wellbeing_score = max(
        0,
        min(100, wellbeing_score)
    )

    return round(wellbeing_score, 2)


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    score = calculate_wellbeing_score(

        stress_level=2,

        anxiety_level=2,

        mood_difficulty=2,

        loneliness=2,

        concentration_difficulty=2,

        feeling_overwhelmed=2,

        sleep_problems_due_to_worry=2,

        emotional_exhaustion=2,

        social_support=4,

        social_isolation=2

    )

    print("\n==============================")

    print("WELLBEING SCORE")

    print("==============================")

    print("Score:", score, "/ 100")

    print("==============================")