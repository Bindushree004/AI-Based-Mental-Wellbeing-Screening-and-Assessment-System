from flask import Blueprint, jsonify, request
from firebase_admin import auth

from config.firebase import db


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/api/dashboard", methods=["GET"])
def get_dashboard():

    try:
        # -----------------------------------
        # Get Authorization header
        # -----------------------------------

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Authorization token is missing"
            }), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "status": "error",
                "message": "Invalid authorization format"
            }), 401

        token = auth_header.split("Bearer ", 1)[1].strip()

        if not token:
            return jsonify({
                "status": "error",
                "message": "Firebase token is missing"
            }), 401

        # -----------------------------------
        # Verify Firebase ID token
        # -----------------------------------

        decoded_token = auth.verify_id_token(token)

        uid = decoded_token["uid"]

        # -----------------------------------
        # Get user information
        # -----------------------------------

        user_ref = db.collection("users").document(uid)
        user_doc = user_ref.get()

        user_data = {}

        if user_doc.exists:
            user_data = user_doc.to_dict()

        # -----------------------------------
        # Get user's assessments
        # -----------------------------------

        assessments_ref = (
            db.collection("assessments")
            .where("userId", "==", uid)
        )

        assessment_docs = assessments_ref.stream()

        assessments = []

        for doc in assessment_docs:

            assessment_data = doc.to_dict()

            assessment_data["id"] = doc.id

            # Convert Firestore timestamp to string
            if assessment_data.get("createdAt"):
                created_at = assessment_data["createdAt"]

                if hasattr(created_at, "isoformat"):
                    assessment_data["createdAt"] = created_at.isoformat()

            assessments.append(assessment_data)

        # -----------------------------------
        # Sort assessments
        # -----------------------------------

        assessments.sort(
            key=lambda x: x.get("createdAt", ""),
            reverse=True
        )

        # -----------------------------------
        # Dashboard statistics
        # -----------------------------------

        assessments_completed = len(assessments)

        latest_assessment = None

        if assessments:
            latest_assessment = assessments[0]

        wellbeing_score = None
        risk_level = None
        last_assessment = None

        if latest_assessment:

            wellbeing_score = latest_assessment.get(
                "wellbeingScore"
            )

            risk_level = latest_assessment.get(
                "riskLevel"
            )

            last_assessment = latest_assessment.get(
                "createdAt"
            )

        # -----------------------------------
        # User information
        # -----------------------------------

        user_name = user_data.get(
            "name",
            decoded_token.get("name", "")
        )

        user_email = user_data.get(
            "email",
            decoded_token.get("email", "")
        )

        # -----------------------------------
        # Response
        # -----------------------------------

        return jsonify({

            "status": "success",

            "user": {
                "uid": uid,
                "name": user_name,
                "email": user_email
            },

            "dashboard": {

                "wellbeingScore": wellbeing_score,

                "riskLevel": risk_level,

                "assessmentsCompleted": assessments_completed,

                "lastAssessment": last_assessment

            },

            "latestAssessment": latest_assessment

        }), 200

    # -----------------------------------
    # Firebase token errors
    # -----------------------------------

    except auth.ExpiredIdTokenError:

        return jsonify({
            "status": "error",
            "message": "Firebase token has expired"
        }), 401

    except auth.InvalidIdTokenError:

        return jsonify({
            "status": "error",
            "message": "Invalid Firebase token"
        }), 401

    # -----------------------------------
    # Other errors
    # -----------------------------------

    except Exception as e:

        print("Dashboard error:", str(e))

        return jsonify({
            "status": "error",
            "message": "Failed to load dashboard",
            "error": str(e)
        }), 500