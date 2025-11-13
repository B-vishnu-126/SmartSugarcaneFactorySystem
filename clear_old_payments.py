import sqlite3

conn = sqlite3.connect("database/farmers.db")
cur = conn.cursor()

cur.execute("DELETE FROM payments")
conn.commit()
conn.close()

print("✅ Old payments deleted successfully!")
