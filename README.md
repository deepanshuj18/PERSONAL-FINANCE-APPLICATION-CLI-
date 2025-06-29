# 💰 Personal Finance Management System (CLI-based)

A simple command-line application to help users manage their personal finances — including budget planning, transaction tracking, and generating monthly/yearly financial reports.

## 🚀 Features

- ✅ User Registration & Login
- 📊 Set Monthly Budgets
- ➕ Add, View, Update, Delete Transactions
- 📆 Monthly & Yearly Reports
- ⚠️ Budget Exceed Warnings
- ✅ All Unit Tests Passed with `pytest`

## 🏗️ Tech Stack

- Python 3.10
- SQLite
- `pytest` for testing
- CLI-based Interface

## 📁 Project Structure
PythonProject1/
├── main.py
├── auth.py
├── budget.py
├── finance.py
├── reports.py
├── utils.py
├── finance.db
├── requirements.txt
├── README.md
└── tests/
├── test_auth.py
├── test_budget.py
├── test_finance.py
└── test_reports.py

# Installation


git clone https://github.com/<your-username>/PythonProject1.git
cd PythonProject1
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Running the App

python main.py

# Run Tests
pytest -v

# Contributing
Pull requests are welcome. For major changes, please open an issue first.
# License
</details>

---

##  2. Create `requirements.txt` in PyCharm

1. Open the terminal inside PyCharm (bottom of the screen).
2. Make sure you're in the virtual environment (e.g., `.venv1`).
3. Run:

```bash
pip freeze > requirements.txt
If you want to manually edit, right-click the file → Edit, and paste:

pytest==8.4.1
Add more if you used other packages like bcrypt, colorama, etc.
