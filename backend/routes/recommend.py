from flask import Blueprint, request, jsonify

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.json

    percentile = data.get("percentile")
    branch = data.get("branch")

    # dummy logic
    colleges = [
        {"name": "ABC College", "cutoff": 90},
        {"name": "XYZ College", "cutoff": 85}
    ]

    result = [c for c in colleges if percentile >= c["cutoff"]]

    return jsonify(result)
