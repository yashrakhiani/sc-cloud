import sqlite3

db_path = 'data/leads.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE leads ADD COLUMN sent_at TEXT")
    print("✅ Added 'sent_at' column successfully")
except sqlite3.OperationalError as e:
    print(f"⚠️  Column might already exist: {e}")

conn.commit()
conn.close()
