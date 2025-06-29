import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3
import pytest
import budget
from budget import set_budget, check_budget_warning, DB_PATH as ORIGINAL_DB_PATH
import gc
import time

TEST_DB = "test_budget.db"

@pytest.fixture(autouse=True)
def setup(monkeypatch):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    # Create test DB with necessary tables
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT,
            amount REAL,
            month TEXT,
            year TEXT,
            UNIQUE(user_id, category, month, year)
        )
    """)

    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            category TEXT,
            amount REAL,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()

    monkeypatch.setattr(budget, "DB_PATH", TEST_DB)
    monkeypatch.setattr(budget, "DB", TEST_DB)
    yield

    try:
        os.remove(TEST_DB)
    except PermissionError:
        time.sleep(1)
        gc.collect()
        os.remove(TEST_DB)

def test_budget_warning_triggered(capfd):
    user_id = 1
    set_budget(user_id, "food", 500, "06", "2025")

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (user_id, type, category, amount, date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, "expense", "food", 600, "2025-06-15"))
    conn.commit()
    conn.close()

    check_budget_warning(user_id, "food", "06", "2025")
    out, _ = capfd.readouterr()
    assert "Budget Exceeded" in out

def test_budget_within_limit(capfd):
    user_id = 1
    set_budget(user_id, "transport", 300, "06", "2025")

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (user_id, type, category, amount, date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, "expense", "transport", 200, "2025-06-10"))
    conn.commit()
    conn.close()

    check_budget_warning(user_id, "transport", "06", "2025")
    out, _ = capfd.readouterr()
    assert "within budget" in out
