from model.prediction.predict_new import predict_wellbeing
from model.scoring.score import calculate_wellbeing_score
from model.scoring.risk import classify_risk
from model.analysis.wellbeing_analysis import generate_analysis
from model.recommendations.recommendations import generate_recommendations


def assess_wellbeing(data):
    """
    Complete wellbeing assessment pipeline.

    Input:
        Dictionary containing questionnaire responses.

    Output:
        Dictionary containing:
        - prediction
        - score
        - risk_level
        - analysis
        - recommendations

    This is a screening prototype and is NOT a medical diagnosis.
    """

    # ==========================================
    # 1. ML PREDICTION
    # ==========================================

    prediction = predict_wellbeing(
        age=data["age"],
        gender=data["gender"],
        occupation=data["occupation"],
        sleep_hours=data["sleep_hours"],
        exercise_days_per_week=data["exercise_days_per_week"],
        screen_time_hours=data["screen_time_hours"],
        stress_level=data["stress_level"],
        anxiety_level=data["anxiety_level"],
        mood_difficulty=data["mood_difficulty"],
        loneliness=data["loneliness"],
        concentration_difficulty=data["concentration_difficulty"],
        feeling_overwhelmed=data["feeling_overwhelmed"],
        sleep_problems_due_to_worry=data[
            "sleep_problems_due_to_worry"
        ],
        emotional_exhaustion=data["emotional_exhaustion"],
        social_support=data["social_support"],
        social_isolation=data["social_isolation"]
    )

    # ==========================================
    # 2. WELLBEING SCORE
    # ==========================================

    score = calculate_wellbeing_score(
        stress_level=data["stress_level"],
        anxiety_level=data["anxiety_level"],
        mood_difficulty=data["mood_difficulty"],
        loneliness=data["loneliness"],
        concentration_difficulty=data[
            "concentration_difficulty"
        ],
        feeling_overwhelmed=data[
            "feeling_overwhelmed"
        ],
        sleep_problems_due_to_worry=data[
            "sleep_problems_due_to_worry"
        ],
        emotional_exhaustion=data[
            "emotional_exhaustion"
        ],
        social_support=data["social_support"],
        social_isolation=data["social_isolation"]
    )

    # ==========================================
    # 3. RISK CLASSIFICATION
    # ==========================================

    risk_level = classify_risk(score)

    # ==========================================
    # 4. AI-BASED / RULE-BASED ANALYSIS
    # ==========================================

    analysis = generate_analysis(
        score=score,
        risk_level=risk_level,
        stress_level=data["stress_level"],
        anxiety_level=data["anxiety_level"],
        sleep_hours=data["sleep_hours"],
        exercise_days_per_week=data[
            "exercise_days_per_week"
        ],
        loneliness=data["loneliness"],
        social_support=data["social_support"],
        emotional_exhaustion=data[
            "emotional_exhaustion"
        ]
    )

    # ==========================================
    # 5. PERSONALIZED RECOMMENDATIONS
    # ==========================================

    recommendations = generate_recommendations(
        stress_level=data["stress_level"],
        anxiety_level=data["anxiety_level"],
        sleep_hours=data["sleep_hours"],
        exercise_days_per_week=data[
            "exercise_days_per_week"
        ],
        loneliness=data["loneliness"],
        social_support=data["social_support"],
        emotional_exhaustion=data[
            "emotional_exhaustion"
        ]
    )

    # ==========================================
    # 6. RETURN COMPLETE RESULT
    # ==========================================

    return {
        "prediction": prediction,
        "score": score,
        "risk_level": risk_level,
        "analysis": analysis,
        "recommendations": recommendations
    }


# ==========================================
# TEST THE COMPLETE PIPELINE
# ==========================================

if __name__ == "__main__":

    sample_user = {

        "age": 25,

        "gender": "Female",

        "occupation": "Student",

        "sleep_hours": 6.5,

        "exercise_days_per_week": 3,

        "screen_time_hours": 5,

        "stress_level": 2,

        "anxiety_level": 2,

        "mood_difficulty": 2,

        "loneliness": 2,

        "concentration_difficulty": 2,

        "feeling_overwhelmed": 2,

        "sleep_problems_due_to_worry": 2,

        "emotional_exhaustion": 2,

        "social_support": 4,

        "social_isolation": 2
    }

    result = assess_wellbeing(sample_user)

    print("\n")
    print("=" * 60)
    print("COMPLETE WELLBEING ASSESSMENT")
    print("=" * 60)

    print("\nPrediction:")
    print(result["prediction"])

    print("\nScore:")
    print(result["score"], "/ 100")

    print("\nRisk Level:")
    print(result["risk_level"])

    print("\nAnalysis:")
    print(result["analysis"])

    print("\nRecommendations:")

    for number, recommendation in enumerate(
        result["recommendations"],
        start=1
    ):
        print(
            f"{number}. {recommendation}"
        )

    print("\n" + "=" * 60)