from flask import (
    Flask, render_template, request, jsonify,
    redirect, url_for, session
)
from functools import wraps
from datetime import datetime
import json, os

app = Flask(__name__)
app.secret_key = "sudais-super-secret-key-change-in-production"

ADMIN_USERNAME = "Sudais"
ADMIN_PASSWORD = "Sudais@345"
MESSAGES_FILE  = "messages.json"

def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            return json.load(f)
    return []

def save_message(name, email, message):
    messages = load_messages()
    messages.append({
        "id":      len(messages) + 1,
        "name":    name,
        "email":   email,
        "message": message,
        "time":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read":    False
    })
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=2)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    data    = request.get_json()
    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    message = data.get("message", "").strip()
    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields are required."}), 400
    save_message(name, email, message)
    return jsonify({"success": True, "message": "Message received! I'll get back to you soon."})

@app.route("/admin")
def admin_root():
    return redirect(url_for("admin_login"))

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        data     = request.get_json(silent=True) or {}
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return jsonify({"success": True})
        return jsonify({"success": False, "error": "Invalid credentials"}), 401
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    messages = load_messages()
    unread   = sum(1 for m in messages if not m["read"])
    return render_template("admin_dashboard.html",
                           messages=messages, unread=unread, total=len(messages))

@app.route("/admin/messages")
@login_required
def admin_messages():
    return jsonify(load_messages())

@app.route("/admin/mark-read/<int:msg_id>", methods=["POST"])
@login_required
def mark_read(msg_id):
    messages = load_messages()
    for m in messages:
        if m["id"] == msg_id:
            m["read"] = True
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=2)
    return jsonify({"success": True})

@app.route("/admin/delete/<int:msg_id>", methods=["DELETE"])
@login_required
def delete_message(msg_id):
    messages = [m for m in load_messages() if m["id"] != msg_id]
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=2)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
