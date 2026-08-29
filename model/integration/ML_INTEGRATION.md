# ML Integration Instructions

## ML File

The ML service is:

model/integration/wellbeing_service.py

## How to use it

In Flask, import:

from model.integration.wellbeing_service import assess_wellbeing

Then send the user's assessment data:

data = {
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

Call:

result = assess_wellbeing(data)

The result contains:

prediction
score
risk_level
analysis
recommendations