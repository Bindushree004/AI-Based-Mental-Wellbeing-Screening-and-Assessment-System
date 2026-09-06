class AssessmentResponse:
    """
    Represents a user's answer to one assessment question.
    """

    COLLECTION = "assessmentResponses"

    def __init__(
        self,
        response_id,
        assessment_id,
        user_id,
        question_id,
        answer,
        score=None
    ):
        self.response_id = response_id
        self.assessment_id = assessment_id
        self.user_id = user_id
        self.question_id = question_id
        self.answer = answer
        self.score = score

    def to_dict(self):
        return {
            "responseId": self.response_id,
            "assessmentId": self.assessment_id,
            "userId": self.user_id,
            "questionId": self.question_id,
            "answer": self.answer,
            "score": self.score
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            response_id=data.get("responseId"),
            assessment_id=data.get("assessmentId"),
            user_id=data.get("userId"),
            question_id=data.get("questionId"),
            answer=data.get("answer"),
            score=data.get("score")
        )