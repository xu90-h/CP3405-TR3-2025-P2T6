# ai_recommender.py
from collections import defaultdict
from db import load_data

# All possible seats in the classroom (A1-G7)
ALL_SEATS = [f"{row}{col}" for row in "ABCDEFG" for col in range(1, 8)]


class SeatRecommender:
    """
    Contextual Bandit-style seat recommender.
    Intelligently suggests seats based on:
    - User's personal history
    - User's preferences in this specific room
    - Global popularity among all users
    - Built-in prior: middle rows (C/D) are preferred
    """

    def __init__(self):
        # Exploration-encouraging score: start with optimistic values
        self.seat_scores = defaultdict(lambda: {"count": 1, "reward": 5.0})

    def select_top_seats(self, user: dict, room: str, occupied: list, n: int = 3) -> list:
        """
        Return the top n recommended available seats for the user.
        """
        user_history = user.get("history_seats", [])
        room_history = user.get("room_history", {}).get(room, [])

        available_seats = [s for s in ALL_SEATS if s not in occupied]

        scores = {}

        # Load global usage statistics
        data = load_data()
        global_popularity = defaultdict(int)
        for u in data.get("users", []):
            for seat in u.get("history_seats", []):
                global_popularity[seat] += 1

        for seat in available_seats:
            score = 1.0  # base score

            # Strong boost: user previously chose this seat in this room
            if seat in room_history:
                score += 5.0

            # Medium boost: user likes this seat in any room
            if seat in user_history:
                score += 3.0

            # Social proof: how many others chose this seat
            score += global_popularity[seat] * 0.5

            # Built-in prior: people prefer middle rows (C and D)
            row = seat[0]
            if row in "CD":
                score += 1.5
            elif row in "AB":
                score += 0.8  # front rows slightly better than back

            scores[seat] = score

        # Return top n seats by score
        top_seats = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return [seat for seat, _ in top_seats]


# Global recommender instance
recommender = SeatRecommender()


def recommend_seats(user_id: str, room: str, occupied: list = None) -> list:
    """
    Public function called by Flask API.
    Returns 3 personalized seat recommendations.
    """
    if occupied is None:
        occupied = []

    data = load_data()
    user = next(
        (u for u in data.get("users", []) if u["user_id"] == user_id),
        None
    )

    # New user? Start with empty history
    if user is None:
        user = {
            "user_id": user_id,
            "history_seats": [],
            "room_history": {}
        }

    return recommender.select_top_seats(
        user=user,
        room=room,
        occupied=occupied,
        n=3
    )