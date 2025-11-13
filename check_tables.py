import sqlite3

conn = sqlite3.connect("database/farmers.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(deliveries)")
columns = cursor.fetchall()

print("📋 Columns in 'deliveries' table:")
for col in columns:
    print("-", col[1])

conn.close()
