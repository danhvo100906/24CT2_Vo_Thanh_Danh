import sqlite3
import os
import json

db_path = 'instance/studybot.db'
if not os.path.exists(db_path):
    print(f"File not found: {db_path}")
    exit(1)

print(f"Absolute path: {os.path.abspath(db_path)}")
print(f"File size: {os.path.getsize(db_path)} bytes")

conn = sqlite3.connect(db_path)
c = conn.cursor()

# B. Table inventory
print("\n--- TABLE INVENTORY ---")
c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = [row[0] for row in c.fetchall()]
for table in tables:
    print(table)

# C. Schema & D. Foreign Keys
print("\n--- SCHEMAS & FOREIGN KEYS ---")
for table in tables:
    print(f"Table: {table}")
    c.execute(f"PRAGMA table_info({table});")
    for col in c.fetchall():
        print("  Column:", col)
    c.execute(f"PRAGMA foreign_key_list({table});")
    fks = c.fetchall()
    if not fks:
        print("  Foreign Keys: NONE")
    else:
        for fk in fks:
            print("  Foreign Key:", fk)

# E. Account evidence
print("\n--- ACCOUNT EVIDENCE ---")
c.execute("SELECT COUNT(*) FROM users;")
print("Total users:", c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM users WHERE role='admin';")
print("Total admins:", c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM users WHERE role='student';")
print("Total students:", c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM users WHERE student_code IS NOT NULL;")
print("Users with student_code:", c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM users WHERE student_code IS NULL;")
print("Users without student_code:", c.fetchone()[0])

c.execute("SELECT id, username, student_code, role FROM users WHERE student_code IS NULL;")
null_code_users = c.fetchall()
print("Users with NULL student_code (legacy/extra):", null_code_users)

c.execute("SELECT COUNT(*) FROM users WHERE role='student' AND student_code LIKE '245122%' OR student_code LIKE '255122%' OR student_code LIKE '265122%';")
print("Students in valid cohorts (24/25/26 and major 5122):", c.fetchone()[0])

# F. Chat history
print("\n--- CHAT HISTORY ---")
c.execute("SELECT COUNT(*) FROM chat_messages;")
print("Total chat messages:", c.fetchone()[0])
c.execute("SELECT * FROM chat_messages LIMIT 1;")
print("Sample row:", c.fetchone())

# G. Feedback
print("\n--- FEEDBACK ---")
c.execute("SELECT COUNT(*) FROM feedbacks;")
print("Total feedbacks:", c.fetchone()[0])
c.execute("SELECT * FROM feedbacks LIMIT 1;")
print("Sample row:", c.fetchone())

conn.close()
