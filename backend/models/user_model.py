from datetime import datetime, timezone


class User:
    """
    Represents a user stored in the Firestore 'users' collection.
    """

    COLLECTION = "users"

    def __init__(
        self,
        uid,
        name,
        email,
        phone=None,
        created_at=None,
        updated_at=None
    ):
        self.uid = uid
        self.name = name
        self.email = email
        self.phone = phone
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def to_dict(self):
        """
        Convert the User object into a dictionary
        suitable for storing in Firestore.
        """
        return {
            "uid": self.uid,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a User object from Firestore data.
        """
        return cls(
            uid=data.get("uid"),
            name=data.get("name", ""),
            email=data.get("email", ""),
            phone=data.get("phone"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )