from flask import Flask, jsonify
from flask_cors import CORS

from config.firebase import db

from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.assessment_routes import assessment_bp
from routes.history_routes import history_bp
from routes.recommendation_routes import recommendation_bp


app = Flask(__name__)


# =========================================================
# CORS
# =========================================================

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173"
            ]
        }
    },
    methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS"
    ],
    allow_headers=[
        "Content-Type",
        "Authorization"
    ],
    supports_credentials=True
)


# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

app.register_blueprint(auth_bp)

app.register_blueprint(dashboard_bp)

# Use a unique registration name to avoid
# Blueprint name conflicts.
app.register_blueprint(
    assessment_bp,
    name="assessment_api"
)

app.register_blueprint(history_bp)

app.register_blueprint(
    recommendation_bp
)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return jsonify({
        "status": "success",
        "message": "AI-Based Mental Wellbeing Backend is running"
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "success",
        "message": "Backend is healthy"
    })


# =========================================================
# FIREBASE TEST
# =========================================================

@app.route("/api/firebase-test")
def firebase_test():

    try:

        test_ref = (
            db
            .collection("system")
            .document("test")
        )

        test_ref.set({
            "status": "connected"
        })

        return jsonify({
            "status": "success",
            "message": "Firebase Firestore connection successful"
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": "Firebase connection failed",
            "error": str(e)
        }), 500


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )