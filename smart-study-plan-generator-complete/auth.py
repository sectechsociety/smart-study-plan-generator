from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection

def register_user(name, email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, datetime('now'))",
            (name, email, generate_password_hash(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id, name, password_hash FROM users WHERE email = ?",
        (email,)
    )
    user = cur.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        return {
            "user_id": user[0],
            "name": user[1]
        }
    return None
