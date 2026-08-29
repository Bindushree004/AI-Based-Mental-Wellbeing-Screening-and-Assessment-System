import numpy as np
import pandas as pd

# Reproducible results
np.random.seed(42)

# Number of synthetic participants
NUMBER_OF_RECORDS = 5000


# ==========================================
# 1. DEMOGRAPHIC FEATURES
# ==========================================

age = np.random.randint(18, 66, NUMBER_OF_RECORDS)

gender = np.random.choice(
    ["Male", "Female", "Other"],
    NUMBER_OF_RECORDS,
    p=[0.48, 0.48, 0.04]
)

occupation = np.random.choice(
    [
        "Student",
        "Employed",
        "Self-employed",
        "Unemployed",
        "Homemaker"
    ],
    NUMBER_OF_RECORDS
)


# ==========================================
# 2. LIFESTYLE FEATURES
# ==========================================

sleep_hours = np.clip(
    np.random.normal(6.8, 1.3, NUMBER_OF_RECORDS),
    3,
    10
).round(1)

exercise_days = np.random.randint(
    0,
    8,
    NUMBER_OF_RECORDS
)

screen_time = np.clip(
    np.random.normal(5.5, 2.0, NUMBER_OF_RECORDS),
    1,
    12
).round(1)


# ==========================================
# 3. WELLBEING FEATURES
# ==========================================

stress = np.random.randint(
    1,
    6,
    NUMBER_OF_RECORDS
)

anxiety = np.random.randint(
    1,
    6,
    NUMBER_OF_RECORDS
)

mood = np.random.randint(
    1,
    6,
    NUMBER_OF_RECORDS
)

loneliness = np.random.randint(
    1,
    6,
    NUMBER_OF_RECORDS
)

concentration_difficulty = np.random.randint(
    1,
    6,
    NUMBER_OF_RECORDS
)

feeling_overwhelmed = np.random.randint(
    1,
    6,
    NUMBER_OF_RECORDS
)

sleep_problems_due_to_worry = np.random.randint(
    1,
    6,
    NUMBER_OF_RECORDS
)

emotional_exhaustion = np.random.randint(
    1,
    6,
    NUMBER_OF_RECORDS
)

social_support = np.random.randint(
    1,
    6,
    NUMBER_OF_RECORDS
)

social_isolation = np.random.randint(
    1,
    6,
    NUMBER_OF_RECORDS
)


# ==========================================
# 4. SYNTHETIC RISK SCORE
# ==========================================
#
# This is ONLY for creating prototype labels.
# It is NOT a medical diagnostic formula.
#
# Higher concerning factors increase risk.
# Higher social support decreases risk.
# ==========================================

risk_score = (
    stress
    + anxiety
    + loneliness
    + concentration_difficulty
    + feeling_overwhelmed
    + sleep_problems_due_to_worry
    + emotional_exhaustion
    + social_isolation
    - social_support
)


# ==========================================
# 5. CREATE THREE RISK CATEGORIES
# ==========================================

risk_level = pd.qcut(
    risk_score,
    q=3,
    labels=[
        "Low Risk",
        "Moderate Risk",
        "High Risk"
    ]
)


# ==========================================
# 6. CREATE DATAFRAME
# ==========================================

df = pd.DataFrame({

    "Age": age,

    "Gender": gender,

    "Occupation": occupation,

    "Sleep_Hours": sleep_hours,

    "Exercise_Days_Per_Week": exercise_days,

    "Screen_Time_Hours": screen_time,

    "Stress_Level": stress,

    "Anxiety_Level": anxiety,

    "Mood_Difficulty": mood,

    "Loneliness": loneliness,

    "Concentration_Difficulty": concentration_difficulty,

    "Feeling_Overwhelmed": feeling_overwhelmed,

    "Sleep_Problems_Due_To_Worry": sleep_problems_due_to_worry,

    "Emotional_Exhaustion": emotional_exhaustion,

    "Social_Support": social_support,

    "Social_Isolation": social_isolation,

    "Risk_Level": risk_level
})


# ==========================================
# 7. SAVE DATASET
# ==========================================

output_file = (
    "dataset/synthetic/"
    "synthetic_mental_wellbeing_dataset.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("Synthetic dataset created successfully!")

print("\nNumber of records:")
print(len(df))

print("\nNumber of columns:")
print(len(df.columns))

print("\nDataset preview:")
print(df.head())

print("\nRisk distribution:")
print(df["Risk_Level"].value_counts())

print("\nSaved to:")
print(output_file)