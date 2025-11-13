import sqlite3
from datetime import datetime
import os, sys

# ✅ Detect correct base path (works in both dev & packaged app)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DB_PATH = os.path.join(BASE_DIR, "database", "farmers.db")

# ✅ Ensure folders exist
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "exports"), exist_ok=True)

print("📂 Using database file:", DB_PATH)

def calculate_payments(rate_per_ton):
    """Calculate and record payments for all farmers."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # ✅ Ensure tables exist
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER,
                total_weight REAL,
                rate_per_ton REAL,
                deductions REAL,
                total_amount REAL,
                payment_date TEXT
            )
        """)

        # ✅ Get all farmers
        cursor.execute("SELECT farmer_id, name FROM farmers")
        farmers = cursor.fetchall()
        if not farmers:
            print("⚠️ No farmers found. Add some farmers first.")
            return

        # ✅ Process each farmer
        for farmer_id, name in farmers:
            cursor.execute("""
                SELECT SUM(cane_weight) FROM deliveries
                WHERE farmer_id = ?
            """, (farmer_id,))
            total_weight = cursor.fetchone()[0]

            if total_weight:
                deductions = 50  # Flat deduction example
                total_amount = (total_weight * rate_per_ton) - deductions

                cursor.execute("""
                    INSERT INTO payments (
                        farmer_id, total_weight, rate_per_ton, deductions, total_amount, payment_date
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    farmer_id,
                    total_weight,
                    rate_per_ton,
                    deductions,
                    total_amount,
                    datetime.now().strftime("%Y-%m-%d")
                ))

                print(f"💰 Payment added for {name}: ₹{round(total_amount, 2)}")
            else:
                print(f"⚠️ No deliveries found for farmer: {name}")

        conn.commit()
        print("\n✅ All payments calculated and saved successfully!")

    except Exception as e:
        print("❌ Error calculating payments:", e)
    finally:
        conn.close()
