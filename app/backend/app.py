from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, os

app = Flask(__name__)
CORS(app)

DB = "/data/notes.db"

def init_db():
    os.makedirs("/data", exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS notes (text TEXT)")
    conn.close()

@app.route("/api/notes", methods=["GET"])
def get_notes():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT text FROM notes").fetchall()
    conn.close()
    return jsonify([r[0] for r in rows])

@app.route("/api/notes", methods=["POST"])
def add_note():
    data = request.json
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO notes VALUES (?)", (data["note"],))
    conn.commit()
    conn.close()
    return {"status": "saved"}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
