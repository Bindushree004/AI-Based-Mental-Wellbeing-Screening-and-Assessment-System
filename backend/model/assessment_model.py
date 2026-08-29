from datetime import datetime

from config.database import db


class Assessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="started"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    user = db.relationship(
        "User",
        backref=db.backref("assessments", lazy=True)
    )

    responses = db.relationship(
        "AssessmentResponse",
        backref="assessment",
        lazy=True,
        cascade="all, delete-orphan"
    )

    result = db.relationship(
        "Result",
        backref="assessment",
        uselist=False,
        cascade="all, delete-orphan"
    )