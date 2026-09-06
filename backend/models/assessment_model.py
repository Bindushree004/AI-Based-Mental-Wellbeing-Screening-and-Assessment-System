from datetime import datetime, timezone


class Assessment:
    """
    Represents a mental wellbeing assessment.
    """

    COLLECTION = "assessments"

    def __init__(
        self,
        assessment_id,
        user_id,
        status="in_progress",
        started_at=None,
        completed_at=None
    ):
        self.assessment_id = assessment_id
        self.user_id = user_id
        self.status = status
        self.started_at = started_at or datetime.now(timezone.utc)
        self.completed_at = completed_at

    def to_dict(self):
        return {
            "assessmentId": self.assessment_id,
            "userId": self.user_id,
            "status": self.status,
            "startedAt": self.started_at,
            "completedAt": self.completed_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            assessment_id=data.get("assessmentId"),
            user_id=data.get("userId"),
            status=data.get("status", "in_progress"),
            started_at=data.get("startedAt"),
            completed_at=data.get("completedAt")
        )