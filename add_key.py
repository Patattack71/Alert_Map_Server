# add_key.py
import sqlite3

key = "ABC123-DEF456-GHI789"  # Your test key

with sqlite3.connect("licenses.db") as conn:
    conn.execute("INSERT INTO licenses (key, machine_id) VALUES (?, ?)", (key, ""))
    conn.commit()
    print("License key added.")
