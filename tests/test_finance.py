import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3
import pytest
from finance import add_transaction, update_transaction, delete_transaction, view_transactions, DB_PATH as ORIGINAL_DB_PATH
import finance
import gc
import time

TEST_DB = "test_finance.db"

@pytest.fixture(autouse=True)
def setup(monkeypatch):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            category TEXT,
            amount REAL,
            description TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

    monkeypatch.setattr(finance, "DB_PATH", TEST_DB)
    yield

    try:
        os.remove(TEST_DB)
    except PermissionError:
        time.sleep(1)
        gc.collect()  # NEW: force garbage collection
        os.remove(TEST_DB)


def test_add_and_view_transaction(capsys):
    user_id = 1
    add_transaction(user_id, "income", "freelance", 5000, "freelance job")
    view_transactions(user_id)
    out, _ = capsys.readouterr()
    assert "freelance" in out


def test_update_transaction(capsys):
    user_id = 1
    add_transaction(user_id, "expense", "food", 200, "lunch")

    # Get the inserted transaction's ID
    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("SELECT id FROM transactions WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
    transaction_id = cur.fetchone()[0]
    conn.close()

    # ✅ Correct usage with 3 arguments
    update_transaction(user_id, transaction_id, 300)

    out, _ = capsys.readouterr()
    assert "updated" in out.lower()

def test_delete_transaction(capfd):
    user_id = 1
    # First add a transaction
    add_transaction(user_id, "expense", "groceries", 200.0, "test delete")

    # Get the transaction ID
    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("SELECT id FROM transactions WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    assert row is not None
    trans_id = row[0]
    conn.close()

    # Now delete it
    delete_transaction(user_id, trans_id)
    out, _ = capfd.readouterr()
    assert "Transaction deleted" in out

    # Confirm it is deleted
    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE id = ?", (trans_id,))
    assert cur.fetchone() is None
    conn.close()