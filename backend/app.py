import os
import sys

# Allow "from backend.X import Y" when run from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from backend.routes.recommend import recommend_bp
from backend.routes.auth import auth_bp

app = Flask(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET", "dev-secret-change-in-prod")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 86400   # 24 hours

# ── Extensions ────────────────────────────────────────────────────────────────
CORS(app)
jwt = JWTManager(app)

# ── Blueprints ────────────────────────────────────────────────────────────────
app.register_blueprint(recommend_bp)
app.register_blueprint(auth_bp)

# ── Health check ──────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return jsonify({
        "message": "SCAGS API is running",
        "version": "1.0.0",
        "endpoints": {
            "POST /auth/register": "Create account",
            "POST /auth/login":    "Login → get JWT token",
            "POST /recommend":     "Get college recommendations (JWT required)",
            "GET  /branches":      "List available branches"
        }
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "true").lower() == "true", port=5000)
