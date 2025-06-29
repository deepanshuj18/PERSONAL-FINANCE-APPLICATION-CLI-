import shutil
import os
import sqlite3

DB_PATH = "finance.db"  # Default for real use

def get_connection():
    return sqlite3.connect(DB_PATH)


DB_FILE = 'finance.db'
BACKUP_DIR = 'backups'

def backup_database():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    backup_name = os.path.join(BACKUP_DIR, f"backup_{DB_FILE}")
    try:
        shutil.copy(DB_FILE, backup_name)
        print(f"✅ Backup created at {backup_name}")
    except FileNotFoundError:
        print("❌ Database file not found for backup.")

def restore_database():
    backup_path = os.path.join(BACKUP_DIR, f"backup_{DB_FILE}")
    if os.path.exists(backup_path):
        try:
            shutil.copy(backup_path, DB_FILE)
            print(f"✅ Database restored from {backup_path}")
        except Exception as e:
            print("❌ Restore failed:", e)
    else:
        print("❌ No backup file found.")
