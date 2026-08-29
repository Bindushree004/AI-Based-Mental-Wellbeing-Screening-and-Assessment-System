from datetime import datetime

from config.database import db


class AssessmentResponse(db.Model):
    __tablename__ = "assessment_responses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("assessments.id"),
        nullable=False
    )

    question_id = db.Column(
        db.Integer,
        nullable=False
    )

    response = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )