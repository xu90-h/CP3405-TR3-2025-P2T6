import sqlite3

# 连接数据库
conn = sqlite3.connect('classroom_seats.db', check_same_thread=False)
cursor = conn.cursor()

def init_db():
    """初始化7×7座位表和日志表"""
    # 座位状态表（7×7共49个座位）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seat_info (
            seat_id TEXT PRIMARY KEY,
            status TEXT DEFAULT "free"  -- free:空闲 booked:已订
        )
    ''')
    # 推荐日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommend_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            seat_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # 插入7×7座位数据（A1-G7）
    rows = ["A", "B", "C", "D", "E", "F", "G"]
    for row in rows:
        for col in range(1, 8):
            seat_id = f"{row}{col}"
            cursor.execute('INSERT OR IGNORE INTO seat_info (seat_id) VALUES (?)', (seat_id,))
    conn.commit()

def get_current_seat_status():
    """获取所有座位的当前状态"""
    cursor.execute('SELECT seat_id, status FROM seat_info')
    return [{"seat_id": row[0], "status": row[1]} for row in cursor.fetchall()]

def save_log(log_data):
    """保存推荐日志"""
    cursor.execute('''
        INSERT INTO recommend_logs (user_id, seat_id)
        VALUES (?, ?)
    ''', (log_data["user_id"], log_data["seat_id"]))
    conn.commit()

def reset_all_seats():
    """重置所有座位为空闲状态"""
    cursor.execute('UPDATE seat_info SET status = "free"')
    conn.commit()

# 初始化数据库
init_db()