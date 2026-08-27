import joblib
import pandas as pd


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

MODEL_PATH = "model/saved_models/wellbeing_model.pkl"

model = joblib.load(MODEL_PATH)


# ==========================================
# PREDICTION FUNCTION
# ==========================================

def predict_wellbeing(
    age,
    gender,
    occupation,
    sleep_hours,
    exercise_days_per_week,
    screen_time_hours,
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

    input_data = pd.DataFrame({

        "Age": [age],

        "Gender": [gender],

        "Occupation": [occupation],

        "Sleep_Hours": [sleep_hours],

        "Exercise_Days_Per_Week": [
            exercise_days_per_week
        ],

        "Screen_Time_Hours": [
            screen_time_hours
        ],

        "Stress_Level": [
            stress_level
        ],

        "Anxiety_Level": [
            anxiety_level
        ],

        "Mood_Difficulty": [
            mood_difficulty
        ],

        "Loneliness": [
            loneliness
        ],

        "Concentration_Difficulty": [
            concentration_difficulty
        ],

        "Feeling_Overwhelmed": [
            feeling_overwhelmed
        ],

        "Sleep_Problems_Due_To_Worry": [
            sleep_problems_due_to_worry
        ],

        "Emotional_Exhaustion": [
            emotional_exhaustion
        ],

        "Social_Support": [
            social_support
        ],

        "Social_Isolation": [
            social_isolation
        ]

    })

    prediction = model.predict(input_data)[0]

    return prediction


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    result = predict_wellbeing(

        age=25,

        gender="Female",

        occupation="Student",

        sleep_hours=6.5,

        exercise_days_per_week=3,

        screen_time_hours=5,

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

    print("\n===================================")
    print("MENTAL WELLBEING PREDICTION")
    print("===================================")
    print("Risk Level:", result)
    print("===================================")