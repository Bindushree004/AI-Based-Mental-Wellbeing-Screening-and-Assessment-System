from datetime import datetime

from config.database import db


class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("assessments.id"),
        nullable=False,
        unique=True
    )

    score = db.Column(
        db.Float,
        nullable=True
    )

    risk_level = db.Column(
        db.String(50),
        nullable=True
    )

    prediction = db.Column(
        db.String(100),
        nullable=True
    )

    analysis = db.Column(
        db.Text,
        nullable=True
    )

    recommendations = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )