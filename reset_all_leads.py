import sqlite3

conn = sqlite3.connect('data/leads.db')
cursor = conn.cursor()

cursor.execute("UPDATE leads SET status='new'")
print(f"✅ Reset {cursor.rowcount} leads back to 'new' status.")

conn.commit()
conn.close()
