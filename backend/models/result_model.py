from datetime import datetime, timezone


class Result:
    """
    Represents the final result of a mental wellbeing assessment.
    """

    COLLECTION = "results"

    def __init__(
        self,
        result_id,
        assessment_id,
        user_id,
        score,
        risk_level,
        prediction=None,
        analysis=None,
        recommendations=None,
        created_at=None
    ):
        self.result_id = result_id
        self.assessment_id = assessment_id
        self.user_id = user_id
        self.score = score
        self.risk_level = risk_level
        self.prediction = prediction
        self.analysis = analysis
        self.recommendations = recommendations or []
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "resultId": self.result_id,
            "assessmentId": self.assessment_id,
            "userId": self.user_id,
            "score": self.score,
            "riskLevel": self.risk_level,
            "prediction": self.prediction,
            "analysis": self.analysis,
            "recommendations": self.recommendations,
            "createdAt": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            result_id=data.get("resultId"),
            assessment_id=data.get("assessmentId"),
            user_id=data.get("userId"),
            score=data.get("score"),
            risk_level=data.get("riskLevel"),
            prediction=data.get("prediction"),
            analysis=data.get("analysis"),
            recommendations=data.get("recommendations", []),
            created_at=data.get("createdAt")
        )