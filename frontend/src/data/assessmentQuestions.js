export const assessmentQuestions = [
  {
    id: 1,
    field: "sleep_hours",
    question: "How many hours do you usually sleep each night?",
    type: "number",
    min: 1,
    max: 24,
    placeholder: "Enter sleep hours",
  },

  {
    id: 2,
    field: "exercise_days_per_week",
    question: "How many days per week do you exercise?",
    type: "number",
    min: 0,
    max: 7,
    placeholder: "Enter number of days",
  },

  {
    id: 3,
    field: "screen_time_hours",
    question: "How many hours per day do you usually spend on screens?",
    type: "number",
    min: 0,
    max: 24,
    placeholder: "Enter screen time",
  },

  {
    id: 4,
    field: "stress_level",
    question: "How would you rate your current stress level?",
    type: "scale",
  },

  {
    id: 5,
    field: "anxiety_level",
    question: "How would you rate your current anxiety level?",
    type: "scale",
  },

  {
    id: 6,
    field: "mood_difficulty",
    question: "How often have you experienced difficulty with your mood?",
    type: "scale",
  },

  {
    id: 7,
    field: "loneliness",
    question: "How often have you felt lonely?",
    type: "scale",
  },

  {
    id: 8,
    field: "concentration_difficulty",
    question: "How often have you had difficulty concentrating?",
    type: "scale",
  },

  {
    id: 9,
    field: "feeling_overwhelmed",
    question: "How often have you felt overwhelmed by your daily responsibilities?",
    type: "scale",
  },

  {
    id: 10,
    field: "sleep_problems_due_to_worry",
    question: "How often have worries caused problems with your sleep?",
    type: "scale",
  },

  {
    id: 11,
    field: "emotional_exhaustion",
    question: "How often have you felt emotionally exhausted?",
    type: "scale",
  },

  {
    id: 12,
    field: "social_support",
    question: "How much social support do you feel you have?",
    type: "scale",
  },

  {
    id: 13,
    field: "social_isolation",
    question: "How often have you felt socially isolated?",
    type: "scale",
  },
];

export const scaleOptions = [
  {
    value: 1,
    label: "Never / Very Low",
  },
  {
    value: 2,
    label: "Sometimes / Low",
  },
  {
    value: 3,
    label: "Often / Moderate",
  },
  {
    value: 4,
    label: "Very Often / High",
  },
  {
    value: 5,
    label: "Almost Always / Very High",
  },
];