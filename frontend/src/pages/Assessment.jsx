import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getIdToken } from "firebase/auth";

import { auth } from "../firebase";
import "./Assessment.css";

function Assessment() {
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const [formData, setFormData] = useState({
    age: "",
    gender: "",
    occupation: "",
    sleepHours: "",
    exerciseDaysPerWeek: "",
    screenTimeHours: "",
    stressLevel: "",
    anxietyLevel: "",
    moodDifficulty: "",
    loneliness: "",
    concentrationDifficulty: "",
    feelingOverwhelmed: "",
    sleepProblemsDueToWorry: "",
    emotionalExhaustion: "",
    socialSupport: "",
    socialIsolation: "",
  });

  const questions = [
    {
      key: "sleepHours",
      title: "Sleep Hours",
      question: "How many hours do you usually sleep per night?",
      type: "number",
      placeholder: "Enter your average sleep hours",
    },
    {
      key: "exerciseDaysPerWeek",
      title: "Exercise Days Per Week",
      question: "How many days per week do you exercise?",
      type: "number",
      placeholder: "Enter number of days",
    },
    {
      key: "screenTimeHours",
      title: "Screen Time Hours",
      question: "How many hours do you spend on screens each day?",
      type: "number",
      placeholder: "Enter your average screen time",
    },
    {
      key: "stressLevel",
      title: "Stress Level",
      question: "How would you rate your current stress level?",
      type: "select",
    },
    {
      key: "anxietyLevel",
      title: "Anxiety Level",
      question: "How would you rate your current anxiety level?",
      type: "select",
    },
    {
      key: "moodDifficulty",
      title: "Mood Difficulty",
      question:
        "How often do you experience difficulty maintaining a positive mood?",
      type: "select",
    },
    {
      key: "loneliness",
      title: "Loneliness",
      question: "How often do you feel lonely?",
      type: "select",
    },
    {
      key: "concentrationDifficulty",
      title: "Concentration Difficulty",
      question: "How often do you have difficulty concentrating?",
      type: "select",
    },
    {
      key: "feelingOverwhelmed",
      title: "Feeling Overwhelmed",
      question:
        "How often do you feel overwhelmed by your responsibilities?",
      type: "select",
    },
    {
      key: "sleepProblemsDueToWorry",
      title: "Sleep Problems Due to Worry",
      question:
        "How often do worries make it difficult for you to sleep?",
      type: "select",
    },
    {
      key: "emotionalExhaustion",
      title: "Emotional Exhaustion",
      question: "How often do you feel emotionally exhausted?",
      type: "select",
    },
    {
      key: "socialSupport",
      title: "Social Support",
      question:
        "How would you rate the level of social support you receive?",
      type: "select",
    },
    {
      key: "socialIsolation",
      title: "Social Isolation",
      question: "How often do you feel socially isolated?",
      type: "select",
    },
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));

    setError("");
  };

  const validateCurrentStep = () => {
    if (step === 1) {
      if (!formData.age) {
        setError("Please enter your age.");
        return false;
      }

      if (!formData.gender) {
        setError("Please select your gender.");
        return false;
      }

      if (!formData.occupation.trim()) {
        setError("Please enter your occupation.");
        return false;
      }

      return true;
    }

    const currentQuestion = questions[step - 2];

    if (!formData[currentQuestion.key]) {
      setError("Please answer this question before continuing.");
      return false;
    }

    return true;
  };

  const submitAssessment = async () => {
  try {
    setSubmitting(true);
    setError("");

    const user = auth.currentUser;

    if (!user) {
      setError("Please log in again before submitting the assessment.");
      setSubmitting(false);
      return;
    }

      const token = await getIdToken(user, true);

    const answers = questions.map((question) => ({
      questionId: question.key,
      answer: formData[question.key],
    }));

    const response = await fetch(
      "http://localhost:5000/api/assessment",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          age: formData.age,
          gender: formData.gender,
          occupation: formData.occupation,
          answers: answers,
        }),
      }
    );

       const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.message || "Failed to submit assessment."
      );
    }

    console.log("Assessment submitted successfully:", data);

    navigate("/dashboard");

  } catch (err) {
    console.error("Assessment submission error:", err);

    setError(
      err.message ||
        "Unable to submit assessment. Please try again."
    );

  } finally {
    setSubmitting(false);
  }
};

  const nextStep = async () => {
    if (!validateCurrentStep()) {
      return;
    }

    if (step < 14) {
      setStep((previousStep) => previousStep + 1);
      return;
    }

    await submitAssessment();
  };

  const previousStep = () => {
    if (step > 1) {
      setStep((previousStep) => previousStep - 1);
      setError("");
    }
  };

  const currentQuestion = questions[step - 2];

  const progressPercentage = Math.round((step / 14) * 100);

  return (
    <div className="assessment-page">

      {/* Header */}
      <div className="assessment-header">
        <div className="assessment-title">

          <div className="brain-icon-container">
            <div className="brain-icon">🧠</div>
          </div>

          <div>
            <h1>Mental Wellbeing Assessment</h1>

            <p>
              Answer the following questions honestly based on
              your recent experiences.
            </p>
          </div>

        </div>
      </div>

      {/* Progress */}
      <div className="assessment-progress">

        <div className="progress-top">

          <span>
            {step === 1
              ? "Basic Information"
              : "Mental Wellbeing Assessment"}
          </span>

          <span>{progressPercentage}%</span>

        </div>

        <div className="progress-bar">

          <div
            className="progress-fill"
            style={{
              width: `${progressPercentage}%`,
            }}
          />

        </div>

      </div>

      {/* Error */}
      {error && (
        <div
          style={{
            maxWidth: "1020px",
            margin: "0 auto 20px",
            padding: "12px 16px",
            background: "#3b1d2a",
            border: "1px solid #ef4444",
            borderRadius: "8px",
            color: "#fca5a5",
            fontSize: "14px",
          }}
        >
          {error}
        </div>
      )}

      {/* Assessment Card */}
      <div className="assessment-card">

        {/* STEP 1 */}
        {step === 1 && (
          <div className="basic-information">

            <div className="section-heading">

              <div className="section-icon">
                👤
              </div>

              <div>
                <h2>Tell us a little about yourself</h2>

                <p className="section-description">
                  This information helps us understand your
                  assessment results.
                </p>
              </div>

            </div>

            {/* Age */}
            <div className="form-group">

              <label htmlFor="age">
                Age
              </label>

              <input
                id="age"
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                placeholder="Enter your age"
                min="1"
                max="100"
              />

            </div>

            {/* Gender */}
            <div className="form-group">

              <label htmlFor="gender">
                Gender
              </label>

              <select
                id="gender"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
              >

                <option value="">
                  Select gender
                </option>

                <option value="Male">
                  Male
                </option>

                <option value="Female">
                  Female
                </option>

                <option value="Other">
                  Other
                </option>

              </select>

            </div>

            {/* Occupation */}
            <div className="form-group">

              <label htmlFor="occupation">
                Occupation
              </label>

              <input
                id="occupation"
                type="text"
                name="occupation"
                value={formData.occupation}
                onChange={handleChange}
                placeholder="Enter your occupation"
              />

            </div>

          </div>
        )}

        {/* STEPS 2 - 14 */}
        {step > 1 && currentQuestion && (
          <div className="question-section">

            <div className="question-header">

              <div className="question-number">
                {step - 1}
              </div>

              <div>
                <h2>
                  {currentQuestion.title}
                </h2>

                <p className="question-text">
                  {currentQuestion.question}
                </p>
              </div>

            </div>

            {/* Number Input */}
            {currentQuestion.type === "number" && (
              <div className="form-group">

                <label htmlFor={currentQuestion.key}>
                  Your Answer
                </label>

                <input
                  id={currentQuestion.key}
                  type="number"
                  name={currentQuestion.key}
                  value={formData[currentQuestion.key]}
                  onChange={handleChange}
                  placeholder={currentQuestion.placeholder}
                  min="0"
                />

              </div>
            )}

            {/* Select Input */}
            {currentQuestion.type === "select" && (
              <div className="form-group">

                <label htmlFor={currentQuestion.key}>
                  Your Answer
                </label>

                <select
                  id={currentQuestion.key}
                  name={currentQuestion.key}
                  value={formData[currentQuestion.key]}
                  onChange={handleChange}
                >

                  <option value="">
                    Select your answer
                  </option>

                  <option value="1">
                    1 - Very Low / Never
                  </option>

                  <option value="2">
                    2 - Low / Rarely
                  </option>

                  <option value="3">
                    3 - Moderate / Sometimes
                  </option>

                  <option value="4">
                    4 - High / Often
                  </option>

                  <option value="5">
                    5 - Very High / Always
                  </option>

                </select>

              </div>
            )}

          </div>
        )}

      </div>

      {/* Navigation */}
      <div className="assessment-navigation">

        <button
          type="button"
          className="nav-arrow back-arrow"
          onClick={previousStep}
          disabled={step === 1 || submitting}
          aria-label="Go to previous step"
        >
          ←
        </button>

        <button
          type="button"
          className="nav-arrow forward-arrow"
          onClick={nextStep}
          disabled={submitting}
          aria-label={
            step === 14
              ? "Submit assessment"
              : "Go to next step"
          }
        >
          {submitting ? "..." : step === 14 ? "✓" : "→"}
        </button>

      </div>

      {/* Disclaimer */}
      <p className="assessment-disclaimer">
        This assessment is intended for wellbeing screening and
        awareness purposes. It is not a medical diagnosis.
      </p>

    </div>
  );
}

export default Assessment;