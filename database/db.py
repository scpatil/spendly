import sqlite3
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

DB_PATH = "spendly.db"

CATEGORIES = [
    "Food", "Transport", "Bills", "Health",
    "Entertainment", "Shopping", "Other",
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    today = datetime.now()
    sample_expenses = [
        (user_id, 450.00, "Bills", (today - timedelta(days=2)).strftime("%Y-%m-%d"), "Electricity bill"),
        (user_id, 320.50, "Food", (today - timedelta(days=1)).strftime("%Y-%m-%d"), "Groceries"),
        (user_id, 150.00, "Transport", (today - timedelta(days=4)).strftime("%Y-%m-%d"), "Cab fare"),
        (user_id, 899.00, "Health", (today - timedelta(days=6)).strftime("%Y-%m-%d"), "Pharmacy"),
        (user_id, 599.00, "Entertainment", (today - timedelta(days=3)).strftime("%Y-%m-%d"), "Movie tickets"),
        (user_id, 1200.00, "Shopping", (today - timedelta(days=8)).strftime("%Y-%m-%d"), "New shoes"),
        (user_id, 75.00, "Other", (today - timedelta(days=5)).strftime("%Y-%m-%d"), "Misc"),
        (user_id, 210.00, "Food", (today - timedelta(days=10)).strftime("%Y-%m-%d"), "Dinner out"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )
    conn.commit()
    conn.close()
