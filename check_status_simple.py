import sqlite3

conn = sqlite3.connect('data/leads.db')
cursor = conn.cursor()

print("--- EMAIL STATUS REPORT ---")
cursor.execute("SELECT id, company, email, status, sent_at FROM leads")
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]} | Status: {row[3]} | Email: {row[2]}")

conn.close()
