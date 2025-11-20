import sqlite3

# Connect to the database
conn = sqlite3.connect('classroom_seats.db', check_same_thread=False)
cursor = conn.cursor()

def init_db():
    """Initialize a 7×7 seating chart and log table"""
    # Seat Status Table (7×7, total of 49 seats)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seat_info (
            seat_id TEXT PRIMARY KEY,
            status TEXT DEFAULT "free"  -- free:空闲 booked:已订
        )
    ''')
    # Recommended Log Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommend_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            seat_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Insert 7×7 seating data (A1-G7)
    rows = ["A", "B", "C", "D", "E", "F", "G"]
    for row in rows:
        for col in range(1, 8):
            seat_id = f"{row}{col}"
            cursor.execute('INSERT OR IGNORE INTO seat_info (seat_id) VALUES (?)', (seat_id,))
    conn.commit()

def get_current_seat_status():
    """Get the current status of all seats"""
    cursor.execute('SELECT seat_id, status FROM seat_info')
    return [{"seat_id": row[0], "status": row[1]} for row in cursor.fetchall()]

def save_log(log_data):
    """Save recommendation log"""
    cursor.execute('''
        INSERT INTO recommend_logs (user_id, seat_id)
        VALUES (?, ?)
    ''', (log_data["user_id"], log_data["seat_id"]))
    conn.commit()

def reset_all_seats():
    """Reset all seats to available"""
    cursor.execute('UPDATE seat_info SET status = "free"')
    conn.commit()

# Initialize the database
init_db()