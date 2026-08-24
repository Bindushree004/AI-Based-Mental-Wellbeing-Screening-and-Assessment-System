def classify_risk(score):
    """
    Convert wellbeing score into a screening risk category.

    This is a prototype classification system.
    It is NOT a medical diagnosis.
    """

    if score >= 70:
        return "Low Risk"

    elif score >= 40:
        return "Moderate Risk"

    else:
        return "High Risk"


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    test_scores = [85, 65, 35]

    for score in test_scores:

        risk = classify_risk(score)

        print(
            f"Score: {score} → {risk}"
        )