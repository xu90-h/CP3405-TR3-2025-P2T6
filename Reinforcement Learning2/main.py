from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from contextlib import contextmanager
from ai_rl_simple_recommender import RLSeatRecommender
from db import SeatDataProcessor
import json
import os

app = FastAPI()

# Cross-origin configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Unify JSON file paths
JSON_FILE_PATH = "seat_data.json"

# Initialize JSON file
def init_json_file():
    if not os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump({"users": []}, f, indent=2)

# Read JSON Data
def load_json_data():
    init_json_file()
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Write JSON data
def save_to_json(data):
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Database connection
@contextmanager
def get_db_conn():
    conn = sqlite3.connect("seat_reserve.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        yield cursor, conn
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Initialize the database
def init_db():
    with get_db_conn() as (cursor, _):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                position_weight REAL DEFAULT 0.33,
                window_weight REAL DEFAULT 0.33,
                aisle_weight REAL DEFAULT 0.34
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seat_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                seat_id TEXT,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

# Get user's past seat selections
def get_user_history_seats(user_id: str) -> list:
    with get_db_conn() as (cursor, _):
        cursor.execute('''
            SELECT DISTINCT seat_id FROM seat_records 
            WHERE user_id = ? ORDER BY create_time DESC
        ''', (user_id,))
        return [row["seat_id"] for row in cursor.fetchall()]

# Update user preferences
def update_user_preference(user_id: str, seat_id: str):
    row = ord(seat_id[0]) - ord("A")
    col = int(seat_id[1:]) - 1
    attr = SeatDataProcessor.get_seat_attr(row, col)

    with get_db_conn() as (cursor, _):
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        preference = {
            "position": user["position_weight"],
            "window": user["window_weight"],
            "aisle": user["aisle_weight"]
        }

    rl_recommender = RLSeatRecommender()
    rl_recommender.update_preference(preference, row, col)

    with get_db_conn() as (cursor, _):
        cursor.execute('''
            UPDATE users SET position_weight = ?, window_weight = ?, aisle_weight = ?
            WHERE user_id = ?
        ''', (preference["position"], preference["window"], preference["aisle"], user_id))

# Initialize
rl_recommender = RLSeatRecommender()
init_db()
init_json_file()


# Interface 1: AI Recommended Seats
@app.get("/api/recommend-seat")
def recommend_seat(user_id: str = Query(...)):
    try:
        with get_db_conn() as (cursor, _):
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            if not user:
                cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
                preference = {"position": 0.33, "window": 0.33, "aisle": 0.34}
            else:
                preference = {
                    "position": user["position_weight"],
                    "window": user["window_weight"],
                    "aisle": user["aisle_weight"]
                }

        history_seats = get_user_history_seats(user_id)
        recommend_seat = rl_recommender.get_recommend(history_seats, preference)

        # Update unified JSON
        json_data = load_json_data()
        user_data = next((u for u in json_data["users"] if u["user_id"] == user_id), None)
        if not user_data:
            user_data = {
                "user_id": user_id,
                "history_seats": history_seats,
                "recommended_seats": [],
                "selected_seats": []
            }
            json_data["users"].append(user_data)
        user_data["recommended_seats"].append(recommend_seat)
        user_data["history_seats"] = history_seats
        save_to_json(json_data)

        # Return format adapted for the frontend
        return {"code": 200, "seat": recommend_seat}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")


# Interface 2: Confirm Seat Selection
@app.post("/api/select-seat")
def select_seat(user_id: str = Query(...), seat_id: str = Query(...)):
    try:
        if len(seat_id) < 2:
            raise HTTPException(status_code=400, detail="Invalid seat ID (e.g., A1/B2)")
        row_char = seat_id[0].upper()
        col_str = seat_id[1:]
        if not (row_char in "ABCDEFG" and col_str.isdigit() and 1 <= int(col_str) <= 7):
            raise HTTPException(status_code=400, detail="Invalid seat ID (e.g., A1/B2)")

        with get_db_conn() as (cursor, _):
            cursor.execute(
                "INSERT INTO seat_records (user_id, seat_id) VALUES (?, ?)",
                (user_id, seat_id)
            )
        update_user_preference(user_id, seat_id)
        history_seats = get_user_history_seats(user_id)

        # Update Unified JSON
        json_data = load_json_data()
        user_data = next((u for u in json_data["users"] if u["user_id"] == user_id), None)
        if not user_data:
            user_data = {
                "user_id": user_id,
                "history_seats": history_seats,
                "recommended_seats": [],
                "selected_seats": []
            }
            json_data["users"].append(user_data)
        user_data["selected_seats"].append(seat_id)
        user_data["history_seats"] = history_seats
        save_to_json(json_data)

        return {"code": 200, "msg": "Seat confirmed", "selected_seat": seat_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Selection failed: {str(e)}")


# Interface 3: Get User's Seat History
@app.get("/api/history-seats")
def get_history_seats_api(user_id: str = Query(...)):
    try:
        history = get_user_history_seats(user_id)
        return {"code": 200, "history_seats": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Load history failed: {str(e)}")


# API 4: Get All Reserved Seats
@app.get("/api/booked-seats")
def get_booked_seats_api():
    try:
        with get_db_conn() as (cursor, _):
            cursor.execute("SELECT DISTINCT seat_id FROM seat_records")
            booked = [row["seat_id"] for row in cursor.fetchall()]
        return {"code": 200, "booked_seats": booked}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Load booked seats failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)