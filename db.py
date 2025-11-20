import sqlite3
from datetime import datetime
from typing import Dict


conn = sqlite3.connect("seat_management.db", check_same_thread=False)
cursor = conn.cursor()

# Create table structure
def create_tables():
    # Seating Real-Time Status Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seat_info (
            seat_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,  -- free/occupied/booked
            distance INTEGER NOT NULL,
            type TEXT NOT NULL
        )
    ''')
    # Recommendation/Booking Log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            seat_id TEXT NOT NULL,
            operation_type TEXT NOT NULL,
            user_preference TEXT,
            create_time DATETIME NOT NULL
        )
    ''')
    conn.commit()

# Initialize seat data
def init_seat_data():
    seats = [
        ("A1", "free", 3, "window"),
        ("A2", "free", 5, "aisle"),
        ("A3", "occupied", 4, "window"),
        ("A4", "free", 2, "aisle"),
        ("B1", "free", 6, "window"),
        ("B2", "free", 1, "aisle")
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO seat_info (seat_id, status, distance, type)
        VALUES (?, ?, ?, ?)
    ''', seats)
    conn.commit()

# Get real-time seat status
def get_current_seat_status():
    cursor.execute("SELECT * FROM seat_info")
    seats = cursor.fetchall()
    return [
        {
            "seat_id": s[0],
            "status": s[1],
            "distance": s[2],
            "type": s[3]
        } for s in seats
    ]

# Store log
def save_log(data: Dict):
    data["create_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO booking_log (user_id, seat_id, operation_type, user_preference, create_time)
        VALUES (:user_id, :seat_id, :operation_type, :user_preference, :create_time)
    ''', data)
    conn.commit()
    return {"code": 200, "msg": "Log stored successfully"}

# Initialize
create_tables()
init_seat_data()