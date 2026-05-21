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
            on_scene_dttm TEXT,
            actual_response_time_seconds REAL,
            UNIQUE(unit_id, received_dttm)
        )
    """)

    connection.commit()
    connection.close()


def insert_prediction(unit_id, received_dttm, predicted_response_time_seconds):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO predictions (
            unit_id,
            received_dttm,
            predicted_response_time_seconds
        )
        VALUES (?, ?, ?)
    """, (unit_id, received_dttm, predicted_response_time_seconds))

    connection.commit()
    connection.close()


def get_prediction(unit_id, received_dttm):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT unit_id, received_dttm, predicted_response_time_seconds
        FROM predictions
        WHERE unit_id = ? AND received_dttm = ?
    """, (unit_id, received_dttm))

    row = cursor.fetchone()
    connection.close()

    return row


def update_actual_response(unit_id, received_dttm, on_scene_dttm, actual_response_time_seconds):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE predictions
        SET on_scene_dttm = ?,
            actual_response_time_seconds = ?
        WHERE unit_id = ? AND received_dttm = ?
    """, (
        on_scene_dttm,
        actual_response_time_seconds,
        unit_id,
        received_dttm
    ))

    connection.commit()
    updated_rows = cursor.rowcount
    connection.close()

    return updated_rows