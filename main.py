from fastapi import FastAPI, HTTPException
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
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            temperature REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

init_db()

# Pydantic model for incoming data
class SensorData(BaseModel):
    latitude: float
    longitude: float
    temperature: float

# Endpoint to receive and store data
@app.post("/data")
async def receive_data(data: SensorData):
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sensor_data (latitude, longitude, temperature) VALUES (?, ?, ?)",
            (data.latitude, data.longitude, data.temperature),
        )
        conn.commit()
        conn.close()
        return {"message": "Data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Endpoint to retrieve stored data (optional)
@app.get("/data")
def get_data():
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, latitude, longitude, temperature, timestamp FROM sensor_data")
        rows = cursor.fetchall()
        conn.close()
        return {"data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
