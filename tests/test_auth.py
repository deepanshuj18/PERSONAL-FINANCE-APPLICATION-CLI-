import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import sqlite3
import time
import pytest
from auth import register, login, DB_PATH as ORIGINAL_DB_PATH
import auth
import gc

TEST_DB = "test_auth.db"

@pytest.fixture(autouse=True)
def setup_and_teardown(monkeypatch):
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            time.sleep(1)
            os.remove(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    monkeypatch.setattr(auth, "DB_PATH", TEST_DB)
    yield

    time.sleep(1)
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            time.sleep(1)
            os.remove(TEST_DB)

def test_register_success():
    assert register("testuser1", "password123") is True

def test_register_duplicate_username():
    register("testuser1", "password123")
    assert register("testuser1", "newpass") is False

def test_login_success():
    register("testuser2", "password123")
    assert login("testuser2", "password123") is not False

def test_login_invalid_password():
    register("secureuser", "securepass")
    user_id = login("secureuser", "wrongpass")
    assert user_id is False