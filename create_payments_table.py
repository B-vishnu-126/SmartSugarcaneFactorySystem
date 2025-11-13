import sqlite3

# Connect to your existing database
# (If it doesn't exist yet, it will be created automatically)
conn = sqlite3.connect("database/farmers.db")
cursor = conn.cursor()

# Create the payments table if not already created
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    total_weight REAL,
    rate_per_ton REAL,
    deductions REAL DEFAULT 0,
    total_amount REAL,
    payment_date TEXT,
    FOREIGN KEY(farmer_id) REFERENCES farmers(farmer_id)
)
""")

# Save changes and close
conn.commit()
conn.close()

print("Payments table created successfully!")
