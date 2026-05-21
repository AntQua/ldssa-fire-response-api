import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "predictions.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_id TEXT NOT NULL,
            received_dttm TEXT NOT NULL,
            predicted_response_time_seconds REAL NOT NULL,
            actual_response_time_seconds REAL,
            on_scene_dttm TEXT,
            UNIQUE(unit_id, received_dttm)
        )
    """)

    connection.commit()
    connection.close()