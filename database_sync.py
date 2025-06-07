# database_sync.py
import sqlite3
import os

os.makedirs("logs", exist_ok=True)
DB_PATH = "logs/pepeprophet.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            timestamp TEXT,
            coin TEXT,
            price REAL,
            volume REAL,
            sentiment REAL,
            score REAL,
            action TEXT,
            confidence REAL,
            future_price REAL,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_signal(signal_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO signals (
            timestamp, coin, price, volume, sentiment, score,
            action, confidence, future_price, result
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, signal_data)
    conn.commit()
    conn.close()

# Initialize database on first import
init_db()
