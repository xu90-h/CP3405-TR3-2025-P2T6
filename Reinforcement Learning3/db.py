# db.py
import json
from typing import Dict, Optional


# Path to the persistent JSON database file
DATA_FILE = "users.json"


def load_data() -> Dict:
    """
    Load user data from users.json.
    Creates an empty structure if the file doesn't exist yet.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": []}
    except json.JSONDecodeError:
        print("Warning: users.json is corrupted. Starting with empty database.")
        return {"users": []}


def save_data(data: Dict) -> None:
    """
    Save the complete user database back to users.json.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_user(user_id: str) -> Optional[Dict]:
    """
    Retrieve a user record by user_id.
    Returns None if the user does not exist.
    """
    data = load_data()
    for user in data.get("users", []):
        if user.get("user_id") == user_id:
            return user
    return None


def update_user_selection(user_id: str, room: str, selected_seat: str) -> None:
    """
    Record a seat selection for a user.
    Creates a new user entry if this is their first time.
    Updates:
      - Global seat history
      - Per-room seat history (for stronger personalization)
    """
    data = load_data()

    # Find existing user or create new one
    user = None
    for u in data["users"]:
        if u["user_id"] == user_id:
            user = u
            break

    if user is None:
        user = {
            "user_id": user_id,
            "history_seats": [],      # All seats ever chosen by this user
            "room_history": {},       # Seat choices per room (contextual memory)
            "selected_seats": []      # Legacy field (kept for compatibility)
        }
        data["users"].append(user)

    # Update global history (avoid duplicates)
    if selected_seat not in user["history_seats"]:
        user["history_seats"].append(selected_seat)

    # Update current selection log
    user["selected_seats"].append(selected_seat)

    # Update room-specific history (key for personalization)
    if room not in user["room_history"]:
        user["room_history"][room] = []
    user["room_history"][room].append(selected_seat)

    # Persist changes
    save_data(data)