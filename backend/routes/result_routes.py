from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from config.database import db
from models.assessment_model import Assessment
from models.assessment_response_model import AssessmentResponse
from models.result_model import Result


result_bp = Blueprint(
    "result",
    __name__,
    url_prefix="/api/results"
)


@result_bp.route("/<int:assessment_id>/generate", methods=["POST"])
@jwt_required()
def generate_result(assessment_id):

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

    if not responses:
        return jsonify({
            "message": "No responses found for this assessment"
        }), 400

    total_score = sum(response.response for response in responses)

    if total_score <= 4:
        risk_level = "Low"
    elif total_score <= 9:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    result = Result.query.filter_by(
        assessment_id=assessment_id
    ).first()

    if result:
        result.score = total_score
        result.risk_level = risk_level
    else:
        result = Result(
            assessment_id=assessment_id,
            score=total_score,
            risk_level=risk_level
        )
        db.session.add(result)

    assessment.status = "completed"
    assessment.completed_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        "message": "Assessment result generated successfully",
        "result": {
            "id": result.id,
            "assessment_id": result.assessment_id,
            "score": result.score,
            "risk_level": result.risk_level,
            "created_at": (
                result.created_at.isoformat()
                if result.created_at else None
            )
        }
    }), 200


@result_bp.route("/<int:assessment_id>", methods=["GET"])
@jwt_required()
def get_result(assessment_id):

    user_id = int(get_jwt_identity())

    assessment = Assessment.query.filter_by(
        id=assessment_id,
        user_id=user_id
    ).first()

    if not assessment:
        return jsonify({
            "message": "Assessment not found"
        }), 404

    result = Result.query.filter_by(
        assessment_id=assessment_id
    ).first()

    if not result:
        return jsonify({
            "message": "Result not generated yet"
        }), 404

    return jsonify({
        "id": result.id,
        "assessment_id": result.assessment_id,
        "score": result.score,
        "risk_level": result.risk_level,
        "created_at": (
            result.created_at.isoformat()
            if result.created_at else None
        )
    }), 200