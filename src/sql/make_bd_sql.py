# create_db_sqlite3.py

import sqlite3

def init_db(db_filename: str = "app.db"):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Включаем поддержку внешних ключей (PRAGMA)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Таблица users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT NOT NULL UNIQUE,
        name TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        timezone TEXT
    );
    """)

    # 2. Таблица goals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        start_date DATE NOT NULL DEFAULT (DATE('now')),
        target_date DATE,
        status TEXT NOT NULL DEFAULT 'active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 3. Таблица strengths_weaknesses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS strengths_weaknesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('strength','weakness')),
        value TEXT NOT NULL,
        source TEXT NOT NULL CHECK(source IN ('self','gpt')) DEFAULT 'self',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 4. Таблица conversations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message_from TEXT NOT NULL CHECK(message_from IN ('user','bot')),
        message_text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        used_for_gpt INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 5. Таблица progress_entries
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        goal_id INTEGER NOT NULL,
        date DATE NOT NULL DEFAULT (DATE('now')),
        status TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(goal_id) REFERENCES goals(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("База данных и таблицы успешно созданы (через sqlite3).")

if __name__ == "__main__":
    init_db()
