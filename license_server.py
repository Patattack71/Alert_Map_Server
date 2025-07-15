from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = "licenses.db"  # <-- Correct variable name here

@app.route("/verify", methods=["GET", "POST"])
def verify():
    key = request.values.get("key")
    machine = request.values.get("machine")

    if not key or not machine:
        return jsonify({"valid": False, "error": "Missing key or machine"}), 400

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.execute("SELECT machine_id FROM licenses WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()

        if row:
            stored_machine = row[0]
            if stored_machine == "" or stored_machine == machine:
                # Bind the machine if not already bound
                if stored_machine == "":
                    conn = sqlite3.connect(DB_FILE)
                    conn.execute("UPDATE licenses SET machine_id = ? WHERE key = ?", (machine, key))
                    conn.commit()
                    conn.close()
                return jsonify({"valid": True})
        
        return jsonify({"valid": False, "error": "Invalid license key or machine ID"})

    except Exception as e:
        return jsonify({"valid": False, "error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
