from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    with sqlite3.connect("licenses.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS licenses (
                key TEXT PRIMARY KEY,
                machine_id TEXT
            )
        ''')

# API to verify license
@app.route("/verify", methods=["POST"])
def verify_license():
    data = request.get_json()
    key = data.get("key")
    machine = data.get("machine")

    if not key or not machine:
        return jsonify({"valid": False, "error": "Missing key or machine"}), 400

    with sqlite3.connect("licenses.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT machine_id FROM licenses WHERE key = ?", (key,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"valid": False, "error": "Key not found"}), 404
        elif result[0] == "" or result[0] == machine:
            if result[0] == "":
                cursor.execute("UPDATE licenses SET machine_id = ? WHERE key = ?", (machine, key))
                conn.commit()
            return jsonify({"valid": True}), 200
        else:
            return jsonify({"valid": False, "error": "Key used on another machine"}), 403

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
