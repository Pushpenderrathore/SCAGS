from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.db import get_db

recommend_bp = Blueprint("recommend", __name__)


def score_college(college, percentile, preferred_location=None, max_fees=None):
    """
    Composite scoring algorithm:
    - Placement weight: 40%
    - Ranking weight:   30%
    - Cutoff margin:    20%  (how comfortably above cutoff you are)
    - Fees weight:      10%  (lower is better, inverted)
    """
    placement_score = college["placement"] / 100.0 * 40

    ranking = college["ranking"] or 30
    ranking_score = max(0, (30 - ranking) / 30) * 30

    margin = percentile - college["cutoff"]
    cutoff_score = min(margin / 10.0, 1.0) * 20  # cap at 10 percentile margin

    max_possible_fees = 250000
    fees_score = max(0, (max_possible_fees - college["fees"]) / max_possible_fees) * 10

    total = placement_score + ranking_score + cutoff_score + fees_score
    return round(total, 2)


@recommend_bp.route("/recommend", methods=["POST"])
@jwt_required()
def recommend():
    data = request.get_json()
    percentile = data.get("percentile")
    branch = data.get("branch", "CSE")
    max_fees = data.get("max_fees")           # optional filter
    location_filter = data.get("location")    # optional filter (state/city substring)

    if percentile is None:
        return jsonify({"error": "percentile is required"}), 400

    try:
        percentile = float(percentile)
    except (ValueError, TypeError):
        return jsonify({"error": "percentile must be a number"}), 400

    if not (0 <= percentile <= 100):
        return jsonify({"error": "percentile must be between 0 and 100"}), 400

    conn = get_db()

    query = """
        SELECT name, branch, cutoff, fees, location, placement, ranking
        FROM colleges
        WHERE branch = ? AND cutoff <= ?
    """
    params = [branch, percentile]

    if max_fees:
        query += " AND fees <= ?"
        params.append(int(max_fees))

    if location_filter:
        query += " AND location LIKE ?"
        params.append(f"%{location_filter}%")

    rows = conn.execute(query, params).fetchall()
    conn.close()

    colleges = [dict(row) for row in rows]

    # Score and sort
    for college in colleges:
        college["score"] = score_college(college, percentile)

    colleges.sort(key=lambda c: c["score"], reverse=True)

    return jsonify({
        "percentile": percentile,
        "branch": branch,
        "count": len(colleges),
        "results": colleges
    })


@recommend_bp.route("/branches", methods=["GET"])
def get_branches():
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT branch FROM colleges ORDER BY branch").fetchall()
    conn.close()
    return jsonify([r["branch"] for r in rows])
