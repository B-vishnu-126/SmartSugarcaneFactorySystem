import sqlite3
import bcrypt
import os

# 🧭 Locate your main database
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "farmers.db")

def verify_user(username, password):
    """
    Verify username and password from the database.
    Returns:
        (True, role) if valid
        (False, error_message) if invalid
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch stored hash and role
        cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return False, "User not found"

        stored_hash, role = user

        # bcrypt.checkpw expects bytes, ensure conversion
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return True, role
        else:
            return False, "Invalid password"

    except Exception as e:
        return False, f"Database error: {e}"
