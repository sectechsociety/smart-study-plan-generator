import sqlite3
import json

DB_NAME = "study_planner.db"


# ---------------- CONNECTION ----------------
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# ---------------- CREATE TABLES ----------------
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # STUDY HISTORY TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS study_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        gpa REAL,
        target_gpa REAL,
        predicted_hours TEXT,
        timetable TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    conn.commit()
    conn.close()


# ---------------- SAVE STUDY PLAN ----------------
def save_study_history(user_id, gpa, target_gpa, learning_style, predicted_hours, timetable):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO study_history
    (user_id, gpa, target_gpa, predicted_hours, timetable)
    VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        gpa,
        target_gpa,
        json.dumps(predicted_hours),     # ✅ JSON
        json.dumps(timetable)            # ✅ JSON
    ))

    conn.commit()
    conn.close()


# ---------------- GET FULL HISTORY ----------------
def get_user_history(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT predicted_hours, timetable, created_at
    FROM study_history
    WHERE user_id = ?
    ORDER BY created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()

    return [
        (json.loads(p), json.loads(t), d)
        for p, t, d in rows
    ]


# ---------------- GET LATEST PLAN ----------------
def get_latest_study_plan(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT predicted_hours, timetable, created_at
    FROM study_history
    WHERE user_id = ?
    ORDER BY created_at DESC
    LIMIT 1
    """, (user_id,))

    row = cur.fetchone()
    conn.close()

    if row:
        predicted, timetable, date = row
        return json.loads(predicted), json.loads(timetable), date

    return None


# ---------------- DELETE HISTORY ----------------
def delete_user_history(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM study_history WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()


# ✅ AUTO INITIALIZE
init_db()
