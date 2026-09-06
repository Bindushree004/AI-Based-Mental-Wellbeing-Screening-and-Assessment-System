from flask import Blueprint, jsonify, request
from firebase_admin import auth
from config.firebase import db


auth_bp = Blueprint("auth", __name__)


# =========================================================
# AUTHENTICATION HELPER
# =========================================================

def get_authenticated_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise ValueError("Authorization token is missing")

    if not auth_header.startswith("Bearer "):
        raise ValueError("Invalid authorization format")

    token = auth_header.split("Bearer ", 1)[1].strip()

    if not token:
        raise ValueError("Authorization token is missing")

    return auth.verify_id_token(token)


# =========================================================
# REGISTER USER
# =========================================================

@auth_bp.route("/api/auth/register", methods=["POST", "OPTIONS"])
def register_user():

    if request.method == "OPTIONS":
        return "", 204

    try:

        # -------------------------------------------------
        # Verify Firebase ID token
        # -------------------------------------------------

        decoded_token = get_authenticated_user()

        uid = decoded_token["uid"]

        # -------------------------------------------------
        # Get request data
        # -------------------------------------------------

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "status": "error",
                "message": "Registration data is missing"
            }), 400

        name = data.get("name", "")
        email = data.get(
            "email",
            decoded_token.get("email", "")
        )
        phone = data.get("phone", "")

        # -------------------------------------------------
        # Create / update Firestore user profile
        # -------------------------------------------------

        user_ref = db.collection("users").document(uid)

        user_data = {
            "uid": uid,
            "name": name,
            "email": email,
            "phone": phone
        }

        user_ref.set(user_data, merge=True)

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return jsonify({
            "status": "success",
            "message": "User registered successfully",
            "user": user_data
        }), 201

    except auth.ExpiredIdTokenError:

        return jsonify({
            "status": "error",
            "message": "Firebase token has expired"
        }), 401

    except auth.InvalidIdTokenError:

        return jsonify({
            "status": "error",
            "message": "Invalid Firebase token"
        }), 401

    except ValueError as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 401

    except Exception as e:

        print("Registration error:", str(e))

        return jsonify({
            "status": "error",
            "message": "Failed to register user",
            "error": str(e)
        }), 500


# =========================================================
# LOGIN USER
# =========================================================

@auth_bp.route("/api/auth/login", methods=["POST", "OPTIONS"])
def login_user():

    if request.method == "OPTIONS":
        return "", 204

    try:

        # -------------------------------------------------
        # Verify Firebase ID token
        # -------------------------------------------------

        decoded_token = get_authenticated_user()

        uid = decoded_token["uid"]

        email = decoded_token.get("email", "")
        name = decoded_token.get("name", "")

        # -------------------------------------------------
        # Get user from Firestore
        # -------------------------------------------------

        user_ref = db.collection("users").document(uid)
        user_doc = user_ref.get()

        if user_doc.exists:

            user_data = user_doc.to_dict()

        else:

            # -------------------------------------------------
            # Create profile if it doesn't exist
            # -------------------------------------------------

            user_data = {
                "uid": uid,
                "email": email,
                "name": name,
                "phone": ""
            }

            user_ref.set(user_data)

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "uid": uid,
                "email": user_data.get("email", email),
                "name": user_data.get("name", name),
                "phone": user_data.get("phone", "")
            }
        }), 200

    except auth.ExpiredIdTokenError:

        return jsonify({
            "status": "error",
            "message": "Firebase token has expired"
        }), 401

    except auth.InvalidIdTokenError:

        return jsonify({
            "status": "error",
            "message": "Invalid Firebase token"
        }), 401

    except ValueError as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 401

    except Exception as e:

        print("Login error:", str(e))

        return jsonify({
            "status": "error",
            "message": "Login failed",
            "error": str(e)
        }), 500


# =========================================================
# GET CURRENT USER
# =========================================================

@auth_bp.route("/api/auth/me", methods=["GET", "OPTIONS"])
def get_current_user():

    if request.method == "OPTIONS":
        return "", 204

    try:

        decoded_token = get_authenticated_user()

        uid = decoded_token["uid"]

        user_ref = db.collection("users").document(uid)
        user_doc = user_ref.get()

        if user_doc.exists:

            user_data = user_doc.to_dict()

        else:

            user_data = {
                "uid": uid,
                "email": decoded_token.get("email", ""),
                "name": decoded_token.get("name", ""),
                "phone": ""
            }

        return jsonify({
            "status": "success",
            "user": {
                "uid": uid,
                "email": user_data.get(
                    "email",
                    decoded_token.get("email", "")
                ),
                "name": user_data.get(
                    "name",
                    decoded_token.get("name", "")
                ),
                "phone": user_data.get(
                    "phone",
                    ""
                )
            }
        }), 200

    except auth.ExpiredIdTokenError:

        return jsonify({
            "status": "error",
            "message": "Firebase token has expired"
        }), 401

    except auth.InvalidIdTokenError:

        return jsonify({
            "status": "error",
            "message": "Invalid Firebase token"
        }), 401

    except ValueError as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 401

    except Exception as e:

        print("Get current user error:", str(e))

        return jsonify({
            "status": "error",
            "message": "Authentication failed",
            "error": str(e)
        }), 500


# =========================================================
# VERIFY TOKEN
# =========================================================

@auth_bp.route("/api/auth/verify", methods=["GET", "OPTIONS"])
def verify_token():

    if request.method == "OPTIONS":
        return "", 204

    try:

        decoded_token = get_authenticated_user()

        return jsonify({
            "status": "success",
            "message": "Token is valid",
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email")
        }), 200

    except auth.ExpiredIdTokenError:

        return jsonify({
            "status": "error",
            "message": "Firebase token has expired"
        }), 401

    except auth.InvalidIdTokenError:

        return jsonify({
            "status": "error",
            "message": "Invalid Firebase token"
        }), 401

    except ValueError as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 401

    except Exception as e:

        print("Token verification error:", str(e))

        return jsonify({
            "status": "error",
            "message": "Token verification failed",
            "error": str(e)
        }), 500