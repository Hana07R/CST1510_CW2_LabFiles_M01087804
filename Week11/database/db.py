import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "platform.db")


def connect_db():
    return sqlite3.connect(DB_PATH)


def init_users_table():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_users_table()
