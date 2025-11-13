import sqlite3
import os

# path of (the database folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "farmers.db")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Farmer Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS farmers (
    farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    village TEXT
)
""")

# Deliveries Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    cane_weight REAL,
    rate_per_ton REAL,
    payment REAL,
    date TEXT,
    FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
)
""")

conn.commit()
conn.close()

print("Database & tables Created Successfully! at:",db_path)