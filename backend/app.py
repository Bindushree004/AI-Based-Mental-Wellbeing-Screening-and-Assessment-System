import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config.database import init_db
from models import User, Assessment, AssessmentResponse, Result

from routes.auth_routes import auth_bp
from routes.assessment_routes import assessment_bp
from routes.profile_routes import profile_bp
from routes.result_routes import result_bp
from routes.history_routes import history_bp


app = Flask(__name__)

# JWT configuration
app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY",
    "dev-secret-key"
)
JWTManager(app)

# Database
init_db(app)

# CORS
CORS(app)

# Routes
app.register_blueprint(auth_bp)
app.register_blueprint(assessment_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(result_bp)
app.register_blueprint(history_bp)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Backend is running"
    })


if __name__ == "__main__":
    app.run(debug=True)