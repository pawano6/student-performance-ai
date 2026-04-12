# database.py
import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT"))
    )

# ---------- CREATE TABLE ----------
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gender VARCHAR(50),
        race VARCHAR(50),
        parental VARCHAR(100),
        lunch VARCHAR(50),
        prep VARCHAR(50),
        math FLOAT,
        reading FLOAT,
        writing FLOAT,
        final_score FLOAT,
        level VARCHAR(20),
        risk VARCHAR(20),
        weak_subject VARCHAR(50),
        timestamp DATETIME
    )
    """)

    conn.commit()
    conn.close()

# ---------- INSERT ----------
def insert_prediction(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO predictions (
        gender, race, parental, lunch, prep,
        math, reading, writing,
        final_score, level, risk, weak_subject, timestamp
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["gender"],
        data["race"],
        data["parental"],
        data["lunch"],
        data["prep"],
        data["math"],
        data["reading"],
        data["writing"],
        data["final_score"],
        data["level"],
        data["risk"],
        data["weak_subject"],
        datetime.now()
    )

    cursor.execute(query, values)
    conn.commit()
    conn.close()

# ---------- FETCH ----------
def fetch_all():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows