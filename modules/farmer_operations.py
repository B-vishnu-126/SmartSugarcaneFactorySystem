import sqlite3
import os
import sys

# Detect the correct base path (works after packaging)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Path to database file
DB_PATH = os.path.join(BASE_DIR, "database", "farmers.db")

# Ensure database folder exists
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)

print("📂 Using database file:", DB_PATH)


# ------------------------------------------------------------
# 🧩 Function 1: Add Farmer
# ------------------------------------------------------------
def add_farmer(name, phone, village):
    """Add a new farmer record to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Ensure farmers table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmers (
                farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                village TEXT
            )
        """)

        cursor.execute(
            "INSERT INTO farmers (name, phone, village) VALUES (?, ?, ?)",
            (name, phone, village)
        )
        conn.commit()
        print(f"✅ Farmer '{name}' added successfully!")
    except Exception as e:
        print("❌ Error adding farmer:", e)
    finally:
        conn.close()


# ------------------------------------------------------------
# 🧩 Function 2: View Farmers
# ------------------------------------------------------------
def view_farmers():
    """Return all farmer records as a list of tuples."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Ensure table exists before querying
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmers (
                farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                village TEXT
            )
        """)

        cursor.execute("SELECT * FROM farmers ORDER BY farmer_id DESC")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print("❌ Error fetching farmers:", e)
        return []
    finally:
        conn.close()


# ------------------------------------------------------------
# 🧩 Function 3: Delete Farmer
# ------------------------------------------------------------
def delete_farmer(farmer_id):
    """Delete a farmer record by ID."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM farmers WHERE farmer_id = ?", (farmer_id,))
        conn.commit()
        print(f"🗑️ Farmer ID {farmer_id} deleted successfully!")
    except Exception as e:
        print("❌ Error deleting farmer:", e)
    finally:
        conn.close()
