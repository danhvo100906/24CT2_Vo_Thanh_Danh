import sqlite3
import json

conn = sqlite3.connect('instance/studybot.db')
c = conn.cursor()
c.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
tables = c.fetchall()

print("=== SCHEMA ===")
for name, sql in tables:
    print(f"Table: {name}")
    print(sql)
    print("-" * 20)

print("=== COUNTS ===")
try:
    c.execute("SELECT count(*) FROM users")
    print("Total users:", c.fetchone()[0])
    c.execute("SELECT count(*) FROM users WHERE role='student'")
    print("Total students:", c.fetchone()[0])
    c.execute("SELECT count(*) FROM users WHERE role='admin'")
    print("Total admins:", c.fetchone()[0])
    
    c.execute("SELECT student_code, count(*) c FROM users WHERE role='student' GROUP BY student_code HAVING c > 1")
    dups = c.fetchall()
    print("Duplicate student_codes:", dups)
except Exception as e:
    print("Error getting counts:", e)

conn.close()
