from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3

# Initialize FastAPI app
app = FastAPI()

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
@app.get("/message")
async def receive_message(message: str = Query(...)):
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (message) VALUES (?)",
            (message,),
        )
        conn.commit()
        conn.close()
        return ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Endpoint to retrieve stored data
@app.get("/messages")
def get_messages():
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, message, timestamp FROM messages")
        rows = cursor.fetchall()
        conn.close()
        return {"data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
