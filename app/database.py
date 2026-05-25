import os
import sqlite3
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "predictions.db"

DATABASE_URL = os.getenv("DATABASE_URL")


def using_postgres():
    return DATABASE_URL is not None and DATABASE_URL != ""


def get_connection():
    if using_postgres():
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    if using_postgres():
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                unit_id TEXT NOT NULL,
                received_dttm TEXT NOT NULL,
                predicted_response_time_seconds DOUBLE PRECISION NOT NULL,
                on_scene_dttm TEXT,
                actual_response_time_seconds DOUBLE PRECISION,
                UNIQUE(unit_id, received_dttm)
            )
        """)
    else:
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

    if using_postgres():
        cursor.execute("""
            INSERT INTO predictions (
                unit_id,
                received_dttm,
                predicted_response_time_seconds
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (unit_id, received_dttm)
            DO UPDATE SET
                predicted_response_time_seconds = EXCLUDED.predicted_response_time_seconds
        """, (unit_id, received_dttm, predicted_response_time_seconds))
    else:
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

    if using_postgres():
        cursor.execute("""
            SELECT unit_id, received_dttm, predicted_response_time_seconds
            FROM predictions
            WHERE unit_id = %s AND received_dttm = %s
        """, (unit_id, received_dttm))

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return (
            row["unit_id"],
            row["received_dttm"],
            row["predicted_response_time_seconds"],
        )

    cursor.execute("""
        SELECT unit_id, received_dttm, predicted_response_time_seconds
        FROM predictions
        WHERE unit_id = ? AND received_dttm = ?
    """, (unit_id, received_dttm))

    row = cursor.fetchone()
    connection.close()

    return row


def update_actual_response(
    unit_id,
    received_dttm,
    on_scene_dttm,
    actual_response_time_seconds,
):
    connection = get_connection()
    cursor = connection.cursor()

    if using_postgres():
        cursor.execute("""
            UPDATE predictions
            SET on_scene_dttm = %s,
                actual_response_time_seconds = %s
            WHERE unit_id = %s AND received_dttm = %s
        """, (
            on_scene_dttm,
            actual_response_time_seconds,
            unit_id,
            received_dttm,
        ))
    else:
        cursor.execute("""
            UPDATE predictions
            SET on_scene_dttm = ?,
                actual_response_time_seconds = ?
            WHERE unit_id = ? AND received_dttm = ?
        """, (
            on_scene_dttm,
            actual_response_time_seconds,
            unit_id,
            received_dttm,
        ))

    connection.commit()
    updated_rows = cursor.rowcount
    connection.close()

    return updated_rows