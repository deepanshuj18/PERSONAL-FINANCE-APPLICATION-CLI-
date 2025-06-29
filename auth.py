import sqlite3
from utils import hash_password

DB_PATH = "finance.db"  # Default for real use

def get_connection():
    return sqlite3.connect(DB_PATH)
def register(username, password):
    hashed_pw = hash_password(password)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            print("✅ Registration successful.")
            return True
    except sqlite3.IntegrityError:
        print("❌ Username already exists. Try a different one.")
        return False


def login(username, password):
    hashed_pw = hash_password(password)
    conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    user = cur.fetchone()
    if user:
        print(f"✅ Welcome back, {username}!")
        return user[0]  # return user_id
    else:
        print("❌ Invalid credentials.")
        return False
