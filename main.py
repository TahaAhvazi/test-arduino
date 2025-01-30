from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

init_db()

# Endpoint to receive and store data via GET method
@app.route("/message", methods=["GET"])
def receive_message():
    try:
        message = request.args.get("message")
        if not message:
            return jsonify({"error": "Message parameter is required"}), 400
        
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (message) VALUES (?)",
            (message,),
        )
        conn.commit()
        conn.close()
        return "", 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Endpoint to retrieve stored data
@app.route("/messages", methods=["GET"])
def get_messages():
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, message, timestamp FROM messages")
        rows = cursor.fetchall()
        conn.close()
        return jsonify({"data": rows}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
