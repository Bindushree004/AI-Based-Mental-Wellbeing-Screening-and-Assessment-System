from flask import Blueprint, jsonify, request
from firebase_admin import auth

from config.firebase import db


history_bp = Blueprint("history", __name__)


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
# GET USER ASSESSMENT HISTORY
# =========================================================

@history_bp.route(
    "/api/assessment/history",
    methods=["GET", "OPTIONS"]
)
def get_assessment_history():

    if request.method == "OPTIONS":
        return "", 204

    try:

        # -------------------------------------------------
        # Verify Firebase user
        # -------------------------------------------------

        decoded_token, error_response, error_status = verify_token()

        if error_response:
            return error_response, error_status

        uid = decoded_token["uid"]

        # -------------------------------------------------
        # Get assessments belonging to logged-in user
        # -------------------------------------------------

        assessment_docs = (
            db.collection("assessments")
            .where("userId", "==", uid)
            .stream()
        )

        assessments = []

        # -------------------------------------------------
        # Convert Firestore documents
        # -------------------------------------------------

        for doc in assessment_docs:

            data = doc.to_dict()

            created_at = data.get("createdAt")

            # ---------------------------------------------
            # Format date
            # ---------------------------------------------

            if created_at:

                try:
                    formatted_date = created_at.strftime(
                        "%B %d, %Y"
                    )

                except Exception:
                    formatted_date = str(created_at)

            else:

                formatted_date = "Unknown date"

            # ---------------------------------------------
            # Store timestamp temporarily for sorting
            # ---------------------------------------------

            timestamp = None

            if created_at and hasattr(
                created_at,
                "timestamp"
            ):

                try:
                    timestamp = created_at.timestamp()

                except Exception:
                    timestamp = 0

            # ---------------------------------------------
            # Create assessment object
            # ---------------------------------------------

            assessment = {

                "id": doc.id,

                "wellbeingScore":
                    data.get("wellbeingScore"),

                "riskLevel":
                    data.get("riskLevel"),

                "status":
                    data.get("status", "Completed"),

                "createdAt":
                    formatted_date,

                "timestamp":
                    timestamp,

                "age":
                    data.get("age"),

                "gender":
                    data.get("gender"),

                "occupation":
                    data.get("occupation"),

                "sleepHours":
                    data.get("sleepHours"),

                "exerciseDaysPerWeek":
                    data.get("exerciseDaysPerWeek"),

                "screenTimeHours":
                    data.get("screenTimeHours"),

                "answers":
                    data.get("answers", []),

                "analysis":
                    data.get("analysis"),

                "recommendations":
                    data.get("recommendations", [])

            }

            assessments.append(assessment)

        # -------------------------------------------------
        # Sort newest assessment first
        # -------------------------------------------------

        assessments.sort(
            key=lambda x: (
                x["timestamp"]
                if x["timestamp"] is not None
                else 0
            ),
            reverse=True
        )

        # -------------------------------------------------
        # Add assessment numbers
        # -------------------------------------------------

        total_assessments = len(assessments)

        for index, assessment in enumerate(assessments):

            assessment["assessmentNumber"] = (
                total_assessments - index
            )

        # -------------------------------------------------
        # Remove internal timestamp
        # -------------------------------------------------

        for assessment in assessments:

            assessment.pop(
                "timestamp",
                None
            )

        # -------------------------------------------------
        # Latest assessment
        # -------------------------------------------------

        latest_assessment = (
            assessments[0]
            if assessments
            else None
        )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return jsonify({

            "status": "success",

            "totalAssessments":
                total_assessments,

            "latestScore":
                latest_assessment.get(
                    "wellbeingScore"
                )
                if latest_assessment
                else None,

            "latestRiskLevel":
                latest_assessment.get(
                    "riskLevel"
                )
                if latest_assessment
                else None,

            "assessments":
                assessments

        }), 200

    except Exception as e:

        print(
            "Assessment history error:",
            str(e)
        )

        return jsonify({

            "status": "error",

            "message":
                "Failed to fetch assessment history",

            "error":
                str(e)

        }), 500


# =========================================================
# GET SINGLE ASSESSMENT
# =========================================================

@history_bp.route(
    "/api/assessment/history/<assessment_id>",
    methods=["GET", "OPTIONS"]
)
def get_single_assessment(assessment_id):

    if request.method == "OPTIONS":
        return "", 204

    try:

        # -------------------------------------------------
        # Verify Firebase user
        # -------------------------------------------------

        decoded_token, error_response, error_status = verify_token()

        if error_response:
            return error_response, error_status

        uid = decoded_token["uid"]

        # -------------------------------------------------
        # Get assessment
        # -------------------------------------------------

        assessment_ref = (
            db.collection("assessments")
            .document(assessment_id)
        )

        assessment_snapshot = assessment_ref.get()

        if not assessment_snapshot.exists:

            return jsonify({
                "status": "error",
                "message": "Assessment not found"
            }), 404

        data = assessment_snapshot.to_dict()

        # -------------------------------------------------
        # Security check
        # -------------------------------------------------

        if data.get("userId") != uid:

            return jsonify({
                "status": "error",
                "message": "You are not authorized to view this assessment"
            }), 403

        # -------------------------------------------------
        # Format date
        # -------------------------------------------------

        created_at = data.get("createdAt")

        if created_at:

            try:

                formatted_date = created_at.strftime(
                    "%B %d, %Y"
                )

            except Exception:

                formatted_date = str(created_at)

        else:

            formatted_date = "Unknown date"

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return jsonify({

            "status": "success",

            "assessment": {

                "id": assessment_snapshot.id,

                "wellbeingScore":
                    data.get("wellbeingScore"),

                "riskLevel":
                    data.get("riskLevel"),

                "status":
                    data.get("status", "Completed"),

                "createdAt":
                    formatted_date,

                "age":
                    data.get("age"),

                "gender":
                    data.get("gender"),

                "occupation":
                    data.get("occupation"),

                "sleepHours":
                    data.get("sleepHours"),

                "exerciseDaysPerWeek":
                    data.get("exerciseDaysPerWeek"),

                "screenTimeHours":
                    data.get("screenTimeHours"),

                "answers":
                    data.get("answers", []),

                "analysis":
                    data.get("analysis"),

                "recommendations":
                    data.get("recommendations", [])

            }

        }), 200

    except Exception as e:

        print(
            "Single assessment error:",
            str(e)
        )

        return jsonify({

            "status": "error",

            "message":
                "Failed to fetch assessment",

            "error":
                str(e)

        }), 500