import sqlite3
import os
import sys

# ✅ Detect correct base path (works in both dev & packaged .exe/.app)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DB_PATH = os.path.join(BASE_DIR, "database", "farmers.db")

# ✅ Ensure folders exist
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "exports"), exist_ok=True)

print("📂 Using database file:", DB_PATH)

# ------------------------------------------------------------
# 🧩 Function 1: Add Delivery
# ------------------------------------------------------------
def add_delivery(farmer_id, cane_weight, rate_per_ton):
    """Add a delivery record linked to a farmer."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Ensure tables exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmers (
                farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                village TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deliveries (
                delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER,
                cane_weight REAL,
                rate_per_ton REAL,
                payment REAL,
                date TEXT
            )
        """)

        # Verify farmer exists
        cursor.execute("SELECT COUNT(*) FROM farmers WHERE farmer_id = ?", (farmer_id,))
        exists = cursor.fetchone()[0]
        if not exists:
            raise Exception(f"Farmer ID {farmer_id} does not exist.")

        # Calculate payment
        payment = cane_weight * rate_per_ton

        # Insert delivery
        cursor.execute("""
            INSERT INTO deliveries (farmer_id, cane_weight, rate_per_ton, payment, date)
            VALUES (?, ?, ?, ?, DATE('now'))
        """, (farmer_id, cane_weight, rate_per_ton, payment))

        conn.commit()
        print(f"✅ Delivery added successfully for Farmer ID {farmer_id}")

    except Exception as e:
        print("❌ Error adding delivery:", e)
    finally:
        if conn:
            conn.close()


# ------------------------------------------------------------
# 🧩 Function 2: View Deliveries
# ------------------------------------------------------------
def view_deliveries():
    """Return all deliveries joined with farmer details."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Ensure table exists (prevents crash)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deliveries (
                delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER,
                cane_weight REAL,
                rate_per_ton REAL,
                payment REAL,
                date TEXT
            )
        """)

        query = """
        SELECT 
            d.delivery_id,
            f.name,
            f.village,
            d.cane_weight,
            d.rate_per_ton,
            d.payment,
            d.date
        FROM deliveries d
        JOIN farmers f ON d.farmer_id = f.farmer_id
        ORDER BY d.delivery_id DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"✅ {len(rows)} Deliveries fetched.")
        return rows

    except Exception as e:
        print("❌ Error fetching deliveries:", e)
        return []
    finally:
        if conn:
            conn.close()


# ------------------------------------------------------------
# 🧩 Function 3: Delete Delivery
# ------------------------------------------------------------
def delete_delivery(delivery_id):
    """Delete a delivery by ID."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM deliveries WHERE delivery_id = ?", (delivery_id,))
        conn.commit()
        print(f"🗑️ Delivery ID {delivery_id} deleted successfully!")
    except Exception as e:
        print("❌ Error deleting delivery:", e)
    finally:
        conn.close()
