# main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_recommender import recommend_seats
from db import update_user_selection
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests


@app.route("/recommend", methods=["POST"])
def ai_recommend():
    """
    Receive user info and current room context,
    return 3 AI-recommended seats calculated by the backend algorithm.
    """
    data = request.get_json()

    user_id = data.get("user_id")
    room = data.get("room")  # e.g., "101", "205"
    building = data.get("building", "")
    floor = data.get("floor", "")

    if not user_id or not room:
        return jsonify({"error": "user_id and room are required"}), 400

    # List of seats already taken in this room (can be extended later)
    occupied_seats = []

    # Core: AI recommendation (100% backend-controlled)
    recommended = recommend_seats(
        user_id=user_id,
        room=room,
        occupied=occupied_seats
    )

    return jsonify({
        "recommended_seats": recommended,
        "message": "AI recommendation successful"
    })


@app.route("/feedback", methods=["POST"])
def feedback():
    """
    Save the seat actually chosen by the user.
    This data will be used to continuously improve the AI model.
    """
    data = request.get_json()

    user_id = data.get("user_id")
    room = data.get("room")
    selected_seat = data.get("selected_seat")

    if not all([user_id, room, selected_seat]):
        return jsonify({"error": "Missing required fields"}), 400

    update_user_selection(user_id, room, selected_seat)

    return jsonify({
        "status": "saved",
        "message": "User selection recorded successfully"
    })


if __name__ == "__main__":
    print("AI Seat Recommendation Service Started")
    print("→ Access at: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)