import sqlite3
import json

db = r"instance/studybot.db"
with open(r"docs/evidence/P1-002_EVIDENCE_FULL.txt", "w", encoding="utf-8") as out:
    def printf(msg=""): out.write(str(msg) + "\n")

    printf("DATABASE: " + db)

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    printf("\n=== SQLITE MASTER (TABLES & INDEXES) ===")
    for row in cur.execute("SELECT type, name, tbl_name, sql FROM sqlite_master WHERE type IN ('table','index') ORDER BY type, name"):
        printf(row)

    tables = ["users", "subjects", "materials", "knowledge_items", "chat_messages", "feedbacks"]
    for table in tables:
        printf(f"\n=== PRAGMA table_info('{table}') ===")
        for row in cur.execute(f"PRAGMA table_info('{table}')"):
            printf(row)

        printf(f"\n=== PRAGMA foreign_key_list('{table}') ===")
        for row in cur.execute(f"PRAGMA foreign_key_list('{table}')"):
            printf(row)

        printf(f"\n=== PRAGMA index_list('{table}') ===")
        indexes = cur.execute(f"PRAGMA index_list('{table}')").fetchall()
        for row in indexes:
            printf(row)
            idx_name = row[1]
            printf(f"--- PRAGMA index_info('{idx_name}') ---")
            for i_row in cur.execute(f"PRAGMA index_info('{idx_name}')"):
                printf("    " + str(i_row))

    printf("\n=== USER COUNTS ===")
    cur.execute("SELECT COUNT(*) FROM users;")
    printf(f"Total users: {cur.fetchone()[0]}")

    printf("\nRole Counts:")
    for row in cur.execute("SELECT role, COUNT(*) FROM users GROUP BY role ORDER BY role;"):
        printf(row)

    printf("\n=== DUPLICATE CHECK ===")
    cur.execute("SELECT student_code, COUNT(*) FROM users WHERE role='student' GROUP BY student_code HAVING COUNT(*) > 1;")
    dups = cur.fetchall()
    if not dups:
        printf("Duplicate valid/assigned student codes = 0")
    else:
        for d in dups: printf(d)

    printf("\n=== STUDENT ACCOUNT EXACT VERIFICATION ===")
    
    # Fetch all student codes
    cur.execute("SELECT student_code, id, username, full_name, role, status FROM users WHERE role='student';")
    all_students = cur.fetchall()
    
    # Separate students by cohort
    def check_cohort(year):
        expected = {f"{year}5122{i:04d}" for i in range(1, 301)}
        actual_codes = [s[0] for s in all_students if s[0] and s[0].startswith(f"{year}5122")]
        actual_set = set(actual_codes)
        printf(f"Cohort {year}:")
        printf(f"Expected count: {len(expected)}")
        printf(f"Actual count: {len(actual_codes)}")
        printf(f"Distinct count: {len(actual_set)}")
        printf(f"Missing: {len(expected - actual_set)}")
        printf(f"Duplicate: {len(actual_codes) - len(actual_set)}")

    check_cohort("24")
    check_cohort("25")
    check_cohort("26")

    printf("\n=== EXACT SET CHECK (ALL COHORTS) ===")
    expected_all = {f"{year}5122{i:04d}" for year in ("24", "25", "26") for i in range(1, 301)}
    
    actual_all_codes = [s[0] for s in all_students if s[0]]
    actual_all_set = set(actual_all_codes)
    
    printf(f"Expected valid student codes = {len(expected_all)}")
    
    # Any code in DB that matches expected format is valid
    valid_actual = actual_all_set.intersection(expected_all)
    printf(f"Actual valid student codes = {len(valid_actual)}")
    
    missing_all = expected_all - actual_all_set
    extra_all = actual_all_set - expected_all
    
    printf(f"Missing = {len(missing_all)}")
    printf(f"Duplicate = {len(actual_all_codes) - len(actual_all_set)}")
    printf(f"Invalid/Extra = {len(extra_all)}")

    printf("\n=== THREE EXTRA STUDENT ACCOUNTS ===")
    printf(f"Extra student rows = {len(extra_all)}")
    printf("Row output (id, student_code, username, full_name, role, status):")
    for s in all_students:
        if s[0] not in expected_all:
            # Print specific fields without password_hash
            printf(f"{s[1]} | {s[0]} | {s[2]} | {s[3]} | {s[4]} | {s[5]}")

    conn.close()
