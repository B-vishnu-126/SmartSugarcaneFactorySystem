import sqlite3
import bcrypt
import os

# 🧭 Locate your database
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
DB_PATH = os.path.join(BASE_DIR, "database", "farmers.db")

# Make sure the database folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 🧩 Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password BLOB NOT NULL,
    role TEXT DEFAULT 'admin'
)
""")

# 🧩 Create a default admin account
default_username = "admin"
default_password = "12345"

# Hash password using bcrypt
hashed = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())

try:
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (default_username, hashed, "admin")
    )
    print("✅ Default admin user created (username: admin, password: 12345)")
except sqlite3.IntegrityError:
    print("ℹ️ Admin user already exists.")

# Save and close
conn.commit()
conn.close()
