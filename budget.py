import sqlite3

DB_PATH = "finance.db"
DB = DB_PATH  # Alias used in tests too

def get_connection():
    return sqlite3.connect(DB_PATH)

def set_budget(user_id, category, amount, month, year):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO budgets (user_id, category, month, year, amount)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, category, month, year)
            DO UPDATE SET amount = excluded.amount
        ''', (user_id, category, month, year, amount))
        conn.commit()
        print(f"✅ Budget set: ₹{amount} for '{category}' in {month}/{year}.")
    except Exception as e:
        print("❌ Error setting budget:", e)

def check_budget_warning(user_id, category, month, year):
    conn = get_connection()
    cur = conn.cursor()

    # Get total expenses
    cur.execute('''
        SELECT SUM(amount)
        FROM transactions
        WHERE user_id = ? AND type = 'expense' AND category = ?
              AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
    ''', (user_id, category, f"{int(month):02}", year))
    total_spent = cur.fetchone()[0] or 0.0

    # Get the budget
    cur.execute('''
        SELECT amount
        FROM budgets
        WHERE user_id = ? AND category = ? AND month = ? AND year = ?
    ''', (user_id, category, f"{int(month):02}", year))
    result = cur.fetchone()

    if result:
        budget_amount = result[0]
        if total_spent > budget_amount:
            print(f"⚠️ Budget Exceeded for '{category}': ₹{total_spent:.2f} spent, budget was ₹{budget_amount:.2f}")
        else:
            print(f"✅ You're within budget for '{category}'. Spent: ₹{total_spent:.2f}, Limit: ₹{budget_amount:.2f}")
    else:
        print(f"ℹ️ No budget set for '{category}' in {month}/{year}.")
