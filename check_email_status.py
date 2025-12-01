import sqlite3

conn = sqlite3.connect('data/leads.db')
cursor = conn.cursor()

print("--- SENT EMAILS ---")
cursor.execute("SELECT id, company, email, status, sent_at FROM leads WHERE status='sent' OR status='failed'")
rows = cursor.fetchall()

if not rows:
    print("No emails sent yet.")
else:
    for row in rows:
        print(f"ID: {row[0]} | Company: {row[1]} | Status: {row[3]} | Time: {row[4]}")

conn.close()
