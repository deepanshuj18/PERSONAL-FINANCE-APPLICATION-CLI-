
import sqlite3

DB_PATH = "finance.db"  # Default for real use

def get_connection():
    return sqlite3.connect(DB_PATH)


def monthly_report(user_id, month, year):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
            SELECT type, SUM(amount) 
            FROM transactions 
            WHERE user_id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY type
        ''', (user_id, f"{int(month):02}", str(year)))
    results = cur.fetchall()

    income = sum(amount for t, amount in results if t == "income")
    expense = sum(amount for t, amount in results if t == "expense")
    savings = income - expense

    print(f"\n📆 Monthly Report for {month}/{year}")
    print(f"Total Income: ₹{income:.2f}")
    print(f"Total Expenses: ₹{expense:.2f}")
    print(f"Net Savings: ₹{savings:.2f}")

def yearly_report(user_id, year):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
            SELECT type, SUM(amount) 
            FROM transactions 
            WHERE user_id = ? AND strftime('%Y', date) = ?
            GROUP BY type
        ''', (user_id, str(year)))
    results = cur.fetchall()

    income = sum(amount for t, amount in results if t == "income")
    expense = sum(amount for t, amount in results if t == "expense")
    savings = income - expense

    print(f"\n📆 Yearly Report for {year}")
    print(f"Total Income: ₹{income:.2f}")
    print(f"Total Expenses: ₹{expense:.2f}")
    print(f"Net Savings: ₹{savings:.2f}")
