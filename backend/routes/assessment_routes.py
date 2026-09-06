from flask import Blueprint, jsonify, request
from firebase_admin import auth, firestore

from config.firebase import db


assessment_bp = Blueprint("assessment", __name__)


# =========================================================
# FIREBASE TOKEN VERIFICATION
# =========================================================

def verify_token():

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None, jsonify({
            "status": "error",
            "message": "Authorization token is missing"
        }), 401

    if not auth_header.startswith("Bearer "):
        return None, jsonify({
            "status": "error",
            "message": "Invalid authorization format"
        }), 401

    token = auth_header.split("Bearer ", 1)[1].strip()

    if not token:
        return None, jsonify({
            "status": "error",
            "message": "Authorization token is empty"
        }), 401

    try:

        decoded_token = auth.verify_id_token(token)

        return decoded_token, None, None

    except auth.ExpiredIdTokenError:

        return None, jsonify({
            "status": "error",
            "message": "Firebase token has expired"
        }), 401

    except auth.InvalidIdTokenError:

        return None, jsonify({
            "status": "error",
            "message": "Invalid Firebase token"
        }), 401

    except Exception as e:

        print("Token verification error:", str(e))

        return None, jsonify({
            "status": "error",
            "message": "Failed to verify authentication"
        }), 401


# =========================================================
# GET ASSESSMENT QUESTIONS
# =========================================================

@assessment_bp.route("/api/assessment", methods=["GET", "OPTIONS"])
def get_assessment():

    if request.method == "OPTIONS":
        return "", 204

    try:

        decoded_token, error_response, error_status = verify_token()

        if error_response:
            return error_response, error_status

        question_docs = db.collection("questions").stream()

        questions = []

        for doc in question_docs:

            question = doc.to_dict()

            question["id"] = doc.id

            questions.append(question)

        # -------------------------------------------------
        # Sort questions
        # -------------------------------------------------

        questions.sort(
            key=lambda x: x.get(
                "questionNumber",
                x.get("order", 0)
            )
        )

        return jsonify({
            "status": "success",
            "questions": questions
        }), 200

    except Exception as e:

        print("Assessment fetch error:", str(e))

        return jsonify({
            "status": "error",
            "message": "Failed to fetch assessment",
            "error": str(e)
        }), 500


# =========================================================
# CALCULATE WELLBEING SCORE
# =========================================================

def calculate_wellbeing_score(answers):

    if not isinstance(answers, list):
        return None

    if len(answers) == 0:
        return None

    # -----------------------------------------------------
    # Questions where HIGHER value means WORSE wellbeing
    # -----------------------------------------------------

    negative_questions = {
        "stressLevel",
        "anxietyLevel",
        "moodDifficulty",
        "loneliness",
        "concentrationDifficulty",
        "feelingOverwhelmed",
        "sleepProblemsDueToWorry",
        "emotionalExhaustion",
        "socialIsolation"
    }

    # -----------------------------------------------------
    # Questions where HIGHER value means BETTER wellbeing
    # -----------------------------------------------------

    positive_questions = {
        "socialSupport"
    }

    wellbeing_values = []

    for item in answers:

        # -------------------------------------------------
        # Accept {question, answer}
        # -------------------------------------------------

        if isinstance(item, dict):

            question = item.get("question")

            value = item.get(
                "answer",
                item.get(
                    "value",
                    item.get("score")
                )
            )

        else:

            # Fallback for plain numeric answers
            question = None
            value = item

        # -------------------------------------------------
        # Convert answer to number
        # -------------------------------------------------

        try:

            value = float(value)

        except (TypeError, ValueError):

            continue

        # -------------------------------------------------
        # Only accept values from 1 to 5
        # -------------------------------------------------

        if value < 1 or value > 5:
            continue

        # -------------------------------------------------
        # Negative questions
        #
        # 1 = Very Low / Never  -> 100 wellbeing
        # 5 = Very High / Always -> 0 wellbeing
        # -------------------------------------------------

        if question in negative_questions:

            wellbeing_value = 6 - value

        # -------------------------------------------------
        # Positive question
        #
        # 1 = Very Low -> 0 wellbeing
        # 5 = Very High -> 100 wellbeing
        # -------------------------------------------------

        elif question in positive_questions:

            wellbeing_value = value

        else:

            # -------------------------------------------------
            # For unknown questions, treat as neutral/negative
            # -------------------------------------------------

            wellbeing_value = 6 - value

        wellbeing_values.append(wellbeing_value)

    # -----------------------------------------------------
    # No valid numeric answers
    # -----------------------------------------------------

    if not wellbeing_values:
        return None

    # -----------------------------------------------------
    # Convert average 1-5 score to 0-100
    # -----------------------------------------------------

    average = sum(wellbeing_values) / len(wellbeing_values)

    wellbeing_score = ((average - 1) / 4) * 100

    wellbeing_score = round(wellbeing_score)

    # -----------------------------------------------------
    # Keep score between 0 and 100
    # -----------------------------------------------------

    wellbeing_score = max(
        0,
        min(100, wellbeing_score)
    )

    return wellbeing_score


# =========================================================
# CALCULATE RISK LEVEL
# =========================================================

def calculate_risk_level(wellbeing_score):

    if wellbeing_score is None:
        return None

    try:

        score = float(wellbeing_score)

    except (TypeError, ValueError):

        return None

    # -----------------------------------------------------
    # Higher wellbeing = lower risk
    # -----------------------------------------------------

    if score >= 70:

        return "Low"

    elif score >= 40:

        return "Moderate"

    else:

        return "High"


# =========================================================
# SUBMIT ASSESSMENT
# =========================================================

@assessment_bp.route("/api/assessment", methods=["POST", "OPTIONS"])
def submit_assessment():

    if request.method == "OPTIONS":
        return "", 204

    try:

        # =================================================
        # VERIFY FIREBASE USER
        # =================================================

        decoded_token, error_response, error_status = verify_token()

        if error_response:
            return error_response, error_status

        uid = decoded_token["uid"]

        # =================================================
        # GET REQUEST DATA
        # =================================================

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "status": "error",
                "message": "Assessment data is missing"
            }), 400

        # =================================================
        # PERSONAL INFORMATION
        # =================================================

        age = data.get("age")
        gender = data.get("gender")
        occupation = data.get("occupation")

        # =================================================
        # ADDITIONAL INFORMATION
        # =================================================

        sleep_hours = data.get("sleepHours")
        exercise_days = data.get("exerciseDaysPerWeek")
        screen_time_hours = data.get("screenTimeHours")

        # =================================================
        # ANSWERS
        # =================================================

        answers = data.get("answers")

        if answers is None:

            return jsonify({
                "status": "error",
                "message": "Answers are missing"
            }), 400

        # =================================================
        # ANSWERS MUST BE ARRAY
        # =================================================

        if not isinstance(answers, list):

            return jsonify({
                "status": "error",
                "message": "Answers must be an array"
            }), 400

        # =================================================
        # MAKE SURE QUESTIONS WERE ANSWERED
        # =================================================

        if len(answers) == 0:

            return jsonify({
                "status": "error",
                "message": "Please answer the assessment questions"
            }), 400

        # =================================================
        # CALCULATE WELLBEING SCORE
        # =================================================

        wellbeing_score = calculate_wellbeing_score(
            answers
        )

        if wellbeing_score is None:

            return jsonify({
                "status": "error",
                "message": "Unable to calculate wellbeing score"
            }), 400

        # =================================================
        # CALCULATE RISK LEVEL
        # =================================================

        risk_level = calculate_risk_level(
            wellbeing_score
        )

        # =================================================
        # CREATE FIRESTORE DATA
        # =================================================

        assessment_data = {

            "userId": uid,

            "age": age,

            "gender": gender,

            "occupation": occupation,

            "sleepHours": sleep_hours,

            "exerciseDaysPerWeek": exercise_days,

            "screenTimeHours": screen_time_hours,

            "answers": answers,

            "wellbeingScore": wellbeing_score,

            "riskLevel": risk_level,

            "createdAt": firestore.SERVER_TIMESTAMP
        }

        # =================================================
        # SAVE TO FIRESTORE
        # =================================================

        assessment_ref = db.collection(
            "assessments"
        ).document()

        assessment_ref.set(
            assessment_data
        )

        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "status": "success",

            "message": "Assessment submitted successfully",

            "assessmentId": assessment_ref.id,

            "assessment": {

                "id": assessment_ref.id,

                "wellbeingScore": wellbeing_score,

                "riskLevel": risk_level
            }

        }), 201

    except Exception as e:

        print(
            "Assessment submission error:",
            str(e)
        )

        return jsonify({

            "status": "error",

            "message": "Failed to submit assessment",

            "error": str(e)

        }), 500


# =========================================================
# GET USER'S ASSESSMENT HISTORY
# =========================================================

@assessment_bp.route(
    "/api/assessment/history",
    methods=["GET", "OPTIONS"]
)
def get_assessment_history():

    if request.method == "OPTIONS":
        return "", 204

    try:

        decoded_token, error_response, error_status = verify_token()

        if error_response:
            return error_response, error_status

        uid = decoded_token["uid"]

        # -------------------------------------------------
        # Get user's assessments
        # -------------------------------------------------

        assessment_docs = (
            db.collection("assessments")
            .where("userId", "==", uid)
            .stream()
        )

        assessments = []

        for doc in assessment_docs:

            assessment = doc.to_dict()

            assessment["id"] = doc.id

            assessments.append(
                assessment
            )

        # -------------------------------------------------
        # Sort newest first
        # -------------------------------------------------

        assessments.sort(
            key=lambda x: (
                x.get("createdAt").timestamp()
                if x.get("createdAt")
                and hasattr(
                    x.get("createdAt"),
                    "timestamp"
                )
                else 0
            ),
            reverse=True
        )

        return jsonify({

            "status": "success",

            "assessments": assessments

        }), 200

    except Exception as e:

        print(
            "Assessment history error:",
            str(e)
        )

        return jsonify({

            "status": "error",

            "message": "Failed to fetch assessment history",

            "error": str(e)

        }), 500


# =========================================================
# GET LATEST ASSESSMENT
# =========================================================

@assessment_bp.route(
    "/api/assessment/latest",
    methods=["GET", "OPTIONS"]
)
def get_latest_assessment():

    if request.method == "OPTIONS":
        return "", 204

    try:

        decoded_token, error_response, error_status = verify_token()

        if error_response:
            return error_response, error_status

        uid = decoded_token["uid"]

        assessment_docs = (
            db.collection("assessments")
            .where("userId", "==", uid)
            .stream()
        )

        assessments = []

        for doc in assessment_docs:

            assessment = doc.to_dict()

            assessment["id"] = doc.id

            assessments.append(
                assessment
            )

        if not assessments:

            return jsonify({

                "status": "success",

                "assessment": None

            }), 200

        # -------------------------------------------------
        # Find newest assessment
        # -------------------------------------------------

        assessments.sort(
            key=lambda x: (
                x.get("createdAt").timestamp()
                if x.get("createdAt")
                and hasattr(
                    x.get("createdAt"),
                    "timestamp"
                )
                else 0
            ),
            reverse=True
        )

        latest = assessments[0]

        return jsonify({

            "status": "success",

            "assessment": latest

        }), 200

    except Exception as e:

        print(
            "Latest assessment error:",
            str(e)
        )

        return jsonify({

            "status": "error",

            "message": "Failed to fetch latest assessment",

            "error": str(e)

        }), 500