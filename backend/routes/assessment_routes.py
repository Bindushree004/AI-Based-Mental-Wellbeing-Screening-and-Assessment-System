from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from config.database import db
from models.assessment_model import Assessment
from models.assessment_response_model import AssessmentResponse


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

    user_id = get_jwt_identity()

    assessment = Assessment(
        user_id=int(user_id),
        status="started"
    )

    db.session.add(assessment)
    db.session.commit()

    return jsonify({
        "message": "Assessment started successfully",
        "assessment": {
            "id": assessment.id,
            "user_id": assessment.user_id,
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

    user_id = get_jwt_identity()

    assessment = Assessment.query.filter_by(
        id=assessment_id,
        user_id=int(user_id)
    ).first()

    if not assessment:
        return jsonify({
            "message": "Assessment not found"
        }), 404

    return jsonify({
        "id": assessment.id,
        "user_id": assessment.user_id,
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

    user_id = get_jwt_identity()

    assessment = Assessment.query.filter_by(
        id=assessment_id,
        user_id=int(user_id)
    ).first()

    if not assessment:
        return jsonify({
            "message": "Assessment not found"
        }), 404

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