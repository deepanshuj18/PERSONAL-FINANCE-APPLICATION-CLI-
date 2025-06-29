import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import pytest
from finance import add_transaction, DB_PATH as ORIGINAL_DB_PATH
from reports import monthly_report, yearly_report
import finance
import gc,time,reports


TEST_DB = "test_reports.db"

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

    import finance, reports  # ⬅ Needed if monkeypatch used below
    monkeypatch.setattr(finance, "DB_PATH", TEST_DB)
    monkeypatch.setattr(reports, "DB_PATH", TEST_DB)

    yield

    time.sleep(0.5)
    for i in range(3):
        try:
            os.remove(TEST_DB)
            break
        except PermissionError:
            time.sleep(1)
            gc.collect()



def test_monthly_report(capsys):
    user_id = 1
    add_transaction(user_id, "income", "salary", 5000, "monthly salary")
    monthly_report(user_id, "06", "2025")
    out, _ = capsys.readouterr()

    assert "Monthly Report for 06/2025" in out
    assert "Total Income: ₹5000.00" in out
    assert "Total Expenses: ₹0.00" in out
    assert "Net Savings: ₹5000.00" in out


def test_yearly_report(capsys):
    user_id = 1
    add_transaction(user_id, "income", "bonus", 10000, "yearly bonus")
    yearly_report(user_id, "2025")
    out, _ = capsys.readouterr()

    assert "Yearly Report for 2025" in out
    assert "Total Income: ₹10000.00" in out
    assert "Total Expenses: ₹0.00" in out
    assert "Net Savings: ₹10000.00" in out
