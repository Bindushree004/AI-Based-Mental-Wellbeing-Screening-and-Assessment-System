import os
import smtplib

from email.message import EmailMessage

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from model.user_model import User
from config.database import db


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# ---------------------------------------------------------
# Token generator for password reset
# ---------------------------------------------------------

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(
        os.getenv("SECRET_KEY")
    )

    return serializer.dumps(email, salt="password-reset")


def verify_reset_token(token):
    serializer = URLSafeTimedSerializer(
        os.getenv("SECRET_KEY")
    )

    try:
        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=3600
        )

        return email

    except (SignatureExpired, BadSignature):
        return None


# ---------------------------------------------------------
# Send password reset email
# ---------------------------------------------------------

def send_reset_email(email, reset_link):

    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")

    message = EmailMessage()

    message["Subject"] = "MindSync AI - Password Reset"
    message["From"] = sender_email
    message["To"] = email

    message.set_content(
        f"""
Hello,

We received a request to reset your MindSync AI password.

Click the link below to reset your password:

{reset_link}

This link will expire in 1 hour.

If you did not request a password reset, you can safely ignore this email.

Regards,
MindSync AI Team
"""
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(message)


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "message": "Name, email and password are required"
        }), 400

    if len(password) < 6:
        return jsonify({
            "message": "Password must be at least 6 characters"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "Email already registered"
        }), 409

    user = User(
        name=name,
        email=email
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful",
        "user": user.to_dict()
    }), 201


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200


# ---------------------------------------------------------
# FORGOT PASSWORD
# ---------------------------------------------------------

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    email = data.get("email")

    if not email:
        return jsonify({
            "message": "Email is required"
        }), 400

    user = User.query.filter_by(email=email).first()

    # Don't reveal whether the email exists
    if not user:
        return jsonify({
            "message": "If the email is registered, a password reset link has been sent."
        }), 200

    try:

        token = generate_reset_token(email)

        frontend_url = os.getenv(
            "FRONTEND_URL",
            "http://localhost:5173"
        )

        reset_link = (
            f"{frontend_url}/reset-password?token={token}"
        )

        send_reset_email(
            email,
            reset_link
        )

        return jsonify({
            "message": "Password reset link has been sent to your email."
        }), 200

    except Exception as error:

        print("Email sending error:", error)

        return jsonify({
            "message": "Unable to send password reset email."
        }), 500


# ---------------------------------------------------------
# RESET PASSWORD
# ---------------------------------------------------------

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    token = data.get("token")
    new_password = data.get("password")

    if not token or not new_password:
        return jsonify({
            "message": "Token and password are required"
        }), 400

    if len(new_password) < 6:
        return jsonify({
            "message": "Password must be at least 6 characters"
        }), 400

    email = verify_reset_token(token)

    if not email:
        return jsonify({
            "message": "Invalid or expired reset link"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    user.set_password(new_password)

    db.session.commit()

    return jsonify({
        "message": "Password reset successful"
    }), 200