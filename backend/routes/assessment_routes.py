from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from config.database import db
from model.assessment_model import Assessment
from model.assessment_response_model import AssessmentResponse
from model.result_model import Result

from model.integration.wellbeing_service import assess_wellbeing


assessment_bp = Blueprint(
    "assessment",
    __name__,
    url_prefix="/api/assessments"
)


# --------------------------------------------------
# CREATE / START ASSESSMENT
# --------------------------------------------------
@assessment_bp.route("/", methods=["POST"])
@jwt_required()
def create_assessment():

    user_id = int(get_jwt_identity())

    data = request.get_json() or {}

    age = data.get("age")
    gender = data.get("gender")
    occupation = data.get("occupation")
    sleep_hours = data.get("sleep_hours")
    exercise_days_per_week = data.get("exercise_days_per_week")
    screen_time_hours = data.get("screen_time_hours")

    assessment = Assessment(
        user_id=user_id,
        age=age,
        gender=gender,
        occupation=occupation,
        sleep_hours=sleep_hours,
        exercise_days_per_week=exercise_days_per_week,
        screen_time_hours=screen_time_hours,
        status="started"
    )

    db.session.add(assessment)
    db.session.commit()

    return jsonify({
        "message": "Assessment started successfully",
        "assessment": {
            "id": assessment.id,
            "user_id": assessment.user_id,
            "age": assessment.age,
            "gender": assessment.gender,
            "occupation": assessment.occupation,
            "sleep_hours": assessment.sleep_hours,
            "exercise_days_per_week": assessment.exercise_days_per_week,
            "screen_time_hours": assessment.screen_time_hours,
            "status": assessment.status,
            "created_at": (
                assessment.created_at.isoformat()
                if assessment.created_at else None
            )
        }
    }), 201


# --------------------------------------------------
# GET ASSESSMENT
# --------------------------------------------------
@assessment_bp.route("/<int:assessment_id>", methods=["GET"])
@jwt_required()
def get_assessment(assessment_id):

    user_id = int(get_jwt_identity())

    assessment = Assessment.query.filter_by(
        id=assessment_id,
        user_id=user_id
    ).first()

    if not assessment:
        return jsonify({
            "message": "Assessment not found"
        }), 404

    return jsonify({
        "id": assessment.id,
        "user_id": assessment.user_id,
        "age": assessment.age,
        "gender": assessment.gender,
        "occupation": assessment.occupation,
        "sleep_hours": assessment.sleep_hours,
        "exercise_days_per_week": assessment.exercise_days_per_week,
        "screen_time_hours": assessment.screen_time_hours,
        "status": assessment.status,
        "created_at": (
            assessment.created_at.isoformat()
            if assessment.created_at else None
        ),
        "completed_at": (
            assessment.completed_at.isoformat()
            if assessment.completed_at else None
        )
    }), 200


# --------------------------------------------------
# SUBMIT ASSESSMENT RESPONSE
# --------------------------------------------------
@assessment_bp.route(
    "/<int:assessment_id>/responses",
    methods=["POST"]
)
@jwt_required()
def submit_response(assessment_id):

    user_id = int(get_jwt_identity())

    assessment = Assessment.query.filter_by(
        id=assessment_id,
        user_id=user_id
    ).first()

    if not assessment:
        return jsonify({
            "message": "Assessment not found"
        }), 404

    if assessment.status == "completed":
        return jsonify({
            "message": "Assessment is already completed"
        }), 400

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    question_id = data.get("question_id")
    response = data.get("response")

    if question_id is None or response is None:
        return jsonify({
            "message": "question_id and response are required"
        }), 400

    try:
        question_id = int(question_id)
        response = int(response)
    except (TypeError, ValueError):
        return jsonify({
            "message": "question_id and response must be integers"
        }), 400

    if question_id < 1 or question_id > 10:
        return jsonify({
            "message": "question_id must be between 1 and 10"
        }), 400

    if response < 1 or response > 4:
        return jsonify({
            "message": "response must be between 1 and 4"
        }), 400

    existing_response = AssessmentResponse.query.filter_by(
        assessment_id=assessment_id,
        question_id=question_id
    ).first()

    if existing_response:

        existing_response.response = response

        db.session.commit()

        return jsonify({
            "message": "Response updated successfully",
            "response": {
                "id": existing_response.id,
                "assessment_id": existing_response.assessment_id,
                "question_id": existing_response.question_id,
                "response": existing_response.response,
                "created_at": (
                    existing_response.created_at.isoformat()
                    if existing_response.created_at else None
                )
            }
        }), 200

    new_response = AssessmentResponse(
        assessment_id=assessment.id,
        question_id=question_id,
        response=response
    )

    db.session.add(new_response)
    db.session.commit()

    return jsonify({
        "message": "Response submitted successfully",
        "response": {
            "id": new_response.id,
            "assessment_id": new_response.assessment_id,
            "question_id": new_response.question_id,
            "response": new_response.response,
            "created_at": (
                new_response.created_at.isoformat()
                if new_response.created_at else None
            )
        }
    }), 201


# --------------------------------------------------
# GENERATE ASSESSMENT RESULT
# --------------------------------------------------
@assessment_bp.route(
    "/<int:assessment_id>/complete",
    methods=["POST"]
)
@jwt_required()
def complete_assessment(assessment_id):

    user_id = int(get_jwt_identity())

    assessment = Assessment.query.filter_by(
        id=assessment_id,
        user_id=user_id
    ).first()

    if not assessment:
        return jsonify({
            "message": "Assessment not found"
        }), 404

    responses = AssessmentResponse.query.filter_by(
        assessment_id=assessment_id
    ).all()

    if len(responses) < 10:
        return jsonify({
            "message": "Please answer all 10 assessment questions",
            "answered": len(responses),
            "required": 10
        }), 400

    response_map = {
        response.question_id: response.response
        for response in responses
    }

    required_question_ids = list(range(1, 11))

    missing_questions = [
        question_id
        for question_id in required_question_ids
        if question_id not in response_map
    ]

    if missing_questions:
        return jsonify({
            "message": "Some assessment questions are unanswered",
            "missing_questions": missing_questions
        }), 400

    if (
        assessment.age is None
        or assessment.gender is None
        or assessment.occupation is None
        or assessment.sleep_hours is None
        or assessment.exercise_days_per_week is None
        or assessment.screen_time_hours is None
    ):
        return jsonify({
            "message": "Basic assessment information is incomplete"
        }), 400

    # --------------------------------------------------
    # MAP QUESTION RESPONSES TO ML FEATURES
    # --------------------------------------------------

    data = {

        "age": assessment.age,

        "gender": assessment.gender,

        "occupation": assessment.occupation,

        "sleep_hours": assessment.sleep_hours,

        "exercise_days_per_week":
            assessment.exercise_days_per_week,

        "screen_time_hours":
            assessment.screen_time_hours,

        "stress_level":
            response_map[1],

        "anxiety_level":
            response_map[2],

        "mood_difficulty":
            response_map[3],

        "loneliness":
            response_map[4],

        "concentration_difficulty":
            response_map[5],

        "feeling_overwhelmed":
            response_map[6],

        "sleep_problems_due_to_worry":
            response_map[7],

        "emotional_exhaustion":
            response_map[8],

        "social_support":
            response_map[9],

        "social_isolation":
            response_map[10]
    }

    # --------------------------------------------------
    # RUN COMPLETE ML / WELLBEING PIPELINE
    # --------------------------------------------------

    try:

        assessment_result = assess_wellbeing(data)

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Unable to generate wellbeing assessment",
            "error": str(error)
        }), 500

    score = assessment_result["score"]
    risk_level = assessment_result["risk_level"]

    # --------------------------------------------------
    # SAVE RESULT
    # --------------------------------------------------

    result = Result.query.filter_by(
        assessment_id=assessment_id
    ).first()

    if result:

        result.score = score
        result.risk_level = risk_level

    else:

        result = Result(
            assessment_id=assessment_id,
            score=score,
            risk_level=risk_level
        )

        db.session.add(result)

    assessment.status = "completed"
    assessment.completed_at = datetime.utcnow()

    db.session.commit()

    # --------------------------------------------------
    # RETURN COMPLETE RESULT
    # --------------------------------------------------

    return jsonify({

        "message":
            "Assessment completed successfully",

        "assessment_id":
            assessment_id,

        "result": {

            "id":
                result.id,

            "assessment_id":
                result.assessment_id,

            "score":
                result.score,

            "risk_level":
                result.risk_level,

            "prediction":
                assessment_result["prediction"],

            "analysis":
                assessment_result["analysis"],

            "recommendations":
                assessment_result["recommendations"],

            "created_at": (
                result.created_at.isoformat()
                if result.created_at else None
            )
        }

    }), 200
