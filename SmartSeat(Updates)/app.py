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
        "type": user_type  # 将用户类型保存到 users.json
    }
    write_json(USERS_FILE, users)
    return jsonify({"success": True, "msg": "Account created successfully"})


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


# Get all reservations (老师端使用)
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
