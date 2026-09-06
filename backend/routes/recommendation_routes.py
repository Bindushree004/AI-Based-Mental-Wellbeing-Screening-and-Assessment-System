from flask import Blueprint, jsonify, request
from firebase_admin import auth
from config.firebase import db


recommendation_bp = Blueprint(
    "recommendation",
    __name__
)


# =========================================================
# VERIFY FIREBASE USER
# =========================================================

def get_current_user():

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise Exception("Authorization header is missing")

    if not auth_header.startswith("Bearer "):
        raise Exception("Invalid authorization format")

    token = auth_header.split("Bearer ")[1]

    if not token:
        raise Exception("Firebase token is missing")

    decoded_token = auth.verify_id_token(token)

    return decoded_token


# =========================================================
# GENERATE RECOMMENDATIONS
# =========================================================

def generate_recommendations(score, risk_level):

    recommendations = []

    # -----------------------------------------------------
    # Sleep
    # -----------------------------------------------------

    recommendations.append({
        "title": "Improve Your Sleep",
        "category": "Sleep",
        "icon": "sleep",
        "description": (
            "Maintain a consistent sleep schedule and aim for "
            "adequate rest each night."
        )
    })

    # -----------------------------------------------------
    # Physical Activity
    # -----------------------------------------------------

    recommendations.append({
        "title": "Stay Physically Active",
        "category": "Physical Activity",
        "icon": "activity",
        "description": (
            "Include regular physical activity in your daily "
            "routine to support your overall wellbeing."
        )
    })

    # -----------------------------------------------------
    # Digital Wellbeing
    # -----------------------------------------------------

    recommendations.append({
        "title": "Manage Screen Time",
        "category": "Digital Wellbeing",
        "icon": "screen",
        "description": (
            "Take regular breaks from screens and avoid excessive "
            "screen usage, especially before bedtime."
        )
    })

    # -----------------------------------------------------
    # Social Wellbeing
    # -----------------------------------------------------

    recommendations.append({
        "title": "Stay Socially Connected",
        "category": "Social Wellbeing",
        "icon": "social",
        "description": (
            "Spend meaningful time with friends, family, or people "
            "who provide positive social support."
        )
    })

    # -----------------------------------------------------
    # Emotional Wellbeing
    # -----------------------------------------------------

    recommendations.append({
        "title": "Take Care of Your Emotional Wellbeing",
        "category": "Emotional Wellbeing",
        "icon": "support",
        "description": (
            "Make time for activities that help you relax, reflect, "
            "and manage everyday emotional challenges."
        )
    })

    # -----------------------------------------------------
    # Stress Management
    # -----------------------------------------------------

    recommendations.append({
        "title": "Practice Stress Management",
        "category": "Mental Wellbeing",
        "icon": "stress",
        "description": (
            "Try relaxation techniques such as deep breathing, "
            "meditation, mindfulness, or taking short breaks."
        )
    })

    # -----------------------------------------------------
    # Additional recommendations for higher risk
    # -----------------------------------------------------

    if risk_level.lower() == "high" or score < 50:

        recommendations.append({
            "title": "Reach Out for Support",
            "category": "Emotional Support",
            "icon": "support",
            "description": (
                "Consider talking with a trusted friend, family "
                "member, counselor, or qualified mental health professional "
                "if you are experiencing ongoing difficulties."
            )
        })

    elif risk_level.lower() == "moderate" or score < 70:

        recommendations.append({
            "title": "Practice Relaxation Regularly",
            "category": "Stress Management",
            "icon": "stress",
            "description": (
                "Set aside a few minutes each day for breathing "
                "exercises, mindfulness, or another relaxing activity."
            )
        })

    return recommendations


# =========================================================
# GET RECOMMENDATIONS
# =========================================================

@recommendation_bp.route(
    "/api/recommendations",
    methods=["GET"]
)
def get_recommendations():

    try:

        # -------------------------------------------------
        # Authenticate user
        # -------------------------------------------------

        decoded_user = get_current_user()

        user_id = decoded_user["uid"]

        # -------------------------------------------------
        # Get user's assessments
        # -------------------------------------------------

        assessments_ref = (
            db.collection("assessments")
            .where("userId", "==", user_id)
            .stream()
        )

        assessments = []

        for document in assessments_ref:

            data = document.to_dict()

            data["_document_id"] = document.id

            assessments.append(data)

        # -------------------------------------------------
        # No assessment
        # -------------------------------------------------

        if not assessments:

            return jsonify({
                "status": "success",
                "hasAssessment": False,
                "recommendations": []
            }), 200

        # -------------------------------------------------
        # Find latest assessment
        # -------------------------------------------------

        def get_sort_value(item):

            value = (
                item.get("createdAt")
                or item.get("created_at")
                or item.get("date")
                or ""
            )

            return str(value)

        assessments.sort(
            key=get_sort_value,
            reverse=True
        )

        latest = assessments[0]

        # -------------------------------------------------
        # Get score
        # -------------------------------------------------

        score = latest.get("score")

        if score is None:
            score = latest.get("overallScore")

        if score is None:
            score = latest.get("wellbeingScore")

        try:
            score = float(score)
        except (TypeError, ValueError):
            score = 0

        # -------------------------------------------------
        # Get risk level
        # -------------------------------------------------

        risk_level = (
            latest.get("riskLevel")
            or latest.get("risk_level")
            or latest.get("risk")
            or "Unknown"
        )

        # -------------------------------------------------
        # Generate recommendations
        # -------------------------------------------------

        recommendations = generate_recommendations(
            score,
            risk_level
        )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return jsonify({
            "status": "success",
            "hasAssessment": True,
            "score": score,
            "riskLevel": risk_level,
            "recommendations": recommendations
        }), 200

    except Exception as e:

        print(
            "Recommendation error:",
            str(e)
        )

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500