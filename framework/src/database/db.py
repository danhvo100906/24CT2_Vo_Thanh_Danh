import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'chatbot.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()

    # Tạo sẵn 1 tài khoản admin mặc định nếu chưa có
    cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
    if cursor.fetchone() is None:
        hashed_pw = generate_password_hash('admin123')
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ('admin', hashed_pw, 'admin')
        )
        conn.commit()
        print("Đã tạo tài khoản admin mặc định (username: admin / password: admin123)")

    conn.close()


def create_user(username, password, role='user'):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = generate_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_pw, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        return dict(user)
    return None


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    return [dict(u) for u in users]