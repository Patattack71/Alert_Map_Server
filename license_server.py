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
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    key = request.args.get('key') or request.form.get('key')
    machine = request.args.get('machine') or request.form.get('machine')

    if not key or not machine:
        return jsonify({"valid": False, "error": "Missing key or machine"}), 400

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM licenses WHERE key = ? AND (machine_id = '' OR machine_id = ?)", (key, machine))
    result = c.fetchone()
    conn.close()

    if result:
        # Optional: Lock this key to the machine
        if result[2] == '':
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("UPDATE licenses SET machine_id = ? WHERE key = ?", (machine, key))
            conn.commit()
            conn.close()

        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False, "error": "Invalid license key or machine ID"}), 403
