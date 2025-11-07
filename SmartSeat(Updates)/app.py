from flask import Flask, request, jsonify, send_from_directory
import json, os, time

# --- Flask setup ---
app = Flask(__name__, static_folder="static", static_url_path="")

# --- Data paths ---
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
SEATS_FILE = os.path.join(DATA_DIR, "seats.json")
RES_FILE = os.path.join(DATA_DIR, "reservations.json")


# --- Helpers ---
def read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# --- Serve HTML pages ---
@app.route("/")
def home():
    return send_from_directory("static", "login.html")


@app.route("/dashboard")
def dashboard():
    return send_from_directory("static", "dashboard.html")


@app.route("/select_building")
def select_building():
    return send_from_directory("static", "select_building.html")


@app.route("/select_seat")
def select_seat():
    return send_from_directory("static", "select_seat.html")


@app.route("/reservation_status")
def reservation_status():
    return send_from_directory("static", "reservation_status.html")


@app.route("/success")
def success():
    return send_from_directory("static", "success.html")


@app.route("/contact")
def contact_page():
    return send_from_directory("static", "contact.html")


@app.route("/teacher_dashboard")
def teacher_dashboard():
    return send_from_directory("static", "teacher_dashboard.html")


# --- API endpoints ---

# Sign up
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    users = read_json(USERS_FILE)

    # verify email
    email = data["email"]
    if not (email.startswith("S") or email.startswith("T")):
        return jsonify({"success": False, "msg": "the start of Email account is (student)S or (Teacher)T."})

    if email in users:
        return jsonify({"success": False, "msg": "Email already registered"})

    # identify user_type
    user_type = "student" if email.startswith("S") else "teacher"

    users[email] = {
        "password": data["password"],
        "name": data.get("name", ""),
        "type": user_type
    }
    write_json(USERS_FILE, users)
    return jsonify({"success": True, "msg": "Account created successfully"})

# --- Attendance helpers (non-breaking) ---
def _attendance_counts(room_seats):
    empty = on_time = late = 0
    for s in room_seats:
        if "state" in s:
            if s["state"] == 0:
                empty += 1
            elif s["state"] == 1:
                on_time += 1
            elif s["state"] == 2:
                late += 1
        else:
            if s.get("status") == "occupied":
                on_time += 1
            else:
                empty += 1
    total = len(room_seats)
    return empty, on_time, late, total

@app.route("/api/room_stats/<room_id>")
def room_stats(room_id):
    all_seats = read_json(SEATS_FILE)
    room_seats = all_seats.get(room_id, [])
    empty, on_time, late, total = _attendance_counts(room_seats)
    if total == 0:
        return jsonify({
            "room": room_id,
            "total": 0,
            "counts": {"empty": 0, "on_time": 0, "late": 0},
            "rates": {"occupancy": 0.0, "absence": 0.0}
        })
    occupancy = round(on_time / total, 4)
    absence = round(empty / total, 4)
    return jsonify({
        "room": room_id,
        "total": total,
        "counts": {"empty": empty, "on_time": on_time, "late": late},
        "rates": {"occupancy": occupancy, "absence": absence}
    })

@app.route("/api/attendance", methods=["POST"])
def update_attendance():
    data = request.json
    room_id = data["room"]
    updates = data.get("updates", [])
    all_seats = read_json(SEATS_FILE)
    room_seats = all_seats.get(room_id, [])

    idx = {s["code"]: i for i, s in enumerate(room_seats) if "code" in s}
    changed = 0
    for u in updates:
        code = u["code"]
        state = int(u["state"])
        if code in idx and state in (0, 1, 2):
            room_seats[idx[code]]["state"] = state
            changed += 1

    all_seats[room_id] = room_seats
    write_json(SEATS_FILE, all_seats)
    return jsonify({"success": True, "updated": changed})

# Login
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    users = read_json(USERS_FILE)
    email = data["email"]
    user = users.get(email)

    if not user or user["password"] != data["password"]:
        return jsonify({"success": False, "msg": "Incorrect email or password"})

    return jsonify({
        "success": True,
        "user": {
            "email": email,
            "name": user["name"],
            "type": user.get("type", "student")  # 使用 user.get 避免 KeyError
        }
    })


# Get seats
@app.route("/api/seats/<room_id>")
def get_seats(room_id):
    seats = read_json(SEATS_FILE).get(room_id, [])
    return jsonify(seats)


# Reserve seats
@app.route("/api/reserve", methods=["POST"])
def reserve():
    data = request.json
    room_id, seats, user = data["room"], data["seats"], data["user"]
    all_seats = read_json(SEATS_FILE)
    room_seats = all_seats.get(room_id, [])

    for s in seats:
        seat = next((x for x in room_seats if x["code"] == s), None)
        if not seat or seat["status"] == "occupied":
            return jsonify({"success": False, "msg": f"Seat {s} is already occupied"})

    for s in room_seats:
        if s["code"] in seats:
            s["status"] = "occupied"
    all_seats[room_id] = room_seats
    write_json(SEATS_FILE, all_seats)

    reservations = read_json(RES_FILE)
    reservations.setdefault(user["email"], []).append({
        "room": room_id,
        "seats": seats,
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    write_json(RES_FILE, reservations)
    return jsonify({"success": True, "msg": "Reservation successful"})


# Get user reservations
@app.route("/api/my_reservations/<email>")
def my_reservations(email):
    reservations = read_json(RES_FILE).get(email, [])
    return jsonify(reservations)


# Get all reservations (Teacher terminal usage)
@app.route("/api/all_reservations")
def all_reservations():
    reservations = read_json(RES_FILE)
    return jsonify(reservations)


# Contact form
@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.json
    print(" New contact message:", data)
    return jsonify({"success": True, "msg": "Message received successfully"})


# --- Run the app ---
if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)
