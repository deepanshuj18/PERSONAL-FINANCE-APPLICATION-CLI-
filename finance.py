import sqlite3
from datetime import datetime


DB_PATH = "finance.db"  # Default for real use

def get_connection():
    return sqlite3.connect(DB_PATH)


def add_transaction(user_id, trans_type, category, amount, description=""):
    date = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
            INSERT INTO transactions (user_id, type, category, amount, date, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, trans_type, category, amount, date, description))
    conn.commit()
    print("✅ Transaction added successfully.")

def view_transactions(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
            SELECT id, type, category, amount, date, description
            FROM transactions
            WHERE user_id = ?
            ORDER BY date DESC
        ''', (user_id,))
    rows = cur.fetchall()
    print("\n📄 Your Transactions:")
    for row in rows:
            print(row)

def delete_transaction(user_id, transaction_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
            DELETE FROM transactions
            WHERE id = ? AND user_id = ?
        ''', (transaction_id, user_id))
    conn.commit()
    print("🗑️ Transaction deleted.")

def update_transaction(user_id, transaction_id, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
            UPDATE transactions
            SET amount = ?
            WHERE id = ? AND user_id = ?
        ''', (amount, transaction_id, user_id))
    conn.commit()
    print("✏️ Transaction updated.")
