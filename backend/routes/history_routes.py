from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.assessment_model import Assessment
from model.result_model import Result


history_bp = Blueprint(
    "history",
    __name__,
    url_prefix="/api/history"
)


@history_bp.route("/", methods=["GET"])
@jwt_required()
def get_history():

    user_id = int(get_jwt_identity())

    assessments = Assessment.query.filter_by(
        user_id=user_id
    ).order_by(
        Assessment.created_at.desc()
    ).all()

    history = []

    for assessment in assessments:

        result = Result.query.filter_by(
            assessment_id=assessment.id
        ).first()

        history.append({
            "assessment_id": assessment.id,
            "status": assessment.status,
            "created_at": (
                assessment.created_at.isoformat()
                if assessment.created_at else None
            ),
            "completed_at": (
                assessment.completed_at.isoformat()
                if assessment.completed_at else None
            ),
            "score": result.score if result else None,
            "risk_level": result.risk_level if result else None
        })

    return jsonify({
        "message": "Assessment history fetched successfully",
        "history": history
    }), 200
